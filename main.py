import fastapi
import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel


load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as problems, incidents, contact details, Company, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "the name of the company that sent the email"
                },                                        
                "incident": {
                    "type": "string",
                    "description": "Try to identify what is the problem that the person is complaining about. The summary of a problem which creates an incident."
                },
                "title":{
                    "type": "string",
                    "description": "Try to identify a propper title for this incident."
                },
                "severity": {
                    "type": "string",
                    "description": "Try to categorise this incident from email as low medium or high. If it is low, it is low; if it is medium, it is medium; if it is high, it is high."
                },
                "reply": {
                    "type": "string",
                    "description": "Try to create a support reply to the customer in from his email in order to calm him down"
                },
                "fixes": {
                    "type": "string",
                    "description": "Suggest based on the problem identified on the email, fixes or paths to people debug the problem."
                }
            },
            "required": ["companyName", "incident", "severity", "reply", "fixes"]
        }
    }
]

class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email: {content} "

    messages = [{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    # companyName = eval(arguments).get("companyName")
    # relevance = eval(arguments).get("relevance")
    # purpose = eval(arguments).get("purpose")
    # category = eval(arguments).get("category")
    # reply = eval(arguments).get("reply")
    # suggested_reply = eval(arguments).get("suggested_reply")
    incident = eval(arguments).get("incident")
    title = eval(arguments).get("title")
    severity = eval(arguments).get("severity")
    fixes = eval(arguments).get("fixes")
    reply = eval(arguments).get("reply")

    return {
        "incident": incident,
        "title": title,
        "severity": severity,
        "fixes": fixes,
        "reply": reply
        }


# email = """
# Dear Jason 
# I hope this message finds you well. I'm Shirley from Gucci;

# I'm looking to purchase some company T-shirt for my team, we are a team of 100k people, and we want to get 2 t-shirt per personl

# Please let me know the price and timeline you can work with;

# Looking forward

# Shirley Lou
# """

# prompt = f"Please extract key information from this email: {email} "
# message = [{"role": "user", "content": prompt}]

# response = openai.ChatCompletion.create(
#     model="gpt-4-0613",
#     messages=message,
#     functions = function_descriptions,
#     function_call="auto"
# )

# print(response)