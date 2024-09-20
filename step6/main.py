from fastapi import FastAPI, APIRouter, Query
import uvicorn
from app.apis.user import user_router

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

if __name__ == "__main__":
	uvicorn.run("main:app", port=5010, reload=True)
