from dotenv import load_dotenv
from src.utils.openai_client import OpenAIClient
from src.agents.moderator import Moderator
from src.agents.debater import Debater
from src.debate.debate_manager import DebateManager

load_dotenv()

def main():
    client = OpenAIClient()
    
    # stream=True is now default in BaseAgent
    moderator = Moderator("Moderator", client)
    debater_a = Debater("Pro", "You argue in favor of the topic", client)
    debater_b = Debater("Con", "You argue against the topic", client)
    
    debate = DebateManager(moderator, [debater_a, debater_b])
    debate.run_debate("Pineapple belongs on pizza", num_rounds=2)

if __name__ == "__main__":
    main()