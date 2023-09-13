# print_arguments/main.py
import argparse
import logging
import os
import re
from typing import List, Optional, Sequence

logger = logging.getLogger()


def fix_file(file: str) -> None:
    logging.warning(f"Fixing {file}")
    with open("tmp.py", "w") as output:
        with open(file, "r") as file_one:
            for line in file_one:
                if not re.search("print", line):
                    output.write(line)

    os.replace("tmp.py", file)


def check_print_file(file: str) -> bool:
    success = True
    with open(file, "r") as file_one:
        for idx, line in enumerate(file_one):
            if re.search("print", line):
                logger.warning(f"[ERROR] detected print : {file} : L{idx}: {line}")
                success = False
    return success


def check_fix_print(filenames: list[str], fix_files: bool) -> int:
    valid: List[bool] = []
    for filename in filenames:
        if not filename.endswith(".py"):
            valid.append(True)
            continue

        check = check_print_file(filename)
        if fix_files and not check:
            fix_file(filename)
        valid.append(check)
    if all(valid):
        return 0
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    parser.add_argument("--no-fix-files", action="store_false")
    args = parser.parse_args(argv)

    if not args.filenames:
        print("Empty file list")
        return 0

    return check_fix_print(args.filenames, args.no_fix_files)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
