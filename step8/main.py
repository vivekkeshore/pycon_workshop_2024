import logging

import uvicorn
from fastapi import FastAPI

import config as app_config
from app.apis import API_ROUTERS
from app.lib.cache import redis_cache

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(module)s | %(lineno)d | %(levelname)s | %(message)s")
app = FastAPI()


for router, kwargs in API_ROUTERS:
	app.include_router(router, **kwargs)

redis_cache.init_app(app_config.REDIS_HOST, app_config.REDIS_PORT, app_config.REDIS_DB)


if __name__ == "__main__":
	uvicorn.run("main:app", port=5010, reload=True)
