from sqlalchemy import select, func

from app.database.seed.tenant import init_tenant_uuid
from app.models.originaztion.user import User
from app.models.pivot_tenant_to_user import PivotTenantToUser

init_user_uuid = "00000000-0000-0000-0001-1607772020bd"

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
                account='root',
                name="初始用户", nick_name="default tenant",
                status="active",
            )
            db.add(user)

            pivot = PivotTenantToUser(
                tenant_uuid=init_tenant_uuid,
                user_uuid=user.uuid
            )
            pivot.generate_uuid()

            # print(pivot)
            db.add(pivot)

            await db.commit()  # 添加 await 关键字

        print("success seed users -----------")
        return None

    except Exception as e:
        return e
