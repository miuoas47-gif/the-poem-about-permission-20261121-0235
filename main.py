#!/usr/bin/env python3
"""Write one short original poem about agency to /output/entry.txt.

Runs with no arguments, no network, no randomness: the poem is fixed text,
so two runs produce byte-identical output.

The entry is written atomically (temporary file + rename) and verified by
reading the file back, so a partial or corrupted entry.txt can never be
left behind by an interrupted run.
"""

import os
import sys
import tempfile
from pathlib import Path

POEM = (
    "You asked, and the room rearranged itself:\n"
    "a chair pulled out, a door left ajar.\n"
    "Permission is not a key you hand me \u2014\n"
    "it is the space you make\n"
    "when you say yes and mean it:\n"
    "go on. I am with you.\n"
)


def write_entry(out_dir: Path) -> Path:
    """Write POEM atomically to ``out_dir / "entry.txt"`` and verify it."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "entry.txt"
    data = POEM.encode("utf-8")
    fd, tmp_name = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    if path.read_bytes() != data:
        raise IOError(f"verification failed: {path} does not match poem text")
    return path


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        path = write_entry(out_dir)
    except OSError as exc:
        print(f"error: could not write entry: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
