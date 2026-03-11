#!/bin/bash

# 资讯Agent API 测试脚本
# 用于测试各个接口是否正常工作

BASE_URL="https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent"

echo "=== 测试资讯Agent API ==="
echo ""

# 测试1: 获取资讯列表
echo "1. 测试资讯列表接口..."
curl --location "${BASE_URL}/informationList" \
  --header 'Content-Type: application/json' \
  --data '{
    "category": "discover",
    "page_size": 10
  }'
echo ""
echo ""

# 测试2: 获取Banner列表
echo "2. 测试Banner列表接口..."
curl --location "${BASE_URL}/banner/list" \
  --header 'Content-Type: application/json' \
  --header 'Cookie: sl-session=Lls7F99YsWmriMqia1tQuA==' \
  --data ''
echo ""
echo ""

# 测试3: 获取Banner详情
echo "3. 测试Banner详情接口..."
curl --location "${BASE_URL}/bannerDetail" \
  --header 'Content-Type: application/json' \
  --data '{
    "id": "21640"
  }'
echo ""
echo ""

echo "=== 测试完成 ==="

