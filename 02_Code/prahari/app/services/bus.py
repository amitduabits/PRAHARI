"""In-process alert bus. PoC stand-in for Kafka."""

from __future__ import annotations

import asyncio
from collections import deque
from typing import Any

_recent: deque[dict[str, Any]] = deque(maxlen=50)
_queues: list[asyncio.Queue] = []


def notify(alert: dict[str, Any]) -> None:
    _recent.append(alert)
    for queue in list(_queues):
        try:
            queue.put_nowait(alert)
        except Exception:
            pass


def subscribe() -> asyncio.Queue:
    queue: asyncio.Queue = asyncio.Queue(maxsize=32)
    _queues.append(queue)
    return queue


def unsubscribe(queue: asyncio.Queue) -> None:
    try:
        _queues.remove(queue)
    except ValueError:
        pass


def recent() -> list[dict[str, Any]]:
    return list(_recent)
