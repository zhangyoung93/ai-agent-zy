"""Agent 基类。

所有 Agent（单 Agent、多 Agent 协作）都继承它，统一接口。
后续在 run() 中实现：规划 -> 工具调用循环 -> 输出。
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..llm.client import LLMClient
from ..tools.registry import ToolRegistry


class Agent(ABC):
    """Agent 抽象基类。"""

    def __init__(
        self,
        llm: LLMClient,
        *,
        tools: ToolRegistry | None = None,
        name: str | None = None,
    ) -> None:
        self.llm = llm
        self.tools = tools or ToolRegistry()
        self.name = name or self.__class__.__name__

    @abstractmethod
    def run(self, task: str) -> str:
        """执行任务，返回文本结果。"""
