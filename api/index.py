import os
import requests
import json

def handler(request):
    # Fetch credentials
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    tenant_id = os.environ.get('TENANT_ID')

    # Get Token
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_resp = requests.post(token_url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }).json()

    if 'access_token' not in token_resp:
        return {'statusCode': 401, 'body': 'Auth Failed'}

    # Get Data
    headers = {'Authorization': f"Bearer {token_resp['access_token']}"}
    data = requests.get("https://graph.microsoft.com/v1.0/subscribedSkus", headers=headers).json()

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }
