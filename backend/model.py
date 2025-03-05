import nltk

nltk.download('punkt_tab')
nltk.download('stopwords')
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

df['cleaned_review'] = df['Review'].apply(preprocess_review)

X = df['cleaned_review']
y = df['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


vectorizer = TfidfVectorizer(max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

def predict_sentiment(review):
    cleaned_review = preprocess_review(review)
    review_tfidf = vectorizer.transform([cleaned_review])
    sentiment = model.predict(review_tfidf)

    if sentiment==1 :
       global positive_count
       positive_count+=1
       return "Good Product"
    else:
        global negative_count
        negative_count+=1
        return "Bad Product"



# # Test the function

# # Interactive testing
# sample_review = input("Enter a product review: ")
# print(predict_sentiment(sample_review))

# List of multiple reviews to test
# reviews = [
#     "This product is amazing! Works exactly as expected, and the quality is top-notch.",
#     "I love this! It's very useful and exceeds my expectations.",
#     "Fantastic product! I would highly recommend it to anyone.",
#     "Great value for money. Does everything it promises and more.",
#     "Perfect for my needs, exactly what I was looking for.",
    
#     "It's okay, does the job but nothing special.",
#     "The product is fine, but could use some improvements.",
#     "It works, but there are better alternatives available.",
#     "Just an average product. It’s neither good nor bad.",
#     "Not great, not terrible. Just a regular product.",
    
#     "Terrible quality. It broke after one use, I wouldn’t recommend it.",
#     "Very disappointing. The product didn’t work as expected.",
#     "Worst purchase I’ve ever made. It’s not worth the money.",
#     "Doesn’t function as described. Complete waste of money.",
#     "I regret buying this. It’s poorly made and unreliable."
# ]

# reviews=["Excellent!","Worst purchase ever","Highly recommended","Terrible","Overpriced but decent","Amazing build quality","Not as described","Great value for money","Completely useless","Exceeded my expectations","Cheap and flimsy","Superb performance","Disappointing experience","A must-have","Would not buy again","Perfect for my needs","Very frustrating to use","Reliable and durable","Not worth the price","Fantastic deal!"
# ]

reviews=[
     "Camera and build quality is great"," Good but battery issue","bad deal in 72k","The best smartphone money can buy!","Awesome Phone"," Battery backup is not so much as i Expected"]

positive_count =0
negative_count=0
# Predict sentiment for each review
for review in reviews:
    print(f"Review: {review}")
    print(f"Sentiment: {predict_sentiment(review)}\n")

if positive_count > negative_count:
       print("Good Product") 
elif negative_count > positive_count:
        print("Bad Product") 
else:
         print("Neutral") 

