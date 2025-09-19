from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
import json

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

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.post("/find-bug")
async def find_bug(snippet: CodeSnippet):
    if not snippet.code.strip():
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty.")
    prompt = f"""
Analyze this {snippet.language} code and respond in JSON:
{snippet.code}
Include keys: bug_type, description, suggestion
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        # Safe access
        if response.candidates and len(response.candidates) > 0:
            text = response.candidates[0].content.parts[0].text
        else:
            text = '{"bug_type":"Unknown","description":"No response","suggestion":"Try again"}'
        return {"result": text}
    except Exception as e:
        return {"result": '{"bug_type":"Error","description":"'+str(e)+'","suggestion":"Check API key or model"}'}
