from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# Initialize the FastAPI app
app = FastAPI()

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the request model
class EmailContent(BaseModel):
    content: str

# Function descriptions
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

# Function to process email content
def extract_info_from_email(email_content: str):
    from_email = str(email_content).split("\n")[0]
    content = str(email_content).split("\n")[1:]
    try:
        prompt = f"Email content (in Portuguese): {email_content}\n\n" \
                 f"Summarize the email, list the tasks, identify any problems, and state the conclusion. Write in Portuguese:"
        response = openai.Completion.create(
            engine="davinci-002",
            prompt=prompt,
            max_tokens=250
        )
        return response.choices[0].json()
    except Exception as e:
        return str(e)

# Define the POST endpoint
@app.post("/")
def process_email(email: EmailContent):
    from_email = str
    content = str
    extracted_info = extract_info_from_email(email.content)
    summary = eval(extracted_info["text"]).json()
    tasks = eval(extracted_info["text"]).json()
    problems = eval(extracted_info["text"]).json()
    conclusion = eval(extracted_info["text"]).json()

    # Further processing of extracted_info to match the required structure is needed here
    return {
        "summary": summary,  # Placeholder, replace with actual parsing logic
        "tasks": tasks,
        "problems": problems,
        "conclusion": conclusion
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
