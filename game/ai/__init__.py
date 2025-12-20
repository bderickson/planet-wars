"""
AI package for Planet Wars
"""
from game.ai.base_ai import BaseAI
from game.ai.simple_ai import SimpleAI


def create_ai(difficulty="medium"):
    """
    Factory function to create an AI based on difficulty
    
    Args:
        difficulty: "easy", "medium", or "hard"
        
    Returns:
        An AI instance
    """
    # For now, all difficulties use SimpleAI with different parameters
    # Later we can add more sophisticated AIs
    return SimpleAI(difficulty)

