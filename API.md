# 🌐 API 参考文档

## 概览

所有工具 API 都采用 REST 风格，支持 JSON 请求和响应。

**基础 URL:** `http://127.0.0.1:8001`

**认证:** 无（POC 版本）

**超时:** 30 秒

---

## 📋 通用响应格式

所有响应都遵循这种格式：

```json
{
  "status": "success|error",
  "message": "操作描述",
  "data": { /* 具体数据 */ },
  "timestamp": "2024-03-25T10:30:00"
}
```

### 响应状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

---

## 🔧 工具 API 详解

### 1. 搜索餐厅 (search_restaurants)

搜索符合条件的餐厅

**方法:** `POST`

**端点:** `/tools/search_restaurants`

**请求体:**

```json
{
  "location": "中关村",
  "cuisine_type": "四川菜"
}
```

**参数说明:**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| location | string | ✅ | 地点/地区 |
| cuisine_type | string | ❌ | 菜系类型（可选） |

**示例请求:**

```bash
curl -X POST http://127.0.0.1:8001/tools/search_restaurants \
  -H "Content-Type: application/json" \
  -d '{
    "location": "中关村",
    "cuisine_type": "四川菜"
  }'
```

**成功响应 (200):**

```json
{
  "status": "success",
  "count": 1,
  "restaurants": [
    {
      "name": "金牌川菜馆",
      "location": "中关村",
      "cuisine": "四川菜",
      "rating": 4.8,
      "phone": "010-12345678"
    }
  ]
}
```

**错误响应 (400):**

```json
{
  "status": "error",
  "message": "location 参数必需"
}
```

**使用示例:**

| 场景 | 请求 |
|------|------|
| 查找特定地点 | `{"location": "银座"}` |
| 查找某菜系 | `{"location": "朝阳", "cuisine_type": "日本菜"}` |
| 查找所有地点 | `{"location": ""}` |

---

### 2. 查询可用时间 (check_availability)

查询餐厅在特定日期的可用时间和空位

**方法:** `POST`

**端点:** `/tools/check_availability`

**请求体:**

```json
{
  "restaurant_name": "金牌川菜馆",
  "date": "2024-12-25"
}
```

**参数说明:**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| restaurant_name | string | ✅ | 餐厅名称 |
| date | string | ✅ | 日期 (YYYY-MM-DD 格式) |

**日期格式:**
- 格式: `YYYY-MM-DD`
- 示例: `2024-12-25`
- 范围: 今天到 30 天后

**示例请求:**

```bash
curl -X POST http://127.0.0.1:8001/tools/check_availability \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_name": "金牌川菜馆",
    "date": "2024-12-25"
  }'
```

**成功响应 (200):**

```json
{
  "status": "success",
  "restaurant": "金牌川菜馆",
  "date": "2024-12-25",
  "available_times": [
    {
      "time": "11:00",
      "available_tables": 5
    },
    {
      "time": "12:00",
      "available_tables": 3
    },
    {
      "time": "19:00",
      "available_tables": 8
    }
  ]
}
```

**错误响应 (404):**

```json
{
  "status": "error",
  "message": "餐厅不存在",
  "restaurant": "未知餐厅"
}
```

**时间说明:**
- 时间段: 11:00 - 22:00
- 间隔: 1 小时
- available_tables: 当前时段可用座位数

---

### 3. 预订餐厅 (make_booking)

为用户预订餐厅

**方法:** `POST`

**端点:** `/tools/make_booking`

**请求体:**

```json
{
  "restaurant_name": "金牌川菜馆",
  "date": "2024-12-25",
  "time": "19:00",
  "people_count": 4,
  "customer_name": "张三",
  "phone": "13800138000"
}
```

**参数说明:**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| restaurant_name | string | ✅ | 餐厅名称 |
| date | string | ✅ | 预订日期 (YYYY-MM-DD) |
| time | string | ✅ | 预订时间 (HH:MM) |
| people_count | integer | ✅ | 人数 (1-20) |
| customer_name | string | ✅ | 客户名字 |
| phone | string | ✅ | 联系电话 |

**验证规则:**
- `people_count`: 1-20 人
- `date`: 今天到 30 天后
- `time`: 11:00-22:00
- `phone`: 有效电话格式

**示例请求:**

```bash
curl -X POST http://127.0.0.1:8001/tools/make_booking \
  -H "Content-Type: application/json" \
  -d '{
    "restaurant_name": "金牌川菜馆",
    "date": "2024-12-25",
    "time": "19:00",
    "people_count": 4,
    "customer_name": "张三",
    "phone": "13800138000"
  }'
```

**成功响应 (200):**

```json
{
  "status": "success",
  "message": "预订成功",
  "booking_id": "BK202403251930012345",
  "booking_details": {
    "booking_id": "BK202403251930012345",
    "restaurant": "金牌川菜馆",
    "date": "2024-12-25",
    "time": "19:00",
    "people_count": 4,
    "customer_name": "张三",
    "phone": "13800138000",
    "status": "confirmed",
    "created_at": "2024-03-25T19:30:45.123456"
  }
}
```

**错误响应 (400):**

```json
{
  "status": "error",
  "message": "人数超过餐厅容量"
}
```

**错误响应 (404):**

```json
{
  "status": "error",
  "message": "餐厅不存在"
}
```

**预订 ID 说明:**
- 格式: `BK` + 时间戳 + 随机数
- 用途: 唯一标识预订
- 示例: `BK202403251930012345`

---

### 4. 查询预订历史 (get_booking_history)

获取某客户的预订历史记录

**方法:** `POST`

**端点:** `/tools/get_booking_history`

**请求体:**

```json
{
  "customer_phone": "13800138000"
}
```

**参数说明:**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| customer_phone | string | ✅ | 客户电话 |

**示例请求:**

```bash
curl -X POST http://127.0.0.1:8001/tools/get_booking_history \
  -H "Content-Type: application/json" \
  -d '{
    "customer_phone": "13800138000"
  }'
```

**成功响应 (200):**

```json
{
  "status": "success",
  "phone": "13800138000",
  "count": 2,
  "bookings": [
    {
      "booking_id": "BK202403251930012345",
      "restaurant": "金牌川菜馆",
      "date": "2024-12-25",
      "time": "19:00",
      "people_count": 4,
      "customer_name": "张三",
      "phone": "13800138000",
      "status": "confirmed",
      "created_at": "2024-03-25T19:30:45.123456"
    },
    {
      "booking_id": "BK202403262000054321",
      "restaurant": "精品粤菜",
      "date": "2024-12-26",
      "time": "20:00",
      "people_count": 2,
      "customer_name": "张三",
      "phone": "13800138000",
      "status": "confirmed",
      "created_at": "2024-03-25T20:00:30.789012"
    }
  ]
}
```

**空结果响应 (200):**

```json
{
  "status": "success",
  "phone": "13800138000",
  "count": 0,
  "bookings": []
}
```

---

### 5. 健康检查 (health)

检查 API 服务器运行状态

**方法:** `GET`

**端点:** `/health`

**示例请求:**

```bash
curl http://127.0.0.1:8001/health
```

**响应:**

```json
{
  "status": "healthy",
  "timestamp": "2024-03-25T19:30:45.123456"
}
```

---

## 🛠️ 工具列表 API

### 获取所有可用工具

**方法:** `GET`

**端点:** `/tools`

**示例请求:**

```bash
curl http://127.0.0.1:8001/tools
```

**响应:**

```json
{
  "tools": [
    {
      "name": "search_restaurants",
      "description": "搜索符合条件的餐厅",
      "parameters": {
        "location": {"type": "string", "description": "地点"},
        "cuisine_type": {"type": "string", "description": "菜系类型（可选）"}
      }
    },
    {
      "name": "check_availability",
      "description": "检查餐厅在特定日期的可用时间",
      "parameters": {
        "restaurant_name": {"type": "string", "description": "餐厅名称"},
        "date": {"type": "string", "description": "日期 (YYYY-MM-DD)"}
      }
    },
    // ... 省略其他工具 ...
  ],
  "tool_count": 4
}
```

---

## 📊 工作流示例

### 完整预订流程

#### 步骤 1: 搜索餐厅

```bash
POST /tools/search_restaurants
{
  "location": "中关村",
  "cuisine_type": "四川菜"
}
```

**响应:**
```json
{
  "status": "success",
  "count": 1,
  "restaurants": [
    {
      "name": "金牌川菜馆",
      "rating": 4.8
    }
  ]
}
```

#### 步骤 2: 查询可用时间

```bash
POST /tools/check_availability
{
  "restaurant_name": "金牌川菜馆",
  "date": "2024-12-25"
}
```

**响应:**
```json
{
  "status": "success",
  "available_times": [
    {"time": "19:00", "available_tables": 8}
  ]
}
```

#### 步骤 3: 进行预订

```bash
POST /tools/make_booking
{
  "restaurant_name": "金牌川菜馆",
  "date": "2024-12-25",
  "time": "19:00",
  "people_count": 4,
  "customer_name": "张三",
  "phone": "13800138000"
}
```

**响应:**
```json
{
  "status": "success",
  "booking_id": "BK202403251930012345"
}
```

#### 步骤 4: 查询历史

```bash
POST /tools/get_booking_history
{
  "customer_phone": "13800138000"
}
```

**响应:**
```json
{
  "status": "success",
  "count": 1,
  "bookings": [
    {
      "booking_id": "BK202403251930012345",
      "restaurant": "金牌川菜馆"
    }
  ]
}
```

---

## 🔍 数据类型详解

### 餐厅对象

```json
{
  "name": "string",        // 餐厅名称
  "location": "string",    // 地理位置
  "cuisine": "string",     // 菜系
  "rating": 4.8,          // 评分 (0-5)
  "phone": "string"       // 电话
}
```

### 预订对象

```json
{
  "booking_id": "BK...",   // 预订 ID
  "restaurant": "string",  // 餐厅名
  "date": "2024-12-25",   // 日期
  "time": "19:00",        // 时间
  "people_count": 4,      // 人数
  "customer_name": "string", // 客户名
  "phone": "string",      // 电话
  "status": "confirmed",  // 状态
  "created_at": "ISO8601" // 创建时间
}
```

### 工具定义对象

```json
{
  "name": "string",       // 工具名称
  "description": "string", // 描述
  "parameters": {         // 参数定义
    "param_name": {
      "type": "string|integer|boolean",
      "description": "string"
    }
  }
}
```

---

## ⚠️ 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 400 Bad Request | 参数缺失或格式错误 | 检查请求参数 |
| 404 Not Found | 餐厅不存在 | 先使用 search_restaurants 查询 |
| 422 Validation Error | 参数类型不匹配 | 检查参数类型 |
| 500 Server Error | 服务器错误 | 检查服务器日志 |

---

## 🔐 安全建议

- ❌ 不要在 URL 中传输敏感信息
- ❌ 不要记录真实用户电话（生产环境）
- ✅ 使用 HTTPS（生产环境）
- ✅ 实施 API 速率限制
- ✅ 添加身份认证

---

## 📈 性能优化

- **缓存**: 搜索结果可缓存 5 分钟
- **分页**: 搜索结果支持分页（待实现）
- **批量操作**: 支持批量查询（待实现）

---

## 🔄 最后更新

**日期:** 2024-03-25  
**版本:** 1.0  
**状态:** POC (Proof of Concept)

---

## 📞 获取帮助

- 查看 `README.md` 获取更多信息
- 查看 `QUICKSTART.md` 快速开始
- 运行 `test_poc.py` 验证 API
- 访问 Swagger UI: http://localhost:8001/docs
