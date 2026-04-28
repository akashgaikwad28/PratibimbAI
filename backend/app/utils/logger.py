import logging
from logging.handlers import RotatingFileHandler
from contextvars import ContextVar
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "pratibimbai.log")

_execution_id_var: ContextVar[str] = ContextVar("execution_id", default="-")


def set_execution_id(eid: str):
    _execution_id_var.set(eid)


class _ExecutionIdFilter(logging.Filter):
    def filter(self, record):
        record.execution_id = _execution_id_var.get()
        return True


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | [%(execution_id)s] | %(name)s | %(message)s")
    f = _ExecutionIdFilter()

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    console.addFilter(f)

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10_000_000, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(fmt)
    file_handler.addFilter(f)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger
