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

KKMT_ORG_ID = os.environ.get("KKMT_ORG_ID")
KKMT_API_KEY = os.environ.get("KKMT_API_KEY")
 
PO_LIST = [
    {
    "type": "Xwire",
    "amount": 11111,
    "direction": "credit",
    "originating_account_id": "9837ebf3-46fe-4afd-814a-78cd82fe82e2",
    "receiving_account_id": "6c153e0c-e890-4414-829c-b9880a19c245",
    "statement_descriptor": "Distribution for fund 123",
    },
    {
    "type": "Xwire",
    "amount": 22222,
    "direction": "credit",
    "originating_account_id": "9837ebf3-46fe-4afd-814a-78cd82fe82e2",
    "receiving_account_id": "6c153e0c-e890-4414-829c-b9880a19c245",
    "statement_descriptor": "Distribution for fund 123",
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
        response = create_po(payment, KKMT_ORG_ID, KKMT_API_KEY)
        print(response.status_code)
        print(response.json())


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