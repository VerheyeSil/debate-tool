from openai import OpenAI
import os

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def get_completion(self, messages, model="gpt-4o-mini", temperature=0.7, stream=False):
        if stream:
            return self._stream_completion(messages, model, temperature)
        else:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
    
    def _stream_completion(self, messages, model, temperature):
        """Stream the response and return complete text"""
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True
        )
        
        complete_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end='', flush=True)
                complete_response += content
        
        print()  # New line after streaming completes
        return complete_response