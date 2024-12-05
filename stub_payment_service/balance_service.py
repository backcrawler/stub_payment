import time

from asyncpg.exceptions import UniqueViolationError

from .db_service import DBConnectionContext
from .enums import IsolationLevelEnum
from .essentials import check_for_injections
from .exceptions import AccountNoExistsError, NoEnoughMoneyError, NoIdempKeyError, SameIdempRequestError


class BalanceService:
    async def peer_balance(self, user_id: str, amount: int, idempotency_key: str | None) -> None:
        if not idempotency_key:
            raise NoIdempKeyError

        async with DBConnectionContext() as conn:
            trans = conn.transaction(isolation=IsolationLevelEnum.repeatable_read)
            try:
                await trans.start()
                try:
                    current_ts = int(time.time())
                    await conn.fetch(
                        """INSERT INTO paymentKey (userId, externalKey, createdTS)
                        VALUES (:user_id, :idempotency_key, :current_ts)"""
                    ).bindparams(user_id=user_id, idempotency_key=idempotency_key, current_ts=current_ts)
                except UniqueViolationError as exc:
                    raise SameIdempRequestError from exc

                await self.check_current_balance_for_change(conn, user_id, amount)

                await conn.fetch(
                    """INSERT INTO customer (userId, balance) VALUES (:user_id, :amount)
                    ON CONFLICT (userId) DO UPDATE SET balance = customer.balance + :amount
                    """
                ).bindparams(user_id=user_id, amount=amount)
            except Exception as exc:
                await trans.rollback()
                raise exc

            else:
                await trans.commit()

    async def check_current_balance_for_change(self, conn, user_id: str, amount: int) -> None:
        if amount >= 0:
            return

        fetch_result = await conn.fetchrow(
            "SELECT balance FROM customer WHERE userid = :user_id"
        ).bindparams(user_id=user_id)
        if not fetch_result:
            raise AccountNoExistsError

        current_balance = fetch_result["balance"]
        to_be = current_balance + amount
        if to_be < 0:
            raise NoEnoughMoneyError

    async def exchange_balance(
        self,
        payer_user_id: str,
        payer_amount: int,
        buyer_user_id: str,
        idempotency_key: str | None,
    ) -> None:
        if not idempotency_key:
            raise NoIdempKeyError

        check_for_injections(payer_user_id)
        check_for_injections(buyer_user_id)
        async with DBConnectionContext() as conn:
            trans = conn.transaction(isolation=IsolationLevelEnum.repeatable_read)
            try:
                await trans.start()
                try:
                    current_ts = int(time.time())
                    await conn.fetch(
                        """INSERT INTO paymentKey (userId, externalKey, createdTS)
                        VALUES (:payer_user_id, :idempotency_key, :current_ts)"""
                    ).bindparams(payer_user_id=buyer_user_id, idempotency_key=idempotency_key, current_ts=current_ts)
                except UniqueViolationError as exc:
                    raise SameIdempRequestError from exc

                await self.check_current_balance_for_change(conn, payer_user_id, -payer_amount)
                await self.check_current_balance_for_change(conn, buyer_user_id, payer_amount)
                fetch_result = await conn.fetchrow(
                    "SELECT balance FROM customer WHERE userid = :buyer_user_id"
                ).bindparams(buyer_user_id=buyer_user_id)
                if not fetch_result:
                    raise AccountNoExistsError

                await conn.fetch(
                    f"""UPDATE customer SET balance = CASE userId
                          WHEN :payer_user_id THEN customer.balance - :payer_amount
                          WHEN :buyer_user_id THEN customer.balance + :payer_amount
                          END
                       WHERE userId IN('{payer_user_id}', '{buyer_user_id}')
                    """
                ).bindparams(payer_user_id=payer_user_id, payer_amount=payer_amount, buyer_user_id=buyer_user_id)

            except Exception as exc:
                await trans.rollback()
                raise exc

            else:
                await trans.commit()
