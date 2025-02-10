from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

data_store = []  # Store name & age data

@app.route("/")
def index():
    return render_template("index.html")  # Load frontend

@socketio.on("connect")
def handle_connect():
    socketio.emit("initialize", data_store)  # Send stored data when a user connects

@socketio.on("newEntry")
def handle_new_entry(data):
    data_store.append(data)
    socketio.emit("newEntry", data)  # Broadcast update to all clients

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
