import json
import logging
import os
import requests
import azure.functions as func
import sys
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
 
script_dir = os.path.dirname( __file__ )
helpers_dir = os.path.join( script_dir, '..', 'helpers' )
sys.path.append( helpers_dir )
import helpers

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Config called.')

    connect_str = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)    

    container_client = blob_service_client.get_container_client(container='test') 

    list = container_client.list_blobs()

    for x in list:
        logging.info(x.name)

    #x = container_client.download_blob('abc.json').readall()

    # try:
    #     req_body = req.get_json()
    # except ValueError:
    #     return func.HttpResponse(status_code=400)

    # logging.info(req_body)

    return func.HttpResponse(status_code=200, body='OK')
