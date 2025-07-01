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
        <h1>Tweet Sentiment Classifier</h1>
        <p className="intro-text">
          This app predicts the sentiment of short tweets or phrases. Type a sentence and press “Predict” to see if it’s classified as Positive, Neutral, or Negative.
        </p>

        <div className="examples">
          <p><strong>Try one of these:</strong></p>
          <ul>
            <li>“I'm really happy with the new phone.” → Positive</li>
            <li>“It’s just another regular day.” → Neutral</li>
            <li>“I hate waiting in traffic.” → Negative</li>
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
