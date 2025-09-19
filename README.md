# AI Bug Identifier

A simple web app that uses Google Gemini AI to analyze code snippets and identify potential bugs (logic, runtime, edge-case, or off-by-one errors).

## Features

- Supports multiple programming languages (Python by default).  
- Highlights logical, runtime, and off-by-one bugs.  
- Minimal frontend for testing code snippets.  
- FastAPI backend integrated with Google Gemini AI.  

## File Structure

```

zerotrail-bug-api/
│── api/
│   └── find-bug.py
│── frontend/
│   └── index.html
│── requirements.txt
│── README.md

````

## Setup (Local)

1. Clone the repository:

```bash
git clone https://github.com/USERNAME/zerotrail-bug-api.git
cd zerotrail-bug-api
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your Google API key in an environment variable:

```bash
setx GOOGLE_API_KEY "YOUR_API_KEY"   # Windows
```

4. Start the backend:

```bash
python -m uvicorn api.find-bug:app --reload
```

5. Open `frontend/index.html` in your browser to test.

## Deployment

* Recommended platforms: Vercel, Render, or Streamlit.
* Make sure to add the `GOOGLE_API_KEY` in the platform’s environment variables.
* Routes:

  * `/` → `frontend/index.html`
  * `/find-bug` → API endpoint

## Requirements

* fastapi
* uvicorn
* pydantic
* google-generativeai
* python-dotenv

## Notes

* `.env` file is ignored for security.
* API key should **never** be hardcoded.
