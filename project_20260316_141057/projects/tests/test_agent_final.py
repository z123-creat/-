"""
验证智能体的核心功能（简化版）
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from agents.agent import build_agent
from langchain_core.messages import HumanMessage

def test_agent_basic():
    """测试智能体基本功能"""
    agent = build_agent()

    print("=" * 70)
    print("验证智能体核心功能")
    print("=" * 70)

    # 测试 1: 文件读取
    print("\n[测试 1] 文件读取和分辨率列表")
    print("-" * 70)
    messages = [HumanMessage(content="请读取 assets/complete_test.mcool 文件，告诉我包含哪些分辨率？")]
    config = {"configurable": {"thread_id": "test-basic-001"}}
    response = agent.invoke({"messages": messages}, config=config)

    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            # 提取关键信息
            content = msg.content
            if "1000" in content and "5000" in content and "10000" in content:
                print("✓ 成功：工具正确识别了三个分辨率（1000, 5000, 10000 bp）")
            else:
                print(f"✗ 失败：未正确识别所有分辨率")
                print(content[:300])
            break

    # 测试 2: TAD 分析（不调用文献检索）
    print("\n[测试 2] TAD 分析")
    print("-" * 70)
    messages = [HumanMessage(content="请直接调用工具分析 assets/complete_test.mcool 文件中 chr1 染色体的 TAD 结构，使用 10000 bp 分辨率，不需要文献检索。")]
    config = {"configurable": {"thread_id": "test-basic-002"}}
    response = agent.invoke({"messages": messages}, config=config)

    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            content = msg.content
            if "TAD" in content or "tad" in content.lower():
                print("✓ 成功：智能体返回了 TAD 分析结果")
            else:
                print(f"✗ 失败：未返回 TAD 分析结果")
                print(content[:300])
            break

    # 测试 3: Compartment 分析
    print("\n[测试 3] Compartment 分析")
    print("-" * 70)
    messages = [HumanMessage(content="请直接调用工具分析 assets/complete_test.mcool 文件中 chr1 染色体的 compartments，使用 10000 bp 分辨率，不需要文献检索。")]
    config = {"configurable": {"thread_id": "test-basic-003"}}
    response = agent.invoke({"messages": messages}, config=config)

    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            content = msg.content
            if "compartment" in content.lower() or "A" in content or "B" in content:
                print("✓ 成功：智能体返回了 Compartment 分析结果")
            else:
                print(f"✗ 失败：未返回 Compartment 分析结果")
                print(content[:300])
            break

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)

if __name__ == "__main__":
    test_agent_basic()
