from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from ..essentials import is_docker

BASE_DIR = Path(__file__).resolve().parent.parent
if not is_docker():
    load_dotenv(Path(BASE_DIR.parent, ".env"))


class DBSettings(BaseSettings):
    db_name: str
    db_host: str
    db_port: str
    db_password: str
    db_user: str


class TaskSettings(BaseSettings):
    clear_payment_key_period: int = 60 * 5  # 5 min default


class Settings(BaseSettings):
    db: DBSettings = DBSettings()  # type: ignore
    task: TaskSettings = TaskSettings()  # type: ignore
    app_name: str = "Payment Service"
    debug: bool = True
    host: str
    log_lvl: str = "INFO"
    port: int
    version: str = "0.0.1"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
