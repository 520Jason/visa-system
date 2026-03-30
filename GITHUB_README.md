# 🛂 签证办理系统

一个基于 Python FastAPI 的签证在线办理平台，包含用户端 Web、后台管理系统和 API 接口。

## 🌟 功能特点

- ✅ 签证产品展示与搜索
- ✅ 在线下单与订单管理
- ✅ 用户登录注册
- ✅ 后台订单管理
- ✅ 后台产品管理
- ✅ 数据统计仪表盘

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 后端 | Python 3 + FastAPI |
| 数据库 | MySQL 8.0 |
| 前端 | HTML + CSS + JavaScript |
| 部署 | 阿里云 ECS |

## 📁 项目结构

```
visa-project/
├── backend/              # 后端 API
│   ├── main.py           # FastAPI 主程序
│   ├── requirements.txt  # Python 依赖
│   └── .env.example      # 环境配置示例
├── frontend/             # 用户端 Web
│   └── index.html
├── admin/                # 后台管理
│   └── index.html
├── database/             # 数据库脚本
│   └── schema.sql
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库信息
```

### 3. 启动服务

```bash
python main.py
```

### 4. 访问应用

- API 文档：http://localhost:8000/docs
- 用户端：打开 `frontend/index.html`
- 后台管理：打开 `admin/index.html`

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/products | GET | 获取产品列表 |
| /api/products/{id} | GET | 获取产品详情 |
| /api/orders | GET/POST | 订单列表/创建订单 |
| /api/auth/login | POST | 用户登录 |
| /api/admin/orders | GET | 后台订单列表 |
| /api/admin/stats | GET | 后台统计数据 |

## 🗄️ 数据库配置

```sql
CREATE DATABASE visa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

导入 `database/schema.sql` 初始化表结构。

## 📱 微信小程序（开发中）

使用 Uni-app 开发，一套代码编译到 H5 和微信小程序。

## 📄 许可证

MIT License

## 📞 联系

如有问题，请提交 Issue 或联系开发者。
