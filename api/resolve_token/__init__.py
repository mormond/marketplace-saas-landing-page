import json
import logging
import os
from azure.identity import CertificateCredential, ClientSecretCredential
from azuremarketplace.microsoft.marketplace.saas import SaaSAPI
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

    cred = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    saas = SaaSAPI(cred)
    url_decoded_mp_token = parse.unquote(marketplace_token)
    resolved_token = saas.fulfillment_operations.resolve(
        x_ms_marketplace_token=url_decoded_mp_token)

    if resolved_token is None:
        return func.HttpResponse(json.dumps({"text": "No valid token found."}))

    my_token = {
        "id": resolved_token.id,
        "subscriptionName": resolved_token.subscription_name,
        "offerId": resolved_token.offer_id,
        "planId": resolved_token.plan_id,
        "quantity": resolved_token.quantity,
        "SubscriptionPublisherId": resolved_token.subscription.publisher_id,
        "saasSubscriptionStatus": resolved_token.subscription.saas_subscription_status,
        "beneficiaryEmailId": resolved_token.subscription.beneficiary.email_id,
        "beneficiaryObjectId": resolved_token.subscription.beneficiary.object_id,
        "beneficiaryTenantId": resolved_token.subscription.beneficiary.tenant_id,
        "beneficiaryPid": resolved_token.subscription.beneficiary.puid,
        "purchaserEmailId": resolved_token.subscription.purchaser.email_id,
        "purchaserObjectId": resolved_token.subscription.purchaser.object_id,
        "purchaserTenantId": resolved_token.subscription.purchaser.tenant_id,
        "purchaserPid": resolved_token.subscription.purchaser.puid,
        # "termTermUnit": resolved_token.subscription.term.term_unit,
        "termStartDate": resolved_token.subscription.term.start_date,
        "termEndDate": resolved_token.subscription.term.end_date,
        "isTest": resolved_token.subscription.is_test,
        "isFreeTrial": resolved_token.subscription.is_free_trial,
        "allowedCustomerOperations": resolved_token.subscription.allowed_customer_operations,
        "sandboxType": resolved_token.subscription.sandbox_type,
        "sessionMode": resolved_token.subscription.session_mode
    }

    return func.HttpResponse(json.dumps({ "text": my_token }))
