# Gen-U AgentCore Edition

This is a refactored version of the Generative AI Use Cases application, focused exclusively on **Amazon Bedrock AgentCore** functionality.

## What's Changed

This edition has been streamlined to include only:

### Frontend

- **AgentCore Chat Page**: The main interface for interacting with Bedrock AgentCore
- **Landing Page**: Simplified to show only AgentCore
- **Settings Page**: For configuration
- **Shared Chat Page**: For sharing conversations
- **Common Components**: All shared UI components and utilities

### Infrastructure (CDK)

- **AgentCore Stack**: Bedrock AgentCore runtime and related resources
- **Common Infrastructure**:
  - Authentication (Cognito)
  - API Gateway
  - Database (DynamoDB)
  - Web hosting (CloudFront + S3)
  - Common security and networking

### Removed Features

All other use cases have been removed:

- Chat, RAG Chat, Agent Chat
- Text Generation, Summarization, Translation
- Image/Video Generation and Analysis
- Meeting Minutes, Writer, Transcription
- Diagram Generation, Web Content Extraction
- Use Case Builder
- MCP Chat, Flow Chat, Voice Chat

## Configuration

The application is configured via `packages/cdk/cdk.json`:

```json
{
  "createGenericAgentCoreRuntime": true,
  "agentEnabled": false,
  "ragEnabled": false,
  "ragKnowledgeBaseEnabled": false,
  "mcpEnabled": false,
  "useCaseBuilderEnabled": false,
  "imageGenerationModelIds": [],
  "videoGenerationModelIds": [],
  "speechToSpeechModelIds": []
}
```

## Deployment

Follow the standard deployment process:

```bash
# Install dependencies
npm ci

# Deploy infrastructure
cd packages/cdk
npx cdk deploy --all

# The frontend will be automatically deployed to S3/CloudFront
```

## Benefits of This Edition

1. **Simplified Codebase**: Easier to understand and maintain
2. **Reduced Infrastructure Costs**: Only deploys necessary resources
3. **Faster Deployment**: Fewer stacks to create
4. **Focused Functionality**: Dedicated to AgentCore use cases
5. **Minimal Code Changes**: Original code structure preserved where possible

## Original Repository

This is based on: https://github.com/aws-samples/generative-ai-use-cases

For the full-featured version with all use cases, please refer to the original repository.
