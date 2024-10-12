from flask import Flask, request, jsonify
from flask_cors import CORS  # สำหรับการจัดการ CORS
import tensorflow as tf
from PIL import Image, UnidentifiedImageError
import numpy as np
import os
import boto3
from botocore.exceptions import NoCredentialsError

# กำหนดเส้นทางของโมเดลโดยใช้ os.path.join
current_directory = os.path.dirname(__file__)
model_path = os.path.join(current_directory, 'AW_model.h5')

# ฟังก์ชันดาวน์โหลดโมเดลจาก S3
def download_model_from_s3(bucket_name, model_key, download_path):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, model_key, download_path)
        print(f"Model downloaded successfully to {download_path}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error downloading model: {e}")

# ดาวน์โหลดโมเดลจาก S3 (ถ้าโมเดลไม่อยู่ในเครื่อง)
if not os.path.exists(model_path):
    download_model_from_s3('your-bucket-name', 'path/to/AW_model.h5', model_path)

# โหลดโมเดล
try:
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

app = Flask(__name__)
CORS(app)  # เปิดใช้งาน CORS สำหรับทุกเส้นทางในแอปพลิเคชัน

def preprocess_image(uploaded_file):
    """
    ฟังก์ชันสำหรับเตรียมรูปภาพที่อัปโหลดก่อนการทำนาย
    """
    try:
        # เปิดและปรับขนาดรูปภาพ
        img = Image.open(uploaded_file)
        img = img.convert('RGB')  # แปลงภาพเป็น RGB เพื่อป้องกันข้อผิดพลาดจากภาพที่มีโหมดสีต่างกัน
        img = img.resize((150, 150))  # ปรับขนาดให้ตรงกับที่โมเดลต้องการ
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # ปรับขนาดพิกเซลให้อยู่ในช่วง 0-1
        return img_array
    except UnidentifiedImageError:
        print("Error: Unidentified image format")
        return None
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    """
    เส้นทางสำหรับการทำนายรูปภาพที่อัปโหลด
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    processed_image = preprocess_image(file)

    if processed_image is None:
        return jsonify({'error': 'Cannot process the uploaded file as an image'}), 400

    try:
        # ทำนายผลด้วยโมเดล
        predictions = model.predict(processed_image)
        class_labels = ['Acne', 'Clear', 'Wrinkles']

        predicted_class = class_labels[np.argmax(predictions)]
        confidence = np.max(predictions) * 100

        return jsonify({'prediction': predicted_class, 'confidence': confidence})
    except Exception as e:
        print(f"Prediction error: {str(e)}")  # แสดงข้อความแสดงข้อผิดพลาดใน console
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

if name == 'appy':
    app.run(debug=True, host='0.0.0.0', port=5000)

  # รันเซิร์ฟเวอร์ Flask บนพอร์ต 5000
