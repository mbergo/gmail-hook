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
        "description": "categorise & extract key info from an email, such as tasks, problems and useful information.",
        "parameters": {
            "type": "object",
            "properties": {
                "people": {
                    "type": "array",
                    "description": "the names of people quoted on the email."
                },                                        
                "Problems": {
                    "type": "string",
                    "description": "Try to identify the problems that are mentioned on the email. Use the name of the problem. If it is not clear, use the name of the problem that is mentioned on the email."
                },
                "Tools":{
                    "type": "string",
                    "description": "Try to identify the tools that are mentioned on the email. Like clouds, SaaSs or tools. Use the name of the tool. If it is not clear, use the name of the tool that is mentioned on the email."
                },
                "Tasks": {
                    "type": "string",
                    "description": "Try to identify which tasks are being asked on the email. Use the name of the task. If it is not clear, use the name of the task that is mentioned on the email. Try to ennumerate them."
                },
                "Comments": {
                    "type": "string",
                    "description": "Try to identify any comments that have lots of relation with what was discussed which would be useful information. Use the name of the comment. If it is not clear, use the name of the comment that is mentioned on the email."
                },
            },
            "required": ["people", "Problems", "Tools", "Tasks", "Comments"]
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
    people = eval(arguments).get("people")
    Problems = eval(arguments).get("Problems")
    Tools = eval(arguments).get("Tools")
    Tasks = eval(arguments).get("Tasks")
    Comments = eval(arguments).get("Comments")

    
    return {
        "people": people,
        "Problems": Problems,
        "Tools": Tools,
        "Tasks": Tasks,
        "Comments": Comments
        }
