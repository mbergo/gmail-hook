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
                "from_email": {
                    "type": "string",
                    "description": "Email address of the person who sent the email."
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
                    "description": "Suggestions to improve the chances of success in the context of what was discussed."
                },
                "move": {
                    "type": "string",
                    "description": "Suggestion to propose a next move in order to increase his chances."
                },
                "topics": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Topics discussed in the between the parts involved."
                },
                "activities": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Activities that the person in question likes to do."
                },
            },
            "required": ["from_email", "action", "chances", "suggestions", "move", "topics", "activities"]
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
    from_email = eval(arguments).get("from_email")
    action = eval(arguments).get("action")
    chances = eval(arguments).get("chances")
    suggestions = eval(arguments).get("suggestions")
    move = eval(arguments).get("move")
    topics = eval(arguments).get("topics")
    activities = eval(arguments).get("activities")

    return {
        "from_email": from_email,
        "action": action,
        "chances": chances,
        "suggestion": suggestions,
        "move": move,
        "topics": topics,
        "activities": activities
    }
