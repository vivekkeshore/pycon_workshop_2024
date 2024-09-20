from sqlalchemy import Index, Column, String, ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel, AuditMixin
from app.models.products.product import Product
from app.models.users.user import User


class Review(BaseModel, AuditMixin):
	__tablename__ = "review"
	__table_args__ = (
		Index("idx_review_user_id", "user_id", unique=False),
		Index("idx_review_product_id", "product_id", unique=False),
		{"schema": "products"},
	)
	user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
	product_id = Column(UUID(as_uuid=True), ForeignKey(Product.id), nullable=False)
	rating = Column(Integer(), nullable=False)
	comment = Column(String(256), nullable=True)
