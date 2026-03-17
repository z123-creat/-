#!/usr/bin/env python3
"""
Coze API 代理服务器
解决 CORS 跨域问题
"""
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
# 启用 CORS
CORS(app)

COZE_API_URL = "https://gsn2v3kydv.coze.site"

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "message": "Proxy server is running"
    })

@app.route('/run', methods=['POST', 'OPTIONS'])
def proxy_run():
    """代理 /run 请求到 Coze API"""
    if request.method == 'OPTIONS':
        # 处理预检请求
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response

    # 获取请求头
    headers = {
        'Content-Type': 'application/json',
    }

    # 转发 Authorization 头
    auth_header = request.headers.get('Authorization')
    if auth_header:
        headers['Authorization'] = auth_header

    # 转发请求到 Coze API
    try:
        coze_response = requests.post(
            f"{COZE_API_URL}/run",
            headers=headers,
            json=request.json,
            timeout=300  # 5分钟超时
        )

        # 返回响应
        response = Response(
            coze_response.content,
            status=coze_response.status_code,
            content_type='application/json'
        )
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Proxy request failed",
            "message": str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """返回主页"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coze API 代理服务器</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #667eea;
            }
            .info {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            code {
                background: #f5f5f5;
                padding: 2px 6px;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Coze API 代理服务器</h1>
            <p>代理服务器正在运行！</p>
            
            <div class="info">
                <strong>使用方法：</strong><br>
                1. 在浏览器中打开 <code>chat_final.html</code><br>
                2. 将 API 地址改为 <code>http://localhost:5000</code><br>
                3. 输入 API Token<br>
                4. 测试连接
            </div>
            
            <h2>API 端点：</h2>
            <ul>
                <li><code>GET /health</code> - 健康检查</li>
                <li><code>POST /run</code> - 运行智能体</li>
            </ul>
            
            <div class="info">
                <strong>注意：</strong><br>
                - 这个代理服务器解决了 CORS 跨域问题<br>
                - 它会将请求转发到 Coze API<br>
                - 请确保代理服务器正在运行
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("=" * 80)
    print("Coze API 代理服务器启动中...")
    print("=" * 80)
    print(f"✅ 代理服务器运行在: http://localhost:5000")
    print(f"🔄 转发请求到: {COZE_API_URL}")
    print("=" * 80)
    print("\n使用方法：")
    print("1. 在浏览器中打开 chat_final.html")
    print("2. 将 API 地址改为: http://localhost:5000")
    print("3. 输入 API Token")
    print("4. 测试连接")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 80)
    app.run(host='0.0.0.0', port=5000, debug=True)
