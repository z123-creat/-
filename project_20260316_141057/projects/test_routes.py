#!/usr/bin/env python3
"""
测试 main.py 中的路由是否正确定义
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入 FastAPI 应用
from main import app

# 打印所有路由
print("=" * 80)
print("FastAPI 应用中的所有路由：")
print("=" * 80)

for route in app.routes:
    print(f"路径: {route.path}")
    print(f"方法: {route.methods}")
    print(f"名称: {route.name}")
    print("-" * 80)

# 检查 CORS 中间件
print("\n" + "=" * 80)
print("中间件配置：")
print("=" * 80)

for middleware in app.user_middleware:
    print(f"中间件: {middleware.cls.__name__}")
    if hasattr(middleware, 'options'):
        print(f"  配置: {middleware.options}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
