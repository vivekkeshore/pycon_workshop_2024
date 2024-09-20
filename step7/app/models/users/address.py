from sqlalchemy import Index, Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel, AuditMixin
from app.models.users.user import User


class Address(BaseModel, AuditMixin):
	__tablename__ = "address"
	__table_args__ = (
		Index("idx_address_user_id", "user_id", unique=False),
		{"schema": "users"},
	)
	user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
	label = Column(String(256), nullable=True)
	address_line1 = Column(String(256), nullable=False)
	address_line2 = Column(String(256), nullable=True)
	city = Column(String(256), nullable=False)
	state = Column(String(256), nullable=False)
	zip_code = Column(String(10), nullable=False)
	country = Column(String(256), nullable=False)
	is_active = Column(Boolean(), default=True, nullable=False)
