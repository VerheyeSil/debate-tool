class BaseAgent:
    def __init__(self, name, system_prompt, client, stream=True):
        self.name = name
        self.system_prompt = system_prompt
        self.client = client
        self.conversation_history = []
        self.stream = stream
    
    def respond(self, context):
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history,
            {"role": "user", "content": context}
        ]
        response = self.client.get_completion(messages, stream=self.stream)
        self.conversation_history.append({"role": "user", "content": context})
        self.conversation_history.append({"role": "assistant", "content": response})
        return response