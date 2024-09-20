from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config as app_config

engine = create_engine(app_config.SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
Base = declarative_base()


class BaseModel(Base):
	__abstract__ = True

	id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)


class AuditMixin(Base):
	__abstract__ = True

	created_at = Column(DateTime, nullable=False, default=datetime.now)
	updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
