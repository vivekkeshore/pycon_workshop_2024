from sqlalchemy import Index, Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel, AuditMixin, Base
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


class RoleDetailView(Base):
	__tablename__ = "role_detail_view"
	__table_args__ = (
		{"schema": "users"},
	)

	user_id = Column(UUID(as_uuid=True), primary_key=True)
	role_id = Column(UUID(as_uuid=True), primary_key=True)
	email = Column(String(256), primary_key=True)
	name = Column(String(256), primary_key=True)
	description = Column(String(256), primary_key=True)
	is_active = Column(Boolean, primary_key=True)
