#!/usr/bin/env python3
"""Baut die statischen Seiten aus src/.

Aufruf (im Ordner serienteile-cnc-drehen.de):
    python3 src/build.py
Erzeugt: index.html, danke.html, danke-leitfaden.html, impressum.html, datenschutz.html
"""
import os
import re
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

subprocess.run([sys.executable, os.path.join(SRC, "svg.py")], check=True)


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()


def write(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(text)
    print("geschrieben:", name)


# ---------- index.html ----------
html = read("index.src.html")
html = html.replace("{{HERO_SVG}}", read("hero.svg")).replace("{{ENV_SVG}}", read("envelope.svg"))


def gallery_img(m):
    path, caption = m.group(1), m.group(2)
    fname = os.path.basename(path)
    return (
        f'<div class="img"><div class="ph">Bild folgt · {fname}</div>'
        f'<img src="{path}" alt="{caption}" loading="lazy" width="1200" height="900" onerror="this.remove()"></div>'
        f"<figcaption>{caption}</figcaption>"
    )


html = re.sub(
    r'<div class="img"><div class="ph">(assets/img/[^<]+)</div></div><figcaption>([^<]+)</figcaption>',
    gallery_img,
    html,
)
write("index.html", html)

# ---------- Unterseiten ----------
HEAD = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · AUROB Serien-Drehteile</title>
<meta name="robots" content="{robots}">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="./"><b>AUROB</b><span>Serien-Drehteile</span></a>
  <nav><a class="btn btn--sm btn--ghost" href="./">← Zur Startseite</a></nav>
</div></header>
<main class="page"><div class="wrap narrow">
"""
FOOT = """
</div></main>
<footer><div class="wrap">
  <div class="titleblock">
    <div><span class="k">Hersteller</span><span class="brand-l">AUROB</span></div>
    <div><span class="k">Benennung</span>Serien-Drehteile Ø 6–60</div>
    <div><span class="k">Kontakt</span><a href="mailto:info@aurob.de">info@aurob.de</a></div>
    <div><span class="k">Rechtliches</span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></div>
  </div>
</div></footer>
</body>
</html>
"""


def page(name, title, body, robots="noindex, follow"):
    write(name, HEAD.format(title=title, robots=robots) + body + FOOT)


page("danke.html", "Anfrage erhalten", """
<p class="kicker"><b>✓</b> Anfrage erhalten</p>
<h1>Danke. Ihre Anfrage ist bei uns.</h1>
<p class="lead">Sie bekommen gleich eine Bestätigung per E-Mail. So geht es weiter:</p>
<div class="steps" style="border-top-color:var(--rule);grid-template-columns:repeat(3,1fr);margin-top:36px">
  <div class="step"><span class="n">01</span><h3>Prüfung</h3><p style="color:var(--ink-2)">Wir prüfen Zeichnung, Werkstoff und Stückzahl.</p></div>
  <div class="step" style="border-left-color:var(--rule)"><span class="n">02</span><h3>Rückfrage</h3><p style="color:var(--ink-2)">Fehlt etwas, melden wir uns kurz bei Ihnen.</p></div>
  <div class="step" style="border-left-color:var(--rule)"><span class="n">03</span><h3>Angebot</h3><p style="color:var(--ink-2)">Innerhalb von 48 Stunden haben Sie Ihren Stückpreis.</p></div>
</div>
<p style="margin-top:48px">Noch eine Datei vergessen? Antworten Sie einfach auf die Bestätigungs-E-Mail.</p>
<div style="margin-top:40px;padding:26px;border:1.5px solid var(--ink);background:#fbfaf7">
  <p class="kicker" style="margin-bottom:12px"><b>Tipp</b> Für die nächste Konstruktion</p>
  <p style="font-size:19px;font-weight:600;margin-bottom:16px">12 Hebel, die Drehteile günstiger machen – der kostenlose Leitfaden.</p>
  <a class="btn" href="leitfaden/AUROB-Leitfaden-Drehteile-guenstiger-konstruieren.pdf" download>Leitfaden herunterladen (PDF) <span class="arr">↓</span></a>
</div>
""")

page("danke-leitfaden.html", "Leitfaden unterwegs", """
<p class="kicker"><b>✓</b> Leitfaden unterwegs</p>
<h1>Der Leitfaden ist in Ihrem Postfach.</h1>
<p class="lead">Nichts angekommen? Prüfen Sie den Spam-Ordner. Oder laden Sie ihn direkt hier:</p>
<p><a class="btn btn--ghost" href="leitfaden/AUROB-Leitfaden-Drehteile-guenstiger-konstruieren.pdf" download>Leitfaden herunterladen (PDF) <span class="arr">↓</span></a></p>
<div style="margin-top:56px;padding:30px;border:1.5px solid var(--ink);background:#fbfaf7">
  <p class="kicker" style="margin-bottom:12px"><b>Nächster Schritt</b> Sie haben schon eine Zeichnung?</p>
  <h2 style="font-size:clamp(26px,3vw,36px);font-variation-settings:'wdth' 85;margin-bottom:14px">Wir prüfen sie kostenlos – mit Stückpreis in 48 Stunden.</h2>
  <p style="color:var(--ink-2)">Sie bekommen dazu konkrete Hinweise, welche der 12 Hebel bei Ihrem Teil greifen.</p>
  <a class="btn btn--signal" href="./#anfrage">Zeichnung senden <span class="arr">→</span></a>
</div>
""")

page("impressum.html", "Impressum", """
<h1>Impressum</h1>
<p><span class="todo">TODO: Vor dem Livegang mit echten Daten füllen. Am besten mit einem Impressum-Generator (z. B. e-recht24) prüfen.</span></p>
<h2>Angaben gemäß § 5 DDG</h2>
<p><span class="todo">[Firmenname, Rechtsform]</span><br><span class="todo">[Straße Nr.]</span><br><span class="todo">[PLZ Ort]</span></p>
<h2>Vertreten durch</h2>
<p><span class="todo">[Geschäftsführer / Inhaber]</span></p>
<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:info@aurob.de">info@aurob.de</a><br>Telefon: <span class="todo">[Telefonnummer]</span></p>
<h2>Registereintrag</h2>
<p><span class="todo">[Registergericht, Registernummer – falls vorhanden]</span></p>
<h2>Umsatzsteuer-ID</h2>
<p><span class="todo">[USt-IdNr. gemäß § 27a UStG]</span></p>
<h2>Verantwortlich für den Inhalt</h2>
<p><span class="todo">[Name, Anschrift]</span></p>
""")

page("datenschutz.html", "Datenschutz", """
<h1>Datenschutzerklärung</h1>
<p><span class="todo">TODO: Entwurf. Vor dem Livegang rechtlich prüfen lassen oder mit einem Generator (z. B. e-recht24, Datenschutz-Generator.de) erstellen.</span></p>
<h2>1. Verantwortlicher</h2>
<p><span class="todo">[Firmenname, Anschrift]</span>, E-Mail: <a href="mailto:info@aurob.de">info@aurob.de</a></p>
<h2>2. Hosting</h2>
<p>Diese Website liegt bei der ALL-INKL.COM – Neue Medien Münnich, Friedersdorf. Beim Aufruf verarbeitet der Server technisch nötige Daten (IP-Adresse, Zeitpunkt, aufgerufene Seite) in Logdateien. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO. Mit dem Hoster besteht ein Vertrag zur Auftragsverarbeitung.</p>
<h2>3. Keine Cookies, kein Tracking</h2>
<p>Diese Seite setzt keine Cookies und nutzt keine Analyse- oder Werbedienste. Schriften werden lokal geladen, nicht von Google.</p>
<h2>4. Anfrageformular</h2>
<p>Wenn Sie eine Anfrage senden, verarbeiten wir Ihre Angaben und hochgeladenen Dateien, um Ihnen ein Angebot zu machen. Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) und Ihre Einwilligung (lit. a). Die Daten gehen per E-Mail an uns. Wir löschen sie, wenn kein Auftrag zustande kommt, spätestens nach 24 Monaten, soweit keine gesetzlichen Aufbewahrungspflichten bestehen.</p>
<h2>5. Leitfaden-Download</h2>
<p>Für den Versand des Leitfadens verarbeiten wir Ihre E-Mail-Adresse. Wir senden Ihnen den Leitfaden und melden uns gegebenenfalls einmal persönlich. Wir schicken keinen Newsletter. Rechtsgrundlage: Art. 6 Abs. 1 lit. b und f DSGVO. Sie können jederzeit widersprechen: eine E-Mail an info@aurob.de genügt.</p>
<h2>6. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit und Widerspruch sowie auf Beschwerde bei einer Aufsichtsbehörde.</p>
""")

# ---------- Leitfaden-PDF ----------
lf = read("leitfaden.html").replace("{{HERO_SVG}}", read("hero.svg"))
tmp = os.path.join(SRC, "_leitfaden.build.html")
with open(tmp, "w", encoding="utf-8") as f:
    f.write(lf)
os.makedirs(os.path.join(ROOT, "leitfaden"), exist_ok=True)
pdf = os.path.join(ROOT, "leitfaden", "AUROB-Leitfaden-Drehteile-guenstiger-konstruieren.pdf")
try:
    subprocess.run(["node", os.path.join(SRC, "pdf.js"), tmp, pdf], check=True)
    print("geschrieben:", os.path.relpath(pdf, ROOT))
except Exception as e:  # Node/Playwright fehlt
    print("PDF übersprungen:", e)
finally:
    os.remove(tmp)
