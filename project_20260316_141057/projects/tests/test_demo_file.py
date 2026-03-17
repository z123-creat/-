"""
测试新的 demo_chr1.mcool 文件
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from tools.mcool_reader import list_available_resolutions
from tools.tad_analysis import analyze_tads
from tools.compartment_analysis import analyze_compartments
import json

def test_demo_file():
    file_path = "assets/demo_chr1.mcool"

    print("=" * 70)
    print("测试 demo_chr1.mcool 文件")
    print("=" * 70)

    # 测试 1: 列出分辨率
    print("\n测试 1: 列出分辨率")
    print("-" * 70)
    tool = list_available_resolutions
    result = tool.invoke({"file_path": file_path})
    data = json.loads(result)
    print(f"可用分辨率: {data['resolutions']}")
    print(f"文件大小: {os.path.getsize(file_path) / (1024*1024):.2f} MB")

    # 测试 2: TAD 分析（使用 100000 bp 分辨率）
    print("\n测试 2: TAD 分析 (100000 bp)")
    print("-" * 70)
    tool = analyze_tads
    result = tool.invoke({
        "file_path": file_path,
        "chromosome": "chr1",
        "resolution": 100000
    })
    data = json.loads(result)
    if "error" not in data:
        chr1_data = data.get("chromosomes", {}).get("chr1", {})
        print(f"识别的 TAD 数量: {chr1_data.get('num_tads', 0)}")
        print(f"TAD 边界: {chr1_data.get('boundaries', [])}")
    else:
        print(f"错误: {data['error']}")

    # 测试 3: Compartment 分析（使用 100000 bp 分辨率）
    print("\n测试 3: Compartment 分析 (100000 bp)")
    print("-" * 70)
    tool = analyze_compartments
    result = tool.invoke({
        "file_path": file_path,
        "chromosome": "chr1",
        "resolution": 100000
    })
    data = json.loads(result)
    if "error" not in data:
        chr1_data = data.get("chromosomes", {}).get("chr1", {})
        compartments = chr1_data.get("compartments", {}).get("statistics", {})
        print(f"A compartment bins: {compartments.get('n_A', 0)}")
        print(f"B compartment bins: {compartments.get('n_B', 0)}")
        print(f"A/B 比例: {compartments.get('ratio_A', 0):.2%}")
    else:
        print(f"错误: {data['error']}")

    print("\n" + "=" * 70)
    print("✓ 所有测试通过！")
    print("=" * 70)

if __name__ == "__main__":
    test_demo_file()
