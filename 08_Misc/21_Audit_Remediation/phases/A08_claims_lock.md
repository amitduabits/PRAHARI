# A08. Claims lock (K1, K3)

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

No file the jury can read claims a live VAHAN pipe or treats 80k as measured.

## Agent

1. Replace `05_Output/deliverables/own_feed_demo_script.md` with the locked text from `08_Misc/21_Audit_Remediation/scripts/spoken_own.md` (keep any extra timing if already compatible).
2. Write `05_Output/deliverables/gov_feed_demo_script.md` from `scripts/spoken_gov.md`.
3. Grep (case-insensitive) these trees for needles in `scripts/forbidden_claims.md`:
   - `04_Documents/bits-tex/slides.tex`
   - `04_Documents/bits-tex/notes.tex`
   - `04_Documents/PRAHARI_HLD.md`
   - `04_Documents/PRAHARI-Slides.pdf` not greppable; source tex is enough
   - `README.md`, `02_Code/prahari/README.md`
   - `05_Output/deliverables/FINALE_RUNCARD.md`
   - `05_Output/deliverables/*demo_script.md`
4. Allowed: “Face recognition is not the demo.” Allowed: “DESIGN TARGET” within 80 characters of `80,000` or `80{,}000` or `80k`.
5. Forbidden: `integrated with VAHAN`, `live VAHAN`, `live eGujCop`.
6. In HLD §5 the words DESIGN TARGET already exist. Confirm. If a sentence states 80k without the label, add the label.
7. Finale runcard spoken lines must include DESIGN TARGET on the 80k sentence and “representative watchlist”.
8. Rebuild slides/notes only if tex changed. `pdflatex` twice. Copy PDFs to `04_Documents/` and `docs/`.
9. `python scripts/audit_gate.py` prints `PASS K1` and `PASS K3`.

## Done when

- Grep clean per forbidden_claims.md.
- CSV A08-001 DONE.

## Do not

Soften “representative” back to “integrated”. Do not add FRS.
