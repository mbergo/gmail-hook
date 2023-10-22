import requests
import json

print(
    requests.post(
        "http://127.0.0.1:10000",
        json={
            "from_email": "gates@microsoft.com",
            "content": "Hi, I'm Bill Gates. I'm the CEO of Microsoft. I'm looking for a new girlfriend. I'm 65 years old. I'm a bill"
        }
    )
)# Meeting Transcription 18-10-2023
