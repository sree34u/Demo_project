"""Low-level filesystem helpers shared across the framework."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union

PathLike = Union[str, Path]


def ensure_directory(path: PathLike) -> Path:
    """Create the directory (and parents) if it doesn't exist, return it."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def path_exists(path: PathLike) -> bool:
    return Path(path).exists()


def read_text(path: PathLike, encoding: str = "utf-8") -> str:
    return Path(path).read_text(encoding=encoding)


def write_text(path: PathLike, content: str, encoding: str = "utf-8") -> None:
    file_path = Path(path)
    ensure_directory(file_path.parent)
    file_path.write_text(content, encoding=encoding)


def read_json(path: PathLike, encoding: str = "utf-8") -> Any:
    return json.loads(read_text(path, encoding=encoding))


def write_json(path: PathLike, data: Any, encoding: str = "utf-8", indent: int = 2) -> None:
    write_text(path, json.dumps(data, indent=indent, ensure_ascii=False), encoding=encoding)