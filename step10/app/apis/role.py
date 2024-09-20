from fastapi import APIRouter, status, Depends
from typing import List, Union

from app.lib.exception_handler import error_handler
from app.schema_models import RoleResponse, RoleCreateRequest, ListRoleRequest, SearchRoleRequest, UpdateRoleRequest
from app.schema_models import GetRoleByNameRequest, GetRoleByIdRequest
from app.services import RoleService
from app.lib.pydantic_helper import make_dependable
from app.apis.auth_helper import authorize_role

role_router = APIRouter()


@role_router.post(
	"/create", response_model=RoleResponse, status_code=status.HTTP_201_CREATED,
	tags=["Role APIs"]
)
@error_handler
async def create(crate_role_request: RoleCreateRequest):
	role = RoleService().create_role(crate_role_request)
	return role


@role_router.get(
	"/list", response_model=Union[List[RoleResponse], int], status_code=status.HTTP_200_OK,
	tags=["Role APIs"]
)
@error_handler
async def list_roles(query_params: ListRoleRequest = Depends(make_dependable(ListRoleRequest))):
	roles = RoleService().get_all_roles(query_params)
	return roles


@role_router.get(
	"/get_by_name/{name}", response_model=RoleResponse, status_code=status.HTTP_200_OK,
	tags=["Role APIs"]
)
@error_handler
async def get_role_by_name(path_params: GetRoleByNameRequest = Depends()):
	role = RoleService().get_role_by_name(path_params.name)
	return role


@role_router.get(
	"/get_by_id/{role_id}", response_model=RoleResponse, status_code=status.HTTP_200_OK,
	tags=["Role APIs"]
)
@error_handler
async def get_role_by_id(path_params: GetRoleByIdRequest = Depends()):
	role = RoleService().get_role_by_id(path_params.role_id)
	return role


@role_router.get(
	"/search", response_model=Union[List[RoleResponse], int], status_code=status.HTTP_200_OK,
	tags=["Role APIs"]
)
@error_handler
async def search_roles(query_params: SearchRoleRequest = Depends(make_dependable(SearchRoleRequest))):
	roles = RoleService().search_roles(query_params)
	return roles


@role_router.put(
	"/update/{role_id}", response_model=RoleResponse, status_code=status.HTTP_200_OK,
	tags=["Role APIs"]
)
@error_handler
async def update_role(update_request: UpdateRoleRequest, current_user=Depends(authorize_role("Admin"))):
	role = RoleService().update_role(update_request, current_user)
	return role
