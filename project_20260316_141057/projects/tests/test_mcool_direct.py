"""
直接测试工具，验证新生成的 mcool 文件
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from tools.mcool_reader import list_available_resolutions
from tools.tad_analysis import analyze_tads
from tools.compartment_analysis import analyze_compartments

def test_mcool_file():
    file_path = "assets/complete_test.mcool"

    print("=" * 70)
    print("测试 1: 列出分辨率")
    print("=" * 70)
    tool = list_available_resolutions
    result = tool.invoke({"file_path": file_path})
    print(result)
    print()

    print("=" * 70)
    print("测试 2: TAD 分析")
    print("=" * 70)
    tool = analyze_tads
    result = tool.invoke({"file_path": file_path, "chromosome": "chr1", "resolution": 10000})
    print(result)
    print()

    print("=" * 70)
    print("测试 3: Compartment 分析")
    print("=" * 70)
    tool = analyze_compartments
    result = tool.invoke({"file_path": file_path, "chromosome": "chr1", "resolution": 10000})
    print(result)
    print()

    print("✓ 所有测试通过！")

if __name__ == "__main__":
    test_mcool_file()
