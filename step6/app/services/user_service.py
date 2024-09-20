from app.schema_models import UserRegisterRequest
from app.db_layer import UserRepo


class UserService:
	@staticmethod
	def register_user(register_request: UserRegisterRequest):
		user = UserRepo().get_user_by_email(register_request.email)
		if user:
			raise ValueError("User already exists")

		user = UserRepo().create_user(register_request.model_dump())
		return user
