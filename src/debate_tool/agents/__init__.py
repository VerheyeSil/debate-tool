"""LLM agents that take part in a debate."""

from debate_tool.agents.base_agent import BaseAgent
from debate_tool.agents.debater import Debater, PartyDebater
from debate_tool.agents.moderator import Moderator

__all__ = ["BaseAgent", "Debater", "PartyDebater", "Moderator"]
