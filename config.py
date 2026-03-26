"""
配置文件 - config.py
存放 Agent 和 API 的配置参数
"""

from typing import Dict, Any, Optional

# ============ LLM 配置 ============
class LLMConfig:
    """LLM 配置"""
    
    # 支持的 LLM 类型
    SUPPORTED_TYPES = ["ollama", "anthropic", "deepseek", "huggingface"]
    
    # Ollama 配置
    OLLAMA = {
        "host": "http://localhost:11434",
        "model": "llama2-chinese",  # 或 neural-chat, mistral
        "temperature": 0.7,
        "timeout": 60,
    }
    
    # Anthropic 配置
    ANTHROPIC = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "temperature": 0.7,
    }
    
    # DeepSeek 配置
    DEEPSEEK = {
        "api_url": "https://api.deepseek.com/chat/completions",
        "model": "deepseek-chat",
        "max_tokens": 1024,
        "temperature": 0.7,
    }
    
    # HuggingFace 配置
    HUGGINGFACE = {
        "api_url": "https://api-inference.huggingface.co/models",
        "model": "meta-llama/Llama-2-7b-chat",
        "timeout": 120,
    }

# ============ API 服务器配置 ============
class APIConfig:
    """API 服务器配置"""
    
    # 服务器配置
    HOST = "127.0.0.1"
    PORT = 8001
    DEBUG = True
    
    # 功能开关
    FEATURES = {
        "search_restaurants": True,
        "check_availability": True,
        "make_booking": True,
        "get_booking_history": True,
        "cancel_booking": False,  # 待实现
        "modify_booking": False,  # 待实现
    }
    
    # 速率限制
    RATE_LIMIT = {
        "enabled": False,  # POC 关闭速率限制
        "requests_per_minute": 60,
    }
    
    # 日志配置
    LOGGING = {
        "level": "INFO",
        "file": "logs/api.log",
    }

# ============ Agent 配置 ============
class AgentConfig:
    """Agent 配置"""
    
    # 模式
    VERBOSE = True  # 输出详细日志
    
    # 对话配置
    CONVERSATION = {
        "max_history": 50,  # 最多保存对话数
        "enable_memory": True,
    }
    
    # 工具配置
    TOOLS = {
        "timeout": 30,
        "max_retries": 3,
        "auto_reload": True,  # 自动重载工具列表
    }
    
    # Agent 行为
    BEHAVIOR = {
        "think_step_by_step": True,
        "explain_decisions": True,
        "ask_for_confirmation": False,
    }

# ============ 数据库配置 ============
class DatabaseConfig:
    """数据库配置"""
    
    # 模式：memory 或 database
    MODE = "memory"  # POC 使用内存存储
    
    # 如果使用数据库
    DATABASE = {
        "type": "sqlite",  # sqlite, postgresql, mysql
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "password",
        "database": "restaurant_booking",
    }
    
    # 内存存储
    MEMORY_STORAGE = {
        "restaurants_file": "data/restaurants.json",
        "bookings_file": "data/bookings.json",
    }

# ============ 业务配置 ============
class BusinessConfig:
    """业务相关配置"""
    
    # 餐厅配置
    RESTAURANTS = {
        "default_capacity": 100,
        "max_advance_booking_days": 30,
        "business_hours_start": "11:00",
        "business_hours_end": "22:00",
    }
    
    # 预订配置
    BOOKING = {
        "confirmation_required": False,
        "cancellation_allowed_hours_before": 2,
        "max_party_size": 20,
        "min_party_size": 1,
    }
    
    # 通知配置
    NOTIFICATIONS = {
        "send_confirmation": True,
        "send_reminders": False,
        "reminder_hours_before": 24,
    }

# ============ 提示词配置 ============
class PromptConfig:
    """LLM 提示词配置"""
    
    # 系统提示
    SYSTEM_PROMPT = """你是一个专业的餐厅预订助手。
你的职责是帮助用户搜索餐厅、查询可用性和进行预订。
始终用中文回复用户。
当用户表达清晰的意图时，调用相应的工具。
在进行预订前，请确认用户的所有信息。"""
    
    # 工具描述模板
    TOOL_DESCRIPTION_TEMPLATE = """
可用工具：
{tools}

当用户请求某个操作时：
1. 分析用户的意图
2. 识别需要调用的工具
3. 提取必要的参数
4. 返回 JSON 格式: {{"tool": "tool_name", "params": {{...}}}}
"""
    
    # 错误处理提示
    ERROR_PROMPT = """很抱歉，我在处理您的请求时出现了错误。
错误信息：{error}
请稍后重试。"""
    
    # 完成提示
    SUCCESS_PROMPT = """您的请求已成功处理！
结果：{result}"""

# ============ 特性标志 ============
class FeatureFlags:
    """特性标志，用于控制实验性功能"""
    
    # 多轮对话
    MULTI_TURN_CONVERSATION = True
    
    # 用户反馈学习
    LEARNING_FROM_FEEDBACK = False
    
    # 用户偏好记忆
    USER_PREFERENCE_MEMORY = False
    
    # 餐厅推荐
    RECOMMENDATION_ENGINE = False
    
    # 评论集成
    REVIEWS_INTEGRATION = False

# ============ 默认配置 ============
DEFAULT_CONFIG = {
    "llm": LLMConfig.OLLAMA,
    "api": APIConfig.__dict__,
    "agent": AgentConfig.__dict__,
    "database": DatabaseConfig.__dict__,
    "business": BusinessConfig.__dict__,
    "features": FeatureFlags.__dict__,
}

# ============ 工具函数 ============
def get_config(config_type: str, key: Optional[str] = None) -> Any:
    """获取配置"""
    configs = {
        "llm": LLMConfig,
        "api": APIConfig,
        "agent": AgentConfig,
        "database": DatabaseConfig,
        "business": BusinessConfig,
        "prompt": PromptConfig,
        "features": FeatureFlags,
    }
    
    if config_type not in configs:
        raise ValueError(f"未知的配置类型: {config_type}")
    
    config = configs[config_type]
    
    if key:
        return getattr(config, key)
    return config

if __name__ == "__main__":
    # 打印所有配置
    print("LLM 配置:")
    print(f"  Ollama: {LLMConfig.OLLAMA}")
    print(f"  Anthropic: {LLMConfig.ANTHROPIC}")
    print()
    print("API 配置:")
    print(f"  Host: {APIConfig.HOST}:{APIConfig.PORT}")
    print()
    print("Agent 配置:")
    print(f"  Verbose: {AgentConfig.VERBOSE}")
