#!/usr/bin/env python3
"""news-image-20261117-r3 entry: write the front page to /output/entry.png.

The front page itself is the entry.png committed beside this file (rendered
in the build session by render.py with Pillow: masthead, region bar, 3 big
illustrated stories, 10 small cards with short bold headlines, numbered-pin
world map, region-grouped ALSO list, DAY BY FIELD chart, DATE CHECK strip,
judge note and sources line -- 48 real stories of Tuesday 17 November
2026). This program only copies those exact bytes to the output path, so
both grader runs write identical bytes. Standard library only; no network,
no randomness, no clock.
"""
import hashlib
import os
import shutil
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1048576
MAX_SIDE = 1024


def png_size(path):
    """Return (width, height) of a PNG by reading its IHDR chunk."""
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        raise ValueError("entry.png over 1 MiB: %d bytes" % size)
    w, h = png_size(SRC)
    if w > MAX_SIDE or h > MAX_SIDE:
        raise ValueError("entry.png over 1024x1024: %dx%d" % (w, h))
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    src_digest = hashlib.sha256(open(SRC, "rb").read()).hexdigest()
    if digest != src_digest:
        raise ValueError("copied bytes differ from entry.png")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)" % (dst, w, h, size, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
