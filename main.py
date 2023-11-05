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
                "emotionalState": {
                    "type": "string",
                    "description": "The emotional state of David. Fears, axieties, everything, comma separated."
                },                                        
                "problems": {
                    "type": "string",
                    "description": "The main problems that David  is facing. If there is more than one, please separate them with a comma."
                },
                "suggestedActions": {
                    "type": "string",
                    "description": "The suggested actions that the user should take. If there is more than one, please separate them with a comma."
                },
                "potentialPathologies": {
                    "type": "string",
                    "description": "The potential pathologies that the user might have. If there is more than one, please separate them with a comma."
                },
                "summary_rola": {
                    "type": "integer",
                    "description": "The number of time that word \"chupa\" was mentioned."
                }
            },
            "required": ["psichologicalState", "problems" "suggestedActions", "potentialPathologies", "summary_rola"]
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
    psichologicalState = eval(arguments).get("psichologicalState")
    problems = eval(arguments).get("problems")
    suggestedActions = eval(arguments).get("suggestedActions")
    potentialPathologies = eval(arguments).get("potentialPathologies")
    summary_rola = eval(arguments).get("summary_rola")

    return {
        "psichologicalState": psichologicalState,
        "problems": problems,
        "suggestedActions": suggestedActions,
        "potentialPathologies": potentialPathologies,
        "summary_rola": summary_rola
        }
