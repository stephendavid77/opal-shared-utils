# OpalSuite Centralized Secret Management Module

## Overview

The `shared/secrets_manager/` module provides a robust and resilient solution for centralized secret management across the `OpalSuite` monorepo. Its primary goal is to abstract the source of sensitive information (API keys, credentials, service account JSONs) from subprojects, allowing them to retrieve secrets through simple helper methods without knowing where the secrets are actually stored. This enhances security, simplifies development, and ensures consistent secret handling practices.

## Architecture

### 1. Core Logic (`core/secret_manager.py`)

*   **Orchestration:** The `secret_manager.py` file contains the main logic that orchestrates the secret retrieval process. It defines the priority chain for fetching secrets from various backends.
*   **Public API:** Exposes simple helper methods (`get_secret(name: str)`, `get_service_account_json(name: str)`) that subprojects call to retrieve secrets.
*   **Caching:** Utilizes an optional caching mechanism (`utils/cache.py`) to reduce repeated API calls to cloud secret managers and improve latency.

### 2. Secret Backends (`backends/`)

This directory houses modular backends, each responsible for retrieving secrets from a specific source. The system is designed to gracefully fall back to the next priority if a secret is not found in a higher-priority backend.

*   **`env_backend.py`:** Retrieves secrets from local `.env` files (parsed using `python-dotenv`) and environment variables.
*   **`keychain_backend.py`:** Retrieves secrets from the local OS secure keychain (e.g., macOS Keychain, Windows Credential Manager, Linux Secret Service) using the `keyring` library.
*   **`cloud_backend.py`:** Retrieves secrets from Google Cloud Secret Manager. It includes retry logic for resilient cloud access and handles Google service account JSON retrieval transparently.

### 3. Utility Functions (`utils/`)

*   **`logger.py`:** Provides a dedicated logger for the secrets manager, configured to never log sensitive information.
*   **`retries.py`:** Implements a decorator for retry logic, primarily used for resilient calls to cloud services.
*   **`cache.py`:** Provides a simple LRU cache decorator for caching retrieved secrets, reducing API calls and latency.

## How it Fits into OpalSuite

*   **Security:** Centralizes secret management, reducing the risk of hardcoded credentials and ensuring consistent security practices across the monorepo.
*   **Abstraction:** Subprojects are decoupled from the underlying secret storage mechanisms, simplifying their code and making them more portable.
*   **Resilience:** The priority-based retrieval and retry logic ensure that applications can gracefully handle missing secrets or temporary network issues.
*   **Local Development & Cloud Deployment:** Seamlessly supports both local development (using `.env` or keychain) and cloud deployment (using Secret Manager).
*   **Extensibility:** The modular backend design allows for easy addition of new secret sources (e.g., AWS Secrets Manager, HashiCorp Vault) in the future without impacting subprojects.

## Getting Started (Development)

1.  **Install Root Dependencies:** Ensure you have installed the root-level Python dependencies (`pip install -r requirements.txt` from the `OpalSuite` root), which include `python-dotenv`, `keyring`, and `google-cloud-secret-manager`.
2.  **Test Local Retrieval:**
    *   Create a `.env` file in the `OpalSuite` root (e.g., `OpalSuite/.env`) with a test secret: `MY_TEST_SECRET=my_value`.
    *   In a Python script or console at the `OpalSuite` root, test retrieval:
        ```python
        from OpalSuite.shared.secrets_manager import get_secret
        secret_value = get_secret("MY_TEST_SECRET")
        print(f"Retrieved secret: {secret_value}")
        ```
3.  **Integrate into Subprojects:** Modify your subprojects to use `from OpalSuite.shared.secrets_manager import get_secret, get_service_account_json` to retrieve their necessary secrets.

## Future Enhancements

*   **Secret Rotation:** Implement mechanisms for automated secret rotation.
*   **Audit Logging:** Integrate with centralized audit logging for secret access.
*   **More Backend Adapters:** Add support for other secret management systems (e.g., AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).
*   **Dynamic Secret Generation:** Explore integration with systems that can dynamically generate temporary credentials.
