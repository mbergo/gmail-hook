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
                "action": {
                    "type": "string",
                    "description": "Which is the best approach for the person in question towards the loved one."
                },                                        
                "chances": {
                    "type": "string",
                    "description": "Try to identify the chances of success of the realionship. High, medium or low."
                }
            },
            "required": ["action", "chances"]
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
    action = eval(arguments).get("action")
    chances = eval(arguments).get("chances")

    return {
        "action": action,
        "chances": chances 
    }


# email = """
# Dear Jason 
# I hope this message finds you well. I'm Shirley from Gucci;

# I'm looking to purchase some company T-shirt for my team, we are a team of 100k people, and we want to get 2 t-shirt per personl

# Please let me know the price and timeline you can work with;

# Looking forward

# Shirley Lou
# """

# prompt = f"Please extract key information from this email: {email} "
# message = [{"role": "user", "content": prompt}]

# response = openai.ChatCompletion.create(
#     model="gpt-4-0613",
#     messages=message,
#     functions = function_descriptions,
#     function_call="auto"
# )

# print(response)