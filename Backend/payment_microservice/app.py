
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
from flask_cors import CORS

app = Flask(__name__)


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

def create_prod():
    stripe.api_key = stripe_keys["secret_key"]
    product = stripe.Product.create(
        name='Testing_prod',
    )
    return product.id

def create_price(PRODUCT_ID):
    stripe.api_key = stripe_keys["secret_key"]
    create_price = stripe.Price.create(
        currency='sgd',
        custom_unit_amount={"enabled": True},
        product=PRODUCT_ID,
    )
    return create_price.id

@app.route("/create-checkout-session", methods=['POST'])
def create_checkout_session():
    domain_url = "http://127.0.0.1:5174"
    stripe.api_key = stripe_keys["secret_key"]

    

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

        prod_id = create_prod()
        price_id = create_price(prod_id)
        

        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "/canceled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[{"price": price_id, "quantity": 1}],
        )
        return jsonify({"sessionId": checkout_session["id"]})
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
    if event['type'] == 'payment_intent.succeeded':
      payment_intent = event['data']['object']
    # ... handle other event types
      print("PaymentIntent was successful!")
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=4242, debug=True)
  print("Running on port 4242...")