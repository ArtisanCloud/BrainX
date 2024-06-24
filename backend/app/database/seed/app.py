from sqlalchemy import select, func

from app.database.seed.tenant import init_tenant_uuid, init_model_provider_uuid
from app.models.app import App
from app.models.app import AppStatus, AppType
from app.models.app_model_config import AppModelConfig
from app.service.model_provider.service import ModelProviderService


# 添加代理人数据
async def seed_apps(db) -> Exception | None:
    try:
        # Check if the table is empty
        apps_count = await db.scalar(select(func.count()).select_from(App))

        if apps_count == 0:
            apps_data = [
                {
                    "uuid": "7c189a18-ef3f-41fd-bda1-1607772020bd",
                    "tenant_uuid": init_tenant_uuid,
                    # "model_provider_uuid": init_model_provider_uuid,
                    "name": "PowerWechat",
                    "description": "代理机器人1号",
                    "status": AppStatus.ACTIVE,
                    "type": AppType.AGENT,
                    "avatar_url": "app-product.png"
                },
                {
                    "uuid": "af932bfd-ff82-47e3-86bd-a31de67f8701",
                    "tenant_uuid": init_tenant_uuid,
                    # "model_provider_uuid": init_model_provider_uuid,
                    "name": "PowerX",
                    "description": "代理机器人1号",
                    "status": AppStatus.ACTIVE,
                    "type": AppType.AGENT,
                    "avatar_url": "app-tech.png"
                },
                {
                    "uuid": "a3f1dae1-5ce6-4b2d-b4be-0004914b819e",
                    "tenant_uuid": init_tenant_uuid,
                    # "model_provider_uuid": init_model_provider_uuid,
                    "name": "BrainX",
                    "description": "代理机器人1号",
                    "status": AppStatus.ACTIVE,
                    "type": AppType.AGENT,
                    "avatar_url": "app-market.png"
                }
            ]

            apps = get_apps_from_data(apps_data)
            db.add_all(apps)
            await db.commit()  # 添加 await 关键字

        return None

    except Exception as e:
        return e


def get_apps_from_data(db, data: list[dict]) -> list[App]:
    service = ModelProviderService(db)
    model_provider, exception = service.get_model_provider_by_uuid(init_model_provider_uuid)
    if exception:
        raise exception

    apps = []
    for item in data:
        app = App(
            uuid=item["uuid"],
            tenant_uuid=item["tenant_uuid"],
            app_model_config_uuid=item["app_model_config_uuid"],
            name=item["name"],
            description=item["description"],
            status=item["status"],
            type=item["type"],
            avatar_url=item["avatar_url"]
        )
        app.model_config = AppModelConfig(
            persona_prompt='',
        )
        app.model_config.model_provider = model_provider
        apps.append(app)

    return apps
