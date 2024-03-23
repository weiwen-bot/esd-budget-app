from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)

# Configure SQLAlchemy to use the provided database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/pool'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Pool model
class Pool(db.Model):
    __tablename__ = 'pool'

    PoolID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    DateCreation = db.Column(db.Date,nullable=False, default=datetime.now)
    Expiry_Date = db.Column(db.Date, nullable=False)
    Current_amount = db.Column(db.Float, nullable=False)
    Budget = db.Column(db.Float, nullable=False)
    Pool_Type = db.Column(db.String(36), nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String(36), nullable=False)

    def __init__(self,Expiry_Date, Current_amount, Budget, Pool_Type, UserID, Status):
        self.Expiry_Date = Expiry_Date
        self.Current_amount = Current_amount
        self.Budget = Budget
        self.Pool_Type = Pool_Type
        self.UserID = UserID
        self.Status = Status

    def json(self):
        return {
            "PoolID": self.PoolID,
            "DateCreation": self.DateCreation,
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
        return jsonify({"code": 500, "data": data, "message": "An error occurred creating the pool."}), 500

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

# API endpoint to get all pools by UserID



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
