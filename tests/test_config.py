"""测试配置加载。全部离线，不依赖真实 API Key。"""

from ai_agent_zy.config import Settings


def test_settings_defaults() -> None:
    s = Settings()
    assert s.deepseek_base_url == "https://api.deepseek.com"
    assert s.deepseek_model == "deepseek-chat"
    assert s.app_env == "development"
    assert s.is_production is False


def test_settings_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
    s = Settings()
    assert s.deepseek_api_key == "sk-test"
    assert s.deepseek_model == "deepseek-v4-pro"


def test_is_production() -> None:
    assert Settings(app_env="production").is_production is True
    assert Settings(app_env="staging").is_production is False
