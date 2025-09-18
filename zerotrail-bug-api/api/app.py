# api/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from mangum import Mangum
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class CodeSnippet(BaseModel):
    language: str
    code: str

@app.post("/find-bug")
def find_bug(snippet: CodeSnippet):
    if not snippet.code.strip():
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty")

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
        Return in JSON.
        """
        response = model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text if response.candidates else {"bug_type": "None"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error from LLM: {str(e)}")

# ✅ Add Mangum handler for Vercel
handler = Mangum(app)
