"""测试工具注册表。纯逻辑，离线可跑。"""

import pytest

from ai_agent_zy.tools import Tool, ToolRegistry, tool


def test_register_and_get() -> None:
    reg = ToolRegistry()
    t = Tool(name="add", description="加法", function=lambda a, b: a + b)
    reg.register(t)

    assert "add" in reg
    assert len(reg) == 1
    assert reg.get("add") is t
    assert reg.list() == [t]


def test_duplicate_register_raises() -> None:
    reg = ToolRegistry()
    reg.register(Tool(name="x", description="", function=lambda: None))
    with pytest.raises(ValueError):
        reg.register(Tool(name="x", description="", function=lambda: None))


def test_get_missing_raises() -> None:
    reg = ToolRegistry()
    with pytest.raises(KeyError):
        reg.get("nope")


def test_tool_decorator() -> None:
    @tool(description="把两个数相加")
    def add(a: int, b: int) -> int:
        return a + b

    assert isinstance(add, Tool)
    assert add.name == "add"
    assert add.function(1, 2) == 3
