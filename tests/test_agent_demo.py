from alpinist.agent import Agent
from alpinist.config import Config


def test_agent_run_once_uses_demo_fixture() -> None:
    config = Config(demo_mode=True)
    agent = Agent(config=config)

    response = agent.run_once("what is demo mode?")

    assert (
        response
        == (
            "Demo mode is deterministic: prompt/response fixtures are local, and unknown "
            "prompts get a stable hash-based fallback."
        )
    )
