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
        "description": "categorise & extract key info from an email, such as use situation, company name/product name, problem, requisition, etc. And please reply everything in the same language of the email.",
        "parameters": {
            "type": "object",
            "properties": {
                "participant_names": {
                    "type": "string",
                    "description": "The name of the participants of the email. Upbeat, medium or down."
                },                                        
                "motivation_level": {
                    "type": "string",
                    "description": "The motivation level of each participant. If there is more than one, please separate them with a comma."
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
            "required": ["participant_names", "motivation_level", "tasks", "summary"]
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
    participant_names = eval(arguments).get("participant_names")
    motivation_level = eval(arguments).get("motivation_level")
    tasks = eval(arguments).get("tasks")
    summary = eval(arguments).get("summary")
    


    return {
        "participant_names": participant_names,
        "motivation_level": motivation_level,
        "tasks": tasks,
        "summary": summary
        }
