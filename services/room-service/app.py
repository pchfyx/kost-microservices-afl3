from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/rooms/health", methods=["GET"])
def health():
    return jsonify({
        "service": "room-service",
        "status": "running"
    })

@app.route("/rooms", methods=["GET"])
def get_rooms():
    return jsonify([
        {"id": 1, "room_number": "A101", "status": "available"},
        {"id": 2, "room_number": "A102", "status": "occupied"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)