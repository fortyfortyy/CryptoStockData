import requests
import json


def fetch_data_from_url(url, headers):
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None


def extract_data_from_url(html_data):
    data = json.loads(html_data)
    return data
