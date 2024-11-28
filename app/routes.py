from flask import Blueprint, jsonify,send_from_directory
from flask import request
import os
import json
# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running!"}), 200

@main.route('/api/audio-files', methods=['GET'])
def audio_files():
     with open("history.json", "r") as file:
        data = json.load(file)
        return jsonify(data), 200

@main.route('/api/audio/<audio_filename>', methods=['GET'])
def audio_file(audio_filename):
    FILES_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), 'audios'))
    print(FILES_DIRECTORY)
    print("audio_filename:",audio_filename)
    try:
        return send_from_directory(FILES_DIRECTORY, audio_filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

