#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化输出资讯列表
"""
import sys
import json

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def clean_text(text):
    """清理文本中的无效Unicode字符"""
    if not text:
        return ""
    if not isinstance(text, str):
        return str(text)
    # 替换无效的Unicode字符（包括surrogate pairs）
    try:
        # 先尝试正常编码
        text.encode('utf-8', errors='strict')
        return text
    except (UnicodeEncodeError, UnicodeError):
        # 如果有问题，替换无效字符
        return text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

def format_news_output():
    """格式化输出资讯列表"""
    try:
        # 从标准输入读取JSON数据，使用surrogatepass处理无效字符
        input_text = sys.stdin.buffer.read().decode('utf-8', errors='surrogatepass')
        data = json.loads(input_text)
        items = data.get('data', {}).get('information_list', [])
        
        print("\n" + "=" * 80)
        print(f"📰 RWA分类资讯列表 (共{len(items)}条)")
        print("=" * 80 + "\n")
        
        for i, item in enumerate(items, 1):
            title = clean_text(item.get("title", "无标题"))
            publish_time = item.get("publish_time", "未知")
            summary = clean_text(item.get("summary", "无摘要"))
            tags = [clean_text(tag) for tag in item.get("tags", [])]
            influence_score = item.get("influence_score", 0)
            news_id = item.get("news_id", "未知")
            word_count = item.get("word_count", 0)
            read_time = item.get("read_time", 0)
            
            # 截取摘要前150个字符
            summary_preview = summary[:150] + "..." if len(summary) > 150 else summary
            
            print(f"【{i}】{title}")
            print(f"    📅 发布时间: {publish_time}")
            print(f"    📝 摘要: {summary_preview}")
            print(f"    🏷️  标签: {', '.join(tags) if tags else '无标签'}")
            print(f"    📊 影响分: {influence_score}")
            print(f"    📄 字数: {word_count} | 阅读时长: {read_time}分钟")
            print(f"    🔗 新闻ID: {news_id}")
            print("-" * 80 + "\n")
        
        print("=" * 80)
        print(f"✅ 共显示 {len(items)} 条资讯")
        print("=" * 80)
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 处理错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    format_news_output()

