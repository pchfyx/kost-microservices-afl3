from flask import Flask, jsonify, request

app = Flask(__name__)

live_messages = []

@app.route("/websocket/health", methods=["GET"])
def health():
    return jsonify({
        "service": "websocket-service",
        "status": "running",
        "note": "This service simulates live push notification endpoint"
    })

@app.route("/websocket/push", methods=["POST"])
def push_message():
    data = request.get_json(silent=True) or {}
    live_messages.append(data)

    print("WebSocket push received:", data)

    return jsonify({
        "message": "Live notification pushed to WebSocket layer",
        "data": data
    })

@app.route("/websocket/messages", methods=["GET"])
def get_messages():
    return jsonify(live_messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)