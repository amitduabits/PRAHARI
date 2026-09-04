from app.services.plates import normalise


def test_hyphen_lower_spaces():
    assert normalise("gj-01-ab-1234") == "GJ01AB1234"
    assert normalise("GJ01 AB1234") == "GJ01AB1234"
    assert normalise(" GJ01AB1234 ") == "GJ01AB1234"


def test_rejects_short_and_noise():
    assert normalise("1234") is None
    assert normalise("G1AB1234") is None
