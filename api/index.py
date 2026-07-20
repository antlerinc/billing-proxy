import os
import requests

def handler(request):
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    tenant_id = os.environ.get('TENANT_ID')

    if not all([client_id, client_secret, tenant_id]):
        return {'statusCode': 400, 'body': 'Missing environment variables.'}

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    
    token_response = requests.post(token_url, data=token_data).json()
    if 'access_token' not in token_response:
        return {'statusCode': 401, 'body': f"Auth failed: {token_response}"}
    
    headers = {'Authorization': f"Bearer {token_response['access_token']}"}
    billing_url = "https://graph.microsoft.com/v1.0/subscribedSkus"
    data_response = requests.get(billing_url, headers=headers)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': data_response.text
    }
