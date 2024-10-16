from sqlalchemy import String, SmallInteger, ForeignKey, Boolean, UUID, Integer, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app import settings
from app.models.base import BaseORM, table_name_dataset, table_name_tenant, table_name_user, \
    table_name_dataset_segment_rule
from enum import IntEnum, Enum


class Dataset(BaseORM):
    __tablename__ = table_name_dataset  # 替换为实际的表名
    __table_args__ = {'schema': settings.database.db_schema}  # 动态指定 schema

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("public."+table_name_tenant + '.uuid'))
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey("public."+table_name_user + '.uuid'), nullable=False)
    updated_user_by = mapped_column(UUID(as_uuid=True), ForeignKey("public."+table_name_user + '.uuid'), nullable=True)

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

    dataset_uuid = mapped_column(UUID(as_uuid=True), ForeignKey(settings.database.db_schema+"." +table_name_dataset + '.uuid'))
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
