import time
from functools import wraps
from typing import Any, Callable

from shared.secrets_manager.utils.logger import logger


def retry(
    max_attempts: int = 3,
    delay_seconds: int = 1,
    catch_exceptions: tuple = (Exception,),
):  # noqa: E501
    """A decorator to retry a function call on failure."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as e:
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay_seconds)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}."
                        )
                        raise

        return wrapper

    return decorator
