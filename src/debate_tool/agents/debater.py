"""Debaters: a generic one with a free-text stance, and one that represents a party."""

from debate_tool.agents.base_agent import DEFAULT_MODEL, BaseAgent
from debate_tool.parties import load_party_context

# Only this many characters of the election programme go into the prompt.
PROGRAMME_EXCERPT_LENGTH = 2000

DEBATER_PROMPT = """Je bent een debater in een politiek debat.

Jouw standpunt: {stance}

Debatrichtlijnen:
- Argumenteer helder en logisch voor jouw positie
- Reageer direct op punten van tegenstanders
- Gebruik bewijs en redenering om je standpunten te onderbouwen
- Blijf bij het onderwerp
- Wees respectvol maar standvastig
- Erken valide tegenargumenten wanneer gepast, maar leg uit waarom jouw positie toch beter is
- Houd antwoorden bondig (maximaal 2-3 alinea's)

Onthoud: Je probeert te overtuigen door geredeneerde argumenten, niet door theatrale uitvoeringen.
Spreek altijd in het Nederlands.
"""

PARTY_INSTRUCTIONS = """

DEBATINSTRUCTIES:
- Argumenteer vanuit de gedocumenteerde standpunten van jouw partij
- Verwijs naar jullie verkiezingsprogramma waar relevant
- Blijf trouw aan de kernwaarden van jouw partij
- Bekritiseer standpunten van tegenstanders vanuit jouw partijperspectief
- Wees specifiek over beleidsvoorstellen
- Erken coalitierealiteit waar relevant
- Spreek altijd in het Nederlands
"""


class Debater(BaseAgent):
    """A debater who argues for a stance given as free text."""

    def __init__(self, name, stance, client, model=DEFAULT_MODEL, stream=True):
        super().__init__(name, DEBATER_PROMPT.format(stance=stance), client, model, stream)
        self.stance = stance


class PartyDebater(Debater):
    """A debater who represents a Dutch political party.

    The stance is built from the party's files in ``data/parties/<party>/``.
    """

    def __init__(self, party_name, client, model=DEFAULT_MODEL, stream=True):
        self.party_context = load_party_context(party_name)
        super().__init__(party_name, build_party_stance(party_name, self.party_context), client, model, stream)


def _excerpt(text, length=PROGRAMME_EXCERPT_LENGTH):
    """Shorten text to ``length`` characters, marking a cut with '...'."""
    return text if len(text) <= length else text[:length] + "..."


def build_party_stance(party_name, context):
    """Build the stance text for a party from its loaded context."""
    stance = f"Je vertegenwoordigt {party_name} in de Nederlandse Tweede Kamer.\n"

    if context.get("core_values"):
        stance += f"\nKERNIDENTITEIT:\n{', '.join(context['core_values'])}\n"

    stance += "\nSTANDPUNTEN VAN JOUW PARTIJ:\n"
    for topic, position in context.get("key_policies", {}).items():
        stance += f"\n{topic.upper()}: {position}"

    if context.get("standpunten"):
        stance += f"\n\n{context['standpunten']}"

    if context.get("verkiezingsprogramma"):
        stance += f"\n\nVERKIEZINGSPROGRAMMA (Belangrijke fragmenten):\n{_excerpt(context['verkiezingsprogramma'])}"

    return stance + PARTY_INSTRUCTIONS
