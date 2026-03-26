"""
基于 LangGraph 的餐厅预订 Agent
支持多轮对话、状态管理和复杂工作流
"""

import json
import requests
from typing import Any, Dict, List, Optional, Annotated
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# ============ 数据结构 ============
class AgentNodeType(str, Enum):
    """Agent 节点类型"""
    START = "start"
    LLM_ANALYZE = "llm_analyze"
    TOOL_EXECUTE = "tool_execute"
    LLM_SUMMARIZE = "llm_summarize"
    END = "end"
    ERROR = "error"

@dataclass
class AgentState:
    """Agent 状态"""
    user_input: str
    conversation_history: List[Dict[str, str]]
    current_step: AgentNodeType
    selected_tool: Optional[str] = None
    tool_params: Optional[Dict[str, Any]] = None
    tool_result: Optional[Dict[str, Any]] = None
    llm_analysis: Optional[str] = None
    final_response: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class LangGraphAgent:
    """LangGraph 风格的 Agent"""
    
    def __init__(self, llm_client, api_base_url: str = "http://127.0.0.1:8001"):
        self.llm = llm_client
        self.api_base_url = api_base_url
        self.tools = []
        self.nodes = {}
        self.edges = {}
        self._build_graph()
    
    def _build_graph(self):
        """构建 LangGraph 图"""
        # 加载工具
        try:
            response = requests.get(f"{self.api_base_url}/tools")
            self.tools = response.json()["tools"]
        except:
            raise Exception("无法连接到 API 服务器")
        
        # 定义节点
        self.nodes = {
            AgentNodeType.LLM_ANALYZE: self._node_llm_analyze,
            AgentNodeType.TOOL_EXECUTE: self._node_tool_execute,
            AgentNodeType.LLM_SUMMARIZE: self._node_llm_summarize,
        }
        
        # 定义边（转移）
        self.edges = {
            AgentNodeType.LLM_ANALYZE: {
                "success": AgentNodeType.TOOL_EXECUTE,
                "error": AgentNodeType.ERROR,
            },
            AgentNodeType.TOOL_EXECUTE: {
                "success": AgentNodeType.LLM_SUMMARIZE,
                "error": AgentNodeType.ERROR,
            },
            AgentNodeType.LLM_SUMMARIZE: {
                "success": AgentNodeType.END,
            }
        }
    
    def _node_llm_analyze(self, state: AgentState) -> AgentState:
        """LLM 分析节点"""
        print(f"\n📊 [节点] LLM 分析用户意图...")
        
        tools_context = self._format_tools_for_llm()
        prompt = f"{tools_context}\n\n用户请求: {state.user_input}"
        
        # 调用 LLM
        response = self.llm.call(prompt, "")
        state.llm_analysis = response
        
        # 解析 LLM 响应
        action = self._parse_tool_action(response)
        if action:
            state.selected_tool = action["tool"]
            state.tool_params = action.get("params", {})
            return state
        else:
            state.error_message = "无法解析 LLM 响应"
            return state
    
    def _node_tool_execute(self, state: AgentState) -> AgentState:
        """工具执行节点"""
        if not state.selected_tool:
            state.error_message = "没有选定的工具"
            return state
        
        print(f"\n🔧 [节点] 执行工具: {state.selected_tool}")
        
        try:
            tool_result = requests.post(
                f"{self.api_base_url}/tools/{state.selected_tool}",
                json=state.tool_params
            )
            if tool_result.status_code == 200:
                state.tool_result = tool_result.json()
            else:
                state.error_message = f"工具调用失败: {tool_result.status_code}"
        except Exception as e:
            state.error_message = str(e)
        
        return state
    
    def _node_llm_summarize(self, state: AgentState) -> AgentState:
        """LLM 总结节点"""
        print(f"\n📝 [节点] LLM 生成最终响应...")
        
        prompt = (
            f"用户请求: {state.user_input}\n"
            f"工具调用: {state.selected_tool}\n"
            f"工具结果: {json.dumps(state.tool_result, ensure_ascii=False)}\n\n"
            f"请用中文总结结果并给出建议。"
        )
        
        response = self.llm.call(prompt, "")
        state.final_response = response
        
        # 记录到对话历史
        state.conversation_history.append({
            "role": "user",
            "content": state.user_input,
            "timestamp": datetime.now().isoformat()
        })
        state.conversation_history.append({
            "role": "assistant",
            "content": state.final_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return state
    
    def _format_tools_for_llm(self) -> str:
        """格式化工具信息给 LLM"""
        text = "你是一个专业的餐厅预订助手。\n\n可用工具:\n"
        for tool in self.tools:
            text += f"- {tool['name']}: {tool['description']}\n"
        text += "\n返回 JSON 格式: {\"tool\": \"tool_name\", \"params\": {...}}\n"
        return text
    
    def _parse_tool_action(self, response: str) -> Optional[Dict[str, Any]]:
        """解析工具动作"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        return None
    
    def execute(self, user_input: str, conversation_history: List[Dict[str, str]] = None) -> AgentState:
        """执行 Agent（LangGraph 流程）"""
        print("\n" + "="*60)
        print(f"🚀 开始执行 Agent流程")
        print("="*60)
        
        # 初始化状态
        state = AgentState(
            user_input=user_input,
            conversation_history=conversation_history or [],
            current_step=AgentNodeType.LLM_ANALYZE
        )
        
        # 执行图
        while state.current_step != AgentNodeType.END:
            print(f"\n→ 当前节点: {state.current_step.value}")
            
            if state.current_step == AgentNodeType.ERROR:
                print(f"❌ 错误: {state.error_message}")
                break
            
            # 执行当前节点
            if state.current_step in self.nodes:
                state = self.nodes[state.current_step](state)
            
            # 确定下一个节点
            if state.current_step in self.edges:
                next_key = "error" if state.error_message else "success"
                state.current_step = self.edges[state.current_step].get(next_key, AgentNodeType.END)
            else:
                state.current_step = AgentNodeType.END
        
        print("\n" + "="*60)
        print("✅ Agent 执行完成")
        print("="*60)
        
        return state

# ============ 使用示例 ============
if __name__ == "__main__":
    from agent import LLMClient
    
    # 初始化
    llm = LLMClient(api_type="ollama")
    agent = LangGraphAgent(llm)
    
    # 执行示例
    test_inputs = [
        "我想在中关村找一家四川菜餐厅",
        "请帮我查一下金牌川菜馆明天7点的可用性",
        "我想预订金牌川菜馆，2024年12月25日19点，4人，我叫张三，电话是13800138000"
    ]
    
    history = []
    for user_input in test_inputs:
        state = agent.execute(user_input, history)
        history = state.conversation_history
        print(f"\n💬 最终响应: {state.final_response}")
        input("\n按 Enter 继续下一个请求...")
