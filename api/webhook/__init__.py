import json
import logging
import os
import requests
from urllib import parse
import azure.functions as func
import sys
 
# setting path
sys.path.append('../helpers')
import helpers

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Webhook called.')
   
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(status_code=400)

    logging.info(req_body)

    if (os.environ['REJECT_CHANGE'].lower() == 'true'):

        tenant_id = os.environ['TENANT_ID']
        client_id = os.environ['CLIENT_ID']
        client_secret = os.environ['CLIENT_SECRET']

        bearer_token = helpers.get_bearer_token(tenant_id, client_id, client_secret)

        subscriptionId = req_body['subscriptionId']
        operationId = req_body['id']

        operations_url = 'https://marketplaceapi.microsoft.com/api/saas/subscriptions/subscriptionId/operations/operationId?api-version=2018-08-31'
        operations_headers = {'Authorization': f"Bearer {bearer_token}", 'Content-Type': 'application/json'}
        operations_data = { 'status': 'Failure' }

        logging.info('Calling path operation - failure')
        operations_r = requests.patch(operations_url, headers=operations_headers, data=operations_data)
        response = operations_r.json()

        if (operations_r.status_code != 200):
            logging.info(f"Patch operation failed. Status code: {operations_r.status_code}")
            return func.HttpResponse(status_code=operations_r.status_code, body=json.dumps({'summary': 'Error calling patch operation.', 'full': 'Error calling patch operation.'}))

    try: 
        web_ack = json.loads(os.environ['WEBHOOK_ACK'])
        status = web_ack['status']
        message = web_ack['message']
        return func.HttpResponse(status_code=status, body=message)
    except:
        return func.HttpResponse(status_code=200, body='OK')
