from flask import Flask, request, jsonify
import os
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from model import predict_sentiment

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "static/uploads"
SERPAPI_KEY = "c35d90adf979c4384952b611ea040be9648b1a1eb67111880aec2798cb9ff126"
IMGUR_CLIENT_ID = "d561e5634adf419"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def limit_words(text, max_words=10):
    words = text.split()
    return ' '.join(words[:max_words])

def upload_to_imgur(image_path):
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    with open(image_path, "rb") as img:
        response = requests.post(
            "https://api.imgur.com/3/upload",
            headers=headers,
            files={"image": img}
        )
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        print("Imgur Upload Error:", response.text)
        return None

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

def scrape_product_details(product_url):
    response = requests.get(product_url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("span", class_="VU-ZEz")
        title = title_tag.text.strip() if title_tag else "Title not found"

        price_tag = soup.find("div", class_="Nx9bqj")
        price = price_tag.text.strip() if price_tag else "Price not found"

        reviews = []
        review_containers = soup.find_all('div', class_=['col EPCmJX', 'col EPCmJX MDcJkH']) 
        for container in review_containers:

            comment_element = container.find(['div', 'p'], class_=['z9E0IG', '_11pzQk'])
            comment = comment_element.get_text(strip=True) if comment_element else "No comment"
            reviews.append(comment)

        return title, price, reviews
    return "Product not found", None, []

def get_amazon_price(product_name):
    search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    response = requests.get(search_url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        for item in products:
            sponsored_tag = item.find("span", string="Sponsored")
            if sponsored_tag:
                continue
            price_tag = item.find("span", class_="a-price-whole")
            if price_tag:
                price = price_tag.text.strip()
            else:
                continue
            link_tag = item.find("a", class_="a-link-normal s-no-outline")
            product_link = "https://www.amazon.in" + link_tag["href"] if link_tag else "No link found"
            return price, product_link
    return None, None

@app.route("/search", methods=["POST"])
def search():
    data = request.form
    search_query = data.get("product_name", "").strip()
    detected_text = None

    if "image" in request.files:
        image = request.files["image"]
        if image.filename != "":
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(image_path)

            imgur_url = upload_to_imgur(image_path)
            if imgur_url:
                params = {
                    "api_key": SERPAPI_KEY,
                    "engine": "google_lens",
                    "url": imgur_url
                }
                response = requests.get("https://serpapi.com/search.json", params=params)
                if response.status_code == 200:
                    data = response.json()
                    if "visual_matches" in data and len(data["visual_matches"]) > 0:
                        detected_text = data["visual_matches"][0].get("title", "Text not found")
                        detected_text = limit_words(detected_text)
                        search_query = detected_text

    flipkart_url = get_product_url(search_query) if search_query else None
    flipkart_title, flipkart_price, flipkart_reviews = scrape_product_details(flipkart_url) if flipkart_url else ("Product not found", None, [])

    print("\nFlipkart Reviews:")
    if flipkart_reviews:
        for idx, review in enumerate(flipkart_reviews, 1):
            print(review)
    else:
        print("No reviews found.")

    amazon_price, amazon_link = get_amazon_price(search_query) if search_query else (None, None)
    
    sentiment_result = {
        "positive": 0,
        "negative": 0,
        "overall": "Neutral Product"  # Default value
    }
    
    if flipkart_reviews:
        positive = 0
        negative = 0
        for review in flipkart_reviews:
            try:
                sentiment = predict_sentiment(review)
                if sentiment == "Good Product":
                    positive += 1
                else:
                    negative += 1
            except Exception as e:
                print(f"Error analyzing sentiment: {str(e)}")

        sentiment_result["positive"] = positive
        sentiment_result["negative"] = negative
        if positive + negative > 0:
            sentiment_result["overall"] = "Good Product" if positive > negative else "Bad Product" if negative > positive else "Neutral Product"
    
    print(sentiment_result)

    return jsonify({
        "search_query": search_query,
        "detected_text": detected_text,
        "flipkart": {
            "title": flipkart_title,
            "price": flipkart_price,
            "url": flipkart_url,
            "reviews": flipkart_reviews
        },
        "amazon": {
            "price": amazon_price,
            "url": amazon_link
        },
        "sentiment_analysis":sentiment_result
    })

if __name__ == "__main__":
    app.run(debug=True)
    
    
