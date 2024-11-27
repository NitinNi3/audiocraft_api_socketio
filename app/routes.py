from flask import Blueprint, jsonify
from flask import request

# Create a Blueprint
main = Blueprint('main', __name__)

@main.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is running!"}), 200

