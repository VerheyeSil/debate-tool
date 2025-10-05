from dotenv import load_dotenv
from src.utils.openai_client import OpenAIClient
from src.agents.moderator import Moderator
from src.agents.debater import PartyDebater
from src.debate.debate_manager import DebateManager

load_dotenv()

def main():
    client = OpenAIClient()
    
    moderator = Moderator("Voorzitter", client)
    
    # Creëer partij-specifieke debaters
    groenlinks = PartyDebater("GroenLinks", client)
    vvd = PartyDebater("VVD", client)
    
    debate = DebateManager(moderator, [groenlinks, vvd])
    
    # Debat over een relevant Nederlands politiek onderwerp
    debate.run_debate("Moet Nederland een vermogensbelasting invoeren?", num_rounds=1)

if __name__ == "__main__":
    main()