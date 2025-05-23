import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

# Set up logging (customize as needed)
logger = logging.getLogger("request-logger")


MAX_BODY_LENGTH = 500


async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    method = request.method
    url_path = request.url.path
    query_params = dict(request.query_params)
    headers = dict(request.headers)

    # Read request body (can only do once, so we replace it)
    body = await request.body()
    body_text = body.decode("utf-8")
    # Optionally truncate to avoid logging massive payloads
    if len(body_text) > MAX_BODY_LENGTH:
        body_text = body_text[:MAX_BODY_LENGTH] + "...(truncated)"

    # Continue processing the request
    response = await call_next(request)

    logger.info(
        f"Request: {method} {url_path} -- {response.status_code}",
        extra={
            "method": method,
            "path": url_path,
            "params": query_params,
            "body": body_text,
            "code": response.status_code,
            "headers": headers,
        },
    )

    return response


def add_request_logging(app: FastAPI) -> None:
    app.middleware("http")(log_requests)
