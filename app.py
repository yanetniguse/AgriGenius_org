import logging
from flask import Flask, request, render_template, jsonify
from irrigation import get_irrigation_recommendation
import sqlite3
import requests
import joblib
import numpy as np
import pickle
import os

app = Flask(__name__)

# Database connection for FAQ chatbot
def get_farming_info(query):
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

# Hugging Face API
HF_API_KEY = "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"
HF_MODEL = "facebook/blenderbot-400M-distill"

def get_chatbot_response(user_query):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_query}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            return data[0]["generated_text"]
        return "⚠️ No meaningful response from AI."
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/faq", methods=["POST"])
def faq():
    user_input = request.form.get("question", "")
    response = get_farming_info(user_input)
    return jsonify({"response": response})

@app.route("/agri-chat", methods=["POST"])
def agri_chat():
    user_message = request.form.get("message", "")
    ai_response = get_chatbot_response(user_message)
    return jsonify({"response": ai_response})

# Mappings for descriptive values
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
        return int(value)
    except (ValueError, TypeError):
        return None

@app.route('/get_irrigation_recommendation', methods=['POST'])
def irrigation_api():
    data = request.json

    soil = convert_to_number(data.get("soil")) or SOIL_MOISTURE_MAP.get(data.get("soil"))
    temp = convert_to_number(data.get("temp")) or TEMPERATURE_MAP.get(data.get("temp"))
    hum = convert_to_number(data.get("hum")) or HUMIDITY_MAP.get(data.get("hum"))

    if soil is None or temp is None or hum is None:
        return jsonify({"recommendation": "⚠️ Invalid input. Please enter valid numbers or descriptions."})

    # Convert to midpoint if range
    if isinstance(soil, tuple): soil = sum(soil) // 2
    if isinstance(temp, tuple): temp = sum(temp) // 2
    if isinstance(hum, tuple): hum = sum(hum) // 2

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

# Load trained model and label encoder
try:
    with open("xgb_crop_model.pkl", "rb") as f:
        model = pickle.load(f)
    logging.debug("✅ XGBoost model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load model: {e}")

try:
    with open("label_encoder.pkl", "rb") as f:
        le = pickle.load(f)
    logging.debug("✅ LabelEncoder loaded successfully.")
except Exception as e:
    logging.error(f"❌ Failed to load LabelEncoder: {e}")

# ✅ Prediction Function
def predict_crop(input_features):
    """
    Predict the recommended crop based on soil and climate conditions.
    :param input_features: List of feature values (N, P, K, Temperature, Humidity, pH, Rainfall)
    :return: Predicted crop label
    """
    input_array = np.array([input_features]).reshape(1, -1)  # Convert input to array
    predicted_label = model.predict(input_array)[0]  # Predict crop
    predicted_crop = le.inverse_transform([predicted_label])[0]  # Convert label back to crop name
    return predicted_crop

# ✅ API Route for Prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json  # Get JSON data from request
        print("🚀 Received prediction request:", data)
        features = [
            data["Nitrogen"], 
            data["Phosphorus"], 
            data["Potassium"], 
            data["Temperature"], 
            data["Humidity"], 
            data["pH"], 
            data["Rainfall"]
        ]
        
        predicted_crop = predict_crop(features)  # Get prediction from model
        return jsonify({"Recommended Crop": predicted_crop})  # Return JSON response
        

    except Exception as e:
        print(f"[PREDICTION ERROR] {e}")
        return jsonify({'error': 'Failed to get prediction. Please try again.'}), 500

logging.debug(f"📂 Current directory contents: {os.listdir()}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
