import time

class DebateManager:
    def __init__(self, moderator, debaters):
        self.moderator = moderator
        self.debaters = debaters
        self.transcript = []
    
    def run_debate(self, topic, num_rounds=3):
        self._print_header(topic)
        
        # Opening
        self._print_speaker(self.moderator.name)
        opening = self.moderator.respond(f"Introduce debate on: {topic}")
        self.log(self.moderator.name, opening)
        self._pause()
        
        # Rounds
        for round_num in range(num_rounds):
            self._print_round(round_num + 1)
            
            for debater in self.debaters:
                self._print_speaker(self.moderator.name)
                prompt = self.moderator.respond(f"Ask {debater.name} for their position")
                self.log(self.moderator.name, prompt)
                self._pause()
                
                self._print_speaker(debater.name)
                response = debater.respond(prompt)
                self.log(debater.name, response)
                self._pause()
        
        # Closing
        self._print_speaker(self.moderator.name)
        closing = self.moderator.close_debate()
        self.log(self.moderator.name, closing)
        
        return self.transcript
    
    def log(self, speaker, message):
        entry = {"speaker": speaker, "message": message}
        self.transcript.append(entry)
    
    def _print_header(self, topic):
        print("\n" + "="*80)
        print(f"DEBATE: {topic}".center(80))
        print("="*80 + "\n")
    
    def _print_round(self, round_num):
        print("\n" + "-"*80)
        print(f"ROUND {round_num}".center(80))
        print("-"*80 + "\n")
    
    def _print_speaker(self, name):
        print(f"\n\033[1m{name}:\033[0m ", end='', flush=True)  # Bold name
    
    def _pause(self, seconds=1):
        """Brief pause between speakers for readability"""
        time.sleep(seconds)