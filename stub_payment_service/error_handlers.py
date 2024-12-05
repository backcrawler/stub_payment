from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .exceptions import PaymentBaseError
from .loggers import logger


async def server_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unexpected exception: {exc}")
    return JSONResponse(content={"result": "failed", "reason": "internal_error"}, status_code=500)


async def payment_error_handler(_: Request, exc: PaymentBaseError) -> JSONResponse:
    if exc.code >= 500:
        logger.exception(f"Payment exception: {exc}")
    else:
        logger.warning(f"Payment error: {exc}")

    return JSONResponse(content={"result": "failed", "reason": exc.slug}, status_code=exc.code)


async def http422_error_handler(
    _: Request,
    exc: RequestValidationError | ValidationError,
) -> JSONResponse:
    return JSONResponse(
        {"errors": exc.errors()},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},  # noqa: UP032, UP030
    },
}
