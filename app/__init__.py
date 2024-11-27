from flask import Flask
from flask_socketio import SocketIO
from music_gen.generate import ChoiraGenerate
# Initialize Flask and Socket.IO
socketio = SocketIO(cors_allowed_origins="*")


choira_generate = ChoiraGenerate(socketio)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'

    # Register routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Initialize Socket.IO
    socketio.init_app(app)

    return app
