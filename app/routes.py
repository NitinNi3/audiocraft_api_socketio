from flask import Blueprint, jsonify,send_from_directory
from flask import request

# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running!"}), 200

@main.route('/api/audio-files', methods=['GET'])
def audio_files():
    return jsonify([]), 200

@main.route('/api/audio/<audio_filename>', methods=['GET'])
def audio_file(audio_filename):
    try:
        return send_from_directory("audios", audio_filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

