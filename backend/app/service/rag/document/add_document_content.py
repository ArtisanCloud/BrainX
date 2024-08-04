import json
from typing import Tuple, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, DatasetSegmentRule
from app.schemas.rag.document import DocumentSchema, RequestAddDocumentContent
from app.service.rag.document.list import transform_documents_to_reply
from app.service.rag.dataset.service import DatasetService
from app.service.rag.document.service import DocumentService

from app.models.rag.document import Document, DocumentStatus, DocumentType


async def add_document_content(
        db: AsyncSession,
        user: User,
        data: RequestAddDocumentContent,
) -> Tuple[List[DocumentSchema] | None, Exception | None]:
    # 获取资源文件
    if data.media_resources is None or len(data.media_resources) == 0:
        return None, Exception("lack of document files")

    # 先获取dataset对象，确认用户拥有这个dataset
    service_dataset = DatasetService(db)
    dataset, exception = await service_dataset.app_dao.get_by_uuid(data.dataset_uuid)
    if exception is not None:
        return None, exception
    if dataset is None:
        return None, Exception("dataset not found")
    if dataset.tenant_uuid != user.tenant_owner_uuid:
        return None, Exception("user not authorized to access this dataset")

    # 加载dataset的segment_rule
    dataset, exception = await service_dataset.app_dao.load_segment_rule(dataset)

    if exception is not None:
        return None, exception
    # 如果没有，则创建新参数的segment_rule
    segment_rule = dataset.segment_rule
    if segment_rule is None:
        if data.rule_mode is None or data.rule is None:
            return None, Exception("lack of segment rule")
        rule = json.dumps(data.rule.dict())
        segment_rule = DatasetSegmentRule(
            dataset_uuid=dataset.uuid,
            mode=data.rule_mode,
            rules=rule,
        )
    else:
        # 如果易经存在了，则不需要更新segment_rule
        segment_rule = None

    # 创建document对象
    documents = []

    for index, media_source in enumerate(data.media_resources):
        documents.append(Document(
            tenant_uuid=user.tenant_owner_uuid,
            dataset_uuid=dataset.uuid,
            created_user_by=user.uuid,
            resource_uuid=media_source.uuid,
            title=media_source.filename,
            status=DocumentStatus.DRAFT,
            type=DocumentType.TEXT,
            document_index=index,
            resource_url=media_source.url,
        ))

    service_document = DocumentService(db)
    segment_rule, documents, exception = await service_document.add_content(segment_rule, documents)

    if exception:
        return None, exception

    return transform_documents_to_reply(documents), None
