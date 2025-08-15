"""Novel Writer Agent Package

A Romance/Fantasy hybrid agent that generates daily novel pages,
inspired by real-world factors like mood, world news, and writer influences.

Built using LangChain and LangGraph for autonomous creative writing.
"""

from .agent import NovelWriterAgent
from .daily_writer import DailyWriter

__version__ = "0.1.0"
__author__ = "Novel Writer Agent Project"

__all__ = ["NovelWriterAgent", "DailyWriter"]
