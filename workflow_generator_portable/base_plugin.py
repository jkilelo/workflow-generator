"""
Mock base plugin classes for testing
"""

from typing import Dict, List, Any
from abc import ABC, abstractmethod

class PluginMetadata:
    def __init__(self, name: str, version: str, description: str, author: str, category: str):
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.category = category

class BasePlugin(ABC):
    def __init__(self):
        pass
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        pass
    
    async def initialize(self) -> bool:
        return True
    
    async def cleanup(self) -> bool:
        return True
    
    @abstractmethod
    def get_api_routes(self) -> List[Dict[str, Any]]:
        pass