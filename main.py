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
        "description": "categorise & extract key info from an email, such as use news, new tools, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "tools": {
                    "type": "string",
                    "description": "The name of the tools that David is using. If there is more than one, please separate them with a comma."
                },                                        
                "description": {
                    "type": "string",
                    "description": "The description each news on the email."
                },
                "category": {
                    "type": "string",
                    "description": "The category of the news. If there is more than one, please separate them with a comma."
                }
            },
            "required": ["tools", "description", "category"]  
        }
    }
]


class Email(BaseModel):
    from_email: str@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))

def chat_completion_request(messages, functions=None, function_call=None, model="gpt-4-0613"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

    content: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email: {content} "

    messages = [{"role": "user", "content": query}]

    response = chat_completion_request(
        model="gpt-4-0613",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    tools = eval(arguments).get("tools")
    description = eval(arguments).get("description")
    category = eval(arguments).get("category")


    return {
        "tools": tools,
        "description": description,
        "category": category
        }
