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
                    "name": "gpt-4",
                    "type": ModelType.LLM.value,
                    "description": 'An advanced language model with enhanced capabilities.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
                {
                    "name": "GPT-4o",
                    "type": ModelType.LLM.value,
                    "description": 'Optimized version of GPT-4 for specific tasks.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
                {
                    "name": "text-embedding-ada-002",
                    "type": ModelType.EMBEDDING.value,
                    "description": 'An efficient model for generating text embeddings.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
                {
                    "name": "text-embedding-3-small",
                    "type": ModelType.EMBEDDING.value,
                    "description": 'Small version of the text embedding model for lightweight applications.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
                {
                    "name": "text-embedding-3-large",
                    "type": ModelType.EMBEDDING.value,
                    "description": 'Large version of the text embedding model for more complex tasks.',
                    "encrypted_config": "{'api_key': 'your_openai_api_key', 'base_url': 'https://api.openai.com/v1/'}",
                },
            ],
        },
        {
            "name": "HuggingFace",
            "description": "HuggingFace offers a variety of transformer models for NLP and other AI tasks, including embeddings and language models.",
            "models": [
                {
                    "name": "bert-base-uncased",
                    "type": ModelType.LLM.value,
                    "description": 'A widely used transformer model for various NLP tasks.',
                    "encrypted_config": "{'api_key': 'your_huggingface_api_key', 'model_path': 'bert-base-uncased'}",
                },
                {
                    "name": "roberta-large",
                    "type": ModelType.LLM.value,
                    "description": 'A robustly optimized version of BERT for better performance.',
                    "encrypted_config": "{'api_key': 'your_huggingface_api_key', 'model_path': 'roberta-large'}",
                },
                {
                    "name": "shibing624_text2vec-base-chinese",
                    "type": ModelType.EMBEDDING.value,
                    "description": 'A base model for generating Chinese text embeddings.',
                    "encrypted_config": "{'api_key': 'your_huggingface_api_key', 'model_path': 'shibing624/text2vec-base-chinese'}",
                },
                {
                    "name": "clip-ViT-L-14",
                    "type": ModelType.IMAGE_EMBEDDING.value,
                    "description": 'A model for visual-text embedding using the CLIP architecture.',
                    "encrypted_config": "{'api_key': 'your_huggingface_api_key', 'model_path': 'openai/clip-vit-large-patch14'}",
                },
                {
                    "name": "vilt-b32-finetuned-vqa",
                    "type": ModelType.IMAGE_EMBEDDING.value,
                    "description": 'A model fine-tuned for visual question answering tasks.',
                    "encrypted_config": "{'api_key': 'your_huggingface_api_key', 'model_path': 'dandelin/vilt-b32-finetuned-vqa'}",
                },
            ],
        },
        {
            "name": "Baidu WenXin",
            "description": "Baidu WenXin provides advanced Chinese language models optimized for NLP tasks.",
            "models": [
                {
                    "name": "ERNIE-Lite-8K",
                    "type": ModelType.LLM.value,
                    "description": 'A Chinese language model optimized for various NLP tasks.',
                    "encrypted_config": "{'api_key': 'your_baidu_wenxin_api_key', 'base_url': 'https://wenxin.baidu.com/api/'}",
                },
            ],
        },
    ]
}
