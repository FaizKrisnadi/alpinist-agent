"""Deterministic local provider for demo mode."""

from __future__ import annotations

import hashlib
import json
from importlib import resources
from pathlib import Path

from alpinist.providers import History


def _repo_fixture_path() -> Path:
    return Path(__file__).resolve().parents[2] / "examples" / "fixtures" / "demo_responses.jsonl"


class MockProvider:
    """Returns fixture-based responses without external API calls."""

    def __init__(self, fixture_path: Path | None = None) -> None:
        self.fixture_path = fixture_path
        if fixture_path is not None:
            self._responses = self._load_responses_from_path(fixture_path)
        else:
            self._responses = self._load_default_responses()

    @staticmethod
    def _normalize(prompt: str) -> str:
        return " ".join(prompt.strip().lower().split())

    @classmethod
    def _parse_jsonl(cls, source: str, jsonl_text: str) -> dict[str, str]:
        responses: dict[str, str] = {}
        lines = jsonl_text.splitlines()

        for line_number, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in fixture {source} at line {line_number}: {exc.msg}"
                ) from exc

            prompt = str(record.get("prompt", "")).strip()
            response = str(record.get("response", "")).strip()
            if prompt and response:
                responses[cls._normalize(prompt)] = response
        return responses

    def _load_responses_from_path(self, fixture_path: Path) -> dict[str, str]:
        if not fixture_path.exists():
            return {}
        text = fixture_path.read_text(encoding="utf-8")
        return self._parse_jsonl(source=str(fixture_path), jsonl_text=text)

    def _load_default_responses(self) -> dict[str, str]:
        # Primary path for installed wheels: package data bundled with the module.
        try:
            package_fixture = resources.files("alpinist").joinpath("fixtures/demo_responses.jsonl")
            if package_fixture.is_file():
                text = package_fixture.read_text(encoding="utf-8")
                return self._parse_jsonl(
                    source="alpinist/fixtures/demo_responses.jsonl",
                    jsonl_text=text,
                )
        except (FileNotFoundError, ModuleNotFoundError, OSError):
            pass

        # Fallback for source tree layouts if package resources are unavailable.
        return self._load_responses_from_path(_repo_fixture_path())

    def generate(self, prompt: str, history: History | None = None) -> str:
        _ = history  # Explicitly ignored for deterministic fixture behavior.
        normalized = self._normalize(prompt)
        if normalized in self._responses:
            return self._responses[normalized]

        condensed = " ".join(prompt.strip().split()) or "[empty prompt]"
        digest = hashlib.sha256(condensed.encode("utf-8")).hexdigest()[:10]
        return (
            f"[demo-mode:{digest}] No canned response for '{condensed[:80]}'. "
            "This deterministic fallback comes from the local mock provider."
        )
