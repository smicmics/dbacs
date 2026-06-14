# DBACS – Revisionsstand
**Stand:** 14. Juni 2026 – Session 14

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
│   └── modul-03-te-berechnung/index.html   Modul 3 – TE-Berechnung + Zonenaufteilung ✅
├── drawings/
│   ├── wandschrank_frontansicht.html       Referenzzeichnung Wandschrank (nicht bearbeiten)
│   └── standschrank_frontansicht.html      Referenzzeichnung Standschrank (nicht bearbeiten)
├── data/
│   ├── ga_komponenten.xlsx                 Pflegewerkzeug (Source of Truth, lokal – nicht versioniert)
│   ├── kabel_nym_j.json                    Kabeldatenbank NYM-J (committed)
│   ├── wandschraenke.json                  Wandschrank-DB Rittal AX (committed)
│   ├── kabelzugschellen.json               Kabelzugschellen-DB Icotek CCL (committed)
│   ├── standschraenke.json                 Standschrank-DB Rittal VX25 (committed)
│   ├── sockel.json                         Sockel-DB Rittal VX (committed)
│   ├── bodenbleche.json                    Bodenblech-DB Rittal VX (committed)
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

**localStorage-Ausgabe**
- `m01_b/h_mplatte_mbereich_wandschrank_mm` → Modul 3
- `m01_ke_pos` → Modul 3

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

**localStorage-Ausgabe**
- `m02_b/h_mplatte_mbereich_standschrank_mm` → Modul 3
- `m02_ke_pos` → Modul 3

---

### Modul 3 – vollständig funktionsfähig ✅ (Session 10–12)
**Titel:** „Modul 3 · TE-Berechnung & Reihenkapazität"
**Datei:** `modules/modul-03-te-berechnung/index.html`

**Zweck:** Berechnung der verfügbaren Teileinheiten auf der Montageplatte sowie vorläufige Zonenaufteilung der Montagefläche auf Basis technischer Mindesthöhen.

#### TE-Berechnung (Fieldsets 1–4)
- Schrank-Typ: Wandschrank / Standschrank (Pflichtauswahl, Standard „— bitte wählen —")
- Montagebereich Breite + Höhe: automatisch via localStorage aus Modul 1/2 (read-only)
- Festwert: te_breite_mm = 18,0 mm (DIN 43880 – Hüllmaße Installationseinbaugeräte)
- Festwert: b_hutschiene_mm = 35 mm (DIN EN 60715 – Hutschiene Breite)
- `n_te = ⌊ b / 18,0 ⌋` (ganze Zahl, abgerundet)
- `flaeche_mbereich_cm2` / `flaeche_mbereich_m2`

#### Zonenaufteilung (Fieldset 5) ← NEU Session 12–13
Berechnet vorläufige Zonenhöhen auf Basis technischer Mindesthöhen (analog h_ke-Logik aus M1/M2).

**Eingaben:**
| Feld | ID | Werte | Beschreibung |
|---|---|---|---|
| Schrankfelder | `zone_modus` | 1 Feld / Mehrere Felder | Ansicht: 1 Feld oder N Felder nebeneinander |
| Leistung/Steuerung | `zone_anordnung` | Übereinander / Nebeneinander | Anordnung L+S auf der Platte (gesperrt bei Mehrere Felder) |
| Netzanschluss | `zone_netztyp` | Drehstrom 3~ / Wechselstrom 1~ | Beeinflusst h_evert_min |

**Mindesthöhen-Berechnung (aufger. 5 mm):**
```
H_KLEMME_STD =  52 mm   (Standard-Klemme 4 mm², Phoenix UK 4)
H_HANDLING   =  15 mm   (Kabelhandling je Seite, wie h_handling_ke)
H_SICHER_WS  =  75 mm   (Sicherungshalter Wechselstrom, NH00/D02)
H_SCHIENE_DS = 150 mm   (Stromschienensystem Drehstrom)
H_KANAL_H    =  40 mm   (Horizontaler Kabelkanal, Platzhalter)
B_KANAL_V    =  40 mm   (Vertikaler Kabelkanal je Seite, Platzhalter)

h_evert = Drehstrom: ceil5(150) = 150 mm
          Wechselstrom: ceil5(15+75+15) = 105 mm
h_klemm = ceil5(15+52+15) = 85 mm

h_verfueg = h − h_evert − h_klemm − 3 × H_KANAL_H
b_inner   = b − 2 × B_KANAL_V

Übereinander: h_leist = ceil5(h_verfueg/2), h_steuer = Rest
Nebeneinander: h_leist = h_steuer = ceil5(h_verfueg/2), b_leist = floor(b_inner/2)
```

**Zonen im SVG (buildLayout):**
| Zone | ID | Farbe | Breite |
|---|---|---|---|
| Energieverteilung | `evert` | `#C8720E` | volle Breite |
| H. Kabelkanal | `kanal_h/ls/ev` | `#888` | volle Breite, kein Label |
| V. Kabelkanal Links | `kanal_vl` | `#888` | B_KANAL_V, in jeder L/S-Zeile |
| V. Kabelkanal Rechts | `kanal_vr` | `#888` | B_KANAL_V, in jeder L/S-Zeile |
| ÜSS + Sich. | `uss` | `#D4A84B` | b_uss, immer links (nach VK_L) |
| Leistungsbaugruppen | `leist` | `#C84E2E` | b_leist_eff |
| Steuerbaugr./DDC | `steuer` | `#4BBECA` | b_steuer (nach VK_L, kein USS) |
| Einsp.-Kl. | `klemm_e` | `#D4A84B` | b_ek (5 TE), immer links |
| Abg.-Kl. Leistung | `klemm_l` | `#2DBD8E` | neben: b/2·f_rest; über: b−B_KANAL_V−b_ek |
| Abg.-Kl. Feldger. | `klemm_f` | `#9A94E8` | neben: Rest/2; über: B_KANAL_V/2 |
| Abg.-Kl. Sensoren | `klemm_s` | `#E8C448` | neben: Rest/2; über: B_KANAL_V/2 |

**Zonenreihenfolge (KE-abhängig):**
- KE oben: Klemmen → H.Kanal → L/S-Zonen → H.Kanal L/S → H.Kanal Evert → Evert
- KE unten: Evert → H.Kanal Evert → L/S-Zonen → H.Kanal L/S → H.Kanal → Klemmen

**SVG-Besonderheiten:**
- `buildLayout(zp)` erzeugt Zeilen-Array mit x/w-Fraktionen
- Kanalstreifen ohne Label (`lbl:''`) – grau erkennbar ohne Textüberschneidung
- Maßlinie rechts je Zeile, Gesamthöhe-Linie außen
- Mehrere Felder: N Felder nebeneinander (intern immer übereinander)
- Kein sekundärer `row.h_mm mm`-Text im SVG; Werte nur über Maßlinien

**localStorage-Ausgabe M3:**
```
m03_zone_modus, m03_zone_anordnung, m03_zone_netztyp, m03_zone_ke_pos, m03_n_felder
m03_h_einsp, m03_h_evert, m03_h_leist, m03_h_steuer, m03_h_klemm
m03_b_leist, m03_b_steuer
```

---

### Datenbanken

**`kabel_nym_j.json`** – 18 NYM-J Typen (3/4/5/7 Adern, 1,5–16 mm²)

**`wandschraenke.json`** – 12 Rittal AX-Wandschränke (600×600 bis 1000×1200 mm)

**`kabelzugschellen.json`** – 4 Icotek CCL Bügelschellen für 30 mm C-Schiene

**`standschraenke.json`** – 11 Rittal VX25 Standschränke

**`sockel.json`** – 8 Rittal VX Sockel (B=600/800/1000/1200 mm × H=100/200 mm)

**`bodenbleche.json`** – 4 Rittal VX Bodenblech-Sätze (je Schrankbreite)
→ Bestellnummern noch zu verifizieren

**`reiheneinbaugeraete.json`** – 24 Einträge: Schmelzsicherungshalter, LSS, Hilfskontakte, FI-Schutzschalter (Eaton + Siemens)
→ Preise noch zu befüllen · Bestellnummern zu verifizieren

---

## Offene Punkte

**Daten verifizieren (Prio mittel)**
1. Bestellnummern `bodenbleche.json` über Rittal-Katalog/Website bestätigen
2. Preisfelder aller DBs befüllen (Listenpreise)

**Modul 3 – mögliche Erweiterungen**
3. Zonenaufteilung: Mindesthöhen als editierbare Felder (Override) – derzeit Festwerte
4. Zonenaufteilung: Warnung bei zu kleiner Montagefläche aktuell als Hinweis (rot), kein Blocker
5. Mehrere Felder + Nebeneinander: aktuell disabled; Konzept für feldweise Nebeneinander-Anordnung

**Nächste Module (Prio hoch)**
6. Modul 4 – Einspeisezone h_einsp (Detailplanung, Eingabe Hauptschalter/ÜSS-Typen)
7. Modul 5 – Klemmenzone h_klemm (Anzahl Klemmen je Gruppe)
8. Startseite: Modul 4–5 Karten aktualisieren wenn Entwicklung beginnt

**Später**
9. Außendurchmesser NYM-J mit echten Herstellerdaten verifizieren
10. Startseite: Screenshot-Vorschau je Modul ergänzen

---

## Entscheidungen (gesperrt)

**Formel h_ke (Modul 1+2)**
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

**SVG / Darstellung (Modul 1+2)**
- SVG dynamisch per JavaScript, feste Höhe SH=390 px, sc = SH/H_mm (maßstäblich)
- Strichstärken proportional zum Maßstab: `lw_s = max(0.8, sc*8)`, `lw_mp = max(0.4, sc*4)`
- Alle Maßketten einheitlich blau #3366BB
- Zonenrahmen-Farben (Amber, Teal) von Maßkettenfarben getrennt

**Modul 3 – TE-Berechnung**
- `te_breite_mm = 18,0 mm` Festwert nach DIN 43880 (Hüllmaße für Installationseinbaugeräte)
- `h_hutschiene_mm = 7,5 mm` Festwert nach DIN EN 60715 (Hutschiene, nur Anzeige)
- `n_te = Math.floor(b / 18.0)` – ganzzahlig abgerundet
- `schrank_typ` wird **nicht** aus localStorage wiederhergestellt – Start immer mit „— bitte wählen —"
- `typLabel` ohne Modulangabe: „Wandschrank" / „Standschrank"
- Formelbox zeigt Eingabewerte mit Einheit mm: `⌊ b mm / 18,0 mm ⌋`
- Copyright: `class="copyright-line"` + `@media print { .copyright-line { display:none !important } }`

**Modul 3 – Zonenaufteilung (gesperrt)**
- Mindesthöhen basieren auf physikalischen Festwerten (wie h_ke-Logik), keine Prozent-Eingabe
- `ceil5()` – alle Mindesthöhen auf 5 mm aufgerundet
- h_klemm = ceil5(H_HANDLING + H_KLEMME_STD + H_HANDLING) = 85 mm (Festwert 4 mm²-Klemme)
- h_einsp = 120 mm (Festwert, nicht überschreibbar)
- 3 Klemmengruppen immer nebeneinander (klemm_l | klemm_f | klemm_s), adjacent zu ihrer Funktionszone
- Anordnung L/S gesperrt (disabled) wenn Modus „Mehrere Felder"
- KE-Position bestimmt Zonenreihenfolge: KE oben → Einsp. oben; KE unten → Einsp. unten, Evert. oben
- `klemm_e` ist kein gültiges Konzept → heißt `klemm_s` (Abgangsklemmen Sensoren)

**Daten / Architektur**
- Single-File HTML pro Modul (GitHub Pages, kein Build-Step)
- Excel als Pflegewerkzeug (nicht versioniert), JSON als Produktivdatenbank (committed)
- Python läuft in WSL
