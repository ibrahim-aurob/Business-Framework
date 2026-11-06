# serienteile-cnc-drehen.de – Landingpage AUROB Fertigung

Statische Seite + 2 PHP-Skripte. Läuft direkt auf all-inkl. Kein CMS, kein Tracking, keine Cookies.

## Ordner

| Pfad | Inhalt |
|---|---|
| `index.html` | Landingpage (gebaut aus `src/index.src.html`) |
| `anfrage.php` | Anfrageformular → Mail mit Anhängen an AUROB + Bestätigung an Kunde |
| `leitfaden.php` | Leadmagnet → Mail mit PDF-Link an Kunde + Lead-Mail an AUROB |
| `danke.html`, `danke-leitfaden.html` | Danke-Seiten mit nächstem Schritt |
| `impressum.html`, `datenschutz.html` | **Platzhalter – vor Livegang füllen** |
| `leitfaden/…pdf` | Leadmagnet: 8 Seiten, „Drehteile günstiger konstruieren“ |
| `inc/config.php` | Empfänger, Absender, Limits, optional n8n-Webhook |
| `assets/` | CSS, JS, Schriften (lokal, DSGVO), Bilder |
| `src/` | Quellen + Build (`python3 src/build.py`) |

## Vor dem Livegang (Pflicht)

1. Bilder erzeugen und in `assets/img/` legen (Liste unten).
2. Impressum mit echten Firmendaten füllen.
3. Datenschutzerklärung prüfen lassen oder per Generator erstellen.
4. Im KAS das Postfach `anfrage@serienteile-cnc-drehen.de` anlegen (Absender der Mails).
5. Telefonnummer eintragen: in `src/index.src.html` nach `TODO Telefon` suchen. Danach `python3 src/build.py`.
6. Zusagen prüfen: „Angebot in 48 h“, „Material und Oberfläche im Preis“, „NDA auf Wunsch“. Nur behalten, was ihr einhaltet.

## Hochladen auf all-inkl

1. KAS → Domain `serienteile-cnc-drehen.de` → Zielverzeichnis prüfen, z. B. `/serienteile-cnc-drehen.de/`.
2. SSL im KAS aktivieren (Let's Encrypt). Im Screenshot fehlt es noch.
3. Per FTP den **Inhalt** dieses Ordners hochladen. `src/` darf mit, die `.htaccess` sperrt ihn.
4. KAS → PHP-Einstellungen: `upload_max_filesize = 20M`, `post_max_size = 25M`.
5. Test: Anfrage mit Datei senden. Leitfaden anfordern. Beide Mails prüfen, auch Spam-Ordner.

## Bilder (assets/img/)

Fehlt ein Bild, zeigt die Seite automatisch die technische Zeichnung bzw. ein Raster mit Dateinamen.
Format: JPG, ca. 1600 px breit, unter 300 KB. Echte Fotos aus eurer Fertigung sind immer besser als generierte.

| Datei | Format | Motiv / Prompt-Idee |
|---|---|---|
| `hero.jpg` | 4:3,3 (1600×1320) | Reihe frisch gedrehter Edelstahl-Präzisionsteile auf geöltem Stahltisch, seitliches Werkstattlicht, geringe Schärfentiefe, neutrale Farben, keine Menschen, kein Text |
| `teil-01.jpg` | 4:3, groß | Abgesetzte Welle aus Edelstahl 1.4305, Ø 25, mit Gewinde, auf grauem Stahl, Makro, Studiolicht von oben |
| `teil-02.jpg` | 4:3 | Messingbuchsen CuZn39Pb3, 20 Stück geordnet, warmes Licht, leicht ölig |
| `teil-03.jpg` | 4:3 | Gewindebolzen M12, galvanisch verzinkt, silbrig-bläulich, in Reihe |
| `teil-04.jpg` | 4:3 | Distanzhülsen Aluminium, schwarz eloxiert, matt, auf hellem Grund |
| `teil-05.jpg` | 4:3 | Hydraulik-Anschlussstücke Edelstahl 1.4404 mit Sechskant und Querbohrung |
| `teil-06.jpg` | 4:3 | Hunderte gleiche Drehteile in grauem Kleinladungsträger (KLT), Draufsicht |
| `og.jpg` (optional) | 1200×630 | Vorschaubild für LinkedIn/WhatsApp – sonst wird `hero.jpg` genutzt |

Bildunterschriften stehen in `src/index.src.html` (Abschnitt 05). Bei anderen Motiven dort anpassen.

## Ändern und neu bauen

```bash
cd landingpages/serienteile-cnc-drehen.de
python3 src/build.py      # baut alle HTML-Seiten und das Leitfaden-PDF (PDF braucht Node + Playwright)
php -S 127.0.0.1:8765     # lokal ansehen: http://127.0.0.1:8765
```

Texte nur in `src/` ändern, nicht in den gebauten `.html`-Dateien.
