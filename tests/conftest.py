import pytest


class FakeClient:
    """Stands in for OpenAIClient: records every request and returns numbered answers."""

    def __init__(self):
        self.calls = []

    def get_completion(self, messages, model="gpt-4o-mini", temperature=0.7, stream=False):
        answer = f"<antwoord {len(self.calls)}>"
        self.calls.append({"messages": [dict(m) for m in messages], "model": model, "stream": stream})
        if stream:
            print(answer)
        return answer


@pytest.fixture
def client():
    return FakeClient()


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda seconds: None)
