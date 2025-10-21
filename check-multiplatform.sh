#!/bin/bash

echo "=== Docker マルチプラットフォーム対応状況確認 ==="

echo "1. Docker Buildx 状態確認:"
docker buildx ls

echo -e "\n2. サポートされているプラットフォーム確認:"
docker buildx inspect --bootstrap

echo -e "\n3. QEMU エミュレーター確認:"
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

echo -e "\n4. binfmt_misc 確認:"
cat /proc/sys/fs/binfmt_misc/qemu-aarch64 2>/dev/null || echo "ARM64エミュレーターが見つかりません"

echo -e "\n5. 簡単なマルチプラットフォームテスト:"
docker buildx build --platform linux/amd64,linux/arm64 --dry-run - <<EOF
FROM alpine:latest
RUN echo "Multi-platform test"
EOF

echo -e "\n=== 確認完了 ==="