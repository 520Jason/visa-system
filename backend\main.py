"""
🛂 签证办理系统 - 后端 API
技术栈：Python + FastAPI + MySQL
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import mysql.connector
import os
import random
import string
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ==================== 应用初始化 ====================

app = FastAPI(
    title="签证办理系统 API",
    description="一站式智能签证办理平台",
    version="1.0.0"
)

# CORS 配置（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 数据库配置 ====================

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "visa_db"),
            charset="utf8mb4"
        )
        return conn
    except Exception as e:
        print(f"数据库连接失败：{e}")
        return None

# 检查是否使用数据库
DB_AVAILABLE = get_db_connection() is not None
if DB_AVAILABLE:
    print("✅ 数据库连接成功")
else:
    print("⚠️  数据库连接失败，使用内存数据模式")

# ==================== 内存数据（演示用） ====================

memory_data = {
    "users": [],
    "products": [
        {
            "id": 1,
            "country": "日本",
            "visa_type": "旅游签证 - 单次",
            "price": 299.00,
            "duration": "5-7 工作日",
            "materials": ["护照原件", "照片 2 张", "身份证复印件", "申请表"],
            "description": "日本个人旅游签证，有效期 3 个月，停留 15 天",
            "status": 1
        },
        {
            "id": 2,
            "country": "泰国",
            "visa_type": "旅游签证",
            "price": 199.00,
            "duration": "3-5 工作日",
            "materials": ["护照原件", "照片 2 张", "往返机票"],
            "description": "泰国落地签/电子签，有效期 3 个月，停留 30 天",
            "status": 1
        },
        {
            "id": 3,
            "country": "越南",
            "visa_type": "旅游签证 - 单次",
            "price": 159.00,
            "duration": "3-5 工作日",
            "materials": ["护照原件", "照片 2 张"],
            "description": "越南电子签证，有效期 1 个月，停留 30 天",
            "status": 1
        },
        {
            "id": 4,
            "country": "新加坡",
            "visa_type": "旅游签证",
            "price": 259.00,
            "duration": "3-5 工作日",
            "materials": ["护照原件", "照片 2 张", "身份证复印件", "在职证明"],
            "description": "新加坡电子签证，有效期 2 年，停留 30 天",
            "status": 1
        },
        {
            "id": 5,
            "country": "韩国",
            "visa_type": "旅游签证 - 单次",
            "price": 399.00,
            "duration": "5-7 工作日",
            "materials": ["护照原件", "照片 1 张", "身份证复印件", "银行流水"],
            "description": "韩国个人旅游签证，有效期 3 个月，停留 90 天",
            "status": 1
        },
        {
            "id": 6,
            "country": "美国",
            "visa_type": "B1/B2 旅游商务",
            "price": 1299.00,
            "duration": "30-60 工作日",
            "materials": ["护照原件", "照片 1 张", "DS160 表", "面签"],
            "description": "美国十年多次往返签证，需面签",
            "status": 1
        }
    ],
    "orders": []
}

# ==================== 数据模型 ====================

class UserLogin(BaseModel):
    phone: str
    password: str

class UserRegister(BaseModel):
    phone: str
    password: str
    nickname: Optional[str] = None

class OrderCreate(BaseModel):
    userId: Optional[int] = None
    productId: int
    applicantInfo: Optional[Dict[str, Any]] = None
    materials: Optional[List[str]] = None
    remark: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: int
    remark: Optional[str] = None

class ProductCreate(BaseModel):
    country: str
    visa_type: str
    price: float
    duration: Optional[str] = None
    materials: Optional[List[str]] = None
    description: Optional[str] = None
    status: Optional[int] = 1

# ==================== 辅助函数 ====================

def generate_order_no():
    """生成订单号"""
    return "V" + str(datetime.now().timestamp()).replace(".", "")[:13] + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )

def query_db(sql: str, params: tuple = None):
    """执行数据库查询"""
    if not DB_AVAILABLE:
        return None
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"查询错误：{e}")
        return None

def execute_db(sql: str, params: tuple = None):
    """执行数据库更新"""
    if not DB_AVAILABLE:
        return None
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
    except Exception as e:
        print(f"执行错误：{e}")
        conn.rollback()
        return None

# ==================== API 接口 ====================

@app.get("/")
def read_root():
    """API 首页"""
    return {
        "message": "🛂 签证办理系统 API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "products": "GET /api/products",
            "product_detail": "GET /api/products/{id}",
            "orders": "GET/POST /api/orders",
            "auth_login": "POST /api/auth/login",
            "auth_register": "POST /api/auth/register",
            "admin_orders": "GET /api/admin/orders",
            "admin_stats": "GET /api/admin/stats"
        }
    }

@app.get("/api")
def api_root():
    """API 信息"""
    return read_root()

# ------------------- 产品接口 -------------------

@app.get("/api/products")
def get_products():
    """获取产品列表"""
    if DB_AVAILABLE:
        products = query_db("SELECT * FROM visa_products WHERE status = 1 ORDER BY sort_order, id")
        if products:
            return {"code": 0, "data": products}
    return {"code": 0, "data": memory_data["products"]}

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    """获取产品详情"""
    if DB_AVAILABLE:
        products = query_db("SELECT * FROM visa_products WHERE id = %s", (product_id,))
        if products:
            return {"code": 0, "data": products[0]}
        return {"code": 1, "message": "产品不存在"}
    
    product = next((p for p in memory_data["products"] if p["id"] == product_id), None)
    if product:
        return {"code": 0, "data": product}
    return {"code": 1, "message": "产品不存在"}

# ------------------- 订单接口 -------------------

@app.get("/api/orders")
def get_orders(userId: Optional[int] = None):
    """获取订单列表"""
    if DB_AVAILABLE:
        if userId:
            orders = query_db("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (userId,))
        else:
            orders = query_db("SELECT * FROM orders ORDER BY created_at DESC")
        if orders is not None:
            return {"code": 0, "data": orders}
    
    orders = memory_data["orders"]
    if userId:
        orders = [o for o in orders if o.get("userId") == userId]
    return {"code": 0, "data": orders}

@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    """获取订单详情"""
    if DB_AVAILABLE:
        orders = query_db("SELECT * FROM orders WHERE id = %s", (order_id,))
        if orders:
            return {"code": 0, "data": orders[0]}
        return {"code": 1, "message": "订单不存在"}
    
    order = next((o for o in memory_data["orders"] if o["id"] == order_id), None)
    if order:
        return {"code": 0, "data": order}
    return {"code": 1, "message": "订单不存在"}

@app.post("/api/orders")
def create_order(order: OrderCreate):
    """创建订单"""
    order_no = generate_order_no()
    
    # 获取产品价格
    product = None
    if DB_AVAILABLE:
        products = query_db("SELECT price FROM visa_products WHERE id = %s", (order.productId,))
        if products:
            product = products[0]
    else:
        product = next((p for p in memory_data["products"] if p["id"] == order.productId), None)
    
    amount = product["price"] if product else 0
    
    if DB_AVAILABLE:
        sql = """INSERT INTO orders 
                 (order_no, user_id, product_id, amount, status, applicant_info, materials, remark) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        order_id = execute_db(sql, (
            order_no,
            order.userId or 1,
            order.productId,
            amount,
            0,  # 待支付
            str(order.applicantInfo or {}),
            str(order.materials or []),
            order.remark or ""
        ))
        if order_id:
            new_order = query_db("SELECT * FROM orders WHERE id = %s", (order_id,))
            return {"code": 0, "data": new_order[0], "message": "订单创建成功"}
    else:
        new_order = {
            "id": len(memory_data["orders"]) + 1,
            "orderNo": order_no,
            "userId": order.userId or 1,
            "productId": order.productId,
            "amount": amount,
            "status": 0,
            "applicantInfo": order.applicantInfo or {},
            "materials": order.materials or [],
            "remark": order.remark or "",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        memory_data["orders"].append(new_order)
        return {"code": 0, "data": new_order, "message": "订单创建成功"}
    
    return {"code": 1, "message": "创建失败"}

# ------------------- 认证接口 -------------------

@app.post("/api/auth/login")
def login(user: UserLogin):
    """用户登录"""
    # 简化版：任意手机号密码都能登录
    user_data = {
        "id": 1,
        "phone": user.phone,
        "nickname": "测试用户",
        "avatar": ""
    }
    
    if DB_AVAILABLE:
        users = query_db("SELECT id, phone, nickname, avatar FROM users WHERE phone = %s", (user.phone,))
        if users:
            user_data = users[0]
    
    return {
        "code": 0,
        "data": {
            "user": user_data,
            "token": "demo_token_" + str(datetime.now().timestamp())
        },
        "message": "登录成功"
    }

@app.post("/api/auth/register")
def register(user: UserRegister):
    """用户注册"""
    if DB_AVAILABLE:
        sql = "INSERT INTO users (phone, password, nickname) VALUES (%s, %s, %s)"
        user_id = execute_db(sql, (user.phone, user.password, user.nickname or "新用户"))
        if user_id:
            return {"code": 0, "data": {"id": user_id, "phone": user.phone}, "message": "注册成功"}
    else:
        new_user = {
            "id": len(memory_data["users"]) + 1,
            "phone": user.phone,
            "nickname": user.nickname or "新用户"
        }
        memory_data["users"].append(new_user)
        return {"code": 0, "data": new_user, "message": "注册成功"}
    
    return {"code": 1, "message": "注册失败"}

# ------------------- 支付接口 -------------------

@app.post("/api/pay/create")
def create_payment(orderId: int, type: str = "wechat"):
    """创建支付订单"""
    return {
        "code": 0,
        "data": {
            "orderId": orderId,
            "type": type,
            "payUrl": "https://example.com/pay",
            "message": "支付订单创建成功（演示模式）"
        }
    }

@app.post("/api/pay/notify")
def payment_notify():
    """支付回调通知"""
    return {"code": 0, "message": "收到回调"}

# ------------------- 后台管理接口 -------------------

@app.get("/api/admin/orders")
def admin_get_orders():
    """后台 - 获取订单列表"""
    if DB_AVAILABLE:
        orders = query_db("SELECT * FROM orders ORDER BY created_at DESC")
        if orders is not None:
            return {"code": 0, "data": orders}
    return {"code": 0, "data": memory_data["orders"]}

@app.put("/api/admin/orders/{order_id}/status")
def admin_update_order_status(order_id: int, update: OrderStatusUpdate):
    """后台 - 更新订单状态"""
    if DB_AVAILABLE:
        sql = "UPDATE orders SET status = %s, remark = %s, updated_at = NOW() WHERE id = %s"
        execute_db(sql, (update.status, update.remark or "", order_id))
        order = query_db("SELECT * FROM orders WHERE id = %s", (order_id,))
        if order:
            return {"code": 0, "data": order[0], "message": "更新成功"}
    else:
        order = next((o for o in memory_data["orders"] if o["id"] == order_id), None)
        if order:
            order["status"] = update.status
            order["remark"] = update.remark or ""
            order["updatedAt"] = datetime.now().isoformat()
            return {"code": 0, "data": order, "message": "更新成功"}
    
    return {"code": 1, "message": "订单不存在"}

@app.get("/api/admin/stats")
def admin_get_stats():
    """后台 - 获取统计数据"""
    if DB_AVAILABLE:
        total = query_db("SELECT COUNT(*) as count FROM orders")
        pending = query_db("SELECT COUNT(*) as count FROM orders WHERE status = 0")
        processing = query_db("SELECT COUNT(*) as count FROM orders WHERE status IN (1, 2)")
        completed = query_db("SELECT COUNT(*) as count FROM orders WHERE status IN (3, 4)")
        revenue = query_db("SELECT SUM(amount) as total FROM orders WHERE status >= 1")
        
        return {
            "code": 0,
            "data": {
                "totalOrders": total[0]["count"] if total else 0,
                "pendingOrders": pending[0]["count"] if pending else 0,
                "processingOrders": processing[0]["count"] if processing else 0,
                "completedOrders": completed[0]["count"] if completed else 0,
                "totalRevenue": float(revenue[0]["total"] or 0) if revenue else 0
            }
        }
    
    orders = memory_data["orders"]
    return {
        "code": 0,
        "data": {
            "totalOrders": len(orders),
            "pendingOrders": len([o for o in orders if o["status"] == 0]),
            "processingOrders": len([o for o in orders if o["status"] in [1, 2]]),
            "completedOrders": len([o for o in orders if o["status"] in [3, 4]]),
            "totalRevenue": sum([o["amount"] for o in orders if o["status"] >= 1])
        }
    }

@app.get("/api/admin/users")
def admin_get_users():
    """后台 - 获取用户列表"""
    if DB_AVAILABLE:
        users = query_db("SELECT id, phone, nickname, avatar, created_at FROM users ORDER BY created_at DESC")
        if users is not None:
            return {"code": 0, "data": users}
    return {"code": 0, "data": memory_data["users"]}

# ------------------- 产品管理接口 -------------------

@app.post("/api/admin/products")
def admin_create_product(product: ProductCreate):
    """后台 - 创建产品"""
    if DB_AVAILABLE:
        sql = """INSERT INTO visa_products 
                 (country, visa_type, price, duration, materials, description, status) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        product_id = execute_db(sql, (
            product.country,
            product.visa_type,
            product.price,
            product.duration or "",
            str(product.materials or []),
            product.description or "",
            product.status or 1
        ))
        if product_id:
            new_product = query_db("SELECT * FROM visa_products WHERE id = %s", (product_id,))
            return {"code": 0, "data": new_product[0], "message": "创建成功"}
    else:
        new_product = {
            "id": len(memory_data["products"]) + 1,
            "country": product.country,
            "visa_type": product.visa_type,
            "price": product.price,
            "duration": product.duration or "",
            "materials": product.materials or [],
            "description": product.description or "",
            "status": product.status or 1
        }
        memory_data["products"].append(new_product)
        return {"code": 0, "data": new_product, "message": "创建成功"}
    
    return {"code": 1, "message": "创建失败"}

@app.put("/api/admin/products/{product_id}")
def admin_update_product(product_id: int, product: ProductCreate):
    """后台 - 更新产品"""
    if DB_AVAILABLE:
        sql = """UPDATE visa_products 
                 SET country=%s, visa_type=%s, price=%s, duration=%s, 
                     materials=%s, description=%s, status=%s 
                 WHERE id=%s"""
        execute_db(sql, (
            product.country,
            product.visa_type,
            product.price,
            product.duration or "",
            str(product.materials or []),
            product.description or "",
            product.status or 1,
            product_id
        ))
        updated = query_db("SELECT * FROM visa_products WHERE id = %s", (product_id,))
        if updated:
            return {"code": 0, "data": updated[0], "message": "更新成功"}
    else:
        idx = next((i for i, p in enumerate(memory_data["products"]) if p["id"] == product_id), None)
        if idx is not None:
            memory_data["products"][idx] = {
                **memory_data["products"][idx],
                "country": product.country,
                "visa_type": product.visa_type,
                "price": product.price,
                "duration": product.duration or "",
                "description": product.description or "",
                "status": product.status or 1
            }
            return {"code": 0, "data": memory_data["products"][idx], "message": "更新成功"}
    
    return {"code": 1, "message": "产品不存在"}

@app.delete("/api/admin/products/{product_id}")
def admin_delete_product(product_id: int):
    """后台 - 删除产品"""
    if DB_AVAILABLE:
        execute_db("UPDATE visa_products SET status = 0 WHERE id = %s", (product_id,))
        return {"code": 0, "message": "删除成功"}
    else:
        memory_data["products"] = [p for p in memory_data["products"] if p["id"] != product_id]
        return {"code": 0, "message": "删除成功"}

# ==================== 启动应用 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000))
    )
