
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
import time
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
    # max_amt = data['remaining'] 
    # pool_name = data['pool_name']
    # userid = data['UserID']
    # poolid = data['PoolID']
    response = invoke_http("http://payment:4242/create-checkout-session", method='POST', json=data)
    print(response)
    return {"redirect":response['url']}


@app.route("/refund/<int:poolid>", methods=['POST'])
def refund(poolid):
    
    transactions_lst = invoke_http(f"http://transaction:5003/transactions/pool/{poolid}/status/Empty", method='GET')['data']['transactions']
    print(transactions_lst)
    pool_info = invoke_http("http://pool:5001/Pool/"+str(poolid), method='GET')['data']
    
    pool_budget = pool_info['Budget']
    curr_amt = pool_info['Current_amount']
    ownerID = pool_info['UserID']
    temp = {}
    orig_total = 0
    
    for transaction in transactions_lst:
        userid =transaction['userID']
        orig_total += transaction['amount']
        if userid in temp:
            temp[userid] += transaction['amount']
        else:
            temp[userid] = transaction['amount']
    print(temp, "TOTAL PER USER", transactions_lst)
    #Caculate portion
    for user, amount in temp.items():
        temp[user] = amount / orig_total
    print(temp, "PPORTION TO ORIG", transactions_lst)
    #Calculate new percentage
    for user, amount in temp.items():
        temp[user] = (curr_amt * amount) / (orig_total * amount)
    
    print(transactions_lst)
    print(temp, "RATIOS", transactions_lst)

    ref_lst = []

    for transaction in transactions_lst:
        userid =transaction['userID']
        percentage_ref = temp[userid]
        ref_amt = transaction['amount'] * percentage_ref
        print(userid , poolid ,"THIS IS THE REFUND META VALUE")
        # Store as list send over bunch of refund
        ref_lst.append({"payment_intent":transaction['paymentIntent'],"metadata":{"UserID": userid, "PoolID": poolid},"amt":int(ref_amt * 100)})
        # refund_obj = stripe.Refund.create(
        #     payment_intent=transaction['paymentIntent'],
        #     metadata={"UserID": userid, "PoolID": poolid},
        #     amount=int(ref_amt * 100),
            
        # )
        # print(refund_obj, "REFUND")
    ref_status = invoke_http("http://payment:4242/refund_mul", method='POST', json={"refunds":ref_lst})
    time.sleep(2)
    #Pull from payment refund db and create refund
    all_refunds = invoke_http(f"http://payment:4242/refund/{poolid}", method='GET')['data']['refunds']

    user_info = invoke_http("http://user:5004/user", method='GET')['data']['users']

    user_map = {}
    print(all_refunds,"ALL REFUNDS")
    for user in user_info:
        user_map[user['UserID']] = user['UserName']

    agg_refund = {}
    for refund in all_refunds:
        ref_amt = float(refund['amount'])
        if refund['UserID'] in agg_refund:
            agg_refund[refund['UserID']] += ref_amt
        else:
            agg_refund[refund['UserID']] = ref_amt
    print(agg_refund,"agg_refund")
    batch_msg = {"batchmessage":[],"owner_msg":[],"notif_type":"refund"}
    total_amt = 0
    for userID,amt in agg_refund.items():
        msg = {}
        msg['UserID'] = userID
        msg['PoolID'] = poolid
        msg['amount'] = float(amt)
        msg['PoolName'] = pool_info['pool_name']
        msg['notif_type'] = 'refund'
        msg['payment_intent'] = 'empty'
        msg['payment_status'] = 'refund'
        msg['amount_total'] = amt
        total_amt += float(amt)
        if userID in user_map:
            msg['UserName'] = user_map[userID]
        else:
            msg['UserName'] = 'no name'
        batch_msg['batchmessage'].append(msg)
    msg['total_amt'] = total_amt
    msg['PoolOwner'] = ownerID
    batch_msg['owner_msg'].append(msg)
    print(batch_msg,"batch_msg")

    message = json.dumps(batch_msg)
    channel.basic_publish(exchange=exchangename, routing_key="refund.success", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2))
    print("\nRequest status ({:d}) published to the RabbitMQ Exchange:".format(
        200), msg)
    del_res = invoke_http(f"http://payment:4242/delete_refund", method='DELETE')
    update_pool_res = invoke_http("http://pool:5001/Pool/"+str(poolid), method='PUT',json={"Current_amount":0})
    update_transaction = invoke_http("http://transaction:5003/transactions/pool/"+str(poolid)+"/status/Empty", method='PUT')

    return jsonify({"Success": "Refund Made"}),200
        





@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        payload = request.get_json()['data']['object']

        msg_dict = {}
        fields_to_send = ['amount_total', 'payment_intent', 'payment_status']
        for x in fields_to_send:
            if x in payload:
                if x == 'amount_total':
                    msg_dict[x] = payload[x] / 100
                else:
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