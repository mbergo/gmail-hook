import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json

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

@app.get("/")
def read_root():
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
			if tool_call["function"]["name"] == "extract_info_from_email":
				tool_call_id = tool_call['id']
				arguments = json.loads(tool_call["function"]["arguments"])

				# Prepare the response based on processed data
				processed_response = {
					"issue": arguments.get("issue"),
					"explanation": arguments.get("explanation"),
					"category": arguments.get("category"),
					"fix": arguments.get("fix")
				}

				# Append the response with the tool_call_id
				messages.append({
					"role": "tool",
					"content": json.dumps(processed_response),
					"tool_call_id": tool_call_id
				})

				# Append the response with the tool_calls
				messages.append({
					"role": "system",
					"content": "Tool calls processed successfully"
				})

	return response.choices[0]["message"]

# Second API call
# second_response = openai.ChatCompletion.create(
#     model="gpt-4-0613",
#     messages=messages,
#     tools=function_descriptions,
#     tool_choice="auto"
# )
# Second API call
# second_response = openai.ChatCompletion.create(
#     model="gpt-4-0613",
#     messages=messages
# )
# return second_response.choices[0]["message"]
else:
	return {"message": "No function call made or different function called"}

