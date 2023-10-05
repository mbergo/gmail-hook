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
                "vmName": {
                    "type": "string",
                    "description": "the name of virtual machine quoted on the email."
                },                                        
                "Status": {
                    "type": "string",
                    "description": "Try to identify if said virtual machine was migrated already or not. Use just migrated or not migrated."
                },
                "Responsible":{
                    "type": "string",
                    "description": "Try to identify the person handling the migration. Use the name of the person. If it is not clear, use the name of the person who sent the email."
                },
                "Impedment": {
                    "type": "string",
                    "description": "Try to identify if the virtual machine is not migrated what is the impedment for it to be migrated. Use the impedment. If none just use None."
                },
                "jiraTickets": {
                    "type": "string",
                    "description": "Try to identify any Jira tickets related to the virtual machine. Use the Jira ticket number (XXX-0101). If none just use None."
                },
                "comments": {
                    "type": "string",
                    "description": "Try to identify any comments related to the virtual machine. Use the comment. If none just use None."
                },
            },
            "required": ["vmName", "Status", "Responsible", "Impedment", "jiraTickets", "comments"]
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
    vmName = eval(arguments).get("vmName")
    Status = eval(arguments).get("Status")
    Responsible = eval(arguments).get("Responsible")
    Impedment = eval(arguments).get("Impedment")
    jiraTickets = eval(arguments).get("jiraTickets")
    comments = eval(arguments).get("comments")

    
    return {
        "vmName": vmName,
        "Status": Status,
        "Responsible": Responsible,
        "Impedment": Impedment,
        "jiraTickets": jiraTickets,
        "comments": comments
        }
