"""pytest 全局 fixtures。"""

import pytest

from ai_agent_zy.config import Settings


@pytest.fixture
def dummy_settings() -> Settings:
    """带假 key 的配置，用于无需真实 API 的测试。"""
    return Settings(deepseek_api_key="sk-dummy-for-testing")
