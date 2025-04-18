from flask import Flask, request, render_template, jsonify
from irrigation import get_irrigation_recommendation
import sqlite3
import requests
import joblib  # For loading the trained model
import numpy as np
import pickle
app = Flask(__name__)

# Database connection for FAQ chatbot
def get_farming_info(query):
    """Search the database for FAQ responses."""
    conn = sqlite3.connect("farming_data.db")
    cursor = conn.cursor()
    
    query = query.lower()
    cursor.execute("SELECT question, response FROM farming_info")
    data = cursor.fetchall()
    
    best_match = None
    highest_score = 0

    for question, response in data:
        score = sum(1 for word in query.split() if word in question.lower() or word in response.lower())
        if score > highest_score:
            highest_score = score
            best_match = response

    conn.close()
    return best_match if best_match else "⚠️ No relevant farming info found. Try using simpler keywords."

# Hugging Face API Credentials
HF_API_KEY = "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"
HF_MODEL = "facebook/blenderbot-400M-distill"

# Function to interact with Hugging Face API
def get_chatbot_response(user_query):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_query}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for HTTP issues
        response_data = response.json()

        # Extract response
        if isinstance(response_data, list) and len(response_data) > 0 and "generated_text" in response_data[0]:
            return response_data[0]["generated_text"]
        else:
            return "⚠️ No meaningful response from AI."
    except requests.exceptions.HTTPError as errh:
        return f"❌ HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return "❌ Connection Error: Please check your internet connection."
    except requests.exceptions.Timeout as errt:
        return "❌ Timeout Error: The API is taking too long to respond."
    except requests.exceptions.RequestException as err:
        return f"❌ API Error: {err}"

# ✅ Flask Route for Home
@app.route("/")
def home():
    return render_template("index.html")  # Render the index.html template

@app.route("/faq", methods=["POST"])
def faq():
    """FAQ Chatbot API."""
    user_input = request.form.get("question", "")
    response = get_farming_info(user_input)
    return jsonify({"response": response})

@app.route("/agri-chat", methods=["POST"])
def agri_chat():
    """AgriChat AI API."""
    user_message = request.form.get("message", "")
    ai_response = get_chatbot_response(user_message)
    return jsonify({"response": ai_response})

# Define mappings for descriptive input to numerical ranges
SOIL_MOISTURE_MAP = {
    "Very Dry": (0, 20),
    "Dry": (21, 40),
    "Moist": (41, 70),
    "Wet": (71, 100)
}

TEMPERATURE_MAP = {
    "Cold": (0, 15),
    "Warm": (16, 30),
    "Hot": (31, 50)
}

HUMIDITY_MAP = {
    "Low": (0, 40),
    "Medium": (41, 70),
    "High": (71, 100)
}

def convert_to_number(value):
    try:
        return int(value)  # Convert to integer if possible
    except (ValueError, TypeError):
        return None  # Return None if conversion fails

@app.route('/get_irrigation_recommendation', methods=['POST'])
def get_irrigation_recommendation():
    data = request.json

    # Convert to number if possible, otherwise map descriptions
    soil = convert_to_number(data.get("soil")) or SOIL_MOISTURE_MAP.get(data.get("soil"))
    temp = convert_to_number(data.get("temp")) or TEMPERATURE_MAP.get(data.get("temp"))
    hum = convert_to_number(data.get("hum")) or HUMIDITY_MAP.get(data.get("hum"))

    # Ensure values exist
    if soil is None or temp is None or hum is None:
        return jsonify({"recommendation": "⚠️ Invalid input. Please enter valid numbers or descriptions."})

    # Convert range values to their midpoints
    if isinstance(soil, tuple):
        soil = sum(soil) // 2
    if isinstance(temp, tuple):
        temp = sum(temp) // 2
    if isinstance(hum, tuple):
        hum = sum(hum) // 2

    # Example irrigation recommendation logic
    recommendation = ""
    if soil < 30:
        recommendation += "💧 Water immediately, soil is too dry!"
    elif soil < 60:
        recommendation += "🟢 Moderate moisture, monitor for dryness."
    else:
        recommendation += "✅ No irrigation needed, soil is well-watered."

    if temp > 35:
        recommendation += " 🌡 High temperature! Consider extra watering."
    elif temp < 10:
        recommendation += " ❄ Cold weather, limit watering."

    if hum < 30:
        recommendation += " 💨 Low humidity! Increase irrigation slightly."

    return jsonify({"recommendation": recommendation})

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# ✅ Load the trained XGBoost model and LabelEncoder
try:
    with open("xgb_crop_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    logging.debug("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")

try:
    with open("label_encoder.pkl", "rb") as le_file:
        le = pickle.load(le_file)
    logging.debug("LabelEncoder loaded successfully.")
except Exception as e:
    logging.error(f"Error loading label encoder: {e}")


import os

logging.debug(f"Current directory contents: {os.listdir()}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT isn't set
    app.run(host='0.0.0.0', port=port)












