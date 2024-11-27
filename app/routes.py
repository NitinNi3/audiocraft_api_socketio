from flask import Blueprint, jsonify
from flask import request

# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running!"}), 200

@main.route('/api/audio-files', methods=['GET'])
def audio_files():
    return jsonify([]), 200

@main.route('/api/audio/:audio_filename', methods=['GET'])
def audio_file():
    return jsonify({"status": "under dev"}), 200

