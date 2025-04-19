### 🌱 **AgriGenius - Smart Agriculture Solution**  
**AI-Powered Agriculture Assistant for Smarter Farming** 🚀  

![image](https://github.com/user-attachments/assets/958d0685-9f9b-4016-925d-1701f1c4d5ea)

---

## 📌 **About AgriGenius**  
AgriGenius is an intelligent agriculture solution designed to help farmers optimize irrigation, predict environmental conditions, and interact with an AI-powered chatbot for real-time farming advice. This system integrates **machine learning, smart sensors, and AI recommendations** to enhance farming efficiency.  

---

## 🚀 **Features**  
✅ **Smart Irrigation System** – Provides AI-based watering recommendations based on soil moisture, temperature, and humidity.  
✅ **Hybrid Input System** – Accepts both numeric values & descriptive inputs (e.g., "Dry", "Cold", "High").  
✅ **Crop Prediction Model 🌾** – ML-based predictor that suggests the most suitable crop based on soil nutrients, weather conditions, and pH.  
✅ **Agri Chatbot 🤖** – AI-powered assistant for answering agricultural queries.  
✅ **Error Handling & Input Validation** – Ensures farmers receive understandable feedback when entering values.  
✅ **Scalable & Extensible** – Designed for future enhancements like crop disease prediction, weather forecasts, and more.  

---

## 🧠 **Machine Learning Crop Prediction Model**  
AgriGenius includes a trained **XGBoost Classifier** model to recommend the most suitable crop based on:

- **Nitrogen (N)**  
- **Phosphorus (P)**  
- **Potassium (K)**  
- **Temperature (°C)**  
- **Humidity (%)**  
- **pH Level**  
- **Rainfall (mm)**

The model was trained using a labeled dataset with multiple crop types and optimized using the `XGBoost` algorithm for high performance and accuracy.

**Input:** JSON payload or form values from UI  
**Output:** Recommended Crop (e.g., "Maize", "Sugarcane", etc.)

> 🔍 Available at `POST /predict` route.

---

## 🛠 **Tech Stack**  
🔹 **Backend:** Flask (Python)  
🔹 **Frontend:** HTML, CSS, JavaScript  
🔹 **Database:** SQLite (or Firebase for future scalability)  
🔹 **AI & ML:** NLP-based Chatbot, XGBoost Crop Prediction  
🔹 **Deployment:** GitHub, Render/Railway  

---

## 🚀 **Installation & Setup**  
### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/yanetniguse/AgriGenius.git
cd AgriGenius
```

### **2️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Application**  
```bash
python app.py
```
Now, visit `http://127.0.0.1:5000` in your browser.

---

## 🌍 **Live Demo**  
[🔗 Click Here to View the Live Version](https://your-live-link.com) _(Add hosting link when deployed)_

---

## 💡 **How It Works**  
1️⃣ **User selects or enters soil moisture, temperature, and humidity levels.**  
2️⃣ **System validates input & maps descriptive terms to numeric ranges.**  
3️⃣ **ML model recommends the best crop for given conditions.**  
4️⃣ **AI provides personalized irrigation & farming recommendations.**  
5️⃣ **Users can also chat with the Agri Chatbot for additional support.**  

---

## 🛠 **Future Enhancements**  
🔹 Add **Weather API Integration** for real-time forecasts.  
🔹 Implement **Machine Learning Models** for crop disease detection.  
🔹 Expand chatbot capabilities with **voice commands**.  
🔹 Support **Multiple Languages** for accessibility.  

---

## 🤝 **Contributing**  
Want to improve **AgriGenius**? Contributions are welcome!  
1. Fork the repo 🍴  
2. Create a feature branch 🚀  
3. Commit your changes ✅  
4. Submit a pull request 🔥  

---

## 📜 **License**  
This project is licensed under the **MIT License**.  

---

## 💬 **Contact & Support**  
📧 **Email:** yanetesfay@gmail.com  
🔗 **LinkedIn:** [yanetniguse7](https://www.linkedin.com/in/yanetniguse7)  
🌍 **Website/Portfolio:** [My Website](https://yanet-niguse-tesfay.vercel.app/)  

---

🔥 _Empowering Farmers with Smart Agriculture Solutions!_ 🌱🚀  
```

---
