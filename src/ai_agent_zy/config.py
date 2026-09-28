"""应用配置：基于 pydantic-settings 从环境变量 / .env 加载。

设计要点：
- 集中管理所有可配置项，类型安全、启动即校验；
- 敏感信息（API Key）只从环境变量读取，绝不写进代码；
- 不同环境（dev/staging/prod）通过 .env 或环境变量区分。
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置。字段名会与同名环境变量（不区分大小写）自动映射。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---- LLM ----
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    # ---- 应用 ----
    app_env: str = "development"  # development | staging | production
    log_level: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """获取全局唯一配置实例（进程内缓存，避免重复解析 .env）。"""
    return Settings()
