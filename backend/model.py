import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("punkt resource not found. Attempting to download.")
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("stopwords resource not found. Attempting to download.")
    nltk.download('stopwords')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('sample.csv')

df['sentiment'] = df['Rating'].apply(lambda x: 1 if x == 2 else 0)

stop_words = set(stopwords.words('english'))

def preprocess_review(text):
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    return ' '.join(filtered_words)

def train_and_save_model():
    df = pd.read_csv('sample.csv')
    df['sentiment'] = df['Rating'].apply(lambda x: 1 if x == 2 else 0)
    df['cleaned_review'] = df['Review'].apply(preprocess_review)
    
    X = df['cleaned_review']
    y = df['sentiment']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)
    
    # Save model and vectorizer
    joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')
    joblib.dump(model, 'sentiment_model.joblib')
    
try:
    vectorizer = joblib.load('tfidf_vectorizer.joblib')
    model = joblib.load('sentiment_model.joblib')
except FileNotFoundError:
    vectorizer = None
    model = None


def predict_sentiment(review):
    if vectorizer is None or model is None:
        raise ValueError("Model not loaded. Train model first.")
    cleaned_review = preprocess_review(review)
    review_tfidf = vectorizer.transform([cleaned_review])
    sentiment = model.predict(review_tfidf)
    return "Good Product" if sentiment == 1 else "Bad Product"


if __name__ == "__main__":
    train_and_save_model()
   


