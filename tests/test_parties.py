import json

import pytest

from debate_tool import parties
from debate_tool.agents.debater import PartyDebater, build_party_stance


def test_loads_bundled_parties_from_any_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    context = parties.load_party_context("VVD")
    assert context["core_values"][0] == "economische vrijheid"
    assert "belastingen" in context["key_policies"]


def test_party_name_lookup_is_case_insensitive():
    assert parties.party_dir("GroenLinks") == parties.party_dir("groenlinks")
    assert parties.party_dir("Groen Links").name == "groen_links"


def test_unknown_party_raises():
    with pytest.raises(FileNotFoundError, match="Known parties: groenlinks, vvd"):
        parties.load_party_context("PvdA")


@pytest.fixture
def fake_party(tmp_path, monkeypatch):
    monkeypatch.setattr(parties, "PARTIES_DIR", tmp_path)
    folder = tmp_path / "testpartij"
    folder.mkdir()
    (folder / "context.json").write_text(json.dumps({"core_values": ["a", "b"], "key_policies": {"zorg": "beter"}}))
    return folder


def test_stance_contains_values_and_policies(fake_party):
    stance = build_party_stance("Testpartij", parties.load_party_context("Testpartij"))
    assert "KERNIDENTITEIT:\na, b" in stance
    assert "ZORG: beter" in stance
    # Empty/missing programme must not leave an empty section behind.
    assert "VERKIEZINGSPROGRAMMA" not in stance


def test_programme_excerpt_is_truncated_only_when_long(fake_party):
    (fake_party / "verkiezingsprogramma.txt").write_text("kort programma")
    stance = build_party_stance("Testpartij", parties.load_party_context("Testpartij"))
    assert "kort programma\n" in stance and "kort programma..." not in stance

    (fake_party / "verkiezingsprogramma.txt").write_text("x" * 3000)
    stance = build_party_stance("Testpartij", parties.load_party_context("Testpartij"))
    assert "x" * 2000 + "..." in stance and "x" * 2001 not in stance


def test_standpunten_are_included(fake_party):
    (fake_party / "standpunten.txt").write_text("Wij zijn voor de fiets.")
    assert "Wij zijn voor de fiets." in PartyDebater("Testpartij", client=None).system_prompt
