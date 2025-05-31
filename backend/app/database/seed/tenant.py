from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.seed import init_user_uuid, init_tenant_uuid
from app.models.base import BaseStatus
from app.models.tenant.tenant import Tenant
from app.service.tenant.service import TenantService


# 添加代理人数据
async def seed_tenants(async_db: AsyncSession) -> Exception | None:
    print("start seed tenants")
    try:
        # Check if the table is empty
        tenants_count = await async_db.scalar(select(func.count()).select_from(Tenant))
        # print(tenants_count)
        if tenants_count == 0:
            tenant = Tenant(
                uuid=init_tenant_uuid,
                name="初始用户租户",
                status=BaseStatus.ACTIVE,
            )

            tenant_service = TenantService(async_db=async_db)
            _ = await tenant_service.add_tenant(tenant)
            # model_providers = [
            #     ProviderModel(
            #         tenant_uuid=init_tenant_uuid,
            #         name='openai',
            #         model_name='gpt-3.5-turbo',
            #         model_type='llm',
            #         encrypted_config='{"api_key": "your_api_key", "base_url": "https://api.openai.com"}',
            #     ),
            #     ProviderModel(
            #         tenant_uuid=init_tenant_uuid,
            #         name='wenxin-ai',
            #         model_name='ERNIE-Lite-8K',
            #         model_type='llm',
            #         encrypted_config='{"api_key": "your_api_key", "api_security": "your_api_security"}',
            #     ),
            # ]
            # model_providers[0].uuid = init_model_provider_uuid
            # db.add_all(model_providers)

        print("success seed tenants -----------")
        return None

    except Exception as e:
        return e
