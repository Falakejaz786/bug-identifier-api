from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import google.generativeai as genai
from mangum import Mangum
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSnippet(BaseModel):
    language: str
    code: str

@app.post("/")
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
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"bug_type": "Unknown", "description": text, "suggestion": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error from LLM: {str(e)}")

handler = Mangum(app)
