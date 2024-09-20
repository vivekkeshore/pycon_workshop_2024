# Pydantic
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserRegisterRequest(BaseModel):
	email: str = Field(
		..., min_length=8,
		max_length=255,
		examples=["vivek@senecaglobal.com"],
		pattern="[a-zA-Z_.]@senecaglobal.com"
	)
	password: str = Field(
		..., min_length=8,
		max_length=255,
		examples=["password"],
	)
	username: str = Field(
		..., min_length=4,
		max_length=128,
		examples=["vivek.keshore"]
	)
	name: str = Field(
		..., min_length=4,
		max_length=128,
		examples=["Vivek Keshore"]
	)
	phone: str = Field(
		None,
		min_length=10,
		max_length=20,
		examples=["1234567890"]
	)
	roles: list[str] = Field(
		...,
		examples=[["admin", "seller"], ["buyer"]]
	)


class UserRegisterResponse(BaseModel):
	id: UUID = Field(
		...,
		examples=["123e4567-e89b-12d3-a456-426614174000"]
	)
	email: str = Field(
		...,
		examples=["vivek.keshore@senecaglobal.com"]
	)
	username: str = Field(
		...,
		examples=["vivek.keshore"]
	)
	name: str = Field(
		...,
		examples=["Vivek Keshore"]
	)
	phone: str = Field(
		None,
		examples=["1234567890"]
	)
	created_at: datetime = Field(
		...,
		examples=["2020-01-01T00:00:00.000000"]
	)
	updated_at: datetime = Field(
		...,
		examples=["2020-01-01T00:00:00.000000"]
	)


class UserDetailResponse(UserRegisterResponse):
	pass
