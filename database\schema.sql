-- 签证办理系统数据库结构
-- 创建数据库
CREATE DATABASE IF NOT EXISTS visa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE visa_db;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    nickname VARCHAR(50) DEFAULT '',
    avatar VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 签证产品表
CREATE TABLE IF NOT EXISTS visa_products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    country VARCHAR(50) NOT NULL COMMENT '国家',
    visa_type VARCHAR(100) NOT NULL COMMENT '签证类型',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    duration VARCHAR(50) DEFAULT '' COMMENT '办理时长',
    materials JSON COMMENT '所需材料',
    description TEXT COMMENT '产品描述',
    status TINYINT DEFAULT 1 COMMENT '1 上架 0 下架',
    sort_order INT DEFAULT 0 COMMENT '排序',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_no VARCHAR(32) UNIQUE NOT NULL COMMENT '订单号',
    user_id INT NOT NULL COMMENT '用户 ID',
    product_id INT NOT NULL COMMENT '产品 ID',
    amount DECIMAL(10,2) NOT NULL COMMENT '金额',
    status TINYINT DEFAULT 0 COMMENT '0 待支付 1 待审核 2 审核中 3 已出签 4 已完成 5 已取消',
    applicant_info JSON COMMENT '申请人信息',
    materials JSON COMMENT '材料文件',
    remark VARCHAR(500) DEFAULT '' COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_order_no (order_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 订单日志表
CREATE TABLE IF NOT EXISTS order_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL COMMENT '订单 ID',
    action VARCHAR(50) NOT NULL COMMENT '操作类型',
    remark VARCHAR(255) DEFAULT '' COMMENT '备注',
    operator_id INT DEFAULT 0 COMMENT '操作人 ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 支付记录表
CREATE TABLE IF NOT EXISTS payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL COMMENT '订单 ID',
    payment_type VARCHAR(20) NOT NULL COMMENT 'wechat/alipay',
    transaction_id VARCHAR(100) DEFAULT '' COMMENT '第三方交易号',
    amount DECIMAL(10,2) NOT NULL COMMENT '金额',
    status TINYINT DEFAULT 0 COMMENT '0 未支付 1 已支付',
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_id (order_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 管理员表
CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    nickname VARCHAR(50) DEFAULT '',
    role VARCHAR(20) DEFAULT 'admin',
    status TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入示例数据
INSERT INTO visa_products (country, visa_type, price, duration, materials, description) VALUES
('日本', '旅游签证 - 单次', 299.00, '5-7 工作日', '["护照原件", "照片 2 张", "身份证复印件", "申请表"]', '日本个人旅游签证，有效期 3 个月，停留 15 天'),
('泰国', '旅游签证', 199.00, '3-5 工作日', '["护照原件", "照片 2 张", "往返机票"]', '泰国落地签/电子签，有效期 3 个月，停留 30 天'),
('越南', '旅游签证 - 单次', 159.00, '3-5 工作日', '["护照原件", "照片 2 张"]', '越南电子签证，有效期 1 个月，停留 30 天'),
('新加坡', '旅游签证', 259.00, '3-5 工作日', '["护照原件", "照片 2 张", "身份证复印件", "在职证明"]', '新加坡电子签证，有效期 2 年，停留 30 天'),
('韩国', '旅游签证 - 单次', 399.00, '5-7 工作日', '["护照原件", "照片 1 张", "身份证复印件", "银行流水"]', '韩国个人旅游签证，有效期 3 个月，停留 90 天'),
('美国', 'B1/B2 旅游商务', 1299.00, '30-60 工作日', '["护照原件", "照片 1 张", "DS160 表", "面签"]', '美国十年多次往返签证，需面签');

-- 插入默认管理员 (密码：admin123)
INSERT INTO admins (username, password, nickname) VALUES
('admin', '$2a$10$XQxHjNzHcKzU5N5qF5qF5.5qF5qF5qF5qF5qF5qF5qF5qF5qF5qF5', '超级管理员');
