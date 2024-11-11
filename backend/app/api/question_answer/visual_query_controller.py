import http

from fastapi import APIRouter, Form, UploadFile, File

from app.core.brainx.llm.langchain import get_llm, get_ollama_llm
from app.logger import logger
from app.schemas.base import ResponseSchema
from app.schemas.question_answer.visual_query import (
    RequestVisualQuery,
    ResponseVisualQuery,
)
from app.service.question_answer.visual_query import visual_query
from app.config.config import settings

router = APIRouter()


@router.post("/visual-query")
async def api_visual_query(
    query: RequestVisualQuery,
) -> ResponseVisualQuery | ResponseSchema:
    """
    query question_answer by text
    """

    try:
        base64Image = query.question_image
        if base64Image.startswith("data:") and "base64," in base64Image:
            # Remove the prefix
            base64Image = base64Image.split("base64,")[1]

        res, exception = await visual_query(base64Image, query.question)
        # print(res, exception)
        if exception:
            logger.error(exception)
            raise Exception("database query: pls check log")
        return res

    except Exception as e:
        # 在这里处理异常，您可以记录日志、返回特定的错误响应等
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)


import tempfile
import os
from typing import List
import ollama


@router.post("/visual-query-by-file")
async def api_visual_query_by_file(
    question: str = Form(...),  # 使用 Form 来接收表单字段
    llm: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # 写入上传的文件内容
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        # 在这里处理临时文件

        # print(question)
        # print(temp_path)

        try:
            response = ollama.chat(
                model="llama3.2-vision",
                messages=[
                    {
                        "role": "user",
                        "content": question,
                        "images": [temp_path],
                    }
                ],
            )

            # 从响应中提取实际的回答文本
            answer = response.get('message', {}).get('content', '')
            

        except ollama._types.ResponseError as e:
            raise Exception(f"Ollama API Error: {str(e)}")

        # 处理完成后删除临时文件
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        return  ResponseVisualQuery(answer=answer)
        

    except Exception as e:
        # 在这里处理异常，您可以记录日志、返回特定的错误响应等
        logger.error(e, exc_info=settings.log.exc_info)
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)
