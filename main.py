import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import httpx
from supabase import create_client, Client

app = FastAPI()

# Environment variables for API keys and URLs
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Models

class Question(BaseModel):
    prompt: str

class Feedback(BaseModel):
    prompt: str
    response: str
    rating: Literal[1, -1]  # 1 = thumbs up, -1 = thumbs down

# Endpoints

@app.get("/test")
async def test_endpoint():
    return {"message": "This is a test endpoint!"}

@app.post("/ask")
async def ask_question(question: Question):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourapp.com",  # Replace with your domain if you want
        "X-Title": "AI Merge Tool"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": question.prompt}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=body,
            headers=headers
        )
        reply = response.json()
        answer = reply["choices"][0]["message"]["content"]

    return {"answer": answer}

@app.post("/feedback")
async def store_feedback(data: Feedback):
    response = supabase.table("feedback").insert(data.dict()).execute()
    if response.status_code == 201:
        return {"message": "Feedback saved!"}
    else:
        return {"error": "Failed to save feedback", "details": response.data}

