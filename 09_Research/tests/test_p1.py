import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from dataclasses import replace

from prresearch.p1_provenance.baselines import NaiveUnionDispatch, StatelessFallback
from prresearch.p1_provenance.dispatch import (
    BIT, ENGINES, LazyEngine, ProvenanceGatedDispatcher, Registry, compile_permitted, default_policy,
)
from prresearch.traces import build_estate


def _engines():
    return {n: LazyEngine(n, weight_bytes=1024) for n in ENGINES}


def test_gov_camera_never_gets_faces():
    cam = build_estate(4, "grid", seed_name="t").cameras[0]
    gov = replace(cam, ownership="Gov", cert_valid=True, data_use_class="public_safety")
    assert not (compile_permitted(gov, default_policy()) & BIT["faces"])


def test_own_camera_with_valid_cert_gets_faces():
    cam = build_estate(4, "grid", seed_name="t").cameras[0]
    own = replace(cam, ownership="Own", cert_valid=True, data_use_class="public_safety")
    assert compile_permitted(own, default_policy()) & BIT["faces"]


def test_rule_order_does_not_matter():
    policy = default_policy()
    for cam in build_estate(60, "grid", seed_name="t").cameras:
        assert compile_permitted(cam, policy) == compile_permitted(cam, list(reversed(policy)))


def test_lazy_faces_never_built_when_no_camera_permits():
    cams = [replace(c, ownership="Gov") for c in build_estate(40, "grid", seed_name="t").cameras]
    reg = Registry()
    for c in cams:
        reg.register(c)
    eng = _engines()
    disp = ProvenanceGatedDispatcher(reg, eng)
    for i, c in enumerate(cams):
        disp.dispatch(c.camera_id, i)
    assert eng["faces"].build_count == 0
    assert not eng["faces"].resident


def test_naive_union_leaks_pixels_even_though_output_matches():
    cams = [replace(c, ownership="Gov") for c in build_estate(40, "grid", seed_name="t").cameras]
    reg = Registry()
    for c in cams:
        reg.register(c)
    gated_eng, naive_eng = _engines(), _engines()
    gated = ProvenanceGatedDispatcher(reg, gated_eng)
    naive = NaiveUnionDispatch(reg, naive_eng)
    for i, c in enumerate(cams):
        a = [r["engine"] for r in gated.dispatch(c.camera_id, i)]
        b = [r["engine"] for r in naive.dispatch(c.camera_id, i)]
        assert sorted(a) == sorted(b)          # identical output
    assert naive_eng["faces"].build_count == 1  # but the model saw the pixels
    assert gated_eng["faces"].build_count == 0


def test_stateless_runs_everything():
    cams = build_estate(10, "grid", seed_name="t").cameras
    reg = Registry()
    for c in cams:
        reg.register(c)
    eng = _engines()
    d = StatelessFallback(reg, eng)
    assert len(d.dispatch(cams[0].camera_id, 0)) == len(ENGINES)


def test_dispatch_does_not_evaluate_rules():
    cams = build_estate(20, "grid", seed_name="t").cameras
    reg = Registry()
    for c in cams:
        reg.register(c)
    d = ProvenanceGatedDispatcher(reg, _engines())
    for i, c in enumerate(cams):
        d.dispatch(c.camera_id, i)
    assert d.rule_evaluations == 0
