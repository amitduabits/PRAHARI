from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import init_db
from app.services.health_probe import probe_reachable


def main() -> None:
    init_db()
    print(probe_reachable())


if __name__ == "__main__":
    main()
