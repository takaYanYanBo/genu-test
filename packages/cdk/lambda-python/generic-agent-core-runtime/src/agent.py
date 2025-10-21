"""Agent management for the agent core runtime using Claude Agent SDK."""

import json
import logging
from collections.abc import AsyncGenerator
from typing import Any, Dict, List
from datetime import datetime

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

from .config import get_system_prompt
from .tools import ToolManager
from .types import Message, ModelInfo
from .utils import process_messages, process_prompt

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages Claude agent creation and execution using Claude Agent SDK."""

    def __init__(self):
        self.tool_manager = ToolManager()
        self.session_id = None
        self.trace_id = None

    def set_session_info(self, session_id: str, trace_id: str):
        """Set session and trace IDs"""
        self.session_id = session_id
        self.trace_id = trace_id
        self.tool_manager.set_session_info(session_id, trace_id)

    async def process_request_streaming(
        self,
        messages: list[Message] | list[dict[str, Any]],
        system_prompt: str | None,
        prompt: str | list[dict[str, Any]],
        model_info: ModelInfo,
    ) -> AsyncGenerator[str]:
        """Process a request using Claude Agent SDK and yield streaming responses"""
        try:
            # Combine system prompts
            combined_system_prompt = get_system_prompt(system_prompt)

            # Process messages and prompt using utility functions
            processed_messages = process_messages(messages)
            processed_prompt = process_prompt(prompt)

            # Build conversation history and current prompt
            conversation_history = ""
            for message in processed_messages:
                role = message.get("role", "user")
                content = message.get("content", "")
                conversation_history += f"{role}: {content}\n"

            # Current prompt
            current_prompt = ""
            if isinstance(processed_prompt, str):
                current_prompt = processed_prompt
            elif isinstance(processed_prompt, list) and processed_prompt:
                # Handle complex prompt format
                for item in processed_prompt:
                    if isinstance(item, dict) and "text" in item:
                        current_prompt += item["text"]

            # Full prompt with conversation history
            full_prompt = f"{conversation_history}\nuser: {current_prompt}" if conversation_history else current_prompt

            # Configure Claude Agent SDK options
            # Get S3 upload tool from our existing tool manager
            upload_tool = self.tool_manager.get_upload_tool()

            # MCP servers configuration (using existing mcp.json setup)
            mcp_servers = {
                "time": {"command": "uvx", "args": ["mcp-server-time"]},
                "awslabs.aws-documentation-mcp-server": {"command": "uvx", "args": ["awslabs.aws-documentation-mcp-server@latest"]},
                "awslabs.cdk-mcp-server": {"command": "uvx", "args": ["awslabs.cdk-mcp-server@latest"]},
                "awslabs.aws-diagram-mcp-server": {"command": "uvx", "args": ["awslabs.aws-diagram-mcp-server@latest"]},
                "awslabs.nova-canvas-mcp-server": {"command": "uvx", "args": ["awslabs.nova-canvas-mcp-server@latest"]}
            }

            options = ClaudeAgentOptions(
                mcp_servers=mcp_servers,
                system_prompt=combined_system_prompt or "You are a helpful AI assistant with access to various tools and MCP servers.",
                allowed_tools=[
                    "mcp__time",
                    "mcp__awslabs.aws-documentation-mcp-server",
                    "mcp__awslabs.cdk-mcp-server",
                    "mcp__awslabs.aws-diagram-mcp-server",
                    "mcp__awslabs.nova-canvas-mcp-server",
                    "Bash",
                    "Edit",
                    "MultiEdit",
                    "NotebookEdit",
                    "WebFetch",
                    "WebSearch",
                    "Write",
                    "Read",
                    "Glob",
                    "Grep"
                ],
                max_turns=10,
            )

            # Use Claude Agent SDK
            async with ClaudeSDKClient(options=options) as client:
                logger.info(f"Starting Claude Agent SDK query: {full_prompt[:100]}...")

                # Send the query
                await client.query(full_prompt)

                # Stream responses and convert to AgentCore format
                async for message in client.receive_response():
                    try:
                        # Convert Claude Agent SDK message to AgentCore format
                        agentcore_event = self._convert_claude_sdk_message_to_agentcore(message)
                        if agentcore_event:
                            yield json.dumps(agentcore_event, ensure_ascii=False) + "\n"

                    except Exception as e:
                        logger.error(f"Error processing Claude SDK message: {e}")
                        continue

                logger.info("Claude Agent SDK query completed")

        except Exception as e:
            logger.error(f"Error processing agent request: {e}")
            error_event = {
                "event": {
                    "internalServerException": {
                        "message": f"An error occurred while processing your request: {str(e)}",
                    }
                }
            }
            yield json.dumps(error_event, ensure_ascii=False) + "\n"

    def _convert_claude_sdk_message_to_agentcore(self, message) -> Dict[str, Any] | None:
        """Convert Claude Agent SDK message to AgentCore-compatible format"""
        try:
            message_type = type(message).__name__

            if not hasattr(message, "content"):
                return None

            # Process content blocks
            for block in message.content:
                block_type = type(block).__name__

                # Handle text content
                if hasattr(block, "text"):
                    return {
                        "event": {
                            "contentBlockDelta": {
                                "delta": {
                                    "text": block.text
                                }
                            }
                        }
                    }

                # Handle tool use
                elif hasattr(block, "name") and hasattr(block, "input"):
                    return {
                        "event": {
                            "contentBlockStart": {
                                "start": {
                                    "toolUse": {
                                        "toolUseId": getattr(block, "id", "unknown"),
                                        "name": block.name,
                                        "input": json.dumps(block.input) if not isinstance(block.input, str) else block.input
                                    }
                                }
                            }
                        }
                    }

                # Handle tool results
                elif hasattr(block, "tool_use_id") and hasattr(block, "content"):
                    return {
                        "event": {
                            "contentBlockDelta": {
                                "delta": {
                                    "text": f"Tool result: {block.content}"
                                }
                            }
                        }
                    }

            return None

        except Exception as e:
            logger.error(f"Error converting Claude SDK message: {e}")
            return None
