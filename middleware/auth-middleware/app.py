from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/private/health", methods=["GET"])
def private_health():
    token = request.headers.get("Authorization")

    if token != "Bearer demo-jwt-token":
        return jsonify({
            "message": "Unauthorized. Missing or invalid token."
        }), 401

    return jsonify({
        "service": "auth-middleware",
        "status": "authorized",
        "message": "Token is valid"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)