# AI Agent 项目常用任务（Linux/macOS/WSL 或 Git Bash 下使用）
# Windows 原生 PowerShell 用户可直接看 README 里的等价命令

PY := .venv/bin/python
ifeq ($(OS),Windows_NT)
	PY := .venv/Scripts/python
endif

.PHONY: setup install run test lint format typecheck clean

## 创建虚拟环境并安装全部依赖（含 dev）
setup:
	py -3 -m venv .venv
	$(PY) -m pip install -e ".[dev]"

## 安装依赖
install:
	$(PY) -m pip install -e ".[dev]"

## 运行 CLI 对话
run:
	$(PY) -m ai_agent_zy hello

## 运行测试
test:
	$(PY) -m pytest

## 代码检查
lint:
	$(PY) -m ruff check .

## 代码格式化
format:
	$(PY) -m ruff format .

## 类型检查
typecheck:
	$(PY) -m mypy src

## 清理构建产物
clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache
