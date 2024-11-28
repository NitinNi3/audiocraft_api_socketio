# -*- coding: utf-8 -*-
from app import create_app, socketio
from app.socket_events import *  # Import socket event handlers

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002, debug=False)
