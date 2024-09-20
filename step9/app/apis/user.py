from fastapi import APIRouter, status, Depends

from app.apis.auth_helper import authenticate_user, authorize_role
from app.lib.exception_handler import error_handler
from app.schema_models import UserRegisterRequest, UserRegisterResponse, UserDetailResponse
from app.services import UserService

user_router = APIRouter()


@user_router.post(
	"/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED,
	tags=["User APIs"]
)
@error_handler
async def register(register_request: UserRegisterRequest):
	user_details = UserService().register_user(register_request)
	return user_details


@user_router.get(
	"/me", response_model=UserDetailResponse,
	status_code=status.HTTP_200_OK, tags=["User APIs"]
)
@error_handler
async def get_current_user(current_user=Depends(authenticate_user)):
	return current_user


@user_router.get(
	"/get_by_email/{email}", response_model=UserDetailResponse,
	status_code=status.HTTP_200_OK, tags=["User APIs"],
	dependencies=[Depends(authorize_role("Admin"))]
)
@error_handler
async def get_user_detail(email: str):
	user_details = UserService().get_user_by_email(email)
	return user_details
