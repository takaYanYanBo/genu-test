"""Data models for the agent core runtime."""

from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    """Message model for agent communication."""
    role: str
    content: str | dict[str, Any]


class ModelInfo(BaseModel):
    modelId: str
    region: str = "us-east-1"


class AgentCoreRequest(BaseModel):
    messages: list[Message] | list[dict[str, Any]] = []
    system_prompt: str | None = None
    prompt: str | list[dict[str, Any]] = ""
    model: ModelInfo = {}
