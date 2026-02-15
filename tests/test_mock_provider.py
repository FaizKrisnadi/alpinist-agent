from alpinist.providers.mock_provider import MockProvider


def test_mock_provider_returns_packaged_fixture_response() -> None:
    provider = MockProvider()

    response = provider.generate("hello alpinist")

    assert (
        response
        == (
            "Hello from Alpinist demo mode. This response is loaded from local fixtures "
            "and does not call external APIs."
        )
    )
