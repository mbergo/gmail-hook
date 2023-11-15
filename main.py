import fastapi
import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import api_key, Model, Completion
import json


load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "Categorize and extract key information from email, such as people, tasks, problems, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "The summary of the email writen in PT-BR."
                },                                        
                "tasks": {
                    "type": "string",
                    "description": "The tasks of the email writen in PT-BR. If there is more than one, please separate them with a comma."
                },
                "problems": {
                    "type": "string",
                    "description": "The problems of the email writen in PT-BR. If there is more than one, please separate them with a comma."
                },
                "conclusion": {
                    "type": "string",
                    "description": "The main idea that can be inferred from the email. Please write in PT-BR."
                }
            },
            "required": ["summary", "tasks", "problems", "conclusion" ]
        }
    }
]

class Email(BaseModel):
    from_email: str
    content: str
    
# function to exrtract info from email
def extract_info_from_email(summary, tasks, problems, conclusion):
    return json.dumps({"summary": summary, "tasks": tasks, "problems": problems, "conclusion": conclusion})

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/")
def read_item(email: Email):
    
    def get_emqil_content(email):
        return email.content.json()

# use gpt function call to extract info from email according to the new API ()

    response = openai.Completion.create(
        model="gpt-4-0613",
        prompt=email.content,
        functions = function_descriptions,
        function_call="auto"
    )
    
    extract_info_from_email = response.choices[0].text
    summary = eval(extract_info_from_email).get("summary")
    tasks = eval(extract_info_from_email).get("tasks")
    conclusion = eval(extract_info_from_email).get("conclusion")
    
    return {"summary": summary, "tasks": tasks, "conclusion": conclusion}



    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        prompt=email.content,
        functions = function_descriptions,
        function_call="auto"
    )
    
    extract_info_from_email = response.choices[0].text
    summary = eval(extract_info_from_email).get("summary")
    tasks = eval(extract_info_from_email).get("tasks")
    problems = eval(extract_info_from_email).get("problems")
    conclusion = eval(extract_info_from_email).get("conclusion")


    return {"summary": summary, "tasks": tasks, "problems": problems, "conclusion": conclusion}

response = read_item(content)
print(response)