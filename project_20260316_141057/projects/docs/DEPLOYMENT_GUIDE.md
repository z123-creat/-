# 三维基因组分析智能体 - 部署与使用指南

## 📋 目录
- [部署方式](#部署方式)
- [访问智能体](#访问智能体)
- [使用方式](#使用方式)
- [API 接口说明](#api-接口说明)
- [常见问题](#常见问题)

---

## 🚀 部署方式

### 方式 1: Coze 平台部署（推荐）

您的项目已经配置好，可以直接在 Coze 平台上部署。

#### 部署步骤

1. **在 Coze 平台创建项目**
   - 登录 [Coze 平台](https://www.coze.cn/)
   - 创建新的工作空间或项目
   - 上传您的代码

2. **配置部署**
   - 入口文件：`src/main.py`
   - 运行命令：自动执行 `scripts/http_run.sh -p 8000`
   - 端口：8000（默认）

3. **启动服务**
   - 点击部署按钮
   - 等待服务启动完成
   - Coze 会分配一个访问 URL（类似：`https://xxxxx.coze.site`）

#### 部署后的访问地址

部署成功后，Coze 会提供一个访问 URL，格式如：
```
https://gsn2v3kydv.coze.site
```

---

### 方式 2: 本地部署

您也可以在本地机器上运行这个智能体。

#### 环境要求
- Python 3.12+
- 依赖包：见 `requirements.txt`

#### 部署步骤

1. **安装依赖**
```bash
cd /workspace/projects
pip install -r requirements.txt
```

2. **启动服务**
```bash
# 方式 1: 使用脚本（推荐）
bash scripts/http_run.sh -p 8000

# 方式 2: 直接运行
python src/main.py -m http -p 8000
```

3. **访问服务**
```
http://localhost:8000
```

---

## 📍 访问智能体

### 部署成功后的访问位置

部署成功后，您可以通过以下方式访问智能体：

#### 1. **API 接口访问**（主要方式）

智能体通过 HTTP API 提供服务，不是通过网页界面。

**基础 URL**：
- **Coze 部署**：`https://xxxxx.coze.site`
- **本地部署**：`http://localhost:8000`

#### 2. **可用的 API 端点**

| 端点 | 方法 | 描述 |
|------|------|------|
| `/run` | POST | 同步运行智能体 |
| `/stream_run` | POST | 流式运行智能体（推荐） |
| `/v1/chat/completions` | POST | OpenAI 兼容接口 |
| `/health` | GET | 健康检查 |
| `/cancel/{run_id}` | POST | 取消运行 |

#### 3. **没有网页聊天界面**

⚠️ **重要提示**：
- 这个智能体**没有提供网页聊天界面**
- 需要通过 **API 调用**来使用
- 或者使用支持 OpenAI API 的客户端

---

## 💬 使用方式

### 方式 1: 使用 curl 命令

#### 基础查询
```bash
curl -X POST https://xxxxx.coze.site/run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "分析 assets/demo_chr1.mcool 文件中 chr1 染色体的 TAD 结构"
      }
    ]
  }'
```

#### 流式响应（推荐）
```bash
curl -X POST https://xxxxx.coze.site/stream_run \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "分析 demo_chr1.mcool 中的 TAD 结构"
      }
    ]
  }'
```

---

### 方式 2: 使用 Python 代码

#### 同步调用
```python
import requests

# 替换为您的部署地址
BASE_URL = "https://xxxxx.coze.site"  # 或 "http://localhost:8000"

response = requests.post(
    f"{BASE_URL}/run",
    json={
        "messages": [
            {
                "role": "user",
                "content": "分析 assets/demo_chr1.mcool 文件中 chr1 染色体的 TAD 结构"
            }
        ]
    }
)

print(response.json())
```

#### 流式调用（推荐）
```python
import requests
import json

BASE_URL = "https://xxxxx.coze.site"

response = requests.post(
    f"{BASE_URL}/stream_run",
    json={
        "messages": [
            {
                "role": "user",
                "content": "分析 demo_chr1.mcool 中的 TAD 结构"
            }
        ]
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        line_str = line.decode('utf-8')
        if line_str.startswith('data:'):
            data = json.loads(line_str[5:])
            print(data.get('content', ''), end='', flush=True)
```

---

### 方式 3: 使用 OpenAI 兼容接口

智能体提供了 OpenAI 兼容的 API，可以使用任何支持 OpenAI 的工具。

#### 使用 OpenAI Python SDK
```python
from openai import OpenAI

# 配置客户端
client = OpenAI(
    api_key="any",  # 任意值即可
    base_url="https://xxxxx.coze.site/v1"
)

# 调用智能体
response = client.chat.completions.create(
    model="agent",
    messages=[
        {
            "role": "user",
            "content": "分析 demo_chr1.mcool 中的 TAD 结构"
        }
    ]
)

print(response.choices[0].message.content)
```

#### 使用支持 OpenAI 的工具
- ChatGPT-Next-Web
- Open WebUI
- Cursor
- Continue
- 任何支持自定义 base_url 的 OpenAI 客户端

---

### 方式 4: 创建简单的聊天界面

如果您想要一个网页聊天界面，可以创建一个简单的 HTML 文件：

```html
<!DOCTYPE html>
<html>
<head>
    <title>三维基因组分析智能体</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        #chat { height: 400px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        #input { width: 70%; padding: 10px; }
        #send { padding: 10px 20px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .assistant { background: #f3e5f5; }
    </style>
</head>
<body>
    <h1>🧬 三维基因组分析智能体</h1>
    <div id="chat"></div>
    <input type="text" id="input" placeholder="输入您的问题...">
    <button onclick="sendMessage()">发送</button>

    <script>
        // 替换为您的部署地址
        const BASE_URL = "https://xxxxx.coze.site";

        async function sendMessage() {
            const input = document.getElementById('input');
            const chat = document.getElementById('chat');
            const message = input.value.trim();

            if (!message) return;

            // 显示用户消息
            chat.innerHTML += `<div class="message user">${message}</div>`;
            input.value = '';

            try {
                const response = await fetch(`${BASE_URL}/run`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        messages: [{ role: 'user', content: message }]
                    })
                });

                const data = await response.json();

                // 显示助手回复
                chat.innerHTML += `<div class="message assistant">${data.messages?.[data.messages.length-1]?.content || data}</div>`;
                chat.scrollTop = chat.scrollHeight;
            } catch (error) {
                chat.innerHTML += `<div class="message assistant" style="color: red;">错误: ${error.message}</div>`;
            }
        }

        // 回车发送
        document.getElementById('input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
```

保存为 `chat.html`，双击打开即可使用。

---

## 📡 API 接口说明

### 1. `/run` - 同步运行

**请求格式**：
```json
{
  "messages": [
    {
      "role": "user",
      "content": "您的问题"
    }
  ]
}
```

**响应格式**：
```json
{
  "messages": [
    {
      "role": "assistant",
      "content": "智能体的回复"
    }
  ],
  "run_id": "会话ID"
}
```

---

### 2. `/stream_run` - 流式运行（推荐）

**请求格式**：
```json
{
  "messages": [
    {
      "role": "user",
      "content": "您的问题"
    }
  ]
}
```

**响应格式**：Server-Sent Events (SSE) 流

```text
event: message
data: {"content": "部分回复", ...}

event: message
data: {"content": "更多内容", ...}
```

---

### 3. `/v1/chat/completions` - OpenAI 兼容接口

**请求格式**（OpenAI 标准）：
```json
{
  "model": "agent",
  "messages": [
    {
      "role": "user",
      "content": "您的问题"
    }
  ]
}
```

**响应格式**（OpenAI 标准）：
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "智能体的回复"
      }
    }
  ]
}
```

---

### 4. `/health` - 健康检查

**请求**：
```bash
GET /health
```

**响应**：
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

---

## 🎯 使用示例

### 示例 1: TAD 分析
```bash
curl -X POST https://xxxxx.coze.site/run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "分析 assets/demo_chr1.mcool 文件中 chr1 染色体的 TAD 结构，使用 100000 bp 分辨率"
      }
    ]
  }'
```

### 示例 2: Compartment 分析
```bash
curl -X POST https://xxxxx.coze.site/run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "分析 demo_chr1.mcool 中 chr1 的 A/B compartments"
      }
    ]
  }'
```

### 示例 3: 文献检索
```bash
curl -X POST https://xxxxx.coze.site/run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "搜索关于 TAD 分析的最新研究文献"
      }
    ]
  }'
```

---

## ❓ 常见问题

### Q1: 部署成功后在哪里找到智能体？
**A**:
- 智能体不是通过网页界面访问的
- 需要通过 API 接口调用
- 部署成功后，Coze 会提供访问 URL（如 `https://xxxxx.coze.site`）
- 使用该 URL + API 端点进行调用

### Q2: 能否在浏览器中直接访问智能体？
**A**:
- 不能直接访问
- 但可以创建一个简单的网页界面（见上方"方式 4"）
- 或者使用支持 OpenAI API 的聊天工具

### Q3: 如何测试智能体是否正常工作？
**A**:
```bash
# 健康检查
curl https://xxxxx.coze.site/health

# 发送测试问题
curl -X POST https://xxxxx.coze.site/run \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "你好"}]}'
```

### Q4: 如何进行多轮对话？
**A**:
```bash
curl -X POST https://xxxxx.coze.site/run \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "分析 chr1 的 TAD"},
      {"role": "assistant", "content": "识别到 16 个 TAD"},
      {"role": "user", "content": "详细说明第 5 个 TAD"}
    ]
  }'
```

### Q5: 智能体支持哪些功能？
**A**:
- ✅ TAD 分析
- ✅ Compartment 分析
- ✅ 文献检索
- ✅ 历史记录查询
- ✅ 多分辨率分析
- ❌ 网页搜索（需要额外添加工具）

### Q6: 如何添加网页搜索功能？
**A**:
可以添加网络搜索工具，具体实现请参考项目文档或联系开发者。

---

## 📞 获取帮助

如果遇到问题，请：

1. **检查日志**：查看 `/app/work/logs/bypass/app.log`
2. **健康检查**：调用 `/health` 端点
3. **查看文档**：阅读项目的 README.md 和 docs 目录
4. **联系支持**：在 Coze 平台提交工单

---

## 🎓 进阶使用

### 使用 Session ID 保持对话状态
```bash
curl -X POST https://xxxxx.coze.site/run \
  -H "Content-Type: application/json" \
  -H "X-Session-Id: my-session-123" \
  -d '{
    "messages": [
      {"role": "user", "content": "分析 chr1"}
    ]
  }'
```

### 取消长时间运行的任务
```bash
curl -X POST https://xxxxx.coze.site/cancel/{run_id}
```

---

**更新日期**: 2026-03-11
**版本**: v1.0.0
