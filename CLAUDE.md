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
│   └── modul-03-architektur/index.html        TE-Berechnung & Reihenkapazität ✅
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
│   ├── reiheneinbaugeraete.json                 Reiheneinbaugeräte-DB (Sicherungsautomaten etc., committed)
│   ├── einzelbauteile.json                      Modul-4-Bauteilkatalog (committed, seit Session 27 über Excel gepflegt)
│   ├── baugruppen.json                          Modul-4-Baugruppen-DB (committed, seit Session 27 über Excel gepflegt)
│   └── xlsx_to_json.py                          Konvertierungsskript Excel → JSON (9 Sheets, `einzelbauteile`/`baugruppen`+`baugruppen_bauteile`-Verknüpfungstabelle seit Session 27)
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
- **Entwickler-Workflow Daten:** Excel bearbeiten → in WSL: `cd /mnt/c/users/smi/cowork/dbacs/data && python3 xlsx_to_json.py` → exportiert alle 6 JSON-Dateien → alle committen
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

## Gesperrte Entscheidungen

Diese Punkte wurden bereits ausführlich diskutiert und entschieden – nicht neu aufgreifen:

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

### Modul 4 – Innenaufbau (Session 20, gesperrt – Grundlayout, Details siehe Session 22/23)
- Layout Session 23: volle-Breite Eingabeleiste (unter Header) → Füllstand-Streifen (8 Mini-Balken, 1 Zeile) → 3-Spalten-Grid 260px Belegung | flex:1 Schranksicht | 340px Stückliste (löst das Session-20/21-Sidebar-Layout ab)
- Gewerk-Tabs: RLT · HKL · Sanitär · Beleuchtung · Elektro → filtert Baugruppen-Dropdown
- Belegungsliste: persistiert als `m04_belegung` (JSON-Array in localStorage)
- Reihen-Parameter: Klemmraum je Seite (Standard 20 mm, editierbar, persistiert als `m04_klemmraum_mm`); Verdrahtungskanal = 40 mm (Konstante, nicht editierbar)
- Physikalische Reihenplatzierung: Reihenfolge Kanal(40mm) → Reihe → Kanal → Reihe → … → Kanal; Reihenhöhe = max(h_mm in Reihe) + 2×Klemmraum; TE-Kapazität je Reihe = floor(b_zone / 18) – gilt nur für die Mehrreihen-Zonen, siehe Session 22
- CSV-Export: Blob-Download `dbacs_stueckliste.csv` (UTF-8 BOM, Semikolon-getrennt)
- `printErgebnis()` wie M1–M3 (A4 landscape, Corporate Header)
- BG_COLORS: 10 Farben zyklisch: #E07B39, #4BBECA, #9A94E8, #2DBD8E, #C84E2E, #D4A84B, #7A74CC, #5BAD6B, #C86090, #A8C4E8

### Modul 4 – Granulare Zonen, Direktbauteile & Indizierung (Session 22, gesperrt)
- **Löst die Session-20-Vereinfachung ab:** statt 3 Sammelzonen (leistung/steuerung/klemmen) jetzt 8 echte Modul-3-Unterzonen, deckungsgleich mit `buildLayout()`-IDs: `klemm_e` (Einspeiseklemmen), `uss` (ÜSS+Vorsicherung), `evert` (Energieverteilung), `leist`/`leist_ext` (Leistungsbaugruppe), `steuer` (Steuerbaugruppe), `klemm_l`/`klemm_f`/`klemm_s` (Abgänge-Klemmen Leistung/Feldgeräte/Sensoren)
- **Zwei Platzierungsmodelle** (Unterscheidung ist zentral, nicht austauschbar):
  - `placeInBands()` – Kanal(40mm)+Klemmraum-Modell für flexible Mehrreihen-Zonen: `leist`, `steuer`, sowie `evert` **nur wenn** Schienensystem aktiv (`zp.useEvKanal===false`, h_evert 300–400mm, großzügig)
  - `placeInKlemmRow()` – 1-Reihen-Modell (keine Kanal/Klemmraum-Klammerung, Breite statt Höhe als Kapazität): `klemm_e`, `uss`, `klemm_l`, `klemm_f`, `klemm_s`, sowie `evert` **ohne** Schienensystem (h_evert=105mm, entspricht bereits `ceil5(15+75+15)` – M3 hat die Einbauhöhe schon exakt bemessen, kein Zusatzraum)
  - **Warum:** h_klemm/h_uss/h_evert-ohne-Schiene sind in M3 bereits als „Handling+Bauteil+Handling“ fertig bemessen; ein zusätzliches Kanal+Klemmraum-Layer von M4 sprengt diese Zonen (führte zu Mehrreihen-Zonen mit 0 platzierten Bauteilen trotz freiem Platz – Session-22-Bugfix)
- **Datenmodell:** `bt.zone || eb.zone` – Zone wird pro Baugruppen-Bauteil-Eintrag optional überschrieben (`baugruppen.json`), Katalog-Default (`einzelbauteile.json`) nur Fallback. Kein Auswahl-UI für Zone zur Laufzeit – ist immer vorab in der Datenpflege festgelegt
- **Zwei Belegungs-Eintragstypen:** `{typ:'baugruppe', bg_id, menge, ci}` (Gewerk-Tabs, Bündel) und `{typ:'einzel', artikel_nr, menge, ci}` (neues Fieldset „Einspeisung, Verteilung & Direktbauteile“, Dropdown mit `<optgroup>` je `kategorie`-Feld). Alte `m04_belegung`-Einträge ohne `typ` werden beim Laden als `'baugruppe'` interpretiert
- **Indizierung:** jeder platzierte Bauteil-Block bekommt eine laufende Nummer je Zone (`idx` in `placeInBands()`/`placeInKlemmRow()`), sichtbar im SVG-Tooltip (`#<idx> · <Bezeichnung>`) und in der Stückliste (`formatIdxList()` – komprimiert zu Bereichen wie `#3–#5, #7`)
- **Stückliste-Aggregation** jetzt nach `(artikel_nr, effektive Zone)` statt nur `artikel_nr` – derselbe Artikel kann je Baugruppe in unterschiedlichen Zonen landen und erscheint dann bewusst als getrennte Zeile
- **Füllstand-Anzeige:** ursprünglich 8 gestapelte Balken in 2 Gruppen – Session 23 macht daraus einen kompakten Streifen, siehe unten
- **Zone-Badges:** `zone-ke`/`zone-us`/`zone-ev`/`zone-l`/`zone-s`/`zone-kl`/`zone-kf`/`zone-ks` (ersetzt die alten `zone-e`/`zone-k`)
- **Nicht umgesetzt (bewusst zurückgestellt):** intelligente DDC-Modul-Packlogik (Belegung bis Datenpunkt-Kapazitätsgrenze inkl. Kunden-Reserve), Drag&Drop-Repositionierung, Integritätsprüfung einer Baugruppen-Instanz, Mehrfeld-Schränke in M4
- Datenbasis jetzt: `data/einzelbauteile.json` (44 Bauteile) + `data/baugruppen.json` (15 GA-Gruppen, Bauteile mit optionalem Zone-Override). Neue Katalogeinträge (Best-effort-Maße, wie `bodenbleche.json` als „zu verifizieren“ zu behandeln): DDC-I/O-Module Siemens Desigo PXA30-W2/PXA30-N (`zone:"steuer"`, Feld `datenpunkte` gespeichert aber unausgewertet), Lasttrennschalter/Sicherungshalter (`zone:"evert"`), ÜSS-Geräte Typ 2 + Vorsicherungshalter (`zone:"uss"`)

### Modul 4 – Layout-Neuordnung: Schranksicht dominant (Session 23, gesperrt)
- **Auslöser:** Live-Test auf GitHub Pages bei 1920×1080 zeigte, dass die Füllstand-Anzeige (Session 22, 8 gestapelte Balken) das mittlere Panel dominierte und die Schranksicht verdrängte; zusätzlich reichte die 340px-Sidebar für die Direktbauteil-Combobox nicht
- **Neue Struktur (volle Seitenbreite, von oben nach unten):** Header → `.eingabeleiste` (Schranktyp, Montagebereich-Anzeige, Klemmraum, Gewerk-Tabs+Baugruppe, Direktbauteil – alle in einer horizontalen Flex-Zeile) → `.fuellstand-strip` (8 Mini-Balken in 1 Zeile, Kurzlabel+Prozentwert, Details im `title`-Tooltip je `.fs-mini`) → `.layout-3col` (jetzt 260px Belegung | 1fr Schranksicht | 340px Stückliste)
- **Schranksicht-Skalierung wie Modul 3:** `buildSVG()` misst `#svg-wrap` per `clientWidth`/`clientHeight` und setzt `sc = Math.min(availW/b, availH/totalH)` (vorher nur breitenskaliert `sc = SW/b`) – SVG bekommt explizite `width`/`height`-Attribute statt `width:100%`, dadurch immer vollständig sichtbar, kein Innen-Scroll. `#svg-wrap` ist jetzt `flex:1` in `.panel-mid` (`display:flex;flex-direction:column`) und zentriert die SVG per Flexbox
- **Resize-Listener** (debounced 150ms) ruft `calculate()` erneut auf, damit die Schranksicht bei Fenstergrößenänderung neu skaliert
- `var_b`/`var_h` zu einem gemeinsamen `var_b`-Span zusammengefasst (`b/h_mplatte_mbereich_...`), da B und H jetzt in einer Zeile mit „×“ getrennt angezeigt werden – `loadMontagebereich()` entsprechend angepasst (referenziert `var_h` nicht mehr)
- Print-CSS: `.eingabeleiste`/`.fuellstand-strip` ausgeblendet (wie `.gewerk-tabs`/`.bg-add-row`), `.layout-3col` Druckspalten auf 200px/1fr/300px angepasst
- `.eb-field label`: Beschreibung und `.var`-Variablenname stehen untereinander (`flex-direction:column`), nicht mehr nebeneinander – verhindert, dass lange Variablennamen die Feldbreite aufblähen und Folgefelder aus dem sichtbaren Bereich schieben

### Modul 4 – Funktionsbereich-Taxonomie (Session 24, gesperrt)
- **„Gewerk" → „Funktionsbereich" umbenannt** – Label in der Eingabeleiste und Konzept: Tabs gruppieren die Bauteil-Datenbank nach Funktionsbereich, nicht mehr nur nach klassischem HOAI-Gewerk
- **10 Funktionsbereiche** (`data-gewerk`-Werte), Reihenfolge fest (2×5-Grid, `grid-template-columns:repeat(5,auto)`): `schaltschrank`, `automation`, `elektro`, `beleuchtung`, `netzwerk`, `lueftung`, `heizung`, `kaelte`, `sanitaer`, `nutzungsspezifisch`
- **Migration bestehender `baugruppen.json`-Einträge** (mechanische Umbenennung, keine inhaltliche Neuzuordnung): `rlt→lueftung`, `hkl→heizung`, `san→sanitaer`, `bel→beleuchtung`, `elek→elektro`. Default-Tab beim Laden: `lueftung` (meiste bestehende Baugruppen)
- **`schaltschrank`, `automation`, `netzwerk`, `kaelte`, `nutzungsspezifisch` sind bewusst leer** – keine Baugruppen bisher zugeordnet, wird Teil der nächsten „Grundlagen"-Session (korrekte Maße + Zonen-Zuordnung der Bauteildaten)
- „Einspeisung, Verteilung & Direktbauteile" → „Spezifische Auswahl Einzelbauteile" umbenannt (Label unverändert funktional)
- Baugruppe-Auswahl und Einzelbauteil-Auswahl jetzt gleich breit (`width:320px` statt `flex:1` beim Einzelbauteil-Feld) – verhindert, dass ein Dropdown deutlich länger als das andere wirkt
- `.eb-field{min-width:0}` + `.bg-add-row select{min-width:0;overflow:hidden;text-overflow:ellipsis}`: Flexbox-Fix, damit lange Baugruppen-/Bauteilnamen das `<select>` nicht über die 320px hinaus aufblähen und Menge/„+"-Button verdrängen (Default-`min-width:auto` von Flex-Kindern war die Ursache)

### Modul 4 – Bedarfsbasierte Breiten-Umverteilung Klemmleisten (Session 25, gesperrt)
- **Problem:** `klemm_l`/`klemm_f`/`klemm_s` hatten feste, aus Modul 3 übernommene Breiten. Wurde z. B. `klemm_s` (Sensoren) stark genutzt, lief sie schnell über, obwohl `klemm_l`/`klemm_f` noch reichlich Platz hatten – der Schrank als Ganzes hätte gereicht.
- **Lösung `redistributeKlemmBands(bandsAll, queues)`:** Die 3 Unterzonen (nicht `klemm_e`/Einspeiseklemmen – die bleibt fix) teilen sich eine gemeinsame Gesamtbreite = Summe ihrer ursprünglichen M3-Bänder (bleibt konstant). Jede Zone bekommt so viel Breite wie ihr TE-Bedarf (Summe `te` der Warteschlange × `TE_MM`) erfordert; reicht die Gesamtbreite, wird der Rest **proportional zum ursprünglichen M3-Verhältnis** verteilt (Füllstand bleibt aussagekräftig, nicht künstlich immer 100%). Reicht sie nicht, bekommt jede Zone einen zu ihrem Bedarf proportionalen Anteil (bestehender Überlauf-Indikator greift wie gehabt) – **kein neues Schaltschrankfeld** in diesem Schritt (bewusst nicht entwickelt).
- Zustandslos: komplette Neuberechnung bei jedem `calculate()`-Aufruf, keine Reihenfolge-Abhängigkeit zwischen Baugruppen.
- Eingebunden in `placeBauteile()` direkt vor der `KLEMM_ZONEN`-Schleife; `buildSVG()` zeichnet das Zonenraster für diese 3 IDs jetzt aus den umverteilten Bändern (`zones[zn].bands`) statt aus `layout.svgRows` (M3-Statik).
- **Idee 2 (Leistung/Steuerung, Höhen-Umverteilung mit verschiebendem Kabelkanal) bewusst zurückgestellt** – eigene Abstimmungsrunde nötig (Mindesthöhe `h_leist ≥ h_klemm`, separater Rechenweg für „Nebeneinander" vs. „Übereinander").

### Modul 4 – Fortlaufender Verdrahtungskanal je Bauteilreihe (Session 26, gesperrt)
- **Problem:** Elektronische Betriebsmittel (Schütz, Motorschutzschalter, Relais, DDC-Modul) haben oben UND unten elektrische Anschlüsse. `placeInBands()` setzte den Verdrahtungskanal (40 mm) bisher nur vor der jeweils ersten Reihe eines Bandes; alle Folgereihen innerhalb desselben Bandes wurden ohne Kanal direkt gestapelt (kein Verdrahtungsraum unter den Bauteilen). Beim Wechsel in ein neues Band (z. B. Leistung → Leistung-Ext) konnte zusätzlich ein abschließender Kanal am Bandende auf den Start-Kanal des nächsten Bandes treffen → zwei Kanäle übereinander, Platzverschwendung ohne Nutzen.
- **Erster Korrekturversuch (verworfen):** Kanal vor jeder Reihe inkl. Reihe 1. Fehlerhaft, da die erste Reihe einer Zone immer bereits direkt an eine bestehende feste M3-Kanalzone grenzt (`kanal_h`/`kanal_ls`/`kanal_ev`, je nach Zonenreihenfolge/KE-Position) – ein zusätzlicher Kanal davor erzeugte erneut zwei Kanäle direkt übereinander (vom Nutzer per Screenshot der Steuerbaugr./DDC-Zone bestätigt).
- **Finale Lösung:** `kanalPending` startet mit `false` – die erste Reihe einer Zone bekommt keinen Kanal davor (nutzt den bereits vorhandenen M3-Kanal). Nach jeder platzierten Reihe wird `kanalPending = true` gesetzt, sodass vor jeder Folgereihe (auch bandübergreifend, z. B. Leistung → Leistung-Ext) genau ein Kanal eingefügt wird – zwei benachbarte Reihen teilen sich diesen Kanal an ihrer gemeinsamen Grenze.
- **Kein abschließender Kanal nach der letzten Reihe:** Leistung und Steuerung münden (in beiden KE-Positionen, Übereinander wie Nebeneinander) immer direkt in eine feste M3-Kanalzone (`kanal_ls`/`kanal_h`/`kanal_ev`), die die untere Anschlussseite der letzten Reihe bereits abdeckt. Der verbleibende Rest des letzten Bandes bleibt als zusätzlicher Klemmraum ungenutzt – akzeptiert, da der Installationsbereich dadurch insgesamt besser ausgenutzt wird als durch einen bandweise garantierten, aber oft sinnlos gestapelten Extra-Kanal.
- Betrifft `placeInBands()`, verwendet für `leist`/`steuer` (immer) sowie `evert` (nur wenn `!zp.useEvKanal`) – gilt also für alle drei mit gleicher Begründung.
- Geprüft für Leistung + Steuerung, Übereinander und Nebeneinander, inkl. bandübergreifendem Wechsel (z. B. Leistung-Ext → Leistung-ÜSS-Reihe): erste Reihe direkt am Zonenanfang ohne Kanal, danach korrekt alternierendes Reihe-Kanal-Reihe-Muster, kein Kanal nach der letzten Reihe.

### Modul 4 – Zonenbeschriftung: Vordergrund-Ebene + robuster Zeilenumbruch (Session 26, gesperrt)
- **Problem 1 (Ebenen/Z-Order):** Zonentext (z. B. „Steuerbaugr./DDC") wurde in `buildSVG()` zusammen mit dem Zonen-Hintergrundrechteck gezeichnet, noch bevor die Bauteil-Blöcke folgten. Da SVG in Dokumentreihenfolge zeichnet (spätere Elemente liegen über früheren), überdeckten Bauteile, die oben in der Zone platziert werden, den Beschreibungstext vollständig.
- **Lösung:** `buildSVG()` sammelt alle Zonen-/Klemmleisten-Beschriftungen in einer separaten `svgLabels`-Zeichenkette statt sie sofort auszugeben, und hängt sie erst ganz am Ende an (nach Kanälen, Bauteil-Blöcken und Overflow-Markierungen) – SVG-Ebenen lassen sich so rein über die Zeichenreihenfolge simulieren, ganz ohne `<g>`-Gruppen oder `foreignObject`. Zusätzlich bekommt der Text einen hellen Konturumriss (`stroke="#FDFCF8" stroke-width="3" paint-order="stroke fill"`), damit er unabhängig von der jeweiligen Bauteilfarbe darunter lesbar bleibt.
- **Problem 2 (Zeilenumbruch):** `wrapSVGText()` (aus Modul 3 portiert) bricht nur an Leerzeichen/Bindestrichen um. Labels wie „Steuerbaugr./DDC" oder „Leistungsbaugr." sind ein einzelnes zusammenhängendes Wort ohne Leerzeichen – bei sehr schmalen Zonen (typischerweise Nebeneinander-Anordnung) blieb der Text einzeilig und lief rechts aus dem Feld heraus.
- **Lösung:** `wrapSVGText()` bricht jetzt zusätzlich hart in `maxChars`-Stücke um, wenn ein einzelnes Wort für sich genommen schon breiter als die Zone ist. Bei extrem schmalen Zonen (Testfall 45 mm) entstehen dadurch viele kurze Zeilen (im Extremfall 1–2 Zeichen je Zeile) – optisch nicht schön, aber der Text bleibt garantiert innerhalb der Zonenbreite. Realistische Zonenbreiten (≥ 90 mm) brechen sinnvoll in 2–3 Zeilen.
- Diese Ebenen-Anpassung betrifft ausschließlich Modul 4 (Modul 3 platziert keine Bauteile über den Zonentext, dort besteht das Überdeckungsproblem nicht); die `wrapSVGText()`-Kopie in Modul 3 hat weiterhin nur den wortbasierten Umbruch ohne harten Fallback – bei Bedarf dort separat nachziehen.

### Modul 4 – Zonen-Legende + sichtbare Bauteil-Nummerierung (Session 26, gesperrt)
- **Idee des Nutzers:** Da die Zonen unterschiedliche Farben haben, hilft eine Farb-Legende zusätzlich zum (nach obigem Fix zwar lesbaren, aber bei schmalen Zonen weiterhin knappen) Zonentext. Kombiniert mit einer am Block sichtbaren Positionsnummer lässt sich ein Bauteil aus der Stückliste heraus im Schrankbild wiederfinden – nicht nur „was ist verbaut", sondern auch „wo genau".
- **Drei Design-Entscheidungen vom Nutzer bestätigt (Standardempfehlung jeweils übernommen):**
  1. Legende zeigt **nur die 8 Zonenfarben** (`ZONE_LABELS`/`ZONE_COLORS`), nicht die Baugruppen-Instanzfarben (`BG_COLORS`) – die gibt es schon als `.bel-dot` in der Belegungsliste, und `ci` verschiebt sich beim Löschen von Einträgen (instabile Legende).
  2. Nummerierung bleibt **pro Zone** (wie bisher) – `placeInBands()`, `placeInKlemmRow()`, `aggregateStueckliste()`, `buildIdxMap()`, `formatIdxList()` unverändert. Jede Nummer ist im Kontext ihrer Zonenfarbe bzw. des Zonen-Badges in der Stückliste eindeutig.
  3. Sichtbare Nummer auf dem Block **ergänzt** die Kurzbezeichnung (`MSS`, `Sch.`), ersetzt sie nicht.
- **`ZONE_COLORS`-Konstante neu** (neben `ZONE_LABELS`, ~Zeile 498) – einzige Quelle für Zonenfarben. Ersetzt die bisher doppelt geführten Farbwerte in `buildFuellstand()` (lokale `color`-Map) und `KLEMM_REDIST_DEF` in `buildSVG()` (dritte Kopie für `klemm_l`/`klemm_f`/`klemm_s`).
- **`buildLegend()`** (neu, vor `wrapSVGText()`) rendert `<div id="cabinet-legend">` (Geschwisterelement von `#svg-wrap` in `.panel-mid`, unterhalb der Schranksicht) aus `ZONE_LABELS`/`ZONE_COLORS` – Aufruf aus `calculate()`. Da `#svg-wrap` `flex:1` in einer `flex-direction:column`-Spalte ist, nimmt sich die Legende nur ihre eigene Höhe; die bestehende Skalierung (`sc = Math.min(availW/zp.b, availH/layout.totalH)`, misst `wrapEl.clientHeight` live) passt sich ohne Codeänderung an.
- **Sichtbare Bauteil-Nummer** in `buildSVG()`'s Block-Loop (kein neuer Layer nötig – die Nummer liegt immer auf dem eigenen Block, nie im Bereich eines Nachbarblocks, anders als die Zonentexte): dreistufig nach Platzangebot –
  1. `bw > 28 && bh > 8` und genug Höhe für zwei Zeilen (`bh >= fs+fsIdx+2`): Kurzbezeichnung + `#idx` als zwei `<tspan>` untereinander.
  2. Gleiche Breiten-/Höhenschwelle, aber zu wenig Höhe für zwei Zeilen: nur die Kurzbezeichnung (wie vor diesem Fix).
  3. Zu schmal für die Kurzbezeichnung, aber breit genug für die Nummer allein (Passgenauigkeit über dieselbe Zeichenbreiten-Heuristik wie `wrapSVGText`, `cw = fs*0.63`): nur `#idx`.
  4. Darunter: kein Text – Mouseover-Tooltip (`<title>#idx · Bezeichnung</title>`, unverändert) bleibt Fallback.
- **Druck:** Keine neue `@media print`-Regel nötig – die Stückliste (mit vollem Bezeichnungstext + Idx-Bereichen wie `#3–#5, #7`) druckt bereits unverändert mit und deckt das vom Nutzer gewünschte „Mouseover-Volltext beim Druck sichern" bereits ab. Die neue Legende ist ein normales, nicht ausgeblendetes Panel-Element und druckt automatisch mit; `.legend-dot` bekommt zusätzlich `-webkit-print-color-adjust:exact;print-color-adjust:exact`, da Browser Hintergrundfarben beim Drucken sonst standardmäßig unterdrücken.
- Kein neues `printFullLayout()`/`buildFullLayoutSVG()` (wie Modul 3) – bewusst nicht entwickelt, da die Stückliste die Volltext-Anforderung bereits erfüllt.

### Zonenfarben (Modul 3 + 4, Session 26, gesperrt) – modulübergreifend identisch
Nutzer-Feedback nach Test der neuen Legende: einige Zonenfarben sahen sich zu
ähnlich (Einspeisung/ÜSS identisch, Sensoren-Klemme auch gelblich). Zusätzlich
sollten Zonenfarben nicht länger mehrfach unabhängig gepflegt werden.
```
const ZONE_COLORS = {
  klemm_e:'#EBDBA0', uss:'#D8A916', evert:'#C8720E', leist:'#C84E2E', steuer:'#4BBECA',
  klemm_l:'#2DBD8E', klemm_f:'#9A94E8', klemm_s:'#C14FA0'
};
```
- **Geänderte Werte:** `klemm_e` (Einspeisung) blasses, entsättigtes Gelb,
  `uss` (ÜSS) kräftigeres Gold-Gelb – vorher beide identisch `#D4A84B`.
  Erster Korrekturversuch hatte die Zuordnung umgekehrt (Einspeisung stark,
  ÜSS blass); auf Nutzerwunsch in derselben Session getauscht – finale
  Zuordnung ist die oben stehende. `klemm_s` (Abg.-Kl. Sensoren) Magenta statt
  Gelbton – vorher `#E8C448`. `evert`, `leist`, `steuer`, `klemm_l`, `klemm_f`
  unverändert.
- **Mechanismus:** kein gemeinsames externes File (Architektur bleibt
  Single-File-HTML pro Modul, kein zusätzlicher `fetch()` nötig, Farben sind
  synchron beim ersten Rendern verfügbar). Stattdessen führt jedes Modul
  seine eigene `ZONE_COLORS`-Konstante – identische Werte, hier zentral
  dokumentiert als verbindliche Quelle (analog zum bereits gesperrten
  Maßketten-Blau `#3366BB`).
- **Modul 4:** `buildLayout()` referenziert jetzt `ZONE_COLORS.<zone>` statt
  Hex-Literalen zu duplizieren (schließt eine bereits vorher bestehende
  interne Inkonsistenz). Dynamisch beim Bestücken entstehende
  Verdrahtungskanäle (`z.channels` in `buildSVG()`) nutzen jetzt `fill="#888"
  fill-opacity="0.22"` statt `#0000000C` und haben kein `"Kanal"`-Textlabel
  mehr – optisch identisch zu den statischen Struktur-Kanälen aus Modul 3.
- **Modul 4 – Nachtrag Füllstand-Streifen:** Die Zonennamen im Füllstand-
  Streifen (`fs-*-lbl`, z. B. „Einsp.-Kl.", „ÜSS") waren fest im HTML
  verdrahtet und wurden von `buildFuellstand()` nie aktualisiert – nur der
  Balken selbst bekam per JS die aktuelle `ZONE_COLORS`-Farbe, das Label
  daneben blieb auf dem alten Stand hängen (dem Nutzer beim Testen
  aufgefallen). Jeder `<span>` hat jetzt eine `id="fs-<id>-lbl"`,
  `buildFuellstand()` setzt `lbl.style.color = ZONE_COLORS[zone]` – Label und
  Balken laufen damit nie wieder auseinander. Die statischen HTML-
  Startwerte wurden zusätzlich auf den aktuellen Stand korrigiert (nur als
  Fallback vor dem ersten `calculate()`-Aufruf relevant).
- **Modul 4 – Zonentext nur auf dem Bildschirm ausgeblendet:** Da die Legende
  bereits Farbe → Zonenname erklärt, entfällt der Zonentext im SVG jetzt für
  die Bildschirmdarstellung (`svg += '<g class="zone-label-layer">...</g>'`,
  CSS `#svg-inner .zone-label-layer{display:none}`). Im Ausdruck bleibt der
  Zonentext erhalten (`@media print{#svg-inner .zone-label-layer{display:inline}}`),
  da dort keine Legende danebenliegt – bewusste Bildschirm/Druck-Abweichung,
  keine JS-Sonderbehandlung nötig, reine CSS-Sichtbarkeitssteuerung.
- **Modul 3:** bekommt dieselbe `ZONE_COLORS`-Konstante (neu, neben
  `TE_BREITE_MM`), `buildLayout()` referenziert sie ebenso; Sidebar-Farbpunkt
  und Sidebar-Textfarbe für „ÜSS + Sich." (`zh_einsp`) aktualisiert.
  **Bewusst NICHT übernommen:** keine Legende, keine Zonentext-Ausblendung
  (Modul 3 platziert keine Bauteile, die den Text überdecken könnten – das
  Ausgangsproblem existiert dort nicht), kein Kanal-Farbfix (Modul 3 kennt
  keine dynamisch erzeugten Verdrahtungskanäle, nur die immer schon grauen,
  textlosen Struktur-Kanäle).
- **Nicht anfassen:** `KE_COLS` (h_ke-Zonenfarben aus Modul 1/2, u. a.
  `zug:'#D4A84B'`) und die Formel-Box-Variablenfarbe für `te_breite` in
  Modul 3 nutzen zufällig denselben alten Hex-Wert wie das vorherige
  ÜSS/Einspeisung-Gelb, gehören aber zu einer anderen, bereits gesperrten
  Farbkonvention (Modul 1/2 h_ke-Formel) bzw. sind reine
  Formel-Variablen-Einfärbung – keine Zonenfarben, nicht Teil dieser
  Konsolidierung.

### Modul 4 – Höhenprüfung Hutschienen-Zonen + Beschriftung schmaler Bauteile (Session 26, gesperrt)
Zwei vom Nutzer vor dem Meilenstein gemeldete Bugs, behoben bevor als
Nächstes reale Bauteile/Funktionsgruppen integriert werden.

- **Bug 1 – Bauteile ohne ausreichenden Platz wurden trotzdem platziert:**
  `placeInKlemmRow()` (genutzt für `klemm_e`, `uss`, `klemm_l`, `klemm_f`,
  `klemm_s` sowie `evert` ohne Schienensystem – alle 6 Hutschienen-Zonen)
  prüfte nur die Breite (TE), nie die Höhe. Ein NH00-Lasttrennschalter
  (155 mm, für ein Schienensystem gedacht) wurde dadurch auch in der
  kompakten 105-mm-Energieverteilung-Zone (kein Schienensystem) "platziert"
  und im SVG verzerrt dargestellt, statt als nicht-platzierbar erkannt zu
  werden. **Fix:** `placeInKlemmRow()` prüft jetzt zusätzlich `d.h_mm <=
  band.h_mm`; zu hohe Bauteile werden übersprungen (nicht platziert, tragen
  zum Overflow bei), die Warteschlange läuft mit den übrigen Geräten weiter
  – ein einzelnes zu hohes Bauteil blockiert nicht die ganze Zeile. Overflow
  wird jetzt über eine separate `placedTotal`-Zählung ermittelt (nicht mehr
  allein über die Queue-Position `idx`), da einzelne Geräte übersprungen
  werden können, ohne dass die Warteschlange "leer" wird. Der bereits
  vorhandene rote Overflow-Marker (`!`) an der Zone greift automatisch,
  keine neue UI nötig.
- **Bewusst nicht Teil dieses Fixes:** eine Kennzeichnung einzelner
  Katalogeinträge als "erfordert Schienensystem" (neues JSON-Feld in
  `einzelbauteile.json` + Ausblenden aus der Bauteil-Dropdown
  `populateEinzelAuswahl()`, wenn kein Schienensystem gewählt ist) – auf
  Nutzerwunsch verschoben in die nächste Sitzung (Bauteile/Funktionsgruppen-
  Integration), da dort ohnehin die komplette Bauteildatenpflege ansteht.
  Der allgemeine Höhen-Fix verhindert die Fehlplatzierung bereits
  unabhängig vom Grund (Schienensystem oder jeder andere Zonentyp/Höhe).
- **Bug 2 – Beschriftung schmaler Bauteile:** die bestehende 3-Stufen-Logik
  aus einer früheren Session (Label+Nummer / nur Label / nur Nummer) hatte
  keine Rückfallebene mehr, wenn selbst die Nummer horizontal nicht passte
  (z. B. beim 1-poligen Sicherungslasttrennleiste-Zusatzmodul) – Ergebnis:
  gar kein sichtbarer Text außer dem Mouseover-Tooltip.
- **Fix – neue Hilfsfunktion `idxLabelSVG(cx, cy, bw, bh, idxStr)`:**
  versucht zuerst die Nummer horizontal (wie bisher), dreht sie als letzte
  Rückfallebene um 90° (`transform="rotate(-90 cx cy)"`) entlang der
  Blockhöhe, wenn horizontal auch verkleinert nicht passt (Achsen dabei
  vertauscht geprüft: Textlänge gegen `bh`, Schriftgröße gegen `bw`). Passt
  auch das nicht, kein Text – Tooltip bleibt Fallback. Erste SVG-
  Textrotation im Projekt (vorher nirgends verwendet). Wird sowohl als
  Rückfallebene für normale Zonen (Tier 3 der bestehenden Logik) als auch
  für Klemmen-Zeilen (siehe unten) genutzt.
- **Fix – Klemmen-Zeilen (`row.mode === 'klemm'`) bekommen nie mehr die
  Kurzbezeichnung, nur Anfang/Ende eines Laufs eine Nummer:** einzelne
  Klemmen sind oft nur 0,5 TE breit und tragen nie eine lesbare
  Einzelbeschriftung. Neue Hilfsfunktion `markFirstLastOfRun(blocks)`
  markiert `blk._showIdx` für den ersten und letzten Block jedes
  zusammenhängenden `artikel_nr`-Laufs innerhalb `row.blocks` (Reihenfolge
  ist bereits Platzierungsreihenfolge). Da `placeInKlemmRow()` je Zone immer
  genau eine Zeile liefert (kein Zeilenumbruch), genügt die Betrachtung
  innerhalb von `row.blocks` – keine zeilenübergreifende Logik nötig.
  Blöcke zwischen Anfang und Ende bleiben bewusst ohne Beschriftung
  (Tooltip bleibt für jeden Block erhalten); die exakte Liste steht
  vollständig in der Stückliste (`formatIdxList()`, z. B. `#3–#5, #7`).
  Geprüft: bei wiederkehrenden Baugruppen-Instanzen (z. B. 4× Klemme A + 1×
  Klemme B je Instanz, 15×) entstehen korrekt kurze Läufe mit jeweils
  eigenem Anfang/Ende statt eines einzigen langen, irreführenden Laufs.

### Modul 4 – Bauteil-Datenbasis über Excel-Pipeline (Session 27, gesperrt)
Vorbereitung der eigentlichen Bauteil-/Baugruppen-Datenarbeit: `einzelbauteile.json`
und `baugruppen.json` liefen bisher als einzige DBs **nicht** über die
Excel-Pipeline (Session 20 direkt als JSON angelegt) – das ist jetzt
nachgezogen, konsistent mit allen anderen 7 DBs.

- **Neue Excel-Sheets** `einzelbauteile`, `baugruppen`, `baugruppen_bauteile`
  (Verknüpfungstabelle: `bg_id`, `artikel_nr`, `menge`, `zone`-Override –
  Excel kann keine verschachtelten Arrays, daher separates Sheet).
  `export_einzelbauteile()`/`export_baugruppen()` in `xlsx_to_json.py` neu,
  nach etabliertem Muster (`aktiv`-Filter, Header-Name-Mapping).
- **Schema-Erweiterung `einzelbauteile`:** `b_mm` (reale Breite, float) ist
  jetzt das Hauptfeld, `te_breite` wird beim Export daraus abgeleitet
  (`Math.ceil(b_mm/18)` bzw. Python `math.ceil`) – nicht mehr händisch
  gepflegt. Neu: `einbaulage` (rein beschreibend, z. B. bei DDC-Modulen),
  `datenpunkt_typ`/`datenpunkt_anzahl`/`klemmen_zusatz` (Datenpunkt-Bedarf
  eines Bauteils, für die spätere DDC-Kapazitäts-Logik – **nur Datenfelder,
  keine Zählung/Auswertung in dieser Session**), `montage_minuten`,
  `preis_lieferung_eur`, `preis_gesamt_eur`. **Wichtig:** Das JSON-Ausgabefeld
  heißt weiterhin `preis_eur` (Excel-Spalte `preis_stueck_eur`, im Export auf
  `preis_eur` zurückgemappt) – Modul 4 liest dieses Feld direkt in
  `buildStueckliste()`/`exportCSV()`, eine Umbenennung hätte dort einen
  Absturz verursacht (im Test aufgefallen, siehe unten).
- **`h_mm`-Konvention dokumentiert:** Einbauhöhe ab Oberkante Hutschiene
  (vertikale Ausdehnung im montierten Zustand), nicht die Bauteiltiefe.
- **Mehrzonen-Fähigkeit:** kein Schema-Umbau – bestehender Mechanismus
  (Katalog-Default-Zone + Baugruppen-Override) reicht aus.
- **Schema-Erweiterung `baugruppen`:** `funktionsbereiche` (Array, ersetzt
  die reine `gewerk`-Einfachzuordnung als vollständige Liste – `gewerk`
  bleibt zusätzlich als Haupt-Tab-Zuordnung erhalten), `automationsfunktionen`
  (Array, z. B. `betriebsmeldung`/`stoermeldung`/`modbus_rtu`), `geprueft`
  (Bool-Tag, manuell bestätigt – alle 15 bestehenden Baugruppen beim Migrieren
  auf `true` gesetzt, da bereits mehrfach getestet).
- **Bug gefunden + behoben:** `buildStueckliste()`/`exportCSV()` gingen bisher
  davon aus, dass `preis_eur` immer gesetzt ist (`e.preis_eur.toFixed(2)` ohne
  Null-Check) – bei den neuen, noch nicht bepreisten Katalogeinträgen stürzte
  das ab. Fix: `hasPreis`-Check, Anzeige „–" statt Absturz, unbepreiste
  Positionen fließen nicht in die Summe ein (kein geratener Wert).
- **Pflegewerkzeug:** bleibt Excel (kein eigenes Editor-Modul) – Nutzer
  editiert `ga_komponenten.xlsx` selbst, Claude liefert recherchierte Werte
  zur Übernahme. **Datei muss beim Schreiben per Skript geschlossen sein**
  (Excel hält einen Lock, `~$ga_komponenten.xlsx` zeigt das an – vor jedem
  Skript-Schreibzugriff prüfen).
- **Recherche-Ergebnis (breit zuerst, 18 neue Katalogeinträge):** Klemmen
  Phoenix Contact UT4/UT6/UT10/UT16/PT2,5-MT + Wago 2002-1201 (mit
  Querschnittsbereich in der Bezeichnung, z. B. „0,14–6 mm²" – expliziter
  Nutzerwunsch); ÜSS-Vorsicherung **D03 bis 100 A** statt NH00 (Siemens
  5SG1812 – NH00 zu breit für die ÜSS-Zone, Nutzer-Korrektur); Dehn
  BLITZDUCTOR XT (Feinschutz Netzwerk/Sensor, Basisteil + Modul getrennt
  katalogisiert); Siemens-Steuertrafos 4AM-Serie (mit Spannungsangabe in der
  Bezeichnung – expliziter Nutzerwunsch); Siemens Desigo PXC100-D; **Metz
  Connect KRS-E06 (digitale LVB, Nachfolger des alten BTR-Relais) + KMA-F8
  (analoge LVB)** – Hersteller/Baureihe vom Nutzer bestätigt, konkrete
  Artikel über Metz-Connect-Produktseite verifiziert. Vier Einträge (Phoenix
  Schirmklemme, Moxa-Switch, Wachendorff-Gateway-Maße, alte Steuertrafo-
  Variante als Auslaufartikel) mangels verifizierter Abmessungen mit
  `aktiv=false` markiert statt geraten – erscheinen erst nach Verifikation.
- **Nicht erfolgreich:** Siemens HIT-Portal (`hit.sbt.siemens.com`) als
  Recherchequelle – WebFetch scheitert an Zertifikatsprüfung, Suchmaschinen
  indizieren nur Produkttitel ohne technische Daten. Für zukünftige
  Siemens-Recherchen weiterhin auf Distributor-Datenblätter (RS Components,
  Rexel, Elektro4000 u. ä.) ausweichen.
- **Bewusst nicht Teil dieser Session:** DDC-Datenpunkte-Countdown-Logik,
  automatische Mehrzonen-Platzierung zur Laufzeit, Zone „Tür" – siehe
  `docs/revison_session.md`.

### Modul 4 – Klemmen-Herstellerbereinigung: Phoenix Contact als Planungsfabrikat (Session 27b, gesperrt)
Nutzer hat nach erster Durchsicht der Excel-Tabelle festgestellt, dass zu
viele Hersteller für Klemmen gemischt waren, und alle bisherigen
Klemmen-Zeilen im `einzelbauteile`-Sheet selbst gelöscht (Weidmüller
W-Series + die zuvor recherchierten Phoenix-Einzelstücke).

- **Planungsfabrikat Klemmen: ausschließlich Phoenix Contact** (Reihenklemmen-
  Programm). Zwei Baureihen, klar nach Zone getrennt:
  - **Einspeisung (`klemm_e`): UT-Reihe, Schraubanschluss.** 5 Baugrößen
    (UT 2,5/4/6/10/16, deckt 1,5–25 mm² ab) × 5 Farben je Größe (braun=L1,
    schwarz=L2, grau=L3, blau=N, grün-gelb=PE als eigene `-PE`-Schutzleiter-
    variante, nicht nur eingefärbte Standardklemme) = 25 Katalogzeilen.
  - **Abgangsklemmen Leistung/Feldgeräte/Sensoren (`klemm_l`/`klemm_f`/
    `klemm_s`): PT-Reihe, Push-in (starr + flexibel), gleicher Klemmentyp
    für alle drei Zonen.** 5 Baugrößen (PT 2,5/4/6/10/16 N, deckt
    0,14–25 mm² ab) × 3 Farben (grau, blau=N, grün-gelb=PE) = 15
    Katalogzeilen. Zonen-Zuordnung läuft wie gehabt über den bestehenden
    Baugruppen-Override-Mechanismus (Katalog-Default `klemm_l`, pro
    Verwendung auf `klemm_f`/`klemm_s` überschreibbar) – **kein
    Schema-Umbau nötig**, genau wie in Session 27 als "Mehrzonen-Fähigkeit"
    vorgesehen.
  - **Messertrennklemme PT 2,5-MT** (0,14–4 mm²) für Feldgeräte/Sensoren mit
    Trenn-/Testfunktion, ergänzend zu den normalen PT-Durchgangsklemmen.
  - Alle Bezeichnungen enthalten jetzt den Querschnittsbereich (Nutzer-
    Vorgabe, z. B. „Durchgangsklemme UT 4, 0,14–6 mm², braun (L1)").
- **Bestehende Baugruppen-Referenzen ummappen, nicht nur neu hinzufügen:**
  die gelöschten Weidmüller-Artikel (`W-Series 1010200000/1010210000/
  1010290000`) wurden in 6 Baugruppen über 19 `baugruppen_bauteile`-Zeilen
  referenziert. Diese wurden 1:1 auf die neuen Phoenix-PT-Äquivalente
  ungemappt (2,5 mm² grau → `3209510`, 2,5 mm² PE → `3209536`, 4 mm² grau →
  `3211757`), sonst hätten bestehende Baugruppen still ein Bauteil verloren
  (Modul 4 überspringt unbekannte `artikel_nr`-Referenzen ohne Fehler –
  genau das Risiko, vor dem in der vorherigen Session gewarnt wurde).
- **Recherche-Methode:** Bestellnummern je Baugröße/Farbe einzeln über
  Phoenix-Contact-Produktseiten-Suchtreffer verifiziert (nicht geraten).
  Zwei Bauteil-Höhen (PT 4, PT 16 N) sind aus der Nachbar-Baugröße
  interpoliert statt einzeln verifiziert – als `quelle_hinweis` in der
  Excel-Zeile vermerkt, Nutzer prüft das selbst gegen die Herstellerseite
  nach ("Web-Test").
- Geprüft im Browser: Einspeisung (5 Klemmen L1/L2/L3/N/PE) und eine
  bestehende Baugruppe mit den neu gemappten Abgangsklemmen platzieren sich
  beide korrekt ohne Overflow.
- **Nutzer-Gegenprüfung (Session 27c):** Nutzer hat alle 41 Klemmen gegen die
  Phoenix-Contact-Herstellerseite geprüft und zwei Fehler korrigiert: (1)
  Typbezeichnung enthielt noch nicht den Farbcode-Suffix (z. B. „UT 2,5 BN"
  statt nur „UT 2,5" mit Farbe nur als Klartext-Anhängsel) – jetzt in
  `bezeichnung` ergänzt; (2) mehrere Höhenangaben waren falsch, vermutlich
  Höhe/Tiefe aus unterschiedlich sortierten Herstellerangaben (B×H×T vs.
  B×T×H) vertauscht – korrigiert. Beide Korrekturen direkt in Excel
  eingetragen, per `xlsx_to_json.py` neu eingelesen, im Browser erneut
  verifiziert (auch die jetzt größeren PT 10/PT 16 N passen weiterhin ohne
  Overflow in die 95-mm-Klemmenzone).
- **`geprueft`-Feld für `einzelbauteile` ergänzt** (analog zum bereits
  bestehenden Feld bei `baugruppen`): Nutzer hatte mangels Tag von Hand
  einzelne Zellen grün eingefärbt, um selbst geprüfte Werte zu markieren –
  das ist für `xlsx_to_json.py` unsichtbar (liest nur Zellwerte, keine
  Formatierung) und geht beim nächsten Neu-Einlesen verloren. Neue Spalte
  `geprueft` (Boolean, Default `false` für alle bestehenden Zeilen) im
  `einzelbauteile`-Sheet, `export_einzelbauteile()` gibt sie jetzt mit aus.
  Bewusst zeilenbasiert (nicht feldbasiert wie die informelle Grünfärbung) –
  gleiche Granularität wie bei `baugruppen`, kein Sonderfall nötig.

### Modul 4 – Bedarfsgesteuerte Reserve für Klemmenbereiche (Session 28, gesperrt)
- **Problem:** `redistributeKlemmBands()` (Session 25) verteilte die
  gemeinsame Breite von `klemm_l`/`klemm_f`/`klemm_s` bei jedem Aufruf
  bedingungslos neu, auch wenn keine Zone gefährdet war, und ohne dass
  geprüft wurde, ob eine spendende Zone dadurch selbst zu knapp wird.
- **Neues Eingabefeld `reserve_pct`** (Default 20 %, editierbar 0–50 %,
  persistiert als `m04_reserve_pct`, Muster identisch zu `klemmraum_mm`) –
  **bewusst schrankweit und generisch benannt, nicht `klemm_*`:** der Wert
  gilt konzeptionell für alle Bereiche außer den Einspeiseklemmen
  (`klemm_e`), auch wenn er in dieser Session nur in
  `redistributeKlemmBands()` ausgewertet wird. Eine spätere Anwendung auf
  `leist`/`steuer`/`evert` soll ohne Umbenennung möglich sein.
- **Neuer Algorithmus in `redistributeKlemmBands(bandsAll, queues,
  reservePct)`:** je Zone `requiredWidth = demandMM/(1-reservePct)`;
  `deficit = max(0, requiredWidth-origWidth)`, `surplus = max(0,
  origWidth-requiredWidth)`. Ohne Deficit irgendwo bleiben die
  Modul-3-Originalbreiten unverändert (keine Umverteilung ohne Anlass).
  Bei Deficit wird proportional aus dem verfügbaren `totalSurplus`
  entnommen (`takeRatio = min(1, totalSurplus/totalDeficit)`) – eine
  Spenderzone gibt nie mehr ab, als ihr eigener Überschuss über ihre
  eigene Reserve-Grenze hinaus hergibt. Reicht der Überschuss nicht,
  bleibt der Rest unerfüllt; der bestehende Overflow-Mechanismus in
  `placeInKlemmRow()` (Breiten-/Höhenprüfung) greift dann unverändert.
- Zustandslos wie schon Session 25: komplette Neuberechnung bei jedem
  `calculate()`-Aufruf, kein Event-getriebenes "pro Klemme prüfen" nötig,
  da `queues[zone]` ohnehin bei jedem Aufruf komplett aus `belegung`
  (Baugruppen-aufgelöst **und** direkt gesetzte Einzelbauteile) neu
  aufgebaut wird.
- `klemm_e` und `uss` bleiben unverändert außen vor.
- **Weiche Reserve-Warnung (Nutzer-Feedback nach erstem Live-Test):** der
  bestehende rote "!"-Overflow-Marker im Schrankbild (`placeInKlemmRow()`,
  `overflow`-Flag) reagiert nur auf harten Kapazitäts-Overflow – eine Zone
  kann ihre Bauteile noch vollständig unterbringen und trotzdem unter dem
  Reserve-Ziel liegen, ohne dass irgendwo ein Hinweis erscheint. Deshalb
  meldet `redistributeKlemmBands()` zusätzlich `shortfall`
  (`totalDeficit > 0 && totalSurplus < totalDeficit` – die Reserve konnte
  trotz Umverteilung für mindestens eine Zone nicht erreicht werden), gibt
  jetzt `{ bands, shortfall }` zurück (vorher nur `bands`).
  `placeBauteile()` reicht es als `reserveShortfall` durch (Rückgabe jetzt
  `{ zones, reserveShortfall }`, vorher nur `zones`), `calculate()` ruft
  `updateReserveWarning(reserveShortfall)`. Ein Warndreieck
  (`#reserve-warn`, `⚠`, Farbe `#E04444` wie der SVG-Overflow) erscheint
  neben dem `reserve_pct`-Eingabefeld statt im Schrankbild – bewusst
  getrennt vom harten Overflow-"!", da der Nutzer hier gezielt den
  Reserve-Wert nachjustieren kann, wenn die Abweichung gering ist.
- **Bewusst nicht Teil dieser Session:** Anwendung der Reserve auf
  `leist`/`steuer`/`evert`, ein zusätzliches Schaltschrankfeld bei
  endgültigem Überlauf (beides zurückgestellt für spätere Sessions).
- Verifiziert direkt gegen die produktive Funktion im Browser (3 Fälle:
  kein Deficit → unverändert; Deficit + ausreichender Spender →
  proportionale Umverteilung ohne Unterschreitung der Spender-Reserve;
  Deficit > verfügbarer Surplus → Teil-Entlastung, Rest bleibt Overflow).

### Modul 4 – Abschließender Kanal unter letzter Reihe & Mengen-Minus (Session 28b, gesperrt)
- **Bug in `placeInBands()` (Session 26):** die Annahme „letzte Reihe grenzt
  immer direkt an die nächste feste M3-Kanalzone" stimmte nur, wenn die
  Zone bis zum letzten mm ausgelastet war. Bei Platzreserve (Normalfall)
  blieb zwischen letzter Reihe und dem festen Kanal eine unmarkierte
  Lücke ohne Verdrahtungsmöglichkeit – der Fehler wanderte bei jeder neu
  hinzugefügten Reihe nur weiter, statt behoben zu sein (vom Nutzer per
  Live-Screenshot aufgedeckt).
- **Fix:** neue Variable `last` (statt nur `kanalPending`) merkt sich
  Band-Index, `yLocal` und `h_row` der zuletzt platzierten Reihe. Nach der
  kompletten Platzierung (äußere `for`-Schleife über `bands` fertig) wird
  einmalig geprüft: `remaining = band.h_mm - last.yLocal`. Ist
  `remaining >= H_KANAL + last.h_row` (d. h. Kanal + eine weitere,
  ähnlich große Reihe würde noch passen), wird ein abschließender Kanal
  gesetzt (`mm_used += H_KANAL`). Reicht der Rest nicht, bleibt er
  unmarkiert – der ohnehin vorhandene feste M3-Kanal am Zonenende ist
  dann nah genug. `last.h_row` (nicht die tatsächliche nächste
  Bauteilgröße, die es ja nicht mehr gibt) dient als Schätzwert für „ein
  weiteres Bauteil plus Klemmraum" – bewusste Vereinfachung, da keine
  bessere Referenzgröße existiert.
- Der bestehende `kanalPending`-Mechanismus (Kanal *zwischen* zwei
  tatsächlich platzierten Reihen, bandgrenzen-übergreifend) bleibt
  unverändert – nur der fehlende Abschluss nach der letzten Reihe kommt
  hinzu. Gilt wie bisher nur für `leist`/`steuer`/`evert` (ohne
  Schienensystem); `placeInKlemmRow()` (Klemmenzeilen) unberührt.
- Verifiziert per synthetischen Funktionstests direkt gegen `placeInBands()`
  im Browser: Platzreserve übrig → Kanal erscheint; Zone fast randvoll
  (Rest < Kanal+Reihe) → kein Kanal; mehrere Reihen mit Rest danach →
  Zwischen-Kanäle unverändert + korrekter Abschluss-Kanal; echter
  Breiten-Overflow → letzte tatsächlich platzierte Reihe bekommt trotzdem
  korrekt ihren Abschluss-Kanal (oder korrekt keinen, wenn der Rest zu
  knapp ist), `overflow`-Flag unverändert.
- **Mengen-Minus in der Add-Zeile (nicht in der Belegungsliste!):** Nutzer-
  Vorgabe war explizit „neben der Stückzahl" – also in `.bg-add-row`
  (Baugruppe UND Einzelbauteil), nicht als Löschen-Ersatz beim bestehenden
  `bel-rm`-„×" in der Belegungsliste. Statt des einzelnen `btn-add`-Buttons
  jetzt `.btn-stack` (`flex-direction:column`, 2px gap) mit zwei kleinen
  Buttons `.btn-add-sm`/`.btn-sub-sm` (Höhe je 13px, zusammen exakt 28px =
  Höhe von Mengenfeld/Dropdown, wie vom Nutzer gefordert „Platzbedarf
  identisch").
- `removeBaugruppeQty()`/`removeEinzelbauteilQty()` (neu, symmetrisch zu
  `addBaugruppe()`/`addEinzelbauteil()`): ziehen die im Mengenfeld
  stehende Zahl vom bestehenden Belegungseintrag der aktuell im Dropdown
  gewählten Baugruppe/des Bauteils ab (nicht fix −1). Kein bestehender
  Eintrag → No-Op (nichts abzuziehen). `menge <= 0` nach dem Abzug →
  Eintrag wird entfernt, `ci`-Farben aller verbleibenden Einträge werden
  wie bei `removeBelegungItem()` neu durchnummeriert.
- Verifiziert im Browser: 5 hinzugefügt → −2 → 3 → −3 → Eintrag entfernt;
  Einzelbauteil analog; No-Op-Fall (Abziehen ohne bestehenden Eintrag)
  bestätigt.

### Modul 4 – Kanal-Rand-Fix, erzwungener Zeilenumbruch, DDC-Datenpunkte-Schema (Session 28c, gesperrt)
Vier Beobachtungen aus einem wahllosen Test-Platzierungslauf (Screenshot),
in drei parallelen Explore-Agents untersucht, davon zwei diese Session
umgesetzt und eine als Datenschema vorbereitet:

- **Kanal-Rand-Inkonsistenz (unabhängiger, vorbestehender Bug, nicht durch
  Session 28/28b verursacht):** 4 statische Zonen-Definitionen in
  `buildLayout()` (`steuer_ueber`, `leist_neben_b` – ihre `kanal_vl`/
  `kanal_vr`-Streifen) fehlte `noStroke:true`, dadurch bekamen sie einen
  sichtbaren 0,6px-Rand, während alle anderen Kanäle (statisch wie
  dynamisch) randlos sind. Einfache Ergänzung, keine Logikänderung.
- **Erzwungener Zeilenumbruch (`rowBreak`), gemeinsamer Mechanismus für
  zwei Probleme:** (1) ein später hinzugefügtes größeres Bauteil (Beispiel
  Steuertrafo) wurde vom Greedy-Packer an eine bereits kompakte Reihe
  angehängt und blähte deren Höhe unnötig auf; (2) Positionierungsregeln
  wie „Motorschutzschalter immer in der Reihe über dem Schütz" waren nicht
  abbildbar. Beide Fälle lösen denselben Mechanismus aus: ein Device mit
  `rowBreak:true` beendet die aktuelle Batch in `placeInBands()` sofort
  (`if (j > idx && (devs[j].rowBreak || te + devs[j].te > te_per_row))
  break;` – wiederverwendet den bereits bestehenden `j>idx`-Guard-Stil der
  TE-Überlauf-Prüfung). Zwei Quellen für das Flag, beide münden in dasselbe
  Device-Feld:
  - **Manuell** (Checkbox „neue Reihe" bei beiden Add-Zeilen,
    `#bg_rowbreak`/`#einzel_rowbreak`): `addBaugruppe()`/
    `addEinzelbauteil()` setzen `belegung[i].rowBreak = true`. Wirkt nur
    auf das dem Queue-Aufbau nach ERSTE Gerät der gesamten
    Belegungszeile (`firstDeviceOfItem`-Flag in `placeBauteile()`) –
    bekannte Einschränkung bei Baugruppen mit Bauteilen in mehreren
    Zonen (das gemeinte Bauteil könnte in einer anderen Zone landen als
    das tatsächlich erste in `bg.bauteile[]`); für den Hauptfall
    (Direktbauteil wie den Steuertrafo, `typ:'einzel'`, immer nur eine
    Zone) nicht relevant. Kein Zurücksetzen über UI in dieser Runde.
  - **Datengetrieben** (`baugruppen_bauteile`-Sheet, neue Spalte
    `zeilenumbruch_davor`): `xlsx_to_json.py`, `export_baugruppen()` gibt
    bei gesetztem Flag `bt.rowBreak = true` aus. Beispiel „MSS über
    Schütz": Flag beim Schütz-Eintrag setzen (MSS steht im
    `bauteile[]`-Array bereits davor).
  - Kein Effekt auf `placeInKlemmRow()` (Klemmenzeilen kennen kein
    Reihen-Konzept).
  - **Bewusst nicht Teil dieser Session:** Beispiel 2 aus der
    Nutzeranfrage („DDC-Module als Block zusammenhalten, keine anderen
    Bauteile dazwischen") – andersartiges Constraint (Gruppierung statt
    Umbruch-vor-Bauteil), eigene Session.
  - Verifiziert direkt gegen `placeInBands()`: 5 Geräte (4×20mm + 1×90mm)
    ohne `rowBreak` → 1 Reihe, Höhe 120mm (durch das große Gerät
    aufgebläht); mit `rowBreak` auf dem großen Gerät → 2 Reihen, erste
    bleibt kompakt bei 50mm, zweite (nur das große Gerät) 120mm – exakt
    das Steuertrafo-Szenario aus dem Screenshot behoben.
- **DDC-Datenpunkte-Schema neu strukturiert (nur Datenmodell, keine
  Laufzeit-Auswertung – Nutzer-Vorgabe):** die bisherigen, nie befüllten
  Felder `datenpunkt_typ`/`datenpunkt_anzahl` (pauschale Summe, keine
  Typ-Aufschlüsselung) werden ersetzt durch 8 einzelne Zählfelder je
  Bauteil – `dp_ai`, `dp_ao`, `dp_bi`, `dp_bo`, `dp_fb_ai`, `dp_fb_ao`,
  `dp_fb_bi`, `dp_fb_bo` (neue Konstante `DP_FELDER` in
  `xlsx_to_json.py`) – plus neue Spalte `automationsanbindung`
  (Boolean), die vermeidet, dieselbe Katalogzeile für „mit/ohne
  Automation" doppelt führen zu müssen. Bei `bauteil_typ==='ddc_io'`
  beschreiben die 8 Felder künftig die bereitgestellte KAPAZITÄT je Typ
  (z. B. PXA30-W2: `dp_ai=4, dp_ao=4, dp_bi=8, dp_bo=8` statt der
  bisherigen pauschalen `datenpunkt_anzahl=24`), bei allen anderen
  Bauteilen den BEDARF je Typ – Angebot/Bedarf-Unterscheidung rein über
  `bauteil_typ`, kein zusätzliches Datenfeld. `export_einzelbauteile()`
  emittiert die Felder nur bei `automationsanbindung=true` (schlankes
  JSON für die übrigen ~40 Bauteile, analog zum bestehenden Muster für
  optionale Felder).
- **Bewusst nicht Teil dieser Session (Folge-Aufgaben):** die eigentliche
  Recherche/Dateneingabe der `dp_*`-Werte für alle Katalogeinträge
  (Nutzer pflegt Excel selbst, wie immer); Migration der beiden
  bestehenden `datenpunkt_anzahl`-Werte (PXA30-W2/PXA30-N) auf die neuen
  Felder (nicht automatisch ableitbar, nur bei diesen beiden aus der
  Bezeichnung „8DI/8DO/4AI/4AO" bekannt); der Laufzeit-Toggle in Modul 4
  (analog `reserve_pct`: „Automationsanbindung berücksichtigen? Ja/Nein",
  aktiv → Auswahl mit `automationsanbindung=true` zählt gegen das von
  platzierten DDC-Modulen bereitgestellte Kontingent je Typ, inaktiv →
  keine Verrechnung) inkl. einer weichen Budget-Warnung analog zur
  Reserve-Warnung – ohne befüllte Daten nicht sinnvoll baubar/testbar.
- Verifiziert per synthetischem Python-Test (WSL) gegen die geänderte
  Extraktionslogik: ohne `automationsanbindung` → keine `dp_*`-Felder
  (Regression-Schutz für die ~40 unveränderten Bauteile); DDC-Modul mit
  8/8/4/4-Verteilung → korrekt übernommen; Sensor mit nur 1× AI → korrekt;
  `automationsanbindung=true` ganz ohne `dp_*`-Werte → nur das Flag, keine
  Nullen. `zeilenumbruch_davor`→`bt.rowBreak` ebenso synthetisch geprüft.
  `python3 -m py_compile xlsx_to_json.py` fehlerfrei.

### Modul 4 – DDC-Datenpunkte: dynamische Verbrauchsrechnung & Auto-Modul-Platzierung (Session 28d, gesperrt)
Löst den in Session 28c bewusst zurückgestellten Laufzeit-Teil ein: die
Excel-Struktur allein verbrauchte noch keine Datenpunkte. Vier
Design-Entscheidungen vom Nutzer bestätigt (Standardempfehlung jeweils
übernommen):
1. **Eigener Reserve-Wert für Datenpunkte** (`ddc_reserve_pct`, Default
   20 %, Muster identisch zu `reserve_pct`/`klemmraum_mm`, eigenes
   Eingabefeld „Reserve Datenpunkte (%)") – bewusst getrennt von der
   Schaltschrank-Reserve, da physikalisch andere Ressource.
2. **Auto-Module sichtbar in einem eigenen Abschnitt** unterhalb der
   Belegungsliste (`#ddc-auto-liste`, `.bel-zeile-auto`: gestrichelter
   Rahmen, kursiv, kein „×"/„−" – nicht editierbar).
3. **Vollständig zustandslos** (wie die Klemmen-Reserve-Umverteilung):
   keine persistierte Modul-Zeile in `belegung`, sondern bei jedem
   `calculate()`-Aufruf komplett neu aus dem aktuellen Bedarf berechnet –
   wird eine Baugruppe/ein Bauteil entfernt, sinkt die berechnete
   Modul-Stückzahl automatisch mit, ohne manuelles Eingreifen.
4. **Feldbus-Typ muss exakt passen** – ein `dp_fb_bi`-Bedarf kann nur
   durch ein Modul gedeckt werden, das selbst `dp_fb_bi` bereitstellt;
   kein Modul verfügbar → Datenpunkttyp landet in `unmet`, keine
   automatische Platzierung, stattdessen weiche Warnung.

**Kernstück `computeDdcAutoModules(demand, supply, reservePct)`** (neu,
vor `placeBauteile()`): je Datenpunkttyp (`DP_TYPES`, 8 Werte, neue
Konstante analog `DP_FELDER` in `xlsx_to_json.py`) `requiredWithReserve =
demand/(1-reservePct)`, `remaining = max(0, requiredWithReserve -
supply)`. Für jeden Typ mit `remaining>0`: passendes `ddc_io`-Modul aus
`EINZELBAUTEILE_DB` suchen (nur `automationsanbindung=true`), das diesen
Typ bereitstellt – bei mehreren Kandidaten wird das Modul bevorzugt, das
die meisten der *aktuell noch offenen* Typen gleichzeitig abdeckt (verhindert
unnötiges Mischen verschiedener Modultypen), Stückzahl = Maximum über alle
von diesem Modul gedeckten offenen Typen von `ceil(remaining/kapazität)`.
Nach Zuweisung werden alle davon betroffenen `remaining`-Werte reduziert,
sodass bereits gedeckte Typen beim Durchlaufen der restlichen `DP_TYPES`
übersprungen werden. Kein Kandidat gefunden → Typ landet in `unmet`.
Bekannte Vereinfachung (dokumentiert, nicht Session-blockierend): die
Kandidatenauswahl ist ein einfacher Greedy-Heuristik, kein globales
Optimum über alle Typen hinweg – bei aktuell nur einem verlässlich
befüllten Modul (PXA30-W2) ohne praktische Auswirkung.

**Bedarf/Angebot-Ermittlung in `placeBauteile()`:** neue `accumulateDp(eb,
menge)`-Hilfsfunktion, aufgerufen für jedes Bauteil beim bestehenden
Queue-Aufbau (Baugruppen-aufgelöst UND Direktbauteile) – bei
`automationsanbindung=true` fließt es abhängig von `bauteil_typ` entweder
in `dpDemand` (Verbraucher) oder `dpSupply` (bereits manuell platzierte
`ddc_io`-Module) je Typ ein. Danach werden die von
`computeDdcAutoModules()` ermittelten Zusatz-Module direkt in
`queues.steuer` eingefügt (`auto:true`-Flag, Titel-Suffix „(automatisch
ergänzt)", Farbe `#6B6862` neutral-grau statt Baugruppen-Farbe) und
durchlaufen ab dort exakt dieselbe `placeInBands()`-Platzierung wie
manuell hinzugefügte Bauteile – landen automatisch in der Stückliste
(`aggregateStueckliste()` aggregiert ohnehin nach `artikel_nr`/Zone aus
den platzierten Blöcken, keine Änderung dort nötig).
`placeBauteile()`-Rückgabe erweitert um `ddcAuto` (`{modules, unmet}`),
`calculate()` reicht es an neue Funktion `updateDdcAutoDisplay()` durch
(rendert `#ddc-auto-liste`, toggelt `#ddc-warn` mit dynamischem Tooltip,
der die konkret unerfüllten Typen benennt – analog `updateReserveWarning()`,
aber bewusst getrennt, da inhaltlich andere Ressource).
- **Bewusst nicht Teil dieser Session:** eine echte Multi-Typ-Optimierung
  der Modulauswahl (aktuell Greedy); Berücksichtigung der Feldbus-Typen in
  der Praxis (kein Katalogeintrag hat bisher `dp_fb_*`-Kapazität – jeder
  Feldbus-Bedarf erzeugt aktuell immer die Warnung).
- Verifiziert direkt gegen die produktiven Funktionen im Browser: kleiner
  Bedarf ohne Angebot → 1× PXA30-W2 (rechnerisch: 2 AI/5 BI Bedarf,
  20 % Reserve → 1 Modul reicht für beides gleichzeitig); hoher Bedarf →
  4× PXA30-W2; Bedarf bereits durch vorhandenes Angebot gedeckt → keine
  Auto-Module; Feldbus-Bedarf ohne Katalog-Match → `unmet` korrekt,
  Warnsymbol aktiv, keine Platzierung. End-to-End mit temporärem
  Test-Sensor-Bauteil (nur in-memory, nicht persistiert) bestätigt: Queue-
  Aufbau, Sidebar-Anzeige und tatsächliche physische Platzierung über
  `placeInBands()` funktionieren zusammen korrekt. `EINZELBAUTEILE_DB` im
  Browser-Cache war beim ersten Testlauf veraltet (Server liefert frische
  Daten, reines Client-Cache-Problem des Testbrowsers) – nach Neuladen
  ohne Cache bestätigt, kein Code-Bug.

### Modul 4 – DDC-Fachwissen & Auto-Modul-Ratchet statt Auto-Reduktion (Session 28e, gesperrt)
**Fachliche Klarstellung vom Nutzer (Grundlage für die künftige
Excel-Struktur, in dieser Session noch nicht umgesetzt):** eine vollständige
DDC-Automationseinrichtung besteht aus Spannungsversorgung (Netzteil einer
Baureihe), CPU, mehreren E/A-Modulen mit physikalischen Datenpunkten
(AI/AO/BI/BO) und optional Kommunikationsmodulen für Feldbus-Integration
(FB_AI/FB_AO/FB_BI/FB_BO). **Wichtig:** die CPU selbst verarbeitet
Datenpunkte, erlaubt aber keinen elektrischen Anschluss – das leisten
ausschließlich die E/A-Module. Der in Session 28c/28d gewählte Ansatz
(`bauteil_typ==='ddc_io'` als Kapazitätsquelle, `dp_*`-Felder je Typ) wurde
vom Nutzer als grundsätzlich richtig bestätigt. **Offen für eine spätere
Session:** eine Excel-Struktur, die CPU, Netzteil und E/A-Module sauber
unterscheidbar macht (aktuell modelliert `bauteil_typ:'ddc_io'` nur
E/A-Kapazität – CPU/Netzteil-Bauteile mit eigener Rolle existieren im
Katalog noch nicht).

**Korrektur der Auto-Modul-Reduktion aus Session 28d:** die dort getroffene
Nutzer-Entscheidung „Modul wird automatisch mitreduziert" wurde nach
Rücksprache revidiert. Begründung: DBACS hat keine feste Positions-/
Kanalzuordnung einzelner Feldgeräte zu einzelnen I/O-Kanälen eines Moduls.
Sinkt der Bedarf und die Modulanzahl wird rein aus der aktuellen Summe neu
berechnet, ist nicht bekannt, WELCHES konkrete Modul entfallen würde, und
die verbleibenden Module rücken nicht automatisch auf einen festen Platz
auf. Ein real installiertes Modul wird in der Praxis auch nicht spontan
wieder ausgebaut, nur weil ein Bauteil aus der Planung entfernt wird. Die
vollständige Lösung (Kanal-/Positionstracking je Feldgerät) ist ein
eigenständiges konzeptionelles Thema für eine spätere Session.
- **Neuer Mechanismus – Ratchet statt Neuberechnung:** neue globale
  State-Variable `ddcWatermark` (`{artikel_nr: höchste bisher berechnete
  Menge}`, persistiert als `m04_ddc_watermark`, geladen beim Start wie
  `belegung`). Neue Funktion `applyDdcWatermark(ddcAuto)` (aufgerufen in
  `placeBauteile()` direkt nach `computeDdcAutoModules()`): hebt jede
  Modul-Menge im Ergebnis auf mindestens den bisherigen Watermark-Wert an
  und aktualisiert den Watermark nach oben, wenn der aktuelle Bedarf ihn
  übersteigt. Ein Artikel, der im aktuellen Durchlauf gar keinen Bedarf
  mehr hat (nicht in `ddcAuto.modules` enthalten), wird trotzdem mit
  seinem Watermark-Stand wieder in die Liste aufgenommen, sofern der
  Katalogeintrag noch existiert.
- `computeDdcAutoModules()` selbst bleibt unverändert eine reine,
  zustandslose Berechnungsfunktion (Bedarf/Angebot/Reserve → Ergebnis) –
  der Ratchet ist bewusst als separater Schritt danach implementiert,
  damit die Kernberechnung isoliert testbar bleibt.
- **Bewusst nicht Teil dieser Session:** eine Möglichkeit, den Watermark
  manuell zurückzusetzen (z. B. bei echtem Rückbau von Hardware oder
  Projekt-Neustart) – aktuell nur über direktes Löschen von
  `m04_ddc_watermark` im Browser-Speicher möglich, keine UI dafür.
- Verifiziert direkt gegen die produktiven Funktionen im Browser:
  hoher Bedarf → 2× PXA30-W2; Bedarf sinkt auf einen Wert, der rechnerisch
  nur noch 1 Modul rechtfertigen würde → bleibt bei 2 (Ratchet hält);
  Bedarf steigt über den bisherigen Watermark → wächst korrekt auf 4;
  `m04_ddc_watermark` persistiert korrekt zwischen den Aufrufen.

### Modul 4 – Eingabeleiste 2-zeiliges Grid, DDC-Zusammenfassung, Rowbreak nur Einzelbauteile (Session 28f, gesperrt)
Nach Live-Test mit allen bisherigen Session-28-Änderungen drei Beobachtungen:

- **Eingabeleiste brach unkontrolliert um:** „Spezifische Auswahl
  Einzelbauteile" rutschte bei normaler Fensterbreite in eine eigene Zeile
  (reines Flexbox-`flex-wrap`, kein kontrollierter Umbruch), was die
  Schranksicht darunter verkleinerte. **Fix:** `.eingabeleiste` von Flexbox
  auf CSS Grid umgestellt (`grid-template-columns:max-content auto 1fr`,
  2 Zeilen). Zeile 1 = linke Feldgruppe (Schranktyp…Reserve Datenpunkte,
  `.eb-row1-left`) + Funktionsbereich (`.eb-funktionsbereich`); Zeile 2 =
  DDC-Zusammenfassung (`#ddc-summary-field`, Spalte 1 – direkt unter der
  linken Feldgruppe) + Baugruppe/Einzelbauteile (`.eb-row2-right`, Spalte 3
  – Baugruppe beginnt dadurch exakt auf derselben x-Position wie
  Funktionsbereich in Zeile 1, da beide dieselbe Grid-Spalte nutzen; kein
  manuelles Breiten-Abgleichen nötig). Ein durchgehender Trenner
  (`.eb-sep-vert`, `grid-row:1/3`) trennt beide Spalten über beide Zeilen
  hinweg als ein zusammenhängender Block. Verifiziert per
  `getBoundingClientRect()` im Browser bei 1280px und 1920px Breite: `x`
  von `#ddc-summary-field` == `x` von `.eb-row1-left`, `x` von
  `.eb-row2-right` == `x` von `.eb-funktionsbereich`, exakte Übereinstimmung
  in beiden Fällen.
- **Neue DDC-Automationseinrichtung-Zusammenfassung** (`#ddc-summary-row`,
  `updateDdcSummary()`, aufgerufen aus `calculate()`): zeigt kompakt für
  jeden der 4 PHYSIKALISCHEN Datenpunkttypen (AI/AO/BI/BO – bewusst ohne
  Feldbus-Typen, Nutzer-Vorgabe) `belegt/Kapazität · Prozent` als Chip.
  `placeBauteile()` liefert dafür neu `ddcSummary` zurück: `cap = dpSupply
  + Summe(automatisch ergänzte Module × deren Kapazität)`, `used =
  dpDemand`. Farbcodierung wie Füllstand-Balken (>100% rot `.ddc-chip-over`,
  >80% amber `.ddc-chip-warn`, sonst neutral `.ddc-chip-ok`). Verifiziert:
  3× Testsensor (1 AI Bedarf) + 1 manuell platziertes PXA30-W2 (4 AI
  Kapazität) → „AI 3/4 · 75%" korrekt; ohne manuelles Modul (nur Bedarf,
  Auto-Modul greift) → Kapazität stammt korrekt aus dem automatisch
  ergänzten Modul.
- **„Neue Reihe"-Checkbox bei Baugruppe entfernt** (nur noch bei
  Einzelbauteile): Nutzer-Einwand berechtigt – eine Baugruppe besteht i. d. R.
  aus mehreren Bauteilen, unklar welches davon die neue Reihe erzwingen
  sollte. `#bg_rowbreak` aus HTML entfernt, `addBaugruppe()` liest/setzt
  kein `rowBreak` mehr, `firstDeviceOfItem`/`item.rowBreak`-Zweig in
  `placeBauteile()`s Baugruppen-Auflösung entfernt. Der **datengetriebene**
  `bt.rowBreak` (aus `baugruppen_bauteile`-Sheet, `zeilenumbruch_davor`,
  Beispiel „MSS über Schütz") bleibt unverändert bestehen – der beantwortet
  die „welches Bauteil"-Frage bereits explizit auf Bauteil-Ebene und ist
  von dieser Einschränkung nicht betroffen.
- **Gemeldeter "neue Reihe funktioniert nicht"-Bug:** ausführlich gegen die
  produktiven Funktionen nachgestellt (echte `addEinzelbauteil()` inkl.
  Checkbox, echte `placeBauteile()`, synthetische aber realistische
  Zonen-Geometrie über `m03_*`-localStorage, da der Testbrowser keinen
  echten Modul-1-3-Datenfluss hat). Mit ausreichend Zonenhöhe platziert der
  komplette Pfad (Checkbox → `belegung[i].rowBreak` → erstes Gerät der
  Queue → `placeInBands()`) korrekt in einer neuen Reihe – **kein Bug
  gefunden**. Bei knapper Zonenhöhe (Testfall 300 mm) verschwindet das
  zusätzliche Modul stattdessen korrekt in den harten Overflow (Kanal +
  neue Reihe passen nicht mehr), was sich falsch anfühlen kann, weil der
  Füllstand-Balken dabei täuschend niedrig bleibt (`mm_used` zählt nur
  tatsächlich Platziertes, nicht das, was durch Overflow verlorenging) –
  vermuteter, aber nicht am Originalfall verifizierter Zusammenhang mit dem
  gemeldeten Verhalten. Nicht abschließend geklärt, da die exakte reale
  Zonen-Geometrie des Nutzers nicht reproduzierbar war; falls der Bug nach
  diesem Layout-Fix weiter auftritt, mit konkretem Artikel + Menge +
  sichtbarem Overflow-Status ("!" im Schrankbild ja/nein) erneut prüfen.

### Modul 4 – Platzierungs-Engine mit Einfüge-Cursor (Session 28g, gesperrt)
Der in Session 28f als "nicht abschließend geklärt" markierte Bug hatte doch
eine Code-Ursache: mit realem Test (2× Baugruppe "Lüftermotor 1-stufig bis
2 kW" + mehrfaches Hinzufügen "Desigo PX..." mit "neue Reihe"-Häkchen)
zeigte sich, dass ein erzwungener Zeilenwechsel auf ALLE gleichartigen
Geräte wirkte statt nur die gerade eingefügten, und Folge-Geräte sich immer
hinter der neuen Reihe einreihten statt in eine noch nicht volle Reihe
davor zurückzukehren. Ursache: `rowBreak` war ein klebriges Boolean auf dem
(ggf. über mehrere Klicks gemergten) Belegungseintrag, und `placeInBands()`
war ein reiner Vorwärts-Läufer ohne Rücksprung-Fähigkeit. Auf Vorschlag des
Nutzers wurde die Platzierungs-Engine grundlegend neu strukturiert (Phase 1
einer größeren, mehrteiligen Neugestaltung – Abstands-Datenschema,
Baugruppen-Editor-Modul und das Füllen der Excel-Datenlücke für das
MSS/Schütz-Beispiel sind bewusst zurückgestellte Folgephasen).

**Kein Merge über einen erzwungenen Wechsel hinweg** (`addEinzelbauteil()`):
ist die "neue Reihe"-Checkbox aktiv, wird IMMER ein neuer, eigenständiger
`belegung`-Eintrag angelegt (`rowBreak:true`), auch wenn derselbe Artikel
schon vorhanden ist – nie mehr in einen bestehenden Eintrag gemergt. Nur
unforcierte Einfügungen mergen weiterhin, und auch nur in einen ebenfalls
unforcierten bestehenden Eintrag. Jede erzwungene Aktion bekommt so eine
eigene, stabile Identität, deren `rowBreak` sich nie rückwirkend auf
früher platzierte Einheiten desselben Artikels auswirkt. `queues[zone]`
bekommt `rowBreak` jetzt für ALLE Einheiten eines forcierten Eintrags
(vorher nur für Einheit 0) – sonst würde nur das erste von mehreren
gleichzeitig hinzugefügten Geräten gruppiert, der Rest fiele zurück in die
normale Reihe (im Test direkt aufgefallen: 2× "neue Reihe" mit Menge>1
gruppierte nur je 1 Gerät korrekt). `removeEinzelbauteilQty()`: sucht jetzt
vom ZULETZT hinzugefügten passenden Eintrag rückwärts (nicht vom ersten),
da seit dieser Session mehrere Einträge desselben Artikels nebeneinander
existieren können.

**`placeInBands()` komplett neu strukturiert – zwei Durchläufe statt einem:**
- *Durchlauf 1* (neue Funktion `assignDevicesToRows()`): ordnet Geräte
  abstrakten Reihen zu (nur Blöcke + Höhe, keine Y-Position, keine
  Bandzuordnung) über zwei Cursor. `normalCursor` zeigt auf die Reihe, in
  die nicht-erzwungene Geräte weiter einsortiert werden (füllt bestehende
  Reihen zuerst auf, neue Reihe entsteht erst am ENDE der Liste, wenn
  nötig). `forcedCursor` zeigt auf die zuletzt für einen erzwungenen
  Wechsel angelegte Reihe – ein Gerät mit `rowBreak:true` versucht zuerst
  dort anzuhängen; reicht der Platz nicht (oder existiert noch keine), wird
  eine neue Reihe direkt nach der aktuellen `forcedCursor`- bzw. (beim
  allerersten Mal) `normalCursor`-Position eingefügt (`Array.splice`, nicht
  ans Ende!) – alle erzwungenen Einfügungen bleiben so als ein
  zusammenhängender Block gruppiert, unabhängig davon, wie viele normale
  Geräte inzwischen dazwischen hinzugefügt wurden. `normalCursor` bleibt
  von alldem unberührt, wodurch nachfolgende normale Geräte automatisch
  zur ursprünglichen Reihe zurückkehren.
- *Durchlauf 2* (im Funktionskörper von `placeInBands()`): berechnet
  Y-Positionen rein sequenziell aus der fertigen Reihenliste – Kanäle
  (`kanalPending`), Bandwechsel und Overflow inhaltlich wie bisher, aber
  jetzt nachgelagert statt live mitgeführt. Löst das
  Höhenwachstum-Verschiebeproblem praktisch von selbst: wächst eine
  frühere Reihe (weil Durchlauf 1 ein höheres Gerät dort eingefügt hat),
  rutscht in Durchlauf 2 automatisch alles Folgende (Kanäle, weitere
  Reihen) nach unten, da ohnehin komplett neu von oben positioniert wird –
  kein Sonderfall zum "Verschieben" nötig.
- **Bekannte, dokumentierte Vereinfachung:** Durchlauf 1 kennt die
  tatsächliche Bandzuordnung noch nicht und nutzt die Breite des ERSTEN
  Bandes der Zone als Näherung für die TE-Passt-Prüfung. Bei Zonen mit
  mehreren Bändern UNTERSCHIEDLICHER Breite (aktuell nicht der Fall –
  `leist`/`leist_ext` haben identische Breite) könnte das nachgeschärft
  werden müssen.
- Rückgabeform unverändert (`{rows, channels, overflow, mm_used}`) – kein
  Änderungsbedarf in `placeBauteile()`, `buildSVG()`, `buildFuellstand()`.
  `placeBauteile()`s Queue-Aufbau selbst brauchte keine strukturelle
  Änderung, nur den oben genannten `rowBreak`-Fix (alle statt nur Einheit 0).
- **Bewusst nicht Teil dieser Session (Folgephasen):** Abstands-/
  Positionierungs-Datenschema (Herstellervorgaben oben/unten/links/rechts,
  Wärmeabfuhr), Baugruppen-Editor-Modul, Excel-Datenlücke für
  `zeilenumbruch_davor` beim MSS/Schütz-Beispiel füllen.
- Verifiziert direkt gegen die produktiven Funktionen im Browser: alle 4
  im Plan festgelegten Testfälle bestehen exakt (getrenntes
  rowBreak-Scoping bei mehreren Einheiten, Rückkehr zum Normal-Cursor nach
  erzwungenem Wechsel, Höhenwachstum verschiebt nachfolgende Reihen/Kanäle
  korrekt, zwei erzwungene Wechsel ohne normales Gerät dazwischen landen in
  derselben Reihe); alle Session-28b/28c-Regressionstests (abschließender
  Kanal, Platzreserve, randvolle Zone, Steuertrafo-Szenario, Overflow)
  liefern identische Ergebnisse wie vor dem Umbau; End-to-End-Test mit dem
  exakten Screenshot-Szenario (2× Lüftermotor-Baugruppe + 5×/2× Desigo
  PXA30-W2/N mit "neue Reihe") bestätigt: Baugruppen-PXA30-N bleiben
  zusammen in der ursprünglichen Reihe, alle erzwungenen Einfügungen
  gruppieren sich korrekt in einer eigenen Reihe, kein Overflow.

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
- `zone_anordnung` (Nebeneinander/Übereinander) wird disabled wenn `zone_modus === 'je_feld'`
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
