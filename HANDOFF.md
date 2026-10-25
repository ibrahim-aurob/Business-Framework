# AUROB Business-Framework – Übergabe an Claude Code

Stand: 25.10.2026, 21:40 Uhr
Von: Claude-Chat (claude.ai)
Für: Claude Code (Code-Bereich)

---

## 1. Ziel

Ibrahim will das komplette Framework seines Betriebs auf **einer** Leinwand abbilden.

- Das Gesamtbild muss als **ein Bild** sichtbar sein. Das hat Priorität.
- Man zoomt rein und klickt Elemente an. So erreicht man die Details.
- Details: Prozesse, Verknüpfungen, Tools, SOPs, Datenbanken.
- Regel: „Wenn du das aufsetzt, läuft der Laden.“
- Das Framework ist das **Grundskelett** für weitere Firmen und Ideen. Das Skelett und die Tools bleiben gleich.
- Das Framework ist auch Teil des geplanten Second Brain.

Vorbild: Instagram-Reels von „business.framwork“ (siehe `bilder/`). Dort ist ein Marketing-Framework in Figma abgebildet:
- Oben die Firmenkarte, darunter die Bereiche.
- Jeder Bereich hat dasselbe Raster: Objective, Tools, Strategie, Unterpunkte.

---

## 2. Feste Arbeitsregeln für Claude

1. **ASD-STE100** gilt für alle Antworten, auch auf Deutsch:
   - kurze Sätze, maximal 20 Wörter
   - eine Aussage pro Satz
   - Aktiv statt Passiv
   - einfache, eindeutige Wörter
   - Schritte als nummerierte Liste
   - keine Einleitung, kein Füllstoff
2. **Vorher fragen.** Vor neuen Vorschlägen und vor jeder Vertiefung fragt Claude zuerst. Grund: Vieles wurde besprochen, aber nicht umgesetzt.
3. Erst das Tool festlegen, dann den Rest.
4. Kommunikation: informell, Deutsch, direkt, umsetzungsorientiert.

---

## 3. Entscheidungen

| Thema | Entscheidung | Grund |
|---|---|---|
| Leinwand | **Miro** | Board liegt dauerhaft online. Claude kann über den Connector lesen und schreiben. |
| Detail-Ebene / Datenbank | **Notion** | Ist schon verbunden. Prozesse, SOPs und Tools liegen als Seiten bzw. Datenbanken dort. Miro-Karten verlinken auf Notion. |
| Obsidian | verworfen | Kein echtes Gesamtbild auf der Leinwand. Demo liegt in `obsidian-demo-verworfen/`. |
| Figma | verworfen | Bringt nur Optik. Der Connector im Free-Plan ist stark begrenzt. Miro erzeugt das Bild. |
| tldraw | verworfen | Kostenlos, aber unklar, ob das Bild dauerhaft und editierbar bleibt. |

### Kosten
- Miro Free: 3 Boards. Das reicht für ein großes Gesamt-Board.
- Miro-Connector (MCP): in allen Plänen. Free: 100 Aufrufe pro Tag. Starter: 500 Aufrufe pro Tag.
- Einige Miro-Funktionen verbrauchen Miro-AI-Credits.
- Notion: keine neuen Kosten.
- Quelle: https://help.miro.com/hc/en-us/articles/31624028247058

---

## 4. Aktueller Stand

| Was | Status | Link |
|---|---|---|
| Miro-Connector | verbunden (claude.ai) | – |
| Miro-Board „AUROB Framework – Demo“ | Firmenkarte + 10 Bereichskarten mit Raster (Stand 25.10.2026) | https://miro.com/app/board/uXjVEVyVTQo=/ |
| Notion-Testseite „AUROB Framework – Demo (Testseite)“ | angelegt, privat | https://app.notion.com/p/4049ed7d062281939737efd1c7f3a94a |
| Notion „AUROB Business-Framework“ (privat, getrennt) | Hauptseite + Datenbank „Bereiche“ mit 10 Seiten | https://app.notion.com/p/4049ed7d062281a99a63ebcc48c42b74 |
| Oberbereiche | **bestätigt** (10 Bereiche, siehe Abschnitt 5) | – |
| find-skills | als Projekt-Skill in `.claude/skills/find-skills/` | – |

---

## 5. Offener Punkt: Oberbereiche

Ibrahims Vorgabe:
- Zuerst die **Oberbereiche**, die für **jedes** Unternehmen gelten.
- Beispiel: Kalkulation ist kein Oberbereich. Sie gehört unter Verkauf/Vertrieb.
- Fulfillment, Vertrieb und Marketing sind getrennte Oberbereiche.
- Unter jedem Oberbereich folgen später viele Unterbegriffe.

Bestätigt am 25.10.2026 (Innovation gehört zu Führung & Strategie):

1. Führung & Strategie – Vision, Ziele, Organisation
2. Marketing – Sichtbarkeit, Website, Leads
3. Vertrieb – Anfrage, Kalkulation, Angebot, Auftrag
4. Fulfillment (Leistungserbringung) – Engineering, Fertigung, Qualität
5. Einkauf & Lieferkette – Lieferanten, Material, Lager, Versand
6. Kundenbetreuung – Reklamation, Kundenbindung, Service
7. Finanzen – Buchhaltung, Rechnungen, Liquidität, Controlling
8. Personal – Recruiting, Einarbeitung, Schulung
9. IT & Systeme – Software, Daten, Automatisierung
10. Recht & Verwaltung – Verträge, Versicherungen, Rechtsform

Umbenannt: „Fulfillment“ heißt jetzt „Leistungserbringung“.

Raster pro Bereichskarte (bestätigt): Ziel, Verantwortlich, Tools, Kernprozesse, KPIs, Schnittstellen.

---

## 6. Skills: find-skills (vercel-labs/skills)

Repo: https://github.com/vercel-labs/skills (MIT-Lizenz)
Kopien im Ordner `repo-doku/`: README.md, AGENTS.md, LICENSE, find-skills/SKILL.md

### Was find-skills macht
- Sucht Skills im Verzeichnis https://skills.sh/.
- Prüft Installationszahl, Quelle und GitHub-Sterne.
- Zeigt Treffer mit Installationsbefehl.
- Installiert erst nach Freigabe.

### Setup in Claude Code (auf Ibrahims PC)
1. Node.js installieren (für `npx`).
2. find-skills global installieren:
   ```bash
   npx skills add https://github.com/vercel-labs/skills --skill find-skills -g -a claude-code -y
   ```
3. Prüfen:
   ```bash
   npx skills list
   ```
4. Claude Code neu starten.

### Wichtige Befehle
```bash
npx skills find <begriff>        # suchen
npx skills add <owner/repo@skill> -g -y   # installieren (global)
npx skills update                # alle aktualisieren
```

### Hinweise aus der Anleitung (Google Doc)
Quelle: https://docs.google.com/document/d/e/2PACX-1vR6fuoyatpLCLciu9jiYgXSkXAkEhLIoREHGf674CIth6rXQtrm3-DLOOnHFCqhTSRlbpopP27Fd_Ow/pub
- Das Ergebnis konkret beschreiben. Vage Anfragen liefern vage Treffer.
- Ohne `-g` gilt ein Skill nur in einem Projekt.
- Erscheint ein Skill nicht: Claude Code neu starten, `npx skills list` prüfen, mit `-a claude-code` neu installieren.
- Treffer vor der Installation prüfen. Ein Skill gibt Claude neue Anweisungen.
- Die Anleitung enthält drei Prompt-Vorlagen: Projekt-Starter, Setup-Check, Wochen-Workflow.

### Ibrahims Arbeitsprompt (Projekt-Starter)
```
Nutz find-skills. Ich arbeite gerade an: [Projekt oder Ziel in einem Satz].
Schau dir dafür auch die Dateien in diesem Ordner an.
Such mir die 5 Skills, die mir dabei am meisten helfen. Zeig mir für jeden
als kurze Liste: Name, was er macht, Quelle, Anzahl Installationen und den
Befehl zum Installieren. Nimm nur Skills mit über 1.000 Installationen.
Installier noch nichts, ich entscheide danach.
```

### Erkenntnis aus dem Chat
- In der claude.ai-Cloud blockiert die Netzwerk-Allowlist `skills.sh`. Darum lieferte `npx skills find` dort keine Treffer.
- Lokal in Claude Code sollte der Befehl funktionieren.
- Top 3 auf skills.sh (25.10.2026): find-skills (4,0 Mio.), grill-me (1,4 Mio.), agent-browser (1,2 Mio.).

---

## 7. Erster Auftrag in Claude Code

1. find-skills installieren (Abschnitt 6).
2. Den Projekt-Starter-Prompt ausführen mit:
   „Business-Framework für AUROB auf Miro + Notion aufbauen, als Skelett für weitere Firmen.“
3. Top 5 zeigen. **Nichts installieren.** Ibrahim entscheidet.
4. Danach: Oberbereiche festlegen (Abschnitt 5). **Vorher fragen.**

Hinweis: Den Miro-Connector in Claude Code separat einrichten, falls er dort fehlt.

---

## 8. Gesprächsverlauf (25.10.2026)

**21:07 – Ibrahim** schickt 3 Screenshots (siehe `bilder/`). Im Kern sagt er: Er will so ein Framework komplett ausarbeiten. Beim Reinzoomen und Anklicken soll alles versteckt sein, was den Betrieb zu 100 % ausmacht. Er will mal hier, mal dort arbeiten, Prozesse beschreiben und Verknüpfungen abbilden. Das Framework soll Teil des Second Brain sein und das Skelett für weitere Firmen. Frage: Wie kann Claude helfen? Welches Tool? Figma muss es nicht sein, vielleicht tldraw.

**Claude:** Erklärt das Vorbild. Empfiehlt Obsidian (Canvas + Notizen). Nennt Figma, tldraw und Notion als Alternativen. Schlägt ein Skelett mit Ebenen und einem Fertigungsfokus vor.

**21:11 – Ibrahim:** Die Antworten sind zu lang und kosten Zeit. Ab jetzt gilt ASD-STE100 als feste Richtlinie.

**Claude:** Bestätigt die Regeln und speichert sie als Präferenz.

**21:12 – Ibrahim:** Er hat tldraw vorgeschlagen. Erst das Tool festlegen, dann der Rest.

**Claude:** Vergleicht tldraw und Obsidian. Nennt die Kombination über das Plugin „tldraw in Obsidian“.

**21:13 – Ibrahim:** Will eine winzige Obsidian-Demo zum Bewerten.

**Claude:** Baut eine Demo-Vault mit Canvas und 6 Notizen (siehe `obsidian-demo-verworfen/`).

**21:20 – Ibrahim:** Das gefällt ihm nicht. Er will das Gesamtbild als ein Bild auf einer Leinwand. Klicks auf eine Datenbank sind okay. Claude muss trotzdem darauf arbeiten können. Er will andere Vorschläge.

**Claude:** Prüft die Connectoren. Schlägt Miro + Notion vor. Nennt tldraw und Figma als Alternativen.

**21:22 – Ibrahim:** Fragt nach den Kosten.

**Claude:** Antwortet mit Miro Free (3 Boards, 100 Aufrufe pro Tag) und Figma Free (stark begrenzt). Notion ist schon vorhanden.

**21:23 – Ibrahim:** „Wozu Figma, wenn Miro das Bild erzeugt?“

**Claude:** Figma ist nicht nötig. Das Set ist Miro + Notion.

**21:25 – Ibrahim:** Warum nicht tldraw, wenn es kostenlos ist?

**Claude:** Bei tldraw ist offen, ob das Bild dauerhaft bleibt. Miro speichert das Board dauerhaft.

**21:26 – Ibrahim:** Entscheidung: Miro + Notion. Er fragt nach dem Link zum Verbinden.

**21:27 – Ibrahim:** Miro ist verbunden. Neue Regel: Vor Vorschlägen und vor jeder Vertiefung immer fragen.

**21:28 – Ibrahim:** Board anlegen: ja. Bereiche besprechen wir gleich. Notion-Testseite: ja.

**Claude:** Legt das Miro-Board und die Notion-Testseite an.

**21:30 – Ibrahim:** Er will zuerst den Vorschlag hören. Die Oberbereiche sollen für jedes Unternehmen gelten. Kalkulation ist nur ein Teil des Verkaufs. Fulfillment, Vertrieb und Marketing sollen getrennt sein.

**Claude:** Schlägt 10 Oberbereiche vor und einen optionalen elften (Abschnitt 5).

**21:31 – Ibrahim:** Er will Claudes Skills über Repos erweitern.

**21:36 – Ibrahim:** Schickt das Repo vercel-labs/skills, das Google Doc und seinen Arbeitsprompt.

**Claude:** Liest beides. Der Test zeigt: skills.sh ist in der Cloud blockiert, aber über die Websuche lesbar.

**21:39 – Ibrahim:** Will diese Übergabe als ZIP für den Code-Bereich.

---

## 9. Ordnerinhalt

```
AUROB-Framework-Handoff/
├── HANDOFF.md                  # diese Datei
├── CLAUDE.md                   # Regeln für Claude Code
├── bilder/                     # 3 Screenshots der Reels
├── repo-doku/                  # vercel-labs/skills: README, AGENTS, LICENSE, find-skills/SKILL.md
└── obsidian-demo-verworfen/    # erste Demo, nur zur Referenz
```
