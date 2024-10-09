# Define the MediaResource models
from sqlalchemy.orm import mapped_column

from app import settings
from app.models.base import BaseORM, table_name_media_resource, table_name_tenant, table_name_user
from sqlalchemy import Column, Integer, String, Boolean, UUID, ForeignKey


class MediaResource(BaseORM):
    __tablename__ = table_name_media_resource
    __table_args__ = {'schema': 'public'}  # 动态指定 schema

    tenant_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("public."+table_name_tenant + '.uuid'))
    created_user_by = mapped_column(UUID(as_uuid=True), ForeignKey("public."+table_name_user + '.uuid'), nullable=False)
    filename = mapped_column(String, comment='名称')
    size = mapped_column(Integer, comment='尺寸')
    width = mapped_column(Integer, comment='宽度')
    height = mapped_column(Integer, comment='长度')
    url = mapped_column(String, comment='url')
    bucket_name = mapped_column(String, comment='Bucket名称')
    is_local_stored = mapped_column(Boolean, comment='是否本地存储', default=False)
    content_type = mapped_column(String, comment='内容类型')
    resource_type = mapped_column(String, comment='媒体类型')
    sort_index = mapped_column(Integer, comment='排序索引')

    def __repr__(self):
        return (
            f"MediaResource: "
            # f"id: {self.id}, "
            f"tenant_uuid: {self.tenant_uuid}, "
            f"created_user_by: {self.created_user_by}, "
            f"filename: {self.filename}, "
            f"size: {self.size}, "
            f"width: {self.width}, "
            f"height: {self.height}, "
            f"url: {self.url}, "
            f"bucket_name: {self.bucket_name}, "
            f"is_local_stored: {self.is_local_stored}, "
            f"content_type: {self.content_type}, "
            f"resource_type: {self.resource_type}, "
            f"sort_index: {self.sort_index}"
        )