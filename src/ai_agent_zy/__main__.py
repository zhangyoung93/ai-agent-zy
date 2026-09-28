"""支持 `python -m ai_agent_zy` 直接运行 CLI。"""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
