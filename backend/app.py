import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from genai_utils import ask_genai

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend'))

app = Flask(__name__, static_folder=FRONTEND_DIR, template_folder=FRONTEND_DIR)
CORS(app, origins=["http://127.0.0.1:5500"])


@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message') if data else None
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    reply = ask_genai(message)
    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
