from fastapi.logger import logger

from app.db_layer import UserRepo, UserRoleRepo
from app.db_layer.sql_context import SqlContext
from app.lib.custom_exceptions import DuplicateRecordError, DBFetchFailureException
from app.lib.custom_exceptions import RecordNotFoundError, CreateRecordException
from app.lib.singleton import Singleton
from app.models import User
from app.schema_models import UserRegisterRequest
from app.services.role_service import RoleService


class UserService(metaclass=Singleton):
	"""
	This class contains the business logic for the user related operations.
	"""
	@staticmethod
	def get_user_by_email(email: str) -> User:
		"""
		This method is used to get the user by email.

		Args:
			email (str): The email of the user.

		Returns:
			User: The user object.

		Raises:
			DBFetchFailureException: If an error occurs while fetching the user.
			RecordNotFoundError: If no user exists with the email.
		"""
		logger.info(f"Calling the get_user_by_email service. Email - {email}")
		try:
			user = UserRepo().get_user_by_email(email)
		except Exception as ex:
			error_msg = f"An Error has occurred while fetching the user details. Email - {email}"
			logger.error(f"{error_msg}. Error - {ex}", exc_info=True)
			raise DBFetchFailureException(error_msg)

		if not user:
			error_msg = f"No user exists with email - {email}"
			logger.debug(error_msg)
			raise RecordNotFoundError(error_msg)

		logger.info(f"User fetched successfully with email - {email}")
		return user

	@staticmethod
	def register_user(register_request: UserRegisterRequest) -> User:
		"""
		This method is used to register a new user.

		Args:
			register_request (UserRegisterRequest): The request object containing the user details.

		Returns:
			User: The user object.

		Raises:
			DuplicateRecordError: If the user already exists.
			DBFetchFailureException: If an error occurs while fetching the user
		"""
		logger.info("Calling the register_user service.")
		roles = []
		for role in register_request.roles:
			role = RoleService.get_role_by_name(role)
			roles.append(role)

		try:
			UserService.get_user_by_email(email=register_request.email)
		except RecordNotFoundError as ex:
			logger.info(f"User doesn't exist with email id - {register_request.email}. Creating a new user.")
		else:
			error_msg = f"User already exists with email id - {register_request.email}"
			logger.error(error_msg)
			raise DuplicateRecordError(error_msg)

		try:
			with SqlContext() as sql_context:
				user = UserRepo().create_user(register_request.model_dump(), commit=False)
				sql_context.session.add(user)
				sql_context.session.flush()
				for role in roles:
					user_role = UserRoleRepo().create_user_role(user.id, role.id, commit=False)
					sql_context.session.add(user_role)

		except Exception as ex:
			error_msg = f"An Error has occurred while registering the new user with email id - {register_request.email}"
			logger.error(f"{error_msg}. Error - {ex}", exc_info=True)
			raise CreateRecordException(error_msg)

		logger.info(f"User created successfully with email id - {register_request.email}")
		return user
