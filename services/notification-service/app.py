from flask import Flask, jsonify
import pika
import json
import threading
import time
import requests

app = Flask(__name__)

notifications = []

def forward_to_websocket(event):
    try:
        response = requests.post(
            "http://websocket-service:5000/websocket/push",
            json=event,
            timeout=5
        )
        print("Forwarded to websocket-service:", response.status_code)
    except Exception as e:
        print("Failed to forward to websocket-service:", e)

def consume_events():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    credentials=pika.PlainCredentials("admin", "admin123")
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue="kost_events", durable=True)

            def callback(ch, method, properties, body):
                event = json.loads(body.decode("utf-8"))

                notification = {
                    "title": "New Kost Event",
                    "event": event
                }

                notifications.append(notification)
                print("Notification received:", notification)

                forward_to_websocket(notification)
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(
                queue="kost_events",
                on_message_callback=callback
            )

            print("Notification Service is waiting for RabbitMQ events...")
            channel.start_consuming()

        except Exception as e:
            print("RabbitMQ connection failed, retrying in 5 seconds...", e)
            time.sleep(5)

@app.route("/notifications/health", methods=["GET"])
def health():
    return jsonify({
        "service": "notification-service",
        "status": "running"
    })

@app.route("/notifications", methods=["GET"])
def get_notifications():
    return jsonify(notifications)

if __name__ == "__main__":
    thread = threading.Thread(target=consume_events)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=5000)