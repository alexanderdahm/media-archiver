"""Data models used by photo_tool."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Photo:
    path: Path
    date: datetime | None = None
    size: int | None = None
