import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set OpenAI API key


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
    
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/")
def analyse_email(email: Email):
    response = client.chat.completions.create(model="gpt-4-0613",
    messages=[{"role": "user", "content": f"Please extract key information from this email: {email.content}"}],
    tools=function_descriptions,
    tool_choice="auto")

    if 'function_call' in response.choices[0]["message"]:
        # Using eval to evaluate the string representation of the arguments dictionary
        arguments = eval(response.choices[0]["message"]["function_call"]["arguments"])
        return {
            "issue": arguments.get("issue"),
            "explanation": arguments.get("explanation"),
            "category": arguments.get("category"),
            "fix": arguments.get("fix")
        }
    else:
        return {"message": "No function call made or different function called"}

                             