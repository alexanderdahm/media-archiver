"""Configuration loader for photo_tool"""

from pathlib import Path
import yaml


def load_config(path: str):
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)
