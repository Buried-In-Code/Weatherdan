import csv
import logging
from argparse import ArgumentParser, Namespace
from datetime import date
from pathlib import Path

from pathvalidate.argparse import sanitize_filepath_arg

from common import __version__, setup_logging
from common.statistics import print_stats
from common.storage import Reading, to_file

LOGGER = logging.getLogger("Weatherdan.importer")


def parse_arguments() -> Namespace:
    parser = ArgumentParser(prog="Weatherdan", allow_abbrev=False)
    parser.version = __version__
    parser.add_argument("import_file", type=sanitize_filepath_arg)
    parser.add_argument("--version", action="version")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main():
    args = parse_arguments()
    setup_logging(args.debug)

    import_file = Path(args.import_file).resolve()
    if not import_file.exists():
        LOGGER.error(f"{args.import_file} not found")
        return
    entries = set()
    with import_file.open("r", encoding="UTF-8") as stream:
        reader = csv.DictReader(stream)
        for entry in reader:
            entries.add(
                Reading(
                    timestamp=date.fromisoformat(entry["Timestamp"]), value=float(entry["Value"])
                )
            )
    to_file(*entries)
    print_stats()
    import_file.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
