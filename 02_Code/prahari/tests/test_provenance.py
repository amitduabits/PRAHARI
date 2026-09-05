from app.services.analyse import engines_for
from app.services.provenance import classify_row, faces_allowed, is_sandbox_id, region_of


def test_sandbox_ids():
    assert is_sandbox_id("cam04")
    assert is_sandbox_id("CAM04")
    assert not is_sandbox_id("CAM-OWN-001")
    assert not is_sandbox_id("CAM-VAL-001")


def test_faces_allowed_own_only():
    assert faces_allowed({"camera_id": "CAM-OWN-001", "ownership": "Own"})
    assert not faces_allowed({"camera_id": "CAM-VAL-001", "ownership": "Gov"})
    assert not faces_allowed({"camera_id": "cam04", "ownership": "Own"})


def test_engines_for_uses_provenance():
    assert "faces" not in engines_for({"camera_id": "cam04", "ownership": "Gov"})
    own = engines_for({"camera_id": "CAM-OWN-001", "ownership": "Own"})
    # faces only present if ANALYTICS_ENGINES includes it
    assert "anpr" in own or "objects" in own or "faces" in own


def test_classify_and_region():
    row = classify_row({"id": "cam04", "name": "04 Paldi Circle"})
    assert row["ownership"] == "Gov"
    assert row["frs_eligible"] is False
    assert row["sandbox"] is True
    assert region_of({"location": "Paldi Circle"}) == "ahmedabad"
    own = classify_row({"camera_id": "CAM-OWN-001", "ownership": "Own", "location": "Own-feed"})
    assert own["frs_eligible"] is True
