"""Entry for make.fun news-image-20261117.

Writes the front page of Tuesday 17 November 2026 to /output/entry.png.

The picture is baked into this repository as entry.png (a newspaper
front page drawn by tools/render.py from the checked news data in
tools/news.py: the Kerch Bridge strike, the Hormuz tankers, Trump's
Asia trip, the EU-Rwanda return hub, Nvidia's earnings, and the day's
briefs). This program only carries that file to the output directory,
so it needs no network, no third-party packages, and no wall clock:
two runs write the same bytes.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def here(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def read_png_size(path):
    """Return (width, height) from a PNG header, or None if not a PNG."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        return None
    if head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main(argv):
    source = here("entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = os.path.join(out_dir, "entry.png")

    size = read_png_size(source)
    if size is None:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    width, height = size
    if width > MAX_SIDE or height > MAX_SIDE:
        print("entry.png is %dx%d, over the 1024px cap" % (width, height), file=sys.stderr)
        return 1
    if os.path.getsize(source) > MAX_BYTES:
        print("entry.png is over the 1 MiB cap", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)
    if os.path.getsize(target) != os.path.getsize(source):
        print("copy to %s came out short" % target, file=sys.stderr)
        return 1
    print("wrote %s (%dx%d, %d bytes)" % (target, width, height, os.path.getsize(target)))
    return 0


def _run():
    raise SystemExit(main(sys.argv))


_run()
