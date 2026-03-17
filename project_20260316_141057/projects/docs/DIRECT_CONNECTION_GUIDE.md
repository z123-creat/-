# 🔧 直接连接 Coze API 的配置方法

## 📋 概述

如果不使用代理服务器，直接连接 Coze API，需要解决 **CORS 跨域问题**。

---

## 🎯 关键问题

### 什么是 CORS？

**CORS（跨域资源共享）** 是浏览器的安全机制，阻止网页从不同域名访问 API。

**问题**：
- 从本地 HTML 文件（`file://`）访问 Coze API
- 从 GitHub Pages（`https://username.github.io`）访问 Coze API
- 浏览器会阻止这些跨域请求

**解决方法**：
1. 在 Coze 平台配置 CORS 允许跨域访问
2. 将 HTML 文件部署到与 Coze API 相同的域名
3. 或使用代理服务器（当前方案）

---

## ✅ 解决方案：在 Coze 平台配置 CORS

### 第 1 步：在 Coze 平台配置 CORS

#### 方法 A：在项目设置中查找

1. **登录 Coze 平台**
   - 访问 https://www.coze.cn/
   - 登录您的账号

2. **进入项目设置**
   - 进入您的项目详情页
   - 找到"设置"或"Settings"标签

3. **查找 CORS 配置**
   在设置页面中查找以下选项：
   - "跨域资源共享" (CORS)
   - "跨域设置"
   - "API 设置" → "CORS"
   - "安全设置" → "CORS"

4. **配置 CORS 规则**
   
   如果找到 CORS 配置，添加以下规则：

   **允许的来源 (Allowed Origins)**：
   ```
   *
   ```
   或（更安全）：
   ```
   https://your-username.github.io
   https://your-project.vercel.app
   ```

   **允许的方法 (Allowed Methods)**：
   ```
   GET, POST, PUT, DELETE, OPTIONS
   ```

   **允许的头部 (Allowed Headers)**：
   ```
   *
   ```

   **允许的凭证 (Allow Credentials)**：
   ```
   false
   ```

5. **保存配置**

---

#### 方法 B：联系 Coze 平台客服

如果在设置中找不到 CORS 配置：

1. 在 Coze 平台找到"帮助"或"客服"
2. 提交工单或联系客服
3. 说明需求：
   - "我需要配置 CORS 跨域访问"
   - "允许从 GitHub Pages 访问我的智能体 API"
   - "API 地址是：https://gsn2v3kydv.coze.site"

---

### 第 2 步：修改 HTML 文件

#### 修改 chat_final.html（使用 Token）

**文件位置**：`docs/chat_final.html`

**修改内容**：

1. 打开 `chat_final.html`
2. 找到第 626 行左右：
   ```javascript
   let baseUrl = 'http://localhost:5000';
   ```

3. **修改为直接连接 Coze API**：
   ```javascript
   let baseUrl = 'https://gsn2v3kydv.coze.site';
   ```

4. 保存文件

---

#### 修改 chat_public.html（公开访问）

**文件位置**：`docs/chat_public.html`

**修改内容**：

1. 打开 `chat_public.html`
2. 找到第 400 行左右：
   ```javascript
   const COZE_PUBLIC_URL = 'https://gsn2v3kydv.coze.site';
   ```

3. **确保使用正确的公开访问地址**：
   - 如果您的公开访问地址不同，请替换
   - 如果不确定，暂时保持不变

4. 保存文件

---

### 第 3 步：部署到 HTTPS 网站

**重要**：从 `file://` 协议访问 Coze API 通常会被阻止，必须部署到 HTTPS 网站。

#### 推荐的免费部署平台：

**方案 A：GitHub Pages**

1. **创建仓库**
   - 在 GitHub 创建新仓库

2. **上传文件**
   - 上传修改后的 HTML 文件
   - 重命名为 `index.html`

3. **启用 GitHub Pages**
   - Settings → Pages
   - 选择分支（main/master）
   - 保存

4. **获取 HTTPS 地址**
   ```
   https://your-username.github.io/your-repo/
   ```

---

**方案 B：Vercel**

1. **安装 Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **部署**
   ```bash
   cd docs
   vercel
   ```

3. **获取 HTTPS 地址**
   ```
   https://your-project.vercel.app
   ```

---

**方案 C：Netlify**

1. **访问 Netlify**
   - 访问 https://www.netlify.com/
   - 注册并登录

2. **拖拽部署**
   - 将 HTML 文件拖拽到部署区域

3. **获取 HTTPS 地址**
   ```
   https://your-project.netlify.app
   ```

---

### 第 4 步：在 Coze 平台添加部署域名到 CORS

如果配置 CORS 时需要指定允许的域名：

1. 将您的部署地址添加到 CORS 配置中：
   ```
   https://your-username.github.io
   https://your-project.vercel.app
   https://your-project.netlify.app
   ```

2. 保存配置

---

### 第 5 步：测试连接

1. **访问部署后的 HTTPS 地址**
   - 在浏览器中打开
   - 例如：`https://your-username.github.io/your-repo/`

2. **测试连接**

   **如果使用 chat_final.html（带 Token）**：
   - 输入 API Token
   - 点击"测试连接"

   **如果使用 chat_public.html（公开访问）**：
   - 页面加载时会自动测试连接
   - 查看连接状态

3. **查看结果**

   **成功**：
   - ✅ 显示"已连接"
   - ✅ 可以发送消息

   **失败**：
   - ❌ 显示"连接失败"
   - ❌ 查看浏览器控制台（F12）查看详细错误

---

## 🔍 常见问题

### 问题 1：仍然显示 CORS 错误

**原因**：CORS 配置未生效

**解决方案**：
1. 等待几分钟，让 CORS 配置生效
2. 检查 CORS 配置是否正确
3. 联系 Coze 平台客服确认

---

### 问题 2：从 file:// 访问失败

**原因**：浏览器阻止从 `file://` 协议的跨域请求

**解决方案**：
- 必须部署到 HTTPS 网站
- 不能直接打开本地 HTML 文件

---

### 问题 3：部署后仍然失败

**原因**：部署域名未添加到 CORS 允许列表

**解决方案**：
1. 在 Coze 平台将部署域名添加到 CORS 配置
2. 使用通配符 `*` 允许所有域名（测试用）

---

## 📊 方案对比

| 方案 | 需要配置 CORS | 需要部署 HTTPS | 推荐度 |
|------|-------------|---------------|--------|
| 代理服务器（当前） | ❌ 否 | ❌ 否 | ⭐⭐⭐⭐⭐ |
| 直接连接 + Coze CORS | ✅ 是 | ✅ 是 | ⭐⭐⭐ |

---

## 🎯 推荐流程

### 测试阶段（本地使用）

**使用代理服务器方案**：
1. 启动代理服务器：`python proxy_server.py`
2. 使用 `chat_final.html`
3. API 地址：`http://localhost:5000`
4. 输入 API Token

### 生产阶段（分享给他人）

**尝试直接连接方案**：
1. 在 Coze 平台配置 CORS
2. 修改 HTML 文件，使用 Coze API 地址
3. 部署到 GitHub Pages / Vercel / Netlify
4. 测试连接

**如果直接连接失败**：
- 回到代理服务器方案
- 或将代理服务器部署到云端（Vercel/Railway）

---

## 💡 关键点

### 必须使用 HTTPS

- ❌ `file://` - 不支持
- ❌ `http://` - 不安全，可能被阻止
- ✅ `https://` - 必须使用

### 必须配置 CORS

- 在 Coze 平台配置允许跨域访问
- 允许的来源可以是 `*` 或特定域名

### 必须部署

- 不能直接打开本地 HTML 文件
- 必须部署到 HTTPS 网站

---

## 📞 需要帮助？

如果按照以上步骤操作后仍然失败，请提供：

1. **您使用的是哪个文件**：chat_final.html 还是 chat_public.html？
2. **是否配置了 CORS**？配置了哪些内容？
3. **部署的 HTTPS 地址是什么**？
4. **浏览器控制台显示什么错误**？（按 F12 查看）

我会帮您进一步诊断和解决问题！😊
