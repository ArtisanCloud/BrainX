from sqlalchemy import UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app import settings
from app.models.base import BasePivotModel, table_name_dataset, table_name_pivot_app_to_dataset
from app.models.app.app import table_name_app


class PivotAppToDataset(BasePivotModel):
    __tablename__ = table_name_pivot_app_to_dataset
    # 合并 schema 和约束条件
    __table_args__ = (
        UniqueConstraint('app_uuid', 'dataset_uuid', name='uq_app_to_dataset'),
        {'schema': settings.database.db_schema},
    )

    app_uuid = mapped_column(UUID(as_uuid=True),
                             ForeignKey(settings.database.db_schema + "." + table_name_app + ".uuid"),
                             nullable=False)
    dataset_uuid = mapped_column(UUID(as_uuid=True),
                                 ForeignKey(settings.database.db_schema + "." + table_name_dataset + ".uuid"),
                                 nullable=False)

    app: Mapped["App"] = relationship("App", back_populates="connected_dataset_pivots")
    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="connected_app_pivots")

    def __repr__(self):
        return (
            f"<PivotAppToDataset("
            f"uuid={self.uuid}, "
            f"app_uuid={self.app_uuid}, "
            f"dataset_uuid={self.dataset_uuid})>"
        )
