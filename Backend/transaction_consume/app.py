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
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/transaction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

transaction_queue = environ.get('transaction_queue') or 'transaction'

db = SQLAlchemy(app)

CORS(app)


class Transaction(db.Model):
    __tablename__ = 'transaction'

    transactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    amount = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.String(36))
    transactionDate = db.Column(db.DateTime, nullable=False, default=datetime.now)
    userID = db.Column(db.Integer, db.ForeignKey('transaction.userID'), nullable=False)
    poolID = db.Column(db.Integer, db.ForeignKey('transaction.poolID'), nullable=False)
    paymentIntent = db.Column(db.String(255), nullable=True)
    refund_status = db.Column(db.String(36), nullable=True)

    def __init__(self, amount, status, userID, poolID, paymentIntent="Empty",refund_status="Empty"):
        self.amount = amount
        self.status = status
        self.userID = userID
        self.poolID = poolID
        self.paymentIntent = paymentIntent
        self.refund_status = refund_status


    def json(self):
        return {"transactionID": self.transactionID, "amount": self.amount, "status": self.status, "transactionDate": self.transactionDate, "userID": self.userID, "poolID": self.poolID,
                "paymentIntent": self.paymentIntent, "refund_status": self.refund_status}


    

def receiveTransaction(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=transaction_queue, on_message_callback=callback, auto_ack=True)
        print('Transaction: Consuming from queue:', transaction_queue)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"Transaction: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("Transaction: Program interrupted by user.") 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nTransaction: Received an Transaction by " + __file__)
    processTransaction(json.loads(body))
    print()

def processTransaction(notif):
    print("Transaction: Recording an Transaction")
    print(notif)
    if notif['notif_type'] == "refund":
        for transaction in notif['batchmessage']:
            recordTransaction(transaction)
        return 200
        
    recordTransaction(notif)
    # noti = Transaction(
    # amount = notif['amount_total'],
    # status = notif['payment_status'],
    # userID = notif['UserID'],
    # poolID = notif['PoolID'],
    # paymentIntent= notif['payment_intent']
    # )
    # try:
    #     db.session.add(noti)
    #     db.session.commit()
    # except Exception as e:
    #     print(e)
    #     print("Transaction: Error recording an Transaction")

def recordTransaction(transaction):
    trans = Transaction(
    amount = transaction['amount_total'],
    status = transaction['payment_status'],
    userID = transaction['UserID'],
    poolID = transaction['PoolID'],
    paymentIntent= transaction['payment_intent']
    )
    try:
        db.session.add(trans)
        db.session.commit()
    except Exception as e:
        print(e)
        print("Transaction: Error recording an Transaction")


if __name__ == '__main__':
    print("activity_log: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("activity_log: Connection established successfully")
    channel = connection.channel()
    with app.app_context():
        receiveTransaction(channel)