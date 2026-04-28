import time
import functools
from app.utils.logger import get_logger

logger = get_logger("graph.wrappers.retry")

def retry_node(max_retries: int = 2, delay: float = 1.0):
    """
    A decorator to add retry logic to LangGraph nodes.
    Useful for handling transient LLM rate limits or network glitches.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(state):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(state)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = delay * (2 ** attempt) # Exponential backoff
                        logger.warning(
                            f"Node {func.__name__} failed (attempt {attempt+1}/{max_retries+1}). "
                            f"Retrying in {wait_time}s... Error: {e}"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Node {func.__name__} exhausted all {max_retries+1} attempts. Final error: {e}")
            
            # Record error in state if possible
            if hasattr(state, "errors"):
                state.errors.append(f"Node {func.__name__} failed after retries: {str(last_exception)}")
            
            raise last_exception
        return wrapper
    return decorator
