from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy.sql import func
from datetime import datetime
from flask_cors import CORS 
import amqp_connection
import pika
import json

app = Flask(__name__)

# Configure SQLAlchemy to use the provided database URL
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/notification'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

notification_queue = environ.get('notification_queue') or 'Notification'

db = SQLAlchemy(app)

CORS(app)


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


    

def receiveNotification(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=notification_queue, on_message_callback=callback, auto_ack=True)
        print('Notification: Consuming from queue:', notification_queue)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"Notification: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("Notification: Program interrupted by user.") 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nNotification: Received an Notification by " + __file__)
    processNotification(json.loads(body))
    print()

def processNotification(notif):
    print("Notification: Recording an Notification")
    print(notif)
    msg = f"{notif['UserName']} has {notif['status']} your request to join pool {notif['PoolName']}"
    noti = Notification(
        notification_type='hello',
    receiver_id=notif['PoolOwner'],
    message=msg,
    status='New'
    )
    try:
        db.session.add(noti)
        db.session.commit()
    except Exception as e:
        print(e)
        print("Notification: Error recording an Notification")

if __name__ == '__main__':
    print("activity_log: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("activity_log: Connection established successfully")
    channel = connection.channel()
    with app.app_context():
        receiveNotification(channel)