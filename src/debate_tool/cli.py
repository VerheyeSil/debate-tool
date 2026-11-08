"""Command-line entry point: runs a debate between GroenLinks and VVD."""

from dotenv import load_dotenv

from debate_tool.agents import Moderator, PartyDebater
from debate_tool.debate_manager import DebateManager
from debate_tool.openai_client import OpenAIClient

TOPIC = "Moet Nederland een vermogensbelasting invoeren?"
PARTIES = ["GroenLinks", "VVD"]


def main():
    load_dotenv()
    client = OpenAIClient()

    moderator = Moderator("Voorzitter", client)
    debaters = [PartyDebater(party, client) for party in PARTIES]

    DebateManager(moderator, debaters).run_debate(TOPIC, num_rounds=1)


if __name__ == "__main__":
    main()
