# Onboard failures

Client: PRAHARI/OpenCV-TCP
Host tried: live.corp8.cloud
UTC: 2026-09-01T05:26:41Z
URL: https://live.corp8.cloud/api/ingest
HTTP: 502
Error: <!DOCTYPE html>
<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en-US"> <![endif]-->
<!--[if IE 7]>    <html class="no-js ie7 oldie" lang="en-US"> <![endif]-->
<!--[if IE 8]>    <html class="no-js ie8 oldie" lang="en-US"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en-US"> <!--<![endif]-->
<head>

<title>corp8.cloud | 502: Bad gateway</title>
<meta charset="UTF-8" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="X-UA-Compatible" c

Do not report cameras as down until /api/ingest returns live:true. 502 means the gateway is up but the ingest process is not. Retry W01; do not email SCRB on 502 alone.

| camera_id | url | UTC | error |
|---|---|---|---|
| (catalogue unreachable) | https://live.corp8.cloud/api/ingest | 2026-09-01T05:26:41Z | HTTP 502: gateway 502 or timeout |
