from sqlalchemy import Index, Column, Integer, ForeignKey, Float, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel, AuditMixin
from app.models.enum_model import OrderStatus
from app.models.products.product import Product
from app.models.users.user import User


class Order(BaseModel, AuditMixin):
	__tablename__ = "order"
	__table_args__ = (
		Index("idx_order_user_id", "user_id", unique=False),
		{"schema": "orders"},
	)
	user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
	total_price = Column(Float(), nullable=False)
	status = Column(Enum(OrderStatus, name="order_status"), default=OrderStatus.PENDING, nullable=False)


class OrderItem(BaseModel, AuditMixin):
	__tablename__ = "order_item"
	__table_args__ = (
		Index("idx_order_item_order_id", "order_id", unique=False),
		Index("idx_order_item_product_id", "product_id", unique=False),
		{"schema": "orders"},
	)
	order_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
	product_id = Column(UUID(as_uuid=True), ForeignKey(Product.id), nullable=False)
	quantity = Column(Integer(), nullable=False)
	price = Column(Float(), nullable=False)
