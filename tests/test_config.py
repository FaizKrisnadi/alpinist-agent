from alpinist.config import Config


def test_default_demo_mode_without_keys(monkeypatch) -> None:
    monkeypatch.delenv("DEMO_MODE", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    config = Config.from_env()

    assert config.demo_mode is True
    assert config.gemini_api_key is None
    assert config.telegram_bot_token is None
    assert config.gemini_model == "gemini-2.5-flash"
    config.validate_for_agent()
