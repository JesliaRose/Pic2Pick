from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

@app.route("/api/search", methods=["POST"])
def search():
    data = request.json
    search_query = data.get("product_name", "")

    flipkart_data = get_flipkart_data(search_query)
    amazon_data = get_amazon_data(search_query)

    return jsonify({
        "flipkart": flipkart_data,
        "amazon": amazon_data
    })

def get_flipkart_data(query):
    url = f"https://www.flipkart.com/search?q={query}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    product = soup.find("a", class_=["CGtC98", "WKTcLC", "VJA3rP"])
    if product:
        title = product.text.strip()
        link = "https://www.flipkart.com" + product["href"]
        price_tag = product.find_next("div", class_="Nx9bqj")
        price = price_tag.text.strip() if price_tag else "Price not found"
        return {"title": title, "price": price, "url": link}
    return {"title": "Not found", "price": "N/A", "url": ""}

def get_amazon_data(query):
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    product = soup.find("div", {"data-component-type": "s-search-result"})
    if product:
        title_tag = product.find("span", class_="a-size-medium")
        title = title_tag.text.strip() if title_tag else "Not found"
        price_tag = product.find("span", class_="a-price-whole")
        price = price_tag.text.strip() if price_tag else "Price not found"
        link_tag = product.find("a", class_="a-link-normal s-no-outline")
        link = "https://www.amazon.in" + link_tag["href"] if link_tag else ""
        return {"title": title, "price": price, "url": link}
    return {"title": "Not found", "price": "N/A", "url": ""}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
