from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)

# order_URL = environ.get('order_URL') or "http://localhost:5001/order" 
# shipping_record_URL = environ.get('shipping_record_URL') or "http://localhost:5002/shipping_record" 
#activity_log_URL = "http://localhost:5003/activity_log"
#error_URL = "http://localhost:5004/error"

exchangename = "pool_request" # exchange name
exchangetype = "topic" # use a 'topic' exchange to enable interaction
connection = amqp_connection.create_connection() 
channel = connection.channel()

if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0) 


@app.route("/create_pool", methods=['POST'])
def create_pool():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            payload = request.get_json()
            pool_info = payload["pool_info"]
            pool_invite = payload["pool_invites"]
            
            print("\nReceived an pool creation in JSON:", pool_info)
            print(pool_info)
            result = poolcreation(pool_info)
            print('\n------------------------')
            print('\nresult: ', result)
            if result['code'] in range(200,300):
                poolID = result['data']['PoolID']
                pool_invite = [{"poolid":poolID,"userid":x} for x in pool_invite]
                friend_result = invoke_http("http://pool_request:5002/pool_request/multiple", method='POST', json=pool_invite)
                print(friend_result, "FRIENDS HAS BEEN ADDED")

            return result

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "pool_management internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

@app.route("/accept_pool_request", methods=['PUT'])
def accept_pool_request():
    print(request.get_json())
    try:
        friend = request.get_json()
        # friend = {
        # "UserID": 1,
        # "PoolID": 1,
        # "status": "Accepted"
        # }
        result = processpool_request(friend)
        return result
       
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "pool_management accept internal error: " + str(e)
        }), 500

def processpool_request(friend):
    friend_res = invoke_http("http://pool_request:5002/pool_request", method='PUT', json=friend)
    res_status = friend_res['data']['status']

    pool_info = invoke_http("http://pool:5001/Pool/"+str(friend['PoolID']), method='GET')
    user_info = invoke_http("http://user:5004/user/"+str(friend['UserID']), method='GET')
    friend['PoolOwner'] = pool_info['data']['UserID']
    friend['PoolName'] = pool_info['data']['pool_name']
    friend['UserName'] = user_info['data']['UserName']
    message = json.dumps(friend)
    if res_status == 'Accepted':
        channel.basic_publish(exchange=exchangename, routing_key="poolrequest.success", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
        
        print("\nRequest status ({:d}) published to the RabbitMQ Exchange:".format(
            200), friend)

    delete_status = invoke_http("http://pool_request:5002/pool_request", method='DELETE', json=friend)
    return jsonify({'code': 200, 'message': 'Pool request responded successfully','delete':delete_status,'friend_res':friend_res})

def poolcreation(pool):

    print('\n-----Invoking pool microservice-----')
    
    pool = {
        "Expiry_Date":"2024-05-23",
        "Current_amount":0,
        "Budget": 100,
        "Pool_Type":"Group",
        "UserID":2,
        "pool_name":"Pool1",
        "pool_desc":"There is a pool for you to join!",
        "Status":"Active"
    }
    pool_result = invoke_http("http://pool:5001/Pool", method='POST', json=pool)
    print('pool_result:', pool_result)

    code = pool_result["code"]
    message =pool_result

 
    if code in range(200, 300):
        print(message)
        return message
    else:
        return {
            "code": 500,
            "data": pool,
            "message": "Failed to create pool."
        }    

    

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for POOL Related...")
    app.run(host="0.0.0.0", port=5100, debug=True)
