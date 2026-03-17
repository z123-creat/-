"""
分析 demo_chr1.mcool 的 TAD 数量
"""
import os
import sys

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from tools.tad_analysis import analyze_tads
import json

def analyze_tad_count():
    """分析 demo_chr1.mcool 的 TAD 数量"""
    file_path = "assets/demo_chr1.mcool"
    chromosome = "chr1"

    print("=" * 70)
    print("分析 demo_chr1.mcool 的 TAD 数量")
    print("=" * 70)

    # 先获取可用分辨率
    from tools.mcool_reader import list_available_resolutions
    tool = list_available_resolutions
    result = tool.invoke({"file_path": file_path})
    data = json.loads(result)

    print(f"\n文件信息:")
    print(f"  文件: {file_path}")
    print(f"  大小: {os.path.getsize(file_path) / (1024*1024):.2f} MB")
    print(f"  染色体: {chromosome}")
    print(f"  可用分辨率: {data['resolutions']}")

    print("\n" + "=" * 70)
    print("不同分辨率下的 TAD 分析结果")
    print("=" * 70)

    tool = analyze_tads

    # 对每个分辨率进行分析
    for resolution in data['resolutions']:
        print(f"\n分辨率: {resolution} bp")
        print("-" * 70)

        result = tool.invoke({
            "file_path": file_path,
            "chromosome": chromosome,
            "resolution": resolution
        })

        data = json.loads(result)

        if "error" not in data:
            chr1_data = data.get("chromosomes", {}).get("chr1", {})

            num_tads = chr1_data.get('num_tads', 0)
            boundaries = chr1_data.get('boundaries', [])
            matrix_shape = chr1_data.get('matrix_shape', [0, 0])
            insulation_stats = chr1_data.get('insulation_score_stats', {})

            print(f"  ✓ TAD 数量: {num_tads}")
            print(f"  ✓ TAD 边界: {boundaries}")
            print(f"  ✓ 矩阵形状: {matrix_shape[0]} x {matrix_shape[1]} bins")

            if insulation_stats:
                print(f"  ✓ 绝缘分数:")
                print(f"    - 均值: {insulation_stats.get('mean', 0):.4f}")
                print(f"    - 标准差: {insulation_stats.get('std', 0):.4f}")
                print(f"    - 最小值: {insulation_stats.get('min', 0):.4f}")
                print(f"    - 最大值: {insulation_stats.get('max', 0):.4f}")

            # 显示 TAD 详情（如果有）
            tads = chr1_data.get('tads', [])
            if tads and len(tads) <= 10:  # 只显示前 10 个
                print(f"  ✓ TAD 详情 (前 {min(len(tads), 10)} 个):")
                for i, tad in enumerate(tads[:10], 1):
                    start = tad.get('start_bin', 0)
                    end = tad.get('end_bin', 0)
                    size = tad.get('size_bins', 0)
                    mean_contacts = tad.get('mean_contacts', 0)
                    print(f"    TAD {i}: bins {start}-{end} (大小: {size}, 平均接触数: {mean_contacts:.2f})")

        else:
            print(f"  ✗ 错误: {data['error']}")

    print("\n" + "=" * 70)
    print("分析完成！")
    print("=" * 70)

    print("\n推荐分辨率:")
    print("  • 10000 bp: 高精度分析（适合精细结构）")
    print("  • 100000 bp: 标准 TAD 分析（推荐）")
    print("  • 1000000 bp: 大尺度分析（适合染色体级）")

if __name__ == "__main__":
    analyze_tad_count()
