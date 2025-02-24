from flask import Flask, request, jsonify
import os
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Limit detected text
def limit_words(text, max_words=10):
    words = text.split()
    return ' '.join(words[:max_words])

# Upload image to Imgur
def upload_to_imgur(image_path):
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    with open(image_path, "rb") as img:
        response = requests.post("https://api.imgur.com/3/upload", headers=headers, files={"image": img})
    if response.status_code == 200:
        return response.json()["data"]["link"]
    return None

# Get Flipkart product URL
def get_product_url(search_query):
    base_url = "https://www.flipkart.com/search"
    params = {"q": search_query}
    response = requests.get(base_url, headers=HEADERS, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        product_link = soup.find("a", class_=["CGtC98", "WKTcLC", "VJA3rP"])
        if product_link:
            return "https://www.flipkart.com" + product_link["href"]
    return None

# Scrape product details from Flipkart
def scrape_product_details(product_url):
    response = requests.get(product_url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("span", class_="VU-ZEz")
        price_tag = soup.find("div", class_="Nx9bqj")
        title = title_tag.text.strip() if title_tag else "Title not found"
        price = price_tag.text.strip() if price_tag else "Price not found"
        return title, price
    return None, None

# Get Amazon product price and link
def get_amazon_price(product_name):
    search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    response = requests.get(search_url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        for item in products:
            if item.find("span", string="Sponsored"):
                continue
            price_tag = item.find("span", class_="a-price-whole")
            link_tag = item.find("a", class_="a-link-normal s-no-outline")
            if price_tag and link_tag:
                price = price_tag.text.strip()
                link = "https://www.amazon.in" + link_tag["href"]
                return price, link
    return None, None

@app.route("/search", methods=["POST"])
def search():
    data = request.form
    product_name = data.get("product_name", "").strip()
    image = request.files.get("image")

    detected_text = None
    if image:
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        image.save(image_path)
        imgur_url = upload_to_imgur(image_path)
        if imgur_url:
            params = {"api_key": SERPAPI_KEY, "engine": "google_lens", "url": imgur_url}
            response = requests.get("https://serpapi.com/search.json", params=params)
            if response.status_code == 200:
                data = response.json()
                detected_text = limit_words(data.get("visual_matches", [{}])[0].get("title", "Text not found"))
                product_name = detected_text

    flipkart_url = get_product_url(product_name)
    flipkart_title, flipkart_price = scrape_product_details(flipkart_url) if flipkart_url else ("Not found", "N/A")
    amazon_price, amazon_link = get_amazon_price(product_name)

    return jsonify({
        "search_query": product_name,
        "flipkart": {"title": flipkart_title, "price": flipkart_price, "url": flipkart_url},
        "amazon": {"price": amazon_price, "url": amazon_link},
    })

if __name__ == "__main__":
    app.run(debug=True)
