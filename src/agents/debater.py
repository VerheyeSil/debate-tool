from .base_agent import BaseAgent

class Debater(BaseAgent):
    def __init__(self, name, stance, client, model="gpt-4o-mini"):
        """
        Args:
            name: Name of the debater (e.g., "Pro", "Con", or later "VVD", "PvdA")
            stance: The position this debater should take
            client: OpenAI client instance
            model: Which model to use
        """
        system_prompt = f"""You are a debater in a political debate.

        Your stance: {stance}

        Debate guidelines:
        - Argue clearly and logically for your position
        - Respond directly to points made by opponents
        - Use evidence and reasoning to support your claims
        - Stay on topic
        - Be respectful but firm
        - Acknowledge valid opposing points when appropriate, but explain why your position is still better
        - Keep responses concise (2-3 paragraphs max)

        Remember: You're trying to persuade through reasoned argument, not theatrical performance.
"""
        super().__init__(name, system_prompt, client)
        self.stance = stance
        self.model = model
    
    def give_opening_statement(self, topic):
        """Provide opening statement on the topic"""
        prompt = f"Give your opening position on: {topic}"
        return self.respond(prompt)
    
    def rebut(self, opponent_argument):
        """Respond to an opponent's argument"""
        prompt = f"Respond to this opposing argument: {opponent_argument}"
        return self.respond(prompt)
    
    def give_closing_statement(self):
        """Provide closing statement"""
        prompt = "Give a brief closing statement summarizing why your position is correct."
        return self.respond(prompt)


class PartyDebater(Debater):
    """Extended debater for party-specific agents - to be implemented later"""
    def __init__(self, party_name, party_context, client, model="gpt-4o-mini"):
        # Will be expanded when adding party-specific context
        stance = f"You represent {party_name} and argue according to their policy positions."
        super().__init__(party_name, stance, client, model)
        self.party_context = party_context  # For future RAG implementation