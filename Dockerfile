# AI Agent 项目基础镜像（后续按需扩展）
FROM python:3.12-slim

WORKDIR /app

# 先复制依赖清单，利用 Docker 层缓存
COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .

# 运行时通过环境变量注入密钥：docker run -e DEEPSEEK_API_KEY=sk-xxx ...
CMD ["python", "-m", "ai_agent_zy", "hello"]
