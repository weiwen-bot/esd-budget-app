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

# Initialize SQLAlchemy
db = SQLAlchemy(app)

CORS(app)

# Define the Pool model
class Pool(db.Model):
    __tablename__ = 'pool'

    PoolID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    DateCreation = db.Column(db.DateTime,nullable=False, default=datetime.now)
    pool_name = db.Column(db.String(50), nullable=False)
    pool_desc = db.Column(db.String(50), nullable=False)
    Expiry_Date = db.Column(db.Date, nullable=False)
    Current_amount = db.Column(db.Float, nullable=False)
    Budget = db.Column(db.Float, nullable=False)
    Pool_Type = db.Column(db.String(36), nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String(36), nullable=False)

    def __init__(self,pool_name,pool_desc,Expiry_Date, Current_amount, Budget, Pool_Type, UserID, Status):
        self.Expiry_Date = Expiry_Date
        self.Current_amount = Current_amount
        self.Budget = Budget
        self.Pool_Type = Pool_Type
        self.UserID = UserID
        self.Status = Status
        self.pool_name = pool_name
        self.pool_desc = pool_desc

    def json(self):
        return {
            "PoolID": self.PoolID,
            "DateCreation": self.DateCreation,
            'pool_name': self.pool_name,
            'pool_desc': self.pool_desc,
            "Expiry_Date": self.Expiry_Date,
            "Current_amount": self.Current_amount,
            "Budget": self.Budget,
            "Pool_Type": self.Pool_Type,
            "UserID": self.UserID,
            "Status": self.Status
        }

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



# API endpoint to create a new pool
@app.route("/Pool", methods=['POST'])
def create_pool():
    data = request.get_json()
    new_pool = Pool(**data)

    try:
        db.session.add(new_pool)
        db.session.commit()
        return jsonify({"code": 201, "data": new_pool.json()}), 201
    except Exception as e:
        print(e)
        return jsonify({"code": 500, "data": data, "message": str(e)}), 500

# API endpoint to update an existing pool
@app.route("/Pool/<int:PoolID>", methods=['PUT'])
def update_pool(PoolID):
    data = request.get_json()
    pool = Pool.query.filter_by(PoolID=PoolID).first()

    if pool:
        try:
            for key, value in data.items():
                setattr(pool, key, value)
            db.session.commit()
            return jsonify({"code": 200, "data": pool.json()})
        except Exception as e:
            return jsonify({"code": 500, "data": data, "message": "An error occurred updating the pool.", "error":str(e)}), 500
    else:
        return jsonify({"code": 404, "message": "Pool not found."}), 404

# API endpoint to get all pools
@app.route("/Pool", methods=['GET'])
def get_all_pools():
    pool_list = Pool.query.all()
    if pool_list:
        return jsonify({"code": 200, "data": {"pools": [pool.json() for pool in pool_list]}})
    return jsonify({"code": 404, "message": "There are no pools."}), 404

@app.route("/pool_mapping", methods=['GET'])
def get_all_poolmapping():
    pool_list = PoolMapping.query.all()
    if pool_list:
        return jsonify({"code": 200, "data": {"pool_mapping": [pool.json() for pool in pool_list]}})
    return jsonify({"code": 404, "message": "There are no pools."}), 404


# API endpoint to get a specific pool by PoolID
@app.route("/pool_mapping/<int:PoolID>", methods=['GET'])
def get_all_poolmapping_id(PoolID):
    try:
        pool_map = PoolMapping.query.filter_by(PoolID=PoolID).all()
    except Exception as e:
        return jsonify({"code": 500, "message": "An error occurred getting the pool mapping.", "error": str(e)}), 500
    if pool_map:
        return jsonify({"code": 200, "data": [pool.json() for pool in pool_map]})
    return jsonify({"code": 404, "message": "Pool not found."}), 404

# API endpoint to get a specific pool by PoolID
@app.route("/Pool/<int:PoolID>", methods=['GET'])
def get_pool(PoolID):
    pool = Pool.query.filter_by(PoolID=PoolID).first()
    if pool:
        return jsonify({"code": 200, "data": pool.json()})
    return jsonify({"code": 404, "message": "Pool not found."}), 404

#delete pool
@app.route("/Pool/<int:PoolID>", methods=['DELETE'])
def delete_pool(PoolID):
    pool = Pool.query.filter_by(PoolID=PoolID).first()
    if pool:
        try:
            db.session.delete(pool)
            db.session.commit()
            return jsonify({"code": 200, "message": "Pool deleted successfully."})
        except Exception as e:
            return jsonify({"code": 500, "message": "An error occurred deleting the pool.", "error": str(e)}), 500
    return jsonify({"code": 404, "message": "Pool not found."}), 404





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
