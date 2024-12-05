import time

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .configs.config import get_settings
from .db_service import DBConnectionContext
from .error_handlers import http422_error_handler, payment_error_handler, server_error_handler
from .exceptions import PaymentBaseError
from .loggers import logger
from .router import router
from .task_utils import create_strict_periodic_task


def get_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name, debug=settings.debug, version=settings.version)

    application.add_event_handler("startup", set_periodic)

    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(PaymentBaseError, payment_error_handler)
    application.add_exception_handler(Exception, server_error_handler)

    application.include_router(router)

    return application


def set_periodic() -> None:
    settings = get_settings()
    async def clear_payment_key_table():
        logger.info("Starting cleaning...")
        required_ts = int(time.time()) - 60  # 1 min
        async with DBConnectionContext() as conn:
            await conn.fetch(f"DELETE FROM paymentKey WHERE createdTS < {required_ts}")

    create_strict_periodic_task(
        clear_payment_key_table, settings.task.clear_payment_key_period, revokable=True
    )  # 5 minutes


# create app and serve forever with uvicorn
app = get_app()
