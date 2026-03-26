from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
import json

app = FastAPI(title="Restaurant Booking API")

# ============ 数据模型 ============
class Tool(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    
class BookingRequest(BaseModel):
    restaurant_name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    people_count: int
    customer_name: str
    phone: str
    
class AvailabilityRequest(BaseModel):
    restaurant_name: str
    date: str  # YYYY-MM-DD

class RestaurantSearchRequest(BaseModel):
    location: str
    cuisine_type: Optional[str] = None
    
# ============ 模拟数据库 ============
RESTAURANTS_DB = {
    "金牌川菜馆": {
        "location": "中关村",
        "cuisine": "四川菜",
        "rating": 4.8,
        "phone": "010-12345678",
        "capacity": 100
    },
    "精品粤菜": {
        "location": "银座",
        "cuisine": "粤菜",
        "rating": 4.6,
        "phone": "010-87654321",
        "capacity": 80
    },
    "日本寿司店": {
        "location": "朝阳",
        "cuisine": "日本菜",
        "rating": 4.7,
        "phone": "010-99999999",
        "capacity": 50
    },
    "意大利披萨": {
        "location": "建国路",
        "cuisine": "意大利菜",
        "rating": 4.5,
        "phone": "010-11111111",
        "capacity": 60
    }
}

BOOKINGS_DB = []

# ============ 工具定义 ============
AVAILABLE_TOOLS = [
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
    {
        "name": "make_booking",
        "description": "预订餐厅",
        "parameters": {
            "restaurant_name": {"type": "string", "description": "餐厅名称"},
            "date": {"type": "string", "description": "日期 (YYYY-MM-DD)"},
            "time": {"type": "string", "description": "时间 (HH:MM)"},
            "people_count": {"type": "integer", "description": "人数"},
            "customer_name": {"type": "string", "description": "客户名称"},
            "phone": {"type": "string", "description": "联系电话"}
        }
    },
    {
        "name": "get_booking_history",
        "description": "获取预订历史记录",
        "parameters": {
            "customer_phone": {"type": "string", "description": "客户电话"}
        }
    }
]

# ============ API 路由 ============
@app.get("/tools")
async def list_tools():
    """获取所有可用工具"""
    return {
        "tools": AVAILABLE_TOOLS,
        "tool_count": len(AVAILABLE_TOOLS)
    }

@app.post("/tools/search_restaurants")
async def search_restaurants(request: RestaurantSearchRequest):
    """搜索餐厅"""
    results = []
    for name, info in RESTAURANTS_DB.items():
        # 按地点过滤
        if request.location.lower() not in info["location"].lower():
            continue
        # 按菜系过滤
        if request.cuisine_type and request.cuisine_type.lower() not in info["cuisine"].lower():
            continue
        results.append({
            "name": name,
            "location": info["location"],
            "cuisine": info["cuisine"],
            "rating": info["rating"],
            "phone": info["phone"]
        })
    
    return {
        "status": "success",
        "count": len(results),
        "restaurants": results
    }

@app.post("/tools/check_availability")
async def check_availability(request: AvailabilityRequest):
    """检查可用时间"""
    if request.restaurant_name not in RESTAURANTS_DB:
        raise HTTPException(status_code=404, detail="餐厅不存在")
    
    # 模拟可用时间
    available_times = []
    for hour in range(11, 22):
        available_count = random.randint(2, 10)
        available_times.append({
            "time": f"{hour:02d}:00",
            "available_tables": available_count
        })
    
    return {
        "status": "success",
        "restaurant": request.restaurant_name,
        "date": request.date,
        "available_times": available_times
    }

@app.post("/tools/make_booking")
async def make_booking(request: BookingRequest):
    """预订餐厅"""
    if request.restaurant_name not in RESTAURANTS_DB:
        raise HTTPException(status_code=404, detail="餐厅不存在")
    
    if request.people_count > RESTAURANTS_DB[request.restaurant_name]["capacity"]:
        raise HTTPException(status_code=400, detail="人数超过餐厅容量")
    
    # 生成预订ID
    booking_id = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
    
    booking = {
        "booking_id": booking_id,
        "restaurant": request.restaurant_name,
        "date": request.date,
        "time": request.time,
        "people_count": request.people_count,
        "customer_name": request.customer_name,
        "phone": request.phone,
        "status": "confirmed",
        "created_at": datetime.now().isoformat()
    }
    
    BOOKINGS_DB.append(booking)
    
    return {
        "status": "success",
        "message": f"预订成功",
        "booking_id": booking_id,
        "booking_details": booking
    }

@app.post("/tools/get_booking_history")
async def get_booking_history(request: Dict[str, str]):
    """获取预订历史"""
    phone = request.get("customer_phone")
    history = [b for b in BOOKINGS_DB if b["phone"] == phone]
    
    return {
        "status": "success",
        "phone": phone,
        "count": len(history),
        "bookings": history
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
