# create a post request to send the email content to the server
import requests
import json

url = "https://ai4d.onrender.com"

# using the phrase "o andre ta gripado e me pediu o custo da aws." as an example, it should send it as json

payload = json.dumps({  "from_email": " ", "content": "o andre ta gripado e me pediu o custo da aws."})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)