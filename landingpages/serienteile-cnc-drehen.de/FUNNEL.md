# Funnel – serienteile-cnc-drehen.de

## 1. Ziel

Maximal viele qualifizierte Anfragen für Serien-Drehteile (ab 100 Stk, Ø 6–60 mm).
Eine Seite. Ein Hauptziel: Zeichnung senden. Ein Nebenziel: Leitfaden holen.

## 2. Funnel-Struktur

```
Traffic (Google Ads, SEO, LinkedIn, Direktansprache)
        │
        ▼
Landingpage ──► Hauptweg: Anfrage mit Zeichnung (2 Schritte) ──► danke.html ──► Angebot in 48 h ──► Auftrag
        │
        └────► Nebenweg: Leitfaden (nur E-Mail) ──► danke-leitfaden.html ──► „Zeichnung senden“
                                                     └─► Lead-Mail an AUROB ──► persönlich nachfassen
```

Warum zwei Wege: Wer heute eine Zeichnung hat, fragt direkt an. Wer erst sammelt, holt den Leitfaden. So geht kein Besucher verloren.

## 3. Aufbau der Seite (Reihenfolge = Kaufentscheidung)

| Nr | Abschnitt | Aufgabe |
|---|---|---|
| – | Hero | Angebot in 5 Sekunden klar: was, ab wie viel, welche Maße, was ist inklusive. CTA sofort sichtbar. |
| 01 | Problem | Schmerz benennen: lange Angebote, durchs Raster fallen, drei Lieferanten. |
| 02 | Ablauf | Lösung in 4 Schritten. „Ein Ansprechpartner.“ |
| 03 | Leistungsbereich | Hüllkurve + Sofort-Prüfung „Passt mein Teil?“. Kleine Zusage vor der großen. Füllt das Formular vor. |
| 04 | Werkstoffe & Oberflächen | Einwände „Könnt ihr mein Material?“ vorwegnehmen. |
| 05 | Galerie | Beweis: echte Teile. |
| 06 | Leitfaden | Leadmagnet für Besucher ohne fertige Zeichnung. |
| 07 | Zusagen | Risiko senken: 48 h, 1 Ansprechpartner, Stückpreis, NDA. |
| 08 | Formular | 2 Schritte. Schritt 1 nur Stückzahl Pflicht. Datei optional. |
| 09 | FAQ | Letzte Einwände. |
| – | Schlussaufruf | Noch einmal beide Wege. |

Mobil: feste Leiste unten mit „Zeichnung senden“, sobald der Hero aus dem Bild ist.

## 4. Leadmagnet

„Drehteile günstiger konstruieren – 12 Hebel für Serien ab 100 Stück“ (8 Seiten PDF).
Prinzip nach Hormozi: Er löst ein enges Problem (zu teure Zeichnung) und zeigt das nächste Problem (wer fertigt das jetzt günstig?). Seite 7 ist eine Anfrage-Checkliste, Seite 8 das Angebot.

## 5. Nachfassen (manuell, bis es läuft)

| Wann | Was | Kanal |
|---|---|---|
| Anfrage + 0 | Automatische Eingangsbestätigung | `anfrage.php` |
| Anfrage + max. 48 h | Angebot mit Kostenhinweisen (Hebel aus dem Leitfaden) | E-Mail |
| Angebot + 3 Tage | Kurzer Anruf: „Passt das Angebot? Fragen?“ | Telefon |
| Angebot + 10 Tage | Letzte Nachfrage, ggf. Alternative (Werkstoff, Losgröße) | E-Mail |
| Leitfaden + 2–3 Tage | Persönliche Mail: „Haben Sie ein Teil, bei dem wir prüfen sollen?“ | E-Mail / LinkedIn |

Hinweis DSGVO: Eine automatische Mail-Serie an Leitfaden-Leads braucht eine eigene Einwilligung (Double-Opt-in). Einzelne persönliche Nachfrage im B2B ist üblich. Vorher rechtlich prüfen.

Optional: `webhook_url` in `inc/config.php` auf einen n8n-Workflow setzen. Dann landet jede Anfrage automatisch in Notion/CRM.

## 6. Traffic (Vorschlag, noch nicht umgesetzt)

1. Google Ads auf Suchbegriffe mit Kaufabsicht: „cnc drehteile serie“, „lohndreherei anfrage“, „drehteile 500 stück“, „drehteile edelstahl fertigen lassen“.
2. Die anderen Domains (cnc-dortmund.de, cnc-bochum.de …) per 301 auf passende Seiten leiten, nicht doppelt befüllen.
3. Direktansprache von Einkäufern im Maschinenbau (z. B. mit Apollo) mit Link zum Leitfaden.

## 7. Kennzahlen

| KPI | Ziel (Startwert, später anpassen) |
|---|---|
| Besucher → Anfrage | 3–6 % |
| Besucher → Leitfaden | 4–8 % |
| Formular Schritt 1 → Schritt 2 → gesendet | > 50 % fertig |
| Anfrage → Angebot | 100 % in 48 h |
| Angebot → Auftrag | messen |

## 8. Quellen der Recherche

- Hormozi, $100M Leads – Leadmagnet: enges Problem lösen, nächstes Problem zeigen: https://www.shortform.com/summary/100m-leads-summary-alex-hormozi
- Mehrstufige RFQ-Formulare, kurze erste Stufe: https://www.thecommerceshop.com/blog/b2b-conversion-rate-optimization-for-manufacturer/
- Benchmarks Landingpages Fertigung: https://www.webtonic.io/blog/manufacturing-landing-page-statistics
- Zu lange RFQ-Formulare kosten Anfragen: https://redefineweb.com/blog/proven-manufacturing-website-design-best-practices-rfqs/
- Jonas Eisert: Die Websuche fand kein Material von ihm. Link oder Kurs bitte nachreichen.
