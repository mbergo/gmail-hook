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

def chat_completion_request( model="gpt-4-1106-preview", messages, functions, function_call):
    return openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messages,
        functions=functions,
        function_call=function_call
    )

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email: {content} "

    messages = [{"role": "user", "content": query}]

    response = chat_completion_request(
        model="gpt-4-1106-preview",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    summary = eval(response.choices[0].text)["summary"]
    tasks = eval(response.choices[0].text)["tasks"]
    problems = eval(response.choices[0].text)["problems"]
    conclusion = eval(response.choices[0].text)["conclusion"]



    

    return {
        "summary": summary,
        "tasks": tasks,
        "problems": problems,
        "conclusion": conclusion        }
