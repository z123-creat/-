"""
生成测试用的 mcool 文件（多分辨率 + 平衡权重）
使用 cooler 库正确创建多分辨率文件
"""
import numpy as np
import pandas as pd
import cooler
import os

def generate_test_mcool(output_path="assets/complete_test.mcool"):
    """
    生成一个包含多分辨率和平衡权重的测试 mcool 文件
    """
    print(f"正在生成 mcool 文件: {output_path}")
    print("=" * 70)

    # 删除旧文件
    if os.path.exists(output_path):
        os.remove(output_path)

    # 定义基因组信息
    chrom_sizes = {
        'chr1': 50000000,   # 50 Mb
        'chr2': 40000000,   # 40 Mb
        'chr3': 30000000    # 30 Mb
    }

    resolutions = [10000, 5000, 1000]

    print(f"染色体: {list(chrom_sizes.keys())}")
    print(f"分辨率: {resolutions} bp")
    print("-" * 70)

    # 为每个分辨率创建临时 cooler 文件
    temp_files = {}

    for resolution in resolutions:
        print(f"\n处理分辨率: {resolution} bp")
        print("-" * 70)

        # 生成 bins
        bins = []
        bin_id = 0
        for chrom, size in chrom_sizes.items():
            num_bins = (size + resolution - 1) // resolution
            for i in range(num_bins):
                start = i * resolution
                end = min(start + resolution, size)
                bins.append({
                    'chrom': chrom,
                    'start': start,
                    'end': end
                })
                bin_id += 1

        bins_df = pd.DataFrame(bins)

        # 生成像素（接触点）
        pixels = []

        # 1. 染色体内的接触（较多）
        for chrom, size in chrom_sizes.items():
            chrom_bins = bins_df[bins_df['chrom'] == chrom]
            chrom_bins_idx = chrom_bins.index.values

            # 对角线附近的接触较多
            for i, bin1_idx in enumerate(chrom_bins_idx[:500]):  # 限制数量
                for j, bin2_idx in enumerate(chrom_bins_idx[:500]):
                    if j >= i:
                        # 距离越近，接触概率越大
                        distance = abs(i - j)
                        if distance > 100:
                            continue

                        # 模拟接触频率（距离越近，接触越多）
                        count = np.random.poisson(100 / (distance + 1))

                        if count > 0:
                            pixels.append({
                                'bin1_id': bin1_idx,
                                'bin2_id': bin2_idx,
                                'count': count
                            })

        # 2. 染色体间接触（较少）
        for chrom1 in chrom_sizes.keys():
            for chrom2 in chrom_sizes.keys():
                if chrom1 >= chrom2:
                    continue

                bins1 = bins_df[bins_df['chrom'] == chrom1]
                bins2 = bins_df[bins_df['chrom'] == chrom2]

                # 生成一些染色体间接触
                for _ in range(min(50, len(bins1) * len(bins2) // 100000)):
                    bin1 = np.random.choice(bins1.index.values)
                    bin2 = np.random.choice(bins2.index.values)
                    count = np.random.poisson(10)
                    if count > 0:
                        pixels.append({
                            'bin1_id': bin1,
                            'bin2_id': bin2,
                            'count': count
                        })

        pixels_df = pd.DataFrame(pixels)

        # 创建临时 cooler 文件
        temp_file = f"temp_{resolution}.cool"
        cooler.create_cooler(
            temp_file,
            bins_df,
            pixels_df
        )

        # 平衡校正
        print(f"  - 执行平衡校正...")
        clr = cooler.Cooler(temp_file)
        try:
            cooler.balance_cooler(clr, cis_only=True, ignore_diags=2, store=True)
            print(f"  ✓ 平衡校正完成")
        except Exception as e:
            print(f"  ✗ 平衡校正失败: {e}")

        temp_files[resolution] = temp_file

    # 将所有分辨率合并到一个 mcool 文件
    print(f"\n合并所有分辨率到 mcool 文件...")
    print("-" * 70)

    cooler.create_cooler(
        output_path,
        bins_df,
        pixels_df,
        metadata={'format': 'mcool'}
    )

    # 使用 cooler.util.merge 或直接拷贝数据
    # 对于多分辨率 mcool，我们需要手动将每个分辨率的数据添加到 resolutions 组中

    import h5py
    with h5py.File(output_path, 'a') as f:
        # 删除默认的分辨率数据（如果是空的）
        if 'bins' in f:
            del f['bins']
        if 'pixels' in f:
            del f['pixels']

        # 创建 resolutions 组（如果不存在）
        if 'resolutions' not in f:
            res_group = f.create_group('resolutions')
        else:
            res_group = f['resolutions']

        # 添加每个分辨率
        for resolution, temp_file in temp_files.items():
            print(f"  - 添加分辨率 {resolution} bp...")
            with h5py.File(temp_file, 'r') as temp_f:
                # 复制所有数据到 resolutions/{resolution}
                res_str = str(resolution)
                if res_str not in res_group:
                    # 创建新的分辨率组
                    temp_f.copy(temp_f['/'], res_group, name=res_str)
                else:
                    # 如果已存在，跳过
                    print(f"    (分辨率 {resolution} 已存在，跳过)")

    # 删除临时文件
    for resolution, temp_file in temp_files.items():
        os.remove(temp_file)

    print(f"\n✓ 文件创建完成: {output_path}")

    # 检查文件大小
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  文件大小: {file_size_mb:.2f} MB")

    if file_size_mb > 500:
        print(f"  ✗ 文件大小超过 500 MB 限制")
        os.remove(output_path)
        return False
    else:
        print(f"  ✓ 文件大小符合要求")

    # 验证文件
    print(f"\n{'=' * 70}")
    print(f"验证 mcool 文件")
    print(f"{'=' * 70}")

    try:
        import h5py
        with h5py.File(output_path, 'r') as f:
            if 'resolutions' not in f:
                print(f"✗ 文件不包含 resolutions 组")
                return False

            resolutions_group = f['resolutions']
            print(f"\n✓ 文件格式验证通过")
            print(f"\n可用的分辨率:")

            for res_key in sorted(resolutions_group.keys(), key=int):
                res = int(res_key)
                res_group = resolutions_group[res_key]

                # 检查 bins 表
                if 'bins' in res_group:
                    bins_group = res_group['bins']
                    chroms = []

                    # 获取染色体列表
                    if 'chrom' in bins_group:
                        chroms_dataset = bins_group['chrom']
                        # 尝试不同的方式读取染色体数据
                        try:
                            if hasattr(chroms_dataset, 'asstr'):
                                chroms = list(set(chroms_dataset.asstr()[:].tolist()))
                            elif hasattr(chroms_dataset, 'asstr_ref'):
                                # 对于 reference 编码的数据
                                ref = chroms_dataset.dtype.fields['chrom'][5]
                                chrom_dtype = h5py.check_vlen_dtype(chroms_dataset.dtype)
                                if chrom_dtype.kind == 'S':
                                    chroms = list(set([c.decode() for c in chroms_dataset[:]]))
                                else:
                                    chroms = list(set(chroms_dataset[:].tolist()))
                            else:
                                # 直接读取
                                chroms_raw = chroms_dataset[:]
                                if chroms_raw.dtype.kind == 'S':
                                    chroms = list(set([c.decode() if isinstance(c, bytes) else c for c in chroms_raw]))
                                else:
                                    chroms = list(set(chroms_raw.tolist()))
                        except Exception as e:
                            print(f"    警告: 无法读取染色体信息: {e}")
                            chroms = ['chr1', 'chr2', 'chr3']  # 默认值

                    total_bins = len(bins_group['chrom']) if 'chrom' in bins_group else 0

                    # 检查平衡权重
                    has_balance = 'weight' in bins_group
                    balance_status = "✓ 包含平衡权重 (bins/weight)" if has_balance else "✗ 缺少平衡权重"

                    # 计算稀疏度
                    if 'pixels' in res_group:
                        pixel_count = len(res_group['pixels']['bin1_id'])
                        sparsity = 1.0 - (pixel_count / (total_bins * total_bins))
                        sparsity_str = f"{sparsity * 100:.2f}%"
                    else:
                        sparsity_str = "N/A"

                    print(f"  - {res} bp")
                    print(f"    染色体: {sorted(list(chroms))}")
                    print(f"    总 bins: {total_bins}")
                    print(f"    {balance_status}")
                    print(f"    chr1 矩阵稀疏度: {sparsity_str}")
                    print()

        return True

    except Exception as e:
        print(f"✗ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = generate_test_mcool()
    if success:
        print("\n✓ mcool 文件生成成功！")
    else:
        print("\n✗ mcool 文件生成失败！")
