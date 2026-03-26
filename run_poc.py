"""
餐厅预订 Agent - 完整 POC 演示
包含 API 服务器启动、Agent 初始化和交互循环
"""

import subprocess
import time
import sys
import os
import signal
import requests
from pathlib import Path

class POCRunner:
    """POC 运行管理器"""
    
    def __init__(self):
        self.api_process = None
        self.api_url = "http://127.0.0.1:8001"
        
    def check_api_health(self) -> bool:
        """检查 API 服务器健康状态"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=2)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.Timeout:
            return False
        except Exception as e:
            return False
    
    def start_api_server(self):
        """启动 API 服务器"""
        print("\n📡 启动 API 服务器...")
        try:
            self.api_process = subprocess.Popen(
                [sys.executable, "api_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
            )
        except Exception as e:
            print(f"❌ 启动失败: {str(e)}")
            return False
        
        # 等待服务器启动
        for i in range(15):
            time.sleep(1)
            print(f"  等待中... ({i+1}/15)", end='\r', flush=True)
            if self.check_api_health():
                print("✓ API 服务器启动成功 (127.0.0.1:8001)          ")
                return True
        
        print("\n❌ API 服务器启动失败")
        # 输出错误信息以便诊断
        try:
            stdout, stderr = self.api_process.communicate(timeout=1)
            if stderr:
                print("\n🔴 错误输出:")
                print(stderr)
            if stdout:
                print("\n📝 标准输出:")
                print(stdout[:500])  # 显示前 500 个字符
        except subprocess.TimeoutExpired:
            print("\n⏱️  进程仍在运行，但未通过健康检查")
            # 尝试读取部分输出
            try:
                self.api_process.kill()
            except:
                pass
        
        return False
    
    def cleanup(self):
        """清理资源"""
        if self.api_process:
            print("\n🛑 关闭 API 服务器...")
            self.api_process.terminate()
            try:
                self.api_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.api_process.kill()
            print("✓ API 服务器已关闭")

def print_banner():
    """打印欢迎横幅"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "🍽️  餐厅预订 Agent - POC 演示" + " "*12 + "║")
    print("║" + " "*18 + "基于 LangGraph 框架" + " "*19 + "║")
    print("╚" + "="*58 + "╝")

def print_instructions():
    """打印使用说明"""
    print("""
┌─ 📖 使用说明 ──────────────────────────────────────────┐
│                                                           │
│ 1️⃣  API 服务将自动启动 (127.0.0.1:8001)                 │
│                                                           │
│ 2️⃣  选择 LLM 方案:                                       │
│     • Ollama (本地) - 推荐用于演示                       │
│     • Anthropic Claude - 需要 API Key                    │
│     • DeepSeek - 需要 API Key                            │
│                                                           │
│ 3️⃣  输入用户请求，Agent 会:                             │
│     • 分析用户意图                                       │
│     • 选择合适的工具                                     │
│     • 调用 API 执行操作                                  │
│     • 生成自然语言响应                                   │
│                                                           │
│ 4️⃣  输入 quit/exit 结束程序                             │
│                                                           │
└─────────────────────────────────────────────────────────┘
    """)

def print_quick_setup():
    """打印快速设置指南"""
    print("""
┌─ 🚀 快速设置指南 ──────────────────────────────────────┐
│                                                           │
│ 选项 A: 使用 Ollama (推荐)                              │
│ ─────────────────────────────────────────────────────    │
│ 1. 下载 Ollama: https://ollama.ai/download               │
│ 2. 启动 Ollama: ollama serve                             │
│ 3. 下载模型:                                             │
│    • ollama pull llama2-chinese                          │
│    • 或: ollama pull neurna-chat                         │
│                                                           │
│ 选项 B: 使用 Anthropic Claude                            │
│ ─────────────────────────────────────────────────────    │
│ 1. 获取免费试用 API Key: https://console.anthropic.com  │
│ 2. 设置环境变量:                                         │
│    Windows: set ANTHROPIC_API_KEY=your-key              │
│    Linux/Mac: export ANTHROPIC_API_KEY=your-key         │
│                                                           │
│ 选项 C: 使用 DeepSeek                                   │
│ ─────────────────────────────────────────────────────    │
│ 1. 获取 API Key: https://platform.deepseek.com          │
│ 2. 设置环境变量:                                         │
│    Windows: set DEEPSEEK_API_KEY=your-key               │
│    Linux/Mac: export DEEPSEEK_API_KEY=your-key          │
│                                                           │
└─────────────────────────────────────────────────────────┘
    """)

def main():
    """主函数"""
    print_banner()
    print_quick_setup()
    input("按 Enter 键继续...")
    
    # 检查依赖
    print("\n📦 检查依赖...")
    try:
        import anthropic
        print("  ✓ anthropic 已安装")
    except:
        print("  ⚠️  anthropic 未安装 (如果不使用 Anthropic 可忽略)")
    
    try:
        import requests
        print("  ✓ requests 已安装")
    except:
        print("  ❌ requests 未安装")
        return
    
    try:
        import fastapi
        print("  ✓ fastapi 已安装")
    except:
        print("  ❌ fastapi 未安装")
        return
    
    # 启动 API 服务
    runner = POCRunner()
    try:
        if not runner.start_api_server():
            print("\n⚠️  API 服务器启动失败")
            print("请检查是否有其他进程占用 8001 端口:")
            print("  Windows: netstat -ano | findstr :8001")
            print("  Linux/Mac: lsof -i :8001")
            return
        
        print_instructions()
        
        # 导入 Agent
        from agent import LLMClient, RestaurantAgent
        
        # 选择 LLM
        print("━"*60)
        print("🤖 LLM 配置")
        print("━"*60)
        print("\n选择 LLM 方案:")
        print("  1. Ollama (本地)")
        print("  2. Anthropic Claude")
        print("  3. DeepSeek")
        print("  4. SSRAI (公司内部，支持 GPT-4o 等)")
        
        choice = input("\n请输入选择 [1/2/3/4] (默认 1): ").strip() or "1"
        
        llm_params = {"api_type": None, "api_key": None, "api_endpoint": None, "model": None}
        
        if choice == "1":
            llm_params["api_type"] = "ollama"
        elif choice == "2":
            llm_params["api_type"] = "anthropic"
            llm_params["api_key"] = os.getenv("ANTHROPIC_API_KEY")
            if not llm_params["api_key"]:
                llm_params["api_key"] = input("请输入 Anthropic API Key: ").strip()
        elif choice == "3":
            llm_params["api_type"] = "deepseek"
            llm_params["api_key"] = os.getenv("DEEPSEEK_API_KEY")
            if not llm_params["api_key"]:
                llm_params["api_key"] = input("请输入 DeepSeek API Key: ").strip()
        elif choice == "4":
            llm_params["api_type"] = "ssrai"
            
            # 获取 SSRAI 配置
            print("\n📋 SSRAI 配置:")
            llm_params["api_endpoint"] = os.getenv("SSRAI_API_ENDPOINT")
            if not llm_params["api_endpoint"]:
                llm_params["api_endpoint"] = input("  请输入 SSRAI API 端点 (如: https://api.example.com/v1): ").strip()
            
            llm_params["api_key"] = os.getenv("SSRAI_API_KEY")
            if not llm_params["api_key"]:
                llm_params["api_key"] = input("  请输入 SSRAI API Key: ").strip()
            
            model_input = input("  请输入模型名称 (默认 gpt-4o): ").strip()
            llm_params["model"] = model_input or "gpt-4o"
            
            print(f"\n✅ SSRAI 配置已保存:")
            print(f"  端点: {llm_params['api_endpoint']}")
            print(f"  模型: {llm_params['model']}")
        else:
            print("无效选择，使用 Ollama")
            llm_params["api_type"] = "ollama"
        
        # 初始化 Agent
        print(f"\n⚙️  初始化 {llm_params['api_type']} LLM...")
        try:
            # 移除 None 值的参数
            init_params = {k: v for k, v in llm_params.items() if v is not None}
            llm = LLMClient(**init_params)
            agent = RestaurantAgent(llm)
            print("✓ Agent 初始化成功！")
        except Exception as e:
            print(f"❌ 初始化失败: {str(e)}")
            if "Ollama" in str(e):
                print("\n💡 如何启动 Ollama:")
                print("  1. 下载: https://ollama.ai/download")
                print("  2. 运行: ollama serve")
                print("  3. 下载模型: ollama pull llama2-chinese")
            elif "SSRAI" in str(e):
                print("\n💡 SSRAI 配置检查:")
                print("  1. 确认 API 端点 URL 正确")
                print("  2. 确认 API Key 有效")
                print("  3. 测试 API 连接: curl -H 'Authorization: Bearer {key}' {endpoint}/chat/completions")
            return
        
        # 交互循环
        print("\n" + "━"*60)
        print("💬 输入 'quit' 或 'exit' 退出\n")
        
        # 测试示例
        print("📝 建议的测试输入:")
        print("  • '我想在中关村找一家四川菜餐厅'")
        print("  • '查一下金牌川菜馆今天的可用时间'")
        print("  • '帮我预订金牌川菜馆，明天19点，4人，我叫张三，电话13800138000'")
        print()
        
        conversation_count = 0
        while True:
            try:
                user_input = input("\n>>> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("\n👋 感谢使用，再见！\n")
                    break
                
                conversation_count += 1
                print(f"\n[对话 #{conversation_count}]")
                
                response = agent.process_user_input(user_input)
                print(f"\n🤖 助手:\n{response}")
                
            except KeyboardInterrupt:
                print("\n\n⌛ 程序被中断")
                break
            except Exception as e:
                print(f"\n❌ 错误: {str(e)}")
                if "连接" in str(e) or "Connection" in str(e):
                    print("💡 提示: API 服务器可能已关闭，正在尝试重启...")
                    if not runner.start_api_server():
                        print("无法重启 API 服务器，程序退出")
                        break
    
    finally:
        runner.cleanup()

if __name__ == "__main__":
    main()
