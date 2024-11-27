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

    # prompt enhnace here

    choira_generate.generate_music_large(data.prompt,data.duration,request.sid)
    emit('response', {'message': data})
