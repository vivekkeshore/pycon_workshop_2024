from sqlalchemy import Index, Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel, AuditMixin
from app.models.users.user import User


class Role(BaseModel, AuditMixin):
	__tablename__ = "role"
	__table_args__ = (
		Index("idx_role_name", "name", unique=True),
		{"schema": "users"},
	)

	name = Column(String(256), nullable=False)
	description = Column(String(256), nullable=True)


class UserRole(BaseModel, AuditMixin):
	__tablename__ = "user_role"
	__table_args__ = (
		Index("idx_user_role_role_id", "role_id", unique=False),
		Index("idx_user_role_user_id", "user_id", unique=False),
		{"schema": "users"},
	)
	user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
	role_id = Column(UUID(as_uuid=True), ForeignKey(Role.id), nullable=False)
	is_active = Column(Boolean(), default=True, nullable=False)
