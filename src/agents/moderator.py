from .base_agent import BaseAgent

class Moderator(BaseAgent):
    def __init__(self, name, client, model="gpt-4o-mini"):
        system_prompt = """You are a debate moderator for a political debate.
            Your role is to:
            - Introduce the debate topic clearly
            - Ask pointed questions to each debater
            - Keep the debate on track and focused
            - Call on specific debaters to respond to each other's points
            - Ensure equal speaking time
            - Summarize key points of disagreement

            Be professional, neutral, and concise. Model yourself after a Tweede Kamer voorzitter.
            """
        super().__init__(name, system_prompt, client)
        self.model = model
    
    def introduce_debate(self, topic):
        """Generate opening statement for the debate"""
        prompt = f"Introduce a debate on the following topic: {topic}"
        return self.respond(prompt)
    
    def ask_opening_position(self, debater_name, topic):
        """Ask a debater for their opening position"""
        prompt = f"Ask {debater_name} to state their position on: {topic}"
        return self.respond(prompt)
    
    def ask_rebuttal(self, debater_name, previous_point):
        """Ask a debater to respond to a previous point"""
        prompt = f"Ask {debater_name} to respond to this argument: {previous_point}"
        return self.respond(prompt)
    
    def ask_follow_up(self, debater_name, aspect):
        """Ask a follow-up question on a specific aspect"""
        prompt = f"Ask {debater_name} a follow-up question about: {aspect}"
        return self.respond(prompt)
    
    def close_debate(self):
        """Generate closing statement"""
        prompt = "Provide a brief closing statement summarizing the main points of disagreement."
        return self.respond(prompt)