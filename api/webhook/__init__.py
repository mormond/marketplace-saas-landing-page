import json
import logging
import os
import requests
from urllib import parse
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Webhook called.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(status_code=400)

    logging.info(req_body)

    return func.HttpResponse(status_code=200, body='OK')
