# api/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
import google.generativeai as genai
from mangum import Mangum
import os

# Configure LLM API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="AI-Powered Bug Identifier")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class CodeSnippet(BaseModel):
    language: str
    code: str

class BugResponse(BaseModel):
    bug_type: str
    description: str
    suggestion: str | None = None

# POST /find-bug
@app.post("/find-bug", response_model=BugResponse)
def find_bug(snippet: CodeSnippet) -> Dict[str, str]:
    if not snippet.code.strip():
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty")
    
    if len(snippet.code.splitlines()) > 30:
        raise HTTPException(status_code=400, detail="Code snippet exceeds 30 lines")

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        You are a helpful AI bug finder.
        Language: {snippet.language}
        Code:
        {snippet.code}

        Identify:
        - Bug type (Logical Bug, Runtime Error, Syntax Error, Edge-case, Off-by-one, or None)
        - Description of the bug
        - Suggestion to fix it
        Return strictly in JSON with keys: bug_type, description, suggestion.
        """
        response = model.generate_content(prompt)
        text = response.candidates[0].content.parts[0].text if response.candidates else "{}"

        import json
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"bug_type": "Unknown", "description": text, "suggestion": None}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error from LLM: {str(e)}")

# GET /sample-cases
@app.get("/sample-cases", response_model=List[BugResponse])
def sample_cases() -> List[Dict[str, str]]:
    return [
        {
            "bug_type": "Logical Bug",
            "description": "The function returns True for odd numbers instead of even.",
            "suggestion": "Use `n % 2 == 0`",
        },
        {
            "bug_type": "Edge-case",
            "description": "The loop skips the first element at index 0.",
            "suggestion": "Use `range(len(arr))` instead of `range(1, len(arr))`",
        },
        {
            "bug_type": "Syntax Error",
            "description": "Assignment uses `=` instead of `==` in the if statement.",
            "suggestion": "Use `if x == 5:`",
        },
    ]

# Mangum handler for Vercel
handler = Mangum(app)
