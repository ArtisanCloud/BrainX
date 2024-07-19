from typing import Optional

from pydantic import constr

from app.models.rag.dataset import DatasetSegmentRule, ImportType
from app.schemas.base import Pagination, ResponsePagination, BaseSchema, BaseObjectSchema


class DatasetSegmentRuleSchema(BaseObjectSchema):
    dataset_uuid: Optional[str] = None
    mode: Optional[str] = None
    rules: Optional[str] = None

    @classmethod
    def from_orm(cls, obj: DatasetSegmentRule):
        base = super().from_orm(obj)
        # print(base)
        return cls(
            **base,
            dataset_uuid=obj.dataset_uuid,
            mode=obj.mode,
            rules=obj.rules
        )


class RequestGetDatasetSegmentRuleList(BaseSchema):
    pagination: Optional[Pagination] = None


class ResponseGetDatasetSegmentRuleList(BaseSchema):
    data: list[DatasetSegmentRuleSchema]
    pagination: ResponsePagination


class RequestCreateDatasetSegmentRule(DatasetSegmentRuleSchema):
    pass


class ResponseCreateDatasetSegmentRule(BaseSchema):
    dataset_segment_rule: DatasetSegmentRuleSchema


class RequestPatchDatasetSegmentRule(DatasetSegmentRuleSchema):
    pass


class ResponsePatchDatasetSegmentRule(BaseSchema):
    dataset_segment_rule: DatasetSegmentRuleSchema


class ResponseDeleteDatasetSegmentRule(BaseSchema):
    result: bool


def make_dataset_segment_rule(dataset_segment_rule: DatasetSegmentRuleSchema) -> DatasetSegmentRule:
    return DatasetSegmentRule(
        dataset_uuid=dataset_segment_rule.dataset_uuid,
        mode=dataset_segment_rule.mode,
        rules=dataset_segment_rule.rules,

    )
