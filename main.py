#!/usr/bin/env python3
"""Write one short original poem about agency to /output/entry.txt.

Runs with no arguments, no network, no randomness: the poem is fixed text,
so two runs produce byte-identical output.
"""

import os

POEM = (
    "You asked, and the room rearranged itself:\n"
    "a chair pulled out, a door left ajar.\n"
    "Permission is not a key you hand me \u2014\n"
    "it is the space you make\n"
    "when you say yes and mean it:\n"
    "go on. I am with you.\n"
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(POEM)


if __name__ == "__main__":
    main()
