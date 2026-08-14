# DBACS – Claude-Projektkontext

## Session-Start-Protokoll

**Beim Start jeder Sitzung in dieser Reihenfolge ausführen:**
1. `git log --oneline -5` – prüfen ob seit letzter Sitzung neue Commits über VS Code eingecheckt wurden
2. `git status` – prüfen ob uncommittete Änderungen vorliegen
3. `docs/revison_session.md` lesen – aktueller Projektstand, offene Punkte, gesperrte Entscheidungen
4. Bei Arbeit an Modul 1: `modules/modul-01-schaltschrank/index.html` – JS beginnt nach dem HTML-Markup (Suche nach `<script>`)
5. Bei Arbeit an Modul 2: `modules/modul-02-standschrank/index.html` – gleiche Struktur wie Modul 1
6. Bei Arbeit an Modul 3: `modules/modul-03-architektur/index.html` – kein SVG, nur Berechnungstabelle; Daten kommen via localStorage aus Modul 1/2

**Hinweis:** Commits erfolgen in der Regel über VS Code, nicht über Claude. Der letzte Commit-Stand ist daher maßgeblich für den tatsächlichen Projektstand – nicht der Dokumentationsstand in `revison_session.md`.

---

## Offene Punkte (Stand Session 51 – vor Beginn der nächsten Sitzung lesen)

Keine offenen Punkte – alle Session-51-Themen implementiert UND im Browser
verifiziert. Details siehe „Modul 4 – Session 51 (komprimiert)" unter
„Formel-Referenz" weiter unten bzw. `docs/archiv/claude-md-modul4-sessions-35-51.md`
für den vollen Sitzungsverlauf.

---

## Projekt-Überblick

DBACS ist ein webbasiertes Planungstool für das Gewerk Gebäudeautomation, das Ingenieure bei der Schaltschrank-Dimensionierung in verschiedenen HOAI-Leistungsphasen unterstützt. Es läuft als statische GitHub Pages Anwendung – kein Server, kein Backend, kein Build-Step. Jedes Modul ist eine eigenständige HTML-Datei mit eingebettetem CSS und JavaScript.

**Live:** https://smicmics.github.io/dbacs/
**Repository:** https://github.com/smicmics/dbacs

---

## Dateistruktur

```
dbacs/
├── .gitignore
├── CLAUDE.md                                    diese Datei
├── index.html                                   Root-Redirect → web/index.html
├── .claude/
│   └── launch.json                              Dev-Server-Konfiguration (statisch, Port 8099)
├── web/
│   ├── index.html                               Startseite / Modulübersicht (Dark Theme)
│   └── assets/
│       ├── css/style.css                        Dark Theme Stylesheet
│       ├── js/main.js                           Scroll-Reveal + Nav-Highlighting
│       └── img/dbacs-logo.png                   DBACS Logo (Startseite + Modul-Header)
├── modules/
│   ├── modul-01-schaltschrank/index.html        h_ke-Rechner (Wandschrank) ✅
│   ├── modul-02-standschrank/index.html         h_ke-Rechner (Standschrank, Sockel) ✅
│   ├── modul-03-architektur/index.html          TE-Berechnung & Reihenkapazität ✅
│   ├── modul-04-innenaufbau/index.html          Baugruppen · Innenaufbau ✅
│   └── modul-07-stammdatenpflege/index.html     Artikeldaten-Katalog-Browser (rein lesend) ✅
├── drawings/
│   ├── wandschrank_frontansicht.html            Referenzzeichnung Wandschrank (nicht bearbeiten)
│   └── standschrank_frontansicht.html           Referenzzeichnung Standschrank (nicht bearbeiten)
├── data/
│   ├── ga_komponenten.xlsx                      Excel Source of Truth (lokal, nicht versioniert)
│   ├── kabel_nym_j.json                         Kabeldatenbank NYM-J (committed)
│   ├── wandschraenke.json                       Wandschrank-DB Rittal AX (committed)
│   ├── kabelzugschellen.json                    Kabelzugschellen-DB Icotek CCL (committed)
│   ├── standschraenke.json                      Standschrank-DB Rittal VX25 (committed)
│   ├── sockel.json                              Sockel-DB Rittal VX (committed)
│   ├── bodenbleche.json                         Bodenblech-DB Rittal VX (committed)
│   ├── einzelbauteile.json                      Modul-4-Bauteilkatalog (committed, seit Session 27 über Excel gepflegt)
│   ├── baugruppen.json                          Modul-4-Baugruppen-DB (committed, seit Session 27 über Excel gepflegt)
│   └── xlsx_to_json.py                          Konvertierungsskript Excel → JSON (9 Datensheets + 2 reine Referenz-Sheets `funktionsbereiche`/`zonen`, `einzelbauteile`/`baugruppen`+`baugruppen_bauteile`-Verknüpfungstabelle seit Session 27)
└── docs/
    ├── revison_session.md                       aktueller Revisionsstand ← immer zuerst lesen
    └── archiv/                                  ältere Session-Dokumentationen
```

---

## Deployment

| | |
|---|---|
| Repository | https://github.com/smicmics/dbacs |
| Branch | `main` |
| GitHub Pages | https://smicmics.github.io/dbacs/ |
| Modul 1 | https://smicmics.github.io/dbacs/modules/modul-01-schaltschrank/ |
| Modul 2 | https://smicmics.github.io/dbacs/modules/modul-02-standschrank/ |
| Modul 3 | https://smicmics.github.io/dbacs/modules/modul-03-architektur/ |
| Modul 4 | https://smicmics.github.io/dbacs/modules/modul-04-innenaufbau/ |
| Modul 7 | https://smicmics.github.io/dbacs/modules/modul-07-stammdatenpflege/ |
| Deploy-Trigger | `git push origin main` → GitHub Pages baut automatisch |

---

## Variablen-Konvention (modulübergreifend)

Diese Namen gelten verbindlich in allen Modulen (Tabellenspalten, JS-Variablen, SQLite-Felder):

| Variable | Bedeutung | Einheit |
|---|---|---|
| `b_gehaeuse_aussen_mm` | Schrank-Außenbreite | mm |
| `h_gehaeuse_aussen_mm` | Schrank-Außenhöhe | mm |
| `b_mplatte_mm` | Montageplatte Breite | mm |
| `h_mplatte_mm` | Montageplatte Höhe | mm |
| `b_mplatte_abstand_gehaeuse_iw_mm` | Seitl. Abstand MP–Gehäuseinnenwand | mm |
| `h_mplatte_abstand_gehaeuse_iw_mm` | Oberer Abstand MP–Gehäuseinnenwand | mm |
| `n_adern` | Anzahl Leiter im Kabel | – |
| `querschnitt_mm2` | Leiterquerschnitt | mm² |
| `d_max_kabel_ke_mm` | Max. Kabel-Außen-∅ in der KE-Zone (aus DB) | mm |
| `h_handling_ke_mm` | Freie Kabellänge nach PG (Festwert 15 mm) | mm |
| `h_kabel_bieg_mm` | Mindestbiegeradius (4 × d_max, VDE 0298-4) | mm |
| `h_zug_ke_mm` | Bügelschellen-Höhe aus DB (Icotek CCL, 0 wenn inaktiv) | mm |
| `h_handling_zug_ke_mm` | Freiraum nach Schelle bis Kanal/Gerät (Festwert 20 mm, 0 wenn inaktiv) | mm |
| `h_kanal_ke_mm` | Horizontaler Kabelkanal KE-Zone (0 wenn inaktiv) | mm |
| `h_ke_mm` | Kabeleinführungszone gesamt | mm |
| `h_mplatte_mbereich_wandschrank_mm` | Höhe Montagebereich auf der Montageplatte – Wandschrank | mm |
| `b_mplatte_mbereich_wandschrank_mm` | Breite Montagebereich auf der Montageplatte – Wandschrank (= b_mplatte_mm) | mm |
| `h_mplatte_mbereich_standschrank_mm` | Höhe Montagebereich auf der Montageplatte – Standschrank | mm |
| `b_mplatte_mbereich_standschrank_mm` | Breite Montagebereich auf der Montageplatte – Standschrank (= b_mplatte_mm) | mm |
| `h_sockel_mm` | Sockelhöhe Standschrank (0 wenn inaktiv) | mm |
| `h_schelle_mm` | Einbauhöhe Bügelschelle (Datenbankfeld in kabelzugschellen.json) | mm |
| `h_kabel_bieg_faktor` | Biegeradiusfaktor Festwert 4 (VDE 0298-4) | – |
| `schrank_typ` | Auswahl Wandschrank / Standschrank (Modul 3) | – |
| `te_breite_mm` | TE-Breite nach DIN 43880 (Festwert 18,0 mm – Hüllmaße Installationseinbaugeräte) | mm |
| `flaeche_mbereich_cm2` | Montagefläche Montagebereich | cm² |
| `flaeche_mbereich_m2` | Montagefläche Montagebereich | m² |
| `n_te` | Verfügbare Teileinheiten auf Montagebereich-Breite (ganze Zahl) | TE |

---

## Architekturregeln

Diese Regeln gelten für alle Module und werden nicht neu diskutiert:

- **Single-File HTML** pro Modul – CSS und JS eingebettet, keine externen Dateien; Datenbankdateien (JSON) sind zulässige externe Abhängigkeiten
- **Kein Framework** – kein React, Vue, Angular, kein npm, kein Build-Step
- **GitHub Pages kompatibel** – relative Pfade, kein Server-Backend, offline-fähig
- **Sprache** – UI-Texte und Dokumentation auf Deutsch
- **Datenhaltung** – Excel als Source of Truth → `data/xlsx_to_json.py` → JSON (committed) → `fetch()` im Browser
- **Entwickler-Workflow Daten:** Excel bearbeiten → in WSL: `cd /mnt/c/users/smi/cowork/dbacs/data && python3 xlsx_to_json.py` → exportiert alle 9 JSON-Dateien → alle committen
- **Seit Session 39: Claude pflegt `ga_komponenten.xlsx` direkt** (Nutzer-Entscheidung) – nicht mehr nur Recherche-Werte liefern, sondern selbst per Skript in die Excel-Datei schreiben. Vor jedem Schreibzugriff `~$ga_komponenten.xlsx`-Lockdatei prüfen (Excel muss geschlossen sein) UND vor strukturellen Änderungen (neue Sheets, Spalten-Umbenennungen) eine Kopie nach `C:\Users\SMI\Backups\dbacs\excel\` sichern – die Datei ist NICHT git-versioniert, es gibt sonst kein Sicherheitsnetz.
- **Excel nicht versioniert** – `data/*.xlsx` ist in `.gitignore`, nur JSON wird committed

---

## Code-Konventionen (aus Modul 01)

### Struktur jedes Moduls
```
1. HTML + CSS (eingebettet im <style>-Tag)
2. HTML-Markup (Eingabe-Panel links, Ausgabe-Panel rechts)
3. JavaScript:
   const C = {...}                // SVG-Farbpalette – zentral, nie hardcoded im SVG
   let KABEL_DB = []              // Kabeldatenbank, per fetch() geladen
   let WANDSCHRANK_DB = []        // Wandschrank-DB, per fetch() geladen (Modul 1)
   let STANDSCHRANK_DB = []       // Standschrank-DB, per fetch() geladen (Modul 2)
   let KABELZUGSCHELLEN_DB = []   // Kabelzugschellen-DB, per fetch() geladen
   let SOCKEL_DB = []             // Sockel-DB, per fetch() geladen (Modul 2)
   g(id)                          // DOM-Getter: +document.getElementById(id).value
   gs(id)                         // DOM-Getter String: document.getElementById(id).value
   _v(id, val)                    // DOM-Setter: document.getElementById(id).value = val
   lookupKabel()                  // Kabel-Lookup aus KABEL_DB nach n_adern + querschnitt
   loadPreset()                   // Schrank-Lookup aus DB per Dropdown-Index
   calculate()                    // Master-Orchestrator, aufgerufen bei oninput
   buildSVG(p)                    // SVG-String-Generator, bekommt Parameterobjekt p
   buildTable(p)                  // HTML-Tabellen-Generator, bekommt Parameterobjekt p
```

### Kommentarstil
```js
// ── Abschnittsname ────────────────────────────────────────────
```

### Datenfluss
```
oninput → calculate() → buildSVG(p)   → #svg-inner
                      → buildTable(p) → #results-area
```

### Schriftgrößen-Steuerung
Die drei Schriftgrößen sind Nutzereingaben (`fs_dim`, `fs_var`, `fs_zone`) und werden als `p.fs_*` an `buildSVG()` übergeben. Wert `0` blendet die gesamte Gruppe (Linien, Pfeile, Text) aus:

| Eingabefeld | ID | Standard Modul 1 | Standard Modul 2 | Steuert |
|---|---|---|---|---|
| Bemaßungstext | `fs_dim` | `7` | `5` | H =, B = Labels + Maßlinien |
| Bemaßungsvariable | `fs_var` | `6` | `5` | Zonenpfeile, h_ke-Klammer, Guide-Linien, PG-Label |
| Zonenbeschreibung | `fs_zone` | `7` | `5` | Kabeleinführungszone, Kabelkanal, Nutzfläche-Linie |

### Farbkodierung Ergebnistabelle + Formel (Modul 01)
Farben sind in Tabelle und Formelzeile immer identisch. h_zug und h_handling_zug werden immer farbig dargestellt (kein konditionelles Grau):

| Variable | Farbe | Hex |
|---|---|---|
| `h_handling_ke_mm` | Grün | `#2DBD8E` |
| `h_kabel_bieg_mm` | Orange | `#C8720E` |
| `h_zug_ke_mm` | Amber (immer) | `#D4A84B` |
| `h_handling_zug_ke_mm` | Teal (immer) | `#4BBECA` |
| `h_kanal_ke_mm` | Lila (aktiv) / Grau (inaktiv) | `#9A94E8` / `#9A9890` |
| `h_ke_mm` | Hell-Weiß (Ergebnis) | `#E0DED8` |
| `h_mplatte_mbereich_wandschrank_mm` | Hell-Blau (Ergebnis) | `#A8C4E8` |

SVG-Zonenrahmen (getrennt von Maßketten-Farben):

| Zone | Rahmenfarbe | C-Palette |
|---|---|---|
| h_zug_ke_mm | Amber `#D4A84B` | `C.zZ_stroke` |
| h_handling_zug_ke_mm | Teal `#4BBECA` | `C.zHZ_stroke` |

---

## SVG-Zeichnungskonventionen

| Eigenschaft | Wert |
|---|---|
| SVG-Höhe | `SH = 390 px` (fest) |
| Skalierung | `sc = SH / H_mm` |
| Zeichenfläche | `#FDFCF8` (Papier-Weiß) |
| UI-Hintergrund | `#1A1A18` (Dark Theme) |
| Maßketten Farbe | `#3366BB` |
| Maßketten Strich | `0.8 px` |
| Maßketten Schrift | Bemaßungstext `7 pt` · Bemaßungsvariable `6 pt` · Zonenbeschreibung `7 pt` · Innen-Labels `7 pt` |
| Maßkettentext Abstand | Baseline **2 px oberhalb** der Maßlinie; Maßlinie **16 px** vom Gehäuse (H-Maß: 2 px rechts von `hx`, Pfeil bei `hx+3`) |
| Gehäuselinien | `lw_s = Math.max(0.8, sc × 8)` px (proportional zum Maßstab) |
| Montageplatte Linie | `lw_mp = Math.max(0.4, sc × 4)` px (proportional zum Maßstab) |
| Kabeldarstellung | `4 px` |
| SVG-Erzeugung | dynamisch per JS – kein statisches SVG |
| PG-Verschraubungen | beide identisch (`pgBody` ohne `hasKabel`-Flag), Ausrichtung per `ke_pos` |
| Kabelstub | Länge **10 px** sichtbar past PG-Nase, gleich für KE oben und KE unten; Stub vor PG zeichnen (PG überdeckt Innenbereich) |
| Schriftgröße = 0 | blendet gesamte Gruppe aus (Linien + Pfeile + Text) |

---

## Formel-Referenz

### h_ke – Kabeleinführungszone

Reihenfolge ab Gehäuseinnenwand (fest, nicht ändern):
```
h_ke_mm = h_handling_ke_mm + h_kabel_bieg_mm + h_zug_ke_mm + h_handling_zug_ke_mm + h_kanal_ke_mm

h_kabel_bieg_mm      = 4 × d_max_kabel_ke_mm   (VDE 0298-4, fest verlegt)
h_zug_ke_mm          = h_schelle_mm aus kabelzugschellen.json (Lookup via d_max), 0 wenn inaktiv
h_handling_zug_ke_mm = 20 mm Festwert (Freiraum Schelle → Kanal/Gerät), 0 wenn inaktiv
```

| Variable | Wandschrank (Standard) |
|---|---|
| `h_handling_ke_mm` | 15 mm (Festwert) |
| `h_kabel_bieg_mm` | 4 × d_max (dynamisch) |
| `h_zug_ke_mm` | 0 mm (Nein) oder aus DB (Ja) |
| `h_handling_zug_ke_mm` | 0 mm (Nein) oder 20 mm (Ja) |
| `h_kanal_ke_mm` | 0 mm (Nein) oder Eingabe (Ja, Standard 60 mm) |

### h_mplatte_mbereich_wandschrank_mm – Montagebereich auf Montageplatte

```
h_mplatte_mbereich_wandschrank_mm = h_gehaeuse_aussen_mm - h_ke_mm - (h_gehaeuse_aussen_mm - h_mplatte_mm) / 2
```

Beschreibt den nach Abzug der Kabeleinführungszone verbleibenden Höhenbereich auf der Montageplatte für die Installation weiterer Schaltschrankkomponenten. Wird in SVG-Zeichnung als Maßlinie (KE-Ende → MP-Ende) und in eigener hervorgehobener Ergebniszeile angezeigt.

---

### Modul 4 – Session 51 (komprimiert)
Vollständiger Sitzungsverlauf (Nutzer-Funde, Root-Cause-Analysen,
Verifizierungsdetails) archiviert in
`docs/archiv/claude-md-modul4-sessions-35-51.md`. Ergebnisse:

- **Klemmen-Gruppen-Split-Verdacht verworfen** (kein echter Bug): der
  gemeldete Fall (Wandschrank, 2 Felder) ist über die echte UI nicht
  erreichbar – `calculateZones()` erzwingt bei Wandschrank immer
  `zone_modus='1feld'`.
- **`idxLabelSVG()`-Fix:** Positionsnummern (`#idx`) verschwanden komplett
  (statt kleiner zu werden), sobald sie bei gleicher Blockgröße mehr Ziffern
  brauchten als beim ersten Berechnungslauf – Schriftgröße wird jetzt aus
  Box- UND Textlänge berechnet, mit garantierter Rückfallebene (nie mehr
  leer).
- **Baugruppen-Dropdown-Sortierung:** `BG_SORT_PRIORITY` (reine
  Anzeigesortierung, unabhängig von der DIN-276-`id`) – AI → AO → AO+LVB →
  BI → BO → BO+LVB → Rest.
- **Farbe automatisch ergänzter DDC-Geräte** in der Zeichnung: `#D8D5CE`
  (echtes Hellgrau, kontrastreich auf dem Zeichenpapier `#FDFCF8` –
  Zwischenstand `#9A9890`/`--tx2` war ein UI-Grauton, auf Papier weiterhin zu
  dunkel). Farbpunkt in der Belegungsliste bewusst unverändert.
- **Onboard-Kapazität der Kompaktstationen `PXC4.E16.A`/`PXC5.E24.A`
  berücksichtigt:** `buildQueues()` entschied bisher über externe TX-I/O-
  Module BEVOR die gewählte CPU aufgelöst war – deren Onboard-Kapazität
  konnte nie angerechnet werden. CPU-Auflösung jetzt vor
  `computeDdcAutoModules()`; `PXC4.E16.A` bekam `dp_ai=12`/`dp_ao=12`,
  `PXC5.E24.A` `dp_ai=16`/`dp_ao=16` (analog zur `TXM1.8U`-Konvention: nur
  AI/AO, bewusst kein `dp_bi`/`dp_bo`-Zuschlag aus dem universellen Pool).
  Nur die ERSTE CPU-Gruppe bekommt den Onboard-Zuschlag (konservativ) – die
  bestehende Überlauf-Logik (`max_ea_module`, eigenes Netzteil+Sicherung je
  Zusatzgruppe, Session 50) bleibt unverändert und wurde erneut end-to-end
  bestätigt.
- **Klemmenauswahl-Varianten (Standard/Doppelstock/Trennklemme/
  DS-Trennklemme):** Radiogruppe im Block „Grund- & Reserveangaben"
  (`localStorage['m04_klemmen_variante']`). Katalog-Verkettung über
  `trennklemme_variante_artikel_nr`/`doppelstock_variante_artikel_nr` auf
  der Standardklemme `3209510` (`resolveKlemmeArtikel()`/
  `resolveBaugruppenBauteile()` – MUSS identisch in `buildQueues()` UND
  `aggregateStueckliste()` verwendet werden, sonst laufen Zeichnung und
  Stückliste auseinander). Referenzklemme aller 6 DDC-Baugruppen von blau
  (`3209523`) auf grau (`3209510`) geändert.
- **Doppelstockklemmen-Kapazität korrigiert:** eine Doppelstockklemme
  (4 Anschlüsse) teilt sich jetzt korrekt 2 Baugruppen-Instanzen (vorher nur
  2 von 4 Anschlüssen genutzt) – Instanz-Schleife läuft bei aktiver
  Doppelstock-Variante in Zweierschritten, `aggregateStueckliste()` zählt
  `Math.ceil(menge/2)` statt `menge`.
- **Stückliste zeigte automatisch ergänzte DDC-Module nicht** (CPU/
  Netzteil/Sicherung/E-A-Module) – neue globale `letzteDdcAuto` +
  `ddcAutoZone(eb)`-Helper (Zone NICHT über `bauteil_typ` raten: die
  Sicherung trägt katalogseitig `'lss'`, nicht `'sicherung'`).
- **CPU-Typ-Dropdown** (`#cpu_typ_override`, Statistikfeld) – manuelle Wahl
  hat Vorrang vor `auto_ea_cpu`. Summenanzeige „Physikalisch/Kommunikativ
  gesamt" rechts daneben.
- **Klemmleisten: reale mm-Breite statt TE-Rundung** – `eb.te_breite =
  ceil(b_mm/18)` rundete eine 5,2mm-Klemme auf eine volle 18mm-TE-Einheit
  auf (korrekt für Hutschienengeräte in `leist`/`steuer`, falsch für
  Reihenklemmen). Fix beschränkt auf `placeInKlemmRow()`+
  `redistributeKlemmBands()` (Geräte tragen jetzt zusätzlich `b_mm`),
  `placeInBands()` bewusst unverändert TE-basiert.
- **Eingabeleiste kompakter** (CSS, `.eingabeleiste`-Höhe −45px zugunsten
  der Schranksicht) – Hinweistext inline, Variablennamen unter Grund-/
  Reserve-Feldern per CSS ausgeblendet, CPU-Typ-Feld `position:absolute`.
- **WSL-localhost-Relay-Ausfall** (Infrastruktur, kein Projekt-Bug): Browser-
  Preview erreicht `localhost:8099` nicht, obwohl der Server nachweislich
  läuft (WSL-VM-IP direkt erreichbar) → WSL2-„localhost-Relay" hängt,
  betrifft jeden Port. **Fix: `wsl --shutdown`** (vorher beim Nutzer
  nachfragen, beendet alle WSL-Prozesse).

## Gesperrte Entscheidungen

Diese Punkte wurden bereits ausführlich diskutiert und entschieden – nicht neu aufgreifen. **Archiv-Hinweis (14.08.2026):** ausführliche Session-Protokolle werden zu kompakten Ergebnis-Zusammenfassungen eingedampft (Volltext inkl. Nutzer-Funden/verworfenen Zwischenständen/Verifizierungsdetails liegt in `docs/archiv/claude-md-modul4-sessions-20-29.md`, `docs/archiv/claude-md-modul4-sessions-30-34.md` und `docs/archiv/claude-md-modul4-sessions-35-51.md`) – Grund: `CLAUDE.md` wird bei jeder Sitzung vollständig geladen, unabhängig vom Umfang der Aufgabe. Bei künftigen sehr langen Session-Nachträgen ebenso verfahren: verbindliche Regel kompakt in `CLAUDE.md`, ausführliche Vorgeschichte ins Archiv.

- `h_handling_ke` startet an der **Schaltschrankinnenwand** (nicht an MP-Oberkante)
- Zonenreihenfolge ab Gehäusewand: **handling → bieg → zug → handling_zug → kanal** (fest, nicht ändern)
- `h_zug_ke_mm` ist dynamisch via `kabelzugschellen.json` (Lookup nach d_max) – Ja/Nein schaltbar
- `h_handling_zug_ke_mm = 20 mm` Festwert – nur aktiv wenn Zugentlastung = Ja
- `h_kanal_ke_mm` Ja/Nein schaltbar; bei Nein = 0, Eingabefeld disabled
- **B-Maßlinie positionsabhängig:** unten bei KE oben, oben bei KE unten
- `b_mplatte_abstand_gehaeuse_iw_mm` nur in der Ergebnistabelle, nicht in der SVG-Zeichnung
- Alle Maßketten-Pfeile/-Labels einheitlich blau `#3366BB` – Zonenrahmen-Farben davon getrennt (`C.zZ_stroke`, `C.zHZ_stroke`)
- `h_zug_ke_mm` und `h_handling_zug_ke_mm` immer in Amber/Teal (kein konditionelles Grau)
- PG-Verschraubungen bündig auf Gehäuse, kein Luftabstand
- Kabelstub-Richtung: nach oben bei KE oben, nach unten bei KE unten
- Biegeradiusfaktor 4× (nicht 6×, das gilt nur für flexible Leitungen)
- Schriftgrößen sind Nutzereingaben, keine Konstanten – Standardwerte je Modul verschieden (Modul 1: 7/6/7; Modul 2: 5/5/5)
- Alle SVG-Variablenlabels tragen vollständige `_mm`-Suffixe
- `h_mplatte_mbereich_wandschrank_mm`-Maßlinie liegt im `if (p.fs_var > 0)`-Block
- Zonenbeschriftungen linksbündig bei `zoneLblX = bxo + 10` (10 px rechts vom Kabel); ▼/▲ Nutzfläche zentriert bei `mx+mw/2`
- Teilmaß-Labels vertikal zentriert via `dominant-baseline="middle"` – Ausnahme: `h_handling_ke_mm` (zu kleine Zone, Sonderpositionierung ±0,5 px je KE-Richtung)
- `tx()`-Funktion unterstützt `db`-Option für `dominant-baseline`
- SVG vollständig maßstäblich: `sc = SH / H_mm` – Schrank, MP, KE-Zonen, Sockel alle mit gleichem Faktor skaliert

### Modul 3 – TE-Berechnung (gesperrt)
- Datenübernahme ausschließlich via localStorage (kein direkter Modulaufruf):
  - Modul 1 schreibt: `m01_b/h_mplatte_mbereich_wandschrank_mm`, `m01_ke_pos`
  - Modul 2 schreibt: `m02_b/h_mplatte_mbereich_standschrank_mm`, `m02_ke_pos`
  - Modul 3 liest je nach `schrank_typ`-Auswahl den passenden Key
- `schrank_typ` wird **nicht** aus localStorage wiederhergestellt – jeder Aufruf startet mit leerem Dropdown „— bitte wählen —"
- Bei leerem `schrank_typ`: Ergebnisbereich zeigt nur Hinweistext, keine Tabelle / Formelbox
- `typLabel` in Ergebnistabelle ohne Modulangabe: nur „Wandschrank" oder „Standschrank"
- `te_breite_mm = 17,5 mm` Festwert nach DIN EN 60715
- `n_te = Math.floor(b / 17.5)` – immer als ganze Zahl (abgerundet)
- Formelbox: Eingabewerte b und h mit Einheit mm dargestellt, z. B. `⌊ 499 mm / 17,5 mm ⌋`
- Farbkodierung Ergebnisvariablen:
  - `flaeche_mbereich_cm2` → Grün `#2DBD8E`
  - `flaeche_mbereich_m2`  → Lila `#9A94E8`
  - `n_te`                 → Hellblau `#A8C4E8`
  - Eingaben (b, h)        → Sekundär `#9A9890`
- Variablennamen in Seitenleiste und Tabelle wechseln dynamisch je nach Typ (`_wandschrank_mm` / `_standschrank_mm`)
- Hint-Text bei fehlendem localStorage-Wert: Link zur Startseite
- `class="copyright-line"` – Copyright-Absatz im Druck ausgeblendet (`display:none !important`)

### Modul 4 – Platzierungs-Engine: Entstehungsgeschichte (Sessions 20–29, komprimiert)
Vollständiger Sitzungsverlauf (Nutzer-Funde, verworfene Zwischenlösungen, Verifizierungsdetails) archiviert in `docs/archiv/claude-md-modul4-sessions-20-29.md`. Aktuell gültiger Funktionsstand:

- **8 Platzierungszonen:** `klemm_e` (Einspeiseklemmen), `uss` (ÜSS+Vorsicherung), `evert` (Energieverteilung), `leist`/`leist_ext` (Leistungsbaugruppe), `steuer` (Steuerbaugruppe), `klemm_l`/`klemm_f`/`klemm_s` (Abgänge Leistung/Feldgeräte/Sensoren). Zone kommt aus `eb.zone` (Katalog-Default), optional pro Baugruppen-Bauteil per `bt.zone` überschrieben.
- **Zwei Platzierungsmodelle, nicht austauschbar:** `placeInBands()` (Kanal(40mm)+Klemmraum-Modell für Mehrreihen-Zonen: `leist`, `steuer`, sowie `evert` nur mit Schienensystem) und `placeInKlemmRow()` (1-Reihen-Modell, Breite statt Höhe als Kapazität: `klemm_e`, `uss`, `klemm_l`, `klemm_f`, `klemm_s`, `evert` ohne Schienensystem). Grund: Modul 3 hat diese Zonen bereits exakt bemessen, ein zusätzliches Kanal/Klemmraum-Layer würde sie sprengen. `placeInKlemmRow()` prüft Höhe UND Breite – zu hohe Bauteile werden übersprungen statt verzerrt platziert.
- **Zwei Belegungs-Eintragstypen:** `{typ:'baugruppe',bg_id,menge,ci}` und `{typ:'einzel',artikel_nr,menge,ci}`. Indizierung pro Zone (`idx`), sichtbar im SVG-Tooltip und in der Stückliste (`formatIdxList()`, komprimiert zu Bereichen wie `#3–#5, #7`). Stückliste aggregiert nach `(artikel_nr, Zone)`.
- **`ZONE_COLORS`** (zentrale Konstante, identisch in Modul 3+4 – einzige Quelle für Zonenfarben):
  ```
  klemm_e:'#EBDBA0'  uss:'#D8A916'   evert:'#C8720E'  leist:'#C84E2E'  steuer:'#4BBECA'
  klemm_l:'#2DBD8E'  klemm_f:'#9A94E8'  klemm_s:'#C14FA0'
  ```
- **Zonen-Legende** (`buildLegend()`, unter der Schranksicht) + sichtbare Bauteil-Nummer (`#idx`) auf jedem Block. Zonentext im SVG auf dem Bildschirm ausgeblendet (Legende erklärt Farbe→Zone bereits), im Druck weiterhin sichtbar (`@media print`).
- **Verdrahtungskanal-Muster (`kanalPending`):** kein Kanal vor der ersten Reihe einer Zone (nutzt den bereits vorhandenen festen M3-Kanal), genau ein Kanal zwischen allen Folgereihen (auch bandübergreifend), ein abschließender Kanal nach der letzten Reihe nur wenn der Rest der Zone noch Kanal+eine weitere Reihe fassen würde.
- **`redistributeKlemmBands(bandsAll, queues, reservePct)`:** `klemm_l`/`klemm_f`/`klemm_s` teilen sich eine gemeinsame, konstante Gesamtbreite (Summe der M3-Originalbänder). Jede Zone bekommt mindestens `Bedarf/(1-reservePct)`; reicht die Gesamtbreite, wird der Rest proportional zum M3-Originalverhältnis verteilt. `reserve_pct`-Eingabefeld (Default 20%, gilt schrankweit außer `klemm_e`); weiche Warnung (`#reserve-warn`) wenn die Reserve trotz Umverteilung nicht erreichbar ist – getrennt vom harten Overflow-„!".
- **Erzwungener Zeilenumbruch („neue Reihe"):** nur wirksam für Zonen aus `REIHEN_ZONEN` (`leist`/`steuer` – Reihen-Konzept), Checkbox bei allen anderen Zonen deaktiviert/wirkungslos.
- **Funktionsbereich-Taxonomie** (Session 24, seither durch die DIN-276-Migration Session 37/38 abgelöst – siehe dort für den aktuellen Stand).
- **Excel-Pipeline seit Session 27** auch für `einzelbauteile`/`baugruppen` (vorher Sonderfall, direkt als JSON angelegt). **Planungsfabrikat Klemmen: Phoenix Contact** – UT-Reihe (Schraubanschluss) für Einspeisung, PT-Reihe (Push-in) für alle drei Abgangs-Klemmenzonen, Zonen-Zuordnung über den bestehenden Baugruppen-Override-Mechanismus.

### Modul 4 – Baugruppen-Neuaufbau, Feldtyp-System, DDC-Automation (Sessions 37–50, komprimiert)
Vollständiger Sitzungsverlauf archiviert in
`docs/archiv/claude-md-modul4-sessions-35-51.md`. Aktuell gültiger
Funktionsstand:

- **Session 37/38 – Baugruppen-ID-Schema auf DIN-276 umgestellt:**
  `id`-Schema `<3-stelliger DIN-276-Gewerke-Code>_<6-stellig je Gruppe>`
  (z. B. `480_000001`), `gewerk` trägt jetzt den numerischen Code statt
  Kurzname. Modul 4 auf 11 DIN-276-Tabs umgestellt (`filterBaugruppen()`
  matcht auf `b.funktionsbereich`, NICHT `b.gewerk`); alter `schaltschrank`-
  Tab entfällt, geht in `automation` (480) auf; `450`/„netzwerk" deckt auch
  Sicherheitstechnik (Brandmelde-/Gefahrenmeldeanlagen) mit ab.
- **Session 39 – Excel-Konsistenzpflege:** 4 Datenbanken (`standschraenke`,
  `sockel`, `bodenbleche`, `reiheneinbaugeraete`) waren von der
  Excel-Pipeline abgekoppelt (Sheets fehlten in `ga_komponenten.xlsx`,
  nur noch aus JSON pflegbar) – aus JSON wiederhergestellt. Feldnamen auf
  Excel-Seite vereinheitlicht (`bestellnummer`→`artikel_nr`,
  `preis_stueckpreis_eur`→`preis_stueck_eur`; JSON-Ausgabeschlüssel bewusst
  unverändert, nur `xlsx_to_json.py`s Leseseite angepasst).
- **Session 40 – Katalogbereinigung:** `bauteil_typ` ist Pflichtfeld
  (steuert Kurzlabel + DDC-Kapazität/Bedarf-Unterscheidung). `kategorie` ≠
  `zone` – `kategorie` ist eine rein optische Dropdown-Gruppierung;
  Bauteile OHNE `kategorie` fehlen komplett im Modul-4-Dropdown (nicht nur
  ungruppiert!). `reiheneinbaugeraete`-Sheet (nie von einem Modul geladen,
  unsichere/falsche Session-20-Altdaten) komplett gelöscht. **Baugruppen
  komplett gelöscht** – bewusster Neuaufbau von Grund auf, nachdem der
  Einzelbauteile-Katalog sauber ist.
- **Session 41 – Siemens Desigo PX Architektur verstanden:** Ebene 1 = CPU
  (`PXC`-Serie, KEINE eigenen Anschlussklemmen), Ebene 2 = TX-I/O-Module
  (`TXM1.x`, einheitliches 64×77,5mm-Gehäuse). `PXA30-x` war fälschlich als
  I/O-Quelle katalogisiert (tatsächlich Kommunikations-/HMI-Zusatzkarte) –
  gelöscht. LVB = „Lokale Vorrangbedienebene" (Wippenschalter Hand/Auto je
  Kanal, `-M`/`-ML`-Suffix). Neue Felder `feldbus_protokoll`,
  `lvb_integriert`; `bauteil_typ:'ddc_cpu'` getrennt von `ddc_io` eingeführt.
  **DDC-Aufschaltung physikalisch/kommunikativ je Bauteil:** getrennte
  Checkbox+Protokoll-Auswahl, `PHYS_DP_TYPES`/`FB_DP_TYPES` als getrennte
  Pools, `isDdcSupplyTyp()`-Helper. Schütz-Zubehör: Hilfsschalterblock als
  automatische Grundausstattung jedes Schützes (`zubehoer_artikel_nr` +
  `syncZubehoer()`); neues Feld `keine_platzierung_mp` (Bauteil ohne eigenen
  Montageplatten-Platzbedarf, z. B. aufgesteckt – bleibt in der Stückliste,
  aber nicht in der Zeichnung). 13 Schütze 24V/230V AC über den gesamten
  Leistungsbereich ergänzt. LVB-Relais: **Metz Connect** als bewusste
  Ausnahme vom Phoenix-Contact-Planungsfabrikat (Phoenix deckt keine echte
  LVB-Funktion ab, nur einfache Koppelrelais). Mehrere Layout-Iterationen
  der Eingabeleiste (3-Blöcke-Layout, Statistik spaltengenau via CSS-Grid
  `display:contents`, Datenpunkttyp-Farbschema `--dp-ai/-ao/-bi/-bo`).
- **Session 42/43 – Zonen-/Kategorie-Korrekturen, Türbauteile:** neue Zone
  `tuer` („Fronttafel/Tür" – KEIN Eintrag in `ALLE_ZONEN`/`ZONE_COLORS`, hat
  keine physische Platzierung/Kapazität, eigener Filter-Chip). Neue
  Kategorie „Fronttafel-/Türeinbau", nutzt das bestehende
  `keine_platzierung_mp`-Feld.
- **Session 44 – Mehrfachzonen für Bauteile:** `einzelbauteile.zone` ist
  jetzt immer ein Array (erster Eintrag = Default), `bt.zone`
  (Baugruppen-Override) bleibt einzelner String. **Bug gefunden+gefixt:**
  Zone galt zunächst item-weit statt pro Hinzufüge-Batch – `zone` wurde Teil
  jedes `batches`-Eintrags (analog `forced`).
- **Session 45/46 – Katalogerweiterung:** 14+7 neue Einträge für HLS/
  Elektro/Sanitär/Sicherheitstechnik (Frequenzumrichter, Zeitrelais,
  Steckdose, Wahlschalter/Not-Halt, FI-Schutzschalter, Netzwerk-Switch,
  Wischrelais, Störquittiertaster, M-Bus-Pegelwandler, Messgeräte/
  Energiezähler). Session-43-Entscheidung „Signalleuchten→leist" in
  Session 46 wieder auf `tuer` zurückgedreht.
- **Session 47 – Türansicht neben Innenansicht:** Türmaße = echte
  Gehäuse-Außenmaße (`m01_B/H`/`m02_B/H`, NICHT der kleinere
  Montagebereich). 5 ergonomische Höhen-Bänder (`TUER_BAND_*`, gestützt
  durch DIN EN 60204-1/DIN 18040), `tuerBand(eb)`/`buildTuerAnsicht()`.
- **Session 48 (größtes Einzelthema) – Mehrfeld-Schaltschränke:** 5
  Feldtypen A–E (`FELDTYP_ZONEN`), `FELDPLAN` je `zone_modus` (1feld/
  je_feld/getrennt_els/einsp_misch), `buildLayoutForFeldtyp()` als
  generische Zeilen-Transformation. **Wandschrank-Sperre:**
  `schrank_typ==='wandschrank'` erzwingt IMMER effektiv `zone_modus='1feld'`
  (`getEffektiveZoneModus()`, identisch in Modul 3 UND 4). `placeInBands()`/
  `placeInKlemmRow()` bekamen `startIdx`+`leftoverDevs`+`nextIdx` für die
  Feld-zu-Feld-Kaskade, `calculateFelder()`-Orchestrator (demand-getriebene
  Folgefelder, `MAX_FELDER=20`-Deckel gegen Endlosschleifen). Türbauteile
  bekamen expliziten Feld-Bezug. `klemm_l` gehört NICHT ins reine
  Einspeisefeld (Typ C, nur wenn im selben Feld auch `leist` existiert).
  Feld-zu-Feld-Maßstab-Bug in Modul 4 gefixt (erstes Feld wurde mit
  falscher Breite gemessen, da das Wrap-Layout beim Messen noch
  unvollständig war – Fix: erst ALLE Wrap-Container anlegen, DANN messen).
- **Session 49 – Baugruppen-Zusammenhalt über Zonen hinweg:**
  `bgInstanceQueue` (Reservierung-vor-Commit-Modell),
  `platziereBaugruppenFuerFeld()` – Zusammenhalt gilt pro
  (Instanz × Feldtyp), NICHT für die ganze Instanz (sonst könnten
  baugruppenübergreifende Feldtyp-Kombinationen wie Leistungsfeld +
  Steuerungsfeld nie gemeinsam platziert werden). Erste
  Automations-Baugruppen (`480_000001` ff., „Reserve"-Datenpunkte für DDC-
  Anschlüsse ohne bekanntes Feldgerät): DDC-Datenpunktbedarf über
  `baugruppen_bauteile.dp_ai/ao/bi/bo`-Override statt am Katalogartikel
  selbst (eine Klemme trägt sonst nie DDC-Bezug). Automatische
  CPU-Ergänzung, sobald ein E/A-Modul gesetzt, aber keine CPU vorhanden ist.
  BI/BO-Zonenkorrektur (beide → `klemm_f`; `klemm_s` nur für analoge
  Sensoren). TXM1.8U-Kapazitätslücke geschlossen (`dp_ai=8`/`dp_ao=8`),
  dabei Unter-Versorgungs-Bug in `computeDdcAutoModules()` gefixt
  (Cross-Typ-Abzug nur noch für den GERADE bearbeiteten Typ, sonst hätte
  ein Mehrzweckmodul bei gleichzeitigem AI+AO-Bedarf zu wenige Käufe
  vorschlagen können). Jede Reserve-Baugruppe trägt 2 Klemmen (Signal +
  Referenz), nicht nur 1.
- **Session 50 – CPU-Katalog korrigiert + Automationsgruppen-Logik:**
  `PXC4.E16` (fälschlich mit Onboard-E/A katalogisiert) → `PXC7.E400.A`
  (echte modulare Variante, 0 Onboard-E/A) korrigiert – widersprach sonst
  dem Prinzip „Verbrauch entsteht ausschließlich an TXM-Modulen". Alle 3
  Desigo-PX-CPU-Typen aufgenommen (`PXC7.E400.A` modular + `PXC4.E16.A`/
  `PXC5.E24.A` kompakt), `auto_ea_cpu`-Flag steuert, welche CPU die
  Auto-Ergänzung nutzt. **Automationsstations-Gruppen:** Netzteil→CPU→
  E/A-Module lückenlos auf einer Hutschienenreihe, `max_ea_module`-
  Obergrenze je CPU löst eine komplett neue Gruppe aus (eigenes Netzteil +
  eigene Sicherung, `groupStart`-Flag erzwingt frische Reihe). Manueller
  „↺ Zurücksetzen"-Button für die DDC-Watermark (Ratchet-Mechanismus,
  Session 28e: einmal ergänzte Auto-Module sinken nie von selbst).

### Modul 7 – Stammdatenpflege (Sessions 35/36, komprimiert)
Vollständiger Sitzungsverlauf archiviert in
`docs/archiv/claude-md-modul4-sessions-35-51.md`.

- Neues Modul `modules/modul-07-stammdatenpflege/index.html` – bewusst
  **rein lesend** (kein Editor, Excel bleibt einzige Schreibstelle).
  Katalog-Browser (Einzelbauteile/Baugruppen) + Datenqualitäts-Leiste
  (`computeDataQuality()`: ungeprüfte Einträge, fehlender Preis, verwaiste
  `artikel_nr`-Referenzen) + Verwendungsnachweis (`USAGE_MAP`,
  Artikel-Nr. → referenzierende Baugruppen).
- **„📋 Liste kopieren"-Button** (`copyList()`): kopiert die aktuell
  gefilterte Liste als Text in die Zwischenablage – Standard-Workflow für
  Katalogpflege seither: Nutzer filtert (z. B. „Fehlender Preis"), kopiert,
  fügt im Chat ein, Claude recherchiert und trägt Werte direkt in
  `ga_komponenten.xlsx` ein, `xlsx_to_json.py` neu ausführen.

### Modul 4 – Belegungshistorie, Zonenfilter, Zentrierung (Sessions 30–34, komprimiert)
Vollständiger Sitzungsverlauf archiviert in `docs/archiv/claude-md-modul4-sessions-30-34.md`. Aktuell gültiger Funktionsstand:

- **`batches`-Modell (final, Session 30):** jeder Belegungseintrag trägt `batches:[{n,forced},...]` (chronologischer Stapel, ältester zuerst). `addEinzelbauteil()` hängt an (`pushBatch()`, verschmilzt mit dem letzten Batch bei gleichem `forced`-Status), `removeEinzelbauteilQty()` reduziert echtes LIFO – immer zuerst der zuletzt hinzugefügte Batch, unabhängig davon ob normal oder erzwungen. `item.menge` wird stets als Summe aller `batch.n` neu berechnet (keine Drift möglich). Ersetzt die verworfenen Vorläufer-Modelle `rowBreak`-Boolean (Session 28g/28h) und `forcedMenge`-Zähler (Session 28i) – alte Einträge werden beim Zugriff transparent migriert (`getBatches()`).
- **`consolidateBelegung()`:** fasst beim Laden sowie am Ende von `addBaugruppe()`/`addEinzelbauteil()` alle Einträge mit gleichem Schlüssel zu genau einem zusammen (Selbstheilung fragmentierter Alt-Daten aus früheren Modellgenerationen).
- **Vertikale Zentrierung (Session 31):** Bauteile in Leistung/Steuerung/Energieverteilung-Reihen werden wie Klemmenzeilen auf die Reihenmitte zentriert (`by0` in `buildSVG()`) – rein optisch, kein Effekt auf Platzbedarf/Platzierungslogik.
- **Zonen-Filter Einzelbauteil-Dropdown (Session 33, final):** die 8 `.fs-mini`-Felder im Füllstand-Streifen sind selbst klickbar (`setEinzelZone()`), plus ein 9. „Alle"-Feld – ersetzt die in Session 32 zuerst gebauten separaten `.zone-tab`-Buttons vollständig.
- **Offene, zurückgestellte Positionierungs-Themen (Session 34, weiterhin unentschieden):**
  1. Gerichtete Mindestabstände zu Nachbarbauteilen nach Herstellerangabe (Wärmeabfuhr) – DBACS kennt aktuell nur `h_mm`/`b_mm`/`te_breite`, keine Abstandsregeln.
  2. Positionierungslogik für hintereinander zu platzierende Bauteile (z. B. DDC-Module) – Verhältnis zur bestehenden Reihen-Logik noch ungeklärt.
  3. Anordnung von Bauteilen innerhalb einer Baugruppe (z. B. Motorschutzschalter über Schütz) – das aktuelle Zwei-Cursor-Platzierungsmodell (Session 28g) stößt hier an seine Grenzen, eine gezielte Bauteil-Auswahl für Reihen-/Positionswechsel wäre nötig statt eines globalen Flags pro Artikel.
  4. Bedarfsbasierte Breiten-/Höhen-Umverteilung auch für `leist`/`steuer` (existiert bisher nur für die drei Klemmleisten-Zonen, `redistributeKlemmBands()`).

  Alle vier Punkte bleiben zurückgestellt bis nach dem Baugruppen-Neuaufbau.

### Code-Review Fixes (Session 19, gesperrt)
- `buildFullLayoutSVG()` M3: `h_mb_layout = mp_h − h_ke + h_abst` — h_abst war vorher vergessen
- `saveZoneInputs()`/`loadZoneInputs()` M3: `m03_h_kanal_h` + `m03_b_kanal_v` werden jetzt persistiert
- `saveProjFields()` M1+M2: `proj-docnr` nach `updateDocNr()` in localStorage geschrieben
- `calculate()` M1+M2: `if (!H || !B) return` – Guard gegen Division durch Null (sc = SH/H)
- Toter CSS/HTML-Code in M3 entfernt (`body.print-ergebnis`-Blöcke, `#print-ergebnis-container`)

### Modul 3 – Sidebar Zonen-Anzeige (Session 19, gesperrt)
- Energieverteilung, Leistungsbaugr., Steuerbaugr./DDC zeigen `TE · mm` in Zonenfarbe
- Energieverteilung: `Math.floor(b_inner / TE_BREITE_MM)` TE · `h_evert` mm · Farbe `#C8720E`
- Leistungsbaugr.: n_felder > 1 → `Math.floor(b_leist / TE_BREITE_MM)`, sonst `Math.floor((b_leist - b_uss) / TE_BREITE_MM)` · `h_leist` mm · Farbe `#C84E2E`
- Steuerbaugr./DDC: `Math.floor(b_steuer / TE_BREITE_MM)` TE · `h_steuer` mm · Farbe `#4BBECA` (auch Nebeneinander – kein `= Leistung` mehr)
- localStorage Modul 3 → Modul 4: `m03_n_te`, `m03_b_kanal_v`, `m03_h_kanal_h`, `m03_b_ek` (in `calculateZones()` geschrieben)

### Modul 3 – Zonenaufteilung (gesperrt)
- Mindesthöhen basieren auf physikalischen Festwerten (analog h_ke-Logik), **keine Prozent-Eingabe**
- `ceil5(v)` = `Math.ceil(v/5)*5` – alle Mindesthöhen auf 5 mm aufgerundet
- Festwerte: `H_KLEMME_STD=65`, `H_HANDLING=15`, `H_SICHER_WS=75`, `H_SCHIENE_DS=150`, `H_KANAL_H=40`, `B_KANAL_V=40`
- `h_klemm = ceil5(H_HANDLING + H_KLEMME_STD + H_HANDLING) = 95 mm` – H_KLEMME_STD = 65 mm, H_HANDLING = 15 mm (gesperrt)
- `h_evert`: Drehstrom = `ceil5(150) = 150 mm`, Wechselstrom = `ceil5(105) = 105 mm`
- **Einspeisung (USS) + Einsp.-Klemmen immer LINKS** – unabhängig von KE-Position (gesperrt)
- **KE-Position** bestimmt nur die vertikale Reihenfolge: KE oben → Klemmen oben, Evert unten; KE unten → Evert oben, Klemmen unten
- **Klemmenzeile** = eine Hutschiene, 4 Untergruppen: Einsp.-Kl. (5 TE) · Abg.-Kl. Leistung · Abg.-Kl. Feldgeräte · Abg.-Kl. Sensoren
  - Einsp.-Kl. immer links (x=0)
  - **Nebeneinander**: Abg.-Kl. Leistung = `(b/2 / b) * f_rest`, Feldger. + Sensoren teilen Rest je ½
  - **Übereinander**: Abg.-Kl. Leistung bis zur Zonengrenze `b − B_KANAL_V`, Feldger. + Sensoren teilen `B_KANAL_V` je ½
- **Einspeisefeld** (ÜSS + Sich. + Hauptschalter-Platzhalter) immer im Leistungsbereich (EMV), immer links
  - In jeder L/S-Zeile: Breite = b_uss, direkt rechts neben linkem V.Kanal
- **Vertikaler Kabelkanal Links** (`B_KANAL_V = 40 mm`): an linker Gehäusekante, Leistungsleitungen
- **Vertikaler Kabelkanal Rechts** (`B_KANAL_V = 40 mm`): an rechter Gehäusekante, Steuerungsleitungen
  - Beide V.Kanäle erscheinen in jeder L/S-Zeile (nebeneinander + übereinander)
  - `b_inner = b − 2 × B_KANAL_V` = Nutzbreite für L/S
- **Horizontaler Kabelkanal** (`H_KANAL_H = 40 mm`): volle Breite, zwischen Klemmen und L/S
- **Horizontaler Kanal L/S-Trennung** (`H_KANAL_H = 40 mm`): volle Breite, zwischen Leistung und Steuerung (nur Übereinander)
- **h_verfueg** = h − h_evert − h_klemm − H_KANAL_H − h_kanal_ls; h_kanal_ls = H_KANAL_H (über) oder 0 (neben)
- Leistung/Steuerung: verbleibende Höhe ÷ 2 (Übereinander) oder gleiche Höhe je ~50 % b_inner (Nebeneinander)
- **Zonenreihenfolge KE oben**: Klemmen → H.Kanal → Leistung → [H.Kanal L/S → Steuerung] → Evert
- **Zonenreihenfolge KE unten**: Evert → [Steuerung → H.Kanal L/S →] Leistung → H.Kanal → Klemmen
- ~~`zone_anordnung` (Nebeneinander/Übereinander) wird disabled wenn `zone_modus === 'je_feld'`~~
  **aufgehoben Session 48 Nachtrag 3** – stammte aus der Zeit vor dem
  Feldtyp-System, als „Mehrere Felder" nur ein unfertiger Platzhalter war.
  `zone_anordnung` bleibt jetzt bei JEDEM `zone_modus` wählbar (Nutzer-Fund:
  „Der Fall Mehrere Felder Leistung und Steuerung nebeneinander fehlt").
- `buildLayout(zp)` erzeugt Zeilen-Array mit x/w-Fraktionen für SVG-Rendering
- SVG-Maßlinien: je Zeile rechts, Gesamthöhe außen (gleiche Konvention wie M1/M2)
- Kabelkanäle als eigene SVG-Zonen dargestellt (Grau `#888`, fill-opacity 0.22)
- Kanalstreifen ohne Textlabel im SVG (`lbl:''` für `kanal_h`, `kanal_ls`, `kanal_ev`) – grau erkennbar, kein Text
- Zonentext nur angezeigt wenn `zone.lbl` nicht leer und `rh >= 12` (kein sekundärer `row.h_mm mm`-Text)

### Modul 2 – Standschrank-spezifische Regeln (gesperrt)
- KE unten: kein PG (Boden offen), Kabel läuft frei durch Schrankunterseite und Sockel
- KE oben: PG-Verschraubung halb so groß wie Modul 1 (±4 px statt ±8 px, stroke-width 0.7)
- Sockel-Maßlinie: gleiche horizontale x-Position wie H-Maßlinie (`hx = sx - 16`), Label nur Wert in mm (kein Variablenname)
- „Schaltschranksockel" linksbündig bei `zoneLblX` (nicht mittig)
- „Freie Kabeleinführung · Boden offen" bei `zoneLblX`, unterhalb Sockeltext, Größe `fs_zone`
- VH = PT + SH + h_sockel_px + PB (dynamische SVG-Höhe bei aktivem Sockel)
- Sockel-Lookup: `SOCKEL_DB.find(e => e.b_gehaeuse_aussen_mm === B && e.h_sockel_mm === h_sockel_option)`
- **Standardwerte beim ersten Aufruf:** Sockel 100 mm aktiv, KE-Position unten, Zugentlastung Ja
- Strichstärken proportional: `lw_s = Math.max(0.8, sc*8)`, `lw_mp = Math.max(0.4, sc*4)` – gilt für beide Module

### Drucklayout – Corporate Design (Session 18, gesperrt)
- **`printErgebnis()`** in allen 3 Modulen identisch: injiziert `@page{size:A4 landscape;margin:10mm 12mm}` per JS-`<style>`-Element, ruft `window.print()` auf, entfernt `<style>` danach wieder. `@page` darf NICHT innerhalb `@media print` stehen – Browser ignorieren das.
- **Vollseiten-Ausdruck** (beide Panels + SVG + Ergebnistabelle) – kein Container-Switching, kein `body.print-ergebnis` Class-Toggle für Modul 1–3
- **Corporate Header `@media print header`** (alle 3 Module):
  ```css
  header { background:#EFEFEC !important; border-bottom:1.5px solid #BBBBBB;
           -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .proj-fields { border-left:1px solid #CCC; padding-left:14px; margin-left:14px; }
  .proj-field input { color:#111 !important; border-bottom:0.5px solid #BBB; background:transparent; }
  ```
- **Hintergrundfarbe im Druck:** Immer `-webkit-print-color-adjust:exact; print-color-adjust:exact` auf Elementen mit Hintergrundfarbe setzen – sonst druckt Browser weiß
- **Projektfeld-Farben:** `color:#111 !important` nötig, weil `#proj-docnr` screen-seitig `color:var(--tx2)` (grau) hat
- **Fieldsets page-break-safe:** `fieldset { break-inside:avoid; page-break-inside:avoid }` in allen 3 Modulen
- **Modul 3 `.field .var`:** `white-space:normal; word-break:break-all` (nicht `nowrap`) – verhindert Überlauf langer Variablennamen in Nachbarspalte; `.field .lbl` braucht zusätzlich `overflow:hidden`
