import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.model_provider.provider_model import ProviderModelDAO
from app.database.seed import init_model_provider_uuid, init_user_uuid
from app.database.seed import init_tenant_uuid
from app.models.app.app import App
from app.models.app.app import AppStatus, AppType
from app.models.app.app_model_config import AppModelConfig


# 添加代理人数据
async def seed_apps(async_db: AsyncSession) -> Exception | None:
    print("start seed apps")
    try:
        # Check if the table is empty
        apps_count = await async_db.scalar(select(func.count()).select_from(App))

        if apps_count == 0:
            apps_data = [
                {
                    "uuid": "7c189a18-ef3f-41fd-bda1-1607772020bd",
                    "tenant_uuid": init_tenant_uuid,
                    "created_user_by": init_user_uuid,
                    # "app_model_config_uuid": init_model_provider_uuid+"01",
                    "name": "PowerWechat",
                    "description": "代理机器人1号",
                    "status": AppStatus.ACTIVE,
                    "type": AppType.AGENT,
                    "avatar_url": "images/app-product.png"
                },
                {
                    "uuid": "af932bfd-ff82-47e3-86bd-a31de67f8701",
                    "tenant_uuid": init_tenant_uuid,
                    "created_user_by": init_user_uuid,
                    # "app_model_config_uuid": init_model_provider_uuid+"02",
                    "name": "PowerX",
                    "description": "代理机器人1号",
                    "status": AppStatus.ACTIVE,
                    "type": AppType.AGENT,
                    "avatar_url": "images/app-tech.png"
                },
                {
                    "uuid": "a3f1dae1-5ce6-4b2d-b4be-0004914b819e",
                    "tenant_uuid": init_tenant_uuid,
                    "created_user_by": init_user_uuid,
                    #                     "app_model_config_uuid": init_model_provider_uuid+"03",
                    "name": "BrainX",
                    "description": "代理机器人1号",
                    "status": AppStatus.ACTIVE,
                    "type": AppType.AGENT,
                    "avatar_url": "images/app-market.png"
                }
            ]

            apps = await get_apps_from_data(async_db, apps_data)
            # print(apps)
            async_db.add_all(apps)
            await async_db.flush()  # 添加 await 关键字

        print("success seed apps -----------")
        return None

    except Exception as e:
        return e


async def get_apps_from_data(async_db: AsyncSession, data: list[dict]) -> list[App]:
    dao = ProviderModelDAO(async_db)

    apps = []
    for i, item in enumerate(data):
        try:
            # 将字符串转换为 UUID 对象
            app_model_config_uuid = uuid.UUID(init_model_provider_uuid + f"{i:02d}")
            # print(11111, app_model_config_uuid)
            # print(f"Converted UUID: {app_model_config_uuid}")
        except ValueError as e:
            print(f"Invalid UUID string: {e}")

        model_provider, exception = await dao.async_get_by_uuid(app_model_config_uuid)
        if exception:
            raise exception

        # print(model_provider)

        app = App(
            uuid=item["uuid"],
            tenant_uuid=item["tenant_uuid"],
            app_model_config_uuid=app_model_config_uuid,
            name=item["name"],
            description=item["description"],
            status=item["status"],
            type=item["type"],
            avatar_url=item["avatar_url"],
            created_user_by=init_user_uuid,
        )
        # print(app)
        # 创建 AppModelConfig 对象并设置其属性
        app_model_config = AppModelConfig(
            uuid=app_model_config_uuid,
            app_uuid=app.uuid,
            persona_prompt='',
        )
        app_model_config.model_provider = model_provider

        # 将 AppModelConfig 对象添加到当前会话
        db.add(app_model_config)

        # 将 AppModelConfig 对象与 App 对象关联
        app.model_config = app_model_config

        apps.append(app)

    return apps
