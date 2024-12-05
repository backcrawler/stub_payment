import asyncpg

from .configs.config import get_settings


class DBConnectionContext:

    def __init__(self):
        self.conn: asyncpg.connection.Connection | None = None
        self._settings = get_settings()

    async def __aenter__(self) -> asyncpg.connection.Connection:
        self.conn = await asyncpg.connect(
            user=self._settings.db.db_user, password=self._settings.db.db_password,
            database=self._settings.db.db_name, host=self._settings.db.db_host, port=self._settings.db.db_port
        )
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.conn.close()


async def get_db_connection() -> asyncpg.connection.Connection:
    settings = get_settings()
    conn = await asyncpg.connect(user=settings.db.db_user, password=settings.db.db_password,
                                 database=settings.db.db_name, host=settings.db.db_host, port=settings.db.db_port)
    return conn
