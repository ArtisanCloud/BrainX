from typing import Tuple, Any

from app.schemas.brainx.demo.format import DemoStructuredUserInfo, ResponseDemoFormatQuery
from app.service.brainx.service import BrainXService


async def demo_struct_output_invoke(
        question: str, llm: str,
):
    service_brain_x = BrainXService(
        llm,
        streaming=False,
    )

    template = """
        Answer the user query in the following format:
       
       {format_instructions}
       
       {query}
       
       基于以上的描述，请直接返回我要的json结果，不要其他的额外文字信息，我只要json格式!!!
       
       """

    return service_brain_x.invoke(
        query={
            "query": question,
        },
        temperature=0.1,
        template=template,
        output_schemas=DemoStructuredUserInfo
    )




async def demo_str_output_invoke(
        question: str, llm: str,
) -> Tuple[Any, Exception | None]:
    service_brain_x = BrainXService(
        llm,
        streaming=False,
    )

    background = "你是一位HR分析师"

    template = """
    {background}
    {query}
    {output}
    """

    output = "请给我一份简单的简历格式"

    return service_brain_x.invoke(
        query={
            "background": background,
            "query": question,
            "output": output,
        },
        template=template,
    )


async def demo_str_output_completion(
        question: str, llm: str,
) -> Tuple[Any, Exception | None]:
    service_brain_x = BrainXService(
        llm,
        streaming=False,
    )

    return service_brain_x.completion(
        query=question
    )
