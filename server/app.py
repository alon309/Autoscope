import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import Flask, request, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename

import uuid  # לייצור מפתחות ייחודיים

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
    # Get the user ID and diagnose string
    user_id = request.form.get('user_id')
    diagnose = request.form.get('diagnose')
    
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']

    # Ensure a safe file name
    filename = secure_filename(image_file.filename)
    unique_filename = f"{user_id}_{filename}"  # Ensure uniqueness

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    image_file.save(temp_file.name)

    # Upload the image to Firebase Storage
    blob = bucket.blob(f'images/{unique_filename}')
    try:
        blob.upload_from_filename(temp_file.name, content_type=image_file.content_type)
        blob.make_public()
        image_url = blob.public_url

        # Update Firestore with the image URL and diagnose
        doc_ref = db.collection('Users').document(user_id)

        if not doc_ref.get().exists:
            os.remove(temp_file.name)  # Cleanup temporary file
            return jsonify({"error": f"User {user_id} does not exist"}), 404

        # Use a unique key for the results
        result_id = str(uuid.uuid4())  # Generate a unique identifier for the result

        # Create or update the results field in Firestore
        doc_ref.update({
            f'results.{result_id}.diagnose': diagnose,
            f'results.{result_id}.image': image_url
        })

        return jsonify({"message": f"Image uploaded and diagnose updated successfully for user {user_id}"}), 200
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
    # Get the user ID
    user_id = request.form.get('user_id')
    
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']

    try:

        return jsonify({"message": f"Image uploaded and diagnosed successfully for user {user_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        print("test")


# Run the server
if __name__ == '__main__':
    app.run(debug=True)
