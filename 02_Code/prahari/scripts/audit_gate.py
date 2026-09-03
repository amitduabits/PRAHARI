"""Machine gate for 08_Misc/21_Audit_Remediation. Exit 1 if S2/S3/S4/S5/K1/K3 fail."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
fails: list[str] = []


def out(ok: bool, code: str, reason: str) -> None:
    print(("PASS " if ok else "FAIL ") + code + " " + reason)
    if not ok:
        fails.append(code)


def read(rel: Path) -> str:
    return rel.read_text(encoding="utf-8", errors="replace") if rel.is_file() else ""


auth = read(ROOT / "app" / "auth.py")
paths = read(ROOT / "app" / "paths.py")
cat = read(ROOT / "app" / "services" / "catalogue.py")
index = read(ROOT / "app" / "static" / "index.html")
appjs = read(ROOT / "app" / "static" / "app.js")
hls_js = ROOT / "app" / "static" / "hls.min.js"

s2 = "allowed" in paths and "resolve" in paths and (
    "outside" in paths.lower() or "media root" in paths.lower()
)
out(s2, "S2", "resolve_media_path jails to media roots" if s2 else "path jail missing")
out("def origin_allowed" in cat, "S3", "HLS origin pin present" if "def origin_allowed" in cat else "origin_allowed missing")
out("[:32]" not in auth and "hexdigest()" in auth and "compare_digest" in auth and "lookup_user" in auth, "S4", "full HMAC and compare_digest" if "[:32]" not in auth else "HMAC still sliced or compare missing")
out(hls_js.is_file() and "jsdelivr" not in index.lower(), "S5", "vendored hls.min.js, no jsdelivr" if hls_js.is_file() else "hls.min.js missing or jsdelivr still in index")

needles_k1 = ["integrated with VAHAN", "live VAHAN", "live eGujCop"]
claim_files = [
    REPO / "05_Output" / "deliverables" / "own_feed_demo_script.md",
    REPO / "05_Output" / "deliverables" / "gov_feed_demo_script.md",
    REPO / "05_Output" / "deliverables" / "FINALE_RUNCARD.md",
    REPO / "04_Documents" / "PRAHARI_HLD.md",
    REPO / "04_Documents" / "bits-tex" / "slides.tex",
    REPO / "04_Documents" / "bits-tex" / "notes.tex",
    REPO / "README.md",
]
blob = "\n".join(read(p) for p in claim_files)
k1_hit = [n for n in needles_k1 if n.lower() in blob.lower()]
out(not k1_hit, "K1", "no live-ministry claims" if not k1_hit else "needle " + k1_hit[0])

k3_ok = True
for p in claim_files:
    text = read(p)
    for m in re.finditer(r"80[,\{\}]?000|80k", text, re.I):
        window = text[max(0, m.start() - 80) : m.end() + 80].lower()
        if "design target" not in window and "design-target" not in window:
            k3_ok = False
            break
out(k3_ok, "K3", "80k labelled DESIGN TARGET" if k3_ok else "80k without DESIGN TARGET nearby")

d3 = "no coordinate" in appjs.lower() or "no gis" in appjs.lower() or "have no coordinates" in appjs.lower()
out(d3 and "data-open" in appjs, "D3", "table open + no-coordinates copy" if d3 else "GIS honesty string missing in app.js")

tess = shutil.which("tesseract")
gov_script = read(REPO / "05_Output" / "deliverables" / "gov_feed_demo_script.md") + read(
    REPO / "08_Misc" / "21_Audit_Remediation" / "scripts" / "spoken_gov.md"
)
d2 = bool(tess) or "operator confirm" in gov_script.lower()
out(d2, "D2", "tesseract on PATH" if tess else "confirm lock in spoken script")

print("INFO S1 rotate JUDGE_PASSWORD and SECRET_KEY in .env before any tunnel; gate does not print secrets")
print("INFO S6 COOKIE_SECURE=1 only behind HTTPS")
print("INFO D1 YouTube + Drive are human; not scored here")
print("INFO D4 do not delete data/prahari.db")

if fails:
    print("FAIL " + ",".join(fails))
    sys.exit(1)
print("PASS")
sys.exit(0)
