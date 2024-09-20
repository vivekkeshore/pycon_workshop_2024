# Pydantic

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Query, Path
from pydantic import BaseModel, Field
from app.lib.constants import UUID_REGEX
from pydantic import Extra, model_validator


class BaseRoleRequest(BaseModel, extra=Extra.forbid):
	id: str = Field(
		..., pattern=UUID_REGEX, description="ID of the Role.",
		examples=["d1a5a8d8-2d9b-4e2e-9d3a-8e0d1b9c0f7c"]
	)


class GetRoleByIdRequest(BaseModel, extra=Extra.forbid):
	role_id: str = Path(
		..., pattern=UUID_REGEX, description="ID of the Role",
		examples=["123e4567-e89b-12d3-a456-426614174000"]
	)


class GetRoleByNameRequest(BaseModel, extra=Extra.forbid):
	name: str = Path(
		..., max_length=256, min_length=1,
		title="Role name", examples=["Admin"]
	)


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


class ListRoleRequest(BaseModel, extra=Extra.forbid):
	page: Optional[int] = Query(None, ge=1, description="Page Number", example=1)
	per_page: Optional[int] = Query(None, ge=1, description="Number of records per page", example=10)
	count: Optional[bool] = Query(
		False,
		description="Flag to count the number of records instead of returning the list",
		example=False
	)

	@model_validator(mode="before")
	def check_query_params(self):
		page, per_page, count = self.get('page'), self.get('per_page'), self.get('count')
		if (page or per_page) and count:
			raise ValueError('Cannot pass both count and page/per_page query params.')

		if (page or per_page) and not (page and per_page):
			raise ValueError('Both page and per_page params required for pagination.')

		return self


class SearchRoleRequest(ListRoleRequest):
	col: str = Query(
		..., min_length=1, max_length=20,
		description="Column name to filter the records."
	)
	value: str = Query(
		..., min_length=1, max_length=256,
		description="Column value for column name to filter the records."
	)


class UpdateRoleRequest(BaseRoleRequest):
	name: Optional[str] = Field(
		None, max_length=256, min_length=1,
		title="Role name", examples=["Admin"]
	)
	description: Optional[str] = Field(
		None, max_length=256, min_length=0,
		title="Role description", examples=["Admin description"]
	)

