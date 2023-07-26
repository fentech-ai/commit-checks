# print_arguments/main.py
import argparse
import logging
import os
import re
from typing import List, Optional, Sequence

logger = logging.getLogger()

pattern = re.compile(r'^(\ )*([a-zA-Z])[\w\d]{0,2}[\s]*(:[^=]*)*=')

def check_var_file(file: str) -> bool:
    success = True
    with open(file, "r") as file_one:
        for idx, line in enumerate(file_one):
            occurence = pattern.search(line)
            if occurence:
                logger.warning(f"[ERROR] Bad variable name: {occurence.group()[:-1].strip()} in {file}")
                logger.warning(f"          L{idx}: {line}")                
                success = False
    return success


def check_var(filenames: list[str]) -> int:
    valid: List[bool] = []
    for filename in filenames:
        if not filename.endswith(".py"):
            valid.append(True)
            continue

        check = check_var_file(filename)
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
        raise ValueError(f"Empty file list")

    return check_var(args.filenames, args.no_fix_files)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())