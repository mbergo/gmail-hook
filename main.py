import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function specifications
function_descriptions = [
    {
        "type": "function",
        "function": {
            "name": "extract_info_from_email",
            "description": "Categorize and extract key info from an email, such as issue, type and gravity. All is related to MFT from Goanywhere.",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue": {
                        "type": "string",
                        "description": "The issue that the email is about, such as a bug, feature request, etc."
                    },                                        
                    "explanation": {
                        "type": "string",
                        "description": "A brief explanation of the issue."
                    },
                    "category": {
                        "type": "string",
                        "description": "Categorize this email in importance and urgency, such as low, medium, high."
                    },
                    "fix": {
                        "type": "string",
                        "description": "Identify if this email is about a fix and provide the fix how to, step-by-step."
                    }
                },
                "required": ["issue", "explanation", "category", "fix"]
            }
        }
    }
]

# Email data model
class Email(BaseModel):
    from_email: str
    content: str

@app.post("/")
def analyse_email(email: Email):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": f"Please extract key information from this email: {email.content}"}],
        tools=function_descriptions,
        tool_choice="auto"
    )

    if 'function_call' in response.choices[0]["message"]:
        arguments = eval(response.choices[0]["message"]["function_call"]["arguments"])

            issue = eval(arguments.get("issue"))
            explanation = eval(arguments.get("explanation"))
            category = eval(arguments.get("category"))
            fix = eval(arguments.get("fix"))
            
            return {
                "issue": issue,
                "explanation": explanation,
                "category": category,
                "fix": fix
            }
                             