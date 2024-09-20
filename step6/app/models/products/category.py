from sqlalchemy import Index, Column, String

from app.models.base_model import BaseModel, AuditMixin


class Category(BaseModel, AuditMixin):
	__tablename__ = "category"
	__table_args__ = (
		Index("idx_category_name", "name", unique=True),
		{"schema": "products"},
	)

	name = Column(String(256), nullable=False, unique=True)
	description = Column(String(256), nullable=True)
