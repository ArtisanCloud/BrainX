from sqlalchemy import select, func

from app.database.seed import init_user_uuid, init_tenant_uuid
from app.models.base import BaseStatus
from app.models.tenant.tenant import Tenant



# 添加代理人数据
async def seed_tenants(db) -> Exception | None:
    print("start seed tenants")
    try:
        # Check if the table is empty
        tenants_count = await db.scalar(select(func.count()).select_from(Tenant))
        # print(tenants_count)
        if tenants_count == 0:
            tenant = Tenant(
                uuid=init_tenant_uuid,
                name="初始用户租户",
                status=BaseStatus.ACTIVE,
            )
            # print(tenant)
            db.add(tenant)

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
            #         name='baidu-ai',
            #         model_name='ERNIE-Lite-8K',
            #         model_type='llm',
            #         encrypted_config='{"api_key": "your_api_key", "api_security": "your_api_security"}',
            #     ),
            # ]
            # model_providers[0].uuid = init_model_provider_uuid
            # db.add_all(model_providers)

            await db.flush()  # 添加 await 关键字

        print("success seed tenants -----------")
        return None

    except Exception as e:
        return e
