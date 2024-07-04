from sqlalchemy import select, func

from app.models.base import BaseStatus
from app.models.tenant import Tenant

init_tenant_uuid = "00000000-0000-0000-0001-1607772020bd"


# 添加代理人数据
async def seed_tenants(db) -> Exception | None:
    print("start seed tenants")
    try:
        # Check if the table is empty
        tenants_count = await db.scalar(select(func.count()).select_from(Tenant))
        # print(tenants_count)
        if tenants_count == 0:
            tenant = Tenant(
                id=1,
                uuid=init_tenant_uuid,
                name="初始用户租户",
                status=BaseStatus.ACTIVE,
            )
            # print(tenant)
            db.add(tenant)

            # model_providers = [
            #     ModelProvider(
            #         tenant_uuid=init_tenant_uuid,
            #         name='openai',
            #         model_name='gpt-3.5-turbo',
            #         model_type='llm',
            #         encrypted_config='{"api_key": "your_api_key", "base_url": "https://api.openai.com"}',
            #     ),
            #     ModelProvider(
            #         tenant_uuid=init_tenant_uuid,
            #         name='baidu-ai',
            #         model_name='ERNIE-Lite-8K',
            #         model_type='llm',
            #         encrypted_config='{"api_key": "your_api_key", "api_security": "your_api_security"}',
            #     ),
            # ]
            # model_providers[0].uuid = init_model_provider_uuid
            # db.add_all(model_providers)

            await db.commit()  # 添加 await 关键字

        print("success seed tenants -----------")
        return None

    except Exception as e:
        return e
