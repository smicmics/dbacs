# DBACS – Revisionsstand
**Stand:** 28. Juni 2026 – Session 19 (Code-Review abgeschlossen)

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
│   ├── launch.json                         Dev-Server-Konfiguration (statischer HTTP-Server Port 8099)
│   └── settings.local.json                 Stop-Hook: auto commit + push nach Aufgabe
├── web/
│   ├── index.html                          Startseite / Modulübersicht (Dark Theme) – 3 Module aktiv
│   └── assets/
│       ├── css/style.css                   Dark Theme Stylesheet
│       ├── js/main.js                      Scroll-Reveal + aktive Nav-Link-Steuerung
│       └── img/dbacs-logo.png              DBACS Logo (Startseite + Modul-Header)
├── modules/
│   ├── modul-01-schaltschrank/index.html   Modul 1 – Wandschrank, vollständig ✅
│   ├── modul-02-standschrank/index.html    Modul 2 – Standschrank, vollständig ✅
│   └── modul-03-architektur/index.html     Modul 3 – TE-Berechnung + Zonenaufteilung ✅
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
│   ├── reiheneinbaugeraete.json            Reiheneinbaugeräte (Eaton + Siemens, committed)
│   └── xlsx_to_json.py                     Konvertierungsskript Excel → JSON (7 Sheets)
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
| Live-URL Modul 3 | https://smicmics.github.io/dbacs/modules/modul-03-architektur/ |
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
- Druckbutton: `printErgebnis()` → Querformat A4, Vollseiten-Ausdruck (beide Panels + SVG)
- DBACS Logo im Header (screen + print), `../../web/assets/img/dbacs-logo.png`
- Strichstärken proportional: `lw_s = Math.max(0.8, sc*8)`, `lw_mp = Math.max(0.4, sc*4)`

**Ergebnisse**
- `h_ke_mm` – Kabeleinführungszone gesamt
- `h_mplatte_mbereich_wandschrank_mm` – Höhe Montagebereich MP
- `b_mplatte_mbereich_wandschrank_mm` = b_mplatte_mm

**localStorage-Ausgabe**
- `m01_b/h_mplatte_mbereich_wandschrank_mm` → Modul 3
- `m01_ke_pos` → Modul 3
- `m01_h_ke_mm`, `m01_h_handling_ke_mm`, `m01_h_kabel_bieg_mm`, `m01_h_zug_ke_mm`, `m01_h_handling_zug_ke_mm`, `m01_h_kanal_ke_mm` → Modul 3 (Vollständiges Layout)
- `m01_kanal_aktiv`, `m01_zug_aktiv`, `m01_B`, `m01_H`, `m01_mp_b`, `m01_mp_h`, `m01_b_abst`, `m01_h_abst` → Modul 3 (Vollständiges Layout)

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
- `m02_h_ke_mm`, `m02_h_handling_ke_mm`, `m02_h_kabel_bieg_mm`, `m02_h_zug_ke_mm`, `m02_h_handling_zug_ke_mm`, `m02_h_kanal_ke_mm` → Modul 3 (Vollständiges Layout)
- `m02_kanal_aktiv`, `m02_zug_aktiv`, `m02_B`, `m02_H`, `m02_mp_b`, `m02_mp_h`, `m02_b_abst`, `m02_h_abst` → Modul 3 (Vollständiges Layout)
- `m02_h_sockel_mm`, `m02_sockel_aktiv` → Modul 3 (Vollständiges Layout – Sockel-Rect + Maßkette)

---

### Modul 3 – vollständig funktionsfähig ✅ (Sessions 10–18)
**Titel:** „Modul 3 · TE-Berechnung · Architektur · Innenaufbau"
**Datei:** `modules/modul-03-architektur/index.html`

**Zweck:** Berechnung der verfügbaren Teileinheiten auf der Montageplatte sowie vorläufige Zonenaufteilung der Montagefläche auf Basis technischer Mindesthöhen.

#### TE-Berechnung (Fieldsets 1–4)
- Schrank-Typ: Wandschrank / Standschrank (Pflichtauswahl, Standard „— bitte wählen —")
- Montagebereich Breite + Höhe: automatisch via localStorage aus Modul 1/2 (read-only)
- Festwert: `TE_BREITE_MM = 18,0 mm` (DIN 43880 – Hüllmaße Installationseinbaugeräte)
- Festwert: `b_hutschiene_mm = 35 mm` (DIN EN 60715 – Hutschiene Breite, nur Anzeige)
- `n_te = ⌊ b / 18,0 ⌋` (ganze Zahl, abgerundet)
- `flaeche_mbereich_cm2` / `flaeche_mbereich_m2`
- Kabelkanal-Festwerte editierbar: `h_kanal_h_mm` (Standard 40 mm), `b_kanal_v_mm` (Standard 40 mm)

#### Zonenaufteilung (Fieldset 5)

**Eingaben:**
| Feld | ID | Werte | Beschreibung |
|---|---|---|---|
| Schrankfelder | `zone_modus` | 1 Feld / Mehrere Felder | Ansicht: 1 Feld oder N Felder nebeneinander |
| Leistung/Steuerung | `zone_anordnung` | Übereinander / Nebeneinander | gesperrt bei Mehrere Felder |
| Netzanschluss | `zone_netztyp` | Drehstrom 3~ / Wechselstrom 1~ | bestimmt h_evert und ÜSS-Größe |
| Schienensystem | `zone_schiene` | Ja / Nein | nur bei Drehstrom sichtbar |
| Polzahl | `zone_schiene_pol` | 3-polig / 4-polig / 5-polig | nur bei Schienensystem=Ja sichtbar |

**Festwerte (JS-Konstanten):**
```
TE_BREITE_MM   = 18,0 mm  (DIN 43880)
H_KLEMME_STD  = 65 mm    (Phoenix XTV 6 → 6 mm², 62,5 mm; PT 2.5 MT → Messertrennkl., 62,5 mm → aufger. 65 mm)
H_HANDLING    = 15 mm    (Kabelhandling je Seite, wie h_handling_ke in M1/M2)
H_SICHER_WS   = 75 mm    (Sicherungshalter D0/NH00, Wechselstrom)
H_SCHIENE_3POL = 300 mm  (60-mm-Schienensystem, 3-polig, mit NH-Trennern – eigene Recherche)
H_SCHIENE_4POL = 350 mm  (60-mm-Schienensystem, 4-polig, mit NH-Trennern)
H_SCHIENE_5POL = 400 mm  (60-mm-Schienensystem, 5-polig, mit NH-Trennern)
H_KANAL_H_DEF =  40 mm  (H. Kabelkanal Standardwert, vom Nutzer editierbar)
B_KANAL_V_DEF =  40 mm  (V. Kabelkanal Standardwert, vom Nutzer editierbar)
TE_USS_WS     = 2 TE     (ÜSS Typ 2, 2-polig, Wechselstrom)
TE_SICH_WS    = 2 TE     (Vorsicherung D0, 1× Halter L-Leiter)
TE_USS_DS     = 4 TE     (ÜSS Typ 2, 4-polig, Drehstrom)
TE_SICH_DS    = 3 TE     (Vorsicherung D0, 3× Halter L1/L2/L3)
TE_KLEMME_ES_WS = 3 TE  (Einspeiseklemmen WS: L1/N/PE)
TE_KLEMME_ES_DS = 5 TE  (Einspeiseklemmen DS: L1/L2/L3/N/PE)
```

**Mindesthöhen-Berechnung:**
```
h_evert:
  DS + Schiene Ja + 3-pol: 300 mm (H_SCHIENE_3POL, kein ceil5 – exakter Herstellerwert)
  DS + Schiene Ja + 4-pol: 350 mm
  DS + Schiene Ja + 5-pol: 400 mm
  DS + Schiene Nein:        ceil5(15 + 75 + 15) = 105 mm (D0 3~ auf Hutschiene)
  Wechselstrom:             ceil5(15 + 75 + 15) = 105 mm

h_klemm = ceil5(H_HANDLING + H_KLEMME_STD + H_HANDLING)
        = ceil5(15 + 65 + 15) = ceil5(95) = 95 mm

useEvKanal = !(netztyp === 'drehstrom' && schiene === 'ja')
n_kanal_h  = useEvKanal ? 4 : 3
  Schiene Ja:  3 H.Kanäle (kanal_h + kanal_ls + kanal_ev)
  Schiene Nein / WS: 4 H.Kanäle (+ kanal_ev2 auf KE-Seite)

h_verfueg = h − h_evert − h_klemm − n_kanal_h × h_kanal_h
b_inner   = b − 2 × b_kanal_v

Übereinander: h_leist = ceil5(h_verfueg/2), h_steuer = Rest
Nebeneinander: h_leist = h_steuer = ceil5(h_verfueg/2), b_leist = floor(b_inner/2)
```

**Zonen im SVG (buildLayout):**
| Zone | ID | Farbe | Breite | Bedingung |
|---|---|---|---|---|
| Energieverteilung | `evert` | `#C8720E` | volle Breite (+ lin. V.Kanal wenn useEvKanal) | immer |
| H. Kabelkanal KE-Seite | `kanal_ev2` | `#888` | volle Breite | nur wenn useEvKanal |
| H. Kabelkanal L/S-Seite | `kanal_ev` | `#888` | volle Breite | immer |
| H. Kabelkanal Klemmen/L | `kanal_h` | `#888` | volle Breite | immer |
| H. Kabelkanal L/S-Trenner | `kanal_ls` | `#888` | volle Breite | immer |
| V. Kabelkanal Links | `kanal_vl` | `#888` | b_kanal_v | in jeder L/S-Zeile |
| V. Kabelkanal Rechts | `kanal_vr` | `#888` | b_kanal_v | in jeder L/S-Zeile |
| ÜSS + Sich. | `uss` | `#D4A84B` | b_uss (max 40 % b), immer links (nach VK_L) | in L/S-Zeile |
| Leistungsbaugruppen | `leist` | `#C84E2E` | b_leist_eff | in L/S-Zeile |
| Steuerbaugr./DDC | `steuer` | `#4BBECA` | b_steuer (nach VK_L, kein USS) | in L/S-Zeile |
| Einsp.-Kl. | `klemm_e` | `#D4A84B` | b_ek (3 TE WS / 5 TE DS), immer links | in Klemmenzeile |
| Abg.-Kl. Leistung | `klemm_l` | `#2DBD8E` | ~b/2 · f_rest | in Klemmenzeile |
| Abg.-Kl. Feldger. | `klemm_f` | `#9A94E8` | Rest/2 | in Klemmenzeile |
| Abg.-Kl. Sensoren | `klemm_s` | `#E8C448` | Rest/2 | in Klemmenzeile |

**Zonenreihenfolge (KE-abhängig):**
- KE oben:  Klemmen → kanal_h → L/S → kanal_ls → kanal_ev → Evert [→ kanal_ev2]
- KE unten: [kanal_ev2 →] Evert → kanal_ev → L/S → kanal_ls → kanal_h → Klemmen

**Besonderheit Evert-Zone:**
- `useEvKanal = false` (Schienensystem Ja): Evert volle Breite – Anschluss seitlich über V.Kanal
- `useEvKanal = true` (kein Schiene / WS): linker V.Kanal sichtbar in Evert-Zone (Kabel muss Montageplattenkante erreichen)

**localStorage – Modul 3 schreibt:**
```
m03_zone_modus, m03_zone_anordnung, m03_zone_netztyp, m03_zone_ke_pos, m03_n_felder
m03_zone_schiene, m03_zone_schiene_pol
m03_b_uss, m03_h_evert, m03_h_leist, m03_h_steuer, m03_h_klemm, m03_b_leist, m03_b_steuer
m03_n_te, m03_b_kanal_v, m03_h_kanal_h, m03_b_ek   ← Session 19 (Grundlage Modul 4)
```

#### Druckbutton „Vollständiges Layout drucken"

**Funktion:** `buildFullLayoutSVG()` – erzeugt kombiniertes SVG des vollständigen Schranks

**Print-CSS `body.print-full`:**
- Header, .layout, .site-footer ausgeblendet – Projektkopf liegt im SVG
- SVG: `width:100%; height:auto` – landscape ratio garantiert durch VW_min=950

**SVG-Header (Corporate Design, im SVG eingebettet):**
- Grauer Balken (fill `#EFEFEC`, Höhe PH=54), Trennlinie `#BBBBBB`
- Logo links, Titel + Schrankinfo, vertikale Trennung bei x=348, Projektfelder rechts
- Footer: Linie + „Stand: DD.MM.YYYY" links, „Seite 1 von 1" mittig

#### Druckbutton „Ergebnis drucken" (alle 3 Module, Session 18)

**Funktion:** `printErgebnis()` – injiziert `@page{size:A4 landscape;margin:10mm 12mm}` per JS, ruft `window.print()` auf (kein Container-Switching)

**Vollseiten-Ausdruck** (Seitenleiste + SVG/Ergebnistabelle), gleicher Inhalt wie Bildschirm

**Corporate Header im `@media print`** (alle 3 Module identisch):
- `header { background:#EFEFEC !important; border-bottom:1.5px solid #BBBBBB; ... }`
- Logo 40×40, Titel, vertikale Trennlinie via `border-left:1px solid #CCC` auf `.proj-fields`
- `.proj-field input { color:#111 !important; border-bottom:0.5px solid #BBB; }`
- `-webkit-print-color-adjust:exact; print-color-adjust:exact` – erzwingt Hintergrundfarbe im Druck

**Fieldsets page-break-safe:** `break-inside:avoid; page-break-inside:avoid` auf `fieldset`

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
4. Warnung bei zu kleiner Montagefläche: aktuell roter Hinweis, kein Blocker
5. Mehrere Felder + Nebeneinander: aktuell disabled; Konzept für feldweise Nebeneinander-Anordnung

**Nächste Schritte (Prio hoch)**
6. ~~Code-Review alle 3 Module~~ ✅ abgeschlossen Session 19
7. Modul 4 – Einspeisezone / Leistungszone (Detailplanung, Eingabe Hauptschalter/ÜSS-Typen, Geräte befüllen)
8. Modul 5 – Klemmenzone h_klemm (Anzahl Klemmen je Gruppe)
9. Startseite: Modul 4–5 Karten aktualisieren wenn Entwicklung beginnt

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

**Modul 3 – TE-Berechnung (gesperrt)**
- `te_breite_mm = 18,0 mm` Festwert nach DIN 43880 (Hüllmaße Installationseinbaugeräte)
- `b_hutschiene_mm = 35 mm` nach DIN EN 60715 (Breite, nicht Höhe – nur Anzeige)
- `n_te = Math.floor(b / 18.0)` – ganzzahlig abgerundet
- `schrank_typ` wird nicht aus localStorage wiederhergestellt – Start immer „— bitte wählen —"
- `typLabel` ohne Modulangabe: „Wandschrank" / „Standschrank"
- Copyright: `class="copyright-line"` + `@media print { .copyright-line { display:none !important } }`

**Modul 3 – Sidebar Zonen-Anzeige (Session 19 – gesperrt)**
- Energieverteilung, Leistungsbaugr., Steuerbaugr./DDC zeigen jetzt `TE · mm` (TE = Breiten-TE der Zone)
- Leistungsbaugr. bei n_felder > 1: größtes Feld (ohne ÜSS-Reservierung) → `Math.floor(b_leist / TE_BREITE_MM)`
- Leistungsbaugr. bei n_felder = 1: `Math.floor((b_leist - b_uss) / TE_BREITE_MM)`
- Energieverteilung TE: `Math.floor(b_inner / TE_BREITE_MM)`
- Steuerbaugr./DDC TE: `Math.floor(b_steuer / TE_BREITE_MM)` – auch im Nebeneinander-Modus (kein `= Leistung` mehr)
- Textfarben Sidebar: Energieverteilung `#C8720E`, Leistungsbaugr. `#C84E2E`, Steuerbaugr. `#4BBECA`

**Modul 3 – Zonenaufteilung (gesperrt)**
- Mindesthöhen basieren auf physikalischen Festwerten (wie h_ke-Logik), keine Prozent-Eingabe
- `ceil5()` – alle berechneten Mindesthöhen auf 5 mm aufgerundet; Schienensystem-Werte sind exakt (kein ceil5)
- H_KLEMME_STD = 65 mm (Phoenix XTV 6 und PT 2.5 MT je 62,5 mm → aufgerundet)
- h_klemm = ceil5(15+65+15) = 95 mm
- Schienensystem-Höhen (60-mm-Technologie): 3-pol=300, 4-pol=350, 5-pol=400 mm – eigene Recherche
- useEvKanal steuert kanal_ev2 und linken V.Kanal in Evert-Zone (gesperrt)
- kanal_ev (L/S-Seite von Evert) ist immer vorhanden – Abführung zu Leistungszone
- Einspeiseklemmen: WS=3 TE (L1/N/PE), DS=5 TE (L1/L2/L3/N/PE)
- Keine Typbezeichnungen in srcKlemm-Texten (kein Kabeltyp, kein Herstellertyp)
- Anordnung L/S gesperrt (disabled) wenn Modus „Mehrere Felder"
- KE-Position bestimmt Zonenreihenfolge (kommt aus Modul 1/2 via localStorage, read-only)

**Code-Review Fixes (Session 19 – gesperrt)**
- M3: `buildFullLayoutSVG()` – `h_mb_layout = mp_h − h_ke + h_abst` (fehlender h_abst-Term korrigiert)
- M3: `h_kanal_h_mm` + `b_kanal_v_mm` werden in `saveZoneInputs()`/`loadZoneInputs()` persistiert
- M3: Toter CSS-Code (`body.print-ergebnis`) und `#print-ergebnis-container` entfernt
- M3: Kommentar korrigiert: `ceil5(95) = 95 mm` (nicht 85 mm)
- M1+M2: `proj-docnr` nach `updateDocNr()` in localStorage gespeichert → erscheint im Vollständigen Layout
- M1+M2: Guard gegen Division durch Null: `if (!H || !B) return` am Anfang von `calculate()`
- CLAUDE.md: `TE_BREITE_MM = 18,0 mm` (DIN 43880), `H_KLEMME_STD = 65 mm`, `h_klemm = 95 mm`

**Drucklayout (Session 18 – gesperrt)**
- Alle 3 Module: `printErgebnis()` injiziert `@page{size:A4 landscape;margin:10mm 12mm}` per JS-`<style>`-Element (NICHT innerhalb `@media print` – wird von Browsern ignoriert)
- Vollseiten-Ausdruck: Seitenleiste + SVG/Grafik + Ergebnistabelle (kein Container-Switching)
- Corporate Header im `@media print`: `background:#EFEFEC`, `border-bottom:1.5px solid #BBBBBB`, Logo 40×40, Titelblock, `border-left:1px solid #CCC` als Separator zu Projektfeldern
- Hintergrundfarbe erzwingen: `-webkit-print-color-adjust:exact; print-color-adjust:exact` auf `header`
- Projektfelder: `color:#111 !important` auf `.proj-field input` (überschreibt graue Dok.-Nr.-Farbe)
- `fieldset { break-inside:avoid; page-break-inside:avoid }` in allen 3 Modulen
- Modul 3 `.field .lbl`: `overflow:hidden` + `.field .var`: `white-space:normal; word-break:break-all` (verhindert Überlauf langer Variablennamen in Nachbarspalte)

**Persistenz Modul 1 + 2 (Session 17)**
- Alle Eingabefelder inkl. B, H, mp_b, mp_h in `M1_INPUT_FIELDS` / `M2_INPUT_FIELDS` → gespeichert via `m01_si_*` / `m02_si_*`
- `_m1SaveReady` / `_m2SaveReady` Flag: `saveInputs()` ist bis zum Abschluss von `loadSavedInputs()` blockiert
- Preset-Index gesondert als `m01_si_preset` / `m02_si_preset`
- Navigation → Modul 3: `gotoModul3()` setzt `m03_autoselect`, Modul 3 wählt Schranktyp automatisch

**Daten / Architektur**
- Single-File HTML pro Modul (GitHub Pages, kein Build-Step)
- Excel als Pflegewerkzeug (nicht versioniert), JSON als Produktivdatenbank (committed)
- Python läuft in WSL
