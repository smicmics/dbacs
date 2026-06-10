# DBACS – Revisionsstand
**Stand:** 10. Juni 2026 – Session 10

---

## Projektziel

Webbasiertes Planungstool für das Gewerk Gebäudeautomation zur Unterstützung der Schaltschrank-Dimensionierung in verschiedenen HOAI-Leistungsphasen, betrieben als statische GitHub Pages Anwendung.

---

## Stack / Architektur

**Technologien**
- Reines HTML/CSS/JavaScript – kein Framework, kein Build-Step
- Eine HTML-Datei pro Modul (Self-contained)
- SVG dynamisch per JavaScript erzeugt, vollständig maßstäblich (`sc = SH / H_mm`)
- Datenhaltung: Excel → Python (WSL) → JSON → fetch() im Browser

**Dateistruktur**
```
dbacs/
├── CLAUDE.md                               Projektkonventionen für Claude (Session-Start)
├── index.html                              Root-Redirect → web/index.html (GitHub Pages)
├── .gitignore                              OS, Editor, Python, data/*.db, data/*.xlsx
├── .claude/
│   └── launch.json                         Dev-Server-Konfiguration (statischer HTTP-Server Port 8099)
├── web/
│   ├── index.html                          Startseite / Modulübersicht (Dark Theme) – 3 Module aktiv
│   └── assets/
│       ├── css/style.css                   Dark Theme Stylesheet
│       ├── js/main.js                      Scroll-Reveal + aktive Nav-Link-Steuerung
│       └── img/dbacs-logo.png              DBACS Logo (Startseite + Modul-Header)
├── modules/
│   ├── modul-01-schaltschrank/index.html   Modul 1 – Wandschrank, vollständig ✅
│   ├── modul-02-standschrank/index.html    Modul 2 – Standschrank, vollständig ✅
│   └── modul-03-te-berechnung/index.html   Modul 3 – TE-Berechnung, vollständig ✅ ← NEU Session 10
├── drawings/
│   ├── wandschrank_frontansicht.html       Referenzzeichnung Wandschrank (nicht bearbeiten)
│   └── standschrank_frontansicht.html      Referenzzeichnung Standschrank (nicht bearbeiten)
├── data/
│   ├── ga_komponenten.xlsx                 Pflegewerkzeug (Source of Truth, lokal – nicht versioniert)
│   ├── kabel_nym_j.json                    Kabeldatenbank NYM-J (committed)
│   ├── wandschraenke.json                  Wandschrank-DB Rittal AX (committed)
│   ├── kabelzugschellen.json               Kabelzugschellen-DB Icotek CCL (committed)
│   ├── standschraenke.json                 Standschrank-DB Rittal VX25 (committed) ← NEU Session 8
│   ├── sockel.json                         Sockel-DB Rittal VX (committed) ← NEU Session 8
│   ├── bodenbleche.json                    Bodenblech-DB Rittal VX (committed) ← NEU Session 8
│   └── xlsx_to_json.py                     Konvertierungsskript Excel → JSON (6 Sheets)
└── docs/
    └── *.md                                Projektdokumentation
```

**Deployment**
| | |
|---|---|
| Repository | https://github.com/smicmics/dbacs |
| Live-URL Startseite | https://smicmics.github.io/dbacs/ |
| Live-URL Modul 1 | https://smicmics.github.io/dbacs/modules/modul-01-schaltschrank/ |
| Live-URL Modul 2 | https://smicmics.github.io/dbacs/modules/modul-02-standschrank/ |
| Live-URL Modul 3 | https://smicmics.github.io/dbacs/modules/modul-03-te-berechnung/ |
| Deploy-Trigger | Push auf `main` Branch → GitHub Pages baut automatisch |

---

## Stand heute

### Modul 1 – vollständig funktionsfähig ✅
**Titel:** „Modul 1 · Wandschrank · Kabeleinführung · Nutzfläche"

**Berechnungsformel h_ke_mm**
```
h_ke_mm = h_handling_ke_mm + h_kabel_bieg_mm + h_zug_ke_mm + h_handling_zug_ke_mm + h_kanal_ke_mm
```

**Eingabepanel**
- Schrank-Außenmaße + Montageplatte
- Wandschrank-Dropdown (Rittal AX, aus `wandschraenke.json`)
- Kabeleinführung: Position oben/unten, Aderzahl, Querschnitt → d_max aus `kabel_nym_j.json`
- Kabelkanal: Ja/Nein-Toggle + Höheneingabe
- Zugentlastung: Ja/Nein → DB-Lookup `kabelzugschellen.json`
- Schriftgrößen SVG: fs_dim=7, fs_var=6, fs_zone=7
- Festwerte: h_handling_ke=15 mm, h_handling_zug_ke=20 mm, Faktor 4×
- Projektfelder im Header (Projekt, Projektnummer, ASP, Bearbeitet von, Dokument-Nr.) → localStorage
- Druckbutton: Ergebnis drucken (float-Layout, Hochformat, 2 Seiten)
- DBACS Logo im Header (screen + print), `../../web/assets/img/dbacs-logo.png`
- Strichstärken proportional: `lw_s = Math.max(0.8, sc*8)`, `lw_mp = Math.max(0.4, sc*4)`

**Ergebnisse**
- `h_ke_mm` – Kabeleinführungszone gesamt
- `h_mplatte_mbereich_wandschrank_mm` – Höhe Montagebereich MP
- `b_mplatte_mbereich_wandschrank_mm` = b_mplatte_mm

---

### Modul 2 – vollständig funktionsfähig ✅
**Titel:** „Modul 2 · Standschrank · Kabeleinführung · Nutzfläche"
**Datei:** `modules/modul-02-standschrank/index.html`

**Unterschiede zu Modul 1:**

| Merkmal | Modul 1 (Wandschrank) | Modul 2 (Standschrank) |
|---|---|---|
| Schrank-DB | `wandschraenke.json` (Rittal AX) | `standschraenke.json` (Rittal VX25) |
| Sockel | nicht vorhanden | `sockel.json` – Ja/Nein, 100/200 mm |
| KE Standard | oben | unten |
| KE unten | mit PG-Verschraubung | freie Einführung, kein PG (Boden offen) |
| KE oben | mit PG | mit PG (halbe Größe vs. Modul 1) |
| Schriftgrößen | fs_dim=7, fs_var=6, fs_zone=7 | fs_dim=5, fs_var=5, fs_zone=5 |
| Ergebnisvariablen | `_wandschrank_` | `_standschrank_` |
| Standardwerte Aufruf | KE oben, Zugentlastung Nein | KE unten, Sockel 100 mm aktiv, Zugentlastung Ja |

**Sockel-Logik:**
- Sockel Ja/Nein toggle → Höhe 100 oder 200 mm wählbar
- DB-Lookup: `SOCKEL_DB.find(e => e.b_gehaeuse_aussen_mm === B && e.h_sockel_mm === h_sockel_option)`
- SVG: Sockel-Rechteck maßstäblich unterhalb des Schranks, Text „Schaltschranksockel" linksbündig bei `zoneLblX`
- Maßlinie Sockel: gleiche horizontale Position wie H-Maßlinie (`hx = sx - 16`), Label nur Wert (ohne Variablenname)
- VH = PT + SH + h_sockel_px + PB (SVG-Höhe dynamisch erweitert)

**KE unten ohne PG:**
- Kabel läuft von KE-Zone durch Schrankinnenraum und Boden in Sockel
- Text „Freie Kabeleinführung · Boden offen" bei `zoneLblX`, unterhalb Sockeltext, Größe `fs_zone`
- Kabelstub: 10 px unterhalb Sockel (oder Schrankunterseite wenn kein Sockel)

**SVG Maßstab + Strichstärken (beide Module):**
```js
const SH    = 390;                           // SVG-Höhe px (fest)
const sc    = SH / p.H;                      // Maßstab px/mm
const lw_s  = +Math.max(0.8, sc * 8).toFixed(1);  // Gehäuselinie (proportional)
const lw_mp = +Math.max(0.4, sc * 4).toFixed(1);  // MP-Linie (proportional)
```
Schrank, Montageplatte, KE-Zonen und Sockel sind immer proportional korrekt dargestellt.
Strichstärken skalieren mit dem Maßstab – kleinere Schrankdarstellungen erhalten dünnere Linien.

**Ergebnisse**
- `h_ke_mm` – Kabeleinführungszone gesamt (gleiche Formel wie Modul 1)
- `h_mplatte_mbereich_standschrank_mm` – Höhe Montagebereich MP
- `b_mplatte_mbereich_standschrank_mm` = b_mplatte_mm

---

### Modul 3 – vollständig funktionsfähig ✅ ← NEU Session 10
**Titel:** „Modul 3 · TE-Berechnung & Reihenkapazität"
**Datei:** `modules/modul-03-te-berechnung/index.html`

**Zweck:** Berechnung der verfügbaren Teileinheiten auf der Montageplatte, auf Basis der Montagebereich-Maße aus Modul 1 oder 2.

**Eingabepanel**
- Schrank-Typ: Wandschrank / Standschrank (Pflichtauswahl, Standard „— bitte wählen —")
- Montagebereich Breite + Höhe: automatisch via localStorage aus Modul 1/2 übernommen (read-only)
- Festwert: te_breite_mm = 17,5 mm (DIN EN 60715)

**localStorage-Datenaustausch**
- Modul 1 schreibt bei jeder Berechnung: `m01_b/h_mplatte_mbereich_wandschrank_mm`
- Modul 2 schreibt bei jeder Berechnung: `m02_b/h_mplatte_mbereich_standschrank_mm`
- Modul 3 liest je nach Typ-Auswahl den passenden Key
- Bei fehlendem Key: Felder = 0, Hinweis mit Link zur Startseite

**Ergebnisse**
- `flaeche_mbereich_cm2` = (b × h) / 100
- `flaeche_mbereich_m2`  = (b × h) / 1 000 000
- `n_te`                 = ⌊ b / 17,5 ⌋ (ganze Zahl, abgerundet)

**Farbkodierung**
| Variable | Farbe | Hex |
|---|---|---|
| Eingaben b, h | Sekundär | `#9A9890` |
| `flaeche_mbereich_cm2` | Grün | `#2DBD8E` |
| `flaeche_mbereich_m2` | Lila | `#9A94E8` |
| `n_te` | Hellblau | `#A8C4E8` |
| `te_breite_mm` (Festwert) | Amber | `#D4A84B` |

**Besonderheiten**
- Kein SVG – nur Ergebnistabelle und Formelbox
- Variablennamen in Seitenleiste und Tabelle wechseln dynamisch je Typ (`_wandschrank_mm` / `_standschrank_mm`)
- Formel-Variablennamen farbig (gleiche Farbe wie Tabellenzeile)
- Copyright-Zeile (`class="copyright-line"`) in Druckansicht ausgeblendet

---

### Datenbanken

**`kabel_nym_j.json`** – 18 NYM-J Typen (3/4/5/7 Adern, 1,5–16 mm²)

**`wandschraenke.json`** – 12 Rittal AX-Wandschränke (600×600 bis 1000×1200 mm)

**`kabelzugschellen.json`** – 4 Icotek CCL Bügelschellen für 30 mm C-Schiene

**`standschraenke.json`** – 11 Rittal VX25 Standschränke ← NEU Session 8

| Bezeichnung | B×H×T (mm) | MP B×H (mm) |
|---|---|---|
| VX 8686.000 | 600×1800×600 | 499×1696 |
| VX 8604.000 | 600×2000×400 | 499×1896 |
| VX 8606.000 | 600×2000×600 | 499×1896 |
| VX 8880.000 | 800×1800×500 | 699×1696 |
| VX 8804.000 | 800×2000×400 | 699×1896 |
| VX 8806.000 | 800×2000×600 | 699×1896 |
| VX 8826.000 | 800×2200×600 | 699×2096 |
| VX 8080.000 | 1000×1800×400 | 899×1696 |
| VX 8006.000 | 1000×2000×600 | 899×1896 |
| VX 8265.000 | 1200×1600×500 | 1099×1496 |
| VX 8205.000 | 1200×2000×500 | 1099×1896 |

Formel: MP_B = B − 101 mm, MP_H = H − 104 mm

**`sockel.json`** – 8 Rittal VX Sockel ← NEU Session 8
B = 600/800/1000/1200 mm × H = 100/200 mm

**`bodenbleche.json`** – 4 Rittal VX Bodenblech-Sätze (je Schrankbreite) ← NEU Session 8
Bestellnummern noch zu verifizieren (aus Rittal-Katalog ableiten)

---

### xlsx_to_json.py

Exportiert alle 6 Sheets in einem Aufruf:
```
python3 xlsx_to_json.py    # aus data/-Verzeichnis in WSL
```
→ `kabel_nym_j.json` + `wandschraenke.json` + `kabelzugschellen.json`
  + `standschraenke.json` + `sockel.json` + `bodenbleche.json`

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
| `h_handling_ke_mm` | Freie Kabellänge nach PG / ab Boden (Festwert 15 mm) | mm |
| `h_kabel_bieg_mm` | Mindestbiegeradius (4 × d_max, VDE 0298-4) | mm |
| `h_zug_ke_mm` | Bügelschellen-Höhe aus DB (Icotek CCL) | mm |
| `h_handling_zug_ke_mm` | Freiraum nach Schelle bis Kabelkanal/Gerät (Festwert 20 mm) | mm |
| `h_kanal_ke_mm` | Horizontaler Kabelkanal KE-Zone | mm |
| `h_ke_mm` | Kabeleinführungszone gesamt | mm |
| `h_mplatte_mbereich_wandschrank_mm` | Höhe Montagebereich MP – Wandschrank | mm |
| `b_mplatte_mbereich_wandschrank_mm` | Breite Montagebereich MP – Wandschrank (= b_mplatte_mm) | mm |
| `h_mplatte_mbereich_standschrank_mm` | Höhe Montagebereich MP – Standschrank | mm |
| `b_mplatte_mbereich_standschrank_mm` | Breite Montagebereich MP – Standschrank (= b_mplatte_mm) | mm |
| `h_sockel_mm` | Sockelhöhe Standschrank (0 wenn inaktiv) | mm |
| `h_schelle_mm` | Einbauhöhe Bügelschelle (Datenbankfeld) | mm |
| `h_kabel_bieg_faktor` | Biegeradiusfaktor (Festwert 4, VDE 0298-4) | – |
| `schrank_typ` | Auswahl Wandschrank / Standschrank (Modul 3) | – |
| `te_breite_mm` | TE-Breite nach DIN EN 60715 (Festwert 17,5 mm) | mm |
| `flaeche_mbereich_cm2` | Montagefläche Montagebereich | cm² |
| `flaeche_mbereich_m2` | Montagefläche Montagebereich | m² |
| `n_te` | Verfügbare Teileinheiten auf Montagebereich-Breite (ganze Zahl) | TE |

---

## Offene Punkte

**Daten verifizieren (Prio mittel)**
1. Bestellnummern `bodenbleche.json` über Rittal-Katalog/Website bestätigen
2. Bestellnummern `sockel.json` (8660001, 8660004, 8660005, 8660021, 8660024) – bestätigt: 8660003, 8660023, 8660025
3. Preisfelder aller DBs befüllen (Listenpreise)

**Nächste Module (Prio hoch)**
4. Modul 4 – Einspeisezone h_einsp (analog h_ke)
5. Modul 5 – Klemmenzone h_klemm
6. Startseite: Modul 4–5 Karten aktualisieren wenn Entwicklung beginnt

**Später**
7. Außendurchmesser NYM-J mit echten Herstellerdaten verifizieren
8. Startseite: Screenshot-Vorschau je Modul ergänzen
9. Standschrank-Zeichnung: Werte der Beispieldarstellung mit realen DB-Werten abgleichen

---

## Entscheidungen (gesperrt)

**Formel h_ke (beide Module)**
- Reihenfolge: handling → bieg → zug → handling_zug → kanal (fest)
- Biegeradius-Faktor 4× (VDE 0298-4, fest verlegt)
- h_handling_ke = 15 mm Festwert
- h_handling_zug_ke = 20 mm Festwert
- Kabelkanal und Zugentlastung einzeln Ja/Nein schaltbar

**Modul 2 – Standschrank-spezifisch**
- KE unten: kein PG (Boden offen), freie Kabeleinführung
- KE oben: PG halb so groß wie Modul 1 (Dimensionen ÷2, stroke-width 0.7)
- Sockel-Maßlinie: gleiche horizontale Position wie H-Maßlinie, Label nur Wert (mm)
- „Schaltschranksockel" + „Freie Kabeleinführung · Boden offen" beide bei zoneLblX linksbündig
- Schriftgrößen Standschrank: fs_dim=5, fs_var=5, fs_zone=5 (Standardwerte)

**SVG / Darstellung (beide Module)**
- SVG dynamisch per JavaScript, feste Höhe SH=390 px, sc = SH/H_mm (maßstäblich)
- Strichstärken proportional zum Maßstab: `lw_s = max(0.8, sc*8)`, `lw_mp = max(0.4, sc*4)`
- Alle Maßketten einheitlich blau #3366BB
- Zonenrahmen-Farben (Amber, Teal) von Maßkettenfarben getrennt
- Zonenbeschriftungen linksbündig bei `zoneLblX = bxo + 10`
- Teilmaß-Labels vertikal zentriert via `dominant-baseline="middle"` (außer h_handling_ke_mm)

**Startseite / Branding**
- DBACS Logo (`web/assets/img/dbacs-logo.png`) in Startseiten-Header und Modul-Headern
- Logo in Print-CSS explizit gesetzt (44px, display:flex im Header)
- Modul-Kacheln: Struktur Titel → Untertitel (blau) → Scope (grau) → Beschreibungstext → Features

**Variablen-Trennung Wand- vs. Standschrank**
- `h/b_mplatte_mbereich_wandschrank_mm` für Modul 1
- `h/b_mplatte_mbereich_standschrank_mm` für Modul 2
- Ermöglicht automatische Datenübernahme in Modul 3 via localStorage

**Modul 3 – TE-Berechnung**
- `te_breite_mm = 17,5 mm` Festwert nach DIN EN 60715 (nicht ändern)
- `n_te = Math.floor(b / 17.5)` – ganzzahlig abgerundet
- Datenfluss: Modul 1/2 → localStorage → Modul 3 (kein direkter Aufruf)
- Standardauswahl `schrank_typ = ""` → alle Felder 0 bis Auswahl erfolgt
- Copyright: `class="copyright-line"` + `@media print { .copyright-line { display:none !important } }`

**Daten / Architektur**
- Single-File HTML pro Modul (GitHub Pages, kein Build-Step)
- Excel als Pflegewerkzeug (nicht versioniert), JSON als Produktivdatenbank (committed)
- Python läuft in WSL
