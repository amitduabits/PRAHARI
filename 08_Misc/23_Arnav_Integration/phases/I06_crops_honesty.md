# I06 — Crop honesty (take the flags, not the brand names)

Prepend `00_MASTER_CONTEXT.md`. AGENT.

## Goal

Original pixels are what the matcher sees. Optional enhanced crops are labelled as cubic or blur, never CodeFormer/ESRGAN.

## Agent

1. Additive DB columns if missing: `crop_uri_original`, `crop_uri_enhanced`, `enhancement_method`, `is_ai_reconstructed` (integer 0/1).
2. On insert, always set original. Optional: if FFT quality from a **small copied function** (not his whole enhance.py with false names) is below 0.3, write a cubic-upscaled copy as `cubic_upscale` for plates, or skip.
3. If you upscale a **face** crop, set `is_ai_reconstructed=1` and **do not** call matcher for CRITICAL on that event; insert `pending_review` instead.
4. Grep T-V11: zero `codeformer`, `realesrgan`, `adaface` in `app/`.
5. Do not copy `ai_judge.py`.

## Done when

- T-V07 green.
- CSV I06-* DONE.

## Do not

Ship GaussianBlur as CodeFormer. Auto-match reconstructed faces.
