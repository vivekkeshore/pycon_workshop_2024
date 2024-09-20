from sqlalchemy import Index, Column, ForeignKey, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel, AuditMixin
from app.models.products.product import Product
from app.models.users.user import User


class Cart(BaseModel, AuditMixin):
	__tablename__ = "cart"
	__table_args__ = (
		Index("idx_cart_user_id", "user_id", unique=False),
		{"schema": "orders"},
	)
	user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)


class CartItem(BaseModel, AuditMixin):
	__tablename__ = "cart_item"
	__table_args__ = (
		Index("idx_cart_item_cart_id", "cart_id", unique=False),
		Index("idx_cart_item_product_id", "product_id", unique=False),
		{"schema": "orders"},
	)
	cart_id = Column(UUID(as_uuid=True), ForeignKey(Cart.id), nullable=False)
	product_id = Column(UUID(as_uuid=True), ForeignKey(Product.id), nullable=False)
	quantity = Column(Integer(), nullable=False)
	price = Column(Float(), nullable=False)
