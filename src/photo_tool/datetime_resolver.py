"""Resolve a datetime for a photo from various sources."""

from datetime import datetime


def resolve_datetime(path):
    """Placeholder: return file modification time as datetime."""
    return datetime.fromtimestamp(path.stat().st_mtime)
