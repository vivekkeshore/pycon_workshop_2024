# Pydantic

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RoleCreateRequest(BaseModel):
	name: str = Field(
		..., min_length=4,
		max_length=256,
		examples=["Admin", "Manager", "Buyer", "Seller"]
	)
	description: str = Field(
		None,
		min_length=10,
		max_length=256,
		examples=["This role is for Admin"]
	)


class RoleResponse(BaseModel):
	id: UUID = Field(
		...,
		examples=["123e4567-e89b-12d3-a456-426614174000"]
	)
	name: str = Field(
		...,
		examples=["Vivek Keshore"]
	)
	description: str = Field(
		None,
		examples=["This role is for Admin"]
	)
	created_at: datetime = Field(
		...,
		examples=["2020-01-01T00:00:00.000000"]
	)
	updated_at: datetime = Field(
		...,
		examples=["2020-01-01T00:00:00.000000"]
	)
