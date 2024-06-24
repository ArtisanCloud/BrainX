from sqlalchemy import select, func

from app.models.app import App
from app.models.base import BaseStatus
from app.models.tenant import Tenant

init_tenant_uuid = "00000000-0000-0000-0001-1607772020bd"
init_model_provider_uuid = "3c189a18-ef3f-41fd-0002-1607772020bd"


# 添加代理人数据
async def seed_tenants(db) -> Exception | None:
    try:
        # Check if the table is empty
        tenants_count = await db.scalar(select(func.count()).select_from(Tenant))
        # print(tenants_count)
        if tenants_count == 0:

            app = App(
                name="test",
            )
            print(app)
            # tenant = Tenant(
            #         id=1,
            #         uuid=init_tenant_uuid,
            #         name="初始用户租户",
            #         status=BaseStatus.ACTIVE,
            #     )
            # print(tenant)
            # tenants = [
            #     tenant
            # ]
            #
            # db.add_all(tenants)

            # model_provider = ModelProvider(
            #     tenant_uuid=init_tenant_uuid,
            # )
            # model_provider.uuid = init_model_provider_uuid

            # db.add(model_provider)

            # await db.commit()  # 添加 await 关键字
        return None

    except Exception as e:
        return e
