from app.constant.ai_model.provider import ProviderID
from app.models.model_provider.provider_model import ModelType

provider_config = {
    "providers": [
        {
            "name": ProviderID.OPENAI.value,
            "description": "OpenAI provides advanced language models and embeddings for various AI applications.",
            "models": [
                {
                    "name": "gpt-3.5-turbo",
                    "type": ModelType.LLM.value,
                    "description": 'A powerful language model_provider for various NLP tasks.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
                # {
                #     "name": "text-embedding-ada-002",
                #     "type": ModelType.TEXT_EMBEDDING.value,
                #     "description": 'An efficient model_provider for generating text embeddings.',
                #     "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                # },
            ],
        },
        {
            "name": ProviderID.HUGGINGFACE_HUB.value,
            "description": "Hugging Face Hub provides a centralized repository for pre-trained models and datasets.",
            "models": [
                {
                    "name": "shibing624_text2vec-base-chinese",
                    "type": ModelType.TEXT_EMBEDDING.value,
                    "description": 'An efficient model_provider for generating text embeddings.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
            ]
        }
    ]
}
