from datetime import datetime, timedelta

from jose import jwt

import config as app_config
from app.lib.constants import JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def generate_token(payload: dict, expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
	expiry_time = datetime.now() + timedelta(minutes=expire_minutes)
	payload.update({"exp": expiry_time})
	encoded_jwt = jwt.encode(payload, app_config.AUTH_SECRET_KEY, algorithm=JWT_ALGORITHM)

	return encoded_jwt
