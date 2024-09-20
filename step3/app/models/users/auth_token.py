from sqlalchemy import Index, Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_model import BaseModel, AuditMixin
from app.models.users.user import User


class AuthToken(BaseModel, AuditMixin):
	__tablename__ = "auth_token"
	__table_args__ = (
		Index("idx_auth_token_user_id", "user_id", unique=False),
		Index("idx_auth_token_token_hash", "token_hash", unique=True),
		{"schema": "users"},
	)
	user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
	token = Column(String(512), nullable=False)
	token_hash = Column(String(256), nullable=False)
	valid_till = Column(DateTime(), nullable=False)
	is_active = Column(Boolean(), default=True, nullable=False)
