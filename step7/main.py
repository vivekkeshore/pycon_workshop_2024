import logging

import uvicorn
from fastapi import FastAPI, APIRouter, Query

from app.apis.user import user_router
from app.apis.role import role_router

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(module)s | %(lineno)d | %(levelname)s | %(message)s")
app = FastAPI()

ping_router = APIRouter()


@ping_router.get("/ping")
async def ping(name: str = Query(None, description="Name of the user", min_length=4, max_length=10, example="John")):
	"""
	This is a simple ping endpoint.
	"""
	if name:
		return f"Hello, {name}! App is running..."
	return "App is running..."


app.include_router(ping_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1/user")
app.include_router(role_router, prefix="/api/v1/role")

if __name__ == "__main__":
	uvicorn.run("main:app", port=5010, reload=True)
