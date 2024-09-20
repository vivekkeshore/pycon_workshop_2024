import re
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.sql.sqltypes import Enum

from app.db_layer.sql_context import SqlContext
from app.lib.constants import UUID_REGEX
from app.models import User
from app.models.base_model import BaseModel
from app.schema_models import BaseModel as BaseModelSchema


class BaseRepo:
	def __init__(self, model):
		self.model = model
		self.query = select(model)

	def get_by_id(self, record_id):
		query = self.query.where(
			self.model.id == str(record_id)
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(query)

		return result.scalar()

	def get_by_col(self, col: str, value: (str, UUID, int, float)):
		query = self.query.where(
			getattr(self.model, col) == value
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(query)

		return result.scalars().all()

	def search_by_col(self, col, value):
		result = self.query.where(
			getattr(self.model, col).ilike(f"%{value}%")
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(result)

		return result.scalars().all()

	def get_all_query(self, query_params: BaseModelSchema, ilike: bool = False) -> [BaseModel]:
		query = self.query
		if ilike and (re.match(UUID_REGEX, query_params.value)):
			ilike = False

		if hasattr(query_params, "col") and query_params.col is not None:
			if (
				hasattr(self.model, "get_exact_match_cols") and
				query_params.col in self.model.get_exact_match_cols()
			) or isinstance(getattr(self.model, query_params.col).expression.type, Enum):
				ilike = False

			query = query.where(
				getattr(self.model, query_params.col) == str(query_params.value)
				if not ilike else
				getattr(self.model, query_params.col).ilike(f"%{query_params.value}%")
			)

		if (
			hasattr(query_params, 'is_active') and hasattr(self.model, 'is_active')
			and query_params.is_active is not None
		):
			query = query.where(self.model.is_active.is_(query_params.is_active))

		return query

	def get_all(self, query_params: BaseModelSchema, ilike: bool = False) -> [BaseModel]:
		query = self.get_all_query(query_params, ilike)
		if query_params.page and query_params.per_page:
			query = query.offset(
				(query_params.page - 1) * query_params.per_page
			).limit(query_params.per_page)

		with SqlContext() as sql_context:
			result = sql_context.execute(query)
			result = result.scalars().all()

		return len(result) if query_params.count else result

	@staticmethod
	def update(record: BaseModel, record_data: (BaseModelSchema, dict), current_user: User = None, commit: bool = True):
		record.set_attributes(record_data)

		record.modified_by = "system"
		if current_user:
			record.modified_by = current_user.name

		if commit:
			with SqlContext() as sql_context:
				sql_context.session.add(record)

		return record

	def create(self, record_data: (BaseModelSchema, dict), current_user: User = None, commit: bool = True):
		record = self.model()
		record.created_by = "system"
		if current_user:
			record.created_by = current_user.name

		record = self.update(record, record_data, current_user, commit)

		return record

	@staticmethod
	def delete(record: BaseModel):
		with SqlContext() as sql_context:
			sql_context.session.delete(record)

	@staticmethod
	def activate_deactivate_record(record: BaseModel, is_active: bool = True):
		record.is_active = is_active

		with SqlContext() as sql_context:
			sql_context.session.add(record)

		return record
