from typing import Optional

import keyring

from shared.secrets_manager.utils.logger import logger


class KeychainBackend:
    def __init__(self):
        logger.info("KeychainBackend initialized.")

    def get_secret(self, name: str) -> Optional[str]:
        try:
            # Service name can be a constant or derived from the app name
            secret = keyring.get_password("OpalSuite", name)
            if secret:
                logger.debug(f"Secret '{name}' found in keychain.")
            else:
                logger.debug(f"Secret '{name}' not found in keychain.")
            return secret
        except Exception as e:
            logger.warning(f"Error accessing keychain for '{name}': {e}")
            return None

    def get_service_account_json(self, name: str) -> Optional[str]:
        return self.get_secret(name)
