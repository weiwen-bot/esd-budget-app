from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/transaction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Transaction(db.Model):
    __tablename__ = 'transaction'

    transactionID = db.Column(db.String(36), primary_key=True)  
    amount = db.Column(db.Float(precision=2), nullable=False)
    status = db.Column(db.String(36))
    transactionDate = db.Column(db.DateTime, nullable=False)
    userID = db.Column(db.String(36), db.ForeignKey('transaction.userID'), nullable=False)
    poolID = db.Column(db.String(36), db.ForeignKey('transaction.poolID'), nullable=False)

    def __init__(self, transactionID, amount, status, transactionDate, userID, poolID):
        self.transactionID = transactionID
        self.amount = amount
        self.status = status
        self.transactionDate = transactionDate
        self.userID = userID
        self.poolID = poolID

    def json(self):
        return {"transactionID": self.transactionID, "amount": self.amount, "status": self.status, "transactionDate": self.transactionDate, "userID": self.userID, "poolID": self.poolID}

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
   

from uuid import uuid4
from datetime import datetime

@app.route("/transactions", methods=['POST'])
def create_Transaction():
    try:
        user_id = request.json.get('userID', None)
        pool_id = request.json.get('poolID', None)
        amount = request.json.get( 'amount')
        status = request.json.get('status')

        if not user_id or not pool_id:
                return jsonify({'code': 400, 'message': 'Missing required fields: userID and poolID'}), 400

        transaction = Transaction(str(uuid4()), amount, status , datetime.utcnow(), user_id, pool_id)
        
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

@app.route("/Transaction/<string:Transaction_id>")
def find_by_Transaction_id(Transaction_id):
    Transaction = db.session.scalars(db.select(Transaction).filter_by(Transaction_id=Transaction_id).limit(1)).first()
    if Transaction:
        return jsonify(
            {
                "code": 200,
                "data": Transaction.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "Transaction_id": Transaction_id
            },
            "message": "Transaction not found."
        }
    ), 404

@app.route("/transactions/<string:transaction_id>", methods=['DELETE'])
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
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)