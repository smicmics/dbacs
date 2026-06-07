# DBACS – Revisionsstand
**Stand:** 7. Juni 2026 – Session 7

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
├── web/
│   ├── index.html                          Startseite / Modulübersicht (Dark Theme)
│   └── assets/
│       ├── css/style.css                   Dark Theme Stylesheet
│       └── js/main.js                      Scroll-Reveal + aktive Nav-Link-Steuerung
├── modules/
│   └── modul-01-schaltschrank/index.html  Modul 1 – vollständig funktionsfähig
├── drawings/
│   └── wandschrank_frontansicht_v7.html   Referenzzeichnung (unverändert)
├── data/
│   ├── ga_komponenten.xlsx                Pflegewerkzeug (Source of Truth, lokal – nicht versioniert)
│   ├── kabel_nym_j.json                   Kabeldatenbank NYM-J (committed)
│   ├── wandschraenke.json                 Wandschrank-DB Rittal AX (committed)
│   ├── kabelzugschellen.json              Kabelzugschellen-DB Icotek CCL (committed) ← NEU Session 6
│   └── xlsx_to_json.py                    Konvertierungsskript Excel → JSON (alle 3 Sheets)
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

### Modul 1 – vollständig funktionsfähig ✅
**Titel:** „Modul 1 · Wandschrank · Kabeleinführung · Nutzfläche"

**Berechnungsformel h_ke_mm (aktuell)**
```
h_ke_mm = h_handling_ke_mm + h_kabel_bieg_mm + h_zug_ke_mm + h_handling_zug_ke_mm + h_kanal_ke_mm
```

Reihenfolge der Zonen ab Gehäuseinnenwand (fest):
1. `h_handling_ke_mm` – freie Kabellänge nach PG (Festwert 15 mm)
2. `h_kabel_bieg_mm` – Mindestbiegeradius (4 × d_max, VDE 0298-4)
3. `h_zug_ke_mm` – Bügelschellen-Höhe (aus DB, 0 wenn inaktiv)
4. `h_handling_zug_ke_mm` – Freiraum nach Schelle bis Kabelkanal/Gerät (Festwert 20 mm, 0 wenn inaktiv)
5. `h_kanal_ke_mm` – horizontaler Kabelkanal (Eingabe, 0 wenn inaktiv)

**Eingabepanel**
- Schrank-Außenmaße + Montageplatte
- Wandschrank-Dropdown (Rittal AX, aus `wandschraenke.json`)
- Kabeleinführung: Position oben/unten, Aderzahl, Querschnitt → d_max aus `kabel_nym_j.json`
- **Kabelkanal:** Ja/Nein-Toggle + Höheneingabe (bei Nein: h_kanal = 0)
- **Zugentlastung im Schaltschrank:** Ja/Nein-Toggle → bei Ja: DB-Lookup in `kabelzugschellen.json` nach d_max, Schellentyp und h_schelle_mm werden angezeigt
- Schriftgrößen SVG (fs_dim, fs_var, fs_zone), Wert 0 blendet Gruppe aus
- Festwerte (nicht editierbar): h_handling_ke=15 mm, h_handling_zug_ke=20 mm, Biegeradiusfaktor 4×

**SVG-Zeichnung**
- Zonendarstellung für KE oben und KE unten korrekt
- Zonen in SVG (alle nur wenn > 0): Handling (hellgrau), Bieg (warmgelb), Zug/Schelle (amber, gestrichelter Rahmen), Handling-Zug (hellblau, gestrichelter Rahmen), Kabelkanal (grau, Fülllinien)
- **C-Profilschiene** maßstabsgerecht in h_zug-Zone gezeichnet: Grundkörper + Flanken + C-Nut
- **Bügelschelle** am Kabel (x = bxo) als U-Bügel mit Schraube
- Maßketten: alle Teilmaße in einheitlichem Blau `#3366BB` (wie h_mplatte_mbereich_mm)
- Zonenbeschriftungen (Kabeleinführungszone, C-Schiene mit Bügelschellen, Kabelkanal Einführungszone): linksbündig, 10 px rechts vom Kabel (`zoneLblX = bxo + 10`)
- ▼/▲ Beginn/Ende Nutzfläche: zentriert bei mx+mw/2
- Teilmaß-Labels: `dominant-baseline="middle"` für exakte vertikale Zentrierung (außer h_handling_ke_mm)
- h_mplatte_mbereich_mm: Maßlinie von KE-Ende bis MP-Ende

**Ergebnistabelle + Formelzeile**

Farbkodierung (Formelzeile und Tabellenzeile immer identisch):

| Variable | Farbe |
|---|---|
| `h_handling_ke_mm` | Grün `#2DBD8E` |
| `h_kabel_bieg_mm` | Orange `#C8720E` |
| `h_zug_ke_mm` | Amber `#D4A84B` (immer, auch bei inaktiv) |
| `h_handling_zug_ke_mm` | Teal `#4BBECA` (immer, auch bei inaktiv) |
| `h_kanal_ke_mm` | Lila `#9A94E8` (aktiv) / Grau `#9A9890` (inaktiv) |
| `h_ke_mm` | Hell-Weiß `#E0DED8` (Ergebnis) |
| `h_mplatte_mbereich_mm` | Hell-Blau `#A8C4E8` (Ergebnis) |
| `b_mplatte_mbereich_mm` | Hell-Blau `#A8C4E8` (Ergebnis) |

SVG-Zonenrahmen-Farben (von Maßketten-Farben getrennt):
- h_zug-Zone: Amber-Rahmen `#D4A84B` via `C.zZ_stroke`
- h_handling_zug-Zone: Teal-Rahmen `#4BBECA` via `C.zHZ_stroke`

**CSS `:root` Variablen** (Session 6 ergänzt):
- `--c-handling`, `--c-bieg`, `--c-zug`, `--c-hz`, `--c-kanal`, `--c-dim`, `--c-result`, `--c-mbereich`
- `--fs-field: 13px`, `--fs-field-sm: 10px` (disabled Textfelder)

---

### Datenbanken

**`kabel_nym_j.json`** – 18 NYM-J Typen (3/4/5/7 Adern, 1,5–16 mm²)

**`wandschraenke.json`** – 12 Rittal AX-Wandschränke (600×600 bis 1000×1200 mm)

**`kabelzugschellen.json`** – Icotek CCL Bügelschellen für 30 mm C-Schiene ← NEU Session 6

| Bezeichnung | Art.-Nr. | d_kabel min–max | h_schelle_mm |
|---|---|---|---|
| CCL 6-13 | 32000 | 6–13 mm | 31 mm |
| CCL 12-19 | 32001 | 12–19 mm | 36 mm |
| CCL 18-23 | 32002 | 18–23 mm | 38 mm |
| CCL 22-32 | 32003 | 22–32 mm | 52 mm |

Lookup-Logik: `d_max >= d_kabel_min_mm && d_max <= d_kabel_max_mm`
Deckt alle Kabel in `kabel_nym_j.json` (d = 9,2–25,5 mm) ab.

**Excel-Sheet `kabelzugschellen` (ga_komponenten.xlsx)**

| Spalte | Typ | Beschreibung |
|---|---|---|
| `aktiv` | BOOL | FALSE = nicht exportiert |
| `hersteller` | TEXT | z.B. „Icotek" |
| `bezeichnung` | TEXT | z.B. „CCL 12-19" |
| `bestellnummer` | TEXT | Artikelnummer |
| `d_kabel_min_mm` | FLOAT | Min. Kabeldurchmesser mm |
| `d_kabel_max_mm` | FLOAT | Max. Kabeldurchmesser mm |
| `h_schelle_mm` | FLOAT | Einbauhöhe Schelle mm (= h_zug_ke_mm) |
| `b_schelle_mm` | FLOAT | Länge Schelle mm |
| `t_schelle_mm` | FLOAT | Tiefe/Breite Schelle mm |
| `preis_stueckpreis_eur` | FLOAT | leer (für Kalkulation vorbereitet) |
| `preis_lieferung_eur` | FLOAT | leer |
| `preis_montage_eur` | FLOAT | leer |
| `preis_gesamt_eur` | FLOAT | leer |

---

### xlsx_to_json.py

Exportiert alle 3 Sheets in einem Aufruf:
```
python3 xlsx_to_json.py    # aus data/-Verzeichnis in WSL
```
→ `kabel_nym_j.json` + `wandschraenke.json` + `kabelzugschellen.json`

---

## Variablen-Konvention (modulübergreifend)

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
| `h_handling_ke_mm` | Freie Kabellänge nach PG (Festwert 15 mm) | mm |
| `h_kabel_bieg_mm` | Mindestbiegeradius (4 × d_max, VDE 0298-4) | mm |
| `h_zug_ke_mm` | Bügelschellen-Höhe aus DB (Icotek CCL) | mm |
| `h_handling_zug_ke_mm` | Freiraum nach Schelle bis Kabelkanal/Gerät (Festwert 20 mm) | mm |
| `h_kanal_ke_mm` | Horizontaler Kabelkanal KE-Zone | mm |
| `h_ke_mm` | Kabeleinführungszone gesamt | mm |
| `h_mplatte_mbereich_mm` | Höhe Montagebereich auf der Montageplatte (nach Abzug KE-Zone) | mm |
| `b_mplatte_mbereich_mm` | Breite Montagebereich auf der Montageplatte (= b_mplatte_mm) | mm |
| `h_schelle_mm` | Einbauhöhe Bügelschelle (Datenbankfeld) | mm |
| `h_kabel_bieg_faktor` | Biegeradiusfaktor (Festwert 4, VDE 0298-4) | – |

---

## Offene Punkte

**Als nächstes (Prio hoch)**
1. Preisfelder Wandschrank-DB und Kabelzugschellen-DB befüllen (Listenpreise)
2. Kabelzugschellen-DB erweitern: Prüfen ob weitere Schellen für spätere Standschrank-Module notwendig
3. Außendurchmesser NYM-J mit echten Herstellerdaten verifizieren

**Mittelfristig**
4. Modul 2 – Stehender Schrank (h_zug_ke aktiv, KE von unten als Standard)
5. Einspeisezone h_einsp erarbeiten (analog zu h_ke)
6. Klemmenzone h_klemm erarbeiten
7. TE-Berechnung pro Reihe und Gesamtkapazität

**Später**
8. Startseite: Screenshot-Vorschau je Modul ergänzen
9. CSS @media print für Druckausgabe (Modul 1)
10. Module 3–5 konzipieren und in Startseite integrieren

---

## Entscheidungen (gesperrt)

**Formel h_ke**
- Reihenfolge: handling → bieg → zug → handling_zug → kanal (physikalisch korrekte Abfolge ab Gehäusewand)
- Biegeradius-Faktor 4× (VDE 0298-4, fest verlegt; 6× nur für flexible Leitungen)
- h_handling_ke = 15 mm Festwert (PG außen, Wandschrank)
- h_handling_zug_ke = 20 mm Festwert (Freiraum Schelle → Kabelkanal/Gerät)
- Kabelkanal und Zugentlastung einzeln als Ja/Nein schaltbar; bei Nein → Wert = 0

**Zugentlastung**
- Produkt: Icotek CCL – Bügelschellen für 30 mm C-Profilschiene
- h_zug_ke_mm = h_schelle_mm (aus DB, vom größten Kabeldurchmesser bestimmt)
- h_handling_zug_ke_mm = 20 mm zusätzlicher Freiraum (fixer Zuschlag)
- C-Schiene und Bügelschelle in SVG-Zeichnung dargestellt

**SVG / Darstellung**
- SVG dynamisch per JavaScript, feste Höhe SH=390 px, sc = SH/H_mm
- Alle Maßketten einheitlich blau #3366BB (= C.dim)
- Zonenrahmen-Farben (Amber, Teal) von Maßkettenfarben getrennt (C.zZ_stroke, C.zHZ_stroke)
- Zonenbeschriftungen linksbündig bei `zoneLblX = bxo + 10` (10 px rechts vom Kabel)
- Teilmaß-Labels vertikal zentriert via `dominant-baseline="middle"` (außer h_handling_ke_mm)
- h_handling_ke_mm: Sonderbehandlung (sehr kleine Zone) – Offset ±0.5 je nach KE-Richtung
- ▼/▲ Beginn/Ende Nutzfläche: anchor:middle bei mx+mw/2

**Farbkodierung**
- Formelzeile und Tabellenzeile verwenden immer identische Farben pro Variable
- h_zug_ke_mm und h_handling_zug_ke_mm immer in ihrer Farbe (kein konditionelles Grau)
- CSS `:root` Custom Properties für alle Zonenfarben definiert

**Daten / Architektur**
- Single-File HTML pro Modul (GitHub Pages, kein Build-Step)
- Excel als Pflegewerkzeug (nicht versioniert), JSON als Produktivdatenbank (committed)
- Python läuft in WSL (kein natives Windows-Python)
- Aktiv-Flag statt Löschung veralteter Datensätze
