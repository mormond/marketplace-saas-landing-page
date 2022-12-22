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

    dump_full_token = True

    if dump_full_token is True:
        my_token = {
            "id": resolved_token.id,
            "subscriptionName": resolved_token.subscription_name,
            "offerId": resolved_token.offer_id,
            "planId": resolved_token.plan_id,
            "quantity": resolved_token.quantity,
            "subscription": {
                "id": resolved_token.subscription.id,
                "publisherId": resolved_token.subscription.publisher_id,
                "offerId": resolved_token.subscription.offer_id,
                "name": resolved_token.subscription.name,
                "saasSubscriptionStatus": resolved_token.subscription.saas_subscription_status,
                "beneficiary": {
                    "emailId": resolved_token.subscription.beneficiary.email_id,
                    "objectId": resolved_token.subscription.beneficiary.object_id,
                    "tenantId": resolved_token.subscription.beneficiary.tenant_id,
                    "puid": resolved_token.subscription.beneficiary.puid
                },
                "purchaser": {
                    "emailId": resolved_token.subscription.purchaser.email_id,
                    "objectId": resolved_token.subscription.purchaser.object_id,
                    "tenantId": resolved_token.subscription.purchaser.tenant_id,
                    "puid": resolved_token.subscription.purchaser.puid
                },
                "planId": resolved_token.subscription.plan_id,
                "term": {
                    # "termUnit": resolved_token.subscription.term.term_unit,
                    "startDate": resolved_token.subscription.term.start_date,
                    "endDate": resolved_token.subscription.term.end_date
                },
                # "autoRenew": resolved_token.subscription.auto_renew,
                "isTest": resolved_token.subscription.is_test,
                "isFreeTrial": resolved_token.subscription.is_free_trial,
                "allowedCustomerOperations": resolved_token.subscription.allowed_customer_operations,
                "sandboxType": resolved_token.subscription.sandbox_type,
                # "lastModified": resolved_token.subscription.last_modified,
                "quantity": resolved_token.subscription.quantity,
                "sessionMode": resolved_token.subscription.session_mode
            }
        }
    else:
        my_token = {
            "id": resolved_token.id,
            "subscriptionName": resolved_token.subscription_name,
            "offerId": resolved_token.offer_id,
            "planId": resolved_token.plan_id,
            "quantity": resolved_token.quantity,
            "subscription": {
                "id": resolved_token.subscription.id,
                "publisherId": resolved_token.subscription.publisher_id,
                "name": resolved_token.subscription.name,
                "saasSubscriptionStatus": resolved_token.subscription.saas_subscription_status,
                "beneficiary": {
                    "emailId": resolved_token.subscription.beneficiary.email_id,
                },
                "purchaser": {
                    "emailId": resolved_token.subscription.purchaser.email_id,
                },
                "term": {
                    # "termUnit": resolved_token.subscription.term.term_unit,
                    "startDate": resolved_token.subscription.term.start_date,
                    "endDate": resolved_token.subscription.term.end_date
                },
                # "autoRenew": resolved_token.subscription.auto_renew,
                "isTest": resolved_token.subscription.is_test,
                "isFreeTrial": resolved_token.subscription.is_free_trial,
                "allowedCustomerOperations": resolved_token.subscription.allowed_customer_operations,
                "sandboxType": resolved_token.subscription.sandbox_type,
                # "lastModified": resolved_token.subscription.last_modified,
                "sessionMode": resolved_token.subscription.session_mode
            }
        }

    return func.HttpResponse(json.dumps({"text": my_token}))
