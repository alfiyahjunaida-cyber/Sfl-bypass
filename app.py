"""
Bukalink - SFL Bypass Web (Flask) untuk Vercel
Deploy : upload app.py + requirements.txt ke GitHub, lalu import di vercel.com
"""

import time
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, render_template_string, request

API_URL = "https://safebypass.vercel.app/api/bypass"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
HEADERS = {
    "Content-Type": "application/json",
    "accept": "application/json",
    "user-agent": USER_AGENT,
    "origin": "https://safebypass.vercel.app",
    "referer": "https://safebypass.vercel.app/",
}

app = Flask(__name__)

INDEX_HTML = r"""{% raw %}<!DOCTYPE html>
<html lang="id" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="#0c1029">
  <title>Bukalink - SFL Bypass</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config = { darkMode: 'class' }</script>
  <style>
    :root {
      --bg: #0c1029;
      --surface: #151b3d;
      --surface-2: #1c2450;
      --line: #2d3670;
      --text: #eceeff;
      --muted: #9aa3d8;
      --amber: #ffc857;
      --amber-ink: #2a1d00;
      --rose: #ff8595;
    }
    html { background: var(--bg); }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
      min-height: 100vh;
      padding-bottom: env(safe-area-inset-bottom, 0px);
    }
    .display { font-family: 'Bricolage Grotesque', 'DM Sans', system-ui, sans-serif; }
    .mono { font-family: 'JetBrains Mono', ui-monospace, 'SFMono-Regular', Menlo, monospace; }
    :focus-visible { outline: 2px solid var(--amber); outline-offset: 2px; }
    .sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }

    .wrap { max-width: 34rem; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }

    /* Wordmark */
    .brand { display: flex; align-items: center; gap: .6rem; font-weight: 700; font-size: 1.15rem; letter-spacing: -.01em; }
    .brand-mark { width: 2rem; height: 2rem; border-radius: .6rem; background: var(--amber); color: var(--amber-ink); display: grid; place-items: center; }

    /* Hero */
    .hero h1 { font-size: clamp(2.35rem, 10vw, 3.6rem); line-height: 1.02; font-weight: 800; letter-spacing: -.035em; margin-top: 2.5rem; }
    .hero p { color: var(--muted); margin-top: 1rem; font-size: 1.02rem; line-height: 1.55; max-width: 30rem; }

    /* Input bar */
    .bar { margin-top: 1.75rem; display: flex; align-items: center; gap: .5rem; background: var(--surface); border: 1.5px solid var(--line); border-radius: 1.15rem; padding: .35rem .35rem .35rem 1rem; transition: border-color .15s; }
    .bar:focus-within { border-color: var(--amber); }
    .bar input { flex: 1; min-width: 0; background: transparent; border: 0; color: var(--text); font-size: 1rem; padding: .8rem 0; outline: none; }
    .bar input::placeholder { color: #6871ad; }
    .btn-ghost { flex: none; background: var(--surface-2); color: var(--text); border: 0; border-radius: .8rem; padding: .65rem .95rem; font-size: .9rem; font-weight: 600; cursor: pointer; }
    .btn-ghost:hover { background: #262f63; }
    .go { width: 100%; margin-top: .75rem; background: var(--amber); color: var(--amber-ink); border: 0; border-radius: 1rem; padding: 1rem; font-size: 1.05rem; font-weight: 700; cursor: pointer; transition: transform .1s, filter .15s; }
    .go:hover { filter: brightness(1.06); }
    .go:active { transform: scale(.985); }
    .go:disabled { opacity: .6; cursor: wait; }

    /* Route */
    .route-wrap { margin-top: 2.25rem; }
    .upper { position: relative; }
    .stop { position: relative; padding-left: 2.25rem; }
    .dot { position: absolute; left: 0; top: 2px; width: 20px; height: 20px; border-radius: 50%; border: 2px solid var(--line); background: var(--bg); z-index: 1; transition: background .3s, border-color .3s; }
    .dot.on { background: var(--amber); border-color: var(--amber); }
    .dot.bad { border-color: var(--rose); }
    .lbl { color: var(--muted); font-size: .85rem; font-weight: 500; }
    .url { margin-top: .25rem; font-size: .85rem; line-height: 1.5; word-break: break-all; color: #c9cffc; }
    .url.faint { color: #59629b; }
    .rail { position: absolute; left: 9px; top: 24px; bottom: -14px; width: 2px; background: repeating-linear-gradient(to bottom, var(--line) 0 6px, transparent 6px 12px); }
    .rail.flow { background: repeating-linear-gradient(to bottom, var(--amber) 0 6px, transparent 6px 12px); background-size: 2px 12px; animation: flow .6s linear infinite; }
    .rail.done { background: var(--amber); transform-origin: top; animation: fill .7s cubic-bezier(.4,0,.2,1); }
    .rail.fail { background: repeating-linear-gradient(to bottom, var(--rose) 0 4px, transparent 4px 12px); }
    @keyframes flow { to { background-position: 0 12px; } }
    @keyframes fill { from { transform: scaleY(0); } to { transform: scaleY(1); } }

    .hop { padding: .9rem 0 1.3rem 2.25rem; display: flex; flex-wrap: wrap; gap: .4rem; min-height: 3.2rem; align-items: center; }
    .chip { background: var(--surface); border: 1px solid var(--line); color: #c9cffc; border-radius: 999px; padding: .2rem .7rem; font-size: .8rem; font-weight: 500; }
    .hint { color: #59629b; font-size: .85rem; }

    .dest { background: var(--surface); border: 1.5px solid var(--line); border-radius: 1.1rem; padding: 1rem 1rem 1rem 2.25rem; margin-left: 0; position: relative; transition: border-color .4s; }
    .dest .dot { top: 1.05rem; left: -10px; }
    .dest.ok { border-color: var(--amber); }
    .dest.err { border-color: #7a3a55; }
    .dest-title { display: flex; align-items: center; gap: .5rem; font-weight: 700; font-size: 1rem; }
    .dest .url { font-size: .9rem; color: var(--text); }
    .dest .err-msg { margin-top: .35rem; color: #ffc0c8; line-height: 1.5; font-size: .93rem; }
    .dest .err-tip { margin-top: .3rem; color: var(--muted); font-size: .85rem; }
    .actions { display: flex; gap: .5rem; margin-top: .9rem; }
    .actions a, .actions button { flex: 1; text-align: center; text-decoration: none; border-radius: .8rem; padding: .7rem .5rem; font-size: .92rem; font-weight: 600; cursor: pointer; border: 0; }
    .a-main { background: var(--amber); color: var(--amber-ink); }
    .a-sub { background: var(--surface-2); color: var(--text); }
    .skel { height: .8rem; border-radius: 6px; background: var(--surface-2); margin-top: .6rem; width: 80%; opacity: .8; animation: pulse 1s ease-in-out infinite alternate; }
    @keyframes pulse { to { opacity: .35; } }

    /* Kunci terbuka: satu momen animasi */
    .lock .shackle { transform-origin: 16px 10px; }
    .dest.ok .lock .shackle { animation: unlock .6s .2s cubic-bezier(.3,1.4,.5,1) both; }
    @keyframes unlock { from { transform: translateY(0) rotate(0); } to { transform: translateY(-3px) rotate(-28deg) translateX(2px); } }

    /* History */
    .history { margin-top: 2.5rem; }
    .history-head { display: flex; justify-content: space-between; align-items: baseline; }
    .history-head h2 { font-size: 1.05rem; font-weight: 700; }
    .link-btn { background: none; border: 0; color: var(--muted); font-size: .85rem; cursor: pointer; text-decoration: underline; padding: .25rem; }
    .h-item { display: block; width: 100%; text-align: left; background: var(--surface); border: 1px solid var(--line); border-radius: .9rem; padding: .7rem .9rem; margin-top: .5rem; cursor: pointer; color: var(--text); }
    .h-item:hover { border-color: #46529c; }
    .h-item .d { font-size: .85rem; word-break: break-all; }
    .h-item .s { color: var(--muted); font-size: .78rem; margin-top: .15rem; word-break: break-all; }

    .foot { margin-top: 2.5rem; color: #59629b; font-size: .8rem; }

    .toast { position: fixed; left: 50%; bottom: calc(1.25rem + env(safe-area-inset-bottom, 0px)); transform: translate(-50%, 1rem); background: var(--text); color: var(--bg); padding: .6rem 1.1rem; border-radius: 999px; font-weight: 600; font-size: .9rem; opacity: 0; pointer-events: none; transition: opacity .2s, transform .2s; z-index: 50; }
    .toast.show { opacity: 1; transform: translate(-50%, 0); }

    @media (prefers-reduced-motion: reduce) {
      .rail.flow, .rail.done, .skel, .dest.ok .lock .shackle { animation: none; }
      .dest.ok .lock .shackle { transform: translateY(-3px) rotate(-28deg) translateX(2px); }
      .toast { transition: none; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <header class="brand">
      <span class="brand-mark" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></svg>
      </span>
      <span class="display">Bukalink</span>
    </header>

    <section class="hero">
      <h1 class="display">Link pendek masuk, tujuan asli keluar.</h1>
      <p>Tempel link sfl.gl dan lihat ke mana link itu sebenarnya mengarah.</p>
    </section>

    <form id="form" autocomplete="off" novalidate>
      <div class="bar">
        <label class="sr" for="url">Link sfl.gl</label>
        <input id="url" type="url" inputmode="url" autocapitalize="off" spellcheck="false" placeholder="https://sfl.gl/xxxx">
        <button type="button" id="paste" class="btn-ghost">Tempel</button>
      </div>
      <button type="submit" id="go" class="go">Bypass</button>
    </form>

    <section id="route" class="route-wrap" aria-live="polite"></section>

    <section id="history" class="history" hidden></section>

    <p class="foot">Memakai API safebypass.vercel.app</p>
  </div>

  <div id="toast" class="toast" role="status" aria-live="polite"></div>

  <script>
    const $ = (id) => document.getElementById(id);
    const input = $("url"), routeEl = $("route"), goBtn = $("go"), toastEl = $("toast"), histEl = $("history");
    const HKEY = "bukalink_riwayat";

    const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
    const isHttp = (u) => /^https?:\/\//i.test(u || "");

    const LOCK = '<svg class="lock" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2.5"/><path class="shackle" d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>';

    let toastTimer;
    function toast(msg) {
      toastEl.textContent = msg;
      toastEl.classList.add("show");
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toastEl.classList.remove("show"), 1800);
    }

    async function copyText(text) {
      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(text);
          return true;
        }
      } catch (e) {}
      try {
        const ta = document.createElement("textarea");
        ta.value = text;
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        const ok = document.execCommand("copy");
        document.body.removeChild(ta);
        return ok;
      } catch (e) {
        return false;
      }
    }

    /* ---------- Jalur (route) ---------- */
    function srcNode(src, dim) {
      return '<div class="stop"><span class="dot' + (dim ? ' on' : '') + '"></span>' +
        '<p class="lbl">Link pendek</p>' +
        (src ? '<p class="url mono">' + esc(src) + '</p>' : '<p class="url mono faint">https://sfl.gl/...</p>') +
        '</div>';
    }

    function renderIdle() {
      routeEl.innerHTML =
        '<div class="upper"><span class="rail"></span>' + srcNode("", false) +
        '<div class="hop"><span class="hint">Hasil bypass muncul di jalur ini.</span></div></div>' +
        '<div class="dest"><span class="dot"></span><div class="dest-title">' + LOCK + '<span>Tujuan akhir</span></div>' +
        '<p class="url mono faint">Belum ada hasil</p></div>';
    }

    function renderLoading(src) {
      routeEl.innerHTML =
        '<div class="upper"><span class="rail flow"></span>' + srcNode(src, true) +
        '<div class="hop"><span class="chip">Memproses...</span></div></div>' +
        '<div class="dest"><span class="dot"></span><div class="dest-title">' + LOCK + '<span>Membuka kunci</span></div>' +
        '<div class="skel"></div><div class="skel" style="width:55%"></div></div>';
    }

    function renderSuccess(src, d) {
      const chips = [];
      if (d.steps != null) chips.push('<span class="chip">' + esc(d.steps) + ' langkah</span>');
      if (d.ms != null) chips.push('<span class="chip">' + esc(d.ms) + ' ms</span>');
      const safe = isHttp(d.url);
      routeEl.innerHTML =
        '<div class="upper"><span class="rail done"></span>' + srcNode(src, true) +
        '<div class="hop">' + (chips.join("") || '<span class="chip">Selesai</span>') + '</div></div>' +
        '<div class="dest ok"><span class="dot on"></span><div class="dest-title">' + LOCK + '<span>Tujuan akhir</span></div>' +
        '<p class="url mono">' + esc(d.url) + '</p>' +
        '<div class="actions">' +
        (safe ? '<a class="a-main" href="' + esc(d.url) + '" target="_blank" rel="noopener noreferrer">Buka link</a>' : '') +
        '<button type="button" class="a-sub" data-copy="' + esc(d.url) + '">Salin link</button>' +
        '</div></div>';
    }

    function renderError(msg, src) {
      routeEl.innerHTML =
        '<div class="upper"><span class="rail fail"></span>' + srcNode(src, false) +
        '<div class="hop"><span class="chip">Terhenti</span></div></div>' +
        '<div class="dest err"><span class="dot bad"></span><div class="dest-title">' + LOCK + '<span>Bypass gagal</span></div>' +
        '<p class="err-msg">' + esc(msg) + '</p>' +
        '<p class="err-tip">Periksa linknya, lalu coba bypass lagi.</p></div>';
    }

    /* ---------- Riwayat (disimpan di browser) ---------- */
    function loadHistory() {
      try { return JSON.parse(localStorage.getItem(HKEY) || "[]"); } catch (e) { return []; }
    }
    function saveHistory(list) {
      try { localStorage.setItem(HKEY, JSON.stringify(list)); } catch (e) {}
    }
    function addHistory(s, d) {
      const list = loadHistory().filter((x) => x.s !== s);
      list.unshift({ s, d });
      saveHistory(list.slice(0, 5));
      renderHistory();
    }
    function renderHistory() {
      const list = loadHistory();
      if (!list.length) { histEl.hidden = true; histEl.innerHTML = ""; return; }
      histEl.hidden = false;
      histEl.innerHTML =
        '<div class="history-head"><h2 class="display">Riwayat</h2><button type="button" class="link-btn" id="clear">Hapus riwayat</button></div>' +
        list.map((x) => '<button type="button" class="h-item" data-copy="' + esc(x.d) + '"><div class="d mono">' + esc(x.d) + '</div><div class="s mono">' + esc(x.s) + '</div></button>').join("");
    }

    /* ---------- Aksi ---------- */
    async function run() {
      const url = input.value.trim();
      if (!url) { renderError("Link belum diisi.", ""); input.focus(); return; }

      goBtn.disabled = true;
      goBtn.textContent = "Memproses...";
      renderLoading(url);

      try {
        const res = await fetch("/bypass", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url })
        });
        const d = await res.json();
        if (d.ok && d.url) {
          renderSuccess(url, d);
          addHistory(url, d.url);
          toast("Berhasil di-bypass");
        } else {
          renderError(d.message || "Bypass gagal", url);
        }
      } catch (e) {
        renderError("Tidak bisa terhubung ke server: " + e.message, url);
      } finally {
        goBtn.disabled = false;
        goBtn.textContent = "Bypass";
      }
    }

    $("form").addEventListener("submit", (e) => { e.preventDefault(); run(); });

    $("paste").addEventListener("click", async () => {
      try {
        const t = await navigator.clipboard.readText();
        if (t) { input.value = t.trim(); input.focus(); return; }
        toast("Clipboard kosong");
      } catch (e) {
        toast("Tempel manual: tekan lama di kolom");
        input.focus();
      }
    });

    document.addEventListener("click", async (e) => {
      const copyBtn = e.target.closest("[data-copy]");
      if (copyBtn) {
        const ok = await copyText(copyBtn.getAttribute("data-copy"));
        toast(ok ? "Link disalin" : "Gagal menyalin, salin manual");
        return;
      }
      if (e.target.id === "clear") {
        saveHistory([]);
        renderHistory();
        toast("Riwayat dihapus");
      }
    });

    renderIdle();
    renderHistory();
  </script>
</body>
</html>{% endraw %}"""


def is_valid_url(value):
    if not value or not isinstance(value, str):
        return False
    try:
        p = urlparse(value)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def result(ok, url=None, message=None, steps=None, ms=None, status=200):
    return jsonify({"ok": ok, "url": url, "message": message, "steps": steps, "ms": ms}), status


@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML)


@app.route("/bypass", methods=["POST"])
def bypass():
    data = request.get_json(silent=True) or {}
    url = str(data.get("url", "")).strip()

    if not is_valid_url(url):
        return result(False, message="Parameter 'url' tidak valid", status=400)

    start = time.time()
    try:
        resp = requests.post(
            API_URL,
            headers=HEADERS,
            json={"url": url, "apiKey": ""},
            timeout=30,
        )
    except requests.exceptions.Timeout:
        return result(False, message="Request ke API timeout", status=504)
    except requests.exceptions.RequestException as e:
        return result(False, message=f"Gagal menghubungi API: {e}", status=502)

    if not resp.ok:
        return result(
            False,
            message=f"Failed to bypass URL: {resp.status_code} {resp.reason}",
            status=502,
        )

    try:
        payload = resp.json()
    except ValueError:
        return result(False, message="Expected JSON response from bypass API", status=502)

    ok = bool(payload.get("ok"))
    steps = payload.get("steps")
    ms = payload.get("ms")
    if not isinstance(steps, int) or isinstance(steps, bool):
        steps = None
    if not isinstance(ms, (int, float)) or isinstance(ms, bool):
        ms = round((time.time() - start) * 1000)

    if ok:
        final_url = payload.get("url")
        if final_url:
            return result(True, url=final_url, steps=steps, ms=ms)
        inter = payload.get("intermediate")
        if payload.get("needsManual") and inter:
            return result(False, message=f"Perlu manual. Link perantara: {inter}", steps=steps, ms=ms)
        return result(False, message="API tidak mengembalikan link", steps=steps, ms=ms)

    return result(False, message=payload.get("message") or "Bypass gagal", steps=steps, ms=ms)
