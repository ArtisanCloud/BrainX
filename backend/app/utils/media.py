import base64
import io
from enum import Enum

from PIL import Image
import numpy as np
import re


class ContentType(Enum):
    PNG = 'image/png'
    JPEG = 'image/jpeg'
    GIF = 'image/gif'
    PDF = 'application/pdf'
    DOC = 'application/msword'
    DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    # TXT 和 MD 文件没有特定的魔术字节，无法通过魔术字节检测


# 常见文件类型的魔术字节
MAGIC_NUMBERS = {
    ContentType.PNG: ['89504E47'],
    ContentType.JPEG: ['FFD8FF'],
    ContentType.GIF: ['47494638'],
    ContentType.PDF: ['25504446'],
    ContentType.DOC: ['D0CF11E0A1B11AE1'],  # DOC 文件
    ContentType.DOCX: ['504B0304'],  # DOCX 文件
}


def image_base64_to_embed(image_string, clip_model):
    # Step 1: Decode the base64 string
    decoded_image = base64.b64decode(image_string)

    # Step 2: Create a BytesIO buffer from the decoded image
    image_buffer = io.BytesIO(decoded_image)

    # Step 3: Create a BufferedReader from the BytesIO buffer
    image_reader = io.BufferedReader(image_buffer)

    # Step 4: Open the image using Image.open
    l_image = Image.open(image_reader)

    # Step 5: Encode the image using clip_model.encode
    image_embedding = clip_model.encode(l_image)

    # Step 6: Convert the embedding to a NumPy array
    image_embedding_array = np.array(image_embedding)

    # Step 7: Convert the array to a list
    image_embedding_list = image_embedding_array.tolist()

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
