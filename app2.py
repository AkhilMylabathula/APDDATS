# app2.py
import os
from flask import Flask, request, render_template
from plant_disease_model import predict_image
import mysql.connector
from datetime import datetime
import cloudinary
import cloudinary.uploader


app = Flask(__name__)

# MySQL database config
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",                     # ← or your MySQL username
#     password="Akhil11&&@@,,",  # ← your actual MySQL password
#     database="flask_app"
# )
# cursor = db.cursor()

# # Ensure the predictions table exists
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS predictions1 (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         predicted_class VARCHAR(100),
#         confidence VARCHAR(20),
#         image_path TEXT,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
# """)

cloudinary.config(
  cloud_name=os.environ.get("CLOUD_NAME"),
  api_key=os.environ.get("CLOUD_API_KEY"),
  api_secret=os.environ.get("CLOUD_API_SECRET")
)

@app.route('/')
def index():
    return render_template('test2.html')

@app.route('/next')
def next_page():
    return render_template('test.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save uploaded/captured image
    upload_result = cloudinary.uploader.upload(file)
    image_url = upload_result['secure_url']

    # Predict using model
    result = predict_image(image_url)
    predicted_class = result['class']
    confidence = f"{result['confidence'] * 100:.2f}%"
    diagnosis = result['diagnosis']
    treatment = result['treatment']

    # Save prediction to MySQL
    # insert_query = """
    #     INSERT INTO predictions1 (predicted_class, confidence, image_path)
    #     VALUES (%s, %s, %s)
    # """
    # cursor.execute(insert_query, (predicted_class, confidence, filepath))
    # db.commit()

    return render_template('test.html',
                           result=predicted_class,
                           confidence=confidence,
                           diagnosis=diagnosis,
                           treatment=treatment,
                           image_path=image_url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # get port from env (important for Render)
    app.run(host="0.0.0.0", port=port)
