"""Loads environment variables and optional per-environment JSON config
overrides used by config.settings."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from utils.file_utils import path_exists, read_json

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_ENV_FILE = _PROJECT_ROOT / ".env"
_DEFAULT_CONFIG_DIR = _PROJECT_ROOT / "config" / "environments"


class ConfigLoader:
    """Resolves configuration from a .env file and optional JSON overrides."""

    def __init__(self, env_file: Optional[Path] = None, config_dir: Optional[Path] = None) -> None:
        self._env_file = env_file or _DEFAULT_ENV_FILE
        self._config_dir = config_dir or _DEFAULT_CONFIG_DIR
        self._env_loaded = False

    def load_env_file(self) -> None:
        """Load variables from the .env file into os.environ, if present."""
        if self._env_loaded:
            return
        if path_exists(self._env_file):
            load_dotenv(dotenv_path=self._env_file, override=False)
        self._env_loaded = True

    def load_json_config(self, filename: str) -> Dict[str, Any]:
        """Load a JSON override file from the config directory.
        Returns an empty dict if the file does not exist."""
        config_path = self._config_dir / filename
        if not path_exists(config_path):
            return {}
        return read_json(config_path)

    def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        self.load_env_file()
        return os.getenv(key, default)


@lru_cache(maxsize=1)
def get_config_loader() -> ConfigLoader:
    """Return the cached, process-wide ConfigLoader instance."""
    return ConfigLoader()