import base64

from app.core.brain.index import get_visual_query_embedding_model
from app.schemas.question_answer.visual_query import ResponseVisualQuery

from PIL import Image
from io import BytesIO


async def visual_query(
        image_string: any,
        question: str,
) -> (ResponseVisualQuery, Exception):

    processor, model = get_visual_query_embedding_model()

    try:

        decoded_image = base64.b64decode(image_string)

        # Load and process the image
        img = Image.open(BytesIO(decoded_image)).convert("RGB")

        # Prepare inputs
        encoding = processor(img, question, return_tensors="pt")

        # Forward pass
        outputs = model(**encoding)
        # print(outputs.last_hidden_state)
        logits = outputs.logits

        idx = logits.argmax(-1).item()
        answer = model.config.id2label[idx]

    except Exception as e:
        return "", e

    res = ResponseVisualQuery(answer=answer)

    return res, None
