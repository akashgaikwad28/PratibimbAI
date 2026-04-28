import time
from typing import Dict, Any, Optional
from app.utils.logger import get_logger

logger = get_logger("utils.tracing")

class Trace:
    """
    A simple tracing container for node execution performance and state.
    Task 7: Observability
    """
    def __init__(self, execution_id: str, node_name: str):
        self.execution_id = execution_id
        self.node_name = node_name
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.status = "started"
        self.metadata: Dict[str, Any] = {}
        self.error: Optional[str] = None

    def complete(self, status: str = "success", metadata: Dict[str, Any] = None):
        self.end_time = time.time()
        self.status = status
        if metadata:
            self.metadata.update(metadata)
        
        duration = round(self.end_time - self.start_time, 3)
        logger.info(
            f"TRACE | {self.execution_id} | {self.node_name} | "
            f"status={status} | duration={duration}s | meta={self.metadata}"
        )

    def fail(self, error: str, metadata: Dict[str, Any] = None):
        self.end_time = time.time()
        self.status = "failed"
        self.error = error
        if metadata:
            self.metadata.update(metadata)
            
        duration = round(self.end_time - self.start_time, 3)
        logger.error(
            f"TRACE | {self.execution_id} | {self.node_name} | "
            f"status=failed | duration={duration}s | error={error}"
        )
