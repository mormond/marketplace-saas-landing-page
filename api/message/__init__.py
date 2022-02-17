import json
import logging
import os
from azure.identity import CertificateCredential, ClientSecretCredential
from azuremarketplace.microsoft.marketplace.saas import SaaSAPI
from urllib import parse;
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

    cred = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    saas = SaaSAPI(cred)
    url_decoded_mp_token = parse.unquote(marketplace_token)
    resolved_token = saas.fulfillment_operations.resolve(x_ms_marketplace_token=url_decoded_mp_token)
    
    my_token = { 
        "subscription_name" : resolved_token.subscription_name,
        "id" : resolved_token.id,
        "offer_id" : resolved_token.offer_id,
        "plan_id" : resolved_token.plan_id,
        "quantity" : resolved_token.quantity
        }

    return func.HttpResponse(json.dumps({"text": my_token}))
