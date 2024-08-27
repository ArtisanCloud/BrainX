from app.models.model_provider.provider_model import ModelType

provider_config = {
    "providers": [
        {
            "name": "OpenAI",
            "description": "OpenAI provides advanced language models and embeddings for various AI applications.",
            "models": [
                {
                    "name": "gpt-3.5-turbo",
                    "type": ModelType.LLM.value,
                    "description": 'A powerful language model for various NLP tasks.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
                {
                    "name": "text-embedding-ada-002",
                    "type": ModelType.EMBEDDING.value,
                    "description": 'An efficient model for generating text embeddings.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
            ],
        }
    ]
}
