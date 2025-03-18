import google.generativeai as genai
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)

# Choose a model (e.g., Gemini Pro)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Function to predict crop recommendation
def get_crop_recommendation(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    prompt = f"""
    Based on the given soil parameters, recommend the best crop to cultivate:

    Nitrogen: {nitrogen}
    Phosphorus: {phosphorus}
    Potassium: {potassium}
    Temperature: {temperature}°C
    Humidity: {humidity}%
    pH: {ph}
    Rainfall: {rainfall}mm

    Provide a detailed response on the best crop to cultivate and why.
    """

    response = model.generate_content(prompt)
    return response.text.strip() if response and response.text else "No recommendation available."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nitrogen = request.form["Nitrogen"]
        phosphorus = request.form["Phosphorus"]
        potassium = request.form["Potassium"]
        temperature = request.form["Temperature"]
        humidity = request.form["Humidity"]
        ph = request.form["pH"]
        rainfall = request.form["Rainfall"]

        result = get_crop_recommendation(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
        return render_template("index.html", result=result)

    return render_template("index.html", result=None)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
