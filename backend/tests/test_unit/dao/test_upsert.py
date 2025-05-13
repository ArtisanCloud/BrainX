import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.libs.security import hash_plain_password
from app.dao.tenant.user import UserDAO
from app.models import User


@pytest.mark.asyncio
async def test_sync_upsert_create(async_db: AsyncSession):
    """测试 sync_upsert 创建新对象"""

    dao = UserDAO(async_db)

    obj = User(
        uuid="00000000-0000-0000-0001-1607772020bf",
        name="Mike", nick_name="mike",
        password=hash_plain_password("123456"),
        account="mike"
    )

    created_obj, err = await dao.async_upsert(obj, "uuid")

    assert err is None  # 确保没有错误
    assert created_obj is not None
    assert str(created_obj.uuid) == "00000000-0000-0000-0001-1607772020bf"
    assert created_obj.name == "Mike"
    assert created_obj.nick_name == "mike"

@pytest.mark.asyncio
async def test_sync_upsert_update(async_db: AsyncSession):
    """测试 sync_upsert 更新已存在的对象"""
    dao = UserDAO(async_db)

    # 先创建一个对象
    obj = User(
        uuid="00000000-0000-0000-0001-1607772020bf",
        name="Mike", nick_name="mike",
        password=hash_plain_password("123456"),
        account="mike"
    )
    _, err = await dao.async_create(obj)
    assert err is None

    # 创建一个新的对象，尝试更新
    updated_obj = User(
        uuid="00000000-0000-0000-0001-1607772020bf",
        name="Mike_updated", nick_name="mike_updated",
        password=hash_plain_password("123456"),
        account="mike_updated"
    )
    result_obj, err = await dao.async_upsert(updated_obj, "uuid")

    assert err is None  # 确保没有错误
    assert result_obj is not None
    assert result_obj.uuid == "00000000-0000-0000-0001-1607772020bf"
    assert result_obj.name == "Mike_updated"
    assert result_obj.nick_name == "mike_updated"

@pytest.mark.asyncio
async def test_sync_upsert_invalid_uid(async_db: AsyncSession):
    """测试 sync_upsert 传入无效的唯一标识字段"""
    dao = UserDAO(dasync_db)
    obj = User(
        uuid="10000000-0000-0000-0001-1607772020bb",
        name="Mike", nick_name="mike",
        password=hash_plain_password("123456"),
        account="mike"
    )

    result_obj, err = await dao.async_upsert(obj, "id")

    assert result_obj is None
    assert isinstance(err, ValueError)
    assert "unknown_field" in str(err)
