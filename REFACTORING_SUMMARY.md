# Gen-U AgentCore Edition - Refactoring Summary

## Overview

This document summarizes the refactoring performed to create an AgentCore-focused version of the Generative AI Use Cases application.

## Changes Made

### 1. Frontend Changes (`packages/web/src`)

#### Deleted Pages

- `AgentChatPage.tsx`
- `ChatPage.tsx`
- `FlowChatPage.tsx`
- `GenerateDiagramPage.tsx`
- `GenerateImagePage.tsx`
- `GenerateTextPage.tsx`
- `GenerateVideoPage.tsx`
- `McpChatPage.tsx`
- `MeetingMinutesPage.tsx`
- `OptimizePromptPage.tsx`
- `RagKnowledgeBasePage.tsx`
- `RagPage.tsx`
- `StatPage.tsx`
- `SummarizePage.tsx`
- `TranscribePage.tsx`
- `TranslatePage.tsx`
- `VideoAnalyzerPage.tsx`
- `VoiceChatPage.tsx`
- `WebContent.tsx`
- `WriterPage.tsx`
- `useCaseBuilder/` (entire directory)
- `UseCaseBuilderRoot.tsx`

#### Kept Pages

- `AgentCorePage.tsx` - Main functionality
- `LandingPage.tsx` - Simplified to show only AgentCore
- `Setting.tsx` - Configuration page
- `SharedChatPage.tsx` - For sharing conversations
- `NotFound.tsx` - Error handling

#### Modified Files

- `main.tsx` - Simplified routing to include only AgentCore routes
- `App.tsx` - Simplified navigation to show only AgentCore menu item
- `LandingPage.tsx` - Simplified to display only AgentCore card

#### Kept Components

All components in `packages/web/src/components/` were kept as they may be used by:

- AgentCorePage
- Common functionality (authentication, layout, etc.)
- Shared utilities

#### Kept Hooks

All hooks in `packages/web/src/hooks/` were kept as they may be used by:

- AgentCorePage
- Common functionality
- Shared utilities

### 2. Infrastructure Changes (`packages/cdk`)

#### Configuration Changes (`cdk.json`)

```json
{
  "createGenericAgentCoreRuntime": true, // Changed from false
  "agentEnabled": false, // Kept as false
  "ragEnabled": false, // Kept as false
  "ragKnowledgeBaseEnabled": false, // Kept as false
  "mcpEnabled": false, // Kept as false
  "useCaseBuilderEnabled": false, // Changed from true
  "imageGenerationModelIds": [], // Cleared
  "videoGenerationModelIds": [], // Cleared
  "speechToSpeechModelIds": [] // Cleared
}
```

#### Kept Infrastructure

- `lib/agent-core-stack.ts` - Main AgentCore infrastructure
- `lib/generative-ai-use-cases-stack.ts` - Main application stack
- `lib/create-stacks.ts` - Stack orchestration
- `lib/construct/` - All constructs (may be used by main stack)
- `lambda/` - All Lambda functions (may be used by API)
- `lambda-python/generic-agent-core-runtime/` - AgentCore runtime

#### Conditional Stacks

The following stacks are created conditionally based on configuration:

- `AgentStack` - Only if `agentEnabled: true`
- `RagKnowledgeBaseStack` - Only if `ragKnowledgeBaseEnabled: true`
- `GuardrailStack` - Only if `guardrailEnabled: true`
- `DashboardStack` - Only if `dashboard: true`
- `CloudFrontWafStack` - Only if IP restrictions or custom domain configured
- `ClosedNetworkStack` - Only if `closedNetworkMode: true`

With the current configuration, only these stacks will be deployed:

- `ApplicationInferenceProfileStack` (for model access)
- `AgentCoreStack` (AgentCore runtime)
- `GenerativeAiUseCasesStack` (main application)

### 3. Preserved Functionality

#### Common Features (Kept)

- Authentication (Cognito User Pool)
- API Gateway
- Database (DynamoDB)
- Web hosting (CloudFront + S3)
- File upload/download
- Chat history
- Message management
- System context management
- Feedback system

#### AgentCore Features (Kept)

- AgentCore runtime
- AgentCore API integration
- AgentCore chat interface
- Model configuration
- Session management

## Deployment

The application can be deployed using the standard process:

```bash
# Install dependencies
npm ci

# Deploy CDK stacks
cd packages/cdk
npx cdk deploy --all
```

## Benefits

1. **Reduced Complexity**: Fewer pages and routes to maintain
2. **Lower Costs**: Only necessary infrastructure is deployed
3. **Faster Deployment**: Fewer stacks to create
4. **Focused Functionality**: Clear purpose and scope
5. **Minimal Code Changes**: Original structure preserved where possible

## Rollback

To restore the original functionality:

1. Restore deleted page files from git history
2. Restore original `main.tsx` and `App.tsx`
3. Restore original `LandingPage.tsx`
4. Update `cdk.json` to enable desired features
5. Redeploy

## Testing Recommendations

1. Test AgentCore chat functionality
2. Test authentication flow
3. Test file upload/download
4. Test chat history and sharing
5. Test settings page
6. Verify only necessary infrastructure is deployed
7. Check CloudWatch logs for any errors

## Notes

- All hooks and components were kept to avoid breaking dependencies
- Lambda functions were kept as they may be used by the API
- The refactoring focused on removing UI pages and disabling infrastructure features
- No changes were made to the core business logic or API structure
