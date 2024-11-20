from datetime import datetime, timezone
from typing import List
import uuid

from sqlalchemy import String, SmallInteger, ForeignKey, Boolean, UUID, Integer, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app import settings
from app.models.base import BaseORM, table_name_dataset, table_name_tenant, table_name_user, \
    table_name_dataset_segment_rule, table_name_pivot_app_to_dataset
from enum import IntEnum, Enum

from app.models.rag.pivot_app_to_dataset import PivotAppToDataset


class Dataset(BaseORM):
    __tablename__ = table_name_dataset  # 替换为实际的表名
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("public." + table_name_tenant + '.uuid'))
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey("public." + table_name_user + '.uuid'),
                                    nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey("public." + table_name_user + '.uuid'),
                                    nullable=True)

    name = mapped_column(String)
    description = mapped_column(String)
    avatar_url = mapped_column(String)
    is_published = mapped_column(Boolean)

    dataset_format = mapped_column(SmallInteger, nullable=False)  # 使用枚举类型定义
    import_type = mapped_column(SmallInteger, nullable=False)  # 使用枚举类型定义
    driver_type = mapped_column(SmallInteger, nullable=False)  # 使用枚举类型定义
    word_count = mapped_column(Integer)
    token_count = mapped_column(Integer)
    embedding_model = mapped_column(String(255))
    embedding_model_provider = mapped_column(String(255))

    tenant: Mapped["Tenant"] = relationship(back_populates="datasets", foreign_keys=[tenant_uuid])
    documents: Mapped["Document"] = relationship(back_populates="dataset", foreign_keys="[Document.dataset_uuid]")
    segment_rule: Mapped["DatasetSegmentRule"] = relationship(back_populates="dataset",
                                                              foreign_keys="[DatasetSegmentRule.dataset_uuid]",
                                                              # uselist=False,
                                                              # lazy="select"
                                                              )
    connected_app_pivots: Mapped[List["PivotAppToDataset"]] = relationship(
        "PivotAppToDataset",
        back_populates="dataset",
    )

    connected_apps: Mapped[List["App"]] = relationship(
        "App",
        secondary=settings.database.db_schema + '.' + table_name_pivot_app_to_dataset,  # 中间表
        back_populates="connected_datasets",
        overlaps="app,connected_dataset_pivots,dataset,connected_app_pivots"
        # viewonly=True
    )

    def create_dataset(
        name: str = "Test Dataset",
        tenant_uuid: uuid.UUID = None,
        created_user_by: uuid.UUID = None,
        **kwargs
    ) -> "Dataset":
        """Create a Dataset instance for testing purposes with minimum required fields"""
        if tenant_uuid is None:
            tenant_uuid = uuid.uuid4()
        if created_user_by is None:
            created_user_by = uuid.uuid4()

        default_values = {
            "uuid": uuid.uuid4(),
            "tenant_uuid": tenant_uuid,
            "created_user_by": created_user_by,
            "name": name,
            "description": "Test dataset description",
            "avatar_url": "https://example.com/avatar.png",
            "is_published": True,
            "dataset_format": 1,
            "import_type": 1,
            "driver_type": 1,
            "word_count": 1000,
            "token_count": 1500,
            "embedding_model": "text-embedding-ada-002",
            "embedding_model_provider": "openai",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        # Override defaults with any provided kwargs
        default_values.update(kwargs)
        
        return Dataset(**default_values)

    def __repr__(self):
        description = self.description[:10] + '...' if self.description is not None else 'No description'
        return (
            f"<Dataset("
            # f"id={self.id}, "
            f"uuid={self.uuid}, "
            f"name='{self.name}', "
            f"tenant_uuid='{self.tenant_uuid}', "
            f"created_user_by='{self.created_user_by}', "
            f"updated_user_by='{self.updated_user_by}', "
            f"description='{description}', "
            f"avatar_url='{self.avatar_url}', "
            f"is_published='{self.is_published}', "
            f"driver_type='{self.driver_type}', "
            f"word_count='{self.word_count}', "
            f"token_count='{self.token_count}', "
            f"embedding_model='{self.embedding_model}', "
            f"embedding_model_provider='{self.embedding_model_provider})>"
        )


class SegmentID(Enum):
    line_break = '\n'
    two_line_break = '\n\n'
    chinese_period = '。'
    chinese_exclamation_mark = '！'
    english_period = '.'
    english_exclamation_mark = '!'
    chinese_question_mark = '？'
    english_question_mark = '?'


class PreProcessingRules(Enum):
    remove_stopwords = "delete_stopwords",
    replace_consecutive_spaces_break_tab = "replace_consecutive_spaces_break_tab",
    delete_urls_and_emails = "delete_urls_and_emails"


class SegmentationMode(IntEnum):
    AUTOMATIC = 1
    CUSTOM = 2


class DatasetSegmentRule(BaseORM):
    __tablename__ = table_name_dataset_segment_rule  # 替换为实际的表名
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    dataset_uuid = mapped_column(UUID(as_uuid=True),
                                 ForeignKey(settings.database.db_schema + "." + table_name_dataset + '.uuid'))
    mode = mapped_column(SmallInteger, nullable=False, default=SegmentationMode.AUTOMATIC)  # 使用枚举类型定义
    rules = mapped_column(Text, nullable=True)  # 自定义分段规则

    dataset: Mapped["Dataset"] = relationship(back_populates="segment_rule", foreign_keys=[dataset_uuid])

    AUTOMATIC_RULES = {
        'segmentation': {
            'segment_id': SegmentID.line_break,
            'max_chunk_length': 800,
            'overlap_chunk_length': 80
        },
        'text_preprocessing_rules': [
            {PreProcessingRules.remove_stopwords: False},
            {PreProcessingRules.replace_consecutive_spaces_break_tab: False},
            {PreProcessingRules.delete_urls_and_emails: False}
        ]
    }

    def __repr__(self):
        return (
            f"<SegmentRule("
            # f"id={self.id}, "
            f"uuid={self.uuid}, "
            f"dataset_uuid='{self.dataset_uuid}', "
            f"mode='{self.mode}', "
            f"rules='{self.rules}')>"
        )
