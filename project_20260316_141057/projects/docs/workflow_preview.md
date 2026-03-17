# 三维基因组分析智能体工作流预览

## 🎯 智能体概述

**智能体名称**: 三维基因组分析智能体
**核心功能**: 基于 mcool 文件的 Hi-C 数据分析，支持 TAD 分析、Compartment 分析、文献验证和历史记录管理

---

## 🏗️ 系统架构

### 1. 核心组件

```
用户输入
    ↓
┌─────────────────────────────────────┐
│     智能体核心 (Agent Core)          │
│   • LangChain Agent                  │
│   • ChatOpenAI (多模态模型)          │
│   • MemorySaver (短期记忆)           │
│   • System Prompt (专业领域知识)     │
└──────────────┬──────────────────────┘
               │
    ┌──────────▼──────────┐
    │   工具调度器        │
    └──────┬──────────────┘
           │
    ┌──────▼─────────────────────────────────────┐
    │              工具层 (8 个工具)             │
    ├────────────────────────────────────────────┤
    │ 1️⃣ 数据读取工具                            │
    │    • read_mcool_file                       │
    │    • get_chromosome_matrix                 │
    │    • list_available_resolutions            │
    ├────────────────────────────────────────────┤
    │ 2️⃣ 分析工具                                │
    │    • analyze_tads (TAD 分析)               │
    │    • analyze_compartments (Compartment)    │
    ├────────────────────────────────────────────┤
    │ 3️⃣ 知识检索                                │
    │    • search_literature (文献搜索)          │
    ├────────────────────────────────────────────┤
    │ 4️⃣ 历史记录管理                            │
    │    • save_analysis (保存结果)              │
    │    • query_analysis_history (查询历史)     │
    └──────────────┬─────────────────────────────┘
                   │
    ┌──────────────▼──────────────────────────────┐
    │              数据层                          │
    ├──────────────────────────────────────────────┤
    │ • assets/complete_test.mcool (测试数据)     │
    │   - 3 个分辨率 (1000/5000/10000 bp)         │
    │   - 3 个染色体 (chr1/chr2/chr3)             │
    │   - 包含平衡权重                            │
    ├──────────────────────────────────────────────┤
    │ • 文献知识库 (3d_genomics_literature)       │
    │   - Science 论文                            │
    │   - Nature 论文                             │
    │   - Cell 论文                               │
    ├──────────────────────────────────────────────┤
    │ • 数据库 (analysis_history 表)              │
    │   - 存储分析历史记录                        │
    │   - 支持查询和复用                          │
    └──────────────┬──────────────────────────────┘
                   │
    ┌──────────────▼──────────────────────────────┐
    │              输出层                          │
    ├──────────────────────────────────────────────┤
    │ • Markdown 格式分析报告                     │
    │ • TAD 边界列表和统计信息                    │
    │ • Compartment 分配结果 (A/B)                │
    │ • 文献验证结论                              │
    └──────────────────────────────────────────────┘
```

---

## 🔄 典型工作流程

### 场景 1: TAD 分析流程

```
用户: "分析 chr1 染色体的 TAD 结构"
    ↓
1. Agent 解析需求 → 识别需要执行 TAD 分析
    ↓
2. 调用 read_mcool_file → 获取文件基本信息
    ↓
3. 调用 list_available_resolutions → 列出可用分辨率
    ↓
4. 调用 analyze_tads → 执行 TAD 分析
    • 读取接触矩阵 (balance=False)
    • 计算绝缘分数
    • 识别 TAD 边界
    • 计算统计信息
    ↓
5. 调用 search_literature → 搜索相关文献验证结论
    ↓
6. 调用 save_analysis → 保存分析结果到数据库
    ↓
7. Agent 整合所有结果 → 生成综合报告
    ↓
输出: TAD 分析报告
  • 识别的 TAD 数量
  • TAD 边界位置
  • 每个TAD的统计信息
  • 文献支持的结论
```

### 场景 2: Compartment 分析流程

```
用户: "分析 chr1 的 A/B compartments"
    ↓
1. Agent 解析需求 → 识别需要执行 Compartment 分析
    ↓
2. 调用 get_chromosome_matrix → 获取接触矩阵
    ↓
3. 调用 analyze_compartments → 执行 PCA 分析
    • 计算观察/期望矩阵
    • 执行主成分分析
    • 识别 A/B compartments
    • 计算统计信息
    ↓
4. 调用 query_analysis_history → 查找历史相似分析
    ↓
5. Agent 对比结果 → 验证一致性
    ↓
输出: Compartment 分析报告
  • A/B compartment 分配
  • 第一主成分 (PC1) 值
  • A/B 区室统计
  • 历史对比结果
```

### 场景 3: 多分辨率分析

```
用户: "比较不同分辨率下的 TAD 分析结果"
    ↓
1. Agent 识别需求 → 需要多分辨率对比
    ↓
2. 调用 list_available_resolutions → 获取所有分辨率
   → [1000 bp, 5000 bp, 10000 bp]
    ↓
3. 对每个分辨率执行 analyze_tads
   • 1000 bp: 高精度 TAD 识别
   • 5000 bp: 标准 TAD 识别
   • 10000 bp: 大尺度 TAD 识别
    ↓
4. Agent 整合多分辨率结果
    ↓
5. 调用 search_literature → 查找多分辨率分析最佳实践
    ↓
输出: 多分辨率对比报告
  • 不同分辨率下的 TAD 数量
  • 边界位置的一致性
  • 分辨率对 TAD 检测的影响
```

---

## 🧰 工具详情

### 数据读取工具

| 工具名称 | 功能 | 输入参数 | 输出 |
|---------|------|---------|------|
| `read_mcool_file` | 读取 mcool 文件基本信息 | file_path | JSON (文件信息) |
| `get_chromosome_matrix` | 获取指定染色体的接触矩阵 | file_path, chromosome, resolution | JSON (矩阵统计) |
| `list_available_resolutions` | 列出所有可用分辨率 | file_path | JSON (分辨率列表) |

### 分析工具

| 工具名称 | 功能 | 输入参数 | 输出 |
|---------|------|---------|------|
| `analyze_tads` | TAD 分析 | file_path, chromosome, resolution, window_size | JSON (TAD 信息) |
| `analyze_compartments` | Compartment 分析 | file_path, chromosome, resolution, use_gc_correction | JSON (Compartment 信息) |

### 知识检索

| 工具名称 | 功能 | 输入参数 | 输出 |
|---------|------|---------|------|
| `search_literature` | 搜索文献知识库 | query, top_k | JSON (文献片段) |

### 历史记录

| 工具名称 | 功能 | 输入参数 | 输出 |
|---------|------|---------|------|
| `save_analysis` | 保存分析结果 | analysis_data | JSON (保存状态) |
| `query_analysis_history` | 查询历史记录 | query_params | JSON (历史记录) |

---

## 📊 数据结构

### 输入数据 (mcool 文件)

```
assets/complete_test.mcool
├── resolutions/
│   ├── 1000/
│   │   ├── bins/ (125,000 bins)
│   │   │   ├── chrom (染色体)
│   │   │   ├── start/start_pos (起始位置)
│   │   │   ├── end/end_pos (结束位置)
│   │   │   └── weight (平衡权重) ✓
│   │   └── pixels/ (838,651 contacts)
│   │       ├── bin1_id
│   │       ├── bin2_id
│   │       └── count
│   ├── 5000/
│   │   ├── bins/ (25,000 bins)
│   │   │   └── weight (平衡权重) ✓
│   │   └── pixels/ (167,264 contacts)
│   └── 10000/
│       ├── bins/ (12,000 bins)
│       │   └── weight (平衡权重) ✓
│       └── pixels/ (83,831 contacts)
├── chroms/ (染色体信息)
└── indexes/ (索引)
```

### 输出数据 (分析报告)

```
TAD 分析报告:
{
  "chromosome": "chr1",
  "resolution": 10000,
  "num_tads": 2,
  "boundaries": [512],
  "tads": [
    {
      "tad_id": 1,
      "start_bin": 0,
      "end_bin": 512,
      "size_bins": 512,
      "mean_contacts": 1.72,
      "max_contact": 126,
      "diagonal_enrichment": 56.91
    }
  ],
  "insulation_score_stats": {
    "mean": 2.29,
    "std": 6.86,
    "min": 0.0,
    "max": 34.66
  }
}

Compartment 分析报告:
{
  "chromosome": "chr1",
  "resolution": 10000,
  "eigenvalue": 69.06,
  "explained_variance_ratio": 1.0,
  "compartments": {
    "assignments": [1, 1, 1, ..., -1, -1, -1],
    "statistics": {
      "n_A": 4857,
      "n_B": 143,
      "total_bins": 5000,
      "ratio_A": 0.97
    }
  }
}
```

---

## 🔍 关键技术点

### 1. 多分辨率支持
- 自动检测 mcool 文件中的分辨率组
- 支持用户指定分辨率或自动选择最高分辨率
- 每个分辨率独立进行平衡校正

### 2. 平衡权重处理
- 使用 `balance=False` 参数避免未平衡数据报错
- 使用 `np.nan_to_num()` 处理异常值 (inf/NaN)
- 确保数据稳定性

### 3. JSON 序列化
- 所有 numpy 类型显式转换为标准 Python 类型
- 确保工具输出可被 Agent 正确解析

### 4. 记忆管理
- 使用滑动窗口保留最近 40 条消息
- 支持多轮对话上下文
- 可扩展为长期记忆

---

## 📝 示例对话

### 对话 1: TAD 分析

```
用户: 请分析 assets/complete_test.mcool 文件中 chr1 染色体的 TAD 结构

智能体: 我来为您分析 chr1 染色体的 TAD 结构。

[工具调用] read_mcool_file(assets/complete_test.mcool)
[工具调用] analyze_tads(chr1, resolution=10000)
[工具调用] search_literature("TAD analysis chr1")

分析完成！

## TAD 分析结果

### 基本信息
- 染色体: chr1
- 分辨率: 10000 bp
- 矩阵形状: 5000 x 5000 bins

### TAD 结构
- 识别的 TAD 数量: 2 个
- TAD 边界: [512]

### TAD 详情
**TAD 1**
- 位置: bins 0-512 (0-5.12 Mb)
- 大小: 512 bins (5.12 Mb)
- 平均接触数: 1.72
- 最大接触数: 126
- 对角线富集: 56.91

**TAD 2**
- 位置: bins 512-5000 (5.12-50 Mb)
- 大小: 4488 bins (44.88 Mb)
- 平均接触数: 0.00
- 最大接触数: 0

### 文献验证
根据文献 [Dixon et al., 2012]，TAD 通常大小在 100kb - 1Mb 之间。
本分析中识别的 TAD 1 大小为 5.12 Mb，略大于典型范围，
可能是由于测试数据的简化导致。
```

### 对话 2: Compartment 分析

```
用户: 分析 chr1 的 A/B compartments

智能体: 我来为您分析 chr1 的 A/B compartments。

[工具调用] analyze_compartments(chr1, resolution=10000)

## Compartment 分析结果

### 基本信息
- 染色体: chr1
- 分辨率: 10000 bp
- 第一主成分特征值: 69.06
- 解释方差比: 100%

### Compartment 分配
- A compartment bins: 4857 (97.14%)
- B compartment bins: 143 (2.86%)

### 结论
chr1 染色体主要由 A compartment 组成，表明该染色体区域
主要处于转录活跃状态。B compartment 占比较小，对应于
转录抑制区域。
```

---

## 🚀 使用方式

### 1. 启动智能体

```bash
cd /workspace/projects
python src/main.py
```

### 2. 交互方式

```python
from agents.agent import build_agent
from langchain_core.messages import HumanMessage

agent = build_agent()

# 执行分析
response = agent.invoke(
    {"messages": [HumanMessage(content="分析 chr1 的 TAD 结构")]},
    config={"configurable": {"thread_id": "session-001"}}
)

print(response["messages"][-1].content)
```

### 3. 直接调用工具

```python
from tools.tad_analysis import analyze_tads
import json

# 调用 TAD 分析工具
result = analyze_tads.invoke({
    "file_path": "assets/complete_test.mcool",
    "chromosome": "chr1",
    "resolution": 10000
})

data = json.loads(result)
print(f"识别的 TAD 数量: {data['chromosomes']['chr1']['num_tads']}")
```

---

## 📌 注意事项

1. **文件路径**: 确保使用 `assets/` 目录下的文件路径
2. **分辨率**: 使用 `list_available_resolutions` 确认可用分辨率
3. **染色体名称**: 使用标准格式 (chr1, chr2, chr3)
4. **数据质量**: 测试数据为模拟数据，真实分析需使用真实 Hi-C 数据

---

## 🔧 技术栈

- **框架**: LangChain 1.0, LangGraph
- **模型**: ChatOpenAI (支持多模态)
- **数据处理**: cooler, numpy, scipy, scikit-learn
- **文件格式**: HDF5 (mcool), JSON
- **知识库**: Coze Knowledge SDK
- **数据库**: Supabase (PostgreSQL)

---

## 📚 相关文献

智能体知识库包含以下文献：

1. **Dixon et al., 2012 (Nature)** - Topological domains in mammalian genomes identified by analysis of chromatin interactions
2. **Lieberman-Aiden et al., 2009 (Science)** - Comprehensive mapping of long-range interactions reveals folding principles of the human genome
3. **Rao et al., 2014 (Cell)** - A 3D map of the human genome at kilobase resolution reveals principles of chromatin looping

---

*生成时间: 2026-03-09*
*版本: 1.0.0*
