
# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

import json
import stripe

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from invokes import invoke_http
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from os import environ
import os
from sqlalchemy.sql import func
from datetime import datetime
import json

app = Flask(__name__)


# CORS(app)
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "webhook_secret": os.environ["WEB_HOOK_SECRET"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"]
}

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

stripe.api_key = stripe_keys["secret_key"]

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = stripe_keys["webhook_secret"]

CORS(app, resources={r'/*': {'origins': '*'}})


class Refund(db.Model):
    __tablename__ = 'refund'

    refundID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    created = db.Column(db.DateTime,nullable=False, default=datetime.now)
    amount = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    PoolID = db.Column(db.Integer, nullable=False)

    def __init__(self,amount,status, UserID, PoolID):
        self.amount = amount
        self.status = status
        self.UserID = UserID
        self.PoolID = PoolID



    def json(self):
        return {
            "amount": self.amount,
            "status": self.status,
            "UserID": self.UserID,
            "PoolID": self.PoolID
        }



@app.route("/config", methods=['GET'])
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

def update_prod(pool_name, max_amt):
    stripe.api_key = stripe_keys["secret_key"]
    product = stripe.Product.modify(
        "prod_PozyyQarWAcdS1",
        name=f'Payment are made to {pool_name}',
        description = f'Maximum amount is {max_amt} SGD',
        
    )
    return product.id

def create_price(max_amt,prod_id):
    stripe.api_key = stripe_keys["secret_key"]
    create_price = stripe.Price.create(
        currency="sgd",
        product = prod_id,
        custom_unit_amount = {"enabled": True,"maximum":max_amt * 100}
    )
    return create_price.id

@app.route("/create-checkout-session", methods=['POST'])
def create_checkout_session():
    domain_url = "http://127.0.0.1:5173"
    stripe.api_key = stripe_keys["secret_key"]

    data = json.loads(request.data)

   
    # max_amt = 2 * 100
    # pool_name = 'Pool Name'
    # userid = 1
    # poolid = 1
     #Amt in cents
    max_amt = data['remaining']
    pool_name = data['pool_name']
    userid = data['UserID']
    poolid = data['PoolID']

    try:
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

        prod_id = update_prod(pool_name,max_amt)
        print("product Updated")
        price_id = create_price(max_amt,prod_id)
        print("price_id Updated")

        checkout_session = stripe.checkout.Session.create(
            # success_url=domain_url + "/success?session_id={CHECKOUT_SESSION_ID}",
            success_url=domain_url + f"/ipp/{poolid}",
            cancel_url=domain_url + "/canceled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[{"price": price_id, "quantity": 1}],
            # int passed with be convereted to string
            metadata={"UserID": userid, "PoolID": poolid}


        )
        print(checkout_session)
        return jsonify({"sessionId": checkout_session["id"],"url":checkout_session["url"]})
    except Exception as e:
        return jsonify(error=str(e)), 403
    

@app.route("/refund_mul", methods=['POST'])
def refund_mul():
    data = request.get_json()["refunds"]
    print(data,"REFDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
    for refund in data:
        refund_obj = stripe.Refund.create(
        payment_intent=refund['payment_intent'],
        metadata=refund["metadata"],
        amount=refund["amt"],
            
        )
        
    return jsonify({"code": 201, "data": data})

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'status': 'error', 'message': 'Invalid payload.'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        forward_webhook(event)
        return jsonify({"code":200,"session":session})
    elif event['type'] == 'charge.refund.updated':
        res = storeRefund(event)
        return f"Successful Recording of Refund {res}"
    return jsonify(success=True), 200

def forward_webhook(payload):
    try:
        response = invoke_http("http://payment_manage:5101/webhook", method='POST', json=payload)
        return jsonify({'status': 'forwarded', 'message': response}), 200
    except Exception as e:
        return jsonify(error=str(e)), 401
    
@app.route('/refund/<int:poolid>', methods=['GET'])
def get_all_refund(poolid):
    refundlist = db.session.scalars(db.select(Refund).filter_by(PoolID=poolid)).all()

    if len(refundlist) > 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "refunds": [ref.json() for ref in refundlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No refunds Found."
        }
    ), 404

@app.route('/delete_refund', methods=['DELETE'])
def delete_all_refund():
    try:
        db.session.query(Refund).delete()
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "All Refunds have been deleted."
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while deleting all Refunds."
            }
        ), 500    

def storeRefund(event):
    print("Refund: Recording an Refund")
    print(event)
    userid = event['data']['object']['metadata']['UserID']
    poolid = event['data']['object']['metadata']['PoolID']
    noti = Refund(
    amount = event['data']['object']['amount'] / 100 ,
    status = 'refunded',
    UserID = userid,
    PoolID = poolid,
    )
    try:
        db.session.add(noti)
        db.session.commit()
    except Exception as e:
        print(e)
        print("Transaction: Error recording an Refund")
    

    

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=4242, debug=True)
  print("Running on port 4242...")