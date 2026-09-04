"""U00 freeze: demo-script strings must survive the duty-desk restyle.

Kill list for U01 (current AI tells, 04 Sep 2026):
- styles.css .kicker uppercase + letter-spacing 0.08em
- h1 letter-spacing 0.12em
- Segoe-only stack; --accent #d4a017 gold tab fill
- --bg #0b1220 navy void
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_demo_script_strings_on_index(client):
    text = client.get("/").text
    lower = text.lower()
    assert "analyse this still" in lower
    assert "DESIGN TARGET" in text
    assert "80,000" in text or "80000" in text
    assert "Enroll" in text
    assert "Reconstruct" in text
    assert "confirm plate" in lower or "operator confirm" in lower
    for tab in ("operations", "cameras", "track", "alerts", "watchlist", "onboard", "gaps"):
        assert f'data-tab="{tab}"' in text
    assert "lorem" not in lower
    assert "todo" not in lower
    assert "tbd" not in lower
    assert "rtsp://" not in lower


def test_seven_tabs_only():
    html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")
    assert html.count("data-tab=") == 7
