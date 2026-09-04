const $ = (id) => document.getElementById(id);
let me = null;
let map, trackMap, trackLayer;
const tiles = new Map();
let ws;

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
}

async function refreshHealth() {
  const res = await fetch("/api/health");
  const data = await res.json();
  const host = data.sentinel_host_configured ? "Sentinel host set" : "SENTINEL_HOST not configured; showing sample cameras";
  $("health-line").innerHTML = "<strong>" + data.status + "</strong><br>" +
    data.cameras + " cameras · " + data.detections + " detections · " + data.watchlist + " watchlist<br>" + host;
  if ($("footer-health")) {
    $("footer-health").textContent = data.cameras + " cameras · " + data.detections + " detections · WS " + (ws && ws.readyState === 1 ? "connected" : "polling");
  }
  if ($("banner") && data.sentinel_host_configured) {
    $("banner").textContent = data.cameras + " cameras · Sentinel host set · sync from cameras.json. Live catalogue cameras have no coordinates.";
  }
}

function color(health) {
  if (health === "live") return "#3dd68c";
  if (health === "degraded") return "#e0b44a";
  if (health === "offline") return "#e85d5d";
  return "#9aa8bd";
}

function initMap() {
  if (map) return;
  map = L.map("map").setView([22.5, 72.5], 7);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18 }).addTo(map);
  trackMap = L.map("track-map").setView([22.5, 72.5], 7);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 18 }).addTo(trackMap);
}

async function loadCameras(department) {
  const q = department ? "?department=" + encodeURIComponent(department) : "";
  const res = await api("/api/cameras" + q);
  if (!res.ok) return;
  const rows = await res.json();
  if (map._markers) map._markers.forEach((m) => map.removeLayer(m));
  map._markers = [];
  rows.forEach((c) => {
    if (c.lat === 0 && c.lon === 0) return;
    const m = L.circleMarker([c.lat, c.lon], { radius: 8, color: color(c.health), fillColor: color(c.health), fillOpacity: 0.85 });
    m.bindPopup(
      "<strong>" + c.camera_id + "</strong><br>" + c.department + " · " + c.location +
      "<br>" + c.ownership + " · " + c.codec +
      "<br><button data-open='" + c.camera_id + "'>Open tile</button>"
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
    "<tr><th>id</th><th>dept</th><th>location</th><th>health</th><th>codec</th><th></th></tr>" +
    rows.map((c) => "<tr><td>" + c.camera_id + "</td><td>" + c.department + "</td><td>" + c.location + "</td><td>" + c.health + "</td><td>" + c.codec + "</td><td><button data-open='" + c.camera_id + "'>Open tile</button></td></tr>").join("");
  table.onclick = (e) => {
    const btn = e.target.getAttribute && e.target.getAttribute("data-open");
    if (btn) openTile(btn);
  };
  const depts = [...new Set(rows.map((c) => c.department))];
  $("filters").innerHTML = ["All"].concat(depts).map((d) => "<span class='chip' data-d='" + d + "'>" + d + "</span>").join("");
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
  wrap.innerHTML = "<p>" + cameraId + " <button data-x>close</button></p><video controls playsinline></video>";
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
    L.polyline(latlngs, { color: "#d4a017" }).addTo(trackLayer);
    latlngs.forEach((ll, i) => L.marker(ll).bindPopup((i + 1) + ". " + data.points[i].location).addTo(trackLayer));
    trackMap.fitBounds(latlngs);
  }
  trackLayer.addTo(trackMap);
  $("track-table").innerHTML = "<tr><th>#</th><th>ts</th><th>camera</th><th>location</th></tr>" +
    data.points.map((p, i) => "<tr><td>" + (i + 1) + "</td><td>" + p.ts + "</td><td>" + p.camera_id + "</td><td>" + p.location + "</td></tr>").join("");
}

async function loadAlerts() {
  const res = await api("/api/alerts?status=open");
  if (!res.ok) return;
  const rows = await res.json();
  $("alert-empty").style.display = rows.length ? "none" : "block";
  $("alert-list").innerHTML = rows.map((a) => {
    let title = a.plate;
    if (a.entity_type === "person") title = a.entity_id || a.plate || "person";
    if (a.entity_type === "intrusion" || a.category === "INTRUSION") title = "INTRUSION @ " + a.camera_id;
    return "<div class='alert " + a.priority + "'><strong>" + a.priority + "</strong> " + title +
      " @ " + a.camera_id + " ×" + a.counter +
      " <button data-ack='" + a.alert_id + "'>Ack</button></div>";
  }).join("");
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
  $("wl-table").innerHTML = "<tr><th>id</th><th>type</th><th>plate</th><th>name</th><th>gallery</th><th>category</th><th>priority</th></tr>" +
    rows.map((w) => "<tr><td>" + w.source_case_id + "</td><td>" + (w.entity_type || "") + "</td><td>" + (w.plate || "") +
      "</td><td>" + (w.name || "") + "</td><td>" + (w.gallery_id || "") + "</td><td>" + w.category + "</td><td>" + w.priority + "</td></tr>").join("");
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
    $("entity-counts").textContent = "Detections by entity_type: " + JSON.stringify(counts);
  }
}

document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("on"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("on"));
    btn.classList.add("on");
    $("panel-" + btn.dataset.tab).classList.add("on");
    if (btn.dataset.tab === "operations" && map) setTimeout(() => map.invalidateSize(), 100);
    if (btn.dataset.tab === "track" && trackMap) setTimeout(() => trackMap.invalidateSize(), 100);
  });
});

$("login-btn").onclick = login;
$("track-form").onsubmit = (e) => { e.preventDefault(); loadTrack($("plate-search").value); };
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
  $("anpr-out").textContent = JSON.stringify(await res.json(), null, 2);
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
  $("analyse-out").textContent = JSON.stringify(await res.json(), null, 2);
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

document.addEventListener("keydown", (e) => {
  if (e.key === "/" && document.activeElement.tagName !== "INPUT") {
    e.preventDefault();
    $("plate-search").focus();
  }
});

api("/api/me").then((r) => {
  if (r.ok) { r.json().then((u) => { me = u; showApp(); boot(); }); }
});
