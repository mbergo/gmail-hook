import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

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
def root():
    return {"message": "Hello World"}
    
@app.post("/")
def analyse_email(email: Email):
    messages = [{"role": "user", "content": f"Please extract key information from this email: {email.content}"}]

    # First API call
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        tools=function_descriptions,
        tool_choice="auto"
    )

    tool_calls = response.choices[0]["message"].get("tool_calls")

if tool_calls:
	for tool_call in tool_calls:
		# Extract tool_call_id
		tool_call_id = tool_call['id']
			if tool_call["function"]["name"] == "extract_info_from_email":
				arguments = json.loads(tool_call["function"]["arguments"])
				
				# Extracting each field separately
		issue = arguments.get("issue")
		explanation = arguments.get("explanation")
		category = arguments.get("category")
		fix = arguments.get("fix")

			# Include the processed responses in the conversation
			messages.append({
	"role": "tool", 
	"content": json.dumps(your_processed_response),
	"tool_call_id": tool_call_id  # Reference the specific tool call
})})

            # Second API call
            second_response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=messages
            )

        return second_response.choices[0]["message"]
    else:
        return {"message": "No function call made or different function called"}
                             