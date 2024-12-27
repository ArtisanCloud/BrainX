import asyncio
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.config import settings

# 创建异步数据库引擎并配置连接池
async_db_engine = create_async_engine(
    settings.database.dsn,
    pool_size=5,          # 设置池大小（最大连接数）
    max_overflow=10,      # 最大溢出连接数
    pool_timeout=3,       # 设置连接池超时时间为3秒
    pool_recycle=3600,    # 连接重用时间（可选）
)

async_session_local = sessionmaker(
    async_db_engine, class_=AsyncSession, expire_on_commit=False
)



@pytest.mark.asyncio
async def test_connection_pool_auto_shrink():
    pool = async_db_engine.pool  # 获取连接池对象
    
    # 初始状态：池大小与活动连接数
    initial_pool_size = pool.size()  # 最大连接数
    initial_checked_out = pool.checkedout()  # 当前被使用的连接数
    print(f"Initial pool size: {initial_pool_size}")
    print(f"Initial checked-out connections: {initial_checked_out}")
    
    # 执行第一次数据库操作
    async with async_session_local() as session1:
        await session1.execute(text("SELECT 1"))
        print(f"Checked-out connections after first operation: {pool.checkedout()}")
    
        # 模拟多个并发操作，查看池的增长
        async with async_session_local() as session2:
            for index in range(10):
                await session2.execute(text("SELECT 1"))
                print(f"Checked-out connections after operation {index + 1}: {pool.checkedout()}")
        
    # 观察池的大小变化
    final_pool_size = pool.size()
    print(f"after multiple operations, Pool size : {final_pool_size}")
    final_checked_out = pool.checkedout()  # 获取当前被使用的连接数
    print(f"after multiple operations, Checked-out connections : {final_checked_out}")
    
    # 设置pool_timeout为3秒，等待5秒确保超时后连接会被回收
    timeout = 4
    await asyncio.sleep(timeout)  # 等待足够时间以确保超时
    pool_size_after_timeout = pool.size()
    checked_out_after_timeout = pool.checkedout()
    print(f"after timeout, Pool size : {pool_size_after_timeout}")
    print(f"after timeout, Checked-out connections : {checked_out_after_timeout}")
    
    # 验证连接池在超时后是否按预期缩减：池大小和活动连接数
    # 确保池大小没有增加，且检查出的连接数有所减少
    assert pool_size_after_timeout <= initial_pool_size, "after timeout, Connection pool size should not increase ."
    assert checked_out_after_timeout <= final_checked_out, "after timeout, Checked-out connections should decrease ."
    
    # 验证池内有足够的活动连接后，不会意外增加新连接
    assert checked_out_after_timeout <= final_checked_out, "after timeout if not in use, Checked-out connections should shrink ."


    # 这里添加断言，确保在所有操作后，checked-out 连接数为 0
    assert pool.checkedout() == 0, "after all operations and timeouts, There should be no checked-out connections ."

