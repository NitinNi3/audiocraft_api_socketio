from flask_socketio import emit
from app import socketio,choira_generate
from flask import request

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('response', {'message': 'Welcome to the world of Ai'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")


@socketio.on('generate-music-large')
def generate_music_large(data):
    print(f"Received message: {data}")
    user_prompt = data['prompt']
    print("User prompt : ",user_prompt)
    crisp_prompt  = f"A crisp and clear sounding {user_prompt}"
    file_name = choira_generate.generate_music_large(user_prompt,crisp_prompt,data['duration'],request.sid)
    emit('music_generated', {'file_name': file_name})
