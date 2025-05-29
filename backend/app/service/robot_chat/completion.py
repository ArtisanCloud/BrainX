from typing import Dict
import ollama
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.brainx.service import BrainXService
from langchain.schema import HumanMessage, SystemMessage


async def completion(
        llm: str,
        async_db: AsyncSession,
        system: str = "",
        user: str = "",
        messages: Dict = None,
        images: list[str] | None = None,
):
    try:

        service_brain_x = BrainXService(
            llm=llm,
            async_db=async_db,
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
