"""Utility functions for the agent core runtime."""

import base64
import logging
import os
import pathlib
import shutil
from typing import Any
from uuid import uuid4

# ContentBlock is no longer needed for Claude Agent SDK

from .config import WORKSPACE_DIR

logger = logging.getLogger(__name__)


def create_id() -> str:
    """Generate a unique session ID"""
    return str(uuid4())


def create_ws_directory():
    """Create workspace directory if it doesn't exist"""
    logger.info("Create ws directory")
    pathlib.Path(WORKSPACE_DIR).mkdir(exist_ok=True)


def clean_ws_directory():
    """Clean up workspace directory"""
    logger.info("Clean ws directory...")
    if os.path.exists(WORKSPACE_DIR):
        shutil.rmtree(WORKSPACE_DIR)


def create_error_response(error_message: str) -> dict:
    """Create a standardized error response"""
    return {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "text": f"An error occurred while processing your request: {error_message}",
                }
            ],
        }
    }


def create_empty_response() -> dict:
    """Create a response for when no message is generated"""
    return {
        "message": {
            "role": "assistant",
            "content": [
                {
                    "text": "I apologize, but I couldn't generate a response. Please try again.",
                }
            ],
        }
    }


# Base64 conversion utilities


def decode_base64_string(value: Any) -> bytes:
    """Convert base64 string or bytes to bytes"""
    if isinstance(value, bytes):
        return value
    elif isinstance(value, str):
        return base64.b64decode(value + "==")  # add padding
    else:
        raise ValueError(f"Invalid value type: {type(value)}")


def convert_content_block_bytes(block: dict[str, Any]) -> dict[str, Any]:
    """Convert base64 strings to bytes in a content block"""
    block = block.copy()

    # Handle image, document, and video blocks
    for media_type in ["image", "document", "video"]:
        if media_type in block:
            media_data = block[media_type]
            if "source" in media_data and "bytes" in media_data["source"]:
                media_data["source"]["bytes"] = decode_base64_string(media_data["source"]["bytes"])

    return block


def process_content_blocks(content_blocks: list[dict[str, Any] | str]) -> list[dict[str, Any]]:
    """Process content blocks for Claude Agent SDK (simplified)"""
    processed_blocks = []

    for block in content_blocks:
        if isinstance(block, str):
            processed_blocks.append({"text": block})
        elif isinstance(block, dict):
            if "text" in block:
                processed_blocks.append({"text": block["text"]})
            else:
                # Convert base64 bytes for compatibility
                converted_block = convert_content_block_bytes(block)
                processed_blocks.append(converted_block)

    return processed_blocks


def process_messages(messages: list[Any] | list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Process messages for Claude Agent SDK (simplified)"""
    if not messages:
        return []

    processed_messages = []
    for message in messages:
        if isinstance(message, dict):
            msg = message.copy()
            if "content" in msg and isinstance(msg["content"], list):
                msg["content"] = [convert_content_block_bytes(block) if isinstance(block, dict) else block for block in msg["content"]]
            processed_messages.append(msg)
        else:
            # Handle non-dict messages (convert to dict format)
            processed_messages.append({"role": "user", "content": str(message)})

    return processed_messages


def process_prompt(prompt: str | list[dict[str, Any]]) -> str | list[dict[str, Any]]:
    """Process prompt for Claude Agent SDK (simplified)"""
    if isinstance(prompt, list):
        return process_content_blocks(prompt)
    return prompt
