from fastapi import APIRouter, status
from app.lib.exception_handler import error_handler

from app.schema_models import UserRegisterRequest, UserRegisterResponse
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
