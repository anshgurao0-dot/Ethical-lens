from abc import ABC, abstractmethod
from typing import Any, Dict
from app.models.product_analysis import AgentVerdict

class BaseAgent(ABC):
    """
    Abstract base class for all Ethical Lens agents.
    Enforces a common interface for analysis and verdict generation.
    """

    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    @abstractmethod
    async def analyze(self, product_data: Dict[str, Any], context: Dict[str, Any] = None) -> AgentVerdict:
        """
        Performs the agent's specific analysis on the product data.

        Args:
            product_data: Dictionary containing raw product information (ingredients, brand, etc.).
            context: Optional dictionary for additional context (e.g., user profile, location).

        Returns:
            AgentVerdict: The agent's findings, score, and status.
        """
        pass
