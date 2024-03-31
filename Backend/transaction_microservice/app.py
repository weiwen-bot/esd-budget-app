
import amqp_connection
import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

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

    def __init__(self, amount, status, userID, poolID, paymentIntent="Empty",refund_status="new"):
        self.amount = amount
        self.status = status
        self.userID = userID
        self.poolID = poolID
        self.paymentIntent = paymentIntent
        self.refund_status = refund_status


    def json(self):
        return {"transactionID": self.transactionID, "amount": self.amount, "status": self.status, "transactionDate": self.transactionDate, "userID": self.userID, "poolID": self.poolID,
                "paymentIntent": self.paymentIntent, "refund_status": self.refund_status}



#get all transactions
@app.route("/transactions")
def get_All_Transactions():
    transactionlist = db.session.scalars(db.select(Transaction)).all()
    


    if len(transactionlist) > 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactionlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No Transactions Found."
        }
    ), 404

#create transaction
@app.route("/transactions", methods=['POST'])
def create_Transaction():
    try:
        user_id = request.json.get('userID', None)
        pool_id = request.json.get('poolID', None)
        amount = request.json.get( 'amount')
        status = request.json.get('status')

        if not user_id or not pool_id:
                return jsonify({'code': 400, 'message': 'Missing required fields: userID and poolID'}), 400

        # transaction = Transaction(str(uuid4()), amount, status , datetime.utcnow(), user_id, pool_id)
        data = request.get_json()
        transaction = Transaction(**data)
        db.session.add(transaction)
        
        db.session.commit()
        return jsonify({'code': 201, 'data': transaction.json()}), 201


    except Exception as e:
        app.logger.exception(f"Error creating transaction: {e}")
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the Transaction. " + str(e)
            }
        ), 500

#get by transaction
@app.route("/transactions/<int:transactionID>")
def find_by_Transaction_id(transactionID):
    transaction = db.session.scalars(db.select(Transaction).filter_by(transactionID=transactionID).limit(1)).first()

    if transaction:
        return jsonify(
            {
                "code": 200,
                "data": transaction.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "Transaction_id": transactionID
            },
            "message": "Transaction not found."
        }
    ), 404


#update transaction
@app.route("/transactions/<int:transactionID>", methods=['PUT'])
def update_transaction(transactionID):
    data = request.get_json()
    transaction = Transaction.query.filter_by(transactionID=transactionID).first()

    if transaction:
        try:
            for key, value in data.items():
                setattr(transaction, key, value)
            db.session.commit()
            return jsonify({"code": 200, "data": transaction.json()})
        except Exception as e:
            return jsonify({"code": 500, "data": data, "message": "An error occurred updating the transaction.", "error":str(e)}), 500
    else:
        return jsonify({"code": 404, "message": "Transaction not found."}), 404

#delete transaction
@app.route("/transactions/<int:transaction_id>", methods=['DELETE'])
def delete_transaction(transaction_id):

    try:
        transaction = Transaction.query.filter_by(transactionID=transaction_id).first()

        if not transaction:
            return jsonify({'code': 404, 'message': 'Transaction not found.'}), 404

        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'code': 200, 'message': 'Transaction deleted successfully.'}), 200

    except Exception as e:
        app.logger.exception(f"Error deleting transaction: {e}")
        return jsonify({'code': 500, 'message': 'An error occurred while deleting the transaction.'}), 500
    

#get transaction by pool
@app.route("/transactions/pool/<int:poolID>")
def get_Transactions_By_Pool(poolID):
    transactionlist = db.session.scalars(db.select(Transaction).filter_by(poolID=poolID)).all()

    if len(transactionlist) > 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactionlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No Transactions Found."
        }
    ), 404

@app.route("/transactions/pool/<int:poolID>/status/<string:refund_status>" , methods=['GET'])
def get_Transactions_By_poolandstatus(poolID,refund_status):
    transactionlist = db.session.scalars(db.select(Transaction).filter_by(poolID=poolID,refund_status=refund_status)).all()

    if len(transactionlist) > 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactionlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No Transactions Found."
        }
    ), 404

@app.route("/transactions/pool/<int:poolID>/status/<string:refund_status>", methods=['PUT'])
def update_Transactions_By_Pool(poolID,refund_status):
    transactionlist = db.session.scalars(db.select(Transaction).filter_by(poolID=poolID,refund_status=refund_status)).all()

    if len(transactionlist) > 0:
        try:
            for transaction in transactionlist:
                transaction.refund_status = "refunded"
            db.session.commit()
            return jsonify({"code": 200, "data": [transaction.json() for transaction in transactionlist]})
        except Exception as e:
            return jsonify({"code": 500, "data": [transaction.json() for transaction in transactionlist], "message": "An error occurred updating the transaction.", "error":str(e)}), 500
    return jsonify(
        {
            "code": 404,
            "message": "No Transactions Found."
        }
    ), 404

# #get transaction by user
# @app.route("/transactions/user/<int:userID>")
# def get_Transactions_By_User(userID):
#     transactionlist = db.session.scalars(db.select(Transaction).filter_by(userID=userID)).all()

#     if len(transactionlist) > 0:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "transactions": [transaction.json() for transaction in transactionlist]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "No Transactions Found."
#         }
#     ), 404

    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5003, debug=True)