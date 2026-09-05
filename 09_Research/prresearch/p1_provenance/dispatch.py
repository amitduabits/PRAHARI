"""Paper 1: provenance-gated inference dispatch.

Mirrors app/services/analyse.py::engines_for, which strips the facial engine
from the permitted set for any camera that is not owned by the operator. Here
the mechanism is generalised to a multi-attribute policy and the permitted set
is compiled once, at registration time, into a bitmask carried by the registry
row. Dispatch is then a single bitmask AND, independent of policy size.

Two properties the paper claims are enforced here in code:

  P1  Dispatch cost is O(1) in the number of policy rules.
  P2  Lazy construction: an engine's weights are never materialised unless some
      registered camera's permitted set contains it. If no camera in the estate
      is permitted facial recognition, the facial model is never built, so the
      weights never enter process memory.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from prresearch.traces import Camera

ENGINES: tuple[str, ...] = ("anpr", "objects", "faces", "occupancy")
BIT = {name: 1 << i for i, name in enumerate(ENGINES)}
ALL_BITS = (1 << len(ENGINES)) - 1


@dataclass(frozen=True)
class Rule:
    """A deny rule: if `predicate(camera)` holds, remove `engines` from the set.

    Deny rules compose by intersection, so rule order does not change the
    result. That is what makes registration-time compilation sound.
    """

    name: str
    predicate: Callable[[Camera], bool]
    engines: tuple[str, ...]

    def mask(self) -> int:
        m = 0
        for e in self.engines:
            m |= BIT[e]
        return ALL_BITS & ~m


def default_policy() -> list[Rule]:
    """The deployed PRAHARI policy, written out as attribute rules."""
    return [
        Rule("frs_own_cameras_only", lambda c: c.ownership != "Own", ("faces",)),
        Rule("frs_needs_valid_cert", lambda c: not c.cert_valid, ("faces",)),
        Rule("traffic_only_no_biometrics", lambda c: c.data_use_class == "traffic_only", ("faces",)),
        Rule("restricted_anpr_only", lambda c: c.data_use_class == "restricted", ("faces", "objects", "occupancy")),
        Rule("expired_cert_no_inference", lambda c: not c.cert_valid and c.ownership == "Private", ("faces", "objects", "occupancy", "anpr")),
        Rule("occupancy_requires_objects", lambda c: c.data_use_class == "restricted", ("occupancy",)),
    ]


def compile_permitted(camera: Camera, policy: Iterable[Rule]) -> int:
    """Registration-time compilation. Called once per camera, never per frame."""
    mask = ALL_BITS
    for rule in policy:
        if rule.predicate(camera):
            mask &= rule.mask()
    return mask


def engines_of(mask: int) -> list[str]:
    return [e for e in ENGINES if mask & BIT[e]]


class LazyEngine:
    """Stands in for a model whose weights are expensive and privacy-relevant."""

    def __init__(self, name: str, weight_bytes: int = 1 << 24) -> None:
        self.name = name
        self.weight_bytes = weight_bytes
        self._weights: bytearray | None = None
        self.build_count = 0

    @property
    def resident(self) -> bool:
        return self._weights is not None

    def infer(self, frame_id: int) -> dict:
        if self._weights is None:  # lazy singleton, as in the deployed engine loaders
            self._weights = bytearray(self.weight_bytes)
            self.build_count += 1
        return {"engine": self.name, "frame_id": frame_id}


class Registry:
    """Camera registry that stores the compiled permitted-engine mask."""

    def __init__(self, policy: Iterable[Rule] | None = None) -> None:
        self.policy = list(policy if policy is not None else default_policy())
        self.rows: dict[str, tuple[Camera, int]] = {}
        self.compile_calls = 0

    def register(self, camera: Camera) -> int:
        mask = compile_permitted(camera, self.policy)
        self.compile_calls += 1
        self.rows[camera.camera_id] = (camera, mask)
        return mask

    def mask_of(self, camera_id: str) -> int:
        return self.rows[camera_id][1]


class ProvenanceGatedDispatcher:
    """The proposed method. One bitmask AND per frame."""

    name = "provenance_gated"

    def __init__(self, registry: Registry, engines: dict[str, LazyEngine]) -> None:
        self.registry = registry
        self.engines = engines
        self.rule_evaluations = 0  # zero by construction at dispatch time

    def dispatch(self, camera_id: str, frame_id: int, requested: int = ALL_BITS) -> list[dict]:
        mask = self.registry.mask_of(camera_id) & requested
        out = []
        for name in ENGINES:
            if mask & BIT[name]:
                out.append(self.engines[name].infer(frame_id))
        return out
