# Use ARM64 base image for Bedrock AgentCore compatibility
FROM --platform=linux/arm64 public.ecr.aws/docker/library/python:3.13

WORKDIR /var/task

# Environment variables for UV package manager
ENV UV_NO_CACHE=1
ENV UV_NO_MANAGED_PYTHON=1
ENV UV_PYTHON=/usr/local/bin/python
ENV UV_INSTALL_DIR=/usr/local/bin
ENV UV_PROJECT_ENVIRONMENT=/tmp/.venv

# Install system dependencies including Node.js
RUN apt-get update -y && apt-get install curl graphviz git -y \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Claude Code CLI globally via npm (official package)
RUN npm install -g @anthropic-ai/claude-code

# Copy dependency files
COPY pyproject.toml .python-version uv.lock ./

# Install Python dependencies
RUN uv sync

# Set environment variables for Claude Code/Agent SDK integration
ENV CLAUDE_CODE_USE_BEDROCK=1
ENV ANTHROPIC_MODEL=us.anthropic.claude-3-5-sonnet-20241022-v2:0

# Copy application files
COPY app.py mcp.json ./
COPY src/ ./src/

# Expose port 8080 as required by AgentCore
EXPOSE 8080

# Start the application with OpenTelemetry instrumentation
CMD ["uv", "run", "opentelemetry-instrument", "python", "app.py"]
