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
        '''
        Get all Available pools belonging to the user
        '''
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
                    username = invoke_http(f"http://user:5004/user/{pool['UserID']}", method='GET')['data']['UserName']
                    pool['PoolOwner'] = username
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

    '''
    Get the pooldetails for the pool
    '''
    try:
        #Owner
        pool_details = invoke_http(f"http://pool:5001/Pool/{poolid}", method='GET')



        all_users = invoke_http(f"http://user:5004/user", method='GET')['data']['users']

        #members
        poolmapping = invoke_http("http://pool:5001/pool_mapping", method='GET')

        all_poolmapping = poolmapping['data']['pool_mapping']

        member_poolid = [x["UserID"] for x in all_poolmapping if x['PoolID'] == poolid]
        print(member_poolid)

        transaction = invoke_http(f"http://transaction:5003/transactions/pool/{poolid}", method='GET')

        pool_dict = {"usernames":[],"transaction":transaction['data']['transactions'], "pool":pool_details['data']}

        for user in all_users:
            if user['UserID'] == pool_details['data']['UserID']:
                pool_dict['usernames'].append({user["UserName"]:"Owner"})
            if user['UserID'] in member_poolid:
                pool_dict['usernames'].append({user["UserName"]:"Member"})



        return pool_dict ,200
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

#get all notification
@app.route("/get_notification/<int:userid>", methods=['GET'])
def get_notification(userid):
    
    try:
        all_notification = invoke_http(f"http://notification:5005/notifications/{userid}", method='GET')
        all_request = invoke_http(f"http://pool_request:5002/pool_request/user/{userid}",method='GET')

        pool = invoke_http(f"http://pool:5001/Pool", method='GET')['data']['pools']
        pool_map = {x["PoolID"]:x["pool_name"] for x in pool}
        user = invoke_http(f"http://user:5004/user", method='GET')['data']['users']
        user_map = {x["UserID"]:x["UserName"] for x in user}

        all_req = {"notif":[],"request":[]}

        if all_request["code"] != 404:
            for req in all_request['data']:
                req['PoolName'] = pool_map[req['PoolID']]
                req['PoolOwner'] = user_map[[ x for x in pool if pool['PoolID'] == req['PoolID']][0]['UserID']]
                all_req['request'].append(req)
            all_req['request'] = all_request['data']

        if all_notification["code"] != 404:
            all_req['notif'] = all_notification['data']
            

        

        return jsonify({"code":200, "data": all_req}), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "pool_management internal error: " + str(e)
        }), 500
    
@app.route("/get_newusers/<int:userid>/<int:poolid>", methods=['GET'])
def get_new_pool_invites(userid,poolid):
    
    try:
        all_users = invoke_http(f"http://user:5004/user", method='GET')['data']['users']

        poolmapping = invoke_http("http://pool:5001/pool_mapping", method='GET')['data']['pool_mapping']

        member_poolid = [x["UserID"] for x in poolmapping if x['PoolID'] == poolid]
        member_poolid.append(userid)

        pool_dict = {"users":[]}
        for user in all_users:
            if user['UserID'] not in member_poolid:
                pool_dict['users'].append(user)

        return pool_dict, 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "pool_management internal error: " + str(e)
        }), 500
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for POOL Related...")
    app.run(host="0.0.0.0", port=5200, debug=True)
