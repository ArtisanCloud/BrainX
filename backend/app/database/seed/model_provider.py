from sqlalchemy import select, func

from app.database.seed.tenant import init_tenant_uuid
from app.models.model_provider import ModelProvider


# 添加代理人数据
async def seed_model_providers(db) -> Exception | None:
    try:
        # Check if the table is empty
        model_providers_count = await db.scalar(select(func.count()).select_from(ModelProvider))
        # print(model_providers_count)
        if model_providers_count == 0:
            model_providers = [
                ModelProvider(
                    tenant_uuid=init_tenant_uuid,
                    name='openai',
                    model_name='gpt-3.5-turbo',
                    model_type='llm',
                    encrypted_config='{"api_key": "your_api_key", "base_url": "https://api.openai.com"}',
                ),
                ModelProvider(
                    tenant_uuid=init_tenant_uuid,
                    name='baidu-ai',
                    model_name='ERNIE-Lite-8K',
                    model_type='llm',
                    encrypted_config='{"api_key": "your_api_key", "api_security": "your_api_security"}',
                ),
            ]
            db.add_all(model_providers)
            await db.commit()  # 添加 await 关键字

        return None

    except Exception as e:
        return e
