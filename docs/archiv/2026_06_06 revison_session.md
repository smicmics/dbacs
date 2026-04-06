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
├── index.html                              Startseite / Modulübersicht
├── modules/
│   └── modul-01-schaltschrank/index.html  h_ke-Rechner (aktive Arbeitsdatei)
├── drawings/
│   └── wandschrank_frontansicht_v7.html   Referenzzeichnung (unverändert)
├── data/
│   ├── ga_komponenten.xlsx                Pflegewerkzeug (Source of Truth)
│   └── ga_komponenten.db                 SQLite, generiert via Python
└── docs/
    └── *.md                               Projektdokumentation
```

---

## Stand heute

**Startseite**
- Dark Theme, Modulübersicht mit 6 Karten
- Modul 1 verlinkt und aktiv, Module 2–6 als "geplant" markiert

**Modul 1 – Kabeleinführungszone h_ke (Wandschrank)**
- Eingaben: Schrank-Außenmaße, Montageplatte, KE-Position (oben/unten), Kabel-∅, Kanaltiefe
- Berechnung vollständig und korrekt implementiert
- Ergebnistabelle mit allen Zwischenwerten
- SVG-Zeichnung dynamisch, skaliert auf jede Schrankhöhe
- Zwei Preset-Schränke (Rittal AX 1213, AX 1209)

**SVG-Zeichnung – Qualität**
- Zonendarstellung korrekt für KE oben und KE unten
- h_handling_ke beginnt an der Schaltschrankinnenwand
- PG-Verschraubungen sitzen bündig auf dem Gehäuse (oben und unten)
- Kabelstub symmetrisch (nach oben / nach unten je nach KE-Seite)
- Nutzfläche-Pfeil zeigt in Kabeleinführungsrichtung (▼ / ▲)
- B-Maßlinie unten bei KE oben, oben bei KE unten
- Alle Maßketten: blau #3366BB, 0.8 px, Schriftgröße 7
- H- und B-Maßtext mit einheitlichem Abstand zur Maßlinie

**Noch nicht begonnen**
- Excel-Datenbankstruktur (Blatt schraenke_wand angelegt, Mustergeräte fehlen)
- Python-Konvertierungsskript (Struktur dokumentiert, nicht implementiert)
- GitHub Pages Deployment

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
- Feste SVG-Höhe 390 px, Skalierungsfaktor sc = 390 / H_mm
- UI dunkel, Zeichenfläche hell (Papier #FDFCF8) für Druckbarkeit
- Alle Maßketten einheitlich blau #3366BB, 0.8 px, Größe 7
- PG-Verschraubungen bündig auf Gehäuse, kein Luftabstand
- B-Maßlinie positionsabhängig (unten bei KE oben, oben bei KE unten)
- b_mplatte_abstand_ssiw nur in Ergebnistabelle, nicht in Zeichnung

**Daten / Architektur**
- Single-File HTML pro Modul (GitHub Pages, kein Build-Step)
- Excel als Pflegewerkzeug (Source of Truth), SQLite als Produktivdatenbank
- Preise als Listenpreise mit Datum-Feld; Aktiv-Flag statt Löschung veralteter Datensätze
- TE-Berechnung als Formel, nicht als fester Wert im Schema
