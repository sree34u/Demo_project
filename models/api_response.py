"""Typed representation of an HTTP response returned by BaseApiClient."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class ApiResponse:
    """Immutable wrapper around a completed HTTP response."""

    status_code: int
    headers: Dict[str, str] = field(default_factory=dict)
    body: Any = None
    url: str = ""
    elapsed_ms: float = 0.0

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300