import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
from flask import Flask, request, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename

import uuid  # לייצור מפתחות ייחודיים
import requests

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'autoscope-88dd0.appspot.com' 
})

# Verify bucket initialization
bucket = storage.bucket()
print(f"Initialized bucket: {bucket.name}")

# Initialize Firestore
db = firestore.client()

# Home screen
@app.route('/')
def home():
    return "Welcome to the Flask App!"

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
    filename = secure_filename(image_file.filename)
    unid = str(uuid.uuid4())
    unique_filename = f"{unid}_{filename}"  # Ensure uniqueness

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

            # Use a unique key for the results
            result_id = str(uuid.uuid4())  # Generate a unique identifier for the result

            # Create or update the results field in Firestore with date and time
            doc_ref.update({
                f'results.{result_id}.diagnose': diagnose,
                f'results.{result_id}.image': image_url,
                f'results.{result_id}.datetime': datetime_str
            })

            return jsonify({"result_id": result_id, "image_url": image_url, "message": f"Image uploaded and diagnose updated successfully for user {user_id}"}), 200

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
        # Get the user ID
        user_id = request.form.get('user_id')
        
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']

        return jsonify({"message": f"Image uploaded and diagnosed successfully for user {user_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        print("test")

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=full_name,
            phone_number="+972111111111"
        )

        user_doc_ref = db.collection('Users').document(user.uid)

        user_doc_ref.set({
            'results': None
        })

        return jsonify({"status": "success", "uid": user.uid}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    print(data)
    email = data.get("email")
    password = data.get("password")

    # URL של ה-API של Firebase
    firebase_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyD25cuiclB7xuXAClAsX3sFpttko-T7X5Y"
    
    firebase_data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    try:
        # שלח בקשה ל-API של Firebase
        response = requests.post(firebase_url, json=firebase_data)
        response.raise_for_status()  # יעלה שגיאה אם הקוד לא 200
        
        user_data = response.json()
        uid = user_data.get("localId")

        # קבל את פרטי המשתמש מ-Firebase Authentication
        firebase_user_info = {
            "email": user_data.get("email"),
            "display_name": user_data.get("displayName"),
            "phone_number": user_data.get("phoneNumber", "+972111111111"),
            "uid": uid
        }
        print(response.json())
        
        # קבל את פרטי המשתמש מהדאטאבייס
        doc_ref = db.collection('Users').document(uid)  # השתמש ב-uid כ-document ID
        user_doc = doc_ref.get()

        if user_doc.exists:
            user_details = user_doc.to_dict()  # קבל את כל הפרטים מהמסמך
            user_details.update(firebase_user_info)  # עדכן את המידע עם פרטי Firebase

            return jsonify(user_details), 200  # החזרת כל הפרטים כולל uid

        else:
            return jsonify({"error": "User not found."}), 404  # טיפול במקרה שהמסמך לא קיים
    
    except requests.exceptions.HTTPError as http_err:
        # קבל את פרטי השגיאה מהתגובה
        error_details = response.json() if response.content else {}
        return jsonify({"error": error_details.get("error", {}).get("message", "An unknown error occurred.")}), 400
    
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@app.route('/api/save_settings', methods=['POST'])
def save_settings():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 415

    data = request.json
    print(f"Received data: {data}")  # הדפס את הנתונים המתקבלים

    user_id = data.get('user_id')
    full_name = data.get('full_name')
    email = data.get('email')
    phone_number = data.get('phone_number')

    try:
        # Update user details in Firebase Authentication
        user = auth.update_user(
            user_id,
            display_name=full_name,
            email=email,
            phone_number=phone_number
        )

        print(f"Updated user: {user.uid}")  # הדפס את מזהה המשתמש המעודכן
        return jsonify({"status": "success", "message": "User details updated successfully"}), 200
    except Exception as e:
        print(f"Error updating user: {str(e)}")  # הדפס שגיאות אם יש
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




# Run the server
if __name__ == '__main__':
    app.run(debug=True)
