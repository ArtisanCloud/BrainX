import base64
import io
from enum import Enum

from PIL import Image
import numpy as np
import re

from sentence_transformers import SentenceTransformer

from app.logger import logger


class ContentType(Enum):
    PNG = 'image/png'
    JPEG = 'image/jpeg'
    GIF = 'image/gif'
    PDF = 'application/pdf'
    DOC = 'application/msword'
    DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    XLS = 'application/vnd.ms-excel'  # Excel xls 文件格式
    XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # Excel xlsx 文件格式
    MARKDOWN = 'text/markdown'  # Markdown 文件格式


# 常见文件类型的魔术字节
MAGIC_NUMBERS = {
    ContentType.PNG: ['89504E47'],
    ContentType.JPEG: ['FFD8FF'],
    ContentType.GIF: ['47494638'],
    ContentType.PDF: ['25504446'],
    ContentType.DOC: ['D0CF11E0A1B11AE1'],  # DOC 文件
    ContentType.DOCX: ['504B0304'],  # DOCX 文件
}


def image_base64_to_embed(image_string: str, clip_model: SentenceTransformer):
    try:
        # Step 1: Decode the base64 string
        decoded_image = base64.b64decode(image_string)
        # print("step 1", decoded_image)

        # Step 2: Create a BytesIO buffer from the decoded image
        image_buffer = io.BytesIO(decoded_image)
        # print("step 2", image_buffer)

        # Step 3: Create a BufferedReader from the BytesIO buffer
        image_reader = io.BufferedReader(image_buffer)
        # print("step 3", image_reader)

        # Step 4: Open the image using Image.open
        l_image = Image.open(image_reader)
        # print("step 4", l_image)

        # Step 5: Encode the image using clip_model.encode
        # print(clip_model, l_image)
        image_embedding = clip_model.encode(l_image)
        # print("step 5", image_embedding)

        # Step 6: Convert the embedding to a NumPy array
        image_embedding_array = np.array(image_embedding)
        # print("step 6")

        # Step 7: Convert the array to a list
        image_embedding_list = image_embedding_array.tolist()
        # print("step 7")

    except Exception as e:
        logger.error(f"Error in image_base64_to_embed: {e}", exc_info=True)
        raise e
    return image_embedding_list


def remove_base64_prefix(base64_data: str) -> str:
    # Split the string by the comma separator
    parts = base64_data.split(',', 1)
    if len(parts) > 1:
        # Return the part after the comma
        return parts[1]
    else:
        # If there's no comma, return the original string
        return base64_data


# 获取内容类型通过 Base64 前缀
def get_content_type_from_base64(base64_data: str) -> str:
    match = re.match(r'^data:(.*?);base64,', base64_data)
    return match.group(1) if match else None


# 将 Base64 转换为字节数组
def base64_to_bytes(base64_data: str) -> bytes:
    return base64.b64decode(remove_base64_prefix(base64_data))


# 通过魔术字节获取内容类型
def get_file_type_from_magic_numbers(base64_data: str) -> str:
    byte_data = base64_to_bytes(base64_data)
    header = byte_data[:4].hex().upper()
    for file_type, magics in MAGIC_NUMBERS.items():
        if any(header.startswith(magic) for magic in magics):
            return file_type
    return None
