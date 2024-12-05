from typing import Annotated

from fastapi import Depends

from .balance_service import BalanceService


def _balance_service_dep() -> BalanceService:
    return BalanceService()


BalanceServiceDep = Annotated[BalanceService, Depends(_balance_service_dep)]
