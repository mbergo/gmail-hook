import fastapi
from openai import Model, CompletionV1
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Example function description for OpenAI's new API structure
function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "Categorize and extract key information from email, such as people, tasks, problems, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "email_content": {
                    "type": "string",
                    "description": "The content of the email."
                }
            },
            "required": ["email_content"]
        }
    }
]

class FunctionCall(BaseModel):
    function: str
    parameters: dict

class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email: {content}"

    messages = [{"role": "user", "content": query}]

    function_call = {
        "function": "extract_info_from_email",
        "parameters": {"email_content": content}
    }

    model = Model(id="text-davinci-002", api_key=OPENAI_API_KEY)

    completion = model.complete(
        prompt=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        function_call=function_call,
        function_description=function_descriptions
    )

    response_data = completion.choices[0].text
    summary, tasks, problems, conclusion = eval(response_data)

    return {
        "summary": summary,
        "tasks": tasks,
        "problems": problems,
        "conclusion": conclusion     
    }

    completion = CompletionV1.create(
        engine=model.id,
        prompt=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        function_descriptions=function_descriptions,
        function_call=function_call.dict()
    )

    response_data = completion.choices[0].json()
    summary = response_data["summary"]
    tasks = response_data["tasks"]
    problems = response_data["problems"]
    conclusion = response_data["conclusion"]


    summary, tasks, problems, conclusion = eval(response_data)

    return {
        "summary": summary,
        "tasks": tasks,
        "problems": problems,
        "conclusion": conclusion     
    }
