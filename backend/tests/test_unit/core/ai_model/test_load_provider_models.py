from typing import Dict

from app import settings
from app.constant.ai_model.huggingface_hub import HuggingFaceHubModelID
from app.constant.ai_model.openai import OpenAIModelID
from app.constant.ai_model.provider import ProviderID
from app.constant.ai_model.wenxin import WenxinModelID
from app.core.ai_model.provider_manager import ProviderManager
from app.core.ai_model.schema.provider import ProviderSchema
from app.core.rag import FrameworkDriverType


def test_load_provider_models(tmp_path, monkeypatch):
    # 调用 load_provider_models 方法
    configurations: Dict[str: ProviderSchema] = ProviderManager(settings.agent.framework_driver ).load_provider_models()

    # 验证 configurations 是否正确加载
    assert configurations is not None

    # 验证每个 provider 的配置是 ProviderSchema 类型
    for provider_name, schema in configurations.items():
        assert isinstance(schema, ProviderSchema), f"{provider_name} 的配置应该是 ProviderSchema 类型."

    # 验证特定提供者是否存在
    assert ProviderID.OPENAI.value in configurations, "OpenAI provider should be in configurations."
    assert ProviderID.HUGGINGFACE_HUB.value in configurations, "HuggingFace Hub provider should be in configurations."
    assert ProviderID.WENXIN.value in configurations, "Wenxin provider should be in configurations."

    # 验证 OpenAI 提供商的模型列表是否正确
    openai_schema = configurations[ProviderID.OPENAI.value]
    assert any(model.model == OpenAIModelID.GPT_3_5_TURBO.value for model in openai_schema.models), \
        "Huggingface Hub provider should have 'gpt-3.5-turbo' model_provider."

    # 验证 Huggingface Hub 提供商的具体模型名称
    hf_schema = configurations[ProviderID.HUGGINGFACE_HUB.value]
    assert any(model.model == HuggingFaceHubModelID.BERT_BASE_UNCASED.value  for model in hf_schema.models), \
        "Huggingface Hub provider should have 'bert-base-uncased' model_provider."
    assert any(model.model == HuggingFaceHubModelID.SHIBING624_TEXT2VEC_BASE_CHINESE.value for model in hf_schema.models), \
        "Huggingface Hub provider should have 'shibing624_text2vec-base-chinese' model_provider."

    # 验证 Wenxin 提供商的具体模型名称
    wenxin_schema = configurations[ProviderID.WENXIN.value]
    assert any(model.model == WenxinModelID.ERNIE_LITE_8K.value for model in wenxin_schema.models), \
        "Wenxin provider should have 'ernie-lite-8k' model_provider."
