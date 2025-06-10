# Tweet Sentiment Classifier

A full-stack app that classifies tweets as **Positive**, **Neutral**, or **Negative**.

This project includes:
- A **Flask REST API** backend deployed on Render
- A **React** frontend deployed on Vercel
- A trained ML model hosted on Hugging Face
- Model trained on IMDB dataset and fine-tuned for tweet sentiment classification

---

## Features

- Frontend built with React
- REST API backend built with Flask
- Preprocessing using NLTK
- TF-IDF vectorization
- Model files dynamically loaded from Hugging Face Hub
- Clean GitHub repo — no large model files stored in Git
- Fully deployable on free hosting services (Render, Vercel)

---

## Live App

- Frontend (Vercel): [https://tweet-sentiment-flask.vercel.app](https://tweet-sentiment-flask.vercel.app)  
- Backend API (Render): [https://tweet-sentiment-api.onrender.com](https://tweet-sentiment-api.onrender.com)

### API Endpoint

```http
POST /predict
Content-Type: application/json

Request Body:
{
  "text": "I love this!"
}

Response:
{
  "prediction": "Positive"
}```

---

## Model Hosting

Model files are hosted publicly on Hugging Face:

- [Model files on Hugging Face](https://huggingface.co/MLwithSam/tweet-sentiment-app/tree/main)
- model.pkl
- tfidf.pkl
- label_encoder.pkl

The Flask API downloads these files dynamically at runtime.
