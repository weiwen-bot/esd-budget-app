#!/usr/bin/env python3
import amqp_connection
import uuid
import json
import pika
from os import environ
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from flask import current_app, jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/notification'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Notification(db.Model):
    __tablename__ = 'notification'

    notificationID = db.Column(db.String(36), primary_key=True)
    notificationType = db.Column(db.String(36), nullable=False)
    senderID = db.Column(db.String(36), nullable=False)
    receiverID = db.Column(db.String(36), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notificationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(36), nullable=False, default='unread')

    def __init__(self, notification_type, sender_id, receiver_id, message, status):
        self.notificationID = str(uuid.uuid4())
        self.notificationType = notification_type
        self.senderID = sender_id   
        self.receiverID = receiver_id
        self.message = message
        self.status = status

    def json(self):
        return {
            'notificationID': self.notificationID,
            'notificationType': self.notificationType,
            'senderID': self.senderID,
            'receiverID': self.receiverID,
            'message': self.message,
            'notificationDate': self.notificationDate,
            'status': self.status,
        }

e_queue_name = environ.get('Notification') or 'Notification'

def receiveNotification():
    try:
        connection = amqp_connection.create_connection()
        channel = connection.channel()

        try:
            channel.queue_declare(queue=e_queue_name, durable=True)

            # Bind the queue to the exchange
            exchange_name = 'Notification'
            channel.queue_bind(exchange=exchange_name, queue=e_queue_name, routing_key='#')

            def callback(channel, method, properties, body):
                print(json.loads(body), "hello")
                try:
                    msg = json.loads(body)
                    
                    new_notification = Notification(
                        notification_type = "new", 
                        sender_id = msg["user_id"], 
                        receiver_id = msg["user_id"],
                        message = "blank",
                        status = msg["status"]
                    )
                    db.session.add(new_notification)
                    db.session.commit()

                except Exception as e:
                    print(f"Error processing message: {e}")

            
            channel.basic_consume(queue=e_queue_name, on_message_callback=callback, auto_ack=True)

            print('notification microservice: Consuming from queue:', e_queue_name)
            channel.start_consuming()

        except KeyboardInterrupt:
            print("notification microservice: Program interrupted by user.")

    except pika.exceptions.AMQPError as e:
        print(f"notification microservice: Failed to connect: {e}")
    except Exception as e:
        print(f"notification microservice: Failed to consume messages: {e}")

@app.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    response = []
    for notification in notifications:
        response.append(notification.json())
    return jsonify(response)

@app.route('/notifications', methods=['POST'])
def post_notification():
    notification_data = request.get_json()

    try:
        notification_id = db.session.query(func.coalesce(func.max(Notification.notificationID), 0) + 1)[0][0]
        notification_type = notification_data.get('notificationType')
        sender_id = notification_data.get('senderID')
        receiver_id = notification_data.get('receiverID')
        message = notification_data.get('message')

        if notification_type and sender_id and receiver_id and message:
            new_notification = Notification(
                notification_type=notification_type,
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message
            )

            db.session.add(new_notification)
            db.session.commit()

            print(f"New notification with ID {new_notification.notificationID} has been posted.")

            return jsonify({'success': True, 'message': 'New notification has been posted.'}), 201

        else:
            print("One or more required fields are missing.")
            return jsonify({'success': False, 'message': 'One or more required fields are missing.'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Error posting notification:")
        return jsonify({'success': False, 'message': 'Error posting notification', 'error':  str(e)}), 500
    
@app.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.filter_by(notification_id=notification_id).first()
    if notification:
        db.session.delete(notification)
        db.session.commit()
        print(f"Notification with ID {notification_id} has been deleted.")
        return jsonify({'success': True, 'message': 'Notification has been deleted.'}), 200
    else:
        print(f"Notification with ID {notification_id} not found.")
        return jsonify({'success': False, 'message': 'Notification not found.'}), 404

if __name__ == "__main__":
    with app.app_context():
        receiveNotification()
    app.run(host="0.0.0.0", port="5005", debug=True)