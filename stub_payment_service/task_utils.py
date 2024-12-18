import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from .loggers import logger


def create_strict_periodic_task(func: Callable, period: int, revokable: bool = False) -> asyncio.Task:
    async def inner(f: Callable) -> None:
        while True:
            try:
                await asyncio.sleep(period)
                if asyncio.iscoroutinefunction(f):
                    await f()
                else:
                    f()
            except Exception as exc:
                if revokable:
                    logger.exception(f"Error while performing periodic strict task with {f.__name__} - {exc}")
                    await asyncio.sleep(1)
                else:
                    raise exc

    return asyncio.create_task(inner(func))


def create_adaptive_periodic_task(func: Callable[..., Awaitable[Any]], period: int) -> asyncio.Task:
    def _handle_task_result(task: asyncio.Task) -> None:
        try:
            task.result()
        except asyncio.CancelledError:
            pass  # Task cancellation should not be logged as an error.
        except Exception as exc:
            logger.exception(f"Error while performing periodic adaptive task with {func.__name__} - {exc}")

    async def inner(f: Callable[..., Awaitable[Any]]) -> None:
        while True:
            task = asyncio.create_task(f())
            task.add_done_callback(_handle_task_result)
            await asyncio.sleep(period)

    return asyncio.create_task(inner(func))

