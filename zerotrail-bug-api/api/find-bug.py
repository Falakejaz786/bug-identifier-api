from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSnippet(BaseModel):
    language: str
    code: str

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not found in environment")

genai.configure(api_key=api_key)

@app.post("/find-bug")
async def find_bug(snippet: CodeSnippet):
    if not snippet.code.strip():
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty.")

    prompt = f"""
Analyze this {snippet.language} code and respond strictly in JSON with keys:
bug_type, description, suggestion
Code:
{snippet.code}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.candidates[0].content.parts[0].text if response.candidates else ""

        # Strip Markdown ```json ... ``` if present
        cleaned = re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)

        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError:
            result = {"raw_response": text}

        return {"result": result}

    except Exception as e:
        return {"result": {"bug_type": "Error", "description": str(e), "suggestion": "Check API key or model"}}
