
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
import os, sys
import json
import os
import stripe
import pika
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from invokes import invoke_http
import amqp_connection
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

exchangename = "payment_status" # exchange name
exchangetype = "topic" # use a 'topic' exchange to enable interaction
connection = amqp_connection.create_connection() 
channel = connection.channel()

if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0) 

@app.route("/payment", methods=['POST'])
def create_payment():
    data = request.json
    '''
    {
        "pool_name": "pool_name",
        "UserID": 1,
        "PoolID": 1,
        "remaining": 100 * 100
    }
    '''
    print(data)
    max_amt = data['remaining'] * 100
    pool_name = data['pool_name']
    userid = data['UserID']
    poolid = data['PoolID']
    response = invoke_http("http://payment:4242/create-checkout-session", method='POST', json=data)
    print(response)
    return {"redirect":response['url']}

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        payload = request.get_json()['data']['object']
        print(payload,"HeELLLO PAYMENT HEREE")

        msg_dict = {}
        fields_to_send = ['amount_total', 'payment_intent', 'payment_status']
        for x in fields_to_send:
            if x in payload:
                msg_dict[x] = payload[x]
        
        msg_dict['notif_type'] = 'payment_status'
        msg_dict['UserID'] = payload['metadata']['UserID']
        msg_dict['PoolID'] = payload['metadata']['PoolID']

        pool_info = invoke_http("http://pool:5001/Pool/"+msg_dict['PoolID'], method='GET')
        user_info = invoke_http("http://user:5004/user/"+msg_dict['UserID'], method='GET')
        msg_dict['PoolOwner'] = pool_info['data']['UserID']
        msg_dict['UserName'] = user_info['data']['UserName']
        msg_dict['PoolName'] = pool_info['data']['pool_name']
        msg_dict['Budget'] = pool_info['data']['Budget']
        msg_dict['payment_intent'] = payload['payment_intent']
        current_amount = pool_info['data']['Current_amount']
        message = json.dumps(msg_dict)

        if msg_dict['payment_status'] == 'paid':
            channel.basic_publish(exchange=exchangename, routing_key="payment.success", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
            print("\nRequest status ({:d}) published to the RabbitMQ Exchange:".format(
                200), msg_dict)
            
            current_amount = current_amount + msg_dict['amount_total']
            update_pool_res = invoke_http("http://pool:5001/Pool/"+msg_dict['PoolID'], method='PUT',json={"Current_amount":current_amount})
            if current_amount / pool_info['data']['Budget']  >= 1:
                msg_dict['notif_type'] = 'pool_status'
                message = json.dumps(msg_dict)
                # update_pool_res = invoke_http("http://pool:5001/Pool/"+msg_dict['PoolID'], method='PUT',json={"Status":"completed"})
                channel.basic_publish(exchange=exchangename, routing_key="payment.fulfil", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
                print("\nRequest status ({:d}) published to the RabbitMQ Exchange:".format(
                200), msg_dict)
                print("Pool is completed")
            


        elif msg_dict['payment_status'] == 'unpaid':
            channel.basic_publish(exchange=exchangename, routing_key="payment.failed", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
            print("\nRequest status ({:d}) published to the RabbitMQ Exchange:".format(
                200), msg_dict)
        

        return jsonify({"resp":payload})
    except Exception as e:
        return jsonify({"error":str(e)}), 400

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5101, debug=True)
  print("Running on port 5101...")