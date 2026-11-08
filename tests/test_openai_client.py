from types import SimpleNamespace as NS

from debate_tool.openai_client import OpenAIClient


class FakeCompletions:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        if kwargs.get("stream"):
            return iter([
                NS(choices=[NS(delta=NS(content="Goed"))]),
                NS(choices=[NS(delta=NS(content=None))]),
                NS(choices=[]),  # e.g. a usage-only chunk
                NS(choices=[NS(delta=NS(content="emiddag"))]),
            ])
        return NS(choices=[NS(message=NS(content="Hallo"))])


def make_client():
    client = OpenAIClient(api_key="test")
    client.client = NS(chat=NS(completions=FakeCompletions()))
    return client


def test_plain_completion():
    client = make_client()
    assert client.get_completion([{"role": "user", "content": "hi"}], model="m") == "Hallo"
    assert client.client.chat.completions.kwargs["model"] == "m"


def test_streamed_completion_prints_and_returns_text(capsys):
    assert make_client().get_completion([], stream=True) == "Goedemiddag"
    assert capsys.readouterr().out == "Goedemiddag\n"
