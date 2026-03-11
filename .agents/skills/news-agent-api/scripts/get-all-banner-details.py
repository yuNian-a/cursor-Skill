#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Banner查询自动化脚本
自动查询Banner列表，然后使用所有xcf_id分别查询详情
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
COOKIE = "sl-session=Lls7F99YsWmriMqia1tQuA=="

# 如果需要使用代理，取消下面的注释并设置代理地址
# PROXIES = {
#     'http': 'http://proxy.example.com:8080',
#     'https': 'http://proxy.example.com:8080'
# }
# 明确禁用代理，避免环境变量中的代理设置影响
PROXIES = {
    'http': None,
    'https': None
}


def get_banner_list() -> Dict[str, Any]:
    """
    步骤1: 获取Banner列表
    """
    print("📋 步骤1: 查询Banner列表...")
    
    url = f"{BASE_URL}/banner/list"
    headers = {
        'Content-Type': 'application/json',
        'Cookie': COOKIE
    }
    
    try:
        # 禁用环境变量中的代理设置
        session = requests.Session()
        session.trust_env = False
        response = session.get(url, headers=headers, proxies=PROXIES, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 200:
            data = result.get('data', {})
            banner_list = data.get('banner_list', [])
            print(f"✅ 成功获取 {len(banner_list)} 个Banner")
            return data
        else:
            print(f"❌ 接口返回错误: {result}")
            return {}
    except Exception as e:
        print(f"❌ 获取Banner列表失败: {e}")
        sys.exit(1)


def extract_xcf_ids(banner_list: List[Dict[str, Any]]) -> List[str]:
    """
    步骤2: 从Banner列表中提取所有xcf_id
    """
    print("\n🔍 步骤2: 提取所有xcf_id...")
    
    xcf_ids = []
    for banner in banner_list:
        xcf_id = banner.get('xcf_id')
        if xcf_id is not None:
            xcf_ids.append(str(xcf_id))
            print(f"  - 找到 xcf_id: {xcf_id} (标题: {banner.get('title', 'N/A')})")
    
    print(f"✅ 共提取到 {len(xcf_ids)} 个xcf_id: {xcf_ids}")
    return xcf_ids


def get_banner_detail(xcf_id: str) -> Dict[str, Any]:
    """
    步骤3: 获取单个Banner详情
    """
    url = f"{BASE_URL}/bannerDetail"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'id': xcf_id
    }
    
    try:
        # 禁用环境变量中的代理设置
        session = requests.Session()
        session.trust_env = False
        response = session.post(url, headers=headers, json=data, proxies=PROXIES, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get('code') == 200:
            return result.get('data', {})
        else:
            print(f"  ⚠️  Banner {xcf_id} 返回错误: {result}")
            return None
    except Exception as e:
        print(f"  ❌ 获取Banner {xcf_id} 详情失败: {e}")
        return None


def get_all_banner_details(xcf_ids: List[str]) -> List[Dict[str, Any]]:
    """
    步骤3: 批量查询所有Banner详情
    """
    print(f"\n📊 步骤3: 批量查询 {len(xcf_ids)} 个Banner详情...")
    
    details = []
    for i, xcf_id in enumerate(xcf_ids, 1):
        print(f"  [{i}/{len(xcf_ids)}] 查询 Banner {xcf_id}...")
        detail = get_banner_detail(xcf_id)
        if detail:
            details.append({
                'xcf_id': xcf_id,
                'detail': detail
            })
            print(f"    ✅ 成功获取详情: {detail.get('title', 'N/A')}")
        else:
            details.append({
                'xcf_id': xcf_id,
                'detail': None,
                'error': '查询失败'
            })
            print(f"    ❌ 查询失败")
    
    print(f"\n✅ 完成！成功获取 {len([d for d in details if d.get('detail')])}/{len(xcf_ids)} 个Banner详情")
    return details


def main():
    """
    主函数：执行完整的自动化流程
    """
    print("=" * 60)
    print("🚀 Banner查询自动化流程")
    print("=" * 60)
    print()
    
    # 步骤1: 获取Banner列表
    banner_data = get_banner_list()
    banner_list = banner_data.get('banner_list', [])
    
    if not banner_list:
        print("❌ 没有可用的Banner")
        sys.exit(1)
    
    # 步骤2: 提取所有xcf_id
    xcf_ids = extract_xcf_ids(banner_list)
    
    if not xcf_ids:
        print("❌ 没有找到有效的xcf_id")
        sys.exit(1)
    
    # 步骤3: 批量查询详情
    all_details = get_all_banner_details(xcf_ids)
    
    # 输出结果摘要
    print("\n" + "=" * 60)
    print("📋 查询结果摘要")
    print("=" * 60)
    
    for item in all_details:
        xcf_id = item['xcf_id']
        detail = item.get('detail')
        if detail:
            print(f"\n✅ Banner {xcf_id}:")
            print(f"   标题: {detail.get('title', 'N/A')}")
            print(f"   新闻ID: {detail.get('newsId', 'N/A')}")
            print(f"   发布时间: {detail.get('publishTime', 'N/A')}")
        else:
            print(f"\n❌ Banner {xcf_id}: 查询失败")
    
    # 可选：保存结果到文件
    output_file = 'banner-details-result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_details, f, ensure_ascii=False, indent=2)
    print(f"\n💾 完整结果已保存到: {output_file}")
    
    print("\n" + "=" * 60)
    print("✅ 自动化流程执行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()

