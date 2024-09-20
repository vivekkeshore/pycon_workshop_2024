import json
import logging

from fastapi import Request
from fastapi import Response, status
from fastapi.responses import JSONResponse
from starlette.types import Message

from app.lib.constants import JSON_SIZE_LIMIT, JSON_MIME_TYPE, CONTENT_TYPE

request_logger = logging.getLogger("RequestLogger")


async def peek_body(request: Request) -> bytes:
	body = await request.body()

	async def receive() -> Message:
		return {"type": "http.request", "body": body}

	request._receive = receive
	return body


def get_url_params_dict(url_params_list: list) -> dict:
	url_params = {}
	for param, val in url_params_list:
		if param in url_params:
			val_list = url_params[param]
			if not isinstance(val_list, list):
				val_list = [val_list]
			val_list.append(val)
			url_params[param] = val_list

		else:
			url_params[param] = val

	return url_params


async def logging_middleware(request: Request, call_next):
	if request.method == "OPTIONS":
		return JSONResponse(content="", status_code=status.HTTP_200_OK)

	query_params_dict = get_url_params_dict(request.query_params._list)
	log_params = {
		"path": request.url.path,
		"method": request.method,
		"params": query_params_dict,
	}
	try:
		content_type = request.headers.get(CONTENT_TYPE)
		if (content_type is not None) and (content_type.lower() == JSON_MIME_TYPE):
			await peek_body(request)
			json_body = await request.json()
		else:
			json_body = {}
	except json.decoder.JSONDecodeError:
		json_body = {}

	if json_body:
		if len(json.dumps(json_body)) > JSON_SIZE_LIMIT:
			return JSONResponse(
				status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
				content="JSON body exceeds the permitted size limit.",
			)

		log_params["json"] = json_body

	request_logger.debug(json.dumps(log_params))
	response: Response = await call_next(request)

	return response
