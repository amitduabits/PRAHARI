import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from prresearch.p3_nextcam.predictors import DistanceOnly, TransitionFrequency, evaluate
from prresearch.traces import build_estate, generate_trips


def test_frequency_beats_distance_on_irregular_topology():
    estate = build_estate(200, "irregular", seed_name="t3")
    trips = generate_trips(estate, 1500, seed_name="t3:trips")
    train, test = trips[:1200], trips[1200:]
    freq = evaluate(TransitionFrequency(estate).fit(train), test)
    dist = evaluate(DistanceOnly(estate), test)
    assert freq["top1"] > dist["top1"] * 1.5


def test_falls_back_to_distance_without_history():
    estate = build_estate(60, "grid", seed_name="t3")
    pred = TransitionFrequency(estate).fit([])
    out = pred.predict([(estate.cameras[0].camera_id, 0.0)], k=3)
    assert len(out) == 3
    assert pred.fallback_uses == 1


def test_probabilities_sum_to_one():
    estate = build_estate(80, "grid", seed_name="t3")
    pred = TransitionFrequency(estate).fit(generate_trips(estate, 400, seed_name="t3:p"))
    for cid in list(pred.trans)[:20]:
        assert abs(sum(p for _, p in pred.probabilities(cid)) - 1.0) < 1e-9
