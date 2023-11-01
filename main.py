import fastapi
import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel





load_dotenv()

app = FastAPI()

openai.api_key = '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'

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as use situation, company name/product name, problem, requisition, etc. And please reply everything in the same language of the email.",
        "parameters": {
            "type": "object",
            "properties": {
                "psichologicalState": {
                    "type": "string",
                    "description": "The psichological state of the user. If there is more than one, please separate them with a comma."
                },                                        
                "mainProblem": {
                    "type": "string",
                    "description": "The main problem that the user is facing. If there is more than one, please separate them with a comma."
                },
                "suggestedActions": {
                    "type": "string",
                    "description": "The suggested actions that the user should take. If there is more than one, please separate them with a comma."
                },
                "summary": {
                    "type": "string",
                    "description": "The summary of the email regarding as a psychological session."
                }
            },
            "required": ["psichologicalState", "mainProblem", "suggestedActions", "summary"]
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
    psichologicalState = eval(arguments).get("psichologicalState")
    mainProblem = eval(arguments).get("mainProblem")
    suggestedActions = eval(arguments).get("suggestedActions")
    summary = eval(arguments).get("summary")

    return {
        "psichologicalState": psichologicalState,
        "mainProblem": mainProblem,
        "suggestedActions": suggestedActions,
        "summary": summary
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