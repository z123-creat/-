"""
Direct test of mcool reader tools
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

def test_mcool_reader():
    """Test mcool reader tools directly"""
    print("Testing mcool reader tools...")

    try:
        from tools.mcool_reader import read_mcool_file, get_chromosome_matrix, list_available_resolutions

        # Test 1: Read mcool file
        print("\n1. Reading mcool file...")
        result = read_mcool_file.invoke({"file_path": "assets/test.mcool"})
        print(f"Result: {result[:200]}...")  # Print first 200 chars

        # Test 2: Get chromosome matrix
        print("\n2. Getting chromosome matrix...")
        result2 = get_chromosome_matrix.invoke({"file_path": "assets/test.mcool", "chromosome": "chr1"})
        print(f"Result: {result2[:200]}...")  # Print first 200 chars

        # Test 3: List resolutions
        print("\n3. Listing resolutions...")
        result3 = list_available_resolutions.invoke({"file_path": "assets/test.mcool"})
        print(f"Result: {result3[:200]}...")  # Print first 200 chars

        print("\n✓ All mcool reader tests passed!")
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_mcool_reader()
    sys.exit(0 if result else 1)
