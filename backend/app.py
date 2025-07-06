import json
import tempfile
from flask import Flask, render_template, request, jsonify
import os
from docai_utils import extract_text_from_document

import sqlite3

DATABASE = "C:/Users/Jie/Desktop/Recipe/database/receipts.db"



#TODO: RESOLVE BACKEND AND FRONTEND DOMAINS MIGHT BE DIFFERENT
#only for local testing
from flask_cors import CORS
#remove this for production


BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..','frontend'))


app= Flask(__name__, template_folder=FRONTEND_DIR)

#NOTE: THIS IS ONLY FOR TESTING, IT IS NOT SECURE
#remove this for production right now is making sure cross origin requests work for testing
CORS(app, origins=["http://127.0.0.1:5500"])
#remove this for production

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn


@app.route('/extract_text_from_document', methods=['POST'])
def extract_text():
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "empty哇"}), 400
    
    #extract extension from the file name
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.pdf', '.tiff', '.gif', '.bmp', '.webp']:
        return jsonify({"error": "Unsupported file type"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        file.save(temp_file.name)
        json_data = extract_text_from_document(file_path=temp_file.name)
    print(json_data)
    return json_data


if __name__ == '__main__': 

    app.run(debug=True, host='127.0.0.1', port=5000)  
