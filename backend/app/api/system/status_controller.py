from fastapi import APIRouter
import logging

from app.core.config import settings

router = APIRouter()

@router.get("/status")
async def server_status():

    return {
        "system": True,
        "version": settings.server.version,
        "WorkerCount": settings.server.worker_count,
        "OllamaUrl": settings.ollama.url,
        # "auth": WEBUI_AUTH,
        # "default_models": app.state.DEFAULT_MODELS,
        # "default_prompt_suggestions": app.state.DEFAULT_PROMPT_SUGGESTIONS,
    }