from typing import Dict
import ollama
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.brainx.base import LLMModel
from app.service.brainx.service import BrainXService
from langchain.schema import HumanMessage, SystemMessage


async def completion(
        tenant_uuid: str,
        user_uuid: str,
        provider: str,
        model: str,
        async_db: AsyncSession = None,
        sync_db: Session = None,
        system: str = "",
        user: str = "",
        messages: Dict = None,
        images: list[str] | None = None,
):
    try:

        service_brain_x = BrainXService(
            tenant_uuid=tenant_uuid,
            app=None,
            async_db=async_db,
            sync_db=sync_db,
            provider_id=provider,
            model_id=model,
            streaming=False,
        )

        if images is None or len(images) == 0:

            query = [SystemMessage(content=system), HumanMessage(content=user)]

            response, exception = service_brain_x.invoke(query=query)
            if exception:
                return None, exception
            return response.content, None

        else:
            response = ollama.chat(
                model=LLMModel.OLLAMA_LLAMA3_2_VISION.value,
                stream=False,
                messages=[
                    {
                        "role": "user",
                        "content": messages,
                        "images": images,
                    }
                ],
            )

            return response, None

    except Exception as e:
        return None, e
