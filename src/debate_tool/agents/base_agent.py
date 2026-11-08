"""Base class for every agent in a debate."""

DEFAULT_MODEL = "gpt-4o-mini"


class BaseAgent:
    """An LLM agent with a system prompt and its own conversation history.

    The history holds everything the agent has heard and said, so each new
    response is generated with the full debate so far as context.
    """

    def __init__(self, name, system_prompt, client, model=DEFAULT_MODEL, stream=True):
        self.name = name
        self.system_prompt = system_prompt
        self.client = client
        self.model = model
        self.stream = stream
        self.conversation_history = []

    def hear(self, speaker, message):
        """Add something another participant said to this agent's history."""
        self.conversation_history.append({"role": "user", "content": f"{speaker}: {message}"})

    def respond(self, prompt=None):
        """Generate a response, optionally after an extra instruction.

        Without a prompt the agent simply answers the last thing it heard.
        The response is printed (streamed live when ``stream`` is on) and
        returned as a string.
        """
        if prompt is not None:
            self.conversation_history.append({"role": "user", "content": prompt})
        messages = [{"role": "system", "content": self.system_prompt}, *self.conversation_history]
        response = self.client.get_completion(messages, model=self.model, stream=self.stream)
        if not self.stream:
            print(response)
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
