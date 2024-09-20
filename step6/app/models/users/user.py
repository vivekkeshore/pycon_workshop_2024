from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Index, Column, String

from app.models.base_model import BaseModel, AuditMixin


class User(BaseModel, AuditMixin):
	__tablename__ = "user"
	__table_args__ = (
		Index("idx_user_name", "name", unique=False),
		Index("idx_user_email", "email", unique=True),
		{"schema": "users"},
	)

	name = Column(String(256), nullable=False)
	username = Column(String(256), nullable=False, unique=True)
	email = Column(String(256), unique=True, nullable=False)
	phone = Column(String(20), nullable=True)
	_password = Column("password", String(256), nullable=False)

	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, password):
		self._password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self._password)
