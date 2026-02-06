"""Filesystem scanner for photo_tool"""

from pathlib import Path


def scan_dirs(directories):
    for d in directories:
        p = Path(d)
        if p.exists():
            for f in p.rglob("*"):
                yield f
