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
│   └── xlsx_to_json.py                          Konvertierungsskript Excel → JSON (6 Sheets)
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
