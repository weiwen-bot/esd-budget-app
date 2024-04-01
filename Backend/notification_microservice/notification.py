#!/usr/bin/env python3

import json
import pika
from os import environ
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

    notificationID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    notificationType = db.Column(db.String(36), nullable=False)
    receiverID = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    notificationDate = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(36), nullable=False)

    def __init__(self, notification_type, receiver_id, message, status):
        self.notificationType = notification_type
        self.receiverID = receiver_id
        self.message = message
        self.status = status

    def json(self):
        return {
            'notificationID': self.notificationID,
            'notificationType': self.notificationType,
            'receiverID': self.receiverID,
            'message': self.message,
            'notificationDate': self.notificationDate,
            'status': self.status,
        }

# e_queue_name = environ.get('Notification') or 'Notification'

# def receiveNotification():
#     try:
#         connection = amqp_connection.create_connection()
#         channel = connection.channel()

#         try:
#             channel.queue_declare(queue=e_queue_name, durable=True)

#             # Bind the queue to the exchange
#             exchange_name = 'Notification'
#             channel.queue_bind(exchange=exchange_name, queue=e_queue_name, routing_key='#')

#             def callback(channel, method, properties, body):
#                 print(json.loads(body), "hello")
#                 try:
#                     msg = json.loads(body)
                    
#                     new_notification = Notification(
#                         notification_type = "new", 
#                         sender_id = msg["user_id"], 
#                         receiver_id = msg["user_id"],
#                         message = "blank",
#                         status = msg["status"]
#                     )
#                     db.session.add(new_notification)
#                     db.session.commit()

#                 except Exception as e:
#                     print(f"Error processing message: {e}")

            
#             channel.basic_consume(queue=e_queue_name, on_message_callback=callback, auto_ack=True)

#             print('notification microservice: Consuming from queue:', e_queue_name)
#             channel.start_consuming()

#         except KeyboardInterrupt:
#             print("notification microservice: Program interrupted by user.")

#     except pika.exceptions.AMQPError as e:
#         print(f"notification microservice: Failed to connect: {e}")
#     except Exception as e:
#         print(f"notification microservice: Failed to consume messages: {e}")




@app.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = Notification.query.all()
    response = []
    for notification in notifications:
        response.append(notification.json())
    return jsonify(response)

@app.route('/notifications/<int:receiverID>', methods=['GET'])
def get_notifications_by_receiver(receiverID):
    notifications = Notification.query.filter_by(receiverID=receiverID).all()
    if notifications:
        try:
        
            response = []
            for notification in notifications:
                response.append(notification.json())
            return jsonify({"code":200,"data":response}), 200
        
        except Exception as e:
            return jsonify({"code": 500, "message": "An error occurred retrieving notifications.", "error": str(e)}), 500
    return jsonify({"code": 404, "message": "Notification not found."}), 404


@app.route("/notifications", methods=['POST'])
def create_notification():
    data = request.get_json()
    notification_type = data.get('notificationType')
    receiver_id = data.get('receiverID')
    message = data.get('message')
    status = data.get('status')

    new_notification = Notification(notification_type, receiver_id, message, status)

    try:
        db.session.add(new_notification)
        db.session.commit()
        return jsonify({"code": 201, "data": new_notification.json()}), 201
    except Exception as e:
        print(e)
        return jsonify({"code": 500, "data": data, "message": str(e)}), 500

#delete notification
@app.route("/notifications/<int:notificationID>", methods=['DELETE'])
def delete_notification(notificationID):
    notification = Notification.query.filter_by(notificationID=notificationID).first()
    if notification:
        try:
            db.session.delete(notification)
            db.session.commit()
            return jsonify({"code": 200, "message": "Notification deleted successfully."})
        except Exception as e:
            return jsonify({"code": 500, "message": "An error occurred deleting the notification.", "error": str(e)}), 500
    return jsonify({"code": 404, "message": "Notification not found."}), 404


if __name__ == "__main__":
    # with app.app_context():
    #     receiveNotification()
    app.run(host="0.0.0.0", port="5005", debug=True)