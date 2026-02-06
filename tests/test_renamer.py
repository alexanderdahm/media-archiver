from pathlib import Path
from photo_tool.renamer import rename_file


def test_rename_file(tmp_path):
    p = tmp_path / "a.txt"
    p.write_text("x")
    dst = rename_file(p, "b.txt")
    assert dst.exists()
