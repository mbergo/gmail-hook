import requests

print(
    requests.post(
        "https://david-d21o.onrender.com/",
        json={
            "from_email": "marcus@bergo.one",
            "content": """
            Hi Marcus,
                I am writing to you regarding the recent changes in your behaviour. I have noticed that you have been more anxious than usual. I would like to know if there is anything that I can do to help you.
            Kind regards,
            Marcus

            """
        }
    )
)