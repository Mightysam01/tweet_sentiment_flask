from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from clean import clean_text
from huggingface_hub import hf_hub_download

# Load model files from Hugging Face
model_path = hf_hub_download(repo_id="MLwithSam/tweet-sentiment-app", filename="model.pkl")
tfidf_path = hf_hub_download(repo_id="MLwithSam/tweet-sentiment-app", filename="tfidf.pkl")
label_encoder_path = hf_hub_download(repo_id="MLwithSam/tweet-sentiment-app", filename="label_encoder.pkl")

# Load models
with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(tfidf_path, "rb") as f:
    tfidf = pickle.load(f)

with open(label_encoder_path, "rb") as f:
    le = pickle.load(f)

# Init Flask app
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Tweet Sentiment API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    tweet = data["text"]

    # Clean and predict
    cleaned = clean_text(tweet)
    vec = tfidf.transform([cleaned])
    pred = model.predict(vec)
    label = le.inverse_transform(pred)[0]

    return jsonify({
        "prediction": label
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
