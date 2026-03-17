"""
测试智能体的 TAD 分析功能
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from agents.agent import build_agent
from langchain_core.messages import HumanMessage

def test_tad_analysis():
    """测试 TAD 分析功能"""
    agent = build_agent()

    print("=" * 70)
    print("测试 TAD 分析功能")
    print("=" * 70)

    # 测试：TAD 分析
    print("\n测试: 对 chr1 进行 TAD 分析（10000 bp 分辨率）")
    print("-" * 70)
    messages = [HumanMessage(content="请分析 assets/complete_test.mcool 文件中 chr1 染色体的 TAD 结构，使用 10000 bp 分辨率。")]
    config = {"configurable": {"thread_id": "test-tad-001"}}
    response = agent.invoke({"messages": messages}, config=config)

    # 提取最终回答
    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            print(msg.content[:800])  # 只打印前 800 个字符
            break

    print("\n✓ 测试完成")

if __name__ == "__main__":
    test_tad_analysis()
