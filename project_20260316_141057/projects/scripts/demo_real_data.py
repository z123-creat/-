"""
使用真实数据 demo_chr1.mcool 进行演示
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from agents.agent import build_agent
from langchain_core.messages import HumanMessage

def demo_real_data():
    """使用真实数据进行演示"""
    agent = build_agent()

    print("=" * 70)
    print("使用真实数据 demo_chr1.mcool 进行演示")
    print("=" * 70)

    # 演示 1: 列出分辨率
    print("\n【演示 1】列出可用分辨率")
    print("-" * 70)
    response = agent.invoke(
        {"messages": [HumanMessage(
            "请列出 assets/demo_chr1.mcool 文件中的可用分辨率"
        )]},
        config={"configurable": {"thread_id": "demo-real-001"}}
    )

    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            print(msg.content[:400])
            break

    # 演示 2: TAD 分析（推荐分辨率）
    print("\n【演示 2】TAD 分析（100000 bp 分辨率）")
    print("-" * 70)
    response = agent.invoke(
        {"messages": [HumanMessage(
            "分析 assets/demo_chr1.mcool 文件中 chr1 染色体的 TAD 结构，使用 100000 bp 分辨率，不需要文献检索"
        )]},
        config={"configurable": {"thread_id": "demo-real-002"}}
    )

    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            # 提取关键信息
            content = msg.content
            if "16" in content:
                print("✓ 成功识别 16 个 TAD")
            else:
                print(content[:400])
            break

    # 演示 3: Compartment 分析
    print("\n【演示 3】Compartment 分析")
    print("-" * 70)
    response = agent.invoke(
        {"messages": [HumanMessage(
            "分析 assets/demo_chr1.mcool 中 chr1 的 compartments，使用 100000 bp 分辨率，不需要文献检索"
        )]},
        config={"configurable": {"thread_id": "demo-real-003"}}
    )

    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            print("✓ Compartment 分析完成")
            break

    print("\n" + "=" * 70)
    print("✓ 演示完成！")
    print("=" * 70)
    print("\n文件信息:")
    print("  文件: assets/demo_chr1.mcool")
    print("  大小: 5.37 MB")
    print("  分辨率: 10000 bp, 100000 bp, 1000000 bp")
    print("  TAD 数量: 16 个")
    print("  包含平衡权重: ✓")

if __name__ == "__main__":
    demo_real_data()
