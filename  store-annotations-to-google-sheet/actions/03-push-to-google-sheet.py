import os
import requests

def push_to_google_sheet(annotations, sheet_url):
    payload = {
        "type": "spreadsheet",
        "data": {
            "columns": list(annotations[0].keys()) if annotations else [],
            "rows": [list(row.values()) for row in annotations]
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(sheet_url, json=payload, headers=headers)

    return {
        "status_code": response.status_code,
        "response_text": response.text
    }

def handler(event, context):
    SHEET_ENDPOINT = event['google_sheet_endpoint']
    return push_to_google_sheet(context, SHEET_ENDPOINT)
