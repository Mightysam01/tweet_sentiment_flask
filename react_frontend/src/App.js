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
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data.prediction);
        setLastText(text); // store what was typed
        setText('');       // clear input field
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
        <h2>Tweet Sentiment App</h2>

        <form onSubmit={handleSubmit} className="predict-form">
          <textarea
            rows="4"
            cols="50"
            placeholder="Type here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            required
            className="text-input"
          />
          <br />
          <button type="submit" disabled={loading} className="predict-button">
            {loading ? "Predicting..." : "Predict"}
          </button>
        </form>

        {prediction && (
          <div className="result-box">
            <p><strong>Tweet:</strong> {lastText}</p>
            <p><strong>Prediction:</strong> {prediction}</p>
          </div>
        )}

        {error && <p style={{ color: 'red' }}>{error}</p>}
      </header>
    </div>
  );
}

export default App;
