/* The memoryless reader. One room per page; all its hops are already in the DOM (ol.hops, one li per
   hop, hop 0 = seed). This script only decides which two are visible: the hop before (context) and
   the hop (current). The hash is the hop: r/<room>.html#12. Rooms link to each other as pages. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var sections = Array.prototype.slice.call(document.querySelectorAll("main > section"));
  var state = { room: null, t: 0, prevT: -1, timer: null, raw: false, sound: false, audio: null };
  var PLAY_MS = 2500;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  // the hop from the hash: "#12", or the old one-page form "#room/12"
  function parseHash() {
    var h = location.hash.replace(/^#/, "");
    var parts = h.split("/"); var t = parseInt(parts[parts.length - 1] || "0", 10);
    return isNaN(t) ? 0 : t;
  }

  function setHash(t) {
    var h = t ? "#" + t : "";
    if (location.hash !== h) history.replaceState(null, "", location.pathname + location.search + h);
  }

  // the other pages, as the build linked them in the top bar
  function link(sel) { var a = $(".topbar " + sel); return a ? a.getAttribute("href") : null; }
  function homeHref() { return link(".home") || "../"; }
  function nextHref() { return link(".next-room") || homeHref(); }
  function prevHref() { return link(".prev-room") || homeHref(); }
  function go(href) { if (href) location.href = href; }

  function show(t) {
    stopPlay();
    var sec = sections[0];
    state.room = sec && sec.classList.contains("room") ? sec.id : null; state.t = t || 0; state.prevT = -1;
    if (state.room) { setHash(state.t); renderRoom(sec); }
  }

  function renderRoom(sec) {
    var n = parseInt(sec.getAttribute("data-n"), 10);
    var t = Math.max(0, Math.min(state.t, n)); state.t = t;
    var ct = $(".counter .t", sec); ct.textContent = t; ct.classList.remove("tick"); void ct.offsetWidth; ct.classList.add("tick");
    $(".btn.back", sec).disabled = t === 0;
    var nextBtn = $(".btn.next", sec);
    if (t >= n) { nextBtn.textContent = nextHref() !== homeHref() ? "next room →" : "index"; nextBtn.classList.add("to-room"); }
    else { nextBtn.textContent = "next"; nextBtn.classList.remove("to-room"); }
    var still = (t === state.prevT + 1);
    $all(".lane", sec).forEach(function (lane, li) {
      renderLane(lane, t, still);
      var h = $('ol.hops > li.hop[data-t="' + t + '"]', lane);
      if (h && state.prevT !== t) setTimeout(function () { tone(h); }, Math.min(li, 6) * 120);
    });
    var st = $(".counter .status", sec); var words = [];
    var lanes = $all(".lane", sec);
    lanes.forEach(function (lane) {
      var h = $('ol.hops > li.hop[data-t="' + t + '"]', lane); if (!h) return;
      var co = h.getAttribute("data-copy-of");
      var lab = lanes.length > 1 && $(".lane-label", lane) ? $(".lane-label", lane).textContent + ": " : "";
      if (co === null && h.getAttribute("data-same-text") === "1") {
        var fd = h.getAttribute("data-fields-differ");
        words.push(lab + (fd === "step" ? "same as hop " + (t - 1) + ", only the step counter moved" : fd ? "same " + (h.getAttribute("data-noun") || "verse") + " as hop " + (t - 1) + ", " + fd.replace(",", " and ") + " differ" : "same words as hop " + (t - 1)));
      }
      else if (co === null && h.getAttribute("data-text-copy-of") !== null) words.push(lab + "text same as hop " + h.getAttribute("data-text-copy-of"));
      if (co !== null) {
        var prev = $('ol.hops > li.hop[data-t="' + (t - 1) + '"]', lane);
        var pco = prev ? prev.getAttribute("data-copy-of") : null;
        var since = (pco !== null && pco === co) ? co : String(t - 1);
        words.push(lab + (parseInt(co, 10) === t - 1 || (pco !== null && pco === co) ? "unchanged since hop " + since : "same as hop " + co));
      }
    });
    if (lanes.length > 2) {
      var holding = 0, ended = 0;
      lanes.forEach(function (lane) {
        var n = parseInt(lane.getAttribute("data-n"), 10);
        if (t > n) { ended++; return; }
        var h = $('ol.hops > li.hop[data-t="' + t + '"]', lane);
        if (h && h.getAttribute("data-copy-of") !== null) holding++;
      });
      words = [];
      if (t > 0 && holding) words.push(holding + " of " + lanes.length + " lanes are copies of an earlier hop");
      if (ended) words.push(ended + " already stopped");
    }
    st.textContent = words.length ? words.join(" / ") : "";
    state.prevT = t;
    setHash(t);
  }

  function renderLane(lane, t, still) {
    var n = parseInt(lane.getAttribute("data-n"), 10);
    var hops = $all("ol.hops > li.hop", lane);
    var ctx = $(".slot.context", lane), cur = $(".slot.current", lane);
    var ended = $(".ended", lane);
    clearSlot(ctx); clearSlot(cur);
    ctx.hidden = (t === 0);
    $(".slot-label", cur).textContent = t === 0 ? "the seed" : "it wrote";
    if (t <= n) {
      if (ended) ended.hidden = true;
      if (t > 0) fillSlot(ctx, hops[t - 1]);
      fillSlot(cur, hops[t], still && hops[t].getAttribute("data-still") === "1");
    } else {
      ctx.hidden = true;
      if (ended) { ended.hidden = false; $(".ended-t", ended).textContent = t; }
      $(".slot-label", cur).textContent = n === 0 ? "the seed" : lane.getAttribute("data-held") === "1" ? "it holds" : "its last hop";
      fillSlot(cur, hops[n], true); $(".hop", cur).classList.add("held");
    }
    var cursor = $(".track .cursor", lane);
    var here = $('.track .bar[data-t="' + Math.min(t, n) + '"]', lane);
    if (cursor && here) { cursor.setAttribute("x", parseFloat(here.getAttribute("x")) - 1); }
    $all(".track .bar", lane).forEach(function (b) { b.classList.toggle("here", parseInt(b.getAttribute("data-t"), 10) === t); });
  }

  function clearSlot(slot) {
    $all(".hop", slot).forEach(function (h) { h.parentNode.removeChild(h); });
    slot.classList.remove("empty");
  }

  function fillSlot(slot, hop, still) {
    var c = hop.cloneNode(true);
    c.removeAttribute("id");
    if (still) c.classList.add("still");
    var asCtx = $(".text.as-context", c);
    if (asCtx) {
      if (slot.classList.contains("context")) { var main = $(".text:not(.as-context)", c); if (main) main.hidden = true; asCtx.hidden = false; }
      else { asCtx.parentNode.removeChild(asCtx); }
    }
    var d = $("details.raw", c); if (d) d.open = state.raw;
    slot.appendChild(c);
  }

  function activeRoom() { return state.room ? document.getElementById(state.room) : null; }

  function step(delta) {
    var sec = activeRoom(); if (!sec || !sec.classList.contains("room")) return;
    var n = parseInt(sec.getAttribute("data-n"), 10);
    var t = state.t + delta;
    if (t > n) { go(nextHref()); return; }
    if (t < 0) t = 0;
    state.t = t; renderRoom(sec);
    var top = $(".controls", sec).getBoundingClientRect().top + window.pageYOffset - 40;
    if (window.pageYOffset > top) window.scrollTo(0, top);
  }

  function goto(t) {
    var sec = activeRoom(); if (!sec) return;
    stopPlay(); state.t = t; renderRoom(sec);
  }

  function startPlay() {
    var sec = activeRoom(); if (!sec) return;
    stopPlay();
    $(".btn.play", sec).textContent = "pause"; $(".btn.play", sec).classList.add("on");
    state.timer = setInterval(function () {
      var n = parseInt(sec.getAttribute("data-n"), 10);
      if (state.t >= n) { stopPlay(); return; }
      state.t += 1; renderRoom(sec);
    }, PLAY_MS);
  }
  function stopPlay() {
    if (state.timer) { clearInterval(state.timer); state.timer = null; }
    $all(".btn.play").forEach(function (b) { b.textContent = "play"; b.classList.remove("on"); });
  }
  function togglePlay() { if (state.timer) stopPlay(); else startPlay(); }

  // sound: one tone per hop. Pitch from ncd to the seed (where the text is), loudness from ncd to the
  // previous hop (how much moved). A fixed point is the same quiet tick every hop.
  function ensureAudio() {
    if (state.audio) return state.audio;
    var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null;
    state.audio = new AC(); return state.audio;
  }
  function tone(hop) {
    if (!state.sound || !hop) return;
    var ac = ensureAudio(); if (!ac) return;
    var play = function () {
      var x0 = parseFloat(hop.getAttribute("data-ncd-x0")); var dp = parseFloat(hop.getAttribute("data-ncd-prev"));
      var seed = isNaN(x0);
      var f = seed ? 220 : 220 * Math.pow(2, 1.5 * Math.max(0, Math.min(1, x0)));          // 220 .. 620 Hz
      var moved = seed ? 0 : Math.max(0, Math.min(1, (dp - 0.03) / 0.8));                     // 0 for a copy, 1 for all new
      var gainV = 0.08 + 0.32 * moved;
      var dur = 0.35 + 0.9 * moved;
      var now = ac.currentTime;
      var g = ac.createGain(); g.gain.setValueAtTime(0.0001, now);
      g.gain.exponentialRampToValueAtTime(gainV, now + 0.015);
      g.gain.exponentialRampToValueAtTime(0.0001, now + dur);
      g.connect(ac.destination);
      [[1, 1, "sine"], [2, 0.35, "triangle"], [3, 0.12, "sine"]].forEach(function (h) {
        var o = ac.createOscillator(); o.type = h[2]; o.frequency.value = f * h[0];
        var og = ac.createGain(); og.gain.value = h[1]; o.connect(og); og.connect(g);
        o.start(now); o.stop(now + dur + 0.1);
      });
    };
    if (ac.state !== "running") { ac.resume().then(play, function () {}); } else { play(); }
  }
  function soundLabel() {
    var ac = state.audio;
    $all(".btn.sound-toggle").forEach(function (b) {
      b.classList.toggle("on", state.sound);
      b.textContent = !state.sound ? "sound" : (ac && ac.state === "running" ? "sound on" : "sound on (click again if silent)");
    });
  }
  function toggleSound() {
    state.sound = !state.sound;
    var ac = state.sound ? ensureAudio() : null;
    if (ac && ac.state !== "running") { ac.resume().then(soundLabel, soundLabel); }
    soundLabel();
    if (state.sound) { var sec = activeRoom(); if (sec) $all(".lane", sec).forEach(function (lane) { tone($('ol.hops > li.hop[data-t="' + state.t + '"]', lane)); }); }
    setTimeout(soundLabel, 400);
  }

  function toggleRaw() {
    state.raw = !state.raw;
    $all(".btn.raw-toggle").forEach(function (b) { b.classList.toggle("on", state.raw); });
    $all(".slot details.raw").forEach(function (d) { d.open = state.raw; });
  }

  // theme: follows the system unless toggled; remembered in localStorage when available
  function applyTheme(th) {
    if (th) document.documentElement.setAttribute("data-theme", th); else document.documentElement.removeAttribute("data-theme");
  }
  function currentTheme() {
    var th = document.documentElement.getAttribute("data-theme");
    if (th) return th;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  try { var saved = localStorage.getItem("loop-theme"); if (saved === "dark" || saved === "light") applyTheme(saved); } catch (err) {}
  var qs = location.search.replace(/^\?/, "");
  if (qs === "dark" || qs === "light") applyTheme(qs);
  function toggleTheme() {
    var next = currentTheme() === "dark" ? "light" : "dark";
    applyTheme(next);
    try { localStorage.setItem("loop-theme", next); } catch (err) {}
  }

  // wiring
  document.addEventListener("click", function (e) {
    var el = e.target;
    if (el.closest && el.closest(".theme-toggle")) { e.preventDefault(); toggleTheme(); return; }
    var sec = el.closest ? el.closest("section.room") : null;
    if (el.closest && el.closest(".btn.next")) { e.preventDefault(); step(1); return; }
    if (el.closest && el.closest(".btn.back")) { e.preventDefault(); step(-1); return; }
    if (el.closest && el.closest(".btn.play")) { e.preventDefault(); togglePlay(); return; }
    if (el.closest && el.closest(".btn.raw-toggle")) { e.preventDefault(); toggleRaw(); return; }
    if (el.closest && el.closest(".btn.sound-toggle")) { e.preventDefault(); toggleSound(); return; }
    var bar = el.closest ? el.closest(".track .bar") : null;
    if (bar) { e.preventDefault(); goto(parseInt(bar.getAttribute("data-t"), 10)); return; }
    var trk = el.closest ? el.closest("svg.track") : null;
    if (trk) { // click on the empty part of the track: nearest bar
      var r = trk.getBoundingClientRect(); var vb = trk.viewBox.baseVal;
      var sx = (e.clientX - r.left) / r.width * vb.width; var best = null, bd = 1e9;
      $all(".bar", trk).forEach(function (b) { var cx = parseFloat(b.getAttribute("x")) + parseFloat(b.getAttribute("width")) / 2; var d = Math.abs(cx - sx); if (d < bd) { bd = d; best = b; } });
      if (best) goto(parseInt(best.getAttribute("data-t"), 10)); return;
    }
    var ctx = el.closest ? el.closest(".slot.context") : null;
    if (ctx && !el.closest("summary")) { ctx.classList.toggle("open"); }
    var manyLane = el.closest(".room.many .lane");
    if (manyLane && !el.closest("summary, a, button, .track")) { manyLane.classList.toggle("open"); }
  });

  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var tag = (e.target && e.target.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA") return;
    if (!$(".topbar")) return;   // the front page has no reader
    if (e.key === "n") { go(nextHref()); return; }
    if (e.key === "b") { go(prevHref()); return; }
    if (e.key === "Escape") { go(homeHref()); return; }
    if (!state.room) return;
    if (e.key === "ArrowRight" || e.key === " " || e.key === "j") { e.preventDefault(); step(1); }
    else if (e.key === "ArrowLeft" || e.key === "k") { e.preventDefault(); step(-1); }
    else if (e.key === "p") { togglePlay(); }
    else if (e.key === "r") { toggleRaw(); }
    else if (e.key === "s") { toggleSound(); }
  });

  window.addEventListener("hashchange", function () {
    var t = parseHash();
    if (state.room && t !== state.t) goto(t);
  });

  show(parseHash());
})();
