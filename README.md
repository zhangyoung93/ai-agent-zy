# ai-agent-zy

企业级 AI Agent 项目骨架，以 **DeepSeek**（OpenAI 兼容接口）为底座。
目标是搭建一套可扩展的工程基础，供后续学习「工具调用 / RAG / 多 Agent 编排」时复用。

## 技术栈

| 类别 | 选型 |
|------|------|
| 语言 | Python 3.11+（推荐 3.12，LLM 生态兼容性最好） |
| LLM 调用 | `openai` SDK（DeepSeek 兼容 OpenAI 接口） |
| 配置管理 | `pydantic-settings`（类型安全 + 启动校验） |
| 测试 | `pytest` |
| 代码质量 | `ruff`（lint + format）、`mypy`（类型检查） |
| 打包 | `hatchling` + `pyproject.toml` |

## 目录结构

```
ai-agent-zy/
├── src/ai_agent_zy/          # 源码（src 布局）
│   ├── config.py             #   配置（pydantic-settings）
│   ├── logging.py            #   日志
│   ├── cli.py                #   CLI 入口（ai-agent 命令）
│   ├── llm/client.py         #   DeepSeek 客户端封装
│   ├── tools/registry.py     #   工具注册表（Function Calling 基础）
│   └── agents/base.py        #   Agent 抽象基类
├── examples/hello_llm.py     # 使用 src 包的示例
├── tests/                    # 单元测试（离线可跑）
├── docs/architecture.md      # 架构说明
├── .github/workflows/ci.yml  # CI 流水线
├── Dockerfile                # 容器化
├── pyproject.toml            # 项目清单 + 工具配置
├── .env.example              # 配置模板
```

## 快速开始（Windows）

### 前置：准备 API Key

项目根目录 `.env` 需要 `DEEPSEEK_API_KEY`。若还没有，参考 [`.env.example`](.env.example) 配置。
（获取：https://platform.deepseek.com → API Keys）

### 方式一：uv（推荐）

`uv` 是当前 Python 最快的包管理器，会根据 `.python-version` 自动安装对应 Python 版本，避免环境混乱。

```powershell
# 1. 安装 uv（二选一）
irm https://astral.sh/uv/install.ps1 | iex
# 或者：pip install uv

# 2. 同步依赖（自动创建 .venv、装 Python 3.12、装依赖）
cd E:\GitHub_Repo\ai-agent-zy
uv sync --extra dev

# 3. 运行
uv run ai-agent hello
# 或：uv run python -m ai_agent_zy hello "你的问题"
```

### 方式二：pip + venv（无需额外工具）

```powershell
cd E:\GitHub_Repo\ai-agent-zy

# 1. 创建虚拟环境（用 py，不要用 python —— 你机器上 python 是商店假别名）
py -3 -m venv .venv

# 2. 安装（-e 可编辑安装，dev 含测试/检查工具）
.venv\Scripts\python -m pip install -e ".[dev]"

# 3. 运行
.venv\Scripts\python -m ai_agent_zy hello
```

## 配置说明

所有配置集中在 `src/ai_agent_zy/config.py` 的 `Settings` 类中，从环境变量 / `.env` 读取。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DEEPSEEK_API_KEY` | （必填） | DeepSeek API Key |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com` | 接口地址 |
| `DEEPSEEK_MODEL` | `deepseek-chat` | 默认模型 |
| `APP_ENV` | `development` | development / staging / production |
| `LOG_LEVEL` | `INFO` | 日志级别 |

模型选择（已实测）：

- `deepseek-chat`：轻量快速，直接给答案，便宜 —— 日常/工具调用首选
- `deepseek-v4-pro`：推理模型（更强），会先"思考"再回答

## 使用

```powershell
# CLI 对话
ai-agent hello "用一句话解释什么是 AI Agent"

# 或运行示例脚本
python examples/hello_llm.py
```

## 开发工作流

```powershell
# 测试（离线，不依赖真实 API）
.venv\Scripts\python -m pytest

# 代码检查
.venv\Scripts\python -m ruff check .

# 代码格式化
.venv\Scripts\python -m ruff format .

# 类型检查
.venv\Scripts\python -m mypy src
```

> 使用 `make`（WSL / Git Bash / CI）可执行：`make setup` / `make test` / `make lint` / `make format`。

## CI/CD

`.github/workflows/ci.yml` 在每次 push / PR 时自动执行：`ruff check` + `ruff format --check` + `pytest`。
单元测试全部离线，无需密钥。

## 下一步学习路线

1. **工具调用（Function Calling）**：把 `tools/registry.py` 转成 OpenAI tools 参数，让 Agent 真正"动手"。
2. **RAG**：引入向量数据库 + 检索。
3. **多 Agent**：基于 `agents/base.py` 扩展协作编排。

详见 [`docs/architecture.md`](docs/architecture.md)。
