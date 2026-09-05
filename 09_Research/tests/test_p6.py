import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from prresearch.p6_platform.platform_model import (
    ONBOARD_S, Authority, default_estate, onboarding_cost, registry_footprint, transport_negotiation,
)


def test_bulk_import_cuts_total_onboarding_cost():
    """The honest version of the claim.

    Bulk import is ~2200x cheaper per camera than the form, but the deployed
    mix still routes 12 percent of cameras through the form, and that tail is
    what dominates the total. The saving is real but it is 8x, not 2000x, and
    the paper has to say so.
    """
    est = default_estate(8000)
    mixed = onboarding_cost(est)["total_hours"]
    allform = onboarding_cost([Authority(a.name, a.cameras, a.transport_mix, "web_form") for a in est])["total_hours"]
    assert allform > 8 * mixed
    assert ONBOARD_S["web_form"] / ONBOARD_S["csv_bulk"] > 2000


def test_form_tail_dominates_the_mixed_estate():
    est = default_estate(8000)
    rows = onboarding_cost(est)["per_authority"]
    form_seconds = sum(r["seconds"] for r in rows if r["mode"] == "web_form")
    total = onboarding_cost(est)["total_seconds"]
    form_cameras = sum(r["cameras"] for r in rows if r["mode"] == "web_form")
    assert form_cameras / 8000 < 0.15
    assert form_seconds / total > 0.95


def test_transport_shares_are_scale_invariant():
    a = transport_negotiation(default_estate(800))["shares"]
    b = transport_negotiation(default_estate(80000))["shares"]
    for k in a:
        assert abs(a[k] - b[k]) < 0.01


def test_audit_dominates_registry_within_a_year():
    f = registry_footprint(80000, 365, 120.0)
    assert f["audit_bytes"] > 1000 * f["registry_bytes"]
