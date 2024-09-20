from fastapi import Query, APIRouter

from app.apis.role import role_router
from app.apis.user import user_router
from app.apis.auth import auth_router

ping_router = APIRouter()


@ping_router.get("/ping")
async def ping(
	name: str = Query(None, description="Name of the user", min_length=4, max_length=10, example="John")
):
	"""
	This is a simple ping endpoint.
	"""
	if name:
		return f"Hello, {name}! App is running..."
	return "App is running..."


API_ROUTERS = [
	(auth_router, {"prefix": "/api"}),
	(user_router, {"prefix": "/api/v1/user"}),
	(role_router, {"prefix": "/api/v1/role"}),
	(ping_router, {"prefix": ""})
]
