import json
import logging
import os
import requests
from urllib import parse
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        marketplace_token = req_body.get('marketplace_token')

    tenant_id = os.environ["TENANT_ID"]
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]

    url_decoded_mp_token = parse.unquote(marketplace_token)

    auth_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
    auth_headers = {'content-type': 'application/x-www-form-urlencoded'}
    auth_data = f'client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&resource=20e940b3-4c77-4b0b-9a53-9e16a1b010a7'

    auth_r = requests.post(auth_url, data=auth_data, headers=auth_headers)

    bearer_token = auth_r.json()['access_token']

    resolve_url = 'https://marketplaceapi.microsoft.com/api/saas/subscriptions/resolve?api-version=2018-08-31'
    resolve_headers = {'Authorization': f'Bearer {bearer_token}',
               'Content-Type': 'application/json',
               'x-ms-marketplace-token': f'{url_decoded_mp_token}'}

    resolve_r = requests.post(resolve_url, headers=resolve_headers)
    resolved_token = resolve_r.json()

    if resolved_token is None:
        return func.HttpResponse(json.dumps({"text": "No valid token found."}))

    dump_full_token = True

    if dump_full_token is True:
        return func.HttpResponse(json.dumps({"text": resolved_token}))
    else:
        my_token = {
            "id": resolved_token['id'],
            "subscriptionName": resolved_token['subscriptionName'],
            "offerId": resolved_token['offerId'],
            "planId": resolved_token['planId'],
            "subscription": {
                "id": resolved_token['subscription']['id'],
                "publisherId": resolved_token['subscription']['publisherId'],
                "name": resolved_token['subscription']['name'],
                "saasSubscriptionStatus": resolved_token['subscription']['saasSubscriptionStatus'],
                "beneficiary": {
                    "emailId": resolved_token['subscription']['beneficiary']['emailId'],
                },
                "purchaser": {
                    "emailId": resolved_token['subscription']['purchaser']['emailId'],
                }
            }
        }

        if resolved_token.get('quantity') is not None:
            my_token['quantity'] = resolved_token['quantity']

        return func.HttpResponse(json.dumps({"text": my_token}))
