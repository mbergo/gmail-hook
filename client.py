
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        url = self.base_url + endpoint
        response = requests.get(url)
        return response.json()

    def post(self, endpoint, data):
        url = self.base_url + endpoint
        response = requests.post(url, json=data)
        return response.json()
