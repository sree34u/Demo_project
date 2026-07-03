"""Application-wide logger factory with console and rotating file handlers."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils.file_utils import ensure_directory

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_MAX_BYTES = 5 * 1024 * 1024
_BACKUP_COUNT = 5


def _build_console_handler(level: int) -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
    return handler


def _build_file_handler(log_dir: str, level: int) -> logging.Handler:
    directory = ensure_directory(Path(log_dir))
    handler = RotatingFileHandler(
        filename=str(directory / "automation.log"),
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
    return handler


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger. Settings are imported lazily to avoid
    a circular import between config.settings and utils.logger."""
    from config.settings import get_settings

    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(_build_console_handler(level))
        logger.addHandler(_build_file_handler(settings.log_dir, level))

    return logger