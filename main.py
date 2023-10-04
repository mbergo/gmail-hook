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
        "description": "categorise & extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "the name of the company that sent the email"
                },                                        
                "purpose": {
                    "type": "string",
                    "description": "Try to identify what is the purpose of the email, such as 1. Sales 2. customer support; 3. consulting; 4. partnership; etc."
                },
                "relevance":{
                    "type": "string",
                    "description": "Try to identify the relevance of the emai. If it is a campaign email, it is not relevant; if it is a reply to a reply, it is relevant; if it customer sales, it is not relevant; etc. Categorise as low, medium, high as you see fit by if the email was sent to many people, the lower the relevance."
                },
                "category": {
                    "type": "string",
                    "description": "Try to categorise this email into categories like those: 1. Sales 2. customer support; 3. consulting; 4. partnership; etc."
                },
                "reply": {
                    "type": "string",
                    "description": "Try to identify if this email is a reply to a previous email or not. If it is a reply, it is a reply; if it is a new email, it is not a reply."
                }
            },
            "required": ["companyName", "purpose", "relevance", "category", "reply"]
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
    companyName = eval(arguments).get("companyName")
    relevance = eval(arguments).get("relevance")
    purpose = eval(arguments).get("purpose")
    category = eval(arguments).get("category")
    reply = eval(arguments).get("reply")


    return {
        "companyName": companyName,
        "relevance": relevance,
        "purpose": purpose,
        "category": category,
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