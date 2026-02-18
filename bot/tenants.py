import os
import re
import yaml
from bot.config import TENANTS_CONFIG
from bot.logger import setup_logger

logger = setup_logger()

_ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")


def _resolve_env_value(value):
    if not isinstance(value, str):
        return value

    def replace(match):
        var_name = match.group(1)
        env_value = os.getenv(var_name)
        if env_value is None:
            logger.warning(f"Missing env var for config: {var_name}")
            return ""
        return env_value

    return _ENV_PATTERN.sub(replace, value)


def _resolve_env(obj):
    if isinstance(obj, dict):
        return {k: _resolve_env(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolve_env(v) for v in obj]
    return _resolve_env_value(obj)


def load_tenants(config_path=TENANTS_CONFIG):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Tenants config not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        raw = yaml.safe_load(file) or {}

    data = _resolve_env(raw)
    tenants = data.get("tenants", [])
    if not tenants:
        logger.warning("No tenants found in config.")
    return tenants


def get_enabled_tenants(config_path=TENANTS_CONFIG):
    tenants = load_tenants(config_path)
    return [t for t in tenants if t.get("enabled", True)]
