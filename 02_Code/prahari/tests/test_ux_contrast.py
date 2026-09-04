"""U07: WCAG 2.2 AA contrast on locked :root tokens."""

import re
from pathlib import Path

CSS = (Path(__file__).resolve().parents[1] / "app" / "static" / "styles.css").read_text(encoding="utf-8")


def _hex_tokens() -> dict[str, str]:
    root = CSS.split(":root", 1)[1].split("}", 1)[0]
    return {m.group(1): m.group(2).lower() for m in re.finditer(r"--([a-z]+):\s*(#[0-9a-fA-F]{6})", root)}


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    l1, l2 = _luminance(a), _luminance(b)
    light, dark = max(l1, l2), min(l1, l2)
    return (light + 0.05) / (dark + 0.05)


def test_token_count_and_high_only_gold():
    tokens = _hex_tokens()
    assert len(tokens) <= 12
    css_gold = [m.group(0) for m in re.finditer(r"#d4a017", CSS, re.I)]
    assert len(css_gold) == 1
    assert tokens.get("high") == "#d4a017"


def test_text_contrast_aa():
    t = _hex_tokens()
    assert contrast(t["ink"], t["field"]) >= 7.0
    assert contrast(t["ink"], t["panel"]) >= 7.0
    assert contrast(t["muted"], t["field"]) >= 4.5
    assert contrast(t["critical"], t["panel"]) >= 3.0
    assert contrast(t["khaki"], t["field"]) >= 3.0
    assert contrast(t["paper"], t["navy"]) >= 4.5
