from typing import Dict
import ollama
from app.core.brainx.base import LLMModel

from app.service.brainx.service import BrainXService
from langchain.schema import HumanMessage, SystemMessage


async def completion(
    llm: str,
    system: str = "",
    user: str = "",
    messages: Dict = None,
    images: list[str] | None = None,
):
    try:

        service_brain_x = BrainXService(
            llm,
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
