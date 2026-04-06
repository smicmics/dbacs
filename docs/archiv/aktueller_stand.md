# DBACS – Aktueller Stand
**Zuletzt aktualisiert:** 06. April 2026

---

## Projektstruktur

```
dbacs/
├── index.html                              ← Startseite / Modulübersicht (fertig)
├── modules/
│   └── modul-01-schaltschrank/
│       └── index.html                      ← h_ke-Rechner (aktive Arbeitsdatei)
├── drawings/
│   └── wandschrank_frontansicht_v7.html    ← Referenzzeichnung (unverändert)
└── docs/
    ├── dbacs_session1_documentation.md
    ├── dbacs_session2_documentation.md
    └── aktueller_stand.md                  ← diese Datei
```

---

## Modul 1 – Status: funktionsfähig, lokal

Eingaben: Schrank-Außenmaße, Montageplatte, KE-Position (oben/unten), Kabel-∅, Kanaltiefe

Berechnungen korrekt:
- h_ke = h_handling_ke + h_zug_ke + h_kabel_bieg + h_kanal_ke
- h_kabel_bieg = 4 × d_max (VDE 0298-4)
- h_handling_ke = 15 mm (Festwert Wandschrank)
- h_zug_ke = 0 mm (PG außen, kein interner Platzbedarf)

SVG-Zeichnung korrekt:
- Zonendarstellung für KE oben und unten
- h_handling startet an Schaltschrankinnenwand
- PG-Verschraubungen sitzen direkt auf Gehäuse
- Alle Maßketten blau, 0.8 px, Schriftgröße 7
- B-Maß unten bei KE oben, B-Maß oben bei KE unten
- Nutzfläche-Pfeil zeigt in Einführungsrichtung

---

## Offene Punkte

**Priorität hoch**
- GitHub Pages Deployment – Dateien noch nicht veröffentlicht
- Testen im Browser nach Deployment (relative Pfade, keine Server-Abhängigkeiten)

**Priorität mittel**
- Modul 2: Stehender Schrank – wie Modul 1, aber h_zug_ke ≠ 0
- Zonenrechteck h_handling bei KE oben: Rechteck überlappt minimal die Gehäusekante (visuell unkritisch)

**Priorität niedrig**
- Responsive/Mobile-Layout verbessern
- CSS @media print für Druckausgabe
- Module 3–6 konzipieren

---

## Entscheidungen (nicht mehr hinterfragen)

- SVG dynamisch per JS, kein statisches SVG
- Feste SVG-Höhe 390 px, Skalierung sc = 390 / H_mm
- h_handling beginnt an Schaltschrankinnenwand, nicht an MP-Oberkante
- h_zug_ke = 0 für Wandschrank (PG außen)
- Alle Maßketten: #3366BB, 0.8 px, Größe 7
- PG bündig auf Gehäuse, kein Luftabstand
- b_mplatte_abstand nur in Ergebnistabelle, nicht in Zeichnung
- B-Maß positionsabhängig (oben bei KE unten, unten bei KE oben)
- UI dunkel, Zeichenfläche hell (Papier #FDFCF8)
- Single-File HTML pro Modul (kein Build-Step, GitHub Pages kompatibel)

---

## Nächste Sitzung – Einstieg

**Lesen:**
1. Diese Datei
2. `modules/modul-01-schaltschrank/index.html` ab Zeile 226 (JS-Teil)

**Fortsetzen mit:**
- GitHub Pages Deployment, oder
- Modul 2 beginnen (Stehender Schrank, h_zug_ke aktiv)
