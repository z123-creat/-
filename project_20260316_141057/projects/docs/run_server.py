#!/usr/bin/env python3
"""
支持 CORS 和 POST 请求的简单 HTTP 服务器
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加 CORS 头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        # 对于所有 POST 请求，返回 404
        # 因为我们只是静态文件服务器，不处理 POST
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {
            "error": "Not Found",
            "message": "This is a static file server. POST requests are not handled here.",
            "note": "The HTML page should send requests directly to the Coze API"
        }
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    PORT = 8000
    server = HTTPServer(('localhost', PORT), CORSRequestHandler)
    print(f"Server running at http://localhost:{PORT}/")
    print("This server supports CORS for GET requests.")
    print("POST requests to this server will return 404.")
    print("The HTML page sends requests directly to Coze API.")
    server.serve_forever()
