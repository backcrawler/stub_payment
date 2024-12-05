from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

from .dependencies import BalanceServiceDep
from .schemas import BalanceChange, MoneyExchange, OperationResultResponse

router = APIRouter()


@router.post(
    "/top-up",
    response_model=OperationResultResponse,
    status_code=status.HTTP_200_OK,
)
async def top_up_balance(
    balance_service: BalanceServiceDep,
    balance_change: BalanceChange,
    idempotency_key: str | None = Header(None),
):
    await balance_service.peer_balance(balance_change.user_id, balance_change.amount, idempotency_key)
    return JSONResponse(content={"result": "success"}, status_code=200)


@router.post(
    "/top-down",
    response_model=OperationResultResponse,
    status_code=status.HTTP_200_OK,
)
async def top_down_balance(
    balance_service: BalanceServiceDep,
    balance_change: BalanceChange,
    idempotency_key: str | None = Header(None),
) -> JSONResponse:
    await balance_service.peer_balance(balance_change.user_id, -balance_change.amount, idempotency_key)
    return JSONResponse(content={"result": "success"}, status_code=200)


@router.post(
    "/exchange",
    response_model=OperationResultResponse,
    status_code=status.HTTP_200_OK,
)
async def exchange_money(
    balance_service: BalanceServiceDep,
    money: MoneyExchange,
    idempotency_key: str | None = Header(None),
):
    await balance_service.exchange_balance(
        money.payer_user_id, money.payer_amount, money.buyer_user_id, idempotency_key
    )
    return JSONResponse(content={"result": "success"}, status_code=200)
