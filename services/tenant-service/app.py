from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/tenants/health", methods=["GET"])
def health():
    return jsonify({
        "service": "tenant-service",
        "status": "running"
    })

@app.route("/tenants", methods=["GET"])
def get_tenants():
    return jsonify([
        {"id": 1, "name": "Budi", "room": "A102"},
        {"id": 2, "name": "Siti", "room": "B201"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)