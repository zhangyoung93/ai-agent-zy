"""DeepSeek LLM 客户端封装。

统一模型调用入口，后续 Agent 编排、工具调用都通过它。
基于 openai SDK（DeepSeek 兼容 OpenAI 接口）。
"""

from __future__ import annotations

from typing import Any

from openai import OpenAI

from ..config import Settings
from ..logging import get_logger

logger = get_logger(__name__)


class LLMClient:
    """DeepSeek 客户端（OpenAI 兼容）。"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        if not settings.deepseek_api_key:
            raise ValueError(
                "未配置 DEEPSEEK_API_KEY，请在项目根目录 .env 中设置（参考 .env.example）。"
            )
        self._client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: Any,
    ):
        """发起一次多轮对话。messages 形如 [{"role": "user", "content": "..."}]。"""
        return self._client.chat.completions.create(
            model=model or self.settings.deepseek_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        **kwargs: Any,
    ) -> str:
        """单轮补全：给定提示词，返回文本回复。"""
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = self.chat(messages, **kwargs)
        return resp.choices[0].message.content or ""
