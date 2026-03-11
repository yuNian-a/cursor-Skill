#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取AI方向新闻资讯脚本
调用资讯列表接口获取AI分类的新闻
"""

import requests
import json
import sys
import os
from typing import List, Dict, Any

# 设置Windows下的输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent"
# 明确禁用代理，避免环境变量中的代理设置影响
PROXIES = {
    'http': None,
    'https': None
}


def get_ai_news_list(page_size: int = 10) -> Dict[str, Any]:
    """
    获取AI方向的新闻资讯列表
    """
    print(f"📰 正在获取 {page_size} 条AI方向新闻资讯...")
    
    url = f"{BASE_URL}/informationList"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'category': 'ai',
        'page_size': page_size
    }
    
    try:
        # 禁用环境变量中的代理设置
        session = requests.Session()
        session.trust_env = False
        response = session.post(url, headers=headers, json=data, proxies=PROXIES, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 200:
            data_result = result.get('data', {})
            information_list = data_result.get('information_list', [])
            print(f"✅ 成功获取 {len(information_list)} 条AI新闻")
            return data_result
        else:
            print(f"❌ 接口返回错误: {result}")
            return {}
    except Exception as e:
        print(f"❌ 获取AI新闻列表失败: {e}")
        sys.exit(1)


def format_news_output(news_list: List[Dict[str, Any]]):
    """
    格式化输出新闻列表
    """
    print("\n" + "=" * 80)
    print("🤖 AI方向新闻资讯")
    print("=" * 80)
    print()
    
    for i, news in enumerate(news_list, 1):
        title = news.get('title', 'N/A')
        summary = news.get('summary', '暂无摘要')
        publish_time = news.get('publish_time', 'N/A')
        news_id = news.get('news_id', 'N/A')
        
        print(f"【{i}】{title}")
        print(f"   发布时间: {publish_time}")
        print(f"   新闻ID: {news_id}")
        print(f"   摘要: {summary}")
        print()
    
    print("=" * 80)


def main():
    """
    主函数
    """
    print("=" * 80)
    print("🚀 获取AI方向新闻资讯")
    print("=" * 80)
    print()
    
    # 获取10条AI新闻
    news_data = get_ai_news_list(page_size=10)
    news_list = news_data.get('information_list', [])
    
    if not news_list:
        print("❌ 没有获取到AI新闻")
        sys.exit(1)
    
    # 格式化输出
    format_news_output(news_list)
    
    # 保存结果到文件
    output_file = 'ai-news-result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)
    print(f"💾 完整结果已保存到: {output_file}")
    
    print("\n" + "=" * 80)
    print("✅ 完成！")
    print("=" * 80)


if __name__ == '__main__':
    main()

