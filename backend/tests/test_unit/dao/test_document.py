from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.models.rag.document import Document, DocumentIndexingStatus
from app.models import User
from app.dao.rag.document import DocumentDAO
from tests import test_user_uuid, test_document_uuid


@pytest.mark.asyncio
async def test_set_indexing_status(db: AsyncSession):
    dao = DocumentDAO(db)
    user_uuid = UUID(test_user_uuid)
    document_uuid = UUID(test_document_uuid)
    # 创建一个文档和用户
    doc = Document(
        uuid=document_uuid,
        created_user_by=user_uuid,
        status=DocumentIndexingStatus.PENDING
    )

    user = User(
        uuid=UUID(test_user_uuid),
        account="test_account",
    )

    # 添加到数据库
    db.add(doc)
    db.add(user)
    await db.flush()

    # 设置状态
    document, error = await dao.async_set_indexing_status(doc, DocumentIndexingStatus.PARSING, user=user)

    assert document is not None
    assert error is None
    assert document.indexing_status == DocumentIndexingStatus.PARSING.value
    assert document.parse_start_at is not None
    assert document.updated_user_by == user_uuid

    # 设置错误状态
    document, error = await dao.async_set_indexing_status(doc, DocumentIndexingStatus.ERROR, error="Test error")

    assert document is not None
    assert error is None
    assert document.indexing_status == DocumentIndexingStatus.ERROR.value
    assert document.error_message == "Test error"
    assert document.error_at is not None
