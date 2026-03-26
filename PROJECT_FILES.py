"""
完整项目文件清单和快速导航
"""

PROJECT_STRUCTURE = """
🍽️ 餐厅预订 Agent POC - 完整项目文件清单
════════════════════════════════════════════════════════════

📂 apipoc/ (项目根目录)
│
├── 🤖 核心代码 (8 个 Python 文件)
│   ├── api_server.py              ⭐ FastAPI 服务器 (工具 API)
│   ├── agent.py                   ⭐ LangGraph Agent + LLM 客户端
│   ├── langgraph_agent.py         🔵 高级 LangGraph 实现
│   ├── config.py                  ⚙️  配置管理系统
│   ├── run_poc.py                 ⭐ POC 主程序 (运行这个!)
│   ├── test_poc.py                🧪 自动化测试
│   ├── verify_project.py          ✓  项目验证脚本
│   └── langgraph_agent.py         📊 高级实现示例
│
├── 📖 完整文档 (5 个 Markdown 文件)
│   ├── README.md                  📚 完整项目文档 (500+ 行)
│   ├── QUICKSTART.md              ⚡ 30秒快速启动
│   ├── SUMMARY.md                 📋 项目总结和架构
│   ├── API.md                     🌐 API 参考文档
│   └── PROJECT_COMPLETION.md      🎉 完成总结
│
├── ⚙️  配置文件 (5 个)
│   ├── requirements.txt           📦 Python 依赖
│   ├── .env                       🔐 环境变量 (实际)
│   ├── .env.example               🔐 环境变量 (模板)
│   ├── Dockerfile                 🐳 Docker 镜像
│   └── docker-compose.yml         🐳 Docker 编排
│
├── 🚀 启动脚本 (2 个)
│   ├── start.bat                  ⚡ Windows 快速启动
│   └── start.sh                   ⚡ Linux/Mac 快速启动
│
└── 📄 本文件
    └── PROJECT_FILES.py           (你在这里)
"""

QUICK_NAVIGATION = {
    "🚀 我想立即启动项目": [
        "1. 阅读: QUICKSTART.md (5 分钟)",
        "2. 运行: python verify_project.py (检查环境)",
        "3. 执行: python run_poc.py (启动应用)",
        "4. 测试: 输入中文请求，Agent 会处理"
    ],
    
    "📚 我想详细了解项目": [
        "1. 开始: README.md (项目总体说明)",
        "2. 架构: SUMMARY.md (工作原理)",
        "3. API: API.md (工具 API 参考)",
        "4. 代码: agent.py (Agent 实现)"
    ],
    
    "🔧 我想修改或扩展功能": [
        "1. 了解: config.py (配置系统)",
        "2. 学习: agent.py (Agent 逻辑)",
        "3. 扩展: api_server.py (添加新工具)",
        "4. 测试: test_poc.py (验证更改)"
    ],
    
    "🐳 我想用 Docker 部署": [
        "1. 构建: docker build -t agent:latest .",
        "2. 运行: docker run -p 8001:8001 agent:latest",
        "3. 或者: docker-compose up -d",
        "4. 访问: http://localhost:8001/health"
    ],
    
    "🆘 出现问题时": [
        "1. 运行: python verify_project.py (诊断环境)",
        "2. 查看: README.md 的故障排除部分",
        "3. 测试: python test_poc.py (验证功能)",
        "4. 日志: 查看终端输出的错误信息"
    ]
}

FILE_DESCRIPTIONS = {
    "api_server.py": {
        "描述": "FastAPI 服务器，提供 4 个工具 API",
        "工具": [
            "search_restaurants - 搜索餐厅",
            "check_availability - 查询可用时间",
            "make_booking - 预订餐厅",
            "get_booking_history - 查询历史"
        ],
        "启动方式": "自动 (run_poc.py 会启动)",
        "端口": "8001",
        "修改场景": "添加新工具、修改业务逻辑"
    },
    
    "agent.py": {
        "描述": "LLM 客户端 + Agent 核心",
        "功能": [
            "LLMClient - 支持 Ollama/Anthropic/DeepSeek",
            "RestaurantAgent - 主 Agent 逻辑",
            "工具调用管理",
            "对话历史记录"
        ],
        "关键方法": "process_user_input()",
        "修改场景": "改变 Agent 行为、修改提示词、调整工具选择逻辑"
    },
    
    "langgraph_agent.py": {
        "描述": "高级 LangGraph 图式实现",
        "特点": "状态管理、节点转移、完整的 Agent 生命周期",
        "参考用途": "学习 LangGraph 框架、实装高级 Agent",
        "修改场景": "实装复杂的 Agent 工作流"
    },
    
    "config.py": {
        "描述": "完整的配置管理系统",
        "配置类": [
            "LLMConfig - LLM 参数",
            "APIConfig - API 服务器设置",
            "AgentConfig - Agent 行为",
            "DatabaseConfig - 数据存储",
            "PromptConfig - AI 提示词"
        ],
        "用处": "统一管理所有配置参数",
        "修改场景": "调整超时、改变模型、修改业务规则"
    },
    
    "run_poc.py": {
        "描述": "完整 POC 入口程序",
        "功能": [
            "检查依赖",
            "自动启动 API 服务器",
            "LLM 选择菜单",
            "交互对话循环",
            "自动清理"
        ],
        "运行": "python run_poc.py",
        "这是": "🚀 主程序，大多数用户会运行这个"
    },
    
    "test_poc.py": {
        "描述": "自动化测试脚本",
        "测试内容": [
            "API 功能测试",
            "Agent 功能测试",
            "Ollama/Anthropic 支持"
        ],
        "运行": "python test_poc.py",
        "用处": "验证环境和功能是否正常"
    },
    
    "README.md": {
        "描述": "完整项目文档",
        "内容": [
            "项目概述",
            "架构说明",
            "快速开始",
            "工具参考",
            "扩展指南",
            "故障排除"
        ],
        "字数": "500+ 行",
        "推荐": "第一个阅读的文档"
    },
    
    "QUICKSTART.md": {
        "描述": "30 秒快速启动指南",
        "包含": [
            "Ollama 快速启动",
            "Anthropic 快速启动",
            "DeepSeek 快速启动",
            "常见错误解决"
        ],
        "时间": "5-10 分钟可上手",
        "推荐": "最少阅读，快速体验"
    },
    
    "SUMMARY.md": {
        "描述": "项目架构和总结",
        "内容": [
            "系统架构图",
            "文件详解",
            "数据流说明",
            "扩展指南",
            "学习路径"
        ],
        "用处": "理解项目设计和架构"
    },
    
    "API.md": {
        "描述": "详细 API 参考文档",
        "包含": [
            "每个工具的详细说明",
            "请求/响应示例",
            "参数说明",
            "错误处理",
            "工作流示例"
        ],
        "用处": "调用 API 时查看参考"
    },
    
    "requirements.txt": {
        "描述": "Python 依赖列表",
        "包括": [
            "fastapi",
            "uvicorn",
            "pydantic",
            "requests",
            "anthropic (可选)",
            "python-dotenv"
        ],
        "安装": "pip install -r requirements.txt"
    }
}

COMMON_TASKS = {
    "快速启动": {
        "步骤": [
            "pip install -r requirements.txt",
            "python run_poc.py",
            "选择 LLM 方案 (1/2/3)",
            "输入中文请求"
        ],
        "时间": "2 分钟"
    },
    
    "测试功能": {
        "步骤": [
            "python verify_project.py (检查环境)",
            "python test_poc.py (运行测试)",
            "查看测试结果"
        ],
        "时间": "1 分钟"
    },
    
    "添加新工具": {
        "步骤": [
            "在 api_server.py 中添加端点",
            "在 AVAILABLE_TOOLS 中注册工具",
            "运行 test_poc.py 验证",
            "Agent 会自动支持新工具"
        ],
        "时间": "15 分钟"
    },
    
    "修改 LLM 提示词": {
        "步骤": [
            "编辑 config.py 中的 PromptConfig",
            "或编辑 agent.py 中的 _format_tools_context()",
            "重新运行 run_poc.py",
            "测试新的提示词效果"
        ],
        "时间": "5 分钟"
    },
    
    "Docker 部署": {
        "步骤": [
            "docker build -t restaurant-agent .",
            "docker run -p 8001:8001 restaurant-agent",
            "或: docker-compose up -d",
            "访问: http://localhost:8001/health"
        ],
        "时间": "3 分钟"
    },
    
    "切换到数据库": {
        "步骤": [
            "修改 config.py DatabaseConfig",
            "修改 api_server.py 的数据存储逻辑",
            "使用 SQLAlchemy 或其他 ORM",
            "运行测试验证"
        ],
        "时间": "30 分钟"
    }
}

TROUBLESHOOTING = {
    "问题": "Ollama 连接失败",
    "原因": "Ollama 未运行或模型未下载",
    "解决": [
        "运行: ollama serve",
        "下载模型: ollama pull llama2-chinese",
        "检查: http://localhost:11434 是否可访问"
    ]
}, {
    "问题": "API 启动失败",
    "原因": "8001 端口被占用",
    "解决": [
        "Windows: netstat -ano | findstr :8001",
        "Mac/Linux: lsof -i :8001",
        "杀死占用进程或用其他端口"
    ]
}, {
    "问题": "LLM API Key 无效",
    "原因": "环境变量未设置或 Key 过期",
    "解决": [
        "检查环境变量是否设置",
        "验证 API Key 是否正确",
        "确认 API Key 未过期"
    ]
}, {
    "问题": "ImportError: No module named xxx",
    "原因": "依赖未安装",
    "解决": [
        "运行: pip install -r requirements.txt",
        "或: pip install <package-name>"
    ]
}

def print_welcome():
    """打印欢迎信息"""
    print(PROJECT_STRUCTURE)
    print("\n" + "="*60)
    print("🎯 快速导航 - 根据你的需求选择:")
    print("="*60)
    
    for i, (title, steps) in enumerate(QUICK_NAVIGATION.items(), 1):
        print(f"\n{i}. {title}")
        for step in steps:
            print(f"   {step}")
    
    print("\n" + "="*60)
    print("📖 查看详细文件说明: python PROJECT_FILES.py --help")
    print("="*60)

if __name__ == "__main__":
    import sys
    
    if "--files" in sys.argv:
        # 打印所有文件说明
        for file, info in FILE_DESCRIPTIONS.items():
            print(f"\n📄 {file}")
            print(f"   {info['描述']}")
            if isinstance(info, dict):
                for key, value in info.items():
                    if key != "描述":
                        print(f"   • {key}: {value}")
    
    elif "--tasks" in sys.argv:
        # 打印常见任务
        for task, info in COMMON_TASKS.items():
            print(f"\n✓ {task} ({info['时间']})")
            for step in info['步骤']:
                print(f"  {step}")
    
    else:
        # 打印欢迎
        print_welcome()
