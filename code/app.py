import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'package'))
import json
from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20.exceptions import V20Error
import account as ac
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    api = API(access_token=ac.access_token, environment=event['environment'])
 
    params = {"instruments": event['instruments']}
    ps = PricingStream(ac.account_number, params)

    statusCode = 200
    message = "OK"
 
    try:
        for rsp in api.request(ps):
            if "bids" in rsp.keys():
                logger.info("bids="+rsp["bids"][0]["price"])
                logger.info("asks="+rsp["asks"][0]["price"])
                break
 
    except V20Error as e:
        statusCode = 500
        message = "Error: {}".format(e)

    return {
        "statusCode": statusCode,
        "body": json.dumps({
            "message": message
        }),
    }
