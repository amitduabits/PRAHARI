import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from prresearch.p4_admission.simulator import (
    ThreeStrikeHealth, generate_arrivals, rotational_sweep, simulate,
)


def test_refuse_bounds_peak_concurrency():
    reqs = generate_arrivals(4000, 6.0, 2.0, "t4")
    r = simulate(reqs, 4, "refuse")
    assert r["peak_concurrent_decoders"] <= 4
    assert r["refused"] > 0


def test_degrade_blows_the_envelope():
    reqs = generate_arrivals(4000, 6.0, 2.0, "t4")
    assert simulate(reqs, 4, "degrade")["peak_concurrent_decoders"] > 4


def test_queue_trades_refusal_for_latency():
    reqs = generate_arrivals(4000, 6.0, 2.0, "t4")
    refuse = simulate(reqs, 4, "refuse")
    queue = simulate(reqs, 4, "queue")
    assert queue["refusal_rate"] == 0.0
    assert queue["p99_latency_s"] > 10 * refuse["p99_latency_s"]


def test_simulation_is_deterministic():
    a = simulate(generate_arrivals(2000, 3.0, 2.0, "t4"), 4, "refuse")
    b = simulate(generate_arrivals(2000, 3.0, 2.0, "t4"), 4, "refuse")
    assert a == b


def test_three_strikes_needed_to_go_offline():
    h = ThreeStrikeHealth()
    assert h.observe("C1", False) != "offline"
    assert h.observe("C1", False) != "offline"
    assert h.observe("C1", False) == "offline"
    h2 = ThreeStrikeHealth()
    h2.observe("C2", False)
    h2.observe("C2", False)
    assert h2.observe("C2", True) == "live"
    assert h2.observe("C2", False) != "offline"


def test_sweep_matches_analytic_bound():
    r = rotational_sweep(600, 4, 1.0, 1800.0, 0.0, "t4:sweep")
    assert abs(r["mean_coverage_interval_s"] - r["analytic_bound_s"]) < 1.0
