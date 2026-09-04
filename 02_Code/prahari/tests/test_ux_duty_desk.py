"""U07 anti-slop: duty-desk tokens, labels, no gold tab fill."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "app" / "static" / "styles.css").read_text(encoding="utf-8")
HTML = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")


def test_tokens_present():
    assert "--field" in CSS
    assert "--khaki" in CSS


def test_h1_tracking_not_wide():
    match = re.search(r"h1\s*\{[^}]*letter-spacing:\s*([^;]+)", CSS)
    assert match, "h1 letter-spacing must be set"
    val = match.group(1).strip()
    if val in {"0", "0em", "normal"}:
        return
    num = float(re.sub(r"[a-zA-Z%]", "", val) or "0")
    assert num <= 0.02


def test_no_kicker_uppercase():
    assert ".kicker" not in CSS
    assert "class=\"kicker\"" not in HTML


def test_label_count():
    assert HTML.lower().count("<label") >= 12


def test_analyse_result_card():
    assert "result-card" in HTML
    assert re.search(r'id="analyse-out"[^>]*result-card|class="result-card"[^>]*id="analyse-out"', HTML)


def test_tab_selected_not_gold_fill():
    assert "background: var(--accent)" not in CSS
    assert "--accent" not in CSS
    assert ".tab.on" in CSS or "aria-selected" in HTML


def test_plex_or_noto_in_stack():
    assert "IBM Plex" in CSS or "Noto Sans" in CSS


def test_seven_tabs_and_demo_verbs(client):
    text = client.get("/").text
    assert text.count("data-tab=") == 7
    lower = text.lower()
    assert "analyse this still" in lower
    assert "log in" in lower
    assert "confirm plate" in lower
