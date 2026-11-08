from debate_tool.agents import Moderator, PartyDebater
from debate_tool.debate_manager import DebateManager

TOPIC = "Moet Nederland een vermogensbelasting invoeren?"


def run(client, num_rounds=1):
    moderator = Moderator("Voorzitter", client)
    debaters = [PartyDebater("GroenLinks", client), PartyDebater("VVD", client)]
    return DebateManager(moderator, debaters).run_debate(TOPIC, num_rounds=num_rounds)


def test_speaking_order_matches_original(client):
    # Same order as recorded from the original code before the refactor.
    transcript = run(client)
    assert [e["speaker"] for e in transcript] == [
        "Voorzitter", "Voorzitter", "GroenLinks", "Voorzitter", "VVD", "Voorzitter",
    ]
    assert [e["message"] for e in transcript] == [f"<antwoord {i}>" for i in range(6)]


def test_rounds_repeat_the_floor_for_every_debater(client):
    assert len(run(client, num_rounds=3)) == 1 + 3 * 4 + 1


def test_moderator_prompts_are_unchanged(client):
    run(client)
    prompts = [c["messages"][-1]["content"] for c in client.calls if c["messages"][0]["content"].startswith("Je bent een debatvoorzitter")]
    assert prompts == [
        f"Introduceer een debat over '{TOPIC}'. De debaters zijn: GroenLinks, VVD. Noem ALLEEN deze debaters, geen anderen.",
        "Vraag GroenLinks (en ALLEEN GroenLinks) om hun positie te geven over dit onderwerp.",
        "Vraag VVD (en ALLEEN VVD) om hun positie te geven over dit onderwerp.",
        "Geef een korte samenvatting van de belangrijkste meningsverschillen in dit debat.",
    ]


def test_debaters_hear_each_other_and_moderator_hears_everyone(client):
    run(client)
    vvd_call = client.calls[4]["messages"]
    assert {"role": "user", "content": "GroenLinks: <antwoord 2>"} in vvd_call
    assert vvd_call[-1] == {"role": "user", "content": "Voorzitter: <antwoord 3>"}

    closing_call = client.calls[5]["messages"]
    assert {"role": "user", "content": "GroenLinks: <antwoord 2>"} in closing_call
    assert {"role": "user", "content": "VVD: <antwoord 4>"} in closing_call


def test_output_is_printed(client, capsys):
    run(client)
    out = capsys.readouterr().out
    assert "DEBAT: " + TOPIC in out and "RONDE 1" in out
    assert "\033[1mVVD:\033[0m <antwoord 4>" in out
