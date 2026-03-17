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

        console.log('🔄 转发请求到 Coze API...');
        const response = await axios.post(
            `${COZE_API_URL}/run`,
            req.body,
            {
                headers,
                timeout: 300000 // 5分钟超时
            }
        );

        console.log('✅ 请求成功');
        res.status(response.status).json(response.data);
    } catch (error) {
        console.error('❌ 请求失败:', error.message);
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
    console.log('='.repeat(80));
    console.log('Coze API 代理服务器启动中...');
    console.log('='.repeat(80));
    console.log(`✅ 代理服务器运行在: http://localhost:${PORT}`);
    console.log(`🔄 转发请求到: ${COZE_API_URL}`);
    console.log('='.repeat(80));
    console.log('\n使用方法：');
    console.log('1. 在浏览器中打开 chat_final.html');
    console.log('2. 将 API 地址改为: http://localhost:5000');
    console.log('3. 输入 API Token');
    console.log('4. 测试连接');
    console.log('\n按 Ctrl+C 停止服务器');
    console.log('='.repeat(80));
});
