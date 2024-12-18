from app import create_app, socketio
from app.socket_events import *

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002, allow_unsafe_werkzeug=True)
