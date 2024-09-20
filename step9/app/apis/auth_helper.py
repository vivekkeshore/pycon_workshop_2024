from fastapi import Depends, HTTPException, status
from fastapi.logger import logger
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

import config as app_config
from app.lib.constants import JWT_ALGORITHM
from app.lib.custom_exceptions import RecordNotFoundError
from app.services import UserService, RoleService

auth_scheme = HTTPBearer()
unauthorized_exception = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Unauthorized access. Token is invalid or expired.",
	headers={"WWW-Authenticate": "Bearer"}
)


async def authenticate_user(token: str = Depends(auth_scheme)):
	try:
		payload = jwt.decode(token.credentials, app_config.AUTH_SECRET_KEY, algorithms=[JWT_ALGORITHM])
		email = payload.get("email")
		if not email:
			raise unauthorized_exception

	except JWTError as ex:
		logger.error(f"Error decoding token. {ex}")
		raise unauthorized_exception

	user = UserService.get_user_by_email(email)

	return user


def authorize_role(role_name):
	def inner(user=Depends(authenticate_user)):
		role = RoleService.get_role_by_name(role_name)

		try:
			user_role = RoleService.get_user_role(user.id, role.id)
		except RecordNotFoundError:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail=f"Unauthorized access. User {user.email} does not have {role_name} role."
			)

		if not user_role.is_active:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail=f"Unauthorized access. Role is not active for the user {user.email}."
			)

		return user
	return inner
