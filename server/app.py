import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
from flask import Flask, request, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from io import BytesIO
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)
print("TensorFlow version:", tf.__version__)

from PIL import Image
import numpy as np
import uuid
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

load_dotenv()
firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')
firebase_url_login = os.getenv('FIREBASE_URL')
main_email = os.getenv('GMAIL_USER')
main_password = os.getenv('GMAIL_PASSWORD')

# Enable CORS for the entire app
CORS(app, resources={r"/*": {"origins": "*"}})

if firebase_credentials is None:
    raise ValueError("Missing FIREBASE_CREDENTIALS in environment variables.")
if firebase_url_login is None:
    raise ValueError("Missing FIREBASE_URL_LOGIN in environment variables.")
if main_email is None:
    raise ValueError("Missing GMAIL_USER in environment variables.")
if main_password is None:
    raise ValueError("Missing GMAIL_PASSWORD in environment variables.")

cred_dict = json.loads(firebase_credentials)

# Define class names (update this based on your dataset)
CLASS_NAMES = ['aom', 'com', 'normal']

# Initialize Firebase
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'autoscope-88dd0.appspot.com'
})

# Verify bucket initialization
bucket = storage.bucket()
print(f"Initialized bucket: {bucket.name}")

# Initialize Firestore
db = firestore.client()

def load_model_dynamic_safe(model_path):
    """
    Wrapper for load_model_dynamic with error handling.
    """
    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"The specified path '{model_path}' does not exist.")

        if os.path.isdir(model_path):
            model = tf.keras.models.load_model(model_path)
            print("Loaded SavedModel format")
        elif model_path.endswith('.h5'):
            model = tf.keras.models.load_model(model_path)
            print("Loaded H5 format")
        else:
            raise ValueError("Unsupported model format. Please provide a SavedModel directory or .h5 file.")

        return model

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None
MODEL_PATH = os.path.join(os.getcwd(), "mysite/ResNet50_model.tflite")
# MODEL_PATH = os.path.join(os.getcwd(), "mysite/VGG16model.tflite")
# MODEL_PATH = os.path.join(os.getcwd(), "mysite/VGG16model.h5")
# MODEL_PATH = os.path.join(os.getcwd(), r"C:\Users\ndvp3\OneDrive - ort braude college of engineering\שולחן העבודה\autoscope\server/VGG16model.h5")
# model = load_model_dynamic_safe(MODEL_PATH)

try:
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    print("TFLite Model loaded successfully!")
    print("Input details:", input_details)
    print("Output details:", output_details)
except Exception as e:
    print(f"Error loading TFLite model: {e}")
    interpreter = None

# Home screen
@app.route('/test')
def home():
    return "AutoScope - Server is Running...!"

@app.route('/api/save_result', methods=['POST'])
def save_result():
    # Get the user ID, diagnose string, and date-time
    user_id = request.form.get('user_id')
    diagnose = request.form.get('diagnose')
    datetime_str = request.form.get('datetime')

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']

    # Ensure a safe file name
    unid = str(uuid.uuid4().hex)
    unique_filename = f"{unid}"

    # Create a temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            image_file.save(temp_file.name)

            # Upload the image to Firebase Storage
            blob = bucket.blob(f'images/{user_id}/{unique_filename}')
            blob.upload_from_filename(temp_file.name, content_type=image_file.content_type)
            blob.make_public()
            image_url = blob.public_url

            # Update Firestore with the image URL, diagnose, and datetime
            doc_ref = db.collection('Users').document(user_id)

            if not doc_ref.get().exists:
                return jsonify({"error": f"User {user_id} does not exist"}), 404

            # Add result to results array
            new_result = {
                'diagnose': diagnose,
                'image': image_url,
                'datetime': datetime_str
            }
            doc_ref.update({
                'results': firestore.ArrayUnion([new_result])
            })

            return jsonify({"message": f"Result added successfully for user {user_id}", "image": image_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Cleanup temporary file
        try:
            os.remove(temp_file.name)
        except OSError as e:
            print(f"Error removing temporary file: {e}")

@app.route('/api/analyze_image', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']
        img = load_img(BytesIO(image_file.stream.read()), target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()

        predictions = interpreter.get_tensor(output_details[0]['index'])
        confidence = predictions[0][0] * 100
        result = "Infected" if confidence > 50 else "Normal"

        return jsonify({
            "result": result,
            "confidence": confidence
        }), 200

    except Exception as e:
        # הדפסת השגיאה לקונסולה לעזרה בדיבוג
        print(f"An error occurred: {str(e)}")
        # החזרת הודעת שגיאה כללית למשתמש
        return jsonify({"error": "An error occurred during image analysis"}), 500

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')
    gender = data.get('gender')

    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=full_name,
            phone_number=phone_number
        )

        user_doc_ref = db.collection('Users').document(user.uid)

        user_doc_ref.set({
            'phone_number': phone_number,
            'gender': gender,
            'results': None
        })

        return jsonify({"status": "success", "uid": user.uid}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    firebase_data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        response = requests.post(firebase_url_login, json=firebase_data)
        response.raise_for_status()

        user_data = response.json()
        uid = user_data.get("localId")

        firebase_user_info = {
            "email": user_data.get("email"),
            "display_name": user_data.get("displayName"),
            "uid": uid
        }

        doc_ref = db.collection('Users').document(uid)
        user_doc = doc_ref.get()
        if user_doc.exists:
            user_details = user_doc.to_dict()
            user_details.update(firebase_user_info)
            return jsonify(user_details), 200
        else:
            return jsonify({"error": "User not found."}), 404

    except requests.exceptions.HTTPError as http_err:
        error_details = response.json() if response.content else {}
        return jsonify({"error": error_details.get("error", {}).get("message", "An unknown error occurred.")}), 400

    except Exception as err:
        return jsonify({"error": str(err)}), 500


@app.route('/api/save_settings', methods=['POST'])
def save_settings():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 415

    data = request.json
    user_id = data.get('user_id')
    full_name = data.get('full_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    gender = data.get('gender')

    try:
        # Update user details in Firebase Authentication
        user = auth.update_user(
            user_id,
            display_name=full_name,
            email=email,
            phone_number=phone_number
        )
        user_doc_ref = db.collection('Users').document(user.uid)
        user_doc_ref.update({
            'phone_number': phone_number,
            'gender': gender
        })

        return jsonify({"status": "success", "message": "User details updated successfully"}), 200
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/get_history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id')  # Get user_id from query params
    try:
        # Fetch the history from Firestore
        doc_ref = db.collection('Users').document(user_id)
        doc = doc_ref.get()
        if not doc.exists:
            return jsonify({"error": f"User {user_id} does not exist"}), 404
        # Assuming the history is stored under 'results' in Firestore
        results = doc.to_dict().get('results', {})
        # Format the history as a list of dictionaries
        history_data = [
            {
                'date': result.get('datetime', ''),
                'image': result.get('image', ''),
                'result': result.get('diagnose', '')
            }
            for result_id, result in results.items()
        ]
        return jsonify(history_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/send_email', methods=['POST'])
def send_email():
    data = request.json
    from_email = data.get("from_email")
    to_email = data.get("to_email")
    subject = data.get("subject")
    content = data.get("html")
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(content, "html"))
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(main_email, main_password)
        server.send_message(msg)
        server.quit()
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run()