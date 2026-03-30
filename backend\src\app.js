const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// 创建 uploads 目录
const fs = require('fs');
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// 数据库连接
const mysql = require('mysql2/promise');
let db;

async function initDB() {
  try {
    db = await mysql.createConnection({
      host: process.env.DB_HOST || 'localhost',
      port: process.env.DB_PORT || 3306,
      user: process.env.DB_USER || 'root',
      password: process.env.DB_PASSWORD || '',
      database: process.env.DB_NAME || 'visa_db'
    });
    console.log('✅ 数据库连接成功');
  } catch (error) {
    console.log('⚠️  数据库连接失败，使用内存数据模式');
    db = null;
  }
}

// 内存数据存储（用于无数据库时的演示）
let memoryData = {
  users: [],
  products: [
    {
      id: 1,
      country: '日本',
      visa_type: '旅游签证 - 单次',
      price: 299,
      duration: '5-7 工作日',
      materials: ['护照原件', '照片 2 张', '身份证复印件', '申请表'],
      description: '日本个人旅游签证，有效期 3 个月，停留 15 天',
      status: 1
    },
    {
      id: 2,
      country: '泰国',
      visa_type: '旅游签证',
      price: 199,
      duration: '3-5 工作日',
      materials: ['护照原件', '照片 2 张', '往返机票'],
      description: '泰国落地签/电子签，有效期 3 个月，停留 30 天',
      status: 1
    },
    {
      id: 3,
      country: '越南',
      visa_type: '旅游签证 - 单次',
      price: 159,
      duration: '3-5 工作日',
      materials: ['护照原件', '照片 2 张'],
      description: '越南电子签证，有效期 1 个月，停留 30 天',
      status: 1
    },
    {
      id: 4,
      country: '新加坡',
      visa_type: '旅游签证',
      price: 259,
      duration: '3-5 工作日',
      materials: ['护照原件', '照片 2 张', '身份证复印件', '在职证明'],
      description: '新加坡电子签证，有效期 2 年，停留 30 天',
      status: 1
    },
    {
      id: 5,
      country: '韩国',
      visa_type: '旅游签证 - 单次',
      price: 399,
      duration: '5-7 工作日',
      materials: ['护照原件', '照片 1 张', '身份证复印件', '银行流水'],
      description: '韩国个人旅游签证，有效期 3 个月，停留 90 天',
      status: 1
    },
    {
      id: 6,
      country: '美国',
      visa_type: 'B1/B2 旅游商务',
      price: 1299,
      duration: '30-60 工作日',
      materials: ['护照原件', '照片 1 张', 'DS160 表', '面签'],
      description: '美国十年多次往返签证，需面签',
      status: 1
    }
  ],
  orders: []
};

// 数据库操作辅助函数
async function query(sql, params) {
  if (db) {
    const [results] = await db.execute(sql, params);
    return results;
  }
  return null;
}

// ==================== 路由 ====================

// 首页 API
app.get('/api', (req, res) => {
  res.json({
    message: '签证办理系统 API',
    version: '1.0.0',
    endpoints: {
      products: 'GET /api/products',
      productDetail: 'GET /api/products/:id',
      orders: 'GET/POST /api/orders',
      login: 'POST /api/auth/login',
      register: 'POST /api/auth/register'
    }
  });
});

// 获取产品列表
app.get('/api/products', async (req, res) => {
  try {
    if (db) {
      const products = await query('SELECT * FROM visa_products WHERE status = 1');
      res.json({ code: 0, data: products || [] });
    } else {
      res.json({ code: 0, data: memoryData.products });
    }
  } catch (error) {
    res.json({ code: 0, data: memoryData.products });
  }
});

// 获取产品详情
app.get('/api/products/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    if (db) {
      const products = await query('SELECT * FROM visa_products WHERE id = ?', [id]);
      res.json({ code: 0, data: products[0] || null });
    } else {
      const product = memoryData.products.find(p => p.id === id);
      res.json({ code: 0, data: product || null });
    }
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 创建订单
app.post('/api/orders', async (req, res) => {
  try {
    const { userId, productId, applicantInfo, materials } = req.body;
    const orderNo = 'V' + Date.now() + Math.random().toString(36).substr(2, 6);
    const product = memoryData.products.find(p => p.id === productId);
    
    const order = {
      id: memoryData.orders.length + 1,
      orderNo,
      userId: userId || 1,
      productId,
      amount: product ? product.price : 0,
      status: 0, // 待支付
      applicantInfo: applicantInfo || {},
      materials: materials || [],
      remark: '',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    memoryData.orders.push(order);
    
    res.json({ code: 0, data: order, message: '订单创建成功' });
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 获取订单列表
app.get('/api/orders', async (req, res) => {
  try {
    const userId = parseInt(req.query.userId) || 1;
    const orders = memoryData.orders.filter(o => o.userId === userId);
    res.json({ code: 0, data: orders });
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 获取订单详情
app.get('/api/orders/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const order = memoryData.orders.find(o => o.id === id);
    res.json({ code: 0, data: order || null });
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 用户登录
app.post('/api/auth/login', async (req, res) => {
  try {
    const { phone, password } = req.body;
    // 简化版：任意手机号密码都能登录
    const user = {
      id: 1,
      phone: phone || '13800138000',
      nickname: '测试用户',
      avatar: ''
    };
    res.json({ 
      code: 0, 
      data: { 
        user,
        token: 'demo_token_' + Date.now()
      },
      message: '登录成功'
    });
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 用户注册
app.post('/api/auth/register', async (req, res) => {
  try {
    const { phone, password } = req.body;
    const user = {
      id: memoryData.users.length + 1,
      phone,
      nickname: '新用户',
      avatar: ''
    };
    memoryData.users.push(user);
    res.json({ code: 0, data: user, message: '注册成功' });
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 模拟支付
app.post('/api/pay/create', async (req, res) => {
  try {
    const { orderId, type } = req.body;
    res.json({
      code: 0,
      data: {
        orderId,
        type,
        payUrl: type === 'wechat' ? 'https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb' : 'https://openapi.alipay.com/gateway.do',
        message: '支付订单创建成功（演示模式）'
      }
    });
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 更新订单状态（后台用）
app.put('/api/admin/orders/:id/status', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const { status, remark } = req.body;
    const order = memoryData.orders.find(o => o.id === id);
    if (order) {
      order.status = status;
      order.remark = remark || '';
      order.updatedAt = new Date().toISOString();
      res.json({ code: 0, data: order, message: '更新成功' });
    } else {
      res.status(404).json({ code: 1, message: '订单不存在' });
    }
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 后台 - 获取订单列表
app.get('/api/admin/orders', async (req, res) => {
  try {
    res.json({ code: 0, data: memoryData.orders });
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// 后台 - 统计数据
app.get('/api/admin/stats', async (req, res) => {
  try {
    const stats = {
      totalOrders: memoryData.orders.length,
      pendingOrders: memoryData.orders.filter(o => o.status === 0).length,
      processingOrders: memoryData.orders.filter(o => o.status === 1 || o.status === 2).length,
      completedOrders: memoryData.orders.filter(o => o.status === 3 || o.status === 4).length,
      totalRevenue: memoryData.orders.filter(o => o.status >= 1).reduce((sum, o) => sum + o.amount, 0)
    };
    res.json({ code: 0, data: stats });
  } catch (error) {
    res.status(500).json({ code: 1, message: error.message });
  }
});

// ==================== 启动服务器 ====================

async function start() {
  await initDB();
  
  app.listen(PORT, () => {
    console.log(`
╔════════════════════════════════════════════════════════╗
║           🛂 签证办理系统 - 后端服务                     ║
╠════════════════════════════════════════════════════════╣
║  🌐 服务地址：http://localhost:${PORT}                   ║
║  📡 API 地址：http://localhost:${PORT}/api               ║
║  📁 上传目录：${uploadsDir}                               ║
║  💾 数据模式：${db ? 'MySQL' : '内存演示模式'}              ║
╚════════════════════════════════════════════════════════╝
    `);
  });
}

start();
