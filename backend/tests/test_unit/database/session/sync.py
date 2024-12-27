import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database.session import get_database_sync_url


# 创建同步数据库引擎并配置连接池
sync_db_engine = create_engine(
    get_database_sync_url(),
    pool_size=5,          # 设置池大小（最大连接数）
    max_overflow=10,      # 最大溢出连接数
    pool_timeout=3,       # 设置连接池超时时间为3秒
    pool_recycle=3600,    # 连接重用时间（可选）
)

sync_session_local = sessionmaker(
    sync_db_engine, 
    expire_on_commit=False
)

@pytest.mark.parametrize("operation", ["first", "multiple", "timeout"])
def test_sync_connection_pool_auto_shrink(operation):
    pool = sync_db_engine.pool  # 获取连接池对象
    
    # 初始状态：池大小与活动连接数
    initial_pool_size = pool.size()  # 最大连接数
    initial_checked_out = pool.checkedout()  # 当前被使用的连接数
    print(f"Initial pool size: {initial_pool_size}")
    print(f"Initial checked-out connections: {initial_checked_out}")
    
    # 执行第一次数据库操作
    if operation == "first":
        with sync_session_local() as session1:
            session1.execute(text("SELECT 1"))
            print(f"Checked-out connections after first operation: {pool.checkedout()}")
    
    # 模拟多个并发操作，查看池的增长
    elif operation == "multiple":
        with sync_session_local() as session2:
            for index in range(10):
                session2.execute(text("SELECT 1"))
                print(f"Checked-out connections after operation {index + 1}: {pool.checkedout()}")
    
    # 设置pool_timeout为3秒，等待5秒确保超时后连接会被回收
    elif operation == "timeout":
        with sync_session_local() as session3:
            session3.execute(text("SELECT 1"))
        # 等待足够时间以确保超时
        import time
        time.sleep(5)
        pool_size_after_timeout = pool.size()
        checked_out_after_timeout = pool.checkedout()
        print(f"Pool size after timeout: {pool_size_after_timeout}")
        print(f"Checked-out connections after timeout: {checked_out_after_timeout}")
        
        # 断言池大小和活动连接数
        assert pool_size_after_timeout <= initial_pool_size, "Connection pool size should not increase after timeout."
        assert checked_out_after_timeout <= initial_checked_out, "Checked-out connections should decrease after timeout."
    
    # 断言连接池最后不应该有未归还的连接
    assert pool.checkedout() == 0, "There should be no checked-out connections after all operations."