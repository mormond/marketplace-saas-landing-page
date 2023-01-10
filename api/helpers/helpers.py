import requests

def get_bearer_token(tenant_id: str, client_id: str, client_secret: str):

    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    auth_headers = {'content-type': 'application/x-www-form-urlencoded'}
    auth_data = f"client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&resource=20e940b3-4c77-4b0b-9a53-9e16a1b010a7"

    auth_r = requests.post(auth_url, data=auth_data, headers=auth_headers)

    return auth_r.json()['access_token']