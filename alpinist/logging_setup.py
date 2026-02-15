"""Logging setup helpers."""

from __future__ import annotations

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure readable process-wide logging."""
    resolved_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=resolved_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )
