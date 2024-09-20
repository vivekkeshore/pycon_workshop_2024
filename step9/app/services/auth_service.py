from random import randint

from fastapi.logger import logger

from app.lib.cache import redis_cache
from app.lib.custom_exceptions import RecordNotFoundError, InvalidPasswordException, InvalidDataException
from app.schema_models import LoginRequest, GetTokenRequest
from app.services.user_service import UserService
from app.lib.jwt_utils import generate_token
from app.db_layer import RoleDetailViewRepo


class AuthService:
	@staticmethod
	def user_login(login_request: LoginRequest):
		logger.info(f"Calling the login service for email id - {login_request.email}")
		try:
			user = UserService.get_user_by_email(login_request.email)
		except RecordNotFoundError:
			logger.info(f"User not found for email id - {login_request.email}")
			raise InvalidPasswordException("Username or password do not match.")

		if not user.verify_password(password=login_request.password):
			logger.info(f"Invalid password for email id - {login_request.email}")
			raise InvalidPasswordException("Username or password do not match.")

		otp = "".join([str(randint(0, 9)) for _ in range(6)])
		redis_cache.set(otp, login_request.email, expiration=120)  # 120 seconds expiration limit

		return otp

	@staticmethod
	def get_access_token(token_request: GetTokenRequest) -> str:
		logger.info(f"Calling the generate token service for email id - {token_request.otp}")

		email_id = redis_cache.get(token_request.otp)
		if not email_id:
			logger.info(f"Invalid or Expired OTP - {token_request.otp}")
			raise InvalidDataException("Invalid or expired OTP.")

		try:
			user = UserService.get_user_by_email(email_id)
		except RecordNotFoundError:
			logger.info(f"User not found for email id - {email_id}")
			raise InvalidDataException("User could not be validated for the given OTP.")

		roles = RoleDetailViewRepo().get_all_user_roles(user.id)
		role_names = [role.name for role in roles]
		payload = {
			"email": user.email,
			"user_id": str(user.id),
			"roles": role_names
		}
		token = generate_token(payload=payload)
		redis_cache.delete(token_request.otp)

		return token
