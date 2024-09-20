from typing import Union, List
from uuid import UUID

from fastapi.logger import logger

from app.db_layer import RoleDetailViewRepo
from app.db_layer import RoleRepo
from app.lib.custom_exceptions import DuplicateRecordError, DBFetchFailureException
from app.lib.custom_exceptions import RecordNotFoundError, CreateRecordException, UpdateRecordException
from app.lib.singleton import Singleton
from app.models import Role, RoleDetailView, User
from app.schema_models import RoleCreateRequest, ListRoleRequest, SearchRoleRequest, UpdateRoleRequest
from app.services.common_service import CommonService


class RoleService(metaclass=Singleton):
	@staticmethod
	def get_all_roles(query_params: ListRoleRequest) -> Union[List[Role], int]:
		roles = CommonService.get_all_records(RoleRepo(), query_params)
		return roles

	@staticmethod
	def get_role_by_name(role_name: str) -> Role:
		role = CommonService.get_record_by_name(RoleRepo(), role_name)
		return role

	@staticmethod
	def get_role_by_id(role_id: (UUID, str)) -> Role:
		role = CommonService.get_record_by_id(RoleRepo(), role_id)
		return role

	@staticmethod
	def search_roles(query_params: SearchRoleRequest) -> Union[List[Role], int]:
		roles = CommonService.search_records(RoleRepo(), query_params)
		return roles

	@staticmethod
	def get_user_role(user_id: (UUID, str), role_id: (UUID, str)) -> RoleDetailView:
		logger.info("Calling the get user role service. role id - {role_id} | user id - {user_id}")

		try:
			user_role = RoleDetailViewRepo().get_user_role(user_id=user_id, role_id=role_id)
		except Exception as ex:
			error_msg = f"An Error has occurred while fetching the user role - {user_id}"
			logger.error(f"{error_msg}. Error - {ex}", exc_info=True)
			raise DBFetchFailureException(error_msg)

		if not user_role:
			logger.debug(f"User role doesn't exist for user id: {user_id} and role id: {role_id}")
			raise RecordNotFoundError(f"User role doesn't exist for user id: {user_id}")

		logger.info(f"User role fetched successfully for user id: {user_id} | role_id: {role_id}")
		return user_role

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

	@staticmethod
	def update_role(update_request: UpdateRoleRequest, current_user: User) -> Role:
		logger.info("Calling the update role service.")
		role = RoleService.get_role_by_id(update_request.id)

		if role.name != update_request.name:
			try:
				RoleService.get_role_by_name(update_request.name)
			except RecordNotFoundError as ex:
				logger.info(
					f"Role doesn't exist with role name - {update_request.name}. Updating the role."
				)
			else:
				error_msg = f"Role already exists with role name: {update_request.name}"
				logger.error(error_msg)
				raise DuplicateRecordError(error_msg)

		try:
			role = RoleRepo().update(role, update_request, current_user)
		except Exception as ex:
			error_msg = f"An Error has occurred while updating the role with role id: {update_request.id}"
			logger.error(f"{error_msg}. Error - {ex}", exc_info=True)
			raise UpdateRecordException(error_msg)

		logger.info(f"Role updated successfully with role id: {update_request.id}")
		return role
