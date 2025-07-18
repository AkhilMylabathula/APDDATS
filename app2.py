# app2.py
import os
from flask import Flask, request, render_template
from plant_disease_model import predict_image
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL database config
db = mysql.connector.connect(
    host="localhost",
    user="root",                     # ← or your MySQL username
    password="Akhil11&&@@,,",  # ← your actual MySQL password
    database="flask_app"
)
cursor = db.cursor()

# Ensure the predictions table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions1 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        predicted_class VARCHAR(100),
        confidence VARCHAR(20),
        image_path TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    filename = "captured.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Predict using model
    result = predict_image(filepath)
    predicted_class = result['class']
    confidence = f"{result['confidence'] * 100:.2f}%"
    diagnosis = result['diagnosis']
    treatment = result['treatment']

    # Save prediction to MySQL
    insert_query = """
        INSERT INTO predictions1 (predicted_class, confidence, image_path)
        VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (predicted_class, confidence, filepath))
    db.commit()

    return render_template('test.html',
                           result=predicted_class,
                           confidence=confidence,
                           diagnosis=diagnosis,
                           treatment=treatment,
                           image_path='/' + filepath)

if __name__ == '__main__':
    app.run(debug=True)
