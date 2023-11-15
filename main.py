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
    summary = eval(arguments).get("summary")
    tasks = eval(arguments).get("tasks")
    problems = eval(arguments).get("problems")
    conclusion = eval(arguments).get("conclusion")


    return {
        "summary": summary,
        "tasks": tasks,
        "problems": problems,
        "conclusion": conclusion
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