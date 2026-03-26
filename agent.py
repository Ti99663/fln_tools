import anthropic
import requests
import json
from typing import Any, Dict, List, Optional
from datetime import datetime

# ============ LLM 配置 ============
# 使用 Anthropic 的免费试用或使用其他免费 LLM 接口
# 如果没有 API Key，可以改用本地 Ollama

class LLMClient:
    """LLM 客户端 - 支持多个免费接口"""
    
    def __init__(self, api_type: str = "ollama", api_key: Optional[str] = None, 
                 api_endpoint: Optional[str] = None, model: Optional[str] = None):
        """
        api_type: "ollama" (本地), "anthropic", "deepseek", "ssrai"
        api_key: API 密钥
        api_endpoint: SSRAI 端点 URL
        model: 模型名称（SSRAI 时使用，如 "gpt-4o"）
        """
        self.api_type = api_type
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.model = model or "gpt-4o"
        
        if api_type == "anthropic" and not api_key:
            raise ValueError("Anthropic 需要 API Key")
        
        if api_type == "deepseek" and not api_key:
            raise ValueError("DeepSeek 需要 API Key")
        
        if api_type == "ssrai":
            if not api_key:
                raise ValueError("SSRAI 需要 API Key")
            if not api_endpoint:
                raise ValueError("SSRAI 需要 API 端点 URL")
    
    def call(self, prompt: str, tools_context: str = "") -> str:
        """调用 LLM"""
        
        if self.api_type == "ollama":
            return self._call_ollama(prompt, tools_context)
        elif self.api_type == "anthropic":
            return self._call_anthropic(prompt, tools_context)
        elif self.api_type == "deepseek":
            return self._call_deepseek(prompt, tools_context)
        elif self.api_type == "ssrai":
            return self._call_ssrai(prompt, tools_context)
        else:
            raise ValueError(f"不支持的 LLM 类型: {self.api_type}")
    
    def _call_ollama(self, prompt: str, tools_context: str) -> str:
        """使用本地 Ollama（需要先启动 ollama serve）"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2-chinese",  # 或 "mistral", "neural-chat"
                    "prompt": f"{tools_context}\n\n{prompt}",
                    "stream": False,
                    "temperature": 0.7,
                }
            )
            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception(f"Ollama API 错误: {response.status_code}")
        except requests.exceptions.ConnectionError:
            raise Exception(
                "无法连接到 Ollama。请先运行: ollama serve\n"
                "并下载模型: ollama pull llama2-chinese"
            )
    
    def _call_anthropic(self, prompt: str, tools_context: str) -> str:
        """使用 Claude API (免费试用)"""
        client = anthropic.Anthropic(api_key=self.api_key)
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"{tools_context}\n\n{prompt}"
                }
            ]
        )
        return message.content[0].text
    
    def _call_deepseek(self, prompt: str, tools_context: str) -> str:
        """使用 DeepSeek API"""
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": tools_context
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1024
            }
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"DeepSeek API 错误: {response.status_code}")
    
    def _call_ssrai(self, prompt: str, tools_context: str) -> str:
        """使用 SSRAI API（支持 GPT-4o 等）"""
        try:
            response = requests.post(
                f"{self.api_endpoint}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": tools_context
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                error_msg = response.text
                raise Exception(f"SSRAI API 错误 ({response.status_code}): {error_msg}")
        except requests.exceptions.ConnectionError:
            raise Exception(
                f"无法连接到 SSRAI API: {self.api_endpoint}\n"
                "请检查 API 端点 URL 是否正确"
            )

# ============ Agent 核心 ============
class RestaurantAgent:
    """餐厅预订 Agent"""
    
    def __init__(self, llm_client: LLMClient, api_base_url: str = "http://127.0.0.1:8001"):
        self.llm = llm_client
        self.api_base_url = api_base_url
        self.tools = []
        self.conversation_history = []
        self._load_tools()
    
    def _load_tools(self):
        """从 API 服务器加载工具定义"""
        try:
            response = requests.get(f"{self.api_base_url}/tools")
            if response.status_code == 200:
                self.tools = response.json()["tools"]
                print(f"✓ 已加载 {len(self.tools)} 个工具")
            else:
                raise Exception("无法加载工具")
        except requests.exceptions.ConnectionError:
            raise Exception(
                f"无法连接到 API 服务器: {self.api_base_url}\n"
                "请先运行: python api_server.py"
            )
    
    def _format_tools_context(self) -> str:
        """格式化工具上下文"""
        tools_text = "你是一个餐厅预订助手。你可以使用以下工具:\n\n"
        for tool in self.tools:
            tools_text += f"- {tool['name']}: {tool['description']}\n"
            tools_text += f"  参数: {json.dumps(tool['parameters'], ensure_ascii=False)}\n"
        tools_text += "\n当用户要求某个操作时,请分析用户的需求,并返回需要调用的工具名称和参数。"
        tools_text += "\n返回格式: {\"tool\": \"tool_name\", \"params\": {...}}"
        return tools_text
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """解析 LLM 响应"""
        # 尝试提取 JSON
        try:
            # 查找 JSON 对象
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # 如果 JSON 解析失败，尝试启发式提取
        if "search_restaurants" in response.lower():
            return {"tool": "search_restaurants", "params": {}}
        elif "availability" in response.lower() or "可用" in response:
            return {"tool": "check_availability", "params": {}}
        elif "booking" in response.lower() or "预订" in response:
            return {"tool": "make_booking", "params": {}}
        elif "history" in response.lower() or "历史" in response:
            return {"tool": "get_booking_history", "params": {}}
        
        return None
    
    def _call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用工具 API"""
        try:
            response = requests.post(
                f"{self.api_base_url}/tools/{tool_name}",
                json=params
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "status": "error",
                    "message": f"工具执行失败: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def process_user_input(self, user_input: str) -> str:
        """处理用户输入"""
        print(f"\n👤 用户: {user_input}")
        
        # 记录对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # 步骤 1: 让 LLM 理解用户意图并选择工具
        tools_context = self._format_tools_context()
        llm_response = self.llm.call(user_input, tools_context)
        print(f"\n🤖 LLM 分析: {llm_response[:200]}...")
        
        # 步骤 2: 解析 LLM 响应获取工具和参数
        tool_action = self._parse_llm_response(llm_response)
        
        if not tool_action or "tool" not in tool_action:
            response_text = f"我理解了: {user_input}\n但我需要直接的指示来调用工具。"
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })
            return response_text
        
        tool_name = tool_action["tool"]
        tool_params = tool_action.get("params", {})
        
        print(f"\n🔧 选定工具: {tool_name}")
        print(f"📋 工具参数: {tool_params}")
        
        # 步骤 3: 调用工具
        tool_result = self._call_tool(tool_name, tool_params)
        print(f"\n✅ 工具结果: {json.dumps(tool_result, ensure_ascii=False, indent=2)}")
        
        # 步骤 4: 让 LLM 生成最终响应
        final_prompt = (
            f"用户请求: {user_input}\n"
            f"调用的工具: {tool_name}\n"
            f"工具返回结果: {json.dumps(tool_result, ensure_ascii=False)}\n\n"
            f"请用中文总结结果,并给出有用的建议。"
        )
        final_response = self.llm.call(final_prompt)
        
        self.conversation_history.append({
            "role": "assistant",
            "content": final_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return final_response
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.conversation_history

# ============ 主程序 ============
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # 选择 LLM 方案
    print("━" * 60)
    print("🍽️  餐厅预订 Agent - LangGraph POC")
    print("━" * 60)
    print("\n选择 LLM 方案:")
    print("1. Ollama (本地, 需要先运行 ollama serve)")
    print("2. Anthropic Claude (需要 API Key)")
    print("3. DeepSeek (需要 API Key)")
    
    choice = input("\n请选择 [1/2/3]: ").strip()
    
    if choice == "1":
        llm_type = "ollama"
        api_key = None
    elif choice == "2":
        llm_type = "anthropic"
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            api_key = input("请输入 Anthropic API Key: ").strip()
    elif choice == "3":
        llm_type = "deepseek"
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            api_key = input("请输入 DeepSeek API Key: ").strip()
    else:
        print("无效选择,使用默认 Ollama")
        llm_type = "ollama"
        api_key = None
    
    try:
        # 初始化 LLM 和 Agent
        llm = LLMClient(api_type=llm_type, api_key=api_key)
        agent = RestaurantAgent(llm)
        
        print("\n✓ Agent 初始化成功！")
        print("━" * 60)
        print("📝 输入 'quit' 或 'exit' 退出\n")
        
        # 交互循环
        while True:
            user_input = input(">>> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 再见！")
                break
            
            try:
                response = agent.process_user_input(user_input)
                print(f"\n🤖 助手: {response}\n")
            except Exception as e:
                print(f"\n❌ 错误: {str(e)}\n")
                print("💡 提示: 确保 API 服务器正在运行 (python api_server.py)\n")
    
    except Exception as e:
        print(f"\n❌ 初始化失败: {str(e)}\n")
        print("💡 快速修复:")
        print("  1. 如果使用 Ollama,请先运行: ollama serve")
        print("  2. 如果使用 Anthropic,请设置 ANTHROPIC_API_KEY 环境变量")
        print("  3. 如果使用 DeepSeek,请设置 DEEPSEEK_API_KEY 环境变量")
