from debate_tool.agents import BaseAgent, Moderator


def test_model_is_passed_to_client(client):
    Moderator("Voorzitter", client, model="other-model").close_debate()
    assert client.calls[0]["model"] == "other-model"


def test_history_includes_what_agent_heard_and_said(client):
    agent = BaseAgent("A", "systeem", client)
    agent.hear("B", "hallo")
    agent.respond()
    agent.respond("nog iets")
    assert client.calls[1]["messages"] == [
        {"role": "system", "content": "systeem"},
        {"role": "user", "content": "B: hallo"},
        {"role": "assistant", "content": "<antwoord 0>"},
        {"role": "user", "content": "nog iets"},
    ]


def test_non_streaming_response_is_still_printed(client, capsys):
    BaseAgent("A", "systeem", client, stream=False).respond("vraag")
    assert capsys.readouterr().out == "<antwoord 0>\n"
