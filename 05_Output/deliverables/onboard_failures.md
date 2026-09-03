# Onboard failures

Client: PRAHARI/OpenCV-TCP
Host: cctv.corp8.cloud (catalogue) / 103.250.160.189:8554 (RTSP)
UTC: 2026-09-03T06:10:14Z
Catalogue: GET https://cctv.corp8.cloud/cameras.json after POST /auth/login
Synced: 30 cameras. Manifest has no live flag; listed cameras treated as live until a probe fails.
Do not email SCRB on a camera that is missing from cameras.json. 502 on live.corp8.cloud (01 Sep) is obsolete.

| camera_id | location | probe | url | error |
|---|---|---|---|---|
| cam04 | 04 Paldi Circle | live | `rtsp://103.250.160.189:8554/stream/cam04` | |
| cam01 | 01 Chiman bhai Bridge | live | `rtsp://103.250.160.189:8554/stream/cam01` | |

No down-reports. cam04 RTSP-TCP frame also saved at `03_Data/recordings/first_live_frame.png` (1920x1080, PTS 1080 ms).

## Catalogue ids

- `cam01` 01 Chiman bhai Bridge
- `cam02` 02 Janpath
- `cam03` 03 O.N.G.C. Office
- `cam04` 04 Paldi Circle
- `cam05` 05 Visat teen Rasta
- `cam06` 06 Timbavadi gate-Junagadh
- `cam07` 07 hero-showroom-gir-somnath
- `cam08` 08 majewadi-gate-junagadh
- `cam09` 09 new-bypass-near-by-circle-junagadh-2
- `cam10` 10 char-chowk-road-2-junagadh
- `cam11` 11 dolatpara-junagadh
- `cam12` 12 Tri Mandir Adalaj Tollnaka
- `cam13` 13 CN Vidhyalaya
- `cam14` 14 Delight RLVD
- `cam15` 15 Suvidha park
- `cam16` 16 Visat P2
- `cam17` 17 Rajkot Bus Port CCTV
- `cam18` 18 Rajkot CCTV
- `cam19` 19 KHAPARIA GRAM PANCHAYAT , TALUKA GANDEVI, DISTRICT NAVSARI
- `cam20` 20 Mohanpura
- `cam21` 23 Patan Dethali Char Rasta
- `cam22` 28 BK Mervada tran Rasta
- `cam23` 30 kheram
- `cam24` 33 dehgam
- `cam25` 34 dhanori
- `cam26` 35 TANKAL
- `cam27` 36 bilimora
- `cam28` 37 bilimora
- `cam29` 38 bilimora
- `cam30` Gandhidham Rambaugh p2
