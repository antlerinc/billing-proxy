import os
import requests
import json

# Your existing logic
def get_billing_data():
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    tenant_id = os.environ.get('TENANT_ID')
    
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    token_response = requests.post(token_url, data=token_data).json()
    if 'access_token' not in token_response:
        return None
    headers = {'Authorization': f"Bearer {token_response['access_token']}"}
    return requests.get("https://graph.microsoft.com/v1.0/subscribedSkus", headers=headers).json()

# Vercel looks for 'app' in wsgi.py
def app(environ, start_response):
    data = get_billing_data()
    status = '200 OK' if data else '500 Internal Server Error'
    response_body = json.dumps(data if data else {"error": "Failed to fetch"})
    
    start_response(status, [('Content-Type', 'application/json')])
    return [response_body.encode('utf-8')]
