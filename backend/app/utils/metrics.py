import time
from app.utils.logger import get_logger

def instrument_node(node_name: str):
    logger = get_logger(f"node.{node_name}")

    def decorator(func):
        def wrapper(state):
            # Extract execution_id for logging context (Task 6)
            execution_id = getattr(state, "execution_id", "unknown")
            logger.info(f"[{execution_id}] START node={node_name}")

            start = time.time()
            try:
                result = func(state)
                duration = round(time.time() - start, 3)

                logger.info(
                    f"[{execution_id}] SUCCESS node={node_name} | duration={duration}s"
                )
                return result

            except Exception as e:
                duration = round(time.time() - start, 3)
                logger.error(
                    f"[{execution_id}] FAILURE node={node_name} | duration={duration}s | error={str(e)}"
                )
                raise

        return wrapper
    return decorator
