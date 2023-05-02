# Generate multiple POs with Async Create Payment Order
# Two options:
# 1) Define the payment orders in the script itself (see `PO_LIST`)
#   Run `python bulk_po.py`
# 2) Define the payment orders in a JSON file and pass that filename as an argument (sys.argv[1])
#   Run `python bulk_po.py wire_payment_orders.json`

import requests
import json
import sys
import os
import uuid  

ORG_ID = os.environ.get("MY_ORG_ID")
API_KEY = os.environ.get("MY_API_KEY")
 
PO_LIST = [
    {
    "type": "ach",
    "amount": 960,
    "direction": "debit",
    "receiving_account_id": "a069dd3e-ff35-461e-b8e4-32328548c861",
    "originating_account_id": "172e4b92-126e-4175-a824-a3ad7107b8a3",
    "description": "SHIP-LABEL",
    "metadata": {
        "Customer ID": "123"
        }
    },
    {
    "type": "ach",
    "amount": 970,
    "direction": "debit",
    "receiving_account_id": "a10129c4-2c26-480a-92a0-6499264f498e",
    "originating_account_id": "172e4b92-126e-4175-a824-a3ad7107b8a3",
    "description": "SHIP-LABEL",
    "metadata": {
        "Customer ID": "456"
        }
    }
]
 
def main():
    # Check to see if file argument has been specified
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as read_file:
            payment_orders = json.load(read_file)
    else:
        payment_orders = PO_LIST

    for payment in payment_orders:
        response = create_po(payment, ORG_ID, API_KEY)
        print(f'Response: {response.status_code}')
        json_resp = response.json()
        print(f'--> {json_resp["type"].upper()} {json_resp["direction"].upper()} for {"${:,.2f}".format(json_resp["amount"]/100)}','\n')


def async_create_po(payload, org_id, api_key):
    url = "https://app.moderntreasury.com/api/payment_orders/create_async"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    try:
        response = requests.post(url=url, auth=(org_id, api_key), headers=headers, json=payload)
        return response
    except Exception as e:
        print(e)
        return "Call failed."

def create_po(payload, org_id, api_key):
    url = "https://app.moderntreasury.com/api/payment_orders"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    try:
        response = requests.post(url=url, auth=(org_id, api_key), headers=headers, json=payload)
        return response
    except Exception as e:
        print(e)
        return "Call failed."


if __name__ == '__main__':
    main()