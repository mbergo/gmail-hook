import fastapi
from openai import api_key_management_v1, Model, CompletionV1
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

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

    function_call = FunctionCall(
        function="extract_info_from_email",
        parameters={"email_content": content}
    )

    model = Model(id="text-davinci-002")
    api_key = os.getenv("OPENAI_API_KEY")
    api_key_manager = api_key_management_v1.Client(api_key)
    api_key_manager.create_secret()
    api_key_manager.create_secret_version()
    api_key_manager.add_secret_to_model(model.id)

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

    response_data = completion.choices[0].text
    summary, tasks, problems, conclusion = eval(response_data)

    return {
        "summary": summary,
        "tasks": tasks,
        "problems": problems,
        "conclusion": conclusion     
    }
