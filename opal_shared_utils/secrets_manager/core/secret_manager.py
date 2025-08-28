import json
import os  # Import os
from typing import Dict, List, Optional

from shared.secrets_manager.backends.cloud_backend import CloudBackend
from shared.secrets_manager.backends.env_backend import EnvBackend
from shared.secrets_manager.backends.keychain_backend import KeychainBackend
from shared.secrets_manager.utils.cache import cached_secret
from shared.secrets_manager.utils.logger import logger


class SecretManager:
    def __init__(self, project_id: Optional[str] = None):
        self.backends = [
            EnvBackend(),
            KeychainBackend(),
        ]

        # Determine environment from OPALSUITE_ENV environment variable
        # Default to 'local' if not set
        opal_suite_env = os.environ.get("OPALSUITE_ENV", "local").lower()

        if opal_suite_env == "cloud":
            self.backends.append(CloudBackend(project_id=project_id))
            logger.info("Cloud environment detected. CloudBackend enabled.")
        else:
            logger.info("Local environment detected. CloudBackend disabled.")

        logger.info(
            "SecretManager initialized with backend priority: Env -> Keychain -> Cloud (if enabled)."
        )

    @cached_secret()
    def get_secret(self, name: str) -> Optional[str]:
        for backend in self.backends:
            secret = backend.get_secret(name)
            if secret is not None:
                logger.debug(
                    f"Secret '{name}' retrieved from {backend.__class__.__name__}."
                )
                return secret
        logger.warning(f"Secret '{name}' not found in any configured backend.")
        return None

    def get_service_account_json(self, name: str) -> Optional[Dict]:
        for backend in self.backends:
            json_data = backend.get_service_account_json(name)
            if json_data is not None:
                logger.debug(
                    f"Service account JSON '{name}' retrieved from {backend.__class__.__name__}."
                )
                # Ensure it's parsed if it came as a string
                if isinstance(json_data, str):
                    try:
                        return json.loads(json_data)
                    except json.JSONDecodeError:
                        logger.error(
                            f"Failed to parse service account JSON from {backend.__class__.__name__} for '{name}'."
                        )
                        return None
                return json_data
        logger.warning(
            f"Service account JSON '{name}' not found in any configured backend."
        )
        return None


# Global instance for easy access by subprojects
_secret_manager_instance = SecretManager()


def get_secret(name: str) -> Optional[str]:
    return _secret_manager_instance.get_secret(name)


def get_service_account_json(name: str) -> Optional[Dict]:
    return _secret_manager_instance.get_service_account_json(name)
