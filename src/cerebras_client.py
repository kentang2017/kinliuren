import os
from cerebras.cloud.sdk import Cerebras

DEFAULT_MODEL = "gpt-oss-120b"


class CerebrasClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("CerebrasClient must be initialized with an API key.")
        self.client = Cerebras(api_key=api_key)

    def get_chat_completion(self, messages, model=DEFAULT_MODEL, **kwargs):
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=model,
            **kwargs
        )
        return chat_completion


class CustomAIClient:
    """Generic OpenAI-compatible client for custom AI providers."""

    def __init__(self, api_key, base_url):
        if not api_key:
            raise ValueError("CustomAIClient must be initialized with an API key.")
        if not base_url:
            raise ValueError("CustomAIClient must be initialized with a server URL.")
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def get_chat_completion(self, messages, model, **kwargs):
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=model,
            **kwargs
        )
        return chat_completion
