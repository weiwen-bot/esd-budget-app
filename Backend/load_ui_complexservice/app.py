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


@app.route("/get_userpools/<int:userid>", methods=['GET'])
def gethomepage(userid):
    # Simple check of input format and data of the request are JSON
        try:
            #Owner
            all_pool = invoke_http("http://pool:5001/Pool", method='GET')
            #members
            poolmapping = invoke_http("http://pool:5001/pool_mapping", method='GET')
            
            print(all_pool)
            print(poolmapping)
            all_pool = all_pool['data']['pools']

            member_list = poolmapping['data']['pool_mapping']

            member_poolid = set([x["PoolID"] for x in member_list if x['UserID'] == userid])

            pool_dict = {"pools":[]}

            for pool in all_pool:
                if pool['UserID'] == userid:
                    pool['ownership'] = "Owner"
                    pool_dict['pools'].append(pool)
                elif pool['PoolID'] in member_poolid:
                    pool['ownership'] = "Member"
                    pool_dict['pools'].append(pool)



            return jsonify({"pools":pool_dict["pools"]})

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


@app.route("/get_pool/<int:poolid>", methods=['GET'])
def get_pool(poolid):
    # Simple check of input format and data of the request are JSON
    try:
        #Owner
        pool_details = invoke_http(f"http://pool:5001/Pool/{poolid}", method='GET')



        all_users = invoke_http(f"http://user:5004/user", method='GET')['data']['users']

        #members
        poolmapping = invoke_http("http://pool:5001/pool_mapping", method='GET')

        all_poolmapping = poolmapping['data']['pool_mapping']

        # print(pool_details)
        # print(all_users)
        # print(poolmapping)
        # print(all_poolmapping)


        member_poolid = [x["UserID"] for x in all_poolmapping if x['PoolID'] == poolid]
        print(member_poolid)

        transaction = invoke_http(f"http://transaction:5003/transactions/pool/{poolid}", method='GET')

        pool_dict = {"usernames":[],"transaction":transaction['data']['transactions'], "pool":pool_details['data']}

        for user in all_users:
            if user['UserID'] == pool_details['data']['UserID']:
                pool_dict['usernames'].append({user["UserName"]:"Owner"})
            if user['UserID'] in member_poolid:
                pool_dict['usernames'].append({user["UserName"]:"Member"})



        return pool_dict
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



    

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for POOL Related...")
    app.run(host="0.0.0.0", port=5200, debug=True)
