"""Paper 1 baselines."""

from __future__ import annotations

from prresearch.p1_provenance.dispatch import (
    ALL_BITS,
    BIT,
    ENGINES,
    LazyEngine,
    Registry,
)


class QueryTimeRBAC:
    """Evaluate every policy rule on every frame. Correct, but O(R) per frame."""

    name = "query_time_rbac"

    def __init__(self, registry: Registry, engines: dict[str, LazyEngine]) -> None:
        self.registry = registry
        self.engines = engines
        self.rule_evaluations = 0

    def dispatch(self, camera_id: str, frame_id: int, requested: int = ALL_BITS) -> list[dict]:
        camera, _ = self.registry.rows[camera_id]
        mask = ALL_BITS
        for rule in self.registry.policy:
            self.rule_evaluations += 1
            if rule.predicate(camera):
                mask &= rule.mask()
        mask &= requested
        return [self.engines[n].infer(frame_id) for n in ENGINES if mask & BIT[n]]


class StatelessFallback:
    """No provenance at all: whatever the caller asks for is what runs."""

    name = "stateless_fallback"

    def __init__(self, registry: Registry, engines: dict[str, LazyEngine]) -> None:
        self.registry = registry
        self.engines = engines
        self.rule_evaluations = 0

    def dispatch(self, camera_id: str, frame_id: int, requested: int = ALL_BITS) -> list[dict]:
        return [self.engines[n].infer(frame_id) for n in ENGINES if requested & BIT[n]]


class NaiveUnionDispatch:
    """Run every engine, then filter the records afterwards.

    This is the architecture the patent distinguishes itself from: the answer is
    filtered but the pixels already reached the model, so the privacy property
    is violated even though the output looks identical.
    """

    name = "naive_union_postfilter"

    def __init__(self, registry: Registry, engines: dict[str, LazyEngine]) -> None:
        self.registry = registry
        self.engines = engines
        self.rule_evaluations = 0

    def dispatch(self, camera_id: str, frame_id: int, requested: int = ALL_BITS) -> list[dict]:
        raw = [self.engines[n].infer(frame_id) for n in ENGINES if requested & BIT[n]]
        mask = self.registry.mask_of(camera_id)
        return [r for r in raw if mask & BIT[r["engine"]]]
