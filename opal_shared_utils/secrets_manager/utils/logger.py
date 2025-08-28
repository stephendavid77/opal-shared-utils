import logging

# Configure a logger for the secrets manager
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Prevent logging secrets
class SecretFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, "msg") and isinstance(record.msg, str):
            # Simple heuristic: avoid logging strings that look like secrets
            # This is NOT foolproof and should be combined with careful logging practices
            if (
                "secret" in record.msg.lower()
                or "password" in record.msg.lower()
                or "key" in record.msg.lower()
            ):
                record.msg = "[SECRET_REDACTED]"
        return True


# Add the filter to the logger
# logger.addFilter(SecretFilter()) # Uncomment in production if needed, but careful logging is better

# Example: Add a console handler if not already configured by the main app
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
