from sqlalchemy import select

from app.db_layer.sql_context import SqlContext
from app.models.users import Role, UserRole, RoleDetailView
from app.db_layer.base_repo import BaseRepo
from app.lib.singleton import Singleton


class RoleRepo(BaseRepo, metaclass=Singleton):
	def __init__(self):
		super().__init__(Role)

	def get_role_by_name(self, name):
		result = self.query.where(
			self.model.name.ilike(name)
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(result)

		return result.scalar()

	def get_role_by_id(self, role_id):
		result = self.query.where(
			self.model.id == str(role_id)
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(result)

		return result.scalar()

	def create_role(self, role_data, commit=True):
		role = self.model()
		role.set_attributes(role_data)

		if commit:
			with SqlContext() as sql_context:
				sql_context.session.add(role)

		return role


class UserRoleRepo:
	def __init__(self):
		self.model = UserRole
		self.query = select(UserRole)

	def get_user_role(self, user_id, role_id):
		result = self.query.where(
			self.model.user_id == str(user_id)
		).where(
			self.model.role_id == str(role_id)
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(result)

		return result.scalar()

	def create_user_role(self, user_id, role_id, commit=True):
		user_role = self.model()
		user_role.user_id = str(user_id)
		user_role.role_id = str(role_id)

		if commit:
			with SqlContext() as sql_context:
				sql_context.session.add(user_role)

		return user_role


class RoleDetailViewRepo:
	def __init__(self):
		self.model = RoleDetailView
		self.query = select(RoleDetailView)

	def get_all_user_roles(self, user_id):
		result = self.query.where(
			self.model.user_id == str(user_id)
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(result)

		return result.scalars()

	def get_user_role(self, user_id, role_id):
		result = self.query.where(
			self.model.user_id == str(user_id)
		).where(
			self.model.role_id == str(role_id)
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(result)

		return result.scalar()
