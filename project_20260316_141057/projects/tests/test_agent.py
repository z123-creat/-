"""
Test script for 3D genome analysis agent
"""
import os
import sys

# Add the workspace to the Python path
workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from agents.agent import build_agent

def test_agent_initialization():
    """Test that the agent can be initialized"""
    print("Testing agent initialization...")

    try:
        agent = build_agent()
        print("✓ Agent initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Agent initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_tools_import():
    """Test that all tools can be imported"""
    print("\nTesting tools import...")

    try:
        from tools.mcool_reader import read_mcool_file, get_chromosome_matrix, list_available_resolutions
        from tools.tad_analysis import analyze_tads
        from tools.compartment_analysis import analyze_compartments
        from tools.knowledge_search import search_literature, get_literature_context
        from tools.analysis_history import save_analysis_record, search_analysis_history, get_analysis_record

        print("✓ All tools imported successfully")
        print(f"  - read_mcool_file: {read_mcool_file.name}")
        print(f"  - get_chromosome_matrix: {get_chromosome_matrix.name}")
        print(f"  - list_available_resolutions: {list_available_resolutions.name}")
        print(f"  - analyze_tads: {analyze_tads.name}")
        print(f"  - analyze_compartments: {analyze_compartments.name}")
        print(f"  - search_literature: {search_literature.name}")
        print(f"  - get_literature_context: {get_literature_context.name}")
        print(f"  - save_analysis_record: {save_analysis_record.name}")
        print(f"  - search_analysis_history: {search_analysis_history.name}")
        print(f"  - get_analysis_record: {get_analysis_record.name}")

        return True
    except Exception as e:
        print(f"✗ Tools import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_config_file():
    """Test that the config file exists and is valid"""
    print("\nTesting config file...")

    config_path = os.path.join(workspace_path, "config", "agent_llm_config.json")

    if not os.path.exists(config_path):
        print(f"✗ Config file not found: {config_path}")
        return False

    try:
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)

        # Validate required fields
        required_fields = ["config", "sp", "tools"]
        for field in required_fields:
            if field not in cfg:
                print(f"✗ Missing required field in config: {field}")
                return False

        # Validate config object
        if "model" not in cfg["config"]:
            print("✗ Missing 'model' in config.config")
            return False

        print("✓ Config file is valid")
        print(f"  Model: {cfg['config']['model']}")
        print(f"  Temperature: {cfg['config']['temperature']}")
        print(f"  Tools count: {len(cfg['tools'])}")

        return True
    except Exception as e:
        print(f"✗ Config file validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("3D Genome Analysis Agent - Test Suite")
    print("=" * 60)

    tests = [
        ("Config File", test_config_file),
        ("Tools Import", test_tools_import),
        ("Agent Initialization", test_agent_initialization)
    ]

    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
