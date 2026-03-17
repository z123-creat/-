"""
Extract and display the agent's response cleanly
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from agents.agent import build_agent
from langchain_core.messages import HumanMessage

def run_analysis():
    """Run the agent and extract the final response"""
    agent = build_agent()

    messages = [
        HumanMessage(content="请分析 assets/test.mcool 文件，对 chr1 染色体进行完整的 TAD 和 Compartment 分析，并生成详细的报告。")
    ]

    config = {
        "configurable": {
            "thread_id": "test-thread-full-001"
        }
    }

    response = agent.invoke({"messages": messages}, config=config)

    # Get the last AIMessage with content
    for msg in reversed(response['messages']):
        if hasattr(msg, 'content') and msg.content and not msg.content.startswith('{'):
            return msg.content

    return "No content found"

if __name__ == "__main__":
    result = run_analysis()
    print(result)
