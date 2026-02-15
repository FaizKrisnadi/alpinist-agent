"""Google Gemini provider implementation."""

from __future__ import annotations

from google import genai
from google.genai import types

from alpinist.providers import History


class ProviderError(RuntimeError):
    """Raised when a provider call fails."""


class GeminiProvider:
    """Text generation provider backed by the official Google GenAI SDK."""

    def __init__(self, api_key: str, model: str, timeout_seconds: int = 20) -> None:
        if not api_key:
            raise ValueError("GeminiProvider requires a non-empty api_key.")
        self._client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=timeout_seconds),
        )
        self._model = model
        self._timeout_seconds = timeout_seconds

    @staticmethod
    def _render_prompt(prompt: str, history: History | None = None) -> str:
        if not history:
            return prompt

        lines: list[str] = []
        for item in history:
            role = item.get("role", "user")
            content = item.get("content", "").strip()
            if content:
                lines.append(f"{role}: {content}")
        lines.append(f"user: {prompt}")
        return "\n".join(lines)

    @staticmethod
    def _extract_text(response: object) -> str | None:
        try:
            text = getattr(response, "text", None)
        except Exception:  # noqa: BLE001 - defensive fallback if SDK text accessor fails
            text = None

        if isinstance(text, str) and text.strip():
            return text.strip()

        candidates = getattr(response, "candidates", None)
        if not candidates:
            return None
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None)
            if not parts:
                continue
            for part in parts:
                part_text = getattr(part, "text", None)
                if isinstance(part_text, str) and part_text.strip():
                    return part_text.strip()
        return None

    def generate(self, prompt: str, history: History | None = None) -> str:
        request_text = self._render_prompt(prompt, history=history)

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=request_text,
                config=types.GenerateContentConfig(temperature=0.2),
            )
        except Exception as exc:  # noqa: BLE001 - provider should gracefully wrap SDK failures
            message = str(exc).lower()
            if "timeout" in message:
                raise ProviderError(
                    f"Gemini request timed out after {self._timeout_seconds} seconds."
                ) from exc
            raise ProviderError(
                "Gemini request failed. Verify GEMINI_API_KEY, GEMINI_MODEL, and network access."
            ) from exc

        text = self._extract_text(response)
        if text:
            return text
        return "Gemini returned an empty response."
