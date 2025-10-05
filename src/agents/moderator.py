from .base_agent import BaseAgent

class Moderator(BaseAgent):
    def __init__(self, name, client, model="gpt-4o-mini"):
        system_prompt = """Je bent een debatvoorzitter voor een politiek debat in de Tweede Kamer.

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
        super().__init__(name, system_prompt, client)
        self.model = model
    
    def introduce_debate(self, topic):
        """Generate opening statement for the debate"""
        prompt = f"Introduceer een debat over het volgende onderwerp: {topic}"
        return self.respond(prompt)
    
    def ask_opening_position(self, debater_name, topic):
        """Ask a debater for their opening position"""
        prompt = f"Vraag {debater_name} om hun standpunt te geven over: {topic}"
        return self.respond(prompt)
    
    def ask_rebuttal(self, debater_name, previous_point):
        """Ask a debater to respond to a previous point"""
        prompt = f"Vraag {debater_name} om te reageren op dit argument: {previous_point}"
        return self.respond(prompt)
    
    def ask_follow_up(self, debater_name, aspect):
        """Ask a follow-up question on a specific aspect"""
        prompt = f"Stel {debater_name} een vervolgvraag over: {aspect}"
        return self.respond(prompt)
    
    def close_debate(self):
        """Generate closing statement"""
        prompt = "Geef een korte samenvatting van de belangrijkste meningsverschillen in dit debat."
        return self.respond(prompt)