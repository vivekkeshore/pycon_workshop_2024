from fastapi import APIRouter, status

from app.lib.exception_handler import error_handler
from app.schema_models import RoleResponse, RoleCreateRequest
from app.services import RoleService

role_router = APIRouter()


@role_router.post(
	"/create", response_model=RoleResponse, status_code=status.HTTP_201_CREATED,
	tags=["Role APIs"]
)
@error_handler
async def create(crate_role_request: RoleCreateRequest):
	role = RoleService().create_role(crate_role_request)
	return role
