from flask import Flask
from flask_socketio import SocketIO
from music_gen.generate import ChoiraGenerate
from song_gen.song_gen import ChoiraSongGenerate
from flask_cors import CORS
# Initialize Flask and Socket.IO
socketio = SocketIO(cors_allowed_origins="*")


choira_generate = ChoiraGenerate(socketio)
choira_song_generate = ChoiraSongGenerate(socketio)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    CORS(app)


    # Register routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Initialize Socket.IO
    socketio.init_app(app)

    return app
