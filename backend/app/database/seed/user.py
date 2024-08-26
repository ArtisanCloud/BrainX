from sqlalchemy import select, func

from app.core.libs.security import hash_plain_password
from app.database.seed import init_user_uuid, init_tenant_uuid
from app.models.originaztion.user import User



# 添加代理人数据
async def seed_users(db) -> Exception | None:
    print("start seed users")
    try:
        # Check if the table is empty
        users_count = await db.scalar(select(func.count()).select_from(User))
        # print(users_count)
        if users_count == 0:
            user = User(
                uuid=init_user_uuid,
                tenant_owner_uuid=init_tenant_uuid,
                account='root',
                password=hash_plain_password("root"),
                name="初始用户", nick_name="default tenant",
                status="active",
            )
            db.add(user)

            # pivot = PivotTenantToUser(
            #     tenant_uuid=init_tenant_uuid,
            #     user_uuid=user.uuid,
            # )
            # pivot.generate_uuid()

            # print(pivot)
            # db.add(pivot)

            await db.flush()  # 添加 await 关键字

        print("success seed users -----------")
        return None

    except Exception as e:
        return e
