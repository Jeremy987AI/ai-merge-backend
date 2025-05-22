from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_ai(request: AskRequest):
    question = request.question

    responses = {}

    # === Call OpenRouter ===
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openrouter/auto",  # You can change this later
            "messages": [
                {"role": "user", "content": question}
            ]
        }
        async with httpx.AsyncClient() as client:
            openrouter_resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            )
            openrouter_text = openrouter_resp.json()['choices'][0]['message']['content']
            responses['openrouter'] = openrouter_text
    except Exception as e:
        responses['openrouter'] = f"Error: {str(e)}"

    # === Add more APIs here (Hugging Face, etc.) ===

    return {
        "question": question,
        "responses": responses
    }
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def query_openrouter(prompt: str, model: str = "mistralai/mistral-7b-instruct"):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",  # or localhost for now
        "X-Title": "AI Merge Assistant"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    url = "https://openrouter.ai/api/v1/chat/completions"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.json()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str
    model: str = "mistralai/mistral-7b-instruct"

@app.post("/ask/openrouter")
async def ask_openrouter(request: PromptRequest):
    try:
        response = await query_openrouter(request.prompt, request.model)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
