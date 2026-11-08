"""Thin wrapper around the OpenAI chat completions API."""

import os

from openai import OpenAI

from debate_tool.agents.base_agent import DEFAULT_MODEL


class OpenAIClient:
    """Gets chat completions, optionally streaming them to the terminal."""

    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def get_completion(self, messages, model=DEFAULT_MODEL, temperature=0.7, stream=False):
        """Return the completion text for a list of chat messages.

        With ``stream=True`` the text is also printed as it arrives.
        """
        if stream:
            return self._stream_completion(messages, model, temperature)
        response = self.client.chat.completions.create(model=model, messages=messages, temperature=temperature)
        return response.choices[0].message.content

    def _stream_completion(self, messages, model, temperature):
        """Print the response while it streams in and return the full text."""
        stream = self.client.chat.completions.create(
            model=model, messages=messages, temperature=temperature, stream=True
        )
        parts = []
        for chunk in stream:
            # Some chunks (e.g. usage info) have no choices.
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                parts.append(content)
        print()
        return "".join(parts)
