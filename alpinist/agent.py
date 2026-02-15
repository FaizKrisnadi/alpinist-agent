"""Agent orchestration for demo and real providers."""

from __future__ import annotations

from typing import cast

from alpinist.config import Config
from alpinist.providers import History, Provider
from alpinist.providers.gemini_provider import GeminiProvider
from alpinist.providers.mock_provider import MockProvider


class Agent:
    """Simple wrapper that selects the active provider based on configuration."""

    def __init__(self, config: Config | None = None, provider: Provider | None = None) -> None:
        self.config = config or Config.from_env()
        self.config.validate_for_agent()
        self.provider = provider or self._build_provider()
        self.history: History = []

    def _build_provider(self) -> Provider:
        if self.config.demo_mode:
            return MockProvider()
        return cast(
            Provider,
            GeminiProvider(
                api_key=self.config.gemini_api_key or "",
                model=self.config.gemini_model,
            ),
        )

    def run_once(self, prompt: str, history: History | None = None) -> str:
        cleaned_prompt = prompt.strip()
        if not cleaned_prompt:
            return "Please provide a non-empty prompt."

        active_history = self.history if history is None else history
        response = self.provider.generate(cleaned_prompt, history=active_history)
        active_history.append({"role": "user", "content": cleaned_prompt})
        active_history.append({"role": "assistant", "content": response})
        return response

    def reset_history(self, history: History | None = None) -> None:
        target = self.history if history is None else history
        target.clear()

    def chat_loop(self) -> None:
        print("Interactive chat started. Type /q to exit.")
        while True:
            try:
                prompt = input("you> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if prompt in {"/q", "/quit", "quit", "exit"}:
                break
            if not prompt:
                continue

            try:
                response = self.run_once(prompt)
            except Exception as exc:  # noqa: BLE001 - interactive UX should continue on failures
                print(f"error> {exc}")
                continue

            print(f"bot> {response}")
