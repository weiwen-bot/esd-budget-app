
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

@app.route("/payment", methods=['POST'])
def create_payment():
   response = invoke_http("http://payment:4242/create-checkout-session", method='POST', json=request.json)
   return {"redirect":response['url']}

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_json()
    print(payload,"HeELLLO PAYMENT HEREE")
    # resp = invoke_http("http://payment:4242/webhook", method='POST', json=payload)
    return jsonify({"resp":payload})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5101, debug=True)
  print("Running on port 5101...")