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
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

poolmap_queue = environ.get('poolmap_queue') or 'pool_mapping'

db = SQLAlchemy(app)

CORS(app)


class PoolMapping(db.Model):
    __tablename__ = 'poolmapping'

    PoolID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, primary_key=True)

    def __init__(self, PoolID, UserID):
        self.PoolID = PoolID
        self.UserID = UserID

    def json(self):
        return {
            "PoolID": self.PoolID,
            "UserID": self.UserID
        }
    

def receivePoolMapping(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=poolmap_queue, on_message_callback=callback, auto_ack=True)
        print('pool mapping: Consuming from queue:', poolmap_queue)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"pool mapping: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("pool mapping: Program interrupted by user.") 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\npool mapping: Received an pool mapping by " + __file__)
    processPoolMapping(json.loads(body))
    print()

def processPoolMapping(poolmap):
    print("pool mapping: Recording an pool mapping")
    print(poolmap)
    new_pool = PoolMapping(PoolID=poolmap['PoolID'], UserID=poolmap['UserID'])

    try:
        db.session.add(new_pool)
        db.session.commit()
    except Exception as e:
        print(e)
        print("pool mapping: Error recording an pool mapping")

if __name__ == '__main__':
    print("activity_log: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("activity_log: Connection established successfully")
    channel = connection.channel()
    with app.app_context():
        receivePoolMapping(channel)