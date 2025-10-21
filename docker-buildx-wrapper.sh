#!/bin/bash
# Docker buildx wrapper for CDK

# Check if --platform flag is present
if [[ "$*" == *"--platform"* ]]; then
    # Replace 'docker build' with 'docker buildx build'
    exec docker buildx build "$@"
else
    # Normal docker command
    exec /usr/bin/docker "$@"
fi
