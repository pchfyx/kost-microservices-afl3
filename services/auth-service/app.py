from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/auth/health", methods=["GET"])
def health():
    return jsonify({
        "service": "auth-service",
        "status": "running"
    })

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin123":
        return jsonify({
            "message": "Login successful",
            "token": "demo-jwt-token"
        })

    return jsonify({
        "message": "Invalid username or password"
    }), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)