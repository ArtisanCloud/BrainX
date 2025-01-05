from fastapi import APIRouter
from app.logger import logger

from app.config.config import settings

router = APIRouter()

@router.get("/status")
async def server_status():
    logger.info("Server status info")
    logger.error("Server status error")
    return {
        "name": settings.server.project_name,
        "system": True,
        "version": settings.server.version,
        "WorkerCount": settings.server.worker_count,
        "OllamaUrl": settings.ollama.url,
        # "api_auth": WEBUI_AUTH,
        # "default_models": app.state.DEFAULT_MODELS,
        # "default_prompt_suggestions": app.state.DEFAULT_PROMPT_SUGGESTIONS,
    }