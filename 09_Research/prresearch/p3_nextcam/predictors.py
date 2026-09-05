"""Paper 3: next-camera prediction from observational data only.

The proposed method is the one shipped in app/services/predict.py: rank the
next camera by the empirical frequency of historical transitions out of the
last-seen camera, and fall back to GIS distance when that camera has no
outgoing history. No Kalman filter, no road network, no motion model.

Baselines implemented here:

  DistanceOnly       nearest cameras by great-circle distance
  ConstantVelocity   a Kalman-style extrapolation of the last displacement,
                     scoring cameras by distance to the predicted position
  GraphNeighbour     the road-network method: assumes the true adjacency is
                     known and ranks its neighbours by degree
  MarkovBackoff      transition frequency with add-alpha smoothing over a
                     global next-camera prior (a stronger statistical baseline)

Every predictor exposes `fit(trips)` then `predict(history, k)`.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Sequence

from prresearch.traces import Camera, Estate, haversine_km

History = Sequence[tuple[str, float]]


class Predictor:
    name = "base"

    def fit(self, trips: Sequence[History]) -> "Predictor":
        return self

    def predict(self, history: History, k: int = 3) -> list[str]:
        raise NotImplementedError


class DistanceOnly(Predictor):
    name = "distance_only"

    def __init__(self, estate: Estate) -> None:
        self.by_id = estate.by_id()
        self._sorted: dict[str, list[str]] = {}

    def _neighbours(self, cid: str) -> list[str]:
        if cid not in self._sorted:
            a = self.by_id[cid]
            d = [
                (haversine_km(a.lat, a.lon, c.lat, c.lon), c.camera_id)
                for c in self.by_id.values()
                if c.camera_id != cid
            ]
            d.sort()
            self._sorted[cid] = [cid2 for _, cid2 in d[:20]]
        return self._sorted[cid]

    def predict(self, history: History, k: int = 3) -> list[str]:
        return self._neighbours(history[-1][0])[:k]


class ConstantVelocity(Predictor):
    """Kalman-style: extrapolate the last displacement, then snap to cameras."""

    name = "constant_velocity"

    def __init__(self, estate: Estate) -> None:
        self.cams: list[Camera] = list(estate.cameras)
        self.by_id = estate.by_id()

    def predict(self, history: History, k: int = 3) -> list[str]:
        last = self.by_id[history[-1][0]]
        if len(history) < 2:
            return DistanceOnly(Estate(self.cams)).predict(history, k)
        prev = self.by_id[history[-2][0]]
        dlat = last.lat - prev.lat
        dlon = last.lon - prev.lon
        plat, plon = last.lat + dlat, last.lon + dlon
        d = [
            (haversine_km(plat, plon, c.lat, c.lon), c.camera_id)
            for c in self.cams
            if c.camera_id != last.camera_id
        ]
        d.sort()
        return [cid for _, cid in d[:k]]


class GraphNeighbour(Predictor):
    """Road-network method, given the true topology as an oracle."""

    name = "graph_neighbour_oracle"

    def __init__(self, estate: Estate) -> None:
        self.adj = estate.adjacency
        self.deg = {cid: len(v) for cid, v in estate.adjacency.items()}
        self.by_id = estate.by_id()

    def predict(self, history: History, k: int = 3) -> list[str]:
        cur = history[-1][0]
        nbrs = list(self.adj.get(cur) or [])
        if not nbrs:
            return []
        a = self.by_id[cur]
        nbrs.sort(key=lambda c: (-self.deg.get(c, 0), haversine_km(a.lat, a.lon, self.by_id[c].lat, self.by_id[c].lon)))
        return nbrs[:k]


class TransitionFrequency(Predictor):
    """The proposed method: empirical transitions, GIS distance as fallback."""

    name = "transition_frequency"

    def __init__(self, estate: Estate) -> None:
        self.estate = estate
        self.by_id = estate.by_id()
        self.trans: dict[str, Counter] = defaultdict(Counter)
        self._dist = DistanceOnly(estate)
        self.fallback_uses = 0
        self.history_uses = 0

    def fit(self, trips: Sequence[History]) -> "TransitionFrequency":
        for trip in trips:
            for (c1, _), (c2, _) in zip(trip, trip[1:]):
                if c1 != c2:
                    self.trans[c1][c2] += 1
        return self

    def probabilities(self, cid: str) -> list[tuple[str, float]]:
        counts = self.trans.get(cid)
        if not counts:
            return []
        total = sum(counts.values())
        return [(c, n / total) for c, n in counts.most_common()]

    def predict(self, history: History, k: int = 3) -> list[str]:
        cur = history[-1][0]
        ranked = self.probabilities(cur)
        if ranked:
            self.history_uses += 1
            out = [c for c, _ in ranked[:k]]
            if len(out) < k:  # pad with geography, as the deployed code does
                out += [c for c in self._dist.predict(history, k * 2) if c not in out]
            return out[:k]
        self.fallback_uses += 1
        return self._dist.predict(history, k)


class MarkovBackoff(TransitionFrequency):
    """Transition frequency plus an add-alpha backoff to a global prior."""

    name = "markov_backoff"

    def __init__(self, estate: Estate, alpha: float = 0.35) -> None:
        super().__init__(estate)
        self.alpha = alpha
        self.prior: Counter = Counter()

    def fit(self, trips: Sequence[History]) -> "MarkovBackoff":
        super().fit(trips)
        for trip in trips:
            for c, _ in trip[1:]:
                self.prior[c] += 1
        return self

    def predict(self, history: History, k: int = 3) -> list[str]:
        cur = history[-1][0]
        counts = self.trans.get(cur) or Counter()
        cand = set(counts) | set(self._dist.predict(history, 12))
        if not cand:
            return []
        total = sum(counts.values())
        prior_total = sum(self.prior.values()) or 1
        scored = []
        for c in cand:
            p_hist = counts.get(c, 0) / total if total else 0.0
            p_prior = self.prior.get(c, 0) / prior_total
            w = total / (total + self.alpha * len(cand)) if total else 0.0
            scored.append((w * p_hist + (1 - w) * p_prior, c))
        scored.sort(reverse=True)
        return [c for _, c in scored[:k]]


def evaluate(pred: Predictor, trips: Sequence[History], min_prefix: int = 1) -> dict:
    """Leave-one-step-out: for every trip position, predict the next camera."""
    ranked, truth = [], []
    for trip in trips:
        for i in range(min_prefix, len(trip)):
            ranked.append(pred.predict(trip[:i], k=3))
            truth.append(trip[i][0])
    top1 = sum(1 for r, y in zip(ranked, truth) if r[:1] and r[0] == y)
    top3 = sum(1 for r, y in zip(ranked, truth) if y in r[:3])
    n = len(truth) or 1
    return {"method": pred.name, "n_queries": len(truth), "top1": top1 / n, "top3": top3 / n}
