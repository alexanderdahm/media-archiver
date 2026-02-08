import argparse
from collections import defaultdict
from datetime import datetime
import sys
from pathlib import Path

from photo_tool.config import load_config, ConfigError, AppConfig
from photo_tool.datetime_resolver import resolve_datetime
from photo_tool.executor import execute_decision
from photo_tool.month_normalizer import normalize_month_folder
from photo_tool.renamer import ensure_unique_name, generate_filename
from photo_tool.reporter import ExecutionResult, ReportConfig, build_report, write_reports
from photo_tool.scanner import scan_directories
from photo_tool.sorter import SortDecision, build_sort_decision


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="media-archiver",
        description="Deterministic photo and video archive organizer",
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to configuration YAML file",
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes to filesystem (default is dry-run)",
    )

    return parser.parse_args(argv)


_MONTH_NAMES = {
    1: "Januar",
    2: "Februar",
    3: "Maerz",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Dezember",
}


def _month_name_from_datetime(value: datetime) -> str:
    """Deprecated shim. Use media_archiver.cli instead."""

    from media_archiver.cli import main


    if __name__ == "__main__":
        raise SystemExit(main())
def _cleanup_empty_dirs(root: Path, candidates: set[Path]) -> None:
