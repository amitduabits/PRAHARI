# How to execute (Arnav engine pack)

Build engine: one conversation = `00_MASTER_CONTEXT.md` + exactly one `phases/I*.md`.  
Fetch Arnav’s files with `git clone --depth 1 https://github.com/ArAv-1/PRAHARI-3.0.git` into `%TEMP%\PRAHARI-3.0` or `08_Misc/23_Arnav_Integration/_upstream/` (gitignore that folder). Copy **named files only**.

## Daily loop

1. Open `csv/integration_actions.csv`. Filter `status!=DONE` and `priority=P0`.
2. Agent rows: new chat, master context, one phase.
3. After each phase: `cd 02_Code/prahari` then `python -m pytest -q` and `python scripts/audit_gate.py`.
4. Tick the CSV. Push `amitduabits/PRAHARI` `main`. Never commit `.env`, AdaFace-named stubs as production, or `yolov8n.pt` if the team prefers git-lfs/download.

## Gates

```
I00 pytest + audit_gate
     │
     ├─ I01 copy layout
     ├─ I02 facenet behind match() ── I03 FRS law tests must stay green
     ├─ I04 yolo behind detect/recognize
     ├─ I05 bytetrack
     ├─ I06 crop honesty
     ├─ I07 enroll UI + pending_review
     ├─ I08 predict
     └─ I09 query optional
              │
            I10 full pytest
            I11 docs
            I12 human own-feed FaceNet still (optional)
```

If torch is not installed, I02/I04/I05 still DONE when the **fallback** path is tested and the swap path is skip-guarded.

## Parallel to Phase 1 videos

Do not delay C13 YouTube for FaceNet. Record the current backend first. Re-shoot own-feed only if FaceNet is green on CAM-OWN-001 before 07 Sep noon.

## Do not

`git pull` ArAv-1 into this repo. `pip install` vision extras as a required CI step. Run FaceNet on a Sentinel id.
