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
        "description": "categorise & extract key info from an email, such as urgency, tasks, summary, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the meet taken from the content."
                },
                "participant_names": {
                    "type": "string",
                    "description": "The name of the participants of the email. Upbeat, medium or down."
                },                                        
                "urgency": {
                    "type": "string",
                    "description": "The urgency of the tasks in the email. High, Medium or Low."
                },
                "tasks": {
                    "type": "string",
                    "description": "The tasks that the participants need to do. If there is more than one, please separate them with a comma."
                },
                "summary": {
                    "type": "string",
                    "description": "Summary of the email. Try to a small summary of the email. Basic what it is about."
                }
            },
            "required": ["title", "participant_names", "urgency", "tasks", "summary"]
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
    title = eval(arguments).get("title")
    participant_names = eval(arguments).get("participant_names")
    urgency = eval(arguments).get("urgency")
    tasks = eval(arguments).get("tasks")
    summary = eval(arguments).get("summary")
    


    return {
        "title": title,
        "participant_names": participant_names,
        "urgency": urgency,
        "tasks": tasks,
        "summary": summary
        }
