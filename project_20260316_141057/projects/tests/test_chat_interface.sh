#!/bin/bash

# 测试智能引导页面功能

echo "======================================"
echo "   智能引导页面功能测试"
echo "======================================"
echo ""

BASE_URL="http://localhost:5000"

# 测试 1：检查健康检查端点
echo "测试 1: 健康检查端点"
echo "--------------------------------------"
HEALTH=$(curl -s "${BASE_URL}/health")
echo "响应: $HEALTH"
if [[ $HEALTH == *"ok"* ]]; then
    echo "✅ 健康检查通过"
else
    echo "❌ 健康检查失败"
fi
echo ""

# 测试 2：检查根路径返回 HTML
echo "测试 2: 根路径返回 HTML"
echo "--------------------------------------"
ROOT_HTML=$(curl -s "${BASE_URL}/")
TITLE=$(echo "$ROOT_HTML" | grep -o '<title>.*</title>')
if [[ $TITLE == *"三维基因组分析智能体"* ]]; then
    echo "✅ 根路径正确返回引导页面"
    echo "   页面标题: $TITLE"
else
    echo "❌ 根路径返回错误"
    echo "   标题: $TITLE"
fi
echo ""

# 测试 3：检查聊天页面路径
echo "测试 3: 聊天页面路径"
echo "--------------------------------------"
CHAT_HTML=$(curl -s "${BASE_URL}/chat")
CHAT_TITLE=$(echo "$CHAT_HTML" | grep -o '<title>.*</title>')
if [[ $CHAT_TITLE == *"三维基因组分析智能体"* ]]; then
    echo "✅ 聊天页面正确返回"
    echo "   页面标题: $CHAT_TITLE"
else
    echo "❌ 聊天页面返回错误"
    echo "   标题: $CHAT_TITLE"
fi
echo ""

# 测试 4：检查 landing.html 文件存在
echo "测试 4: 文件存在性检查"
echo "--------------------------------------"
if [ -f "src/templates/landing.html" ]; then
    echo "✅ landing.html 文件存在"
    echo "   文件大小: $(wc -c < src/templates/landing.html) 字节"
else
    echo "❌ landing.html 文件不存在"
fi

if [ -f "src/templates/chat_with_token.html" ]; then
    echo "✅ chat_with_token.html 文件存在"
    echo "   文件大小: $(wc -c < src/templates/chat_with_token.html) 字节"
else
    echo "❌ chat_with_token.html 文件不存在"
fi
echo ""

# 测试 5：检查 HTML 完整性
echo "测试 5: HTML 完整性检查"
echo "--------------------------------------"
LANDING_TAGS=$(grep -c "</html>" src/templates/landing.html)
CHAT_TAGS=$(grep -c "</html>" src/templates/chat_with_token.html)

if [ "$LANDING_TAGS" -eq 1 ]; then
    echo "✅ landing.html HTML 标签完整"
else
    echo "❌ landing.html HTML 标签不完整 (找到 $LANDING_TAGS 个 </html>)"
fi

if [ "$CHAT_TAGS" -eq 1 ]; then
    echo "✅ chat_with_token.html HTML 标签完整"
else
    echo "❌ chat_with_token.html HTML 标签不完整 (找到 $CHAT_TAGS 个 </html>)"
fi
echo ""

# 测试 6：检查 JavaScript 关键功能
echo "测试 6: JavaScript 功能检查"
echo "--------------------------------------"
LANDING_JS=$(grep -c "testConnection" src/templates/landing.html)
CHAT_JS=$(grep -c "sendMessage" src/templates/chat_with_token.html)

if [ "$LANDING_JS" -gt 0 ]; then
    echo "✅ landing.html 包含 JavaScript 函数"
    echo "   testConnection 函数: 找到 $LANDING_JS 处引用"
else
    echo "❌ landing.html JavaScript 功能缺失"
fi

if [ "$CHAT_JS" -gt 0 ]; then
    echo "✅ chat_with_token.html 包含 JavaScript 函数"
    echo "   sendMessage 函数: 找到 $CHAT_JS 处引用"
else
    echo "❌ chat_with_token.html JavaScript 功能缺失"
fi
echo ""

# 测试 7：检查路由配置
echo "测试 7: 路由配置检查"
echo "--------------------------------------"
MAIN_ROUTES=$(grep -c "@app.get" src/main.py)
LANDING_ROUTE=$(grep -c 'get_landing_page' src/main.py)
CHAT_ROUTE=$(grep -c 'get_chat_page' src/main.py)

echo "main.py 中的路由总数: $MAIN_ROUTES"

if [ "$LANDING_ROUTE" -gt 0 ]; then
    echo "✅ 根路径路由已配置 (get_landing_page)"
else
    echo "❌ 根路径路由缺失"
fi

if [ "$CHAT_ROUTE" -gt 0 ]; then
    echo "✅ 聊天页面路由已配置 (get_chat_page)"
else
    echo "❌ 聊天页面路由缺失"
fi
echo ""

# 测试 8：检查导入
echo "测试 8: 导入检查"
echo "--------------------------------------"
HAS_OS=$(grep -c "^import os" src/main.py)
HAS_HTML=$(grep -c "HTMLResponse" src/main.py)

if [ "$HAS_OS" -gt 0 ]; then
    echo "✅ os 模块已导入"
else
    echo "❌ os 模块未导入"
fi

if [ "$HAS_HTML" -gt 0 ]; then
    echo "✅ HTMLResponse 已导入"
else
    echo "❌ HTMLResponse 未导入"
fi
echo ""

# 总结
echo "======================================"
echo "   测试总结"
echo "======================================"
echo ""
echo "请访问以下地址测试："
echo "  • 引导页面: http://localhost:5000"
echo "  • 聊天页面: http://localhost:5000/chat"
echo "  • 健康检查: http://localhost:5000/health"
echo ""
echo "部署后访问："
echo "  • 引导页面: https://gsn2v3kydv.coze.site"
echo "  • 聊天页面: https://gsn2v3kydv.coze.site/chat"
echo ""
