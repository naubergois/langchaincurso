import os
import requests
import pandas as pd
from pyod.models.ecod import ECOD
from langchain_core.tools import tool

@tool
def run_pyod_anomaly_detection(input_text: str) -> float:
    """
    Analyzes the input text for anomalies using PyOD (ECOD model).
    Since PyOD works on numerical data, this tool effectively 'simulates'
    extraction of numerical features (e.g., length, word count, complexity)
    to generate an anomaly score. 
    Returns the anomaly score (higher is more anomalous).
    """
    try:
        # Simulate feature extraction from text
        # In a real scenario, this would extract financial figures or log data
        # Here we use text metrics as proxfy features
        features = {
            "length": len(input_text),
            "word_count": len(input_text.split()),
            "avg_word_len": sum(len(w) for w in input_text.split()) / len(input_text.split()) if input_text else 0,
            "capital_ratio": sum(1 for c in input_text if c.isupper()) / len(input_text) if input_text else 0
        }
        
        # Create a small 'context' dataset to compare against (simulated normal behavior)
        # We generate some synthetic 'normal' data points
        normal_data = pd.DataFrame([
            {"length": 500, "word_count": 80, "avg_word_len": 5.5, "capital_ratio": 0.05},
            {"length": 600, "word_count": 100, "avg_word_len": 5.0, "capital_ratio": 0.04},
            {"length": 450, "word_count": 70, "avg_word_len": 6.0, "capital_ratio": 0.06},
            {"length": 550, "word_count": 90, "avg_word_len": 5.2, "capital_ratio": 0.05},
            {"length": 520, "word_count": 85, "avg_word_len": 5.3, "capital_ratio": 0.05},
        ])
        
        current_data = pd.DataFrame([features])
        
        # Train ECOD (Unsupervised) on 'normal' data + current data to see where it stands
        # Note: In production, you'd load a pre-trained model.
        combined_data = pd.concat([normal_data, current_data], ignore_index=True)
        
        clf = ECOD()
        clf.fit(combined_data)
        
        # Get score for the last element (our input)
        scores = clf.decision_scores_
        input_score = scores[-1]
        
        return float(input_score)
        
    except Exception as e:
        print(f"Error in PyOD tool: {e}")
        return 0.0

@tool
def send_telegram_message(message: str, chat_id: str, bot_token: str) -> str:
    """
    Sends a message via Telegram Bot API.
    """
    if not chat_id or not bot_token:
        return "Telegram credentials missing. Message not sent."
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return "Message sent successfully!"
    except Exception as e:
        return f"Failed to send Telegram message: {e}"
