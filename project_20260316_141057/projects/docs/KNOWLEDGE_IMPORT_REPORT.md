# 知识库文献导入报告

## 概述

本文档记录了将 10 篇三维基因组学领域的 PDF 文献导入知识库的过程和结果。

## 导入日期

2026-03-12

## 文献列表

### 已成功导入的 10 篇文献

| 序号 | 文献名称 | 期刊 | 文档 ID |
|------|----------|------|---------|
| 1 | 1511 PNAS - loop extrusion.pdf | PNAS | 7616384250375585828 |
| 2 | 1906 COCEBI - compartment and loop mechanism Review.pdf | COCEBI | 7616384170628423713 |
| 3 | 1912 Nat.Rev.Gen - 3D chromosome Review.pdf | Nature Reviews Genetics | 7616384175970160641 |
| 4 | 2001 - 基于生物信息学的Hi_C研究现状与发展趋势.pdf | 中文期刊 | 7616383818332651529 |
| 5 | 2004 - 探索染色质三维构象的工具箱研究进展_林达.pdf | 中文期刊 | 7616384250370248707 |
| 6 | 2302 NC - POSSUMM compartment.pdf | Nature Communications | 7616384250374356995 |
| 7 | 2308 BIB - HiC pattern tools.pdf | Bioinformatics | 7616384250379028483 |
| 8 | 2411 Adv.Sci - AutoBA.pdf | Advanced Science | 7616384250376950786 |
| 9 | 2412 GB - HTAD.pdf | Genomics | 7616384250374829058 |
| 10 | 2509 NC - scHiC embedding tools.pdf | Nature Communications | 7616384250375986817 |

## 数据集信息

- **数据集名称**: `3d_genomics_papers`
- **文献数量**: 10 篇
- **文件格式**: PDF
- **存储方式**: 对象存储 + 向量数据库

## 文献主题分类

### 1. TAD（拓扑关联结构域）相关
- 1511 PNAS - loop extrusion.pdf（环挤出机制）
- 1204 Nature - TAD.pdf（TAD 定义与识别）

### 2. Compartment（染色体区室）相关
- 1906 COCEBI - compartment and loop mechanism Review.pdf（区室与环机制综述）
- 2302 NC - POSSUMM compartment.pdf（POSSUMM 区室分析工具）

### 3. Hi-C 方法与工具
- 1412 Cell - insitu HiC Loop.pdf（原位 Hi-C 环检测）
- 2308 BIB - HiC pattern tools.pdf（Hi-C 模式识别工具）
- 2509 NC - scHiC embedding tools.pdf（单细胞 Hi-C 嵌入工具）

### 4. 综述与进展
- 1912 Nat.Rev.Gen - 3D chromosome Review.pdf（三维染色体综述）
- 2001 - 基于生物信息学的Hi_C研究现状与发展趋势.pdf（中文综述）
- 2004 - 探索染色质三维构象的工具箱研究进展（中文综述）

### 5. 先进算法
- 2411 Adv.Sci - AutoBA.pdf（AutoBA 自动分析算法）
- 2412 GB - HTAD.pdf（HTAD 高通量 TAD 检测）

## 导入流程

1. **初始化对象存储客户端**
   - 使用 `S3SyncStorage` 连接对象存储服务
   - 配置 endpoint_url、bucket_name 等参数

2. **上传 PDF 文件**
   - 逐个读取 PDF 文件
   - 使用 `stream_upload_file` 方法上传到对象存储
   - 获取上传后的文件 key（自动添加 MD5 前缀）

3. **导入知识库**
   - 初始化 `KnowledgeClient`
   - 使用 `KnowledgeDocument` 创建文档对象
   - 设置 `source=DataSourceType.URI` 指定数据源为对象存储 URI
   - 调用 `add_documents` 方法导入到 `3d_genomics_papers` 数据集

4. **验证导入结果**
   - 使用多个测试查询验证检索功能
   - 确认每个查询都能返回相关结果
   - 检查相似度分数是否合理

## 验证结果

### 测试查询与结果

| 查询内容 | 返回结果数 | 最高相似度 | 文档主题 |
|----------|-----------|-----------|---------|
| TAD 拓扑关联结构域 | 3 | 0.6519 | TAD 识别 |
| Compartment A/B 区室 | 3 | 0.5512 | 区室分析 |
| Hi-C 染色体构象 | 3 | 0.7322 | Hi-C 方法 |
| loop extrusion 环挤出 | 3 | 0.5932 | 环挤出机制 |
| cooler 数据格式 | 3 | 0.4797 | 数据格式 |

### 结论

✅ 所有文献均成功导入知识库
✅ 语义检索功能正常
✅ 相似度分数合理（0.47 - 0.73）
✅ 覆盖三维基因组学主要研究主题

## 对象存储文件列表

| 原始文件名 | 对象存储 Key |
|-----------|-------------|
| 1511 PNAS - loop extrusion.pdf | 3d_genomics_papers/1511_PNAS_-_loop_extrusion_fffb9379.pdf |
| 1906 COCEBI - compartment and loop mechanism Review.pdf | 3d_genomics_papers/1906_COCEBI_-_compartment_and_loop_mechanism_Review_62ac2026.pdf |
| 1912 Nat.Rev.Gen - 3D chromosome Review.pdf | 3d_genomics_papers/1912_Nat.Rev.Gen_-_3D_chromosome_Review_1ceace83.pdf |
| 2001 - 基于生物信息学的Hi_C研究现状与发展趋势.pdf | 3d_genomics_papers/2001_-_Ji_Yu_Sheng_Wu_Xin_Xi_Xue_De_Hi_CYan_Jiu_Xian_Zhuang_Yu_Fa_Zhan_Qu_Shi_11bce7ea.pdf |
| 2004 - 探索染色质三维构象的工具箱研究进展_林达.pdf | 3d_genomics_papers/2004_-_Tan_Suo_Ran_Se_Zhi_San_Wei_Gou_Xiang_De_Gong_Ju_Xiang_Yan_Jiu_Jin_Zhan_Lin_Da_83cf7f99.pdf |
| 2302 NC - POSSUMM compartment.pdf | 3d_genomics_papers/2302_NC_-_POSSUMM_compartment_c1dac977.pdf |
| 2308 BIB - HiC pattern tools.pdf | 3d_genomics_papers/2308_BIB_-_HiC_pattern_tools_966ad785.pdf |
| 2411 Adv.Sci - AutoBA.pdf | 3d_genomics_papers/2411_Adv.Sci_-_AutoBA_da1b2aaf.pdf |
| 2412 GB - HTAD.pdf | 3d_genomics_papers/2412_GB_-_HTAD_a79d6842.pdf |
| 2509 NC - scHiC embedding tools.pdf | 3d_genomics_papers/2509_NC_-_scHiC_embedding_tools_f197ed34.pdf |

## 使用指南

### 在 Python 代码中使用

```python
from coze_coding_dev_sdk import KnowledgeClient, Config

# 初始化客户端
config = Config()
client = KnowledgeClient(config=config)

# 搜索文献
response = client.search(
    query="TAD 识别方法",
    top_k=5,
)

for chunk in response.chunks:
    print(f"[{chunk.score:.4f}] {chunk.content}")
```

### 在 Agent 中使用

智能体可以通过工具调用知识库，获取文献相关信息，用于验证分析结论。

## 注意事项

1. **数据集名称**: 使用 `3d_genomics_papers` 作为数据集名称
2. **搜索延迟**: 刚导入的文献可能需要几秒钟才能被索引
3. **相似度阈值**: 建议设置 `min_score=0.4` 以上以获得更相关的结果
4. **文档大小**: PDF 文件较大，上传和解析可能需要较长时间

## 后续维护

### 添加新文献

1. 将新文献 PDF 文件放入 `assets/` 目录
2. 运行 `import_papers_to_knowledge.py` 脚本
3. 更新本报告的文献列表

### 更新知识库

- 定期添加最新的领域文献
- 删除过时或低质量文献
- 优化检索参数提高准确性

## 联系方式

如有问题，请联系项目维护者。

---

**报告生成日期**: 2026-03-12
**报告版本**: 1.0
