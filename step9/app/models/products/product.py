from sqlalchemy import Index, Column, String, ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel, AuditMixin
from app.models.products.category import Category


class Product(BaseModel, AuditMixin):
	__tablename__ = "product"
	__table_args__ = (
		Index("idx_product_name", "name", unique=False),
		Index("idx_product_category_id", "category_id", unique=False),
		{"schema": "products"},
	)
	category_id = Column(UUID(as_uuid=True), ForeignKey(Category.id), nullable=False)
	name = Column(String(256), nullable=False)
	description = Column(String(256), nullable=True)
	price = Column(Float(), nullable=False)
	stock = Column(Integer(), nullable=False)
