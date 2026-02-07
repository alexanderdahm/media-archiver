import argparse
from collections import defaultdict
from datetime import datetime
import sys
from pathlib import Path

from photo_tool.config import load_config, ConfigError, AppConfig
from photo_tool.datetime_resolver import resolve_datetime
from photo_tool.executor import execute_decision
from photo_tool.month_normalizer import normalize_month_folder
from photo_tool.renamer import generate_filename
from photo_tool.reporter import ExecutionResult, ReportConfig, build_report, write_reports
from photo_tool.scanner import scan_directories
from photo_tool.sorter import build_sort_decision


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="photo-tool",
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
    return _MONTH_NAMES[value.month]


def _current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")


def run_pipeline(config: AppConfig, apply: bool) -> None:
    scan_result = scan_directories([config.paths.unsorted])

    planned_names: dict[Path, set[str]] = defaultdict(set)
    execution_results: list[ExecutionResult] = []

    for info in scan_result.supported:
        resolution = resolve_datetime(
            filename=info.name,
            exif_datetime=None,
            fs_modified=datetime.fromtimestamp(info.modified_timestamp),
        )

        month_folder = normalize_month_folder(
            _month_name_from_datetime(resolution.datetime)
        )
        if month_folder is None:
            continue

        target_dir = config.paths.archive_root / f"{resolution.datetime.year:04d}" / month_folder
        existing_names = planned_names[target_dir]

        canonical_name = generate_filename(
            original_name=info.name,
            resolved_datetime=resolution.datetime,
            source=resolution.source,
            existing_names=existing_names,
        )

        planned_names[target_dir].add(canonical_name)
        target_path = target_dir / canonical_name
        target_exists = target_path.exists()

        decision = build_sort_decision(
            archive_root=config.paths.archive_root,
            source_path=info.absolute_path,
            resolved_datetime=resolution.datetime,
            month_folder=month_folder,
            canonical_name=canonical_name,
            move_files=config.behavior.move_files,
            target_exists=target_exists,
        )

        performed = execute_decision(
            decision=decision,
            apply=apply,
        )

        execution_results.append(
            ExecutionResult(decision=decision, performed=performed)
        )

    report = build_report(
        results=execution_results,
        config=ReportConfig(
            dry_run=not apply,
            move_files=config.behavior.move_files,
        ),
        timestamp=_current_timestamp(),
    )

    if config.reporting.markdown or config.reporting.json:
        write_reports(
            report=report,
            output_dir=config.paths.report_output,
            prefix="dry_run" if not apply else "apply",
        )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        config = load_config(Path(args.config))
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    if args.apply and config.behavior.dry_run:
        print(
            "WARNING: --apply was provided, but config.behavior.dry_run is true. "
            "No filesystem changes will be performed.",
            file=sys.stderr,
        )
    apply = args.apply and not config.behavior.dry_run
    run_pipeline(config, apply)

    print("Configuration loaded successfully.")
    print(f"Dry-run mode: {config.behavior.dry_run and not args.apply}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
