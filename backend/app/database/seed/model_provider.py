from sqlalchemy import select, func

from app.constant.provider_config import provider_config
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
            providers = []
            models = []
            for config in provider_config["providers"]:
                provider = Provider(
                        provider_name=config.get("name"),
                        provider_type=ProviderType.SYSTEM.value,
                        encrypted_config='',
                        is_valid=True,
                    )
                db.add(provider)
                await db.flush()
                await db.refresh(provider)

                for model_config in config["models"]:
                    model = ProviderModel(
                        provider_uuid=provider.uuid,
                        tenant_uuid=init_tenant_uuid,
                        model_name=model_config["name"],
                        model_type=model_config["type"],
                        encrypted_config=model_config["encrypted_config"],
                    )
                    models.append(model)

                providers.append(provider)

            # Check if the table is empty
            model_providers_count = await db.scalar(select(func.count()).select_from(ProviderModel))
            # print(model_providers_count)
            if model_providers_count == 0:
                db.add_all(models)
                await db.flush()  # 添加 await 关键字

        return None

    except Exception as e:
        return e
