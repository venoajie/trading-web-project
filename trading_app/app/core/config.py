
# trading-app-backend/app/core/config.py
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Load non-secret settings from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # --- Non-Secret Database Configuration ---
    DATABASE_USER: str = "trading_web_project_user"
    DATABASE_HOST: str = "pgbouncer"
    DATABASE_PORT: int = 6432
    DATABASE_DB: str = "central_db" # The database name

    # --- File-based Secret Configuration ---
    # These env vars will contain the path to the secret file inside the container
    DATABASE_PASSWORD_FILE: Path = Path("/run/secrets/db_password")
    LIBRARIAN_API_KEY_FILE: Path = Path("/run/secrets/librarian_api_key")

    # --- Other Application Settings ---
    APP_NAME: str = "Trading App"
    SECRET_KEY: str # For JWT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    LIBRARIAN_API_URL: str = "http://librarian:8000/api/v1/chat"

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        """
        Assembles the full database connection string, reading the password
        from the secret file.
        """
        try:
            password = self.DATABASE_PASSWORD_FILE.read_text().strip()
        except FileNotFoundError:
            logger.critical(f"Database password file not found at: {self.DATABASE_PASSWORD_FILE}")
            raise

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DATABASE_USER,
            password=password,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            path=self.DATABASE_DB,
        )

    @computed_field
    @property
    def LIBRARIAN_API_KEY(self) -> str:
        """
        Reads the Librarian API key from its secret file.
        """
        try:
            return self.LIBRARIAN_API_KEY_FILE.read_text().strip()
        except FileNotFoundError:
            logger.critical(f"Librarian API key file not found at: {self.LIBRARIAN_API_KEY_FILE}")
            raise

settings = Settings()
