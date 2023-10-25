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
        "description": "categorise & extract key info from an email, such as use situatio, company name/product name, problem, requisition, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "the name of the company that sent the email or the product name which the email is about. Whatever is easier."
                },                                        
                "task": {
                    "type": "string",
                    "description": "Try to identify what is the purpose of the email, such as incident report or normal request. Return Request or Incident."
                },
                "summary":{
                    "type": "string",
                    "description": "Try to a small summary of the email. Basic what it is about."
                },
                "description": {
                    "type": "string",
                    "description": "Try to write a clearer description of the email for a DevOps understand easily."
                },
                "suggested_reply": {
                    "type": "string",
                    "description": "Suggest a reply to this email based I am devops open to new opportunities and not too formal."
                }
            },
            "required": [ "companyName", "task", "summary", "description", "suggested_reply"]
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
    task = eval(arguments).get("task")
    summary = eval(arguments).get("summary")
    description = eval(arguments).get("description")
    suggested_reply = eval(arguments).get("suggested_reply")


    return {
        "companyName": companyName,
        "task": task,
        "summary": summary,
        "description": description,
        "suggested_reply": suggested_reply
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