"""Rename files according to resolved datetimes and rules."""

from pathlib import Path


def rename_file(src: Path, new_name: str):
    dst = src.with_name(new_name)
    src.replace(dst)
    return dst
