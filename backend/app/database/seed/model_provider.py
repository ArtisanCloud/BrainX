from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant.provider_config import provider_config
from app.database.seed import init_tenant_uuid
from app.models import Provider
from app.models.model_provider.provider import ProviderType
from app.models.tenant.tenant import TenantDefaultModel


async def seed_default_tenant_models(async_db:AsyncSession) -> Exception | None:
    try:
        # Check if the table is empty
        providers_count = await async_db.scalar(select(func.count()).select_from(Provider))
        if providers_count == 0:
            providers = []
            models = []

            for provider_name, config in provider_config.items():

                provider = Provider(
                    tenant_uuid=init_tenant_uuid,
                    provider_name=provider_name,
                    provider_type=ProviderType.SYSTEM.value,
                    encrypted_config="",
                    is_valid=True,
                )
                async_db.add(provider)
                await async_db.flush()
                await async_db.refresh(provider)

                for model_name, model_configs in config["models"].items():
                    model = TenantDefaultModel(
                        tenant_uuid=init_tenant_uuid,
                        provider_uuid=provider.uuid,
                        provider_name=provider_name,
                        name=model_name,
                        type=model_configs["type"],
                    )
                    models.append(model)

                providers.append(provider)

            # Check if the table is empty
            model_providers_count = await async_db.scalar(
                select(func.count()).select_from(TenantDefaultModel)
            )
            # print(model_providers_count)
            if model_providers_count == 0:
                async_db.add_all(models)
                await async_db.flush()  # 添加 await 关键字

        return None

    except Exception as e:
        return e


# async def seed_model_providers(async_db:AsyncSession) -> Exception | None:
#     try:
#         provider_config = ProviderManager().load_provider_models()
#         # Check if the table is empty
#         providers_count = await db.scalar(select(func.count()).select_from(Provider))
#         if providers_count == 0:
#             providers = []
#             models = []
#
#             # print(provider_config)
#             for key, config in provider_config.items():
#                 provider = Provider(
#                     provider_name=config["provider"],
#                     provider_type=ProviderType.SYSTEM.value,
#                     encrypted_config='',
#                     is_valid=True,
#                 )
#                 async_db.add(provider)
#                 await async_db.flush()
#                 await async_db.refresh(provider)
#
#                 for model_type, model_configs in config["models"].items():
#                     for model_name, model_config in model_configs.items():
#                         model_display_name = model_config.get("title", {}).get("zh_Hans", model_name)
#                         model = ProviderModel(
#                             provider_uuid=provider.uuid,
#                             provider_name=config["provider"],
#                             tenant_uuid=init_tenant_uuid,
#                             model_name=model_display_name,
#                             model_type=model_type,
#                             encrypted_config='',
#                             is_valid=True,
#                         )
#                         models.append(model)
#
#                 providers.append(provider)
#
#             # Check if the table is empty
#             model_providers_count = await db.scalar(select(func.count()).select_from(ProviderModel))
#             # print(model_providers_count)
#             if model_providers_count == 0:
#                 async_db.add_all(models)
#                 await async_db.flush()  # 添加 await 关键字
#
#         return None
#
#     except Exception as e:
#         return e
