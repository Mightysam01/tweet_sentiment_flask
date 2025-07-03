import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [lastText, setLastText] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction('');
    setError('');

    try {
      const response = await fetch("https://tweet-sentiment-api.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data.prediction);
        setLastText(text);
        setText('');
      } else {
        setError(data.error || "An error occurred.");
      }
    } catch (err) {
      setError("Failed to connect to server.");
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Tweet Sentiment Classifier </h1>
        <p className="intro-text">
          This app predicts the sentiment of tweets related to <strong>airline services and customer complaints</strong>.
          It was trained on the <strong>US Airline Sentiment Dataset</strong>, which contains tweets from airline customers. 
          As such, the model tends to lean more toward detecting <strong>negative sentiment</strong>, since most tweets in the dataset are customer complaints.
        </p>
        <p>
          If you're looking for a more general-purpose and balanced sentiment analysis model trained on diverse tweets,
          you can try the improved version here:&nbsp;
          <a href="https://tweet-sentiment-flask-v2-0.vercel.app/" target="_blank" rel="noopener noreferrer">
            Tweet Sentiment Analyzer v2.0
          </a>
        </p>

        <div className="examples">
          <p><strong>Example Tweets You Can Try:</strong></p>
          <ul>
            <li>"The flight was delayed for 3 hours with no explanation." → Negative</li>
            <li>"The customer service representative was helpful." → Positive</li>
            <li>"Just landed at JFK airport." → Neutral</li>
          </ul>
        </div>

        <form onSubmit={handleSubmit} className="predict-form">
          <textarea
            rows="4"
            cols="50"
            placeholder="Type a tweet here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            required
            className="text-input"
          />
          <button type="submit" disabled={loading} className="predict-button">
            {loading ? "Predicting..." : "Predict"}
          </button>
        </form>

        {prediction && (
          <div className="result-box">
            <p><strong>Input:</strong> {lastText}</p>
            <p><strong>Prediction:</strong> {prediction}</p>
          </div>
        )}

        {error && <p className="error-message">{error}</p>}
      </header>
    </div>
  );
}

export default App;
