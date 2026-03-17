"""
测试智能体使用新生成的 mcool 文件
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from agents.agent import build_agent
from langchain_core.messages import HumanMessage

def test_agent_with_mcool():
    """测试智能体使用新生成的 mcool 文件"""
    agent = build_agent()

    print("=" * 70)
    print("测试智能体分析 mcool 文件")
    print("=" * 70)

    # 测试：列出分辨率
    print("\n测试: 列出可用分辨率")
    print("-" * 70)
    messages = [HumanMessage(content="请列出 assets/complete_test.mcool 文件中的可用分辨率。")]
    config = {"configurable": {"thread_id": "test-mcool-001"}}
    response = agent.invoke({"messages": messages}, config=config)

    # 提取最终回答
    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            print(msg.content[:500])  # 只打印前 500 个字符
            break

    print("\n✓ 测试完成")

if __name__ == "__main__":
    test_agent_with_mcool()
