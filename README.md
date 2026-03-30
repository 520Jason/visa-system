# 🛂 签证办理系统

一个简易的签证在线办理平台，包含 Web 前端、后台管理系统和 API 后端。

**技术栈：Python + FastAPI + MySQL + Vue/HTML**

## 📁 项目结构

```
visa-project/
├── backend/          # 后端 API (Python + FastAPI)
│   ├── main.py       # 主程序
│   ├── requirements.txt  # Python 依赖
│   ├── uploads/      # 上传文件目录
│   └── .env          # 环境配置
├── frontend/         # 前端网页
│   └── index.html    # 主页
├── admin/            # 后台管理 (待开发)
├── database/         # 数据库脚本
│   └── schema.sql    # 表结构
└── README.md         # 说明文档
```

## 🚀 快速开始

### 方式一：直接打开前端（无需后端）

1. 用浏览器直接打开 `frontend/index.html`
2. 可以查看页面效果（使用演示数据）

### 方式二：完整运行（后端 + 前端）

#### 1. 安装 Node.js

- 下载地址：https://nodejs.org/zh-cn/download/
- 安装完成后验证：
  ```bash
  node --version
  npm --version
  ```

#### 2. 安装后端依赖

```bash
cd visa-project/backend
npm install
```

#### 3. 配置环境变量（可选）

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，配置数据库等信息
# 如果不配置，系统会使用内存数据模式运行
```

#### 4. 启动后端服务

```bash
# 开发模式（自动重启）
npm run dev

# 或普通模式
npm start
```

看到以下输出表示启动成功：
```
╔════════════════════════════════════════════════════════╗
║           🛂 签证办理系统 - 后端服务                     ║
╠════════════════════════════════════════════════════════╣
║  🌐 服务地址：http://localhost:3000                    ║
║  📡 API 地址：http://localhost:3000/api                ║
╚════════════════════════════════════════════════════════╝
```

#### 5. 打开前端页面

- 直接打开 `frontend/index.html`
- 或在浏览器访问：`http://localhost:3000`（需要配置静态文件服务）

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/products` | GET | 获取产品列表 |
| `/api/products/:id` | GET | 获取产品详情 |
| `/api/orders` | GET/POST | 订单列表/创建订单 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/admin/orders` | GET | 后台订单列表 |
| `/api/admin/stats` | GET | 后台统计数据 |

## 🗄️ 数据库配置

### 安装 MySQL

推荐使用 phpStudy 一键安装：https://www.xp.cn/

或官方安装：https://dev.mysql.com/downloads/mysql/

### 导入数据库

```bash
# 登录 MySQL
mysql -u root -p

# 执行脚本
source database/schema.sql
```

### 配置连接

编辑 `backend/.env` 文件：
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=visa_db
```

## 📱 功能说明

### 用户端功能
- ✅ 首页展示（Banner、数据统计、服务特色）
- ✅ 签证产品列表
- ✅ 产品详情查看
- ✅ 在线下单
- ✅ 订单查询
- ✅ 用户登录

### 后台功能（开发中）
- ⏳ 订单管理
- ⏳ 产品管理
- ⏳ 数据统计

## 🔧 开发计划

- [ ] 后台管理系统
- [ ] 微信小程序（Uni-app）
- [ ] 支付接口对接
- [ ] 材料上传功能
- [ ] 短信验证码
- [ ] 邮件通知

## ⚠️ 注意事项

1. **演示模式**：未配置数据库时，系统使用内存数据，重启后数据清空
2. **支付功能**：当前为模拟支付，实际使用需对接微信/支付宝
3. **安全性**：演示版本未做完整安全验证，生产环境需加强

## 📞 技术支持

如有问题，请查看控制台日志或联系开发者。
