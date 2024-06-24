from app.logger import logger
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import SessionLocal


async def get_db_session() -> AsyncSession:
    from app.api.context_manager import context_set_db_session_rollback
    async with SessionLocal() as db:
        try:
            yield db
            #  commit the db session if no exception occurs
            #  if context_set_db_session_rollback is set to True then rollback the db session
            if context_set_db_session_rollback.get():
                logger.info('rollback db session')
                await db.rollback()
            else:
                await db.commit()
        except Exception as e:
            #  rollback the db session if any exception occurs
            logger.error(e)
            await db.rollback()
        finally:
            #  close the db session
            await db.close()
