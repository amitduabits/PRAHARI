"""T-V11: app/ must not name models that are not loaded."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "app"
FORBIDDEN = ("codeformer", "realesrgan", "adaface")


def test_no_forbidden_model_names_in_app():
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if path.suffix.lower() not in {".py", ".html", ".js", ".css", ".txt", ".md"}:
            continue
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for needle in FORBIDDEN:
            if needle in text:
                hits.append(f"{path.relative_to(ROOT)}:{needle}")
    assert hits == []
