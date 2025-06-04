from app.constant.ai_model.huggingface_hub import HuggingFaceHubModelID
from app.constant.ai_model.openai import OpenAIModelID
from app.constant.ai_model.provider import ProviderID
from app.core.brainx.entity.runtime.provider_model import ModelType

provider_config = {
    ProviderID.OPENAI.value: {
        "description": "OpenAI provides advanced language models and embeddings for various AI applications.",
        "models": {
            OpenAIModelID.GPT_3_5_TURBO.value: {
                "type": ModelType.LLM.value,
                "description": 'A powerful language model_provider for various NLP tasks.',
                "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
            },
        },
    },
    ProviderID.HUGGINGFACE_HUB.value: {
        "description": "Hugging Face Hub provides a centralized repository for pre-trained models and datasets.",
        "models": {
            HuggingFaceHubModelID.SHIBING624_TEXT2VEC_BASE_CHINESE.value: {
                "type": ModelType.TEXT_EMBEDDING.value,
                "description": 'An efficient model_provider for generating text embeddings.',
                "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
            },
        },
    }
}
