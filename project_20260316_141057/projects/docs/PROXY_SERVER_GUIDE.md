# 🚀 Coze API 代理服务器使用指南

## 📋 问题说明

**问题**：直接打开本地 HTML 文件（`file://` 协议）访问 Coze API 时，遇到 **CORS 跨域错误**。

**错误信息**：
```
Access to fetch at 'https://gsn2v3kydv.coze.site/run' from origin 'null' has been blocked by CORS policy
```

**原因**：
- 浏览器安全策略阻止从本地文件向 HTTPS 网站发送请求
- Coze API 没有返回正确的 CORS 头

---

## ✅ 解决方案：使用代理服务器

### 方案 1：使用 Python 代理服务器（推荐）

#### 步骤 1：安装依赖

```bash
pip install flask flask-cors requests
```

#### 步骤 2：启动代理服务器

```bash
cd C:\Users\Lenovo\Downloads
python proxy_server.py
```

**启动成功后，你会看到**：
```
================================================================================
Coze API 代理服务器启动中...
================================================================================
✅ 代理服务器运行在: http://localhost:5000
🔄 转发请求到: https://gsn2v3kydv.coze.site
================================================================================
...
```

#### 步骤 3：配置并使用聊天界面

1. **打开 `chat_final.html`**
   - 直接双击文件在浏览器中打开

2. **修改 API 地址**
   - 将 "API 地址" 从 `https://gsn2v3kydv.coze.site` 改为 `http://localhost:5000`
   - 点击"测试连接"

3. **输入 API Token**
   - 从 Coze 平台获取 API Token
   - 粘贴到"API Token"输入框
   - 点击"测试连接"

#### 步骤 4：验证连接

**成功**：
- ✅ 显示："✅ 连接成功！"
- ✅ 状态变为"● 已连接"

**失败**：
- ❌ 检查 API Token 是否正确
- ❌ 检查代理服务器是否正在运行

---

### 方案 2：使用 Node.js 代理服务器

#### 步骤 1：安装依赖

```bash
npm install express cors axios
```

#### 步骤 2：创建代理服务器

创建文件 `proxy_server.js`：

```javascript
const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = 5000;
const COZE_API_URL = 'https://gsn2v3kydv.coze.site';

// 启用 CORS
app.use(cors());
app.use(express.json());

// 健康检查
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        message: 'Proxy server is running'
    });
});

// 代理 /run 请求
app.post('/run', async (req, res) => {
    try {
        const headers = {
            'Content-Type': 'application/json',
        };

        // 转发 Authorization 头
        if (req.headers.authorization) {
            headers['Authorization'] = req.headers.authorization;
        }

        const response = await axios.post(
            `${COZE_API_URL}/run`,
            req.body,
            {
                headers,
                timeout: 300000 // 5分钟超时
            }
        );

        res.status(response.status).json(response.data);
    } catch (error) {
        if (error.response) {
            res.status(error.response.status).json(error.response.data);
        } else {
            res.status(500).json({
                error: 'Proxy request failed',
                message: error.message
            });
        }
    }
});

app.listen(PORT, () => {
    console.log(`🚀 代理服务器运行在: http://localhost:${PORT}`);
    console.log(`🔄 转发请求到: ${COZE_API_URL}`);
    console.log('\n使用方法：');
    console.log('1. 在浏览器中打开 chat_final.html');
    console.log('2. 将 API 地址改为: http://localhost:5000');
    console.log('3. 输入 API Token');
    console.log('4. 测试连接');
});
```

#### 步骤 3：启动代理服务器

```bash
node proxy_server.js
```

---

### 方案 3：使用 http-server with Proxy（最简单）

#### 步骤 1：安装 http-server

```bash
npm install -g http-server
```

#### 步骤 2：启动服务器

```bash
cd C:\Users\Lenovo\Downloads
http-server -p 8000 --cors --proxy https://gsn2v3kydv.coze.site
```

#### 步骤 3：使用聊天界面

1. 在浏览器中访问：`http://localhost:8000/chat_final.html`
2. 将 API 地址改为：`http://localhost:8000`
3. 输入 API Token
4. 测试连接

---

## 🔍 工作原理

### 为什么需要代理？

**直接访问（失败）**：
```
浏览器 (file://) → Coze API (https://)
                    ↓
                CORS 阻止 ❌
```

**通过代理（成功）**：
```
浏览器 (http://localhost) → 代理服务器 (http://localhost) → Coze API (https://)
                              ↓
                          允许 CORS ✅
```

### 代理服务器做了什么？

1. **接收请求**：从浏览器接收请求
2. **添加 CORS 头**：返回正确的 CORS 头
3. **转发请求**：将请求转发到 Coze API
4. **返回响应**：将 Coze API 的响应返回给浏览器

---

## 📋 快速开始

### 最快的方法（Python）

```bash
# 1. 安装依赖
pip install flask flask-cors requests

# 2. 启动代理服务器
cd C:\Users\Lenovo\Downloads
python proxy_server.py

# 3. 打开聊天界面
# 在浏览器中打开 chat_final.html

# 4. 修改配置
# API 地址: http://localhost:5000
# API Token: [从 Coze 平台获取]

# 5. 测试连接
# 点击"测试连接"按钮
```

---

## ❓ 常见问题

### Q: 代理服务器启动失败？

**A**: 检查端口是否被占用
```bash
# Windows
netstat -ano | findstr :5000
```

如果被占用，修改 `proxy_server.py` 中的端口：
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # 改为 5001
```

### Q: 连接超时？

**A**: 检查网络连接和代理服务器日志

### Q: Token 错误？

**A**: 检查 API Token 是否正确和未过期

---

## 🎯 总结

**核心问题**：CORS 跨域限制

**解决方案**：使用代理服务器

**推荐方案**：
- ✅ Python Flask 代理服务器（最稳定）
- ✅ Node.js 代理服务器（最灵活）
- ✅ http-server with Proxy（最简单）

**使用步骤**：
1. 启动代理服务器
2. 修改 API 地址为 `http://localhost:5000`
3. 输入 API Token
4. 测试连接

**结果**：
- ✅ 成功连接
- ✅ 可以正常对话
- ✅ 使用智能体功能

---

## 📞 需要帮助？

如果遇到问题，请提供：
1. 代理服务器的启动日志
2. 浏览器控制台的错误信息
3. 连接时显示的错误信息
