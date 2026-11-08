from debate_tool import cli


def test_main_runs_full_debate(client, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # must not depend on the working directory
    monkeypatch.setattr(cli, "OpenAIClient", lambda: client)
    cli.main()
    assert len(client.calls) == 6
