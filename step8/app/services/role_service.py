from fastapi.logger import logger

from app.db_layer import RoleRepo
from app.lib.custom_exceptions import DuplicateRecordError, DBFetchFailureException
from app.lib.custom_exceptions import RecordNotFoundError, CreateRecordException
from app.lib.singleton import Singleton
from app.models import Role
from app.schema_models import RoleCreateRequest


class RoleService(metaclass=Singleton):
	@staticmethod
	def get_role_by_name(role_name: str) -> Role:
		logger.info("Calling the get role by name service.")

		try:
			role = RoleRepo().get_role_by_name(name=role_name)
		except Exception as ex:
			error_msg = f"An Error has occurred while fetching the role - {role_name}"
			logger.error(f"{error_msg}. Error - {ex}", exc_info=True)
			raise DBFetchFailureException(error_msg)

		if not role:
			error_msg = f"Role doesn't exist with role name: {role_name}"
			logger.debug(error_msg)
			raise RecordNotFoundError(error_msg)

		logger.info(f"Role fetched successfully with role name: {role_name}")
		return role

	@staticmethod
	def create_role(create_role_request: RoleCreateRequest) -> Role:
		logger.info("Calling the Create role service.")
		try:
			RoleService.get_role_by_name(create_role_request.name)
		except RecordNotFoundError as ex:
			logger.info(
				f"Role doesn't exist with role name - {create_role_request.name}. Creating a new role."
			)
		else:
			error_msg = f"Role already exists with role name: {create_role_request.name}"
			logger.error(error_msg)
			raise DuplicateRecordError(error_msg)

		try:
			role = RoleRepo().create_role(create_role_request.model_dump())
		except Exception as ex:
			error_msg = f"An Error has occurred while creating the new role with role name: {create_role_request.name}"
			logger.error(f"{error_msg}. Error - {ex}", exc_info=True)
			raise CreateRecordException(error_msg)

		logger.info(f"Role created successfully with role name: {create_role_request.name}")
		return role
