from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

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
