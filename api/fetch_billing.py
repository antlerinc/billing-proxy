from http.server import BaseHTTPRequestHandler
import os
import requests
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        CLIENT_ID = os.getenv("CLIENT_ID")
        CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        TENANT_ID = os.getenv("TENANT_ID")
        BASE_URL = "https://api.opentext.com"

        # 1. Get Token
        token_resp = requests.post(f"{BASE_URL}/tenants/{TENANT_ID}/oauth2/token", data={
            "client_id": CLIENT_ID, 
            "client_secret": CLIENT_SECRET, 
            "grant_type": "client_credentials"
        })
        
        if token_resp.status_code != 200:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Auth Failed")
            return

        token = token_resp.json().get("access_token")

        # 2. Get Data
        data_resp = requests.get(f"{BASE_URL}/api/securecloud/usage/charges", 
                                 headers={"Authorization": f"Bearer {token}"})

        # 3. Return Data
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(data_resp.content)
