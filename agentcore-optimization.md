# AgentCore 最適化設定ガイド

## 1. デプロイ前の準備

### x86_64系CPU環境での事前設定
```bash
# ARM64エミュレーション有効化（必須）
docker run --privileged --rm tonistiigi/binfmt --install arm64
```

## 2. 推奨設定変更

### cdk.json の最適化
```json
{
  "createGenericAgentCoreRuntime": true,
  "agentEnabled": true,
  "agentCoreExternalRuntimes": [],
  "modelRegion": "us-east-1"
}
```

### メモリとタイムアウトの調整
```typescript
// generic-agent-core.ts での推奨設定
memorySize: 4096,  // 2048 → 4096に増加
timeout: Duration.minutes(15),  // 10 → 15分に延長
```

### 環境変数の拡張
```typescript
environmentVariables: {
  FILE_BUCKET: this._fileBucket.bucketName,
  MAX_ITERATIONS: '30',
  WORKSPACE_DIR: '/tmp/ws',
  AWS_REGION: Stack.of(this).region,
  UV_NO_CACHE: '1'
}
```

## 3. パフォーマンス最適化

### Docker イメージの最適化
- ARM64プラットフォーム使用
- マルチステージビルド活用
- 不要なパッケージ除去

### ログ設定の最適化
```python
# config.py での推奨設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

## 4. セキュリティ設定

### IAM権限の最小化
- 必要最小限の権限のみ付与
- リソース固有のARN指定
- 条件付きアクセス制御

### ネットワークセキュリティ
```typescript
networkMode: 'PUBLIC',  // または 'PRIVATE'
serverProtocol: 'HTTP', // または 'HTTPS'
```

## 5. モニタリング設定

### CloudWatch統合
- メトリクス収集有効化
- ログ集約設定
- アラーム設定

### X-Ray トレーシング
- 分散トレーシング有効化
- パフォーマンス分析