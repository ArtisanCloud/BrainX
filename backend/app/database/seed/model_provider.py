from sqlalchemy import select, func

from app.database.seed import init_tenant_uuid, init_model_provider_uuid
from app.models import Provider
from app.models.model_provider.provider_model import ProviderModel
from app.models.model_provider.provider import ProviderType


# 添加代理人数据
async def seed_model_providers(db) -> Exception | None:
    try:

        # Check if the table is empty
        providers_count = await db.scalar(select(func.count()).select_from(Provider))
        if providers_count == 0:
            providers = [
                Provider(
                    provider_name='OpenAI',
                    provider_type=ProviderType.SYSTEM.value,
                    encrypted_config='',
                    is_valid=True,
                ),
                Provider(
                    provider_name='HuggingFace',
                    provider_type=ProviderType.SYSTEM.value,
                    encrypted_config='',
                    is_valid=True,
                ),
                Provider(
                    provider_name='Baidu WenWin',
                    provider_type=ProviderType.SYSTEM.value,
                    encrypted_config='',
                    is_valid=True,
                )
            ]

            db.add_all(providers)
            await db.flush()  # 添加 await 关键字

            # Check if the table is empty
            model_providers_count = await db.scalar(select(func.count()).select_from(ProviderModel))
            # print(model_providers_count)
            if model_providers_count == 0:
                model_providers = [
                    ProviderModel(
                        provider_uuid=providers[0].uuid,
                        tenant_uuid=init_tenant_uuid,
                        model_name='gpt-3.5-turbo',
                        model_type='llm',
                        encrypted_config='{"api_key": "your_api_key", "base_url": "https://api.openai.com"}',
                    ),
                    ProviderModel(
                        provider_uuid=providers[2].uuid,
                        tenant_uuid=init_tenant_uuid,
                        model_name='ERNIE-Lite-8K',
                        model_type='llm',
                        encrypted_config='{"api_key": "your_api_key", "api_security": "your_api_security"}',
                    ),
                ]
                model_providers[0].uuid = init_model_provider_uuid
                db.add_all(model_providers)
                await db.flush()  # 添加 await 关键字

        return None

    except Exception as e:
        return e
