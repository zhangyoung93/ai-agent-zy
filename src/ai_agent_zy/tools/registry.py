"""工具注册表：Agent 调用外部能力的统一管理。

这是"工具调用（Function Calling）"的基础设施：
- Tool：一个可被 LLM 调用的函数 + 元数据（名称、描述、参数 JSON Schema）
- ToolRegistry：注册、查询、列出工具

下一步学习 Function Calling 时，会把这里的工具转换成 OpenAI 的 tools 参数。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Tool:
    """一个可被 LLM 调用的工具。"""

    name: str
    description: str
    function: Callable[..., Any]
    parameters: dict[str, Any] = field(default_factory=dict)  # 参数 JSON Schema


class ToolRegistry:
    """工具集合，支持注册、查询、列出。"""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"工具 {tool.name!r} 已注册")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"未注册的工具：{name}")
        return self._tools[name]

    def list(self) -> list[Tool]:
        return list(self._tools.values())

    def __contains__(self, name: str) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)


def tool(
    name: str | None = None,
    *,
    description: str = "",
    parameters: dict[str, Any] | None = None,
):
    """装饰器：把一个普通函数包装成 Tool（稍后用于 Function Calling）。"""

    def decorator(func: Callable[..., Any]) -> Tool:
        return Tool(
            name=name or func.__name__,
            description=description or (func.__doc__ or "").strip(),
            function=func,
            parameters=parameters or {},
        )

    return decorator
