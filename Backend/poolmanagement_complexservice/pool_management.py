from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

pool_service_URL = "http://localhost:5005/app"
user_management_URL = "http://localhost:5006/app"
transaction_service_URL = "http://localhost:5007/app"
payment_service_URL = "http://localhost:4242/app"
error_URL = "http://localhost:5008/app"


@app.route("/pool_management", methods=['POST'])
def pool_management():
    # Simple check of input format and data of the request are JSON
    # Pool ID and user ID is avaliable from request as UI page body contents from Post Request already defines this two things 
    if request.is_json:
        try:
            transaction_data = request.get_json()
            print("\nReceived a transaction in JSON:", transaction_data)
            #first call payment service 
            payment_result = process_payment(transaction_data)
            print("\nReceived a transaction in JSON:", payment_result)
            # Extracting payment_result 
            payment_status = payment_result.get("data", {}).get("payment_result", None) 
            # if payment not success ask user if they want to retry 
            if payment_status != "success": 
                print("Payment not Successful") 
                inp = input("Would you like to retry payment? [Yes/No]")
                if inp.lower() == "yes":
                    payment_result = process_payment(transaction_data)

                else:
                    #not sure how to redirect to individual pool page
                    return 'Payment failed'

            # If payment successful, then proceed with creating transaction
            # 1. Send transaction data to process transaction
            result = processTransaction(transaction_data)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "pool_management.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processTransaction(transaction_data):
    # 2. Send the transaction data into transaction microservice
    # Invoke the transaction microservice
    print('\n-----Invoking transaction microservice-----')
    transaction_result = invoke_http(transaction_service_URL, method='POST', json=transaction_data)
    print('transaction_result:', transaction_result)

    #Change to notification instead

    # Check the transaction result; if a failure, send it to the error microservice.
    code = transaction_result["code"]
    if code not in range(200, 300):

        # Inform the error microservice
        print('\n\n-----Invoking error microservice as order fails-----')
        invoke_http(error_URL, method="POST", json=transaction_result)
        # - reply from the invocation is not used; 
        # continue even if this invocation fails
        print("transaction status ({:d}) sent to the error microservice:".format(
            code), transaction_result)
        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": transaction_result},
            "message": "Order creation failure sent for error handling."
        }

    # 7. Return transaction result
    return {
        "code": 201,
        "data": {
            "order_result": transaction_result,
        }
    }

def process_payment(transaction_data): 
    # 2. Send the order info {cart items} 
    # Invoke the order microservice 
    print('\n-----Invoking order microservice-----') 
    payment = invoke_http(payment_service_URL, method='POST', json=transaction_data) 
    payment_status = payment['status'] 
    if payment_status == 'success': 
        return { 
            "code": 201, 
            "data": { 
                "payment_result": payment 
            } 
        } 
    else: 
        return { 
            "code": 500, 
            "data": { 
                "payment_result": payment 
            }, 
            "message": "Payment creation failure sent for error handling." 
        }
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    
