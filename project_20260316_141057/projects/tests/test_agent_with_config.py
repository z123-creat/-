"""
Test the agent with proper configuration
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from agents.agent import build_agent
from langchain_core.messages import HumanMessage

def test_agent_with_config():
    """Test the agent with proper configuration"""
    print("Testing agent with proper configuration...")
    print("=" * 60)

    try:
        # Build agent
        agent = build_agent()
        print("✓ Agent initialized\n")

        # Create test messages
        messages = [
            HumanMessage(content="请列出 assets/test.mcool 文件中的可用分辨率。")
        ]

        print("Message:", messages[0].content)
        print("-" * 60)

        # Invoke agent with config
        config = {
            "configurable": {
                "thread_id": "test-thread-001"
            }
        }

        print("Invoking agent...")
        response = agent.invoke({"messages": messages}, config=config)

        print("\n" + "=" * 60)
        print("Agent Response:")
        print("=" * 60)
        print(response)

        # Get the final message
        if hasattr(response, 'messages') and len(response['messages']) > 0:
            last_message = response['messages'][-1]
            print("\nFinal Answer:")
            print(last_message.content)

        return True

    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_agent_with_config()
    sys.exit(0 if result else 1)
