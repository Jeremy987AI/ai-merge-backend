from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Allow frontend requests (adjust origin in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str
    user_id: str | None = None

@app.post("/ask")
async def ask_ai(req: PromptRequest):
    prompt = req.prompt
    user_id = req.user_id

    # Placeholder response merging function
    response = await merge_ai_responses(prompt)
    return {"merged_response": response}

async def merge_ai_responses(prompt):
    # This will call multiple AI APIs
    # Placeholder example below
    results = await asyncio.gather(
        call_openrouter(prompt),
        call_huggingface(prompt)
    )
    # Merge logic: just combine for now
    return "\n\n".join(results)

async def call_openrouter(prompt):
    return f"[OpenRouter AI says]: response to '{prompt}'"

async def call_huggingface(prompt):
    return f"[Hugging Face AI says]: response to '{prompt}'"
