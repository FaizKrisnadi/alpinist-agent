"""Provider interfaces and implementations."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

History = list[dict[str, str]]


@runtime_checkable
class Provider(Protocol):
    def generate(self, prompt: str, history: History | None = None) -> str:
        """Generate a response from a prompt and optional prior history."""
