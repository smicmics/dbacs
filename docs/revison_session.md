# DBACS – Revisionsstand
**Stand:** 06. April 2026

---

## Projektziel

Webbasiertes Planungstool für das Gewerk Gebäudeautomation zur Unterstützung der Schaltschrank-Dimensionierung in verschiedenen HOAI-Leistungsphasen, betrieben als statische GitHub Pages Anwendung.

---

## Stack / Architektur

**Technologien**
- Reines HTML/CSS/JavaScript – kein Framework, kein Build-Step
- Eine HTML-Datei pro Modul (Self-contained)
- SVG dynamisch per JavaScript erzeugt
- Datenhaltung geplant: SQLite via sql.js (WebAssembly), Pflege über Excel

**Warum so**
- GitHub Pages kompatibel ohne Server
- Kein Deployment-Aufwand
- Offline-fähig
- Erweiterbar Modul für Modul

**Dateistruktur**
```
dbacs/
├── CLAUDE.md                               Projektkonventionen für Claude (Session-Start)
├── web/
│   ├── index.html                          Startseite / Modulübersicht
│   └── assets/                             CSS + JS der Startseite
├── modules/
│   └── modul-01-schaltschrank/index.html  h_ke-Rechner (aktive Arbeitsdatei)
├── drawings/
│   └── wandschrank_frontansicht_v7.html   Referenzzeichnung (unverändert)
├── data/
│   ├── ga_komponenten.xlsx                Pflegewerkzeug (Source of Truth, noch leer)
│   └── ga_komponenten.db                 SQLite, generiert via Python (noch leer)
└── docs/
    └── *.md                               Projektdokumentation
```

---

## Stand heute

**Startseite (web/index.html)**
- Dark Theme, Modulübersicht mit 6 Karten
- Modul 1 verlinkt und aktiv, Module 2–6 als "geplant" markiert
- Footer: „Erstellt von: Stephan Michler · DBACS Planungstool · 2026"

**Modul 1 – Kabeleinführungszone h_ke (Wandschrank)**
- Eingaben: Schrank-Außenmaße, Montageplatte, KE-Position (oben/unten), Kabel-∅, Kanaltiefe
- Berechnung vollständig und korrekt implementiert
- Ergebnistabelle mit standardisierten Variablennamen (siehe Variablen-Konvention)
- Variablen-Labels im Eingabeformular zeigen kanonische Variablennamen
- SVG-Zeichnung dynamisch, skaliert auf jede Schrankhöhe
- Zwei Preset-Schränke (Rittal AX 1213, AX 1209)
- Footer: „Erstellt von: Stephan Michler · DBACS Planungstool · 2026"

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

**CLAUDE.md**
- Session-Start-Protokoll, Architekturregeln, Code-Konventionen, SVG-Konventionen
- Variablen-Konvention (modulübergreifend), Farbkodierung, Schriftgrößen-Steuerung
- Gesperrte Entscheidungen

**Noch nicht begonnen**
- Excel-Datenbankstruktur
- Python-Konvertierungsskript
- GitHub Pages Deployment

---

## Variablen-Konvention (modulübergreifend)

Verbindliche Variablennamen für alle Module, Ergebnistabellen und SQLite-Felder:

| Variable | Bedeutung | Einheit |
|---|---|---|
| `b_gehaeuse_aussen_mm` | Schrank-Außenbreite | mm |
| `h_gehaeuse_aussen_mm` | Schrank-Außenhöhe | mm |
| `b_mplatte_mm` | Montageplatte Breite | mm |
| `h_mplatte_mm` | Montageplatte Höhe | mm |
| `b_mplatte_abstand_gehaeuse_iw_mm` | Seitl. Abstand MP–Gehäuseinnenwand | mm |
| `h_mplatte_abstand_gehaeuse_iw_mm` | Oberer Abstand MP–Gehäuseinnenwand | mm |
| `d_max_kabel_ke_mm` | Max. Kabel-Außen-∅ KE-Zone | mm |
| `h_handling_ke_mm` | Freie Kabellänge nach PG | mm |
| `h_zug_ke_mm` | Zugentlastung intern | mm |
| `h_kabel_bieg_mm` | Mindestbiegeradius (4 × d_max) | mm |
| `h_kanal_ke_mm` | Horizontaler Kabelkanal KE-Zone | mm |
| `h_ke_mm` | Kabeleinführungszone gesamt | mm |

---

## Offene Punkte

**Als nächstes (Prio hoch)**
1. GitHub Pages Deployment – Dateien veröffentlichen, Pfade testen
2. Modul 2 – Stehender Schrank (wie Modul 1, aber h_zug_ke ≈ 35 mm aktiv)

**Mittelfristig**
3. Einspeisezone h_einsp erarbeiten (analog zu h_ke)
4. Klemmenzone h_klemm erarbeiten
5. TE-Berechnung pro Reihe und Gesamtkapazität
6. Excel-Datei mit Mustergeräten befüllen
7. Python-Konvertierungsskript implementieren

**Später**
8. Zonenrechteck h_handling bei KE oben bereinigen (überlappt minimal Gehäusekante)
9. Responsive Layout / Mobile
10. CSS @media print für Druckausgabe
11. Module 3–6 konzipieren

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

**Daten / Architektur**
- Single-File HTML pro Modul (GitHub Pages, kein Build-Step)
- Excel als Pflegewerkzeug (Source of Truth), SQLite als Produktivdatenbank
- Preise als Listenpreise mit Datum-Feld; Aktiv-Flag statt Löschung veralteter Datensätze
- TE-Berechnung als Formel, nicht als fester Wert im Schema
