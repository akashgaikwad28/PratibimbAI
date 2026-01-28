import time
from app.utils.logger import get_logger

def instrument_node(node_name: str):
    logger = get_logger(f"node.{node_name}")

    def decorator(func):
        def wrapper(state):
            logger.info("START")

            start = time.time()
            try:
                result = func(state)
                duration = round(time.time() - start, 3)

                logger.info(
                    f"SUCCESS | duration={duration}s"
                )
                return result

            except Exception as e:
                duration = round(time.time() - start, 3)
                logger.error(
                    f"FAILURE | duration={duration}s | error={str(e)}"
                )
                raise

        return wrapper
    return decorator
