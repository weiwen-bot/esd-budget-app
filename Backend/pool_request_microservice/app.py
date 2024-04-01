from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from sqlalchemy.sql import func
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)

# Configure SQLAlchemy to use the provided database URL

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root@localhost:3306/pool_request"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

CORS(app)

# Define the Pool model
class pool_request(db.Model):
    __tablename__ = 'pool_request'

    pool_requestID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    created = db.Column(db.DateTime,nullable=False, default=datetime.now)
    PoolID = db.Column(db.Integer, nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(36), nullable=False)

    def __init__(self, PoolID, UserID, status):
        self.PoolID = PoolID
        self.UserID = UserID
        self.status = status

    def json(self):
        return {
            "pool_requestID": self.pool_requestID,
            "PoolID": self.PoolID,
            "created": self.created,
            "UserID": self.UserID,
            "status": self.status
        }


# Get pool request for each user
@app.route("/pool_request/user/<int:UserId>", methods=['GET'])
def get_by_user(UserId):
    pool_requests = pool_request.query.filter_by(UserID=UserId)
    pool_requests = [row.json() for row in pool_requests]

    if pool_requests:
        try:
            return jsonify({"code": 200, "data": pool_requests})
        except Exception as e:
            return jsonify({"code": 500, "data": pool_requests, "message": "An error occurred updating the pool_request.", "error":str(e)}), 500
    else:
        return jsonify({"code": 404, "message": "Pool not found."}), 404
    

@app.route("/pool_request/pool/<int:PoolID>", methods=['GET'])
def get_by_req_pool(PoolID):
    pool_requests = pool_request.query.filter_by(PoolID=PoolID)
    pool_requests = [row.json() for row in pool_requests]

    if pool_requests:
        try:
            return jsonify({"code": 200, "data": pool_requests})
        except Exception as e:
            return jsonify({"code": 500, "data": pool_requests, "message": "An error occurred getting the pool_request.", "error":str(e)}), 500
    else:
        return jsonify({"code": 404, "message": "Pool_req not found."}), 404
    
    

# create pool request for the poolid and userid
@app.route("/pool_request",methods=['POST'])
def create_poolrequest():
    try:
        data = request.get_json()
        userid = data['UserID']
        poolid = data['PoolID']
        
        pool_requests = pool_request.query.filter_by(UserID=userid,PoolID=poolid).first()
        if not pool_requests:

            pool_requests = pool_request(poolid,userid,'pending')
            db.session.add(pool_requests)

            db.session.commit()
            return jsonify({"code": 201, "data": pool_requests.json()})
        else:
            return jsonify({"code": 400, "message": "Pool request already exists."}), 400
    except Exception as e:
            return jsonify({"code": 500, "data": data, "message": "An error occurred updating the pool_request.", "error":str(e)}), 500
    

@app.route("/pool_request/multiple",methods=['POST'])
def create_mul_poolrequest():
    try:
        data = request.get_json()
        for invite in data:
            pool_requests = pool_request(invite['poolid'],invite['userid'],'pending')
            db.session.add(pool_requests)
        db.session.commit()
        return jsonify({"code": 201, "data": data})
    except Exception as e:
        return jsonify({"code": 500, "data": data, "message": "An error occurred updating the pool_request.", "error":str(e)}), 500

#accept or decline friend request
@app.route("/pool_request",methods=['PUT'])
def update_poolrequest():
    try:
        data = request.get_json()
        userid = data['UserID']
        poolid = data['PoolID']
        status = data['status']

        pool_requests = db.session.scalars(db.select(pool_request).filter_by(UserID=userid,PoolID=poolid).limit(1)).first()
        print(pool_request.query.filter_by(PoolID=1).first())
        print(pool_request.query.filter_by(PoolID=1).filter_by(UserID=5).first())
        if pool_requests:
            pool_requests.status = status
            db.session.commit()
            return jsonify({"code": 200, "data": pool_requests.json()})
        else:
            return jsonify({
            "code": 404,
            "data": {
                "UserID": userid,
                "PoolID": poolid
            },
            "message": "request not found."}), 404
    except Exception as e:
        return jsonify({"code": 500, "data": data, "message": "An error occurred updating the pool_request.", "error":str(e)}), 500
    

# delete pool request of user
@app.route("/pool_request",methods=['DELETE'])
def delete_poolrequest():
    try:
        data = request.get_json()
        userid = data['UserID']
        poolid = data['PoolID']

        pool_requests = pool_request.query.filter_by(UserID=userid,PoolID=poolid).first()
        db.session.delete(pool_requests)
        db.session.commit()
        return jsonify({"code": 200, "data": pool_requests.json()})
    except Exception as e:
        return jsonify({"code": 500, "data": data, "message": "An error occurred updating the pool_request.", "error":str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
