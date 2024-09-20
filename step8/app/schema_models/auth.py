# Pydantic

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
	email: str = Field(
		..., min_length=8,
		max_length=255,
		examples=["vivek@senecaglobal.com"],
		pattern="[a-zA-Z0-9_.]@senecaglobal.com"
	)
	password: str = Field(
		..., min_length=8,
		max_length=255,
		examples=["abc123"],
	)


class OTPBaseModel(BaseModel):
	otp: str = Field(
		..., min_length=6,
		max_length=6,
		examples=["123456"],
	)


class LoginResponse(OTPBaseModel):
	pass


class GetTokenRequest(OTPBaseModel):
	pass
