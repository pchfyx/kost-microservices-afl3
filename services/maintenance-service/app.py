from flask import Flask, jsonify
import pika
import json
import time

app = Flask(__name__)

def publish_event(event_data):
    for attempt in range(10):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    credentials=pika.PlainCredentials("admin", "admin123")
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue="kost_events", durable=True)

            channel.basic_publish(
                exchange="",
                routing_key="kost_events",
                body=json.dumps(event_data),
                properties=pika.BasicProperties(delivery_mode=2)
            )

            connection.close()
            return True

        except Exception as e:
            print(f"RabbitMQ not ready, retrying... {attempt + 1}/10 | {e}")
            time.sleep(2)

    return False

@app.route("/maintenance/health", methods=["GET"])
def health():
    return jsonify({
        "service": "maintenance-service",
        "status": "running"
    })

@app.route("/maintenance", methods=["GET"])
def get_maintenance():
    return jsonify([
        {"id": 1, "room": "A102", "issue": "AC rusak", "status": "pending"},
        {"id": 2, "room": "B201", "issue": "Lampu mati", "status": "done"}
    ])

@app.route("/maintenance/update", methods=["POST", "GET"])
def update_maintenance():
    event = {
        "source": "maintenance-service",
        "type": "MAINTENANCE_UPDATED",
        "message": "Status maintenance kamar A102 diperbarui",
        "room": "A102",
        "issue": "AC rusak",
        "status": "in_progress"
    }

    success = publish_event(event)

    if success:
        return jsonify({
            "message": "Maintenance event published to RabbitMQ",
            "event": event
        })

    return jsonify({
        "message": "Failed to publish maintenance event"
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)