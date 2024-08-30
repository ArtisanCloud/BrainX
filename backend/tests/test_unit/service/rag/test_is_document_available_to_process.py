from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pytest

from app.models.rag.document import DocumentIndexingStatus, ContentType
from app.service.task.rag.service import RagProcessorTaskService


@pytest.fixture
def mock_document():
    return MagicMock()


def test_is_document_available_to_process(mock_document):
    # 模拟当前时间
    now = datetime(2024, 8, 30, 12, 0, 0)
    five_minutes_later = now + timedelta(minutes=5)

    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = now

        # 设置测试条件
        mock_document.indexing_status = DocumentIndexingStatus.PENDING.value
        mock_document.is_archived = False
        mock_document.dataset_uuid = "test-dataset-uuid"
        mock_document.created_user_by = "test-user-uuid"
        mock_document.error_message = None
        mock_document.error_at = None
        mock_document.is_paused = False
        mock_document.resource_uuid = "test-resource-uuid"
        mock_document.resource_url = None
        mock_document.content_type = ContentType.LOCAL_DOCUMENT.value
        mock_document.process_start_at = now
        mock_document.process_end_at = five_minutes_later
        mock_document.dataset_process_rule_uuid = "test-process-rule-uuid"

        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)

        # 断言文档可处理，且没有错误
        assert error is None, f"Unexpected error occurred: {error}"
        assert available, "Expected document to be available for processing"

        # 测试文档状态为 processing 时不可处理
        mock_document.indexing_status = DocumentIndexingStatus.INDEXING.value
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when status is processing: {error}")

        # 测试文档被归档时不可处理
        mock_document.is_archived = True
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when document is archived: {error}")

        # 测试文档缺少 dataset_uuid 时不可处理
        mock_document.is_archived = False
        mock_document.dataset_uuid = None
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when dataset_uuid is missing: {error}")

        # 测试文档缺少 created_user_by 时不可处理
        mock_document.dataset_uuid = "test-dataset-uuid"
        mock_document.created_user_by = None
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when created_user_by is missing: {error}")

        # 测试文档存在错误信息时不可处理
        mock_document.created_user_by = "test-user-uuid"
        mock_document.error_message = "Some error occurred"
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when document has an unresolved error: {error}")

        # 测试文档被暂停时不可处理
        mock_document.error_message = None
        mock_document.is_paused = True
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when document is paused: {error}")

        # 测试文档缺少资源 UUID 和 URL 时不可处理
        mock_document.is_paused = False
        mock_document.resource_uuid = None
        mock_document.resource_url = None
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when both resource UUID and URL are missing: {error}")

        # 测试文档内容类型无效时不可处理
        mock_document.resource_uuid = "test-resource-uuid"
        mock_document.content_type = "invalid_content_type"
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when document content type is invalid: {error}")

        # 测试处理时间不合理时不可处理
        mock_document.content_type = ContentType.LOCAL_DOCUMENT.value
        mock_document.process_start_at = five_minutes_later
        mock_document.process_end_at = now
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when process start time is after end time: {error}")

        # 测试缺少处理规则 UUID 时不可处理
        mock_document.process_start_at = now
        mock_document.process_end_at = five_minutes_later
        mock_document.dataset_process_rule_uuid = None
        available, error = RagProcessorTaskService.is_document_available_to_process(mock_document)
        assert not available
        assert error is not None
        print(f"Error when dataset process rule UUID is missing: {error}")
