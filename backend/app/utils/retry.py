import time
import logging

def retry(
    fn,
    retries: int = 3,
    delay: float = 1.0,
    logger: logging.Logger | None = None,
    error_msg: str = "Operation failed"
):
    last_exception = None

    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exception = e
            if logger:
                logger.warning(
                    f"{error_msg} | attempt {attempt}/{retries} | error={e}"
                )
            time.sleep(delay)

    raise last_exception
