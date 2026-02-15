from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response

def json_response(data: dict | None = None, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        }
    )


def error_json_response(
    http_status: int,
    status: str = "error",
    message: str | None = None,
    data: dict | None = None,
):
    if data is not None and not isinstance(data, dict):
        data = {"detail": str(data)}

    return aiohttp_json_response(
        status=http_status, # Убедитесь, что это int
        data={
            "status": status,
            "message": str(message) if message else "",
            "data": data or {},
        },
    )