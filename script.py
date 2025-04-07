from flask import Flask, jsonify
import requests
import urllib.parse
import datetime
import json
from creds import credentials

app = Flask(__name__)

@app.route('/get-orders', methods=['GET'])
def get_orders():
    # Getting the LWA access token using the Seller Central App credentials.
    token_response = requests.post(
        "https://api.amazon.com/auth/o2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": credentials["refresh_token"],
            "client_id": credentials["lwa_app_id"],
            "client_secret": credentials["lwa_client_secret"],
        },
    )
    access_token = token_response.json()["access_token"]

    # North America SP API endpoint
    endpoint = "https://sellingpartnerapi-na.amazon.com"

    # US Amazon Marketplace ID
    marketplace_id = "ATVPDKIKX0DER"

    # Downloading orders
    request_params = {
        "MarketplaceIds": marketplace_id,
        "CreatedAfter": (
            datetime.datetime.now() - datetime.timedelta(days=30)
        ).isoformat(),
    }

    orders = requests.get(
        endpoint + "/orders/v0/orders?" + urllib.parse.urlencode(request_params),
        headers={"x-amz-access-token": access_token},
    )

    # Return the JSON response
    return jsonify(orders.json())

if __name__ == '__main__':
    app.run(debug=True)