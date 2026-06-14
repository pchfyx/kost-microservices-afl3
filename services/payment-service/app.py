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

@app.route("/payments/health", methods=["GET"])
def health():
    return jsonify({
        "service": "payment-service",
        "status": "running"
    })

@app.route("/payments", methods=["GET"])
def get_payments():
    return jsonify([
        {"id": 1, "tenant": "Budi", "amount": 1500000, "status": "paid"},
        {"id": 2, "tenant": "Siti", "amount": 1500000, "status": "unpaid"}
    ])

@app.route("/payments/pay", methods=["POST", "GET"])
def pay():
    event = {
        "source": "payment-service",
        "type": "PAYMENT_CONFIRMED",
        "message": "Pembayaran kos berhasil dikonfirmasi",
        "tenant": "Budi",
        "amount": 1500000
    }

    success = publish_event(event)

    if success:
        return jsonify({
            "message": "Payment event published to RabbitMQ",
            "event": event
        })

    return jsonify({
        "message": "Failed to publish payment event"
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)