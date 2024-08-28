from typing import Dict

from app.core.ai_model.model_provider.provider_manager import ProviderManager
from app.core.ai_model.model_provider.schema.provider import ProviderSchema


def test_load_provider_models(tmp_path, monkeypatch):
    # 调用 load_provider_models 方法
    configurations: Dict[str: ProviderSchema] = ProviderManager().load_provider_models()

    # 验证 configurations 是否正确加载
    assert configurations is not None

    # 验证每个 provider 的配置是 ProviderSchema 类型
    for provider_name, schema in configurations.items():
        assert isinstance(schema, ProviderSchema), f"{provider_name} 的配置应该是 ProviderSchema 类型."

    # 验证特定提供者是否存在
    assert "openai" in configurations, "OpenAI provider should be in configurations."
    assert "huggingface_hub" in configurations, "Huggingface Hub provider should be in configurations."
    assert "wenxin" in configurations, "Wenxin provider should be in configurations."

    # 验证 OpenAI 提供商的模型列表是否正确
    openai_schema = configurations["openai"]
    assert any(model.model == "gpt-3.5-turbo" for model in openai_schema.models), \
        "Huggingface Hub provider should have 'gpt-3.5-turbo' model."

    # 验证 Huggingface Hub 提供商的具体模型名称
    hf_schema = configurations["huggingface_hub"]
    assert any(model.model == "bert-base-uncased" for model in hf_schema.models), \
        "Huggingface Hub provider should have 'bert-base-uncased' model."
    assert any(model.model == "shibing624_text2vec-base-chinese" for model in hf_schema.models), \
        "Huggingface Hub provider should have 'shibing624_text2vec-base-chinese' model."

    # 验证 Wenxin 提供商的具体模型名称
    wenxin_schema = configurations["wenxin"]
    assert any(model.model == "ernie-lite-8k" for model in wenxin_schema.models), \
            "Wenxin provider should have 'ernie-lite-8k' model."