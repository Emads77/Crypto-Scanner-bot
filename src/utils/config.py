import tomli
from pathlib import Path
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from config.toml"""
    config_path = Path("config.toml")
    
    if not config_path.exists():
        raise FileNotFoundError(
            "config.toml not found. Create it with your Telegram credentials."
        )
    
    with open(config_path, "rb") as f:
        return tomli.load(f)