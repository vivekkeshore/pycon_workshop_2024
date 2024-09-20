from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schema_models import UserRegisterRequest, UserRegisterResponse
from app.services import UserService

user_router = APIRouter()


@user_router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(register_request: UserRegisterRequest):
	try:
		user_details = UserService().register_user(register_request)
	except ValueError as e:
		return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_409_CONFLICT)
	except Exception as e:
		return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return user_details

