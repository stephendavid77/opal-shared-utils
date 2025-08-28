import json
from typing import Optional

# Try to import google.cloud.secretmanager, but allow the backend to be used
# even if the library is not installed (e.g., for local development without GCP setup)
try:
    from google.api_core.exceptions import GoogleAPIError, NotFound
    from google.cloud import secretmanager

    _HAS_GCP_LIBS = True
except ImportError:
    secretmanager = None
    NotFound = type("NotFound", (Exception,), {})
    GoogleAPIError = type("GoogleAPIError", (Exception,), {})
    _HAS_GCP_LIBS = False

from shared.secrets_manager.utils.logger import logger
from shared.secrets_manager.utils.retries import retry


class CloudBackend:
    def __init__(self, project_id: Optional[str] = None):
        if not _HAS_GCP_LIBS:
            logger.warning(
                "Google Cloud Secret Manager libraries not found. CloudBackend will not function."
            )
            self.client = None
            self.project_id = None
            return

        self.client = secretmanager.SecretManagerServiceClient()
        # Attempt to get project_id from environment or client default
        if project_id:
            self.project_id = project_id
        else:
            try:
                # This might require google-auth or default credentials setup
                from google.auth import default

                _, self.project_id = default()
            except Exception as e:
                logger.warning(
                    f"Could not determine GCP project ID automatically: {e}. Please provide it explicitly."
                )
                self.project_id = None

        if self.project_id:
            logger.info(f"CloudBackend initialized for project: {self.project_id}")
        else:
            logger.error("CloudBackend initialized without a valid GCP project ID.")

    @retry(max_attempts=3, delay_seconds=2, catch_exceptions=(GoogleAPIError,))
    def _get_secret_value(self, secret_id: str) -> Optional[str]:
        if not self.client or not self.project_id:
            logger.debug(
                f"CloudBackend not configured, cannot retrieve secret '{secret_id}'."
            )
            return None

        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        try:
            response = self.client.access_secret_version(request={"name": name})
            secret_value = response.payload.data.decode("UTF-8")
            logger.debug(f"Secret '{secret_id}' found in Cloud Secret Manager.")
            return secret_value
        except NotFound:
            logger.debug(f"Secret '{secret_id}' not found in Cloud Secret Manager.")
            return None
        except GoogleAPIError as e:
            logger.error(f"Google API error retrieving secret '{secret_id}': {e}")
            raise  # Re-raise to trigger retry
        except Exception as e:
            logger.error(f"Unexpected error retrieving secret '{secret_id}': {e}")
            return None

    def get_secret(self, name: str) -> Optional[str]:
        return self._get_secret_value(name)

    def get_service_account_json(self, name: str) -> Optional[dict]:
        json_str = self._get_secret_value(name)
        if json_str:
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse service account JSON for '{name}': {e}")
                return None
        return None
