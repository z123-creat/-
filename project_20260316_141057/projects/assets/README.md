# 测试数据文件说明

本目录包含用于测试三维基因组分析智能体的 mcool 格式 Hi-C 数据文件。

---

## 📁 文件列表

### 1. complete_test.mcool（模拟数据）
- **文件大小**: 0.58 MB
- **创建方式**: 使用 `scripts/generate_mcool.py` 生成
- **分辨率**: 1000 bp, 5000 bp, 10000 bp
- **染色体**: chr1, chr2, chr3
- **特点**:
  - 小文件，适合快速测试
  - 包含平衡权重
  - 模拟数据，结构简单

### 2. demo_chr1.mcool（真实数据）⭐ 推荐
- **文件大小**: 5.37 MB
- **来源**: 真实 Hi-C 数据
- **分辨率**: 10000 bp, 100000 bp, 1000000 bp
- **染色体**: chr1
- **特点**:
  - 真实数据，更贴近实际应用
  - 包含平衡权重
  - TAD 分析可识别 16 个 TAD
  - 更高分辨率选项

---

## 🔍 文件对比

| 特性 | complete_test.mcool | demo_chr1.mcool |
|------|---------------------|-----------------|
| 文件大小 | 0.58 MB | 5.37 MB |
| 数据类型 | 模拟数据 | 真实数据 |
| 分辨率数量 | 3 | 3 |
| 分辨率范围 | 1kb - 10kb | 10kb - 1Mb |
| 染色体数量 | 3 | 1 |
| TAD 数量 | 2 | 16 |
| 适用场景 | 快速测试、功能验证 | 真实分析、性能测试 |

---

## 🚀 使用建议

### 快速测试（开发阶段）
```python
# 使用小文件快速测试
file_path = "assets/complete_test.mcool"
```

### 真实分析（演示/验证）
```python
# 使用真实数据进行演示
file_path = "assets/demo_chr1.mcool"
```

### 分辨率选择

#### complete_test.mcool
- **1000 bp**: 精细结构分析
- **5000 bp**: 标准 TAD 分析
- **10000 bp**: 大尺度结构

#### demo_chr1.mcool
- **10000 bp**: 高精度分析（2,4896 bins）
- **100000 bp**: 标准 TAD 分析（2,490 bins，推荐）
- **1000000 bp**: 染色体级分析（249 bins）

---

## 📊 测试结果示例

### demo_chr1.mcool @ 100000 bp

#### TAD 分析结果
```json
{
  "chromosome": "chr1",
  "resolution": 100000,
  "num_tads": 16,
  "boundaries": [8, 1213, 1219, 1229, 1236, 1254, 1264, 1418, 1422, 1433, 1440, 1445, 1458, 1472, 1489]
}
```

#### 文件信息
- 总 bins: 2,490
- 总接触点: 843,096
- 包含平衡权重: ✓

---

## 🔧 工具调用示例

### 列出分辨率
```python
from tools.mcool_reader import list_available_resolutions

result = list_available_resolutions.invoke({
    "file_path": "assets/demo_chr1.mcool"
})
# 返回: [10000, 100000, 1000000]
```

### TAD 分析
```python
from tools.tad_analysis import analyze_tads

result = analyze_tads.invoke({
    "file_path": "assets/demo_chr1.mcool",
    "chromosome": "chr1",
    "resolution": 100000
})
# 识别 16 个 TAD
```

### Compartment 分析
```python
from tools.compartment_analysis import analyze_compartments

result = analyze_compartments.invoke({
    "file_path": "assets/demo_chr1.mcool",
    "chromosome": "chr1",
    "resolution": 100000
})
# 执行 PCA 分析
```

---

## 📝 生成新测试数据

如果需要生成新的测试数据，可以使用：

```bash
python scripts/generate_mcool.py
```

这将在 `assets/` 目录下生成新的 `complete_test.mcool` 文件。

---

## 🎯 推荐使用场景

1. **功能开发**: 使用 `complete_test.mcool`（快速反馈）
2. **性能测试**: 使用 `demo_chr1.mcool`（真实负载）
3. **用户演示**: 使用 `demo_chr1.mcool`（真实结果）
4. **文档示例**: 使用 `demo_chr1.mcool`（更有说服力）

---

**最后更新**: 2026-03-09
