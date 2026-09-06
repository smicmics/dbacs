---
name: dbacs-recherche
description: >-
  Vollständiger Ablauf für Katalog- und Recherchearbeit an DBACS: neue Baugruppen,
  Einzelbauteile oder Feldgeräte anlegen, fehlende Preise beschaffen, technische
  Daten / Herstellerdatenblätter (Abmessungen, Klemmenpläne, Datenpunkte) prüfen –
  und das Ergebnis über die Excel-Pipeline (ga_komponenten.xlsx → xlsx_to_json.py →
  Browser-Verifikation) einpflegen. Unbedingt verwenden, sobald in DBACS von
  Recherche, Katalog, Bauteil, Baugruppe, Feldgerät, Datenblatt, Artikelnummer,
  Abmessungen, Klemmen, Datenpunkten, Planungsfabrikat oder Preisen die Rede ist –
  auch wenn der Nutzer das Wort „Skill" nicht sagt. Nicht verwenden für reine
  Code-/Layout-Änderungen an den Modul-HTML-Dateien ohne Katalogbezug.
---

# DBACS – Recherche & Katalogpflege

Dieser Skill kapselt den wiederkehrenden Ablauf, mit dem in DBACS neue
Katalogdaten entstehen. Er hat einen **harten Stopp-Punkt bei der Freigabe**:
vor der Freigabe wird nichts in `ga_komponenten.xlsx` geschrieben.

Verbindliche Fachregeln stehen **nicht hier**, sondern in `CLAUDE.md`:
- `## Baugruppen-Modellierungsregeln (verbindlich)` – die 12 Regeln zu Klemmzonen,
  Steuerspannung, Koppelrelais, PE-Klemmen, kommunikativen Datenpunkten.
- `## Offene Punkte` – aktueller Restbestand an Recherche-Aufgaben.
- Die je Themenblock komprimierten Session-Zusammenfassungen.

Lies die relevanten `CLAUDE.md`-Abschnitte, bevor du eine Herleitung baust. Dieser
Skill sagt *wie* recherchiert und eingepflegt wird, `CLAUDE.md` sagt *was* fachlich
gilt.

Detail-Referenzen in diesem Skill:
- `references/planungsfabrikate.md` – bevorzugter Hersteller je Kategorie + wo die
  belastbaren Datenblätter/Preise liegen.
- `references/excel-pipeline.md` – Sheet-/Spaltenschema, WSL-Aufruf, Lock-/Backup-
  Regeln, Export, Browser-Verifikationscheckliste.
- `scripts/xlsx_write_template.py` – Muster-Writer (openpyxl) für neue/geänderte
  Zeilen in `ga_komponenten.xlsx`, nicht-destruktiv.

---

## Ablauf in 7 Phasen

### Phase 1 – Auftrag in Themenblöcke zerlegen

Zerlege die Rechercheaufgabe in **3–6 in sich geschlossene Blöcke**, einer je
Fork. Sinnvolle Schnitte:
- **je Gerätefamilie / Hersteller** (z. B. „alle Aquametro-Zähler DN50", „alle
  Belimo Energy-Valve-Baugrößen"),
- **je Baugruppe**, wenn mehrere unabhängige Baugruppen anzulegen sind,
- **je Preislisten-Häppchen** von ~5–10 Artikeln, wenn es reine Preissuche ist.

Ein Block ist gut geschnitten, wenn ein Fork ihn ohne Rückfrage an den
Hauptthread abarbeiten kann. Notiere die Blockliste kurz sichtbar für den Nutzer
(eine Zeile je Block), dann direkt weiter zu Phase 2 – **keine Rückfrage zur
Aufteilung**.

### Phase 2 – Forks direkt starten

Starte **alle Blöcke als Hintergrund-Forks in einem einzigen Turn**
(`Agent`, `subagent_type: "general-purpose"`, `run_in_background: true`). Jeder
Fork-Prompt enthält:

1. **Ziel**: was genau gesucht wird (Artikelnummer, Abmessungen b/h/t in mm,
   Kategorie, `zone`, Datenpunkte, Klemmenplan, Preis netto).
2. **Planungsfabrikat** für die Kategorie (aus `references/planungsfabrikate.md`)
   und die Anweisung: **Originaldatenblatt zuerst**. Binär-komprimierte
   Siemens-PDFs lokal per `pypdf`/`pdftotext` in WSL auslesen – der WebFetch-
   Zusammenfasser scheitert daran zuverlässig.
3. **Preisquellen-Rang**: Herstellerlistenpreis → namhafter Großhandel/
   Distributor → (nur zur Not, klar markiert) aus Brutto zurückgerechnet.
   Reine Gebraucht-/Privatangebote ausgeschlossen; die Marktplatz-Storefront
   eines Fachdistributors mit **Neuware** ist zulässig, dann aber im
   `quelle_hinweis` zusätzlich „abgekündigt/Auslauf, kein regulärer Listenpreis"
   vermerken (Details `references/planungsfabrikate.md`). Alles netto, Stand als
   `~MM/YYYY` notieren.
4. **Ausgabeformat**: strukturierte Fakten **mit Quell-URL je Einzelfakt**,
   geschrieben nach `scratchpad/fork_<n>_<slug>_ergebnis.md` (Projekt-Scratchpad,
   gitignored – bleibt über Sessions erhalten). Keine Excel-Zugriffe im Fork.
5. **Kein Raten**: was nicht belastbar auffindbar ist, wird als offen markiert,
   nicht geschätzt.

Wenn Forks nicht verfügbar sind (z. B. dieser Skill läuft selbst in einem
Subagenten ohne verschachtelte Spawns): dieselben Blöcke **nacheinander inline**
abarbeiten, Ergebnisse trotzdem je Block nach `scratchpad/fork_<n>_*.md`
schreiben.

### Phase 3 – Zusammenführen und Herleitung bauen

Lies alle `scratchpad/fork_*_ergebnis.md`. Die Herleitung folgt einer **festen
Reihenfolge** – nie rückwärts vom gewünschten Datenpunkt her raten:

1. **Datenblatt des Feldgeräts / externen Bauteils auswerten** – jeder
   elektrische Anschluss mit seiner Angabe (Signalart, Spannung, Kontakt/
   Wechsler, Schutzklasse, VA, eigener Erdungsanschluss ja/nein).
2. **Daraus die Anschluss-Anforderung an den Schaltschrank ableiten** – wie wird
   das Gerät angeklemmt, in welcher Zone (`klemm_l/f/s` …), und **welche
   schrankinternen Bauteile** zieht das nach sich (Koppelrelais, Steuertrafo/
   Netzteil über den Ratchet, LSS/MSS, PE-Klemme nur bei eigener Erdungsklemme
   im Plan …).
3. **Erst wenn Anschluss und Bauteile feststehen: die physischen Datenpunkte
   definieren** (`dp_ai/ao/bi/bo`) – sie ergeben sich aus den real verdrahteten
   Signalen, nicht umgekehrt.
4. **Kommunikative Datenpunkte** (`dp_fb_*` + Protokoll) ebenfalls auf
   Datenblatt-Basis definieren, **sobald die Werte nicht über eine
   herstellereigene Zusatz-/Kommunikationskarte mit eigener Platzierung laufen**
   (dann wären sie ein eigenes Bauteil). Bus direkt am Gerät ⇒ kommunikativ,
   ohne Schaltschrankplatz.

**Das Datenblatt ist die Grenze, nicht die Wunschliste.** Ein Datenpunkt, den
das Projekt braucht, für den das gewählte Gerät aber **keinen Anschluss / keine
Schnittstelle** hat, wird **nicht erfunden**. Das ist das Signal, in Phase 1/2
zurückzuspringen und ein **alternatives Bauteil** zu suchen, das die Funktion
real herausführt (anderer Sensor mit aktivem Ausgang, Antrieb mit Rückmelde-
kontakt, Zähler mit Busmodul …). In der Restliste festhalten: „Funktion X am
Gerät Y nicht anschließbar → Alternative gesucht / Rückfrage an den Nutzer".

Erstelle je neuem/geändertem Katalogeintrag eine **Herleitungstabelle** – das ist
Pflicht und spart dem Nutzer die Gegenprüfarbeit. Sie muss die Kette
**elektrische Datenblattangabe → Anschluss-/Bauteilbedarf → Datenpunkt** sichtbar
machen, nicht nur das Ergebnis:

| Klemme / Anschluss lt. Datenblatt | Elektrische Angabe (Signalart, Spannung, Kontakt/Wechsler, Schutzklasse, VA) | DBACS-Zone (`klemm_l/f/s`, `steuer` …) | Datenpunkt (`dp_ai/ao/bi/bo`, `dp_fb_*` + Protokoll) | → Ableitung: welche Modellierungsregel greift und warum | Bauteil / Artikel-Nr. |
|---|---|---|---|---|---|

Die vorletzte Spalte ist der Kern: hier steht z. B. „aktives 0–10 V-Signal ⇒
`benoetigt_steuerspannung` (Regel 5)", „nur 1 Wechslerkontakt, aber Abschaltung
+ getrennte Meldung nötig ⇒ Koppelrelais 230 V (Regel 6)", „Schutzklasse III,
kein eigener Erdungsanschluss im Klemmenplan ⇒ keine PE-Klemme (Regel 8)",
„Motorstatus über RS485 ⇒ `dp_fb_bi` @ `modbus_rtu` als Override **auf der
Geräte-/Bauteilzeile** (Regel 12), keine physische Klemme, kein
Kommunikationsbauteil-Ratchet (Session-58-Systematik)".

Dazu:
- Die **Modellierungsregeln aus `CLAUDE.md`** anwenden und je Entscheidung
  benennen, welche Regel greift (Klemmzonen-Grundsatz, Steuerspannungs-Ratchet,
  Koppelrelais-Pattern, PE-Klemme nur bei eigener Erdungsklemme im Plan,
  kommunikative `dp_fb_*` statt physischer Platzierung …).
- **Namensregel** für den Auswahltext: `Text Bauteil → Messbereich →
  Versorgungsspannung → Zulassungen`.
- **Artikel-Referenz-Integrität**: `baugruppen_bauteile.artikel_nr` ist immer die
  echte Katalog-Artikelnummer, nie eine Typbezeichnung.
- Eine **Restliste offener Punkte** (unbestätigte Maße, fehlende Preise, nicht
  gefundene Klemmenpläne) – wandert später nach `CLAUDE.md` → „Offene Punkte".

### Phase 4 – Freigabe-Loop (HARTER STOPP)

Lege dem Nutzer vor:
- die vorgeschlagenen Katalogzeilen (Sheet, Spaltenwerte),
- die Herleitungstabelle(n),
- **je Fakt den Quell-Link**,
- die Restliste offener Punkte.

Dann **anhalten**. Nichts an `ga_komponenten.xlsx` ändern, bis der Nutzer anhand
der Links freigibt. Rückfragen des Nutzers einarbeiten, erneut vorlegen. Dieser
Stopp ist der wichtigste Teil des Skills (Memory
`feedback_planungsfabrikat_workflow`).

### Phase 5 – Eintrag in ga_komponenten.xlsx

Erst nach Freigabe. Siehe `references/excel-pipeline.md` für Details. Kurz:
1. **Lock prüfen**: `~$ga_komponenten.xlsx` darf nicht existieren (Excel zu).
2. **Backup** nach `C:\Users\SMI\Backups\dbacs\excel\` vor strukturellen
   Änderungen (neue Sheets, umbenannte Spalten) – die Datei ist nicht
   git-versioniert, sonst kein Sicherheitsnetz.
3. **Writer-Skript** nach `scripts/xlsx_write_template.py` in den Projekt-
   Scratchpad kopieren, anpassen, per WSL-`python3`/openpyxl ausführen. Neue
   Zeilen anhängen, bestehende `quelle_hinweis`-Texte **additiv** ergänzen
   (`[Preisrecherche MM/YYYY] …`), nie überschreiben.

### Phase 6 – Export nach JSON

```
MSYS_NO_PATHCONV=1 wsl bash -lc "cd /mnt/c/users/smi/cowork/dbacs/data && python3 xlsx_to_json.py"
```

Exportiert alle 9 JSON-Dateien. Danach die Zähl-Zeile aus der Skriptausgabe
prüfen (baugruppen / einzelbauteile / feldgeraete) und gegen die Erwartung nach
dem Eintrag abgleichen.

### Phase 7 – Browser-Verifikation

Dev-Server starten (`preview_start` mit `name: "dbacs-static"`), dann je nach
Änderung Modul 4 / 5 / 7 öffnen und prüfen (Checkliste in
`references/excel-pipeline.md`): richtige Dropdown-Gruppierung im passenden
Gewerke-Tab, Stückliste, DDC-Statistik, Steuerspannungs- und Kommunikations-
bauteil-Automatik, kommunikative Datenpunkte, **keine Konsolenfehler**. Ein
Screenshot des relevanten Zustands an den Nutzer.

### Abschluss

- `CLAUDE.md` → „Offene Punkte" und `docs/revison_session.md` fortschreiben
  (neue Kataloginhalte, verbleibende Restliste, absolute Daten statt „heute").
- Commit/Push passieren automatisch über den Stop-Hook – nicht manuell committen,
  nicht danach fragen (Memory `feedback_stop_hook_commit`).

---

## Leitplanken

- **Nicht raten.** Unbelegte Maße/Preise/Klemmen sind offene Punkte, keine
  Schätzwerte. Lieber eine Zeile mehr in der Restliste.
- **Excel ist die einzige Schreibstelle.** JSON nie von Hand editieren.
- **Fachregeln kommen aus `CLAUDE.md`**, nicht aus dem Gedächtnis – bei jeder
  neuen Baugruppe den dortigen Klemmenplan-Hinweis (Regel 8: Suche nach
  „ground"/„Erdung"/„Schutzleiter" im Originaldatenblatt) tatsächlich ausführen.
- **Herleitungstabelle immer mitliefern** – auch bei scheinbar simplen Einträgen.
