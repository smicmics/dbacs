# DBACS – Revisionsstand
**Stand:** 12. April 2026 – Session 4

---

## Projektziel

Webbasiertes Planungstool für das Gewerk Gebäudeautomation zur Unterstützung der Schaltschrank-Dimensionierung in verschiedenen HOAI-Leistungsphasen, betrieben als statische GitHub Pages Anwendung.

---

## Stack / Architektur

**Technologien**
- Reines HTML/CSS/JavaScript – kein Framework, kein Build-Step
- Eine HTML-Datei pro Modul (Self-contained)
- SVG dynamisch per JavaScript erzeugt
- Datenhaltung: Excel → Python (WSL) → JSON → fetch() im Browser

**Warum so**
- GitHub Pages kompatibel ohne Server
- Kein Deployment-Aufwand
- Offline-fähig
- Erweiterbar Modul für Modul

**Dateistruktur**
```
dbacs/
├── CLAUDE.md                               Projektkonventionen für Claude (Session-Start)
├── index.html                              Root-Redirect → web/index.html (GitHub Pages)
├── .gitignore                              OS, Editor, Python, data/*.db, data/*.xlsx, settings.local.json
├── .claude/
│   └── launch.json                         Dev-Server-Konfiguration (statischer HTTP-Server Port 8099)
├── web/                                    ← erstellt Session 2 (12.04.2026)
│   ├── index.html                          Startseite / Modulübersicht (Dark Theme)
│   └── assets/
│       ├── css/style.css                   Dark Theme Stylesheet
│       └── js/main.js                      Scroll-Reveal + aktive Nav-Link-Steuerung
├── modules/
│   └── modul-01-schaltschrank/index.html  h_ke-Rechner (aktive Arbeitsdatei)
├── drawings/
│   └── wandschrank_frontansicht_v7.html   Referenzzeichnung (unverändert)
├── data/
│   ├── ga_komponenten.xlsx                Pflegewerkzeug (Source of Truth, lokal – nicht versioniert)
│   ├── kabel_nym_j.json                   Kabeldatenbank NYM-J (committed, aus Excel generiert)
│   ├── wandschraenke.json                 Wandschrank-DB Rittal AX (committed, aus Excel generiert)
│   └── xlsx_to_json.py                    Konvertierungsskript Excel → JSON (WSL: python3)
└── docs/
    └── *.md                               Projektdokumentation
```

**Deployment**
| | |
|---|---|
| Repository | https://github.com/smicmics/dbacs |
| Live-URL Startseite | https://smicmics.github.io/dbacs/ |
| Live-URL Modul 1 | https://smicmics.github.io/dbacs/modules/modul-01-schaltschrank/ |
| Deploy-Trigger | Push auf `main` Branch → GitHub Pages baut automatisch |
| Branch / Quelle | `main` / Root (`/`) |

---

## Stand heute

**Startseite (web/index.html)** ← erstellt Session 2 (12.04.2026)
- Dark Theme (`#0d1117` Basis, Blau-Akzente, Grün für aktive Zustände)
- Sektionen: Hero, Modulübersicht, Architektur, Pflegeworkflow, Projektstatus, Footer
- Modulübersicht: Modul 1 aktiv verlinkt, Module 2–5 als „Geplant" markiert
- Scroll-Reveal-Animation, aktive Nav-Link-Hervorhebung via IntersectionObserver
- Footer: „Erstellt von: Stephan Michler · DBACS Planungstool · 2026"
- Responsive (mobile: Nav ausgeblendet, einspaltig)

**Modul 1 – Kabeleinführungszone h_ke (Wandschrank)**
- Eingaben: Schrank-Außenmaße, Montageplatte, KE-Position (oben/unten), Kanaltiefe
- Kabelauswahl: Aderzahl (3/4/5/7) + Querschnitt (1,5–16 mm²) → d_max aus JSON-DB
- d_max bleibt manuell überschreibbar (Sonderkabel)
- Berechnung vollständig und korrekt implementiert
- Ergebnistabelle mit standardisierten Variablennamen (siehe Variablen-Konvention)
- Variablen-Labels im Eingabeformular zeigen kanonische Variablennamen
- SVG-Zeichnung dynamisch, skaliert auf jede Schrankhöhe
- Wandschrank-Auswahl: einzelnes Dropdown, befüllt aus `wandschraenke.json`
- Standardauswahl beim Laden: Rittal AX 1214.000 · KE oben · 5×6 mm²
- Footer: „Erstellt von: Stephan Michler · DBACS Planungstool · 2026"

**Kabeldatenbank (Session 3)**
- `data/kabel_nym_j.json` – 18 NYM-J Typen (3/4/5/7 Adern, 1,5–16 mm²), Richtwerte Draka 2024
- fetch() lädt JSON beim Seitenaufruf; Fallback: d_max manuell eingebbar

**Wandschrank-Datenbank (Session 4)**
- `data/wandschraenke.json` – 12 Rittal AX-Wandschränke, ab 600×600 mm
- Sheet `wandschraenke` in `ga_komponenten.xlsx` angelegt (13 Spalten, siehe Schema)
- Preisfelder vorhanden (noch nicht befüllt): Stückpreis, Lieferung, Montage, Gesamt
- Preisfelder werden in Modul 1 nicht ausgewertet – für spätere Module vorgesehen
- Modelle: AX 1060, 1054, 1090, 1209, 1091, 1260, 1261, 1180, 1100, 1110, 1213, 1214

**Excel-Schema Sheet `wandschraenke`**

| Spalte | Typ | Beschreibung |
|---|---|---|
| `aktiv` | BOOL | FALSE = nicht exportiert |
| `hersteller` | TEXT | z.B. „Rittal" |
| `bezeichnung` | TEXT | z.B. „AX 1214.000" |
| `bestellnummer` | TEXT | Artikelnummer |
| `b_gehaeuse_aussen_mm` | INT | Außenbreite mm |
| `h_gehaeuse_aussen_mm` | INT | Außenhöhe mm |
| `t_gehaeuse_aussen_mm` | INT | Außentiefe mm |
| `b_mplatte_mm` | INT | Montageplatte Breite mm |
| `h_mplatte_mm` | INT | Montageplatte Höhe mm |
| `preis_stueckpreis_eur` | FLOAT | Schrank + MP + Montagezubehör |
| `preis_lieferung_eur` | FLOAT | Lieferkosten |
| `preis_montage_eur` | FLOAT | Montage-DL (Aufhängung) |
| `preis_gesamt_eur` | FLOAT | Gesamtpreis |

**xlsx_to_json.py (Session 4 – refactored)**
- Exportiert jetzt beide Sheets: `kabel_nym_j` → `kabel_nym_j.json` und `wandschraenke` → `wandschraenke.json`
- Aufruf unverändert: `python3 xlsx_to_json.py` aus dem `data/`-Verzeichnis in WSL

**SVG-Zeichnung – Qualität**
- Zonendarstellung korrekt für KE oben und KE unten
- h_handling_ke beginnt an der Schaltschrankinnenwand
- PG-Verschraubungen bündig auf Gehäuse, beide identisch (kein Leerkreis-Indikator)
- Kabelstub 10 px sichtbar über/unter PG-Nase, gleiche Länge für KE oben und KE unten
- Kabelstub wird vor pgBody gezeichnet, PG überdeckt den Innenbereich
- Nutzfläche-Pfeil zeigt in Kabeleinführungsrichtung (▼ / ▲)
- B-Maßlinie unten bei KE oben, oben bei KE unten
- Alle Maßketten: blau #3366BB, 0.8 px
- Maßlinie 16 px vom Gehäuse; Maßkettentext-Baseline 2 px oberhalb der Maßlinie
- h_handling_ke-Label bei KE unten: 2 px nach oben versetzt (vermeidet Schnitt mit h_ke-Maßlinie)

**Schriftgrößen-Steuerung**
- Drei Eingabefelder im Panel: Bemaßungstext (7), Bemaßungsvariable (6), Zonenbeschreibung (7)
- Wert 0 blendet gesamte Gruppe aus (Linien, Pfeile, Text) → Druckoptimierung
- Innen-Labels (Maßangaben im Gehäuse): einheitlich 7 pt

**Farbkodierung Ergebnistabelle + Formelzeile**
- h_handling_ke: Grün `#2DBD8E`
- h_kabel_bieg: Orange `#C8720E`
- h_kanal_ke: Lila `#9A94E8`
- h_zug_ke: Grau `#9A9890` (für Wandschrank nicht relevant, keine Hervorhebung)
- Farben in Formelzeile und Tabellenspalten identisch

**GitHub Pages Deployment**
- Repository: https://github.com/smicmics/dbacs (öffentlich)
- Deployment über GitHub Pages, Branch `main`, Root `/`
- Root `index.html` leitet per Meta-Refresh auf `web/index.html` weiter
- `.gitignore` schützt lokale Dateien (data/*.db, data/*.xlsx, .claude/settings.local.json)
- Stand Session 4: Änderungen noch nicht committed (ausstehend)

---

## Variablen-Konvention (modulübergreifend)

Verbindliche Variablennamen für alle Module, Ergebnistabellen und JSON-Felder:

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
| `d_max_kabel_ke_mm` | Max. Kabel-Außen-∅ KE-Zone (aus DB) | mm |
| `h_handling_ke_mm` | Freie Kabellänge nach PG | mm |
| `h_zug_ke_mm` | Zugentlastung intern | mm |
| `h_kabel_bieg_mm` | Mindestbiegeradius (4 × d_max) | mm |
| `h_kanal_ke_mm` | Horizontaler Kabelkanal KE-Zone | mm |
| `h_ke_mm` | Kabeleinführungszone gesamt | mm |

---

## Offene Punkte

**Als nächstes (Prio hoch)**
1. Modul 2 – Stehender Schrank (wie Modul 1, aber h_zug_ke ≈ 35 mm aktiv)
2. Außendurchmesser NYM-J in Excel mit echten Herstellerdaten verifizieren und ggf. korrigieren
3. Preisfelder Wandschrank-DB befüllen (Rittal Listenpreise recherchieren)

**Mittelfristig**
4. Einspeisezone h_einsp erarbeiten (analog zu h_ke)
5. Klemmenzone h_klemm erarbeiten
6. TE-Berechnung pro Reihe und Gesamtkapazität
7. Excel-Datei mit Mustergeräten befüllen

**Später**
8. Zonenrechteck h_handling bei KE oben bereinigen (überlappt minimal Gehäusekante)
9. Startseite: Screenshot-Vorschau je Modul ergänzen
10. CSS @media print für Druckausgabe (Modul 1)
11. Module 3–5 konzipieren und in Startseite integrieren

---

## Entscheidungen

**Formel h_ke**
- h_ke = h_handling_ke + h_zug_ke + h_kabel_bieg + h_kanal_ke
- Biegeradius-Faktor 4 × Außen-∅ (VDE 0298-4, fest verlegt – nicht 6×, das gilt für flexible Leitungen)
- h_zug_ke = 0 mm beim Wandschrank (PG-Zugentlastung sitzt außen am Gehäuse)
- h_handling_ke = 15 mm Festwert Wandschrank (liegt im Spalt MP–Innenwand, kein zusätzlicher MP-Platzbedarf, dennoch konservativ eingerechnet)
- h_kanal_ke = 60 mm Standard Wandschrank (Standschrank ggf. 80 mm)
- h_handling beginnt an der Schaltschrankinnenwand, nicht an der MP-Oberkante

**SVG / Darstellung**
- SVG dynamisch per JavaScript erzeugt, keine statische Grafik
- Feste SVG-Höhe SH=390 px, Skalierungsfaktor sc = SH/H_mm
- UI dunkel, Zeichenfläche hell (Papier #FDFCF8) für Druckbarkeit
- Alle Maßketten einheitlich blau #3366BB, 0.8 px
- Schriftgrößen sind Nutzereingaben (fs_dim=7, fs_var=6, fs_zone=7); Wert 0 = Gruppe ausblenden
- Maßlinie 16 px vom Gehäuse; Maßkettentext-Baseline 2 px oberhalb der Maßlinie
- PG-Verschraubungen bündig auf Gehäuse, beide identisch (pgBody ohne hasKabel-Flag)
- Kabelstub 10 px sichtbar past PG-Nase; vor pgBody zeichnen (PG überdeckt Innenbereich)
- B-Maßlinie positionsabhängig (unten bei KE oben, oben bei KE unten)
- b_mplatte_abstand_gehaeuse_iw_mm nur in Ergebnistabelle, nicht in Zeichnung
- h_handling_ke-Label bei KE unten: dy=-2 (Versatz vermeidet Schnitt mit h_ke-Maßlinie)

**Farbkodierung**
- h_ke-Komponenten in Tabelle und Formel einheitlich eingefärbt (grün/orange/lila)
- h_zug_ke bleibt grau (für Wandschrank nicht relevant)

**Wandschrank-Dropdown (Session 4)**
- Einzelnes `<select>`-Dropdown statt Preset-Buttons (kein hardcodiertes `const PRESETS` mehr)
- Optionen werden dynamisch per fetch() aus `wandschraenke.json` befüllt
- Auswahl befüllt nur Gehäusegeometrie (B, H, mp_b, mp_h) – Kabelfelder und KE-Position bleiben Nutzereingabe
- Standardauswahl: `opt.selected = true` direkt am Option-Element (zuverlässiger als `sel.value = idx`)
- Default-Schrank: AX 1214.000 (Rittal, 1000×1200×400 mm)
- Default-Kabel: 5×6 mm² · KE-Position: oben

**Daten / Architektur**
- Single-File HTML pro Modul (GitHub Pages, kein Build-Step)
- Excel als Pflegewerkzeug (Source of Truth), JSON als Produktivdatenbank
- `xlsx_to_json.py` exportiert beide Sheets in einem Aufruf
- Preise als Listenpreise; Aktiv-Flag statt Löschung veralteter Datensätze
- TE-Berechnung als Formel, nicht als fester Wert im Schema
