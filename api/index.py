import os
import requests

def handler(request):
    # Get your credentials from Vercel Environment Variables
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    tenant_id = os.environ.get('TENANT_ID')

    if not all([client_id, client_secret, tenant_id]):
        return {
            'statusCode': 400,
            'body': 'Missing required environment variables.'
        }

    # 1. Get OAuth Token
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    
    token_response = requests.post(token_url, data=token_data).json()
    
    if 'access_token' not in token_response:
        return {
            'statusCode': 401,
            'body': f"Auth failed: {token_response}"
        }
    
    access_token = token_response['access_token']

    # 2. Fetch Billing Data
    headers = {'Authorization': f'Bearer {access_token}'}
    # REPLACE THIS URL WITH YOUR SPECIFIC GRAPH API ENDPOINT
    billing_url = "https://graph.microsoft.com/v1.0/YOUR_ENDPOINT_HERE" 
    
    data_response = requests.get(billing_url, headers=headers)

    # 3. Return to Vercel
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': data_response.text
    }
