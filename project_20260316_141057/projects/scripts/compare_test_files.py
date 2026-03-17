"""
对比两个测试文件的使用情况
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from tools.mcool_reader import list_available_resolutions
from tools.tad_analysis import analyze_tads
import json

def compare_files():
    """对比两个测试文件"""
    files = [
        ("assets/complete_test.mcool", "模拟数据"),
        ("assets/demo_chr1.mcool", "真实数据 ⭐")
    ]

    print("=" * 70)
    print("测试数据文件对比")
    print("=" * 70)

    for file_path, description in files:
        print(f"\n{description}")
        print("-" * 70)
        print(f"文件: {file_path}")
        print(f"大小: {os.path.getsize(file_path) / (1024*1024):.2f} MB")

        # 列出分辨率
        tool = list_available_resolutions
        result = tool.invoke({"file_path": file_path})
        data = json.loads(result)
        print(f"分辨率: {data['resolutions']}")

        # TAD 分析（使用中等分辨率）
        res = 10000 if 10000 in data['resolutions'] else 100000
        tool = analyze_tads
        result = tool.invoke({
            "file_path": file_path,
            "chromosome": "chr1",
            "resolution": res
        })
        data = json.loads(result)

        if "error" not in data:
            chr1_data = data.get("chromosomes", {}).get("chr1", {})
            print(f"TAD 数量: {chr1_data.get('num_tads', 0)}")
            print(f"分辨率: {res} bp")

    print("\n" + "=" * 70)
    print("✓ 对比完成！")
    print("=" * 70)
    print("\n推荐使用:")
    print("  • 开发测试: assets/complete_test.mcool (小文件，快速)")
    print("  • 演示验证: assets/demo_chr1.mcool (真实数据，推荐)")

if __name__ == "__main__":
    compare_files()
