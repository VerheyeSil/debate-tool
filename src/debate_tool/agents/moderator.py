"""The debate chair (voorzitter) who leads the debate."""

from debate_tool.agents.base_agent import DEFAULT_MODEL, BaseAgent

MODERATOR_PROMPT = """Je bent een debatvoorzitter voor een politiek debat in de Tweede Kamer.

Je rol is om:
- Het debatonderwerp duidelijk te introduceren
- Gerichte vragen te stellen aan elke debater
- Het debat gefocust en on-topic te houden
- Specifieke debaters op te roepen om te reageren op elkaars argumenten
- Gelijke spreektijd te waarborgen
- Belangrijke meningsverschillen samen te vatten

Wees professioneel, neutraal en bondig. Gedraag je als een echte Tweede Kamer voorzitter.
Spreek altijd in het Nederlands.
"""


class Moderator(BaseAgent):
    """Introduces the topic, gives each debater the floor and closes the debate."""

    def __init__(self, name, client, model=DEFAULT_MODEL):
        super().__init__(name, MODERATOR_PROMPT, client, model)

    def introduce_debate(self, topic, debater_names):
        """Open the debate and introduce only the given debaters."""
        names = ", ".join(debater_names)
        return self.respond(
            f"Introduceer een debat over '{topic}'. De debaters zijn: {names}. "
            f"Noem ALLEEN deze debaters, geen anderen."
        )

    def give_floor(self, debater_name):
        """Ask one debater for their position on the topic."""
        return self.respond(
            f"Vraag {debater_name} (en ALLEEN {debater_name}) om hun positie te geven over dit onderwerp."
        )

    def close_debate(self):
        """Summarise the main disagreements of the debate."""
        return self.respond(
            "Geef een korte samenvatting van de belangrijkste meningsverschillen in dit debat."
        )
