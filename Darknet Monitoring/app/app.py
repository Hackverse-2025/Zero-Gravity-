from flask import Flask, render_template, request
import pandas as pd
import tensorflow as tf
import requests
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Load AI Model
model = tf.keras.models.load_model("models/darknet_model.h5")

# Load Dataset
df = pd.read_csv("data/darknet_data.csv")

# Function to check threat intelligence
def check_ip_reputation(ip):
    api_key = "YOUR_VIRUSTOTAL_API_KEY"
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}

# Route: Home (Dashboard)
@app.route('/')
def dashboard():
    return render_template("dashboard.html", data=df.to_dict(orient="records"))

# Route: Check IP
@app.route('/check_ip', methods=['POST'])
def check_ip():
    ip = request.form['ip']
    result = check_ip_reputation(ip)
    return render_template("dashboard.html", data=df.to_dict(orient="records"), ip_result=result)

# Route: Generate PDF Report
@app.route('/generate_report')
def generate_report():
    c = canvas.Canvas("darknet_report.pdf")
    c.drawString(100, 800, "Darknet Traffic Report")
    
    y_position = 780
    for index, row in df.iterrows():
        c.drawString(100, y_position, f"IP: {row['src_ip']} -> {row['dst_ip']} | Category: {row['category']}")
        y_position -= 20

    c.save()
    return "PDF Report Generated Successfully!"

if __name__ == '__main__':
    app.run(debug=True)
