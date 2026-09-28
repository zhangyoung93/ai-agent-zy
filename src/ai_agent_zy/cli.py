"""命令行入口。

用法：
    ai-agent hello "你的问题"
    python -m ai_agent_zy hello "你的问题"
"""

from __future__ import annotations

import argparse
import sys

from .config import get_settings
from .llm.client import LLMClient
from .logging import get_logger, setup_logging

logger = get_logger(__name__)


def cmd_hello(args: argparse.Namespace) -> int:
    """调用 LLM 完成一次对话。"""
    client = LLMClient(get_settings())
    reply = client.complete(
        args.prompt,
        system="你是一个耐心的编程老师，回答通俗易懂。",
    )
    print("\n模型回复：")
    print(reply)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-agent",
        description="AI Agent 命令行工具",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_hello = sub.add_parser("hello", help="调用 LLM 进行一次对话")
    p_hello.add_argument(
        "prompt",
        nargs="?",
        default="用一句话解释：什么是 AI Agent？",
        help="要问的问题（默认演示问题）",
    )
    p_hello.set_defaults(func=cmd_hello)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(get_settings().log_level)

    logger.info("执行命令1: %s", args.command)
    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001 - 顶层统一兜底
        logger.exception("命令执行失败: %s", exc)
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
