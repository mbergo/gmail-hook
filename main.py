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
        "description": "Interpret the email content  & extract key info from an email, such as probability, using the given info for relationshp advice.",
        "parameters": {
            "type": "object",
            "properties": {
                "situation": {
                    "type": "string",
                    "description": "Situation of the person in question."
                },
                "action": {
                    "type": "string",
                    "description": "Which is the best approach for the person in question towards the loved one."
                },                                        
                "chances": {
                    "type": "string",
                    "description": "Try to identify the chances of success of the realionship. High, medium or low."
                },
                "suggestions": {
                    "type": "string",
                    "description": "Try to suggest activities that can improve their relationshp."
                },
                "move": {
                    "type": "string",
                    "description": "Try suggestion of micro actions that can be done to attract her his attention."
                },
                "topics": {
                    "type": "string",
                    "description": "Tru to identify topics discussed in the between the parts involved."
                }
            },
            "required": ["situation", "action", "chances", "suggestions", "move", "topics"]
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
    
    try:
        arguments = response.choices[0]["message"]["function_call"]["arguments"]
        situation = eval(arguments).get("situation")
        action = eval(arguments).get("action")
        chances = eval(arguments).get("chances")
        suggestions = eval(arguments).get("suggestions")
        move = eval(arguments).get("move")
        topics = eval(arguments).get("topics")
    except:
        situation = "",
        action = "",
        chances = "",
        suggestions = "",
        move = "",
        topics = ""
        pass
    
    


    return {
        "situation": situation,
        "action": action,
        "chances": chances,
        "suggestion": suggestions,
        "move": move,
        "topics": topics
    }
