from .base_agent import BaseAgent
import json
import os

class Debater(BaseAgent):
    def __init__(self, name, stance, client, model="gpt-4o-mini", stream=True):
        system_prompt = f"""Je bent een debater in een politiek debat.

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
        super().__init__(name, system_prompt, client, stream)
        self.stance = stance
        self.model = model
    
    def give_opening_statement(self, topic):
        """Geef openingsstatement over het onderwerp"""
        prompt = f"Geef je openingspositie over: {topic}"
        return self.respond(prompt)
    
    def rebut(self, opponent_argument):
        """Reageer op een argument van de tegenstander"""
        prompt = f"Reageer op dit tegenargument: {opponent_argument}"
        return self.respond(prompt)
    
    def give_closing_statement(self):
        """Geef slotstatement"""
        prompt = "Geef een kort slotwoord waarin je samenvat waarom jouw positie juist is."
        return self.respond(prompt)


class PartyDebater(Debater):
    """Debater die een specifieke Nederlandse politieke partij vertegenwoordigt"""
    
    def __init__(self, party_name, client, model="gpt-4o-mini", stream=True):
        # Laad partijcontext
        party_context = self._load_party_context(party_name)
        
        # Creëer partij-specifiek standpunt
        stance = self._create_party_stance(party_name, party_context)
        
        super().__init__(party_name, stance, client, model, stream)
        self.party_context = party_context
    
    def _load_party_context(self, party_name):
        """Laad partijdocumenten en context"""
        party_dir = f"data/parties/{party_name.lower().replace(' ', '_')}"
        
        context = {
            "party_name": party_name,
            "policies": {}
        }
        
        # Laad context.json indien aanwezig
        context_file = os.path.join(party_dir, "context.json")
        if os.path.exists(context_file):
            with open(context_file, 'r', encoding='utf-8') as f:
                context.update(json.load(f))
        
        # Laad verkiezingsprogramma
        program_file = os.path.join(party_dir, "verkiezingsprogramma.txt")
        if os.path.exists(program_file):
            with open(program_file, 'r', encoding='utf-8') as f:
                context["verkiezingsprogramma"] = f.read()
        
        # Laad standpunten
        standpunten_file = os.path.join(party_dir, "standpunten.txt")
        if os.path.exists(standpunten_file):
            with open(standpunten_file, 'r', encoding='utf-8') as f:
                context["standpunten"] = f.read()
        
        return context
    
    def _create_party_stance(self, party_name, context):
        """Creëer een uitgebreide positie gebaseerd op partijcontext"""
        stance = f"""Je vertegenwoordigt {party_name} in de Nederlandse Tweede Kamer.

KERNIDENTITEIT:
{', '.join(context.get('core_values', ['Progressieve waarden']))}

STANDPUNTEN VAN JOUW PARTIJ:
"""
        
        # Voeg kernbeleid toe indien beschikbaar
        if "key_policies" in context:
            for topic, position in context["key_policies"].items():
                stance += f"\n{topic.upper()}: {position}"
        
        # Voeg relevante fragmenten uit verkiezingsprogramma toe
        if "verkiezingsprogramma" in context:
            stance += f"\n\nVERKIEZINGSPROGRAMMA (Belangrijke fragmenten):\n{context['verkiezingsprogramma'][:2000]}..."
        
        stance += """

DEBATINSTRUCTIES:
- Argumenteer vanuit de gedocumenteerde standpunten van jouw partij
- Verwijs naar jullie verkiezingsprogramma waar relevant
- Blijf trouw aan de kernwaarden van jouw partij
- Bekritiseer standpunten van tegenstanders vanuit jouw partijperspectief
- Wees specifiek over beleidsvoorstellen
- Erken coalitierealiteit waar relevant
- Spreek altijd in het Nederlands
"""
        
        return stance