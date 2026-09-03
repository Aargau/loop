/* The memoryless reader. All hops are already in the DOM (ol.hops, one li per hop, hop 0 = seed).
   This script only decides which two are visible: the hop before (context) and the hop (current). */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var sections = Array.prototype.slice.call(document.querySelectorAll("main > section"));
  var order = sections.map(function (s) { return s.id; });
  var state = { room: null, t: 0, prevT: -1, timer: null, raw: false, sound: false, audio: null };
  var PLAY_MS = 2500;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function parseHash() {
    var h = location.hash.replace(/^#/, "");
    if (!h) return { room: null, t: 0 };
    var parts = h.split("/");
    var id = parts[0]; var t = parseInt(parts[1] || "0", 10);
    if (!document.getElementById(id)) return { room: null, t: 0 };
    return { room: id, t: isNaN(t) ? 0 : t };
  }

  function setHash(room, t) {
    var h = room ? ("#" + room + (t ? "/" + t : "")) : "#";
    if (location.hash !== h) history.replaceState(null, "", h);
  }

  function roomTitle(sec) {
    var h2 = $("h2", sec); if (!h2) return sec.id;
    var num = $(".num", h2);
    var title = h2.textContent.replace(num ? num.textContent : "", "").trim();
    return (num ? num.textContent + " " : "") + title;
  }

  function show(room, t, opts) {
    opts = opts || {};
    stopPlay();
    sections.forEach(function (s) { s.classList.toggle("active", s.id === room); });
    document.body.classList.toggle("front-view", !room);
    document.body.classList.toggle("reader-view", !!room);
    state.room = room; state.t = t || 0; state.prevT = -1;
    setHash(room, state.t);
    var sec = room ? document.getElementById(room) : null;
    var where = $(".topbar .where");
    document.title = sec ? roomTitle(sec) + " · " + $(".topbar .home").textContent : $(".topbar .home").textContent;
    if (sec) {
      where.textContent = roomTitle(sec);
      var i = order.indexOf(room);
      var prev = $(".topbar .prev-room"), next = $(".topbar .next-room");
      prev.href = i > 0 ? "#" + order[i - 1] : "#"; prev.title = i > 0 ? roomTitle(sections[i - 1]) : "index";
      next.href = i < order.length - 1 ? "#" + order[i + 1] : "#"; next.title = i < order.length - 1 ? roomTitle(sections[i + 1]) : "index";
      if (sec.classList.contains("room")) renderRoom(sec);
      else {
        var pn = $(".pagenav", sec);
        if (!pn) { pn = document.createElement("p"); pn.className = "pagenav"; sec.appendChild(pn); }
        pn.innerHTML = (i > 0 ? '<a href="#' + order[i - 1] + '">&larr; ' + esc(roomTitle(sections[i - 1])) + '</a>' : '<a href="#">&larr; index</a>')
          + ' &nbsp; ' + (i < order.length - 1 ? '<a href="#' + order[i + 1] + '">' + esc(roomTitle(sections[i + 1])) + ' &rarr;</a>' : '<a href="#">index &rarr;</a>');
      }
    }
    if (!opts.keepScroll) { window.scrollTo(0, 0); requestAnimationFrame(function () { window.scrollTo(0, 0); }); }
  }

  function renderRoom(sec) {
    var n = parseInt(sec.getAttribute("data-n"), 10);
    var t = Math.max(0, Math.min(state.t, n)); state.t = t;
    var ct = $(".counter .t", sec); ct.textContent = t; ct.classList.remove("tick"); void ct.offsetWidth; ct.classList.add("tick");
    $(".btn.back", sec).disabled = t === 0;
    var nextBtn = $(".btn.next", sec);
    var i = order.indexOf(sec.id);
    if (t >= n) { nextBtn.textContent = i < order.length - 1 ? "next room →" : "index"; nextBtn.classList.add("to-room"); }
    else { nextBtn.textContent = "next"; nextBtn.classList.remove("to-room"); }
    var still = (t === state.prevT + 1);
    $all(".lane", sec).forEach(function (lane, li) {
      renderLane(lane, t, still);
      var h = $('ol.hops > li.hop[data-t="' + t + '"]', lane);
      if (h && state.prevT !== t) setTimeout(function () { tone(h); }, li * 120);
    });
    var st = $(".counter .status", sec); var words = [];
    var lanes = $all(".lane", sec);
    lanes.forEach(function (lane) {
      var h = $('ol.hops > li.hop[data-t="' + t + '"]', lane); if (!h) return;
      var co = h.getAttribute("data-copy-of");
      var lab = lanes.length > 1 && $(".lane-label", lane) ? $(".lane-label", lane).textContent + ": " : "";
      if (co === null && h.getAttribute("data-same-text") === "1") words.push(lab + "same words as hop " + (t - 1));
      else if (co === null && h.getAttribute("data-text-copy-of") !== null) words.push(lab + "text same as hop " + h.getAttribute("data-text-copy-of"));
      if (co !== null) {
        var prev = $('ol.hops > li.hop[data-t="' + (t - 1) + '"]', lane);
        var pco = prev ? prev.getAttribute("data-copy-of") : null;
        var since = (pco !== null && pco === co) ? co : String(t - 1);
        words.push(lab + (parseInt(co, 10) === t - 1 || (pco !== null && pco === co) ? "unchanged since hop " + since : "same as hop " + co));
      }
    });
    st.textContent = words.length ? words.join(" / ") : "";
    state.prevT = t;
    setHash(sec.id, t);
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
    if (t > n) { var i = order.indexOf(sec.id); if (i < order.length - 1) show(order[i + 1], 0); else show(null, 0); return; }
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
  });

  document.addEventListener("keydown", function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var tag = (e.target && e.target.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA") return;
    if (!state.room) { if (e.key === "ArrowRight" || e.key === "Enter" && false) { } return; }
    if (e.key === "ArrowRight" || e.key === " " || e.key === "j") { e.preventDefault(); step(1); }
    else if (e.key === "ArrowLeft" || e.key === "k") { e.preventDefault(); step(-1); }
    else if (e.key === "p") { togglePlay(); }
    else if (e.key === "r") { toggleRaw(); }
    else if (e.key === "s") { toggleSound(); }
    else if (e.key === "Escape") { show(null, 0); }
    else if (e.key === "n") { var i = order.indexOf(state.room); if (i < order.length - 1) show(order[i + 1], 0); }
    else if (e.key === "b") { var j = order.indexOf(state.room); if (j > 0) show(order[j - 1], 0); }
  });

  window.addEventListener("hashchange", function () {
    var h = parseHash();
    if (h.room !== state.room || h.t !== state.t) show(h.room, h.t);
  });

  var h0 = parseHash();
  show(h0.room, h0.t);
})();
