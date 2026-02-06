from pathlib import Path
from photo_tool.datetime_resolver import resolve_datetime


def test_resolve_datetime(tmp_path):
    p = tmp_path / "img.jpg"
    p.write_text("x")
    dt = resolve_datetime(p)
    assert dt is not None
