import streamlit as st
import pickle
import numpy as np
from clean import clean_text

# Load saved models
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# App UI
st.set_page_config(page_title="Tweet Sentiment Classifier", layout="centered")
st.title("🧠 Tweet Sentiment Classifier")
st.markdown("Enter a tweet below to classify it as **Positive**, **Neutral**, or **Negative**.")

tweet = st.text_area("Your Tweet", height=120)

if st.button("Predict Sentiment"):
    if tweet.strip() == "":
        st.warning("Please enter a tweet.")
    else:
        cleaned = clean_text(tweet)
        vec = tfidf.transform([cleaned])
        pred = model.predict(vec)
        label = le.inverse_transform(pred)[0]

        st.subheader("Prediction:")
        st.success(f"**{label.upper()}** sentiment")
