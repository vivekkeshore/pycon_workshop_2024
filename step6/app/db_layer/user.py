from app.models.users import User
from sqlalchemy import select
from app.db_layer.sql_context import SqlContext


class UserRepo:
	def __init__(self):
		self.model = User
		self.query = select(User)

	def get_user_by_email(self, email_id):
		result = self.query.where(
			self.model.email == email_id
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(result)

		return result.scalar()

	def get_user_by_id(self, user_id):
		result = self.query.where(
			self.model.id == str(user_id)
		)

		with SqlContext() as sql_context:
			result = sql_context.execute(result)

		return result.scalar()

	def create_user(self, user_data, commit=True):
		user = self.model()
		user.set_attributes(user_data)

		if commit:
			with SqlContext() as sql_context:
				sql_context.session.add(user)

		return user
