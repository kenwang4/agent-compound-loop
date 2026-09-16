#!/usr/bin/env python3
"""CLI shim — prefer `writeback-candidate` or `python -m writeback_candidate`."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from a bare clone without install
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from writeback_candidate.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
