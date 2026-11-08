"""Running a debate: who speaks when, and what everyone hears."""

import time


class DebateManager:
    """Runs a debate between a moderator and debaters and keeps a transcript.

    Everything a participant says is passed on to all other participants, so
    debaters can respond to each other and the moderator can summarise.
    """

    def __init__(self, moderator, debaters, pause_seconds=1):
        self.moderator = moderator
        self.debaters = debaters
        self.pause_seconds = pause_seconds
        self.transcript = []

    @property
    def participants(self):
        return [self.moderator, *self.debaters]

    def run_debate(self, topic, num_rounds=3):
        """Run the full debate and return the transcript.

        Each round the moderator gives every debater the floor once.
        """
        self._print_header(topic)

        self._speak(self.moderator, self.moderator.introduce_debate, topic, [d.name for d in self.debaters])

        for round_num in range(1, num_rounds + 1):
            self._print_round(round_num)
            for debater in self.debaters:
                self._speak(self.moderator, self.moderator.give_floor, debater.name)
                self._speak(debater, debater.respond)

        self._speak(self.moderator, self.moderator.close_debate, pause=False)
        return self.transcript

    def _speak(self, speaker, action, *args, pause=True):
        """Let a participant speak, log it and share it with everyone else."""
        self._print_speaker(speaker.name)
        message = action(*args)
        self.log(speaker.name, message)
        for participant in self.participants:
            if participant is not speaker:
                participant.hear(speaker.name, message)
        if pause:
            # Short pause between speakers to keep the output readable.
            time.sleep(self.pause_seconds)

    def log(self, speaker, message):
        """Add a statement to the transcript."""
        self.transcript.append({"speaker": speaker, "message": message})

    @staticmethod
    def _print_header(topic):
        print("\n" + "=" * 80)
        print(f"DEBAT: {topic}".center(80))
        print("=" * 80 + "\n")

    @staticmethod
    def _print_round(round_num):
        print("\n" + "-" * 80)
        print(f"RONDE {round_num}".center(80))
        print("-" * 80 + "\n")

    @staticmethod
    def _print_speaker(name):
        # Speaker name in bold; the response is printed on the same line.
        print(f"\n\033[1m{name}:\033[0m ", end="", flush=True)
