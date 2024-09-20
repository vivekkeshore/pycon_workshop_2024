from fastapi import APIRouter, status

from app.lib.exception_handler import error_handler
from app.schema_models import LoginRequest, LoginResponse, GetTokenRequest
from app.services import AuthService

auth_router = APIRouter()


@auth_router.post(
	"/login", response_model=LoginResponse,
	status_code=status.HTTP_200_OK, tags=["Auth APIs"]
)
@error_handler
async def login(login_request: LoginRequest):
	otp = AuthService.user_login(login_request)
	return {"otp": otp}


@auth_router.post(
	"/get_token",
	status_code=status.HTTP_200_OK, tags=["Auth APIs"]
)
@error_handler
async def get_token(token_request: GetTokenRequest):
	token = AuthService.get_access_token(token_request)
	return {"token": token}
