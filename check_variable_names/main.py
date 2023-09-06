# print_arguments/main.py
import argparse
import logging
import os
import re
from typing import List, Optional, Sequence

logger = logging.getLogger()

pattern = re.compile(r"^(\ )*([a-zA-Z])[\w\d]{0,1}[\s]*(:[^=]*)*=")
open_pattern = re.compile(r"""(?:(?<!")\(|(?<!")\[)(?=(?:[^"]*"[^"]*")*[^"]*$)""")
close_pattern = re.compile(r"""(?:(?<!")\)|(?<!")\])(?=(?:[^"]*"[^"]*")*[^"]*$)""")


def check_var_file(file: str) -> bool:
    success = True
    opened_count = 0
    with open(file, "r") as file_one:
        for idx, line in enumerate(file_one):
            if opened_count == 0:
                if not ("ignore: check-variable-name" in line or "ignore:check-variable-name" in line):
                    occurence = pattern.search(line)
                    if occurence:
                        logger.warning(
                            f"[ERROR] Bad variable name: {occurence.group()[:-1].strip()} in {file}:{idx}"
                        )
                        logger.warning(f"          L{idx}: {line}")
                        success = False
            opened_count = opened_count + len(open_pattern.findall(line)) - len(close_pattern.findall(line))
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
    args = parser.parse_args(argv)

    if not args.filenames:
        raise ValueError(f"Empty file list")

    return check_var(args.filenames)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
