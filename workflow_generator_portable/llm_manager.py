"""
Mock LLM manager for testing
"""

class LLMManager:
    def __init__(self):
        pass
    
    async def initialize(self):
        return True
    
    async def cleanup(self):
        return True
    
    async def generate(self, provider_name: str, messages: list, **kwargs):
        return "Mock LLM response"