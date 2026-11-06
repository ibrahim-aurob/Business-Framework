/* serienteile-cnc-drehen.de – Interaktion. Ohne Bibliotheken. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Zeitstempel gegen Bots */
  $$(".ts").forEach(function (i) { i.value = String(Date.now()); });

  /* ---------- Passt mein Teil? ---------- */
  var cD = $("#c-d"), cL = $("#c-l"), cQ = $("#c-q"), out = $("#c-out");
  var probe = document.getElementById("probe");
  // Diagramm-Geometrie (muss zu svg.py passen)
  var G = { ml: 64, mt: 28, pw: 552, ph: 334 };
  function num(el) { var v = parseFloat(String(el.value).replace(",", ".")); return isNaN(v) ? null : v; }
  function maxLen(d) { if (d < 6 || d > 60) return 0; return d < 40 ? 80 : 150; }

  function check() {
    if (!out) return;
    var d = num(cD), l = num(cL), q = num(cQ);
    out.className = "";
    if (probe) {
      if (d !== null && l !== null) {
        var x = G.ml + Math.min(l, 160) / 160 * G.pw;
        var y = G.mt + G.ph - Math.min(d, 70) / 70 * G.ph;
        probe.setAttribute("transform", "translate(" + x.toFixed(1) + "," + y.toFixed(1) + ")");
        probe.style.display = "";
      } else probe.style.display = "none";
    }
    if (d === null || l === null) { out.textContent = "Tragen Sie Durchmesser und Länge ein."; return; }

    var lim = maxLen(d);
    var fits = lim > 0 && l > 0 && l <= lim;
    var qtyLow = q !== null && q < 100;
    var link = '<a href="#anfrage" data-prefill>Mit diesen Werten anfragen →</a>';

    if (fits && !qtyLow) {
      out.className = "ok";
      out.innerHTML = "<b>Passt.</b> Bereich " + (d < 40 ? "A" : "B") + ", bis " + lim + " mm Länge. " + link;
    } else if (fits && qtyLow) {
      out.className = "no";
      out.innerHTML = "<b>Maße passen.</b> Wir fertigen ab 100 Stück. Bei Folgebedarf lohnt die Anfrage trotzdem. " + link;
    } else if (d < 6 || d > 60) {
      out.className = "no";
      out.innerHTML = "<b>Außerhalb Ø 6–60 mm.</b> Schicken Sie die Zeichnung trotzdem. Wir sagen ehrlich, ob wir helfen können. " + link;
    } else {
      out.className = "no";
      out.innerHTML = "<b>Zu lang für Ø " + d + " mm.</b> Hier sind bis " + lim + " mm möglich. Fragen Sie trotzdem an – oft gibt es eine Lösung. " + link;
    }
  }
  [cD, cL, cQ].forEach(function (el) { if (el) el.addEventListener("input", check); });

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-prefill]");
    if (!a) return;
    var d = num(cD), l = num(cL), q = num(cQ);
    if (d !== null) $("#durchmesser").value = String(d).replace(".", ",");
    if (l !== null) $("#laenge").value = String(l).replace(".", ",");
    if (q !== null && q > 0) $("#menge").value = Math.round(q);
  });

  /* ---------- Mobile CTA-Leiste ---------- */
  var mbar = $("#mbar"), hero = $(".hero"), rfq = $("#anfrage");
  if (mbar && "IntersectionObserver" in window) {
    var heroVisible = true, rfqVisible = false;
    var upd = function () { mbar.classList.toggle("show", !heroVisible && !rfqVisible); };
    new IntersectionObserver(function (en) { heroVisible = en[0].isIntersecting; upd(); }, { threshold: 0.15 }).observe(hero);
    new IntersectionObserver(function (en) { rfqVisible = en[0].isIntersecting; upd(); }, { threshold: 0.05 }).observe(rfq);
  }

  /* ---------- Anfrage-Formular (2 Schritte) ---------- */
  var form = $("#rfq-form");
  if (!form) return;
  var s1 = $('[data-step="1"]', form), s2 = $('[data-step="2"]', form);
  var next = $("#next"), back = $("#back"), send = $("#send"), note = $("#step-note"), status = $("#rfq-status");
  var input = $("#files"), list = $("#file-list"), drop = $("#drop"), ferr = $("#file-err");
  var MAX_FILES = 5, MAX_BYTES = 20 * 1024 * 1024;
  var files = [];
  var canDT = (function () { try { return !!new DataTransfer(); } catch (e) { return false; } })();

  function go(step) {
    s1.hidden = step !== 1; s2.hidden = step !== 2;
    next.hidden = step !== 1; send.hidden = step !== 2; back.hidden = step !== 2;
    note.textContent = step === 1 ? "Schritt 1 von 2 · kostenlos" : "Schritt 2 von 2 · fast geschafft";
    $$("[data-bar]", form).forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-bar") === String(step)); });
  }
  go(1);

  function fmt(b) { return b > 1048576 ? (b / 1048576).toFixed(1) + " MB" : Math.max(1, Math.round(b / 1024)) + " KB"; }
  function syncInput() {
    if (!canDT) return;
    var dt = new DataTransfer();
    files.forEach(function (f) { dt.items.add(f); });
    input.files = dt.files;
  }
  function render() {
    list.innerHTML = "";
    files.forEach(function (f, i) {
      var li = document.createElement("li");
      li.innerHTML = "<span></span><span>" + fmt(f.size) + ' <button type="button" aria-label="Datei entfernen">✕</button></span>';
      li.firstChild.textContent = f.name;
      li.querySelector("button").addEventListener("click", function () { files.splice(i, 1); syncInput(); render(); });
      list.appendChild(li);
    });
  }
  function addFiles(fl) {
    ferr.parentNode.classList.remove("invalid");
    var arr = Array.prototype.slice.call(fl);
    if (!canDT) { files = arr; render(); return; }
    arr.forEach(function (f) {
      if (!files.some(function (g) { return g.name === f.name && g.size === f.size; })) files.push(f);
    });
    var total = files.reduce(function (s, f) { return s + f.size; }, 0);
    if (files.length > MAX_FILES || total > MAX_BYTES) {
      files = files.slice(0, MAX_FILES);
      while (files.reduce(function (s, f) { return s + f.size; }, 0) > MAX_BYTES) files.pop();
      ferr.textContent = "Maximal " + MAX_FILES + " Dateien und 20 MB. Größere Dateien bitte per E-Mail.";
      ferr.parentNode.classList.add("invalid");
    }
    syncInput(); render();
  }
  input.addEventListener("change", function () { addFiles(input.files); });
  ["dragenter", "dragover"].forEach(function (t) { drop.addEventListener(t, function () { drop.classList.add("over"); }); });
  ["dragleave", "drop"].forEach(function (t) { drop.addEventListener(t, function () { drop.classList.remove("over"); }); });
  if (canDT) {
    drop.addEventListener("drop", function (e) { e.preventDefault(); addFiles(e.dataTransfer.files); });
  }

  function invalid(id, bad) { var f = $(id); if (f) f.classList.toggle("invalid", bad); return bad; }
  function v1() {
    var m = parseInt($("#menge").value, 10);
    return !invalid("#f-menge", !(m > 0));
  }
  function v2() {
    var ok = true;
    if (invalid("#f-name", !$("#name").value.trim())) ok = false;
    if (invalid("#f-firma", !$("#firma").value.trim())) ok = false;
    if (invalid("#f-email", !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test($("#email").value.trim()))) ok = false;
    if (invalid("#f-consent", !form.einwilligung.checked)) ok = false;
    return ok;
  }

  next.addEventListener("click", function () {
    if (!v1()) { $("#menge").focus(); return; }
    go(2);
    $("#name").focus({ preventScroll: true });
    form.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  back.addEventListener("click", function () { go(1); });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    status.classList.remove("show");
    if (s2.hidden) { next.click(); return; }
    if (!v1()) { go(1); $("#menge").focus(); return; }
    if (!v2()) { var f = $(".invalid input", s2); if (f) f.focus(); return; }
    if (!window.fetch || !window.FormData) { form.submit(); return; }

    var fd = new FormData(form);
    if (!canDT) { fd.delete && fd.delete("dateien[]"); files.forEach(function (f) { fd.append("dateien[]", f); }); }
    send.disabled = true;
    var label = send.innerHTML;
    send.textContent = "Wird gesendet …";

    fetch(form.action, { method: "POST", body: fd, headers: { "Accept": "application/json" } })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (res) {
        if (res && res.ok) { window.location.href = res.redirect || "danke.html"; return; }
        throw new Error((res && res.error) || "Unbekannter Fehler");
      })
      .catch(function (err) {
        status.textContent = "Senden fehlgeschlagen: " + err.message + " Bitte schreiben Sie uns direkt an info@aurob.de.";
        status.classList.add("show");
        send.disabled = false; send.innerHTML = label;
      });
  });
})();
