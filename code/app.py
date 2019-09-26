import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'package'))
import json
from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20.exceptions import V20Error
import account as ac
import logging
import datetime
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    environment = event['environment']
    instruments = event['instruments']

    statusCode = 200
    message = "OK"

    api = API(access_token=ac.access_token, environment=environment)
 
    params = {"instruments": instruments}
    ps = PricingStream(ac.account_number, params)
    
    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table(instruments)

    try:
        for rsp in api.request(ps):
            if "bids" in rsp.keys():
                table.put_item(
                    Item = {
                        "DATETIME": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y%m%d%H%M%S'),
                        "bid": rsp["bids"][0]["price"],
                        "ask": rsp["asks"][0]["price"]
                    }
                )
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
