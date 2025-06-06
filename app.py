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
        
        # Add this after your single tweet section

st.markdown("---")
st.header("📂 Batch Prediction (Upload CSV)")

uploaded_file = st.file_uploader("Upload CSV with a `text` column", type=["csv"])

if uploaded_file is not None:
    df_upload = None
    try:
        df_upload = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")

    if df_upload is not None:
        # Safe error checking: ensure 'text' column exists
        if 'text' not in df_upload.columns:
            st.error("CSV must contain a `text` column.")
        else:
            st.write("Preview of uploaded data:")
            st.write(df_upload.head())

            # Clean, vectorize, predict
            df_upload['clean_text'] = df_upload['text'].apply(clean_text)
            vec = tfidf.transform(df_upload['clean_text'])
            preds = model.predict(vec)
            proba = model.predict_proba(vec)

            df_upload['predicted_sentiment'] = le.inverse_transform(preds)

            df_upload['confidence_negative'] = proba[:, 0]
            df_upload['confidence_neutral'] = proba[:, 1]
            df_upload['confidence_positive'] = proba[:, 2]

            st.write("Predictions:")
            st.write(df_upload[['text', 'predicted_sentiment', 'confidence_negative', 'confidence_neutral', 'confidence_positive']])

            # Allow download
            csv_result = df_upload.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Predictions as CSV", csv_result, "tweet_predictions.csv", "text/csv")


        st.subheader("Prediction:")
        st.success(f"**{label.upper()}** sentiment")
