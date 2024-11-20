from dataclasses import dataclass, field
from enum import Enum
import importlib
from typing import Dict, Generic, List, Any, Optional, TypeVar

from pydantic import BaseModel

from app.logger import logger
from app.core.workflow.node.base import BaseNode
from app.core.workflow.state import GraphState


class PluginMode(Enum):
    API = "api"
    CODE = "code"


class APIFieldMapping(BaseModel):
    name: str
    description: str
    type: str
    input_method: str
    default_value: Any
    must_input: bool = True
    enabled: bool = True


class APIConfig(BaseModel):
    name: str
    description: str
    endpoint: str
    method: str = "POST"
    headers: Dict[str, str] = {}
    timeout: int = 30
    input_mapping: Dict[str, APIFieldMapping] = {}
    output_mapping: Dict[str, APIFieldMapping] = {}

T = TypeVar('T')

@dataclass
class Args(Generic[T]):
    input: T
    logger: Any

class CodeConfig(BaseModel):
    name: str
    description: str
    code: str
    input_mapping: Optional[Dict] = {}
    output_mapping: Optional[Dict] = {}


class PluginConfig(BaseModel):
    mode: PluginMode
    api_config: Optional[APIConfig] = None
    code_config: Optional[CodeConfig] = None
    enabled: bool = True


class PluginNode(BaseNode):
    # tool: List[Any] = field(default_factory=list)
    config:PluginConfig = None

    def __init__(self, node_data: dict):
        super().__init__(node_data)
        # self.tool = node_data.get("tool", None)
        config = node_data.get("config", None)
        # print("config:", config)
        if config:
            self.config = PluginConfig(**config)
        
        

    def execute(self, state: GraphState):
        super().execute(state)

        # if self.tool is None:
        #     state["messages"].append("~~~skip plugin node here because no tool is provided~~~")
        #     return state

        # 准备输入参数
        inputs = self._prepare_inputs(state)

        # 根据模式执行相应的逻辑
        if self.config.mode == PluginMode.API:
            outputs = self._execute_api(inputs)
        else:
            outputs = self._execute_code(inputs)

        # 映射输出到状态
        self._map_outputs_to_state(state, outputs)
    
        state["messages"].append("~~~finish plugin node here ")
        return state

    def _prepare_inputs(self, state: GraphState) -> Dict[str, Any]:
        """根据输入映射从状态中提取参数"""
        return self.input_vars
        # return {
        #     output_key: state.get(input_path)
        #     for output_key, input_path in self.config.input_mapping.items()
        # }

    def _execute_api(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """执行 API 调用"""
        if not self.config.api_config:
            raise ValueError("API config is required for API mode")
        # 实现 API 调用逻辑
        pass

    def _execute_code(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """执行自定义代码"""
        if not self.config.code_config or not self.config.code_config.code:
            raise ValueError("Code is required for Code mode")
        # 实现代码执行逻辑
        try:
            # 创建模块
            spec = importlib.util.spec_from_loader('plugin_execute_code', loader=None)
            module = importlib.util.module_from_spec(spec)
            
            # 注入必要的依赖，直接在模块命名空间中定义所需的类和变量
            module.__dict__.update({
                'Args': Args,
                'Input': Dict[str, Any],
                'Output': Dict[str, Any],
                'logger': logger
            })
            # 执行代码
            exec(self.config.code_config.code, module.__dict__)
            
            if not hasattr(module, 'handler'):
                raise ValueError("No handler function found in code")
            
            # 准备参数
            args = Args(
                input=inputs,
                logger=logger
            )
            
            # 调用 handler
            result = module.handler(args)
            return result
            
        except Exception as e:
            logger.error(f"Code execution failed: {str(e)}")
            raise
        


    def _map_outputs_to_state(self, state: GraphState, outputs: Dict[str, Any]):
        """将输出映射回状态"""
        return self.output_vars
        # for output_key, state_path in self.config.output_mapping.items():
        #     if output_key in outputs:
        #         state[state_path] = outputs[output_key]
