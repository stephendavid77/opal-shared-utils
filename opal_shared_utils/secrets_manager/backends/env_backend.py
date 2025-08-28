import os
from typing import Optional

from dotenv import load_dotenv

from shared.secrets_manager.utils.logger import logger


class EnvBackend:
    def __init__(self):
        # Load .env file once when the backend is initialized
        load_dotenv()
        logger.info("EnvBackend initialized: .env file loaded.")

    def get_secret(self, name: str) -> Optional[str]:
        secret = os.getenv(name)
        if secret:
            logger.debug(f"Secret '{name}' found in environment variables.")
        else:
            logger.debug(f"Secret '{name}' not found in environment variables.")
        return secret

    def get_service_account_json(self, name: str) -> Optional[str]:
        # For service account JSON, it's typically stored as a base64 encoded string
        # or directly as a multi-line environment variable.
        # This backend will return the raw string, parsing happens at a higher level.
        return self.get_secret(name)
