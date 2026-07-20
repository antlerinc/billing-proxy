from http.server import BaseHTTPRequestHandler
import os
import requests
import json

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
    billing_url = "https://graph.microsoft.com/v1.0/subscribedSkus"
    return requests.get(billing_url, headers=headers).json()

# This is the "app" variable Vercel is looking for
def app(request, start_response):
    data = get_billing_data()
    
    status = '200 OK' if data else '500 Internal Server Error'
    response_body = json.dumps(data if data else {"error": "Failed to fetch"})
    
    response_headers = [('Content-Type', 'application/json')]
    start_response(status, response_headers)
    
    return [response_body.encode('utf-8')]
