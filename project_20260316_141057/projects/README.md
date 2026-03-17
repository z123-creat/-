# 三维基因组分析智能体

基于 LangChain 和 LangGraph 的三维基因组分析智能体，支持 mcool 格式 Hi-C 数据的 TAD 分析、Compartment 分析、文献知识库检索和历史记录管理。

## 📋 目录

- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [部署与使用](#部署与使用)
- [网页聊天界面](#网页聊天界面)
- [工作流程](#工作流程)
- [项目结构](#项目结构)
- [使用示例](#使用示例)
- [文档](#文档)
- [技术栈](#技术栈)

---

## 功能特性

### 核心分析功能
- ✅ **mcool 文件读取**: 支持多分辨率 Hi-C 数据文件
- ✅ **TAD 分析**: 拓扑关联结构域识别和分析
- ✅ **Compartment 分析**: A/B 区室识别和 PCA 分析
- ✅ **文献验证**: 基于知识库的结论验证

### 数据管理
- ✅ **多分辨率支持**: 自动检测和切换不同分辨率 (1000/5000/10000 bp)
- ✅ **平衡权重处理**: 支持未平衡数据
- ✅ **历史记录**: 分析结果保存和查询
- ✅ **短期记忆**: 多轮对话上下文管理

---

## 快速开始

### 1. 环境要求
- Python 3.12+
- 依赖包: 见 `requirements.txt`

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动智能体
```bash
python src/main.py
```

### 4. 测试工具
```bash
# 直接测试工具功能
python tests/test_mcool_direct.py

# 测试智能体
python tests/test_agent_mcool.py
```

---

## 🚀 部署与使用

### 部署方式

您的智能体可以通过以下方式部署：

#### 方式 1: Coze 平台部署（推荐）
在 Coze 平台上创建项目，上传代码，点击部署即可。详细步骤请参见：
👉 **[部署与使用指南](docs/DEPLOYMENT_GUIDE.md)**

#### 方式 2: 本地部署
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
bash scripts/http_run.sh -p 8000

# 3. 访问服务
http://localhost:8000
```

### 如何使用智能体

部署成功后，您可以通过以下方式与智能体交互：

#### 1. 访问域名（智能引导）⭐⭐⭐

**直接访问部署域名即可！**

```
https://gsn2v3kydv.coze.site
```

页面会自动：
- ✅ 检测服务配置
- ✅ 判断是否需要认证
- ✅ 自动跳转到聊天界面
- ✅ 无需手动配置

**详细使用说明**：👉 **[智能引导页面使用指南](docs/SMART_LANDING_GUIDE.md)**

#### 2. 使用本地聊天界面 💬
双击打开 **[docs/chat.html](docs/chat.html)** 或 **[docs/chat_with_apikey.html](docs/chat_with_apikey.html)**，输入您的 API 地址，即可开始对话！

#### 3. 使用 API 调用
```bash
curl -X POST https://your-api-url/run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "分析 assets/demo_chr1.mcool 的 TAD 结构"
      }
    ]
  }'
```

#### 3. 使用 OpenAI 兼容接口
智能体支持 OpenAI API 格式，可以使用任何支持 OpenAI 的工具。

详细使用说明请参见：**[部署与使用指南](docs/DEPLOYMENT_GUIDE.md)**

---

## 🌐 网页聊天界面

### 访问方式

#### 方式 1：访问域名（智能引导）⭐⭐⭐ 推荐

```
https://gsn2v3kydv.coze.site
```

访问域名后：
- 页面自动检测服务配置
- 如果不需要认证，自动跳转到聊天界面
- 如果需要认证，提示输入 Token
- 无需任何手动配置

**特点**：
- ✅ 智能检测，自动配置
- ✅ 一键分享链接给好友
- ✅ 支持公开访问和认证访问
- ✅ 流畅的用户体验
- ✅ 移动端适配

#### 方式 2：直接访问聊天界面

```
https://gsn2v3kydv.coze.site/chat
```

或带 Token：

```
https://gsn2v3kydv.coze.site/chat?token=YOUR_TOKEN
```

#### 方式 3：本地聊天界面

双击打开以下文件之一：

- **[docs/chat.html](docs/chat.html)** - 基础聊天界面
- **[docs/chat_with_apikey.html](docs/chat_with_apikey.html)** - 支持 API Key 的版本

#### 方式 4：API 调用

通过 RESTful API 调用智能体功能。

### 分享给好友

您可以轻松分享智能体给好友：

1. **直接分享域名**：
   ```
   https://gsn2v3kydv.coze.site
   ```
   好友打开后自动跳转，无需任何配置！

2. **带 Token 分享**（如需要）：
   ```
   https://gsn2v3kydv.coze.site/chat?token=YOUR_TOKEN
   ```
   ⚠️ 注意：Token 会暴露在 URL 中

3. **发布到社交平台**：
   - 在微博、Twitter 等平台发布链接
   - 其他用户点击链接即可访问

### 详细文档

- **[智能引导页面使用指南](docs/SMART_LANDING_GUIDE.md)** ⭐ - 智能检测和自动配置
- **[网页聊天界面使用指南](docs/CHAT_INTERFACE_GUIDE.md)** - 聊天界面详细说明

---

## 🔄 工作流程

智能体的完整工作流程如下：

```
用户输入 → 需求解析 → 工具调度 → 数据分析 → 知识验证 → 结果整合 → 输出报告
```

详细工作流请参见: [docs/workflow_preview.md](docs/workflow_preview.md)

### 典型分析场景

#### 场景 1: TAD 分析
1. 读取 mcool 文件
2. 执行 TAD 分析
3. 搜索文献验证
4. 生成分析报告

#### 场景 2: Compartment 分析
1. 获取接触矩阵
2. 执行 PCA 分析
3. 查询历史记录
4. 生成可视化报告

#### 场景 3: 多分辨率对比
1. 列出所有分辨率
2. 对每个分辨率执行分析
3. 对比不同分辨率的结果
4. 生成对比报告

---

## 项目结构

```
.
├── config/                      # 配置目录
│   └── agent_llm_config.json    # 智能体配置
├── docs/                        # 文档目录
│   ├── workflow_preview.md      # 工作流预览
│   ├── detailed_workflow.mmd    # 详细工作流图
│   └── PROJECT_SUMMARY.md       # 项目总结
├── scripts/                     # 脚本目录
│   ├── generate_mcool.py        # 生成测试数据
│   └── generate_workflow_preview.py  # 生成工作流预览
├── assets/                      # 资源目录
│   ├── complete_test.mcool      # 模拟测试数据
│   └── demo_chr1.mcool          # 真实测试数据 ⭐
├── src/                         # 源代码目录
│   ├── agents/                  # 智能体代码
│   │   └── agent.py             # 智能体主逻辑
│   ├── tools/                   # 工具定义
│   │   ├── mcool_reader.py      # mcool 文件读取
│   │   ├── tad_analysis.py      # TAD 分析
│   │   ├── compartment_analysis.py  # Compartment 分析
│   │   ├── knowledge_search.py  # 文献搜索
│   │   └── analysis_history.py  # 历史记录管理
│   ├── storage/                 # 存储初始化
│   ├── utils/                   # 工具函数
│   └── main.py                  # 运行入口
├── tests/                       # 测试目录
│   ├── test_mcool_direct.py     # 工具直接测试
│   └── test_agent_mcool.py      # 智能体测试
├── AGENT.md                     # 智能体规范
├── README.md                    # 项目说明 (本文件)
└── requirements.txt             # 依赖列表
```

---

## 使用示例

### 示例 1: TAD 分析（真实数据）

```python
from agents.agent import build_agent
from langchain_core.messages import HumanMessage

agent = build_agent()

# 使用真实数据分析
response = agent.invoke(
    {"messages": [HumanMessage(
        "分析 assets/demo_chr1.mcool 文件中 chr1 染色体的 TAD 结构，使用 100000 bp 分辨率"
    )]},
    config={"configurable": {"thread_id": "session-001"}}
)

print(response["messages"][-1].content)
# 输出: 识别 16 个 TAD
```

### 示例 2: Compartment 分析（真实数据）

```python
from agents.agent import build_agent
from langchain_core.messages import HumanMessage

agent = build_agent()

response = agent.invoke(
    {"messages": [HumanMessage(
        "分析 demo_chr1.mcool 中 chr1 的 A/B compartments，使用 100000 bp 分辨率"
    )]},
    config={"configurable": {"thread_id": "session-002"}}
)

print(response["messages"][-1].content)
```

### 示例 3: 快速测试（模拟数据）

```python
from agents.agent import build_agent
from langchain_core.messages import HumanMessage

agent = build_agent()

# 使用模拟数据快速测试
response = agent.invoke(
    {"messages": [HumanMessage(
        "分析 assets/complete_test.mcool 文件中 chr1 染色体的 TAD 结构"
    )]},
    config={"configurable": {"thread_id": "session-003"}}
)

print(response["messages"][-1].content)
```

### 示例 2: Compartment 分析

```python
from agents.agent import build_agent
from langchain_core.messages import HumanMessage

agent = build_agent()

response = agent.invoke(
    {"messages": [HumanMessage(
        "分析 chr1 的 A/B compartments，使用 10000 bp 分辨率"
    )]},
    config={"configurable": {"thread_id": "session-002"}}
)

print(response["messages"][-1].content)
```

### 示例 3: 直接调用工具

```python
from tools.tad_analysis import analyze_tads
import json

result = analyze_tads.invoke({
    "file_path": "assets/complete_test.mcool",
    "chromosome": "chr1",
    "resolution": 10000
})

data = json.loads(result)
print(f"识别的 TAD 数量: {data['chromosomes']['chr1']['num_tads']}")
```

---

## 工具列表

### 数据读取工具
| 工具 | 功能 | 参数 |
|------|------|------|
| `read_mcool_file` | 读取 mcool 文件 | file_path |
| `get_chromosome_matrix` | 获取接触矩阵 | file_path, chromosome, resolution |
| `list_available_resolutions` | 列出分辨率 | file_path |

### 分析工具
| 工具 | 功能 | 参数 |
|------|------|------|
| `analyze_tads` | TAD 分析 | file_path, chromosome, resolution |
| `analyze_compartments` | Compartment 分析 | file_path, chromosome, resolution |

### 知识和历史
| 工具 | 功能 | 参数 |
|------|------|------|
| `search_literature` | 文献搜索 | query, top_k |
| `save_analysis` | 保存分析 | analysis_data |
| `query_analysis_history` | 查询历史 | query_params |

---

## 📚 文档

### 快速开始
- **[智能引导页面快速开始](docs/QUICKSTART_SMART_LANDING.md)** 🚀 - 3 步开始使用

### 使用指南
- **[智能引导页面使用指南](docs/SMART_LANDING_GUIDE.md)** ⭐ - 智能检测和自动配置
- **[网页聊天界面使用指南](docs/CHAT_INTERFACE_GUIDE.md)** - 聊天界面详细说明
- **[部署与使用指南](docs/DEPLOYMENT_GUIDE.md)** - 如何部署和使用智能体
- **[网页聊天界面](docs/chat.html)** 💬 - 简单的网页聊天界面（双击打开）
- **[网页聊天界面（带 API Key）](docs/chat_with_apikey.html)** 💬 - 支持 API Key 的聊天界面

### 工作流程
- [工作流索引](docs/index_workflow.html) - 所有工作流图版本
- [工作流预览](docs/workflow_preview.md) - 详细的智能体工作流说明
- [版本对比](docs/VERSION_COMPARISON.md) - 不同版本工作流图的对比

### 项目文档
- [项目总结](docs/PROJECT_SUMMARY.md) - 项目交付物和功能清单
- [智能体规范](AGENT.md) - 智能体开发规范

### 测试数据
- [测试数据说明](assets/README.md) - 测试数据使用指南

---

## 测试数据

项目包含两个测试用的 mcool 文件：

### 1. complete_test.mcool（模拟数据）
- **文件大小**: 0.58 MB
- **分辨率**: 1000 bp, 5000 bp, 10000 bp
- **染色体**: chr1, chr2, chr3
- **平衡权重**: 所有分辨率都包含
- **特点**: 小文件，适合快速测试

### 2. demo_chr1.mcool（真实数据）⭐ 推荐
- **文件大小**: 5.37 MB
- **分辨率**: 10000 bp, 100000 bp, 1000000 bp
- **染色体**: chr1
- **平衡权重**: 所有分辨率都包含
- **特点**: 真实数据，识别 16 个 TAD

详细说明请参见: [assets/README.md](assets/README.md)

### 生成新的测试数据
```bash
python scripts/generate_mcool.py
```

### 测试新文件
```bash
python tests/test_demo_file.py
```

---

## 技术栈

- **框架**: LangChain 1.0, LangGraph
- **模型**: ChatOpenAI (多模态)
- **数据处理**: cooler, numpy, scipy, scikit-learn, h5py
- **文件格式**: HDF5 (mcool), JSON
- **知识库**: Coze Knowledge SDK
- **数据库**: Supabase (PostgreSQL)
- **开发语言**: Python 3.12

---

## 常见问题

### Q: 如何指定分析分辨率？
A: 使用 `list_available_resolutions` 查看可用分辨率，然后在分析工具中指定 `resolution` 参数。

### Q: 为什么有些分析返回空结果？
A: 可能是由于测试数据的限制。真实分析应使用完整的 Hi-C 数据。

### Q: 如何查看历史分析记录？
A: 使用 `query_analysis_history` 工具查询数据库中的历史记录。

### Q: 智能体支持哪些文件格式？
A: 当前支持 mcool 格式的 Hi-C 数据文件。

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

本项目采用 MIT 许可证。

---

**项目状态**: ✅ 已完成
**版本**: 1.0.0
**更新时间**: 2026-03-09
