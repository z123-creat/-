"""
生成智能体工作流预览图
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from agents.agent import build_agent

def generate_workflow_preview():
    """生成工作流预览"""
    print("=" * 70)
    print("生成三维基因组分析智能体工作流预览")
    print("=" * 70)

    # 构建智能体
    agent = build_agent()

    # 获取工作流图
    graph = agent.get_graph()

    # 生成 Mermaid 格式的图表
    mermaid_code = graph.draw_mermaid()

    # 保存到文件
    output_path = "docs/workflow_preview.mmd"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)

    print(f"\n✓ Mermaid 格式工作流已保存到: {output_path}")
    print("\n" + mermaid_code)

    # 生成文本格式的工作流说明
    print("\n" + "=" * 70)
    print("工作流说明")
    print("=" * 70)

    print("\n【智能体架构】")
    print("  - 核心框架: LangGraph + LangChain")
    print("  - 大模型: ChatOpenAI (支持多轮对话和工具调用)")
    print("  - 记忆: MemorySaver (短期记忆，保留最近 40 条消息)")

    print("\n【工具列表】")
    tools_info = [
        ("read_mcool_file", "读取 mcool 文件，获取文件基本信息"),
        ("get_chromosome_matrix", "获取指定染色体的接触矩阵"),
        ("list_available_resolutions", "列出多分辨率 mcool 文件的所有分辨率"),
        ("analyze_tads", "TAD (拓扑关联结构域) 分析"),
        ("analyze_compartments", "Compartment (A/B 区室) 分析"),
        ("search_literature", "搜索文献知识库"),
        ("save_analysis", "保存分析结果到数据库"),
        ("query_analysis_history", "查询历史分析记录")
    ]

    for i, (tool_name, tool_desc) in enumerate(tools_info, 1):
        print(f"  {i}. {tool_name}")
        print(f"     - {tool_desc}")

    print("\n【工作流程】")
    print("""
    用户输入
       ↓
    ┌──────────────┐
    │  Agent LLM   │
    └──────┬───────┘
           │
    ┌──────▼──────┐
    │  需求解析   │  ← 理解用户意图
    └──────┬──────┘
           │
    ┌──────▼──────────────────────┐
    │      工具调度器             │
    └──────┬──────────────────────┘
           │
    ┌──────▼──────────────┬──────────────────────┐
    │   数据读取工具      │   分析工具           │
    ├─────────────────────┼──────────────────────┤
    │ • read_mcool_file   │ • analyze_tads       │
    │ • get_chromosome... │ • analyze_compart... │
    │ • list_resolutions  │                      │
    └─────────┬──────────┴──────────┬───────────┘
              │                     │
    ┌─────────▼─────────────────────▼───────────┐
    │         结果整合与推理                     │
    └─────────┬─────────────────────┬───────────┘
              │                     │
    ┌─────────▼─────────────┬──────▼───────────┐
    │   知识库搜索          │  历史记录管理   │
    │ • search_literature   │ • save_analysis  │
    │                      │ • query_history  │
    └─────────┬─────────────┴──────────────────┘
              │
    ┌─────────▼──────────┐
    │   结论验证         │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │   生成报告         │
    └─────────┬──────────┘
              ↓
         输出给用户
    """)

    print("\n【典型分析场景】")
    print("\n场景 1: TAD 分析")
    print("  1. 用户: '分析 chr1 的 TAD 结构'")
    print("  2. Agent → read_mcool_file (获取文件信息)")
    print("  3. Agent → analyze_tads (执行 TAD 分析)")
    print("  4. Agent → search_literature (验证结论)")
    print("  5. Agent → 生成综合报告")

    print("\n场景 2: Compartment 分析")
    print("  1. 用户: '分析 chr2 的 A/B compartments'")
    print("  2. Agent → list_available_resolutions (选择分辨率)")
    print("  3. Agent → analyze_compartments (执行分析)")
    print("  4. Agent → save_analysis (保存结果)")
    print("  5. Agent → 生成可视化报告")

    print("\n" + "=" * 70)
    print("✓ 工作流预览生成完成！")
    print("=" * 70)

if __name__ == "__main__":
    generate_workflow_preview()
