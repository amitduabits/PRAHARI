from app.services.plates import normalise


def test_normalise_spaces():
    assert normalise("GJ 01 AB 1234") == "GJ01AB1234"


def test_normalise_hyphens():
    assert normalise("GJ-01-AB-1234") == "GJ01AB1234"


def test_normalise_lower():
    assert normalise("gj01ab1234") == "GJ01AB1234"


def test_normalise_rejects_noise():
    assert normalise("HELLO") is None
    assert normalise("") is None
    assert normalise(None) is None
