import base64
import io
from PIL import Image
import numpy as np


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
