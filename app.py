import streamlit as st
import pickle
import numpy as np
from clean import clean_text
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(repo_id="MLwithSam/tweet-sentiment-app", filename="model.pkl")
tfidf_path = hf_hub_download(repo_id="MLwithSam/tweet-sentiment-app", filename="tfidf.pkl")
label_encoder_path = hf_hub_download(repo_id="MLwithSam/tweet-sentiment-app", filename="label_encoder.pkl")

# Load saved models
with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(tfidf_path, "rb") as f:
    tfidf = pickle.load(f)

with open(label_encoder_path, "rb") as f:
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
