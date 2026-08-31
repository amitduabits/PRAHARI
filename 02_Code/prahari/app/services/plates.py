"""Indian number-plate normaliser. Event time is not this module's job."""

from __future__ import annotations

import re

PLATE_RE = re.compile(r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$")


def normalise(raw: str | None) -> str | None:
    if raw is None:
        return None
    compact = re.sub(r"[\s\-]", "", str(raw)).upper()
    if not compact:
        return None
    if PLATE_RE.match(compact):
        return compact
    return None
