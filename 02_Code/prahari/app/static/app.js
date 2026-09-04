const $ = (id) => document.getElementById(id);
let me = null;
let map, trackMap, trackLayer;
const tiles = new Map();
let ws;
let camFilter = "";

function esc(s) {
  return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

async function api(path, opts = {}) {
  const headers = Object.assign({}, opts.headers || {});
  if (opts.json) {
    headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(opts.json);
  }
  const res = await fetch(path, Object.assign({ credentials: "include" }, opts, { headers }));
  return res;
}

function showApp() {
  $("login-card").classList.add("hidden");
  $("app").classList.remove("hidden");
  tickClock();
}

async function login() {
  $("login-err").textContent = "";
  const res = await api("/api/login", { method: "POST", json: { username: $("user").value, password: $("pass").value } });
  if (!res.ok) {
    $("login-err").textContent = "Login failed";
    return;
  }
  me = await res.json();
  showApp();
  await boot();
}

async function boot() {
  await refreshHealth();
  initMap();
  await loadCameras();
  await loadTrack();
  await loadAlerts();
  await loadWatchlist();
  await loadGaps();
  connectWs();
  setInterval(refreshHealth, 8000);
  setInterval(loadAlerts, 5000);
  setInterval(tickClock, 1000);
}

function tickClock() {
  if (!$("clock")) return;
  $("clock").textContent = new Date().toLocaleTimeString("en-IN", { hour12: false, timeZone: "Asia/Kolkata" }) + " IST";
}

async function refreshHealth() {
  const res = await fetch("/api/health");
  const data = await res.json();
  const host = data.sentinel_host_configured ? "Sentinel host set" : "sample cameras";
  if ($("health-line")) {
    $("health-line").innerHTML =
      "<span>" + esc(data.status) + "</span>" +
      "<span>" + data.cameras + " cameras</span>" +
      "<span>" + data.detections + " detections</span>" +
      "<span>WS " + (ws && ws.readyState === 1 ? "connected" : "polling") + "</span>" +
      "<span>" + esc(host) + "</span>";
  }
  if ($("footer-health")) {
    $("footer-health").textContent = data.cameras + " cameras · " + data.detections + " detections · WS " + (ws && ws.readyState === 1 ? "connected" : "polling");
  }
  if ($("banner") && data.sentinel_host_configured) {
    $("banner").textContent = "sync from cameras.json. Live catalogue cameras have no coordinates.";
  }
}

function color(health) {
  if (health === "live") return "#3f8f5b";
  if (health === "degraded") return "#c4a35a";
  if (health === "offline") return "#8a4038";
  return "#c5c2a8";
}

function initMap() {
  if (map) return;
  map = L.map("map").setView([22.5, 72.5], 7);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18 }).addTo(map);
  trackMap = L.map("track-map").setView([22.5, 72.5], 7);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18 }).addTo(trackMap);
}

async function loadCameras(department) {
  if (department !== undefined) camFilter = department;
  const q = camFilter ? "?department=" + encodeURIComponent(camFilter) : "";
  const res = await api("/api/cameras" + q);
  if (!res.ok) return;
  const rows = await res.json();
  if (map._markers) map._markers.forEach((m) => map.removeLayer(m));
  map._markers = [];
  rows.forEach((c) => {
    if (c.lat === 0 && c.lon === 0) return;
    const m = L.circleMarker([c.lat, c.lon], { radius: 8, color: color(c.health), fillColor: color(c.health), fillOpacity: 0.85 });
    m.bindPopup(
      "<strong class='id'>" + esc(c.camera_id) + "</strong><br>" + esc(c.department) + " · " + esc(c.location) +
      "<br>" + esc(c.ownership) + " · " + esc(c.codec) +
      "<br><button data-open='" + esc(c.camera_id) + "'>Open</button>"
    );
    m.addTo(map);
    map._markers.push(m);
  });
  map.on("popupopen", (ev) => {
    const btn = ev.popup._contentNode.querySelector("[data-open]");
    if (btn) btn.onclick = () => openTile(btn.getAttribute("data-open"));
  });
  const table = $("cam-table");
  table.innerHTML = "<caption>Live catalogue cameras have no coordinates. Open them from this table.</caption>" +
    "<thead><tr><th>id</th><th>dept</th><th>location</th><th>health</th><th>codec</th><th></th></tr></thead><tbody>" +
    rows.map((c) => "<tr><td class='id'>" + esc(c.camera_id) + "</td><td>" + esc(c.department) + "</td><td>" + esc(c.location) +
      "</td><td><span class='dot " + esc(c.health) + "'></span>" + esc(c.health) + "</td><td>" + esc(c.codec) +
      "</td><td><button data-open='" + esc(c.camera_id) + "'>Open</button></td></tr>").join("") +
    "</tbody>";
  table.onclick = (e) => {
    const btn = e.target.getAttribute && e.target.getAttribute("data-open");
    if (btn) openTile(btn);
  };
  const depts = [...new Set(rows.map((c) => c.department))];
  $("filters").innerHTML = ["All"].concat(depts).map((d) => {
    const on = (d === "All" && !camFilter) || d === camFilter ? " on" : "";
    return "<span class='chip" + on + "' data-d='" + esc(d) + "'>" + esc(d) + "</span>";
  }).join("");
  $("filters").onclick = (e) => {
    const d = e.target.getAttribute("data-d");
    if (d) loadCameras(d === "All" ? "" : d);
  };
}

async function openTile(cameraId) {
  $("tile-err").textContent = "";
  const camRes = await api("/api/cameras/" + encodeURIComponent(cameraId));
  const cam = await camRes.json();
  if (cam.playback && cam.playback.kind === "unavailable") {
    $("tile-empty").textContent = cam.playback.reason || "Drop own_feed.mp4 into 03_Data/recordings";
    return;
  }
  const sess = await api("/api/sessions", { method: "POST", json: { camera_id: cameraId } });
  if (sess.status === 429) {
    $("tile-err").textContent = "Fifth live session rejected. Close a tile first.";
    return;
  }
  const token = cam.playback.token;
  const url = "/api/stream/" + encodeURIComponent(cameraId) + "?token=" + encodeURIComponent(token);
  if (tiles.has(cameraId)) return;
  const wrap = document.createElement("div");
  wrap.className = "tile";
  wrap.innerHTML = "<p>" + esc(cameraId) + " <button data-x>Close</button></p><video controls playsinline></video>";
  const video = wrap.querySelector("video");
  if (cam.playback && cam.playback.kind === "hls" && window.Hls && window.Hls.isSupported()) {
    const hls = new window.Hls({ enableWorker: true, startPosition: -1 });
    hls.loadSource(url);
    hls.attachMedia(video);
    wrap._hls = hls;
  } else {
    video.src = url;
  }
  wrap.querySelector("[data-x]").onclick = async () => {
    if (wrap._hls) wrap._hls.destroy();
    await api("/api/sessions/" + encodeURIComponent(cameraId), { method: "DELETE" });
    wrap.remove();
    tiles.delete(cameraId);
  };
  $("wall").appendChild(wrap);
  tiles.set(cameraId, wrap);
  $("tile-empty").textContent = "";
}

async function loadTrack(plate) {
  plate = plate || $("plate-search").value || "GJ01AB1234";
  const res = await api("/api/track/" + encodeURIComponent(plate));
  if (!res.ok) return;
  const data = await res.json();
  $("csv-link").href = "/api/track/" + encodeURIComponent(plate) + "/report.csv";
  $("track-meta").textContent = data.count + " points · " + (data.category || "") +
    (data.flags.length ? " · flags: " + data.flags.map((f) => f.note).join("; ") : "");
  if (trackLayer) trackMap.removeLayer(trackLayer);
  const latlngs = data.points.filter((p) => p.lat && p.lon).map((p) => [p.lat, p.lon]);
  trackLayer = L.layerGroup();
  if (latlngs.length) {
    L.polyline(latlngs, { color: "#a38b4d" }).addTo(trackLayer);
    latlngs.forEach((ll, i) => L.marker(ll).bindPopup((i + 1) + ". " + data.points[i].location).addTo(trackLayer));
    trackMap.fitBounds(latlngs);
  }
  trackLayer.addTo(trackMap);
  $("track-table").innerHTML = "<thead><tr><th>#</th><th>ts</th><th>camera</th><th>location</th></tr></thead><tbody>" +
    data.points.map((p, i) => "<tr><td>" + (i + 1) + "</td><td>" + esc(p.ts) + "</td><td class='id'>" + esc(p.camera_id) + "</td><td>" + esc(p.location) + "</td></tr>").join("") +
    "</tbody>";
}

function ageLabel(ts) {
  if (!ts) return "";
  const t = Date.parse(ts);
  if (!t) return "";
  const s = Math.max(0, (Date.now() - t) / 1000);
  if (s < 60) return Math.round(s) + "s";
  if (s < 3600) return Math.round(s / 60) + "m";
  return Math.round(s / 3600) + "h";
}

async function loadAlerts() {
  const openRes = await api("/api/alerts?status=open");
  const pendingRes = await api("/api/alerts?status=pending_review");
  if (!openRes.ok) return;
  const rows = await openRes.json();
  if (pendingRes.ok) rows.push(...await pendingRes.json());
  const rank = { CRITICAL: 0, HIGH: 1, LOW: 2 };
  rows.sort((a, b) => (rank[a.priority] || 9) - (rank[b.priority] || 9));
  $("alert-empty").style.display = rows.length ? "none" : "block";
  $("alert-list").innerHTML = "<table class='alert-table'><thead><tr><th>PRI</th><th>entity</th><th>camera</th><th>age</th><th>count</th><th></th></tr></thead><tbody>" +
    rows.map((a) => {
      let title = a.plate;
      if (a.entity_type === "person") title = a.entity_id || a.plate || "person";
      if (a.entity_type === "intrusion" || a.category === "INTRUSION") title = "INTRUSION @ " + a.camera_id;
      const review = a.status === "pending_review" ? " pending_review" : "";
      return "<tr class='alert-row " + esc(a.priority) + "'><td class='pri'>" + esc(a.priority) + review +
        "</td><td>" + esc(title) + "</td><td class='id'>" + esc(a.camera_id) + "</td><td>" + ageLabel(a.ts) +
        "</td><td>×" + esc(a.counter) + "</td><td><button data-ack='" + esc(a.alert_id) + "'>Ack</button></td></tr>";
    }).join("") + "</tbody></table>";
  $("alert-list").onclick = async (e) => {
    const id = e.target.getAttribute("data-ack");
    if (!id) return;
    await api("/api/alerts/" + id + "/ack", { method: "POST" });
    loadAlerts();
  };
}

function connectWs() {
  try {
    ws = new WebSocket((location.protocol === "https:" ? "wss://" : "ws://") + location.host + "/ws/alerts");
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.type === "alert") loadAlerts();
    };
  } catch (e) {
    ws = null;
  }
}

async function loadWatchlist() {
  const res = await api("/api/watchlist");
  if (!res.ok) return;
  const rows = await res.json();
  $("wl-table").innerHTML = "<thead><tr><th>id</th><th>type</th><th>plate</th><th>name</th><th>gallery</th><th>category</th><th>priority</th></tr></thead><tbody>" +
    rows.map((w) => "<tr><td class='id'>" + esc(w.source_case_id) + "</td><td>" + esc(w.entity_type || "") + "</td><td class='id'>" + esc(w.plate || "") +
      "</td><td>" + esc(w.name || "") + "</td><td class='id'>" + esc(w.gallery_id || "") + "</td><td>" + esc(w.category) + "</td><td>" + esc(w.priority) + "</td></tr>").join("") +
    "</tbody>";
}

async function loadGaps() {
  const res = await api("/api/gap-report");
  if (!res.ok) return;
  $("gap-out").textContent = JSON.stringify(await res.json(), null, 2);
  const det = await api("/api/detections");
  if (det.ok && $("entity-counts")) {
    const rows = await det.json();
    const counts = {};
    rows.forEach((r) => {
      const k = r.entity_type || "vehicle";
      counts[k] = (counts[k] || 0) + 1;
    });
    const body = Object.keys(counts).map((k) => "<tr><td>" + esc(k) + "</td><td>" + counts[k] + "</td></tr>").join("");
    $("entity-counts").innerHTML = "<table><thead><tr><th>entity_type</th><th>n</th></tr></thead><tbody>" + body + "</tbody></table>";
  }
}

function renderResult(el, payload) {
  if (!el) return;
  const events = payload.events || (payload.event ? [payload.event] : []);
  if (!events.length) {
    const note = payload.inserted === false ? "No plate. Use Confirm plate if the still is readable." : "No events.";
    el.innerHTML = "<p>" + note + "</p><details><summary>raw</summary><pre>" + esc(JSON.stringify(payload, null, 2)) + "</pre></details>";
    return;
  }
  const rows = events.map((e) => {
    const src = e.source === "operator_confirm" ? "Operator confirm" : (e.source || "");
    const ident = e.plate || e.face_id || e.object_class || e.entity_id || "";
    return "<tr><td>" + esc(e.entity_type || "") + "</td><td class='id'>" + esc(ident) + "</td><td>" + esc(src) + "</td><td>" + esc(e.confidence ?? "") + "</td></tr>";
  }).join("");
  el.innerHTML = "<table><thead><tr><th>type</th><th>id</th><th>source</th><th>conf</th></tr></thead><tbody>" +
    rows + "</tbody></table><details><summary>raw</summary><pre>" + esc(JSON.stringify(payload, null, 2)) + "</pre></details>";
}

document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => {
      b.classList.remove("on");
      b.setAttribute("aria-selected", "false");
    });
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("on"));
    btn.classList.add("on");
    btn.setAttribute("aria-selected", "true");
    $("panel-" + btn.dataset.tab).classList.add("on");
    if (btn.dataset.tab === "operations" && map) setTimeout(() => map.invalidateSize(), 100);
    if (btn.dataset.tab === "track" && trackMap) setTimeout(() => trackMap.invalidateSize(), 100);
  });
});

$("login-btn").onclick = login;
$("track-form").onsubmit = (e) => { e.preventDefault(); loadTrack($("plate-search").value); };
if ($("predict-btn")) {
  $("predict-btn").onclick = async () => {
    const plate = $("plate-search").value || "GJ01AB1234";
    const res = await api("/api/predict/" + encodeURIComponent(plate));
    $("predict-out").textContent = JSON.stringify(await res.json(), null, 2);
  };
}
$("onboard-form").onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const body = Object.fromEntries(fd.entries());
  body.consent = fd.get("consent") === "on";
  body.lat = parseFloat(body.lat); body.lon = parseFloat(body.lon);
  await api("/api/cameras", { method: "POST", json: body });
  loadCameras();
};
$("csv-file").onchange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const fd = new FormData();
  fd.append("file", file);
  await api("/api/cameras/import", { method: "POST", body: fd });
  loadCameras();
};
$("anpr-file").onchange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const fd = new FormData();
  fd.append("file", file);
  fd.append("camera_id", $("anpr-cam").value);
  const res = await api("/api/ingest/frame", { method: "POST", body: fd });
  renderResult($("anpr-out"), await res.json());
  loadAlerts();
};
$("analyse-file").onchange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const fd = new FormData();
  fd.append("file", file);
  fd.append("camera_id", $("analyse-cam").value);
  fd.append("engines", $("analyse-cam").value.indexOf("cam") === 0 ? "anpr,objects" : "anpr,objects,faces");
  const res = await api("/api/ingest/analyse", { method: "POST", body: fd });
  renderResult($("analyse-out"), await res.json());
  loadAlerts();
  loadGaps();
};
$("confirm-form").onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  await api("/api/ingest/confirm", { method: "POST", json: { camera_id: fd.get("camera_id"), plate: fd.get("plate") } });
  loadAlerts();
  loadTrack();
};
$("confirm-face-form").onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  await api("/api/ingest/confirm-face", { method: "POST", json: { camera_id: fd.get("camera_id"), gallery_id: fd.get("gallery_id") } });
  loadAlerts();
};
$("wl-form").onsubmit = async (e) => {
  e.preventDefault();
  const fd = new FormData(e.target);
  await api("/api/watchlist", { method: "POST", json: Object.fromEntries(fd.entries()) });
  loadWatchlist();
};
if ($("enroll-person-form")) {
  $("enroll-person-form").onsubmit = async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const res = await api("/api/faces/enroll", { method: "POST", body: fd });
    renderResult($("enroll-out"), await res.json());
    loadWatchlist();
  };
}

document.addEventListener("keydown", (e) => {
  if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
    e.preventDefault();
    $("plate-search").focus();
  }
});

api("/api/me").then((r) => {
  if (r.ok) { r.json().then((u) => { me = u; showApp(); boot(); }); }
});
