
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
import os
import stripe

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from invokes import invoke_http
app = Flask(__name__)

# CORS(app)
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "webhook_secret": os.environ["WEB_HOOK_SECRET"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"]
}

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.

stripe.api_key = stripe_keys["secret_key"]

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = stripe_keys["webhook_secret"]

CORS(app, resources={r'/*': {'origins': '*'}})



@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

def update_prod(pool_name, max_amt):
    stripe.api_key = stripe_keys["secret_key"]
    product = stripe.Product.modify(
        "prod_PozyyQarWAcdS1",
        name=f'Payment are made to {pool_name}',
        description = f'Maximum amount is {max_amt/100} SGD',
        
    )
    return product.id

def create_price(max_amt,prod_id):
    stripe.api_key = stripe_keys["secret_key"]
    create_price = stripe.Price.create(
        currency="sgd",
        product = prod_id,
        custom_unit_amount = {"enabled": True,"maximum":max_amt}
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
    max_amt = data['remaining'] * 100
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
            success_url=domain_url + "/success?session_id={CHECKOUT_SESSION_ID}",
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

    # Handle the event
    # if event['type'] == 'payment_intent.succeeded':
    #   payment_intent = event['data']['object']
    #   print("PaymentIntent was successful!")
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        forward_webhook(event)
        return jsonify({"code":200,"session":session})
    # else:
    #   print('Unhandled event type {}'.format(event['type']))

    

    return jsonify(success=True), 200

def forward_webhook(payload):
    try:
        response = invoke_http("http://payment_manage:5101/webhook", method='POST', json=payload)
        return jsonify({'status': 'forwarded', 'message': response}), 200
    except Exception as e:
        return jsonify(error=str(e)), 401
    

    

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=4242, debug=True)
  print("Running on port 4242...")