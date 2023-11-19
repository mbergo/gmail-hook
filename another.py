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


# Function descriptions for OpenAI
function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "Categorize and extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "The name of the company that sent the email."
                },                                        
                "purpose": {
                    "type": "string",
                    "description": "Identify the purpose of the email, such as sales, customer support, consulting, partnership, etc."
                },
                "relevance": {
                    "type": "string",
                    "description": "Identify the relevance of the email, categorized as low, medium, high."
                },
                "category": {
                    "type": "string",
                    "description": "Categorize this email, like sales, customer support, consulting, partnership, etc."
                },
                "reply": {
                    "type": "string",
                    "description": "Identify if this email is a reply to a previous email."
                },
                "suggested_reply": {
                    "type": "string",
                    "description": "Suggest a reply to this email."
                }
            },
            "required": ["companyName", "purpose", "relevance", "category", "reply", "suggested_reply"]
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

@app.post("/analyse_email")
def analyse_email(email: Email):
    try:
        response = client.chat.completions.create(model="gpt-4-0613",
        messages=[{"role": "user", "content": f"Please extract key information from this email: {email.content}"}],
        functions=function_descriptions,
        function_call="auto")

        arguments = response.choices[0]["message"]["function_call"]["arguments"]

        return {
            "companyName": arguments.get("companyName"),
            "relevance": arguments.get("relevance"),
            "purpose": arguments.get("purpose"),
            "category": arguments.get("category"),
            "reply": arguments.get("reply"),
            "suggested_reply": arguments.get("suggested_reply")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
