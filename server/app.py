import firebase_admin
from firebase_admin import credentials, firestore, storage
from flask import Flask, request, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

# אתחול Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'autoscope-88dd0'  # יש להחליף בשם הדלי שלך ב-Firebase Storage
})

# אתחול Firestore
db = firestore.client()

# מסך הבית
@app.route('/')
def home():
    return "Welcome to the Flask App!"

# עדכון שדה diagnose עבור משתמש מסוים
@app.route('/api/update_diagnose', methods=['POST'])
def update_diagnose():
    data = request.json  # קבלת הנתונים מהבקשה
    
    if not data or 'user_id' not in data or 'diagnose' not in data:
        return jsonify({"error": "Missing required fields: user_id, diagnose"}), 400

    user_id = data['user_id']
    diagnose = data['diagnose']

    # מציאת המסמך ועדכון שדה diagnose בתוך תת השדה results/1/diagnose
    doc_ref = db.collection('Users').document(user_id)
    
    try:
        doc_ref.update({
            'results.1.diagnose': diagnose
        })
        return jsonify({"message": f"Diagnose updated successfully for user {user_id}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# העלאת תמונה ועדכון השדה 'image' ב-Firestore
@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files or 'user_id' not in request.form:
        return jsonify({"error": "Missing file or user_id"}), 400
    
    file = request.files['file']
    user_id = request.form['user_id']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        # שמירת הקובץ זמנית במערכת
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        file.save(temp_path)
        
        # העלאת הקובץ ל-Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'images/{filename}')
        blob.upload_from_filename(temp_path)
        
        # מחיקת הקובץ הזמני
        os.remove(temp_path) 

        # קבלת URL ציבורי לתמונה
        blob.make_public()
        public_url = blob.public_url

        # עדכון שדה 'image' במסמך של המשתמש ב-Firestore
        doc_ref = db.collection('Users').document(user_id)
        try:
            doc_ref.update({
                'details.results.1.image': public_url
            })
            return jsonify({"message": "Image uploaded and Firestore updated successfully", "url": public_url}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# הפעלת השרת
if __name__ == '__main__':
    app.run(debug=True)
