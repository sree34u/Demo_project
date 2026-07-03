"""Centralized, typed application settings loaded from environment variables
and optional per-environment JSON overrides."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from utils.config_loader import get_config_loader


@dataclass(frozen=True)
class Settings:
    """Immutable application configuration."""

    environment: str
    base_url: str
    api_base_url: str
    browser: str
    headless: bool
    default_timeout_ms: int
    api_timeout_seconds: int
    log_dir: str
    log_level: str
    screenshot_dir: str


def _to_bool(value: str, default: bool) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _to_int(value: str, default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _build_settings() -> Settings:
    loader = get_config_loader()
    loader.load_env_file()

    environment = os.getenv("ENV", "dev").strip().lower()
    overrides = loader.load_json_config(f"{environment}.json")

    def resolve(key: str, env_var: str, default: str) -> str:
        return str(overrides.get(key, os.getenv(env_var, default)))

    return Settings(
        environment=environment,
        base_url=resolve("base_url", "BASE_URL", "http://localhost"),
        api_base_url=resolve("api_base_url", "API_BASE_URL", "http://localhost/api"),
        browser=resolve("browser", "BROWSER", "chromium"),
        headless=_to_bool(str(overrides.get("headless", os.getenv("HEADLESS", "true"))), True),
        default_timeout_ms=_to_int(
            str(overrides.get("default_timeout_ms", os.getenv("DEFAULT_TIMEOUT_MS", "30000"))), 30000
        ),
        api_timeout_seconds=_to_int(
            str(overrides.get("api_timeout_seconds", os.getenv("API_TIMEOUT_SECONDS", "30"))), 30
        ),
        log_dir=resolve("log_dir", "LOG_DIR", "logs"),
        log_level=resolve("log_level", "LOG_LEVEL", "INFO"),
        screenshot_dir=resolve("screenshot_dir", "SCREENSHOT_DIR", "screenshots"),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached, process-wide Settings instance."""
    return _build_settings()