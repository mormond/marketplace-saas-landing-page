import json
import logging
import os
import requests
from urllib import parse
import azure.functions as func
import sys

script_dir = os.path.dirname( __file__ )
helpers_dir = os.path.join( script_dir, '..', 'helpers' )
sys.path.append( helpers_dir )
import helpers
 
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        marketplace_token = req_body.get('marketplace_token')

    url_decoded_mp_token = parse.unquote(marketplace_token)

    tenant_id = os.environ['TENANT_ID']
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    bearer_token = helpers.get_bearer_token(tenant_id, client_id, client_secret)

    resolve_url = 'https://marketplaceapi.microsoft.com/api/saas/subscriptions/resolve?api-version=2018-08-31'
    resolve_headers = {'Authorization': f"Bearer {bearer_token}",
                       'Content-Type': 'application/json',
                       'x-ms-marketplace-token': f"{url_decoded_mp_token}"}

    resolve_r = requests.post(resolve_url, headers=resolve_headers)
    resolved_token = resolve_r.json()

    if (resolve_r.status_code != 200 or resolved_token is None):
        return func.HttpResponse(json.dumps({'summary': 'No valid token found.', 'full': 'No valid token found.'}))

    summary_token = {
        'id': resolved_token['id'],
        'subscriptionName': resolved_token['subscriptionName'],
        'offerId': resolved_token['offerId'],
        'planId': resolved_token['planId'],
        'subscription': {
            'id': resolved_token['subscription']['id'],
            'publisherId': resolved_token['subscription']['publisherId'],
            'name': resolved_token['subscription']['name'],
            'saasSubscriptionStatus': resolved_token['subscription']['saasSubscriptionStatus'],
            'beneficiary': {
                'emailId': resolved_token['subscription']['beneficiary']['emailId'],
            },
            'purchaser': {
                'emailId': resolved_token['subscription']['purchaser']['emailId'],
            }
        }
    }

    if resolved_token.get('quantity') is not None:
        summary_token['quantity'] = resolved_token['quantity']

    return func.HttpResponse(json.dumps({'summary': summary_token, 'full': resolved_token}))
