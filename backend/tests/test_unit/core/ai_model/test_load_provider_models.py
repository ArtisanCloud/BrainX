from app.core.ai_model.model_provider.provider_manager import ProviderManager


def test_load_provider_models(tmp_path, monkeypatch):
    # 调用 load_provider_models 方法
    configurations = ProviderManager().load_provider_models()

    # 验证 configurations 是否正确加载
    assert configurations is not None
    assert "openai" in configurations
    assert "huggingface_hub" in configurations
    assert "wenxin" in configurations

    # 验证 OpenAI 提供商的模型类型和具体模型
    assert "models" in configurations["openai"], "OpenAI provider should have 'models' key."
    assert "llm" in configurations["openai"]["models"], "OpenAI provider should have 'llm' key."
    assert "gpt-3.5-turbo" in configurations["openai"]["models"]["llm"], "OpenAI provider should have 'gpt-3.5-turbo' key in 'llm'."
    assert "gpt-4" in configurations["openai"]["models"]["llm"], "OpenAI provider should have 'gpt-4' key in 'llm'."
    assert "text_embedding" in configurations["openai"]["models"], "OpenAI provider should have 'text_embedding' key."
    assert "ada-002" in configurations["openai"]["models"]["text_embedding"], "OpenAI provider should have 'ada-002' key."
    assert "davinci-002" in configurations["openai"]["models"]["text_embedding"], "OpenAI provider should have 'davinci-002' key."

    # 验证 Huggingface Hub 提供商的模型类型和具体模型
    assert "models" in configurations["huggingface_hub"], "Huggingface Hub provider should have 'models' key."
    assert "llm" in configurations["huggingface_hub"]["models"], "Huggingface Hub provider should have 'llm' key."
    assert "bert-base-uncased" in configurations["huggingface_hub"]["models"][
        "llm"], "Huggingface Hub provider should have 'bert-base-uncased' key in 'llm'."
    assert "roberta-large" in configurations["huggingface_hub"]["models"][
        "llm"], "Huggingface Hub provider should have 'roberta-large' key in 'llm'."
    assert "text_embedding" in configurations["huggingface_hub"]["models"], "Huggingface Hub provider should have 'text_embedding' key."
    assert "bert-base-uncased" in configurations["huggingface_hub"]["models"][
        "llm"], "Huggingface Hub provider should have 'bert-base-uncased' key in 'llm'."
    assert "roberta-large" in configurations["huggingface_hub"]["models"][
        "llm"], "Huggingface Hub provider should have 'roberta-large' key in 'llm'."

    # 验证 Wenxin 提供商的模型类型
    assert "models" in configurations["wenxin"], "Wenxin provider should have 'models' key."
    assert "llm" in configurations["wenxin"]["models"], "Wenxin provider should have 'llm' key."
    assert "ernie-lite-8k" in configurations["wenxin"]["models"][
        "llm"], "Wenxin Hub provider should have 'ernie-lite-8k' key in 'llm'."
