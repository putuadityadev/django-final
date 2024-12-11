import requests
import json
import base64

class MidtransClient:
    def __init__(self, server_key, client_key, is_production=False):
        self.server_key = server_key
        self.client_key = client_key
        self.is_production = is_production
        
        # Base URL
        self.base_url = 'https://app.midtrans.com' if is_production else 'https://app.sandbox.midtrans.com'
        
        # Encode server key
        self.auth_string = base64.b64encode(f'{server_key}:'.encode()).decode()

    def create_transaction(self, payload):
        url = f'{self.base_url}/snap/v1/transactions'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.auth_string}'
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Midtrans API Error: {response.text}")

    def status_transaction(self, order_id):
        url = f'{self.base_url}/v2/{order_id}/status'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.auth_string}'
        }

        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Midtrans API Error: {response.text}")