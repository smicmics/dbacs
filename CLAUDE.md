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

## Offene Punkte (Stand Session 54 – vor Beginn der nächsten Sitzung lesen)

- Starrer Stabtemperaturfühler mit Flansch für den Lüftungskanal: existiert in
  der europäischen Symaro-Reihe nicht (nur biegsame Kapillare, auch bei
  QAM2120.040). Alternativen anderer Hersteller sind noch zu recherchieren
  (Nutzer-Vorgabe: „Wir werden noch Alternativen suchen").
- Preise mehrerer Session-52-Feldgeräte unbestätigt/fehlend (QBM81-10,
  QBM3020-10, KRM-1-DZ/KRM-2-DZ, Montagekonsole KS) – siehe
  `quelle_hinweis` je Eintrag.
- Grundsatzfrage farbige L1/L2/L3-Klemmen (UT-Reihe Einspeisung) vs. Praxis
  (Nutzer-Hinweis Session 52: „in der Praxis werden die farbigen Klemmen für
  L1 L2 und L3 meist gar nicht eingesetzt") – ggf. später auf grau+PE
  umstellen, noch nicht entschieden.
- Preise Session-53-Feldgeräte unbestätigt: Kanal-CO2-Fühler QPM2100 (kein
  belastbarer EU/EUR-Preis gefunden) und Luftstromwächter KRIWAN INT511
  20N842S021 (gefundene Distributor-Preise nicht eindeutig dieser
  24V-AC/DC-Variante zuordenbar) – siehe `quelle_hinweis` je Eintrag.
- Preise aller 5 Session-54-Feldgeräte unbestätigt/fehlend (QAF64.2-J,
  QBM3020-3, QFM2160, QAA27, QPA2062) – kein belastbarer EUR-Preis gefunden,
  siehe `quelle_hinweis` je Eintrag.
- **Zurückgestellt (Session 54):** Raumtemperatur- und Feuchtesensor mit
  Sollwertversteller sowie Raumtemperatur-/Feuchte-/CO2-Sensor mit
  Sollwertversteller – in der aktuellen Siemens-Symaro-Reihe existiert keine
  Kombination aus (aktivem) Feuchtesignal + Sollwertversteller-Drehknopf
  (Sollwertversteller nur in der älteren rein-passiven QAA25/26/27-Familie,
  nur Temperatur ohne Feuchte). Ein Sollwertversteller zusammen mit CO2
  existiert bei Siemens nur in digitalen Bus-Raumbediengeräten (QAW70/QMX3,
  PPS/KNX) – Protokoll aktuell nicht von DBACS unterstützt (nur mbus/
  modbus_rtu/modbus_tcp). Alternativen anderer Hersteller noch zu
  recherchieren, falls der Nutzer diese beiden Kombinationen weiterhin
  benötigt.
- Preise aller 10 Session-54-Feldgeräte Heizung/Kälte/Sanitär unbestätigt/
  fehlend (QBE1900-P7, QBE2003-P4, QBE2003-P10, PST010RG12S, QVE1901,
  SDBAM6, SYR-933.1, TWP1F, STB1F, STB+TWF) – kein belastbarer EUR-Preis
  gefunden, siehe `quelle_hinweis` je Eintrag.
- **Sicherheitsdruckbegrenzer „2-stufig" (Nutzer-Anfrage Session 54) nicht
  gefunden:** weder im Honeywell/FEMA-SDBAM-Katalog noch sonst ein
  Einzelgerät mit 2 unabhängigen Schaltpunkten in einem Gehäuse gefunden.
  Auf Nutzer-Anweisung zurückgestellt („Stelle die Doppellösung zurück,
  wenn Du kein passendes Gerät bei Honeywell findest") – aktuell nur
  1-stufige SDBAM6-Baugruppen angelegt (`420_000007`/`008`). Bei Bedarf
  später klären, ob 2 in Serie geschaltete SDBAM-Einheiten oder ein anderer
  Hersteller die Anforderung abdecken.
- **Smart Press PST010RG12S (Honeywell/FEMA, `420_000005`) – Pin-Belegung
  der 2 M12-Steckverbinder nicht bis auf Pin-Ebene verifiziert:** nur aus
  einer Katalog-Kurzübersicht (Zubehör-Kabeldosen ST12-5) abgeleitet, kein
  vollständiges Datenblatt mit Anschlussschema gefunden. Vor Verdrahtung im
  Projekt das vollständige Smart-Press-Datenblatt gegenprüfen.
- **Wassermangelsicherung SYR-933.1 (`420_000009`) – Zweck der 4. Ader
  ungeklärt:** Anschlusskabel H05VV-F 4x1mm², obwohl der Wechsler
  (1-polig) nur 3 Signaladern (gemeinsam/Schließer/Öffner) braucht. Weder
  eine separate PE-Klemme noch eine andere Erklärung im Datenblatt/in der
  Bedienungsanleitung gefunden (Schaltbild dort nur als Grafik hinterlegt,
  nicht textuell auslesbar) – aktuell wie bisher mit 2 Klemmen modelliert
  (nur der genutzte Kontakt + gemeinsam). Bei Bedarf SYR direkt kontaktieren
  oder Schaltbild-Grafik visuell prüfen.
- **Sicherheitsdruckbegrenzer SDBAM6 für p-Min-Rolle (`420_000008`)
  entgegen Herstellerkatalog verwendet:** der Honeywell/FEMA-Katalog
  dokumentiert SDBAM ausdrücklich nur für Maximaldrucküberwachung (eigene
  DWR-Baureihe für Minimaldruckbegrenzung vorgesehen) – auf ausdrücklichen
  Nutzer-Wunsch dennoch für beide Rollen eingesetzt, siehe `quelle_hinweis`.
- Preise der 2 USV-Feldgeräte (`2320225` QUINT-UPS-Umschalteinheit,
  `2320296` UPS-BAT-Batteriemodul, beide Phoenix Contact, `480_000011`)
  unbestätigt/fehlend – kein belastbarer EUR-Preis gefunden, siehe
  `quelle_hinweis` je Eintrag.

Sonst keine offenen Punkte – Session 51/52 vollständig implementiert UND im
Browser verifiziert; die daraus erarbeiteten Modellierungsregeln sind jetzt
als verlässliche Grundlage unter „## Baugruppen-Modellierungsregeln
(verbindlich)" verzeichnet (weitere Baugruppen können darauf aufbauen).
Details zum Ergebnis siehe „Modul 4 – Session 51 (komprimiert)" unter
„Formel-Referenz" weiter unten bzw. `docs/archiv/claude-md-modul4-sessions-35-51.md`
und `docs/archiv/claude-md-modul4-session-52.md` für den vollen
Sitzungsverlauf.

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
│   ├── modul-03-architektur/index.html          TE-Berechnung & Reihenkapazität ✅
│   ├── modul-04-innenaufbau/index.html          Baugruppen · Innenaufbau ✅
│   ├── modul-05-feldgeraete/index.html          Feldgeräte-Stückliste (rein lesend, gespeist aus Modul 4) ✅
│   └── modul-07-stammdatenpflege/index.html     Artikeldaten-Katalog-Browser (rein lesend) ✅
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
│   ├── einzelbauteile.json                      Modul-4-Bauteilkatalog (committed, seit Session 27 über Excel gepflegt)
│   ├── baugruppen.json                          Modul-4-Baugruppen-DB (committed, seit Session 27 über Excel gepflegt)
│   ├── feldgeraete.json                         Feldgeräte-Katalog außerhalb des Schaltschranks (committed, Modul 5)
│   └── xlsx_to_json.py                          Konvertierungsskript Excel → JSON (9 Datensheets + 2 reine Referenz-Sheets `funktionsbereiche`/`zonen`, `einzelbauteile`/`baugruppen`+`baugruppen_bauteile`-Verknüpfungstabelle seit Session 27)
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
| Modul 4 | https://smicmics.github.io/dbacs/modules/modul-04-innenaufbau/ |
| Modul 5 | https://smicmics.github.io/dbacs/modules/modul-05-feldgeraete/ |
| Modul 7 | https://smicmics.github.io/dbacs/modules/modul-07-stammdatenpflege/ |
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
- **Entwickler-Workflow Daten:** Excel bearbeiten → in WSL: `cd /mnt/c/users/smi/cowork/dbacs/data && python3 xlsx_to_json.py` → exportiert alle 9 JSON-Dateien → alle committen
- **Seit Session 39: Claude pflegt `ga_komponenten.xlsx` direkt** (Nutzer-Entscheidung) – nicht mehr nur Recherche-Werte liefern, sondern selbst per Skript in die Excel-Datei schreiben. Vor jedem Schreibzugriff `~$ga_komponenten.xlsx`-Lockdatei prüfen (Excel muss geschlossen sein) UND vor strukturellen Änderungen (neue Sheets, Spalten-Umbenennungen) eine Kopie nach `C:\Users\SMI\Backups\dbacs\excel\` sichern – die Datei ist NICHT git-versioniert, es gibt sonst kein Sicherheitsnetz.
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

## Baugruppen-Modellierungsregeln (verbindlich)

Diese 7 Regeln wurden über Modul-4/5-Sessions 51/52 anhand konkreter
Feldgeräte-Baugruppen erarbeitet und vom Nutzer als verlässliche Grundlage
für alle künftigen Baugruppen bestätigt. Ausführliche Herleitung/Beispiele:
`docs/archiv/claude-md-modul4-session-52.md`.

1. **Klemmzonen-Grundsatz (Sensor vs. Feldgerät):** `klemm_s` ist für echte
   Messsensoren reserviert – sowohl passiv (Widerstandsmessung ohne
   Hilfsenergie) als auch aktiv mit Analogausgang. Jedes Schaltgerät
   (binärer Kontakt/Relaisausgang, kein Analogsignal) ist ein Feldgerät und
   gehört auf `klemm_f` – auch wenn sein Signal am Ende als BI an die DDC
   geht (die Zone richtet sich nach der Signalart am Gerät, nicht nach dem
   Ziel). Nur echte Leistungs-/Netzanschlüsse (Versorgung, Leistungssteuerung
   zu einem Aktor) bleiben `klemm_l`.
2. **Kabel-Klemmen-Kohärenz:** 1 Kabel = zusammenhängende Klemmen in EINER
   Zone; mehrere Kabel = Aufteilung auf mehrere Zonen zulässig.
3. **Farbcodierung:** nur echte Bus-/Versorgungsanschlüsse (Leistungs-
   anschlüsse, echte Busklemmen) sind farbig. Alle Melde-/Relaiskontakt-
   Klemmen bleiben Standard-grau, unabhängig davon in welcher Zone sie
   liegen.
4. **Namensregel:** Auswahltext-Suffix-Reihenfolge, jeweils nur falls
   zutreffend: `Text Bauteil → Messbereich → Versorgungsspannung →
   Zulassungen/Zertifizierungen`.
5. **Steuerspannungs-Grundsatz:** jedes Feldgerät mit eigener Versorgungs-
   spannung braucht eine passende, abgesicherte Steuerspannungsquelle
   (230V AC/24V AC → Trenn-/Steuertrafo + 2 Sicherungen; 24V DC → Netzteil +
   1 Sicherung) – „alles nach Erfordernis": ist die Quelle im Projekt schon
   vorhanden, nichts tun, sonst automatisch ergänzen (Ratchet-Mechanismus,
   nie doppelt). Eine Desigo-PX-CPU mit 24V-AC-Bedarf teilt sich denselben
   Sicherheitstrafo mit den 24V-AC-Feldgeräten im selben Schrank (Siemens-
   Vorschrift) – ein Trafo pro Schrank für alle 24V-AC-Verbraucher, bewusst
   ohne VA-Kapazitätsbilanzierung.
6. **Sicherheitsketten-Pattern (Koppelrelais):** hat ein Feldgerät nur 1
   Wechslerkontakt, braucht aber gleichzeitig eine Leistungssteuerung
   (Abschaltung) UND eine getrennte DDC-Meldung, wird ein Koppelrelais
   zwischengeschaltet (Sensor-Wechsler → Relaisspule → 2 galvanisch
   getrennte Ausgänge). **Spulenspannung Standard 230V AC** – erlaubt
   längere zulässige Kabelstrecken bis zur Anlage als 24V AC. **24V AC ist
   gleichwertig einsetzbar:** beide Varianten laufen über einen
   Sicherheitstrafo, daher kein Unterschied in der Ausfallsicherheit
   zwischen ihnen. **Nicht 24V DC:** eine DC-Spule bräuchte ein
   zusätzliches Netzteil als weiteren Ausfallpunkt in der Sicherheitskette.
   Geräte mit bereits mehreren getrennten nativen Kontakten (z. B.
   Kanalrauchmelder mit Umschalter+Öffner) brauchen dieses Pattern nicht.
   Interne Geräte mit eigenen Schraubklemmen (wie das Koppelrelais selbst)
   brauchen keine zusätzlichen Landeklemmen für ihre Ausgänge – die
   geräteeigenen Klemmen sind der Anschlusspunkt.
7. **Artikel-Referenz-Integrität:** `baugruppen_bauteile.artikel_nr` muss
   immer die echte Katalog-Artikelnummer sein, nie eine Typbezeichnung –
   ein Lookup-Fehler schlägt sonst still fehl (`if (!eb) return`), das
   Bauteil verschwindet unbemerkt aus Zeichnung UND Stückliste. Nach
   größeren Umbauten hilft ein vollständiger Katalog-Scan (alle
   `baugruppen[].bauteile[].artikel_nr` gegen alle
   `einzelbauteile[].artikel_nr` prüfen).
8. **PE-/Schutzleiterklemme (Session 54 Nachtrag, verbindlich):** hat ein
   Feldgerät laut Originaldatenblatt im Klemmen-/Anschlussplan einen
   **eigenen, separat aufgeführten** Erdungs-/Schutzleiteranschluss
   (zusätzlich zu den Signal-/Kontaktklemmen), bekommt die Baugruppe eine
   zusätzliche Schutzleiterklemme (grün-gelb, z. B. `3209536` in
   klemm_l/f/s, analog `304xxxx`-PE-Typen in klemm_e) in derselben Zone.
   **Nicht** allein anhand der Schutzklasse (I/II/III) entscheiden – mehrere
   Schutzklasse-I-Geräte in Session 54 hatten laut Anschlussplan trotzdem
   KEINE separate PE-Klemme (Erdung läuft dort über die ins bereits
   geerdete Rohrsystem eingeschraubte Metall-Tauchhülse/-verschraubung,
   nicht über eine gesonderte Ader). Maßgeblich ist ausschließlich, ob der
   Klemmenplan im Datenblatt eine eigene Erdungsklemme explizit ausweist.
   Bei Neuanlage künftiger Baugruppen den Klemmenplan gezielt darauf prüfen
   (Suche nach „ground"/„Erdung"/„Schutzleiter" im Originaldatenblatt, nicht
   nur die Katalog-Kurzübersicht).

---

### Modul 4/5 – Kanal-CO2/VOC-Fühler + Luftstromwächter (Session 53, gesperrt)
Erste Baugruppen nach der Session-52-Konsolidierung – Testfall für die neuen
Modellierungsregeln, keine Korrekturen nötig (Regeln direkt beim ersten
Versuch korrekt angewendet). 4 neue Baugruppen `430_000017`–`430_000020`
(alle Lüftung), Siemens Symaro-Baureihe QPM11../QPM21.. (Datenblatt
CE1N1962de, 2025-03-26, aktuell):
- `430_000017` „Kanal-CO2-Fühler" (QPM2100, 3 Klemmen G/G0/X1, 1x AI)
- `430_000018` „Kanal-VOC-Fühler" (QPM1100, 3 Klemmen, 1x AI)
- `430_000019` „Kanal-CO2/VOC-Kombifühler" (QPM2102, 4 Klemmen G/G0/X1/X2,
  2x AI – X1 CO2-Rohsignal, X2 Maximalauswahl-Lüftungsbedarfssignal)
- `430_000020` „Luftstromwächter" – **Herstellerabweichung KRIWAN**: Siemens'
  eigenes `INT511` ist im HIT-Portal abgekündigt, der Originalhersteller
  KRIWAN Industrie-Elektronik führt das Gerät unverändert als aktuelles
  Produkt weiter (analog Oppermann/Metz-Connect-Präzedenzfall). 24V-AC/DC-
  Variante `20N842S021`, kalorimetrisch 0,2-10m/s, Relais-Wechsler. Nach
  Regel 1 (Schaltgerät, kein Analogsignal) komplett `klemm_f` (4 Klemmen:
  2x Versorgung + 2x Relaiskontakt COM/NO), 1x BI.

**Alle 4 Geräte bringen ihren Kanalmontage-Flansch bereits im
Lieferumfang mit** (Originaldatenblätter explizit geprüft) – kein
separater Zubehör-Mechanismus nötig, anders als zunächst vom Nutzer
erwartet. Alle 4 Baugruppen `benoetigt_steuerspannung:'24vac'` (Regel 5).

Verifiziert direkt im Browser (frischer Tab, Standschrank über Modul
2+3-Pipeline, Drehstrom-Netztyp): Stückliste zeigt korrekt `KS`
Durchgangsklemme ×10 (3+3+4) und `KF` ×4, Steuerspannungs-Automatik
ergänzt korrekt 1x `Steuertransformator 400V/24V 250VA` (Drehstrom-
Variante via `resolveNetztypArtikel()`) + 2x LSS + automatisch ergänzte
CPU/E-A-Module (`Physikalisch gesamt: 5` = 4 AI + 1 BI, `Feldgeräte
gesamt: 4`). Modul 5 zeigt alle 4 Geräte mit korrektem Hersteller
(3x Siemens, 1x KRIWAN) und Preisen (239,90€/657,00€ bepreist, 2x
unbepreist „–", Summe 896,90€). Keine Konsolenfehler.

### Modul 4 – Baugruppen-Dropdown nach Kategorie gruppiert (Session 53 Nachtrag, gesperrt)
Nutzer-Wunsch: bei wachsender Baugruppenzahl wird die flache Dropdown-Liste
unübersichtlich – Gruppierung analog zur bereits bestehenden
Einzelbauteile-Kategorisierung (`populateEinzelAuswahl()`, Session 27/40).
Neues Feld `baugruppen.kategorie` (rein optische Gruppierung, unabhängig von
`zone`/`gewerk`/`funktionsbereich` – exakt wie bei `einzelbauteile.kategorie`),
alle 30 Bestands-Baugruppen zugeordnet: **Raumsensoren**, **Luftkanalsensoren**,
**Luftkanalwächter**, **Tauchfühler**, **Datenpunkt-Reserve**,
**Automationsstation**, **Energieversorgung** (Kategorie + die 3 Baugruppen
`480_000008`–`010` direkt im Anschluss auf Nutzer-Wunsch von „Steuerspannung"
auf „Energieversorgung" umbenannt – betrifft nur Anzeigename/Kategorie/
Namens-Präfix in `beschreibung`, NICHT das interne Feld
`benoetigt_steuerspannung`/die JS-Bezeichner `STEUERSPANNUNG_*` – die bleiben
als technische Schema-/Codenamen unverändert). Die vom Nutzer vorgeschlagene
Kategorie „Raumwächter" bleibt bis zur ersten passenden Baugruppe ungenutzt –
Kategorien entstehen rein aus den Daten, keine leeren Platzhalter nötig).
`filterBaugruppen()` baut jetzt `<optgroup>`-Elemente (alphabetisch sortiert,
wie bei den Einzelbauteilen), `BG_SORT_PRIORITY` bleibt als Sortierung
*innerhalb* einer Kategorie erhalten (wirkt aktuell nur auf die 6
Datenpunkt-Reserve-Baugruppen: AI→AO→AO+LVB→BI→BO→BO+LVB). **Gleiche strikte
Regel wie bei den Einzelbauteilen (Session 40): eine Baugruppe OHNE
`kategorie` fehlt komplett im Dropdown** – jede künftige neue Baugruppe
braucht also zwingend eine Kategorie.

Verifiziert direkt im Browser (Hard-Reload zur Vermeidung von Skript-Caching):
Lüftung-Tab zeigt korrekt 3 Gruppen (Luftkanalsensoren/-wächter,
Raumsensoren), Automation-Tab 3 Gruppen (Automationsstation,
Datenpunkt-Reserve in der richtigen Priorität, Steuerspannung),
Heizung-Tab 2 Gruppen (Raumsensoren, Tauchfühler). Hinzufügen einer
Baugruppe aus dem gruppierten Dropdown funktioniert unverändert
(`addBaugruppe()`/Mengen-Merge betroffen von der Umstellung nicht). Keine
Konsolenfehler.

### Modul 4/5 – Weitere Lüftungswächter/-sensoren + Raumsensoren (Session 54, gesperrt)
5 neue Baugruppen `430_000021`–`430_000025` (alle Lüftung, Siemens-Leitfabrikat,
Originaldatenblätter recherchiert – teils binär-komprimierte Siemens-PDFs
per `pypdf` in WSL ausgelesen, Session-41-Präzedenzfall):
- `430_000021` „Frostschutzwächter, Kapillare 2m" (Symaro QAF64.2-J) –
  Kombigerät mit kontinuierlichem 0-10V-Temperatursignal UND potentialfreiem
  Relais-Wechslerkontakt; hier bewusst nur der Schaltkontakt verdrahtet
  (Nutzer-Entscheidung, schlanker/konsistent zu den übrigen
  Luftkanalwächter-Baugruppen). Braucht selbst 24V-AC-Versorgung (2
  zusätzliche Feldklemmen G/G0) UND folgt dem Sicherheitsketten-
  Koppelrelais-Pattern (Regel 6, 1 Wechsler reicht nicht für Ventilator-
  Abschaltung + getrennte DDC-Meldung) – 4 Feldklemmen + 1 Koppelrelais
  (230VAC-Spule) im Leistungsfeld, 1x BI.
- `430_000022` „Differenzdrucksensor Kanal 0...300 Pa" (Symaro QBM3020-3) –
  Analogsensor (0-10V, 3 Klemmen G/M/U), 1x AI. Baugleiche Baureihe wie das
  bereits katalogisierte QBM3020-10 (`430_000013`), nur anderer Messbereich.
- `430_000023` „Kanalfühler für Feuchte und Temperatur" (Symaro QFM2160,
  Nachfolgebezeichnung des im Handel als „QFM21.." abgekündigten
  Vorgängers) – 4 Klemmen G/G0/X1(Feuchte)/X2(Temp), 2x AI.
- `430_000024` „Raumtemperatursensor passiv mit Sollwertversteller ±3K"
  (Siemens QAA27, gleiche Gerätefamilie wie das bereits katalogisierte
  QAA24) – passiv, 3 Klemmen B/M/R (Temperatur- und Sollwertsignal getrennt,
  je eigener passiver Messkanal), 2x AI.
- `430_000025` „Raum-CO2-, Feuchte- und Temperatursensor" (Symaro QPA2062,
  gleiche Familie wie QPA2000/QPA1000) – 5 Klemmen G/G0/X1(CO2)/X2(Feuchte)/
  X3(Temp), 3x AI.

**Nutzer-Fund/-Entscheidung:** die vom Nutzer ebenfalls angefragte
„Differenzdruckmessung ca. 100-1000 Pa" hätte exakt denselben Siemens-
Artikel (QBM3020-10) ergeben, der bereits als `430_000013` „Drucksensor
Kanaldruck" existiert – auf Nutzer-Hinweis („Wenn der Drucksensor schon da
ist, dann keine neue Baugruppe anlegen dafür") keine zweite Baugruppe mit
identischem Artikel angelegt. Die beiden Kombinationen „Feuchtesensor mit
Sollwertversteller" und „CO2/Feuchte-Sensor mit Sollwertversteller" wurden
zurückgestellt, da kein passendes Siemens-Symaro-Produkt existiert (siehe
„Offene Punkte" oben).

Alle 5 neuen Feldgeräte-Artikel zusätzlich in `feldgeraete.json` angelegt
(Kategorie „Kanalsensor"/„Raumsensor", analog zu allen bisherigen
Lüftungssensor-Baugruppen – 100%ige Verknüpfungsdichte
`feldgeraet_artikel_nr` ↔ `feldgeraete.json` vor dieser Session geprüft und
bewusst fortgeführt), noch ohne bestätigten Preis.

Verifiziert direkt im Browser (Standschrank über Modul 2+3-Pipeline,
Drehstrom-Netztyp): alle 5 Baugruppen im Lüftung-Tab korrekt in ihren
Kategorien einsortiert und hinzufügbar, Stückliste aggregiert korrekt `KF`
×4 (Frostwächter-Feldklemmen) und `KS` ×15 (3+4+3+5, restliche 4 Baugruppen),
DDC-Statistik zeigt korrekt `Physikalisch gesamt: 9` (8 AI + 1 BI) und
`Feldgeräte gesamt: 5`. Steuerspannungs-Automatik ergänzt korrekt sowohl
1x Steuertransformator 400V/24V (Drehstrom-Variante, 4 der 5 Baugruppen
brauchen 24V AC) als auch 1x Sicherheits-/Trenntransformator 400V/230V
(für die Koppelrelais-Spule) mit je zugehörigen Sicherungen; DDC-Module
automatisch ergänzt (2x TXM1.8U für 8x AI, 1x TXM1.16D für 1x BI, 1x
PXC7.E400.A). Keine Konsolenfehler.

**Nachtrag (Session 54, gesperrt):** Nutzer-Wunsch nach dem ersten Durchlauf
– Auswahltext des bereits bestehenden `430_000013` („Drucksensor
Kanaldruck") und des neuen `430_000022` angleichen und im Dropdown
hintereinander anzeigen. Beide jetzt einheitlich „Differenzdrucksensor
Kanaldruck 0...XXXX Pa, 24V AC/DC" (Namensregel: Text Bauteil →
Messbereich → Versorgungsspannung, siehe Regel 4). Dabei fiel auf, dass die
neu formulierte Klemmenbezeichnung in der Beschreibung fälschlich „G/G0"
statt der laut Originaldatenblatt CA1N1916en01 tatsächlichen Klemmen „G
(Versorgung) / M (Messnull) / U (Signal)" nannte – korrigiert in beiden
Baugruppen sowie in den zugehörigen `feldgeraete.json`-Einträgen
(QBM3020-10/-3). Reihenfolge im Dropdown folgt bei Baugruppen ohne
`BG_SORT_PRIORITY`-Eintrag der Zeilenreihenfolge im Excel-Sheet
(`filterBaugruppen()`, stabiler Sort) – `430_000022` daher direkt hinter
`430_000013` in die Excel-Zeilenreihenfolge einsortiert (IDs selbst bleiben
unverändert, nur die Zeilenposition wurde getauscht). Verifiziert im
Browser: beide Einträge erscheinen jetzt konsistent benannt und
unmittelbar hintereinander im Lüftung-Tab, keine Konsolenfehler.

### Modul 4/5 – Heizung/Kälte/Sanitär: Druck-, Strömungs- und Temperaturwächter (Session 54, gesperrt)
Erste Baugruppen für die wasserführenden Gewerke (410 Sanitär/420 Heizung/
434 Kälte) – bisher waren nur Lüftung (430) und Automation (480) befüllt.
Neue Kategorie „Sensoren und Wächter" (analog „Luftkanalsensoren" in
Lüftung) eingeführt, 12 neue Baugruppen `420_000001`–`420_000012`
(führendes Gewerk 420/Heizung, da alle Baugruppen heizungsrelevant sind;
`funktionsbereich`-Array steuert die Sichtbarkeit in den einzelnen Tabs).
Planungsfabrikat für diese Gerätegruppe **Siemens QBE-/QVE-Baureihe**
(Druck-/Strömungssensorik) bzw. **Honeywell/FEMA** (mechanische mediengefüllte
Druck-/Temperaturschalter, Sicherheitsbegrenzer – Siemens führt diese
Gerätekategorien nicht) – neues Muster für „wo Siemens nicht fündig wird":
Honeywell/FEMA als zweite Planungsfabrikat-Ebene für Heizung/Kälte/Sanitär-
Sicherheitstechnik (analog KRIWAN-Ausnahme bei Lüftung, Session 53):
- `420_000001`/`002` „Druckwächter Max/Min" (Siemens QBE1900-P7, -0,3...7 bar,
  Wechselkontakt, selbstrückstellend) – **ein Gerätetyp für beide Rollen**
  (Nutzer-Entscheidung: Kontaktwahl Schließer/Öffner vor Ort entscheidet
  Max/Min, keine zwei Artikel nötig). Namenskonvention auf Nutzer-Wunsch:
  Messbereich immer im Namen, Funktionskennung „(p-Max)"/„(p-Min)" am Ende
  der Beschreibung – **gilt als Vorlage für alle künftigen Wächter-Paare**.
- `420_000003`/`004` „Drucksensor 0-4bar/0-10bar" (Siemens QBE2003-P4/-P10,
  0-10V, G/U/M-Klemmenschema wie QBM3020).
- `420_000005` „Drucksensor und -wächter Kombi" (Honeywell/FEMA Smart Press
  PST010RG12S) – einziges gefundenes Gerät mit gleichzeitig 2 Schaltausgängen
  UND Analogausgang 0-10V in einem Gehäuse; Versorgung DC14-36V (erste
  Baugruppe mit `benoetigt_steuerspannung:'24vdc'` außerhalb der reinen
  DDC-Netzteile) – Pin-Belegung der 2 M12-Steckverbinder nur näherungsweise
  bekannt, siehe „Offene Punkte".
- `420_000006` „Strömungswächter" (Siemens QVE1901) – schraubt direkt in ein
  T-Stück mit G½"-Innengewinde, Paddel kürzbar für DN20-200.
- `420_000007`/`008` „Sicherheitsdruckbegrenzer Max/Min" (Honeywell/FEMA
  SDBAM6, 1,2-6 bar, TÜV/DGRL 2014/68/EU, plombierbar/manueller Reset) –
  Herstellerkatalog dokumentiert dieses Gerät nur für Maximaldrucküber-
  wachung, auf Nutzer-Wunsch dennoch für beide Rollen verwendet (siehe
  „Offene Punkte"). Die vom Nutzer angefragte „2-stufige" Variante (2
  unabhängige Schaltpunkte in einem Gehäuse) wurde nicht gefunden und
  zurückgestellt.
- `420_000009` „Wassermangelsicherung" (**SYR/Hans Sasserath 933.1**,
  DN20, mit Verriegelung) – weder Siemens noch Honeywell/FEMA noch IFM
  führen Wassermangelsicherungen im Programm, SYR als weitere
  Herstellerabweichung recherchiert und mit Nutzer abgestimmt (Hinweis kam
  leicht verunklart als „Sasserat nbach" – korrekt aufgelöst zu SYR/Sasserath).
- `420_000010`/`011`/`012` „Temperaturwächter"/„Sicherheitstemperatur-
  begrenzer"/„Kombi Temperaturwächter+STB" (Honeywell/FEMA TWP1F/STB1F/
  STB+TWF, alle G½"-Tauchhülse Messing, TÜV-geprüft nach DIN EN14597/DGRL
  2014/68/EU) – STB+TWF hat 2 unabhängige native Schaltelemente (Öffner für
  STB + Wechsler für TW) in einem Gehäuse, braucht daher **kein**
  Koppelrelais (Regel-6-Ausnahme wie beim Kanalrauchmelder).

**Modellierungsmuster bestätigt:** alle mechanischen Schalter (Druck-,
Strömungs-, Temperaturwächter/-begrenzer) sind potentialfrei und brauchen
keine eigene Steuerspannung (2 Klemmen je Kontakt, `klemm_f`, 1x BI) – nur
die elektronischen Sensoren/Transmitter (Drucksensor, Kombi-Drucksensor)
brauchen eine Versorgungsspannung (`benoetigt_steuerspannung`).

**Nachtrag (Session 54, gesperrt):** Nutzer-Wunsch nach dem ersten
Durchlauf – Kategorie „Sensoren und Wächter" in zwei getrennte Kategorien
aufgeteilt: **„Sensoren flüssiges Medium"** (kontinuierliches Analogsignal:
`420_000003`–`005` Drucksensoren + Kombi) und **„Wächter flüssiges
Medium"** (reiner Schaltkontakt: `420_000001`/`002`/`006`–`012`). Die
Kombi-Baugruppe `420_000005` (Analogausgang UND 2 Schaltausgänge) bewusst
bei Sensoren einsortiert (Namensreihenfolge „Drucksensor und -wächter"
sowie thematische Nähe zu den beiden reinen Drucksensor-Baugruppen).
Zusätzlich die bisher eigenständige Kategorie „Tauchfühler" (Heizung/Kälte,
`430_000006`/`007`) aufgelöst und in „Sensoren flüssiges Medium"
überführt – damit gibt es keine Einzel-Kategorie mit nur 2 Einträgen mehr,
und Drucksensoren/Tauchfühler stehen thematisch zusammenhängend im
Dropdown, analog zum Luftkanalsensoren/-wächter-Muster aus Lüftung.
Verifiziert im Browser (Sanitär/Heizung/Kälte-Tabs): korrekte 2-Gruppen-
Aufteilung je Tab, keine Konsolenfehler.

Verifiziert direkt im Browser (Standschrank über Modul 2+3-Pipeline,
Drehstrom-Netztyp, zusätzlich zu den 5 Lüftungssensor-Baugruppen aus
demselben Sitzungslauf): alle 12 Baugruppen korrekt in „Sensoren und
Wächter" gruppiert, Sanitär-Tab zeigt korrekt nur die 6 gewerkübergreifenden
Geräte, Kälte-Tab zusätzlich die 2 Sicherheitsdruckbegrenzer, Heizung alle
12. Stückliste aggregiert korrekt `KF` 28 und `KS` 22 (kumulativ mit den 4
KF/15 KS aus den Lüftungssensoren). DDC-Statistik `Physikalisch gesamt: 24`
(11 AI + 13 BI, kumulativ), `Feldgeräte gesamt: 17`. Steuerspannungs-
Automatik ergänzt korrekt alle drei benötigten Quellen gleichzeitig: 24V-AC-
Trafo (Drehstrom-Variante), 230V-AC-Trenntrafo (Koppelrelais aus den
Lüftungssensoren) UND erstmals ein 24V-DC-Netzteil (QUINT-PS/1AC/24DC/2,5)
für die Smart-Press-Kombi-Baugruppe. Keine Konsolenfehler.

**Nachtrag PE-Klemme (Session 54, gesperrt):** Nutzer-Nachfrage „haben
Druckwächter/Strömungswächter wirklich keine Versorgungsspannung, da steht
ja nichts dazu" führte zur systematischen Nachprüfung aller Original-
Installationsanleitungen (nicht nur Katalogseiten) auf Erdungs-/PE-Klemmen.
Ergebnis: **`420_000001`/`002` (Druckwächter Max/Min, Siemens QBE1900-P7,
Schutzklasse I) hatten eine fehlende PE-Klemme** – Datenblatt weist explizit
„1x for grounding connection" als 4. Klemme zusätzlich zu den 3
Signalklemmen aus. Beide Baugruppen um 1x Schutzleiterklemme `3209536`
(grün-gelb, `klemm_f`) ergänzt (jetzt 3 statt 2 Klemmen je Baugruppe).
Alle übrigen Session-54-Wächter/-Sensoren gezielt gegengeprüft (QVE1901
Schutzklasse II, QBE2003-P Schutzklasse III, SDBAM6 laut Anleitung nur
„Klemme 1 und 3", STB1F/TWP1F/STB+TWF laut baugleicher Schwesterserie
STW/STB trotz Schutzklasse I nur 3 Klemmen ohne separate PE) – **keine
Änderung nötig**, siehe Regel 8 unter „Baugruppen-Modellierungsregeln
(verbindlich)" für die daraus abgeleitete, undogmatische Prüfregel
(Datenblatt-Klemmenplan entscheidet, nicht pauschal die Schutzklasse).
`SYR-933.1` (Wassermangelsicherung) bleibt als einziger Fall ungeklärt
(4-adriges Anschlusskabel bei nur 3 benötigten Signaladern, Schaltbild im
Datenblatt nur als Grafik hinterlegt, nicht textuell auslesbar) – siehe
„Offene Punkte". Verifiziert im Browser (isolierter Test nur mit den 2
Druckwächter-Baugruppen, `m04_belegung` zuvor geleert): Stückliste zeigt
korrekt `KF Durchgangsklemme` ×4 (Positionen #1–#2, #4–#5) und `KF
Schutzleiterklemme PE` ×2 (Positionen #3, #6), keine Konsolenfehler.

**Nutzer-Feedback (Session 54, gesperrt):** ab sofort nach Neuanlage jeder
Baugruppe eine kurze Herleitungs-Tabelle bereitstellen (Baugruppe → Klemmen
lt. Datenblatt → daraus abgeleitete DBACS-Klemmen/Zone → Datenpunkte) –
spart dem Nutzer eigene Testarbeit beim Durchklicken in Modul 4. Siehe auch
Memory `feedback_baugruppen_herleitung.md`.

### Modul 4/5 – Schaltschrank-USV (Session 54, gesperrt)
Erste Baugruppe für Gewerk 480/Automation seit Session 50, `480_000011`
„Schaltschrank-USV 24V DC mit Meldekontakten" – bereits in Session 53 als
künftiger Punkt angekündigt, jetzt umgesetzt. Zweite Planungsfabrikat-Ebene
diesmal bewusst NICHT über „Siemens hat nichts, also Alternative" gewählt:
Siemens hat mit SITOP UPS500S/UPS1600 durchaus passende USV-Produkte mit
Meldekontakten gefunden (siehe Recherche), aber Nutzer-Entscheidung fiel
bewusst auf **Phoenix Contact QUINT-UPS**, um dieselbe Marke wie das
bereits bestehende 24V-DC-Netzteil (`480_000009`, Planungsfabrikat-
Konsistenz) zu nutzen. Aufbau folgt dem Phoenix-Systemkonzept „Netzteil +
elektronische Umschalteinheit + Energiespeicher" (3 getrennte Bausteine):
- Vorhandenes 24V-DC-Netzteil (Ratchet-Mechanismus, automatisch ergänzt
  falls noch nicht vorhanden) → **QUINT-UPS/24DC/24DC/10** Umschalteinheit
  (`2320225`, IQ-Technologie, Kondensator-/Akku-Pufferung bis 3h bei
  38Ah) → **UPS-BAT/VRLA/24DC/1,3AH** Batteriemodul (`2320296`, kleinste
  Standardgröße, ~20min bei 2A/~5min bei 5A, werkzeugloser Wechsel,
  eigene interne 15A-Sicherung) – beide als eigenständige Hutschienen-
  Bausteine im Leistungsfeld (`leist`), analog zu den bestehenden
  Trafo-/Netzteil-Baugruppen.
- 3 potentialfreie Meldekontakte (Schließer, DIN-Kontaktnummerierung
  13/14 Alarm, 23/24 Batteriebetrieb, 33/34 Batterieladung) auf je 2
  Landeklemmen in `klemm_f`, Datenpunktbedarf 3x BI.
- `benoetigt_steuerspannung:'24vdc'` auf Baugruppenebene, damit die
  Steuerspannungs-Automatik bei Bedarf das 24V-DC-Netzteil eigenständig
  ergänzt (getestet: isolierte Belegung nur mit dieser einen Baugruppe
  ergänzte korrekt 1x QUINT-PS/1AC/24DC/2,5).

Verifiziert direkt im Browser (Standschrank, `m04_belegung` zuvor
geleert): Baugruppe erscheint korrekt unter „Energieversorgung" im
Automation-Tab, `Physikalisch gesamt: 3` (3x BI), `Feldgeräte gesamt: 0`
(kein `feldgeraet_artikel_nr` – interne Schaltschrank-Komponente, kein
externes Betriebsmittel), Stückliste zeigt Umschalteinheit + Batteriemodul
+ `KF Durchgangsklemme` ×6 sowie automatisch ergänztes QUINT-PS. Keine
Konsolenfehler.

### Modul 4 – Session 51 (komprimiert)
Vollständiger Sitzungsverlauf (Nutzer-Funde, Root-Cause-Analysen,
Verifizierungsdetails) archiviert in
`docs/archiv/claude-md-modul4-sessions-35-51.md`. Ergebnisse:

- **Klemmen-Gruppen-Split-Verdacht verworfen** (kein echter Bug): der
  gemeldete Fall (Wandschrank, 2 Felder) ist über die echte UI nicht
  erreichbar – `calculateZones()` erzwingt bei Wandschrank immer
  `zone_modus='1feld'`.
- **`idxLabelSVG()`-Fix:** Positionsnummern (`#idx`) verschwanden komplett
  (statt kleiner zu werden), sobald sie bei gleicher Blockgröße mehr Ziffern
  brauchten als beim ersten Berechnungslauf – Schriftgröße wird jetzt aus
  Box- UND Textlänge berechnet, mit garantierter Rückfallebene (nie mehr
  leer).
- **Baugruppen-Dropdown-Sortierung:** `BG_SORT_PRIORITY` (reine
  Anzeigesortierung, unabhängig von der DIN-276-`id`) – AI → AO → AO+LVB →
  BI → BO → BO+LVB → Rest.
- **Farbe automatisch ergänzter DDC-Geräte** in der Zeichnung: `#D8D5CE`
  (echtes Hellgrau, kontrastreich auf dem Zeichenpapier `#FDFCF8` –
  Zwischenstand `#9A9890`/`--tx2` war ein UI-Grauton, auf Papier weiterhin zu
  dunkel). Farbpunkt in der Belegungsliste bewusst unverändert.
- **Onboard-Kapazität der Kompaktstationen `PXC4.E16.A`/`PXC5.E24.A`
  berücksichtigt:** `buildQueues()` entschied bisher über externe TX-I/O-
  Module BEVOR die gewählte CPU aufgelöst war – deren Onboard-Kapazität
  konnte nie angerechnet werden. CPU-Auflösung jetzt vor
  `computeDdcAutoModules()`; `PXC4.E16.A` bekam `dp_ai=12`/`dp_ao=12`,
  `PXC5.E24.A` `dp_ai=16`/`dp_ao=16` (analog zur `TXM1.8U`-Konvention: nur
  AI/AO, bewusst kein `dp_bi`/`dp_bo`-Zuschlag aus dem universellen Pool).
  Nur die ERSTE CPU-Gruppe bekommt den Onboard-Zuschlag (konservativ) – die
  bestehende Überlauf-Logik (`max_ea_module`, eigenes Netzteil+Sicherung je
  Zusatzgruppe, Session 50) bleibt unverändert und wurde erneut end-to-end
  bestätigt.
- **Klemmenauswahl-Varianten (Standard/Doppelstock/Trennklemme/
  DS-Trennklemme):** Radiogruppe im Block „Grund- & Reserveangaben"
  (`localStorage['m04_klemmen_variante']`). Katalog-Verkettung über
  `trennklemme_variante_artikel_nr`/`doppelstock_variante_artikel_nr` auf
  der Standardklemme `3209510` (`resolveKlemmeArtikel()`/
  `resolveBaugruppenBauteile()` – MUSS identisch in `buildQueues()` UND
  `aggregateStueckliste()` verwendet werden, sonst laufen Zeichnung und
  Stückliste auseinander). Referenzklemme aller 6 DDC-Baugruppen von blau
  (`3209523`) auf grau (`3209510`) geändert.
- **Doppelstockklemmen-Kapazität korrigiert:** eine Doppelstockklemme
  (4 Anschlüsse) teilt sich jetzt korrekt 2 Baugruppen-Instanzen (vorher nur
  2 von 4 Anschlüssen genutzt) – Instanz-Schleife läuft bei aktiver
  Doppelstock-Variante in Zweierschritten, `aggregateStueckliste()` zählt
  `Math.ceil(menge/2)` statt `menge`.
- **Stückliste zeigte automatisch ergänzte DDC-Module nicht** (CPU/
  Netzteil/Sicherung/E-A-Module) – neue globale `letzteDdcAuto` +
  `ddcAutoZone(eb)`-Helper (Zone NICHT über `bauteil_typ` raten: die
  Sicherung trägt katalogseitig `'lss'`, nicht `'sicherung'`).
- **CPU-Typ-Dropdown** (`#cpu_typ_override`, Statistikfeld) – manuelle Wahl
  hat Vorrang vor `auto_ea_cpu`. Summenanzeige „Physikalisch/Kommunikativ
  gesamt" rechts daneben.
- **Klemmleisten: reale mm-Breite statt TE-Rundung** – `eb.te_breite =
  ceil(b_mm/18)` rundete eine 5,2mm-Klemme auf eine volle 18mm-TE-Einheit
  auf (korrekt für Hutschienengeräte in `leist`/`steuer`, falsch für
  Reihenklemmen). Fix beschränkt auf `placeInKlemmRow()`+
  `redistributeKlemmBands()` (Geräte tragen jetzt zusätzlich `b_mm`),
  `placeInBands()` bewusst unverändert TE-basiert.
- **Eingabeleiste kompakter** (CSS, `.eingabeleiste`-Höhe −45px zugunsten
  der Schranksicht) – Hinweistext inline, Variablennamen unter Grund-/
  Reserve-Feldern per CSS ausgeblendet, CPU-Typ-Feld `position:absolute`.
- **WSL-localhost-Relay-Ausfall** (Infrastruktur, kein Projekt-Bug): Browser-
  Preview erreicht `localhost:8099` nicht, obwohl der Server nachweislich
  läuft (WSL-VM-IP direkt erreichbar) → WSL2-„localhost-Relay" hängt,
  betrifft jeden Port. **Fix: `wsl --shutdown`** (vorher beim Nutzer
  nachfragen, beendet alle WSL-Prozesse).

### Modul 5 – Feldgeräte-Stückliste angelegt, Baugruppen-Modularisierung diskutiert (Session 51 Nachtrag 7, gesperrt)
Strategiediskussion vor dem Anlegen weiterer Baugruppen: mit wachsender
Katalogzahl wird die Auswahl unübersichtlich (Beispiel Umwälzpumpe: 8+
genannte Varianten sind eigentlich ~5 orthogonale Achsen – Ansteuerung
Direkt/Sanftanlauf/FU, Handschalter-Bedienebene an der Tür vs. LVB im
Schrank selbst zugangsbeschränkt, DDC-Schaltbefehl, Rückmeldequelle
Hilfskontakte vs. Pumpenelektronik/Bus, physikalisch als Standard/
kommunikativ als Kundenoption – kombinatorisch 70+ statt 8 Fälle). Als
Zielbild vorgeschlagen und vom Nutzer bestätigt („können wir probieren"):
Baugruppen in `grundschaltung`/`zusatzbaustein`/`standalone` kategorisieren
(neue Felder `baustein_typ`/`baustein_kategorie`, NOCH NICHT angelegt) statt
flacher Varianten-Benennung – der bestehende Platzierungs-/Stückliste-/
DDC-Mechanismus unterstützt das schon heute ohne Codeänderung, da rein
mengenbasiert aggregiert wird (keine Instanz-Verknüpfung zwischen
Grundschaltung und Zusatzbaustein nötig). **Vorerst zurückgestellt** –
Nutzer-Entscheidung: erst einfache, nicht modularisierte Baugruppen anlegen
(Sensoren/Feldgeräte), die Modularisierung später bei Bedarf einführen.

**Stattdessen umgesetzt: Feldgeräte-Katalog + Modul 5.** Zweite,
eigenständige Stückliste für externe Betriebsmittel (Pumpen, Feldsensoren/
-aktoren) außerhalb des Schaltschranks, getrennt von der bestehenden
Schaltschrank-Stückliste. Neues Excel-Sheet `feldgeraete` (analog
`einzelbauteile`, aber ohne `b_mm`/`h_mm`/`te_breite`/`zone` – wird nicht in
der Schaltschrank-SVG platziert): `aktiv, artikel_nr, bezeichnung,
hersteller, kategorie, preis_stueck_eur, quelle_hinweis, geprueft`. Neues
Feld `baugruppen.feldgeraet_artikel_nr` (optionale FK) ergänzt das
bestehende Freitextfeld `betriebsmittel` (Session 49) – `betriebsmittel`
bleibt die Kurzbezeichnung, `feldgeraet_artikel_nr` verknüpft zusätzlich mit
einem echten bepreisten Katalogeintrag, sobald einer existiert; ohne
Verknüpfung zeigt Modul 5 nur eine unbepreiste Mengenzeile.
**Planungsfabrikat Pumpen: Wilo** (Nutzer-Vorgabe). Bei größerer
Herstellerauswahl in anderen Kategorien: nachfragen statt selbst
entscheiden, gemeinsam festlegen.

**Datenblätter bewusst NICHT lokal gespeichert:** Repository ist öffentlich
(GitHub Pages) – Herstellerdatenblätter als PDF ablegen würde geschütztes
Material weiterverbreiten. Stattdessen wie bisher: extrahierte Fakten +
Quelle-URL + Rechercheddatum in `quelle_hinweis`, bei Feldgeräten bewusst
ausführlicher als bisher üblich (welche Signale potentialfrei vs. Bus,
ob ein optionales Modul nötig ist), da diese Entscheidung direkt in die
Schaltschrank-Planung durchschlägt.

**Modul 5** (`modules/modul-05-feldgeraete/index.html`, rein lesend, Struktur
identisch zu Modul 7): liest `localStorage['m04_belegung']` (kein direkter
Modulaufruf, gleicher Kontrakt wie Modul 3↔1/2) + `baugruppen.json` +
`feldgeraete.json` unabhängig neu ein, aggregiert nach
`feldgeraet_artikel_nr` (bepreist) bzw. `betriebsmittel`-Freitext
(unbepreist, wie bei `aggregateStueckliste()` zeigt „–" statt 0,00€ und
fließt nicht in die Summe ein). Grund für ein eigenes Modul statt eines
Panels in Modul 4: dort ist der Platz schon knapp (siehe Eingabeleiste-
Kompaktierung weiter oben) – Modul 5 bekommt mehr Raum, analog zum
Modul-7-Präzedenzfall. **Modul 4 bekam nur zwei kleine Ergänzungen:** Zeile
„Feldgeräte gesamt" (`sumFeldgeraete()`) neben Physikalisch/Kommunikativ
gesamt, Button „→ Modul 5 · Feldgeräte" neben „← Zurück zu Modul 3". Modul
05 auf der Startseite von Platzhalter („Datenpunkt-Management") auf aktiv
umgestellt, `hero-stats` „5"→„6".

Verifiziert direkt im Browser: `feldgeraete.json` korrekt leer exportiert
(`[]`, Sheet angelegt aber noch keine Einträge); synthetischer Testfall
(1 Baugruppe mit `feldgeraet_artikel_nr`-Verknüpfung, 1 nur mit
`betriebsmittel`-Freitext) zeigt in Modul 5 korrekt eine bepreiste und eine
unbepreiste Zeile, Summe berücksichtigt nur die bepreiste; „Feldgeräte
gesamt"-Zeile in Modul 4 zeigt korrekte Mengensumme, keine Überlappung mit
der DDC-Statistik-Zeile (Zeilenhöhe/Schriftgröße von `#ddc_summary_totals`
dafür leicht reduziert). Keine Konsolenfehler in Modul 4, 5 oder auf der
Startseite. Backup vor der Excel-Strukturänderung:
`C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-feldgeraete-schema_*.xlsx`.

### Erste Feldgeräte-Baugruppen: 4 Raumsensoren, Siemens Symaro (Session 51 Nachtrag 8, gesperrt)
Erste Nutzung des neuen Feldgeräte-Katalogs (siehe vorheriger Abschnitt).
**Planungsfabrikat Sensoren/Feldgeräte: Siemens** (Nutzer-Vorgabe). Workflow
bestätigt sich als praktikabel: Claude recherchiert (Originaldatenblätter,
bei binär-komprimierten Siemens-PDFs per `pypdf` in WSL ausgelesen – siehe
Session 41-Präzedenzfall, funktioniert weiterhin zuverlässig), präsentiert
Fund + Link, Nutzer entscheidet vor dem Eintragen.

**4 Baugruppen angelegt** (`430_000001`–`430_000004` – ursprünglich unter
`480_00000{8-11}`/Gewerk Automation angelegt, per Nutzer-Korrektur direkt
im Anschluss auf Gewerk 430/Lüftung umbenannt, siehe „Baugruppen mehreren
Gewerken zuordenbar" weiter unten; Zone `klemm_s`, `funktionsbereich:
['heizung','lueftung','kaelte']`, je 1× `dp_ai` auf der Signalklemme):
- `430_000001` „Raumtemperatursensor passiv" – Siemens `QAA24` (LG-Ni1000),
  2 Klemmen (B/M, passiv, keine Versorgung).
- `430_000002` „Raum-CO2-Sensor" – Siemens `QPA2000` (NDIR, 0…2000ppm),
  3 Klemmen (G/G0 Versorgung + X1 Signal).
- `430_000003` „Raum-VOC-Sensor" – Siemens `QPA1000` (Metalloxid-Halbleiter),
  3 Klemmen, gleiche Baureihe/Datenblatt wie QPA2000.
- `430_000004` „Raumfeuchtesensor" – Siemens `QFA2000` (kapazitiv), 3 Klemmen.
  Klemmenbezeichnung nicht aus dem QFA2000-eigenen Datenblatt bestätigt
  (Abruf scheiterte am Timeout), sondern aus dem 20 Jahre durchgängig
  gleichen Siemens-Klemmenschema (G/G0+Signal) der QFA/QPA-Familie
  abgeleitet – vor Verdrahtung idealerweise gegenprüfen.

Alle 4 Klemmen sind `3209510` (PT 2,5 grau, Standardklemme) – auch bei den
aktiven Sensoren, da 24V-SELV-Versorgungsleitungen (anders als
230V-Leistungsanschlüsse) keine Farbcodierung nach der Session-51-Regel
„Farben sind für Leistungsanschlüsse ab 230V AC" brauchen.

**Bewusst NICHT angelegt (Nutzer-Entscheidung nach Rückfrage):**
- Raumtemperatursensor aktiv – einziger Siemens-Kandidat (`QAA2071`,
  4-20mA) ist laut HIT-Portal „In phase-out", kein Nachfolger für „nur
  Temperatur, aktiv" als Einzelprodukt in der aktuellen Symaro-Reihe
  gefunden (nur noch innerhalb der QFA/QPA-Kombisensoren abgedeckt).
- Raumtemperatur- und Feuchtesensor (Temperatur passiv, Feuchte aktiv) –
  kein einzelnes Siemens-Katalogprodukt mit dieser gemischten Kombination
  gefunden (QFA-Kombisensoren bieten Temperatur immer nur aktiv).
- Raumtemperatur- und Feuchtesensor aktiv (`QFA3160`) – Nutzer-Einschätzung:
  Gehäuse/Optik nur für industrielle Umgebungen geeignet, nicht für
  Bereiche mit architektonischen Anforderungen.

Verifiziert direkt im Browser (Standschrank, echte Katalogdaten):
Testbelegung (2× Raumtemperatursensor + je 1× CO2/VOC/Feuchte) liefert
`dp_ai used:5` (korrekt, 1 pro Instanz), `bgInstanceQueue` mit korrekter
Klemmenzahl je Instanz (2/2/3/3/3), Stückliste aggregiert korrekt
`3209510` Menge 13 in `klemm_s`; Modul 5 zeigt alle 4 Feldgeräte mit
korrektem Hersteller/Preis/Menge/Summe (1207,66 €). Keine Konsolenfehler.
Backup: `C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-raumsensoren_*.xlsx`.
**Korrektur (Session 51 Nachtrag 9, direkt im Anschluss):** siehe nächster
Abschnitt – die IDs `480_000008`–`011` wurden zu `430_000001`–`004`
umbenannt.

### Baugruppen mehreren Gewerken zuordenbar: funktionsbereich als Array (Session 51 Nachtrag 9, gesperrt)
Nutzer-Fund: die 4 neuen Raumsensor-Baugruppen waren unter „Automation"
einsortiert – falsch, „es handelt sich nicht um Automationsgeräte". Sie
müssen stattdessen in Heizung, Lüftung UND Kälte gleichzeitig auswählbar
sein (ein Raumsensor wird je nach Projekt für unterschiedliche
Anlagentypen eingesetzt).

**Datenmodell:** `baugruppen.funktionsbereich` ist jetzt immer ein Array
(Komma-Liste in Excel), auch bei nur einem Wert – exakt analog zu
`einzelbauteile.zone` (Session 44). `filterBaugruppen()` in Modul 4 prüft
entsprechend `b.funktionsbereich.includes(gew)` statt `===`.
`baugruppen.gewerk` (DIN-276-Code) bleibt bewusst EINWERTIG – wird in
Modul 7 exakt gefiltert/anzeigt, ein Komma-Wert würde dort die
Filterlogik brechen. Bei mehreren gleichzeitig zutreffenden Gewerken
führt der Nutzer eines als „führend" (hier auf Nachfrage: **430 ·
Lüftung**).

**ID-Konsequenz:** die ID kodiert laut Schema (Session 37/38) den
führenden DIN-276-Code – mit `gewerk` 480→430 mussten auch die IDs
umbenannt werden, sonst widerspricht die ID dem eigenen Schema. Kein
Konflikt mit alten `430_xxxxxx`-Einträgen (Baugruppen wurden in Session 40
komplett neu aufgebaut, keine Altlasten): `480_000008`–`011` →
**`430_000001`–`004`**, `baugruppen_bauteile.bg_id` (11 Zeilen) nachgezogen.

Verifiziert direkt im Browser: Tabs Heizung/Lüftung/Kälte zeigen jeweils
alle 4 Sensor-Baugruppen korrekt; Tab Automation zeigt sie korrekt NICHT
mehr (nur noch die 7 DDC-Reserve-Baugruppen); Modul 7 rendert
`funktionsbereich` als lesbaren Komma-Text ohne Fehler (kein eigener
Formatter nötig, `String()`-Fallback reicht, wie bereits beim analogen
`zone`-Array). Regressionstest mit umbenannter ID (`430_000002`, 2×
Instanzen) bestätigt Platzierung/Stückliste/Feldgeräte-Summe weiterhin
korrekt. Keine Konsolenfehler.

### Raumsensoren-Nachtrag: CO2/VOC nur Lüftung, Kombifühler T+rH ergänzt (Session 51 Nachtrag 10, gesperrt)
Zwei Nutzer-Korrekturen direkt im Anschluss: **CO2- und VOC-Sensor
(`430_000002`/`003`) gehören weder zu Kälte noch zu Heizung** – anders als
Temperatur/Feuchte sind Luftqualitätssensoren nur in RLT-Anlagen sinnvoll.
`funktionsbereich` beider Baugruppen auf `['lueftung']` (einwertig)
korrigiert. Raumtemperatursensor passiv (`430_000001`) und
Raumfeuchtesensor (`430_000004`) bleiben unverändert bei
Heizung/Lüftung/Kälte.

**Neue Baugruppe `430_000005` „Raumtemperatur- und Feuchtesensor"**
(Lüftung/Heizung/Kälte) – Siemens `QFA2060` (Symaro, Standardgenauigkeit).
Bewusst NICHT `QFA3160` (bereits verworfen, Messstab-Bauform/industrielle
Optik) – `QFA2060` hat stattdessen dasselbe flache Wandaufbaugehäuse wie
`QAA24`/`QPA2000` (90×100×36mm, IP30), architektonisch unauffällig. 4
Klemmen (G/G0 Versorgung, U1 Feuchte-Signal, U2 Temperatur-Signal – aus
dem Schwestermodell `QFA3160` abgeleitet, gleiches Familienschema),
Datenpunktbedarf 2× AI (je Instanz). Kein Preis eingetragen – nur
Gebrauchtmarkt-/US-Distributor-Preise gefunden, nach Session-45-Konvention
nicht übernommen.

Verifiziert direkt im Browser: Heizung/Kälte zeigen nach der Korrektur
korrekt nur noch 3 Sensoren (T-passiv, Feuchte, Kombi), Lüftung zeigt alle
5; Testbelegung (2× Kombifühler) liefert `dp_ai used:4` (2 pro Instanz),
8 Klemmen in der Stückliste, Modul 5 zeigt den Kombifühler korrekt
unbepreist („–", nicht in der Summe). Keine Konsolenfehler.

### Tauchtemperaturfühler 100/150mm für Heizung/Kälte (Session 51 Nachtrag 11, gesperrt)
Nutzer-Wunsch: passive Tauchtemperaturfühler bis 200mm Baulänge mit
passender Tauchhülse, vorgeschlagen 3 Größen (~65/~135/~200-250mm).
**Recherche-Ergebnis (Siemens-Originaldatenblatt CE1N1781en, 2017-07-19,
Symaro `QAE21..`): die Baureihe bietet ausschließlich 100mm und 150mm als
Baulänge – weder 65mm noch 200-250mm existieren als Katalogvariante.**
Dem Nutzer mit Tabelle vorgelegt, auf Rückmeldung beide reale Größen
übernommen (keine 3. Größe).

**2 neue Baugruppen** `430_000006`/`430_000007` „Tauchtemperatursensor
100mm"/„150mm" (Heizung/Kälte, NICHT Lüftung – reine Medientemperatur in
Rohren/Behältern). Siemens **`QAE2120.010`**/**`QAE2120.015`** – bewusst
die LG-Ni1000-Elementvariante (konsistent zu `QAA24`) UND die einzige
Ausführung dieser Baureihe, bei der die Tauchhülse (Schutztasche mit
Gewindenippel G½A) bereits im Lieferumfang enthalten ist (alle anderen
Elementtypen Pt100/Pt1000/NTC verlangen die Tauchhülse als separates
Zubehör). 2 Klemmen (B/M, passiv, polaritätsunabhängig vertauschbar),
1× `dp_ai`. Preise 85,08€/89,63€ (Siemens HIT-Portal-Preis).

Verifiziert direkt im Browser: Heizung UND Kälte zeigen beide Größen
korrekt, Lüftung korrekt nicht; Testbelegung (je 1×) liefert `dp_ai
used:2`, 4 Klemmen, Modul 5 zeigt beide korrekt bepreist (Summe 174,71€).
Keine Konsolenfehler. Backup:
`C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-tauchfuehler_*.xlsx`.
Damit sind die Raumsensoren fürs Erste abgeschlossen.

### Modul 4/5 – Lüftungssensoren, Steuerspannungs-Automatik, Sicherheitsketten (Session 52, komprimiert)
Vollständiger Sitzungsverlauf (Nutzer-Funde, Root-Cause-Analysen,
verworfene Zwischenstände, Verifizierungsdetails) archiviert in
`docs/archiv/claude-md-modul4-session-52.md`. Die daraus destillierten,
dauerhaft gültigen Modellierungsregeln stehen kompakt unter
„Baugruppen-Modellierungsregeln (verbindlich)" weiter oben – hier nur noch
das inhaltliche Ergebnis:

- **9 neue Lüftungssensor-Baugruppen** `430_000008`–`430_000016`
  (Siemens-Leitfabrikat, Rauchmelder Oppermann): Kanaltemperaturfühler
  0,4m/2,0m, Kanalfeuchtefühler, 2× Differenzdruckwächter (Filter-/
  Ventilatorüberwachung), Drucksensor Kanaldruck, Kanalhygrostat, 2×
  Kanalrauchmelder (24V/230V, DIBt-Zulassung zur direkten
  Klappenansteuerung).
- **Pflichtzubehör-Mechanismus für Feldgeräte** (`feldgeraete.zubehoer_feldgeraet_artikel_nr`/
  `zubehoer_menge`): ein Feldgerät kann automatisch ein zweites,
  nicht selbst wählbares Feldgeräte-Entry mitziehen (z. B. Montagekonsole
  zum Kanalrauchmelder) – erscheint in Modul 5, zählt nicht in Modul 4s
  „Feldgeräte gesamt". Vom Nutzer als wiederkehrendes Pattern angekündigt.
- **Sicherheitsketten-Koppelrelais-Pattern** eingeführt (1-Wechsler-Feldgeräte
  ohne getrennte Kontakte für Leistungssteuerung + DDC-Meldung): neues
  Bauteil `2967099` (230VAC-Spule), siehe Regel 6.
- **Steuerspannungs-Auto-Ergänzung** (analog zur DDC-Auto-Modul-Ergänzung,
  aber präsenzbasiert): `benoetigt_steuerspannung` auf Einzelbauteil- UND
  Baugruppen-Ebene, `steuerspannungWatermark`-Ratchet, 3 neue Baugruppen
  `480_000008`–`010` „Steuerspannung 24V AC/24V DC/230V AC". Netztyp-Automatik
  (`drehstrom_variante_artikel_nr`/`resolveNetztypArtikel()`) wählt die
  230V- oder 400V-Primärvariante anhand von `m03_zone_netztyp` ohne
  manuellen Zusatzschritt in Modul 4.
- **Desigo-PX-CPUs auf 24V AC umgestellt** (Siemens-Vorgabe: nur bei
  AC-Speisung liefert die Station 24V AC an die TX-I/O-Klemme V~ und das
  Triac-Modul TXM1.8T funktioniert nur AC-versorgt) und teilen sich seither
  **denselben Sicherheitstrafo wie die 24V-AC-Feldgeräte im selben Schrank**
  (Siemens-Vorschrift) – Trafo sitzt im Leistungsfeld, nicht mehr direkt vor
  der CPU im Steuerungsfeld (bewusster Bruch der Session-50-Regel „Netzteil
  immer direkt vor CPU", nur für das Netzteil – die CPU→TXM-Modul-Reihenfolge
  bleibt unverändert). Bewusst keine VA-Kapazitätsbilanzierung.
- **Klemmzonen-Grundsatzregel Sensor vs. Feldgerät** verbindlich festgelegt
  (siehe Regel 1) und rückwirkend auf 5 Baugruppen angewendet.
- **Diverse Korrekturen:** Sicherungen der Steuerspannungs-Baugruppen von
  `leist` nach `evert`; Sekundärsicherung CPU-Trafo B16A→B10A (Siemens-Vorgabe
  max. 10A für die 24V-AC-Leitung); Koppelrelais-Baugruppen von 7 auf 3
  Bauteile reduziert (keine separaten Landeklemmen für relaiseigene
  Kontakte); Kanalrauchmelder komplett auf `klemm_f` inkl. 230V-Versorgung
  umgestellt; zwei Nachzügler-Bugs behoben (doppeltes Netzteil in
  „Automationsstation (AE)", kaputte `artikel_nr`-Referenz `QUINT-PS/…`
  statt `2866690` bei „Steuerspannung 24V DC" – siehe Regel 7).

Alles direkt im Browser verifiziert (frische Tabs, vollständig geleertes
`localStorage` zur Vermeidung von Watermark-Cross-Contamination). Backups:
`C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-lueftungssensoren_*.xlsx`.

## Gesperrte Entscheidungen

Diese Punkte wurden bereits ausführlich diskutiert und entschieden – nicht neu aufgreifen. **Archiv-Hinweis (15.08.2026):** ausführliche Session-Protokolle werden zu kompakten Ergebnis-Zusammenfassungen eingedampft (Volltext inkl. Nutzer-Funden/verworfenen Zwischenständen/Verifizierungsdetails liegt in `docs/archiv/claude-md-modul4-sessions-20-29.md`, `docs/archiv/claude-md-modul4-sessions-30-34.md`, `docs/archiv/claude-md-modul4-sessions-35-51.md` und `docs/archiv/claude-md-modul4-session-52.md`) – Grund: `CLAUDE.md` wird bei jeder Sitzung vollständig geladen, unabhängig vom Umfang der Aufgabe. Bei künftigen sehr langen Session-Nachträgen ebenso verfahren: verbindliche Regel kompakt in `CLAUDE.md`, ausführliche Vorgeschichte ins Archiv. Die aus Session 51/52 destillierten Baugruppen-Modellierungsregeln stehen dauerhaft unter „## Baugruppen-Modellierungsregeln (verbindlich)" weiter oben.

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

### Modul 4 – Platzierungs-Engine: Entstehungsgeschichte (Sessions 20–29, komprimiert)
Vollständiger Sitzungsverlauf (Nutzer-Funde, verworfene Zwischenlösungen, Verifizierungsdetails) archiviert in `docs/archiv/claude-md-modul4-sessions-20-29.md`. Aktuell gültiger Funktionsstand:

- **8 Platzierungszonen:** `klemm_e` (Einspeiseklemmen), `uss` (ÜSS+Vorsicherung), `evert` (Energieverteilung), `leist`/`leist_ext` (Leistungsbaugruppe), `steuer` (Steuerbaugruppe), `klemm_l`/`klemm_f`/`klemm_s` (Abgänge Leistung/Feldgeräte/Sensoren). Zone kommt aus `eb.zone` (Katalog-Default), optional pro Baugruppen-Bauteil per `bt.zone` überschrieben.
- **Zwei Platzierungsmodelle, nicht austauschbar:** `placeInBands()` (Kanal(40mm)+Klemmraum-Modell für Mehrreihen-Zonen: `leist`, `steuer`, sowie `evert` nur mit Schienensystem) und `placeInKlemmRow()` (1-Reihen-Modell, Breite statt Höhe als Kapazität: `klemm_e`, `uss`, `klemm_l`, `klemm_f`, `klemm_s`, `evert` ohne Schienensystem). Grund: Modul 3 hat diese Zonen bereits exakt bemessen, ein zusätzliches Kanal/Klemmraum-Layer würde sie sprengen. `placeInKlemmRow()` prüft Höhe UND Breite – zu hohe Bauteile werden übersprungen statt verzerrt platziert.
- **Zwei Belegungs-Eintragstypen:** `{typ:'baugruppe',bg_id,menge,ci}` und `{typ:'einzel',artikel_nr,menge,ci}`. Indizierung pro Zone (`idx`), sichtbar im SVG-Tooltip und in der Stückliste (`formatIdxList()`, komprimiert zu Bereichen wie `#3–#5, #7`). Stückliste aggregiert nach `(artikel_nr, Zone)`.
- **`ZONE_COLORS`** (zentrale Konstante, identisch in Modul 3+4 – einzige Quelle für Zonenfarben):
  ```
  klemm_e:'#EBDBA0'  uss:'#D8A916'   evert:'#C8720E'  leist:'#C84E2E'  steuer:'#4BBECA'
  klemm_l:'#2DBD8E'  klemm_f:'#9A94E8'  klemm_s:'#C14FA0'
  ```
- **Zonen-Legende** (`buildLegend()`, unter der Schranksicht) + sichtbare Bauteil-Nummer (`#idx`) auf jedem Block. Zonentext im SVG auf dem Bildschirm ausgeblendet (Legende erklärt Farbe→Zone bereits), im Druck weiterhin sichtbar (`@media print`).
- **Verdrahtungskanal-Muster (`kanalPending`):** kein Kanal vor der ersten Reihe einer Zone (nutzt den bereits vorhandenen festen M3-Kanal), genau ein Kanal zwischen allen Folgereihen (auch bandübergreifend), ein abschließender Kanal nach der letzten Reihe nur wenn der Rest der Zone noch Kanal+eine weitere Reihe fassen würde.
- **`redistributeKlemmBands(bandsAll, queues, reservePct)`:** `klemm_l`/`klemm_f`/`klemm_s` teilen sich eine gemeinsame, konstante Gesamtbreite (Summe der M3-Originalbänder). Jede Zone bekommt mindestens `Bedarf/(1-reservePct)`; reicht die Gesamtbreite, wird der Rest proportional zum M3-Originalverhältnis verteilt. `reserve_pct`-Eingabefeld (Default 20%, gilt schrankweit außer `klemm_e`); weiche Warnung (`#reserve-warn`) wenn die Reserve trotz Umverteilung nicht erreichbar ist – getrennt vom harten Overflow-„!".
- **Erzwungener Zeilenumbruch („neue Reihe"):** nur wirksam für Zonen aus `REIHEN_ZONEN` (`leist`/`steuer` – Reihen-Konzept), Checkbox bei allen anderen Zonen deaktiviert/wirkungslos.
- **Funktionsbereich-Taxonomie** (Session 24, seither durch die DIN-276-Migration Session 37/38 abgelöst – siehe dort für den aktuellen Stand).
- **Excel-Pipeline seit Session 27** auch für `einzelbauteile`/`baugruppen` (vorher Sonderfall, direkt als JSON angelegt). **Planungsfabrikat Klemmen: Phoenix Contact** – UT-Reihe (Schraubanschluss) für Einspeisung, PT-Reihe (Push-in) für alle drei Abgangs-Klemmenzonen, Zonen-Zuordnung über den bestehenden Baugruppen-Override-Mechanismus.

### Modul 4 – Baugruppen-Neuaufbau, Feldtyp-System, DDC-Automation (Sessions 37–50, komprimiert)
Vollständiger Sitzungsverlauf archiviert in
`docs/archiv/claude-md-modul4-sessions-35-51.md`. Aktuell gültiger
Funktionsstand:

- **Session 37/38 – Baugruppen-ID-Schema auf DIN-276 umgestellt:**
  `id`-Schema `<3-stelliger DIN-276-Gewerke-Code>_<6-stellig je Gruppe>`
  (z. B. `480_000001`), `gewerk` trägt jetzt den numerischen Code statt
  Kurzname. Modul 4 auf 11 DIN-276-Tabs umgestellt (`filterBaugruppen()`
  matcht auf `b.funktionsbereich`, NICHT `b.gewerk`); alter `schaltschrank`-
  Tab entfällt, geht in `automation` (480) auf; `450`/„netzwerk" deckt auch
  Sicherheitstechnik (Brandmelde-/Gefahrenmeldeanlagen) mit ab.
- **Session 39 – Excel-Konsistenzpflege:** 4 Datenbanken (`standschraenke`,
  `sockel`, `bodenbleche`, `reiheneinbaugeraete`) waren von der
  Excel-Pipeline abgekoppelt (Sheets fehlten in `ga_komponenten.xlsx`,
  nur noch aus JSON pflegbar) – aus JSON wiederhergestellt. Feldnamen auf
  Excel-Seite vereinheitlicht (`bestellnummer`→`artikel_nr`,
  `preis_stueckpreis_eur`→`preis_stueck_eur`; JSON-Ausgabeschlüssel bewusst
  unverändert, nur `xlsx_to_json.py`s Leseseite angepasst).
- **Session 40 – Katalogbereinigung:** `bauteil_typ` ist Pflichtfeld
  (steuert Kurzlabel + DDC-Kapazität/Bedarf-Unterscheidung). `kategorie` ≠
  `zone` – `kategorie` ist eine rein optische Dropdown-Gruppierung;
  Bauteile OHNE `kategorie` fehlen komplett im Modul-4-Dropdown (nicht nur
  ungruppiert!). `reiheneinbaugeraete`-Sheet (nie von einem Modul geladen,
  unsichere/falsche Session-20-Altdaten) komplett gelöscht. **Baugruppen
  komplett gelöscht** – bewusster Neuaufbau von Grund auf, nachdem der
  Einzelbauteile-Katalog sauber ist.
- **Session 41 – Siemens Desigo PX Architektur verstanden:** Ebene 1 = CPU
  (`PXC`-Serie, KEINE eigenen Anschlussklemmen), Ebene 2 = TX-I/O-Module
  (`TXM1.x`, einheitliches 64×77,5mm-Gehäuse). `PXA30-x` war fälschlich als
  I/O-Quelle katalogisiert (tatsächlich Kommunikations-/HMI-Zusatzkarte) –
  gelöscht. LVB = „Lokale Vorrangbedienebene" (Wippenschalter Hand/Auto je
  Kanal, `-M`/`-ML`-Suffix). Neue Felder `feldbus_protokoll`,
  `lvb_integriert`; `bauteil_typ:'ddc_cpu'` getrennt von `ddc_io` eingeführt.
  **DDC-Aufschaltung physikalisch/kommunikativ je Bauteil:** getrennte
  Checkbox+Protokoll-Auswahl, `PHYS_DP_TYPES`/`FB_DP_TYPES` als getrennte
  Pools, `isDdcSupplyTyp()`-Helper. Schütz-Zubehör: Hilfsschalterblock als
  automatische Grundausstattung jedes Schützes (`zubehoer_artikel_nr` +
  `syncZubehoer()`); neues Feld `keine_platzierung_mp` (Bauteil ohne eigenen
  Montageplatten-Platzbedarf, z. B. aufgesteckt – bleibt in der Stückliste,
  aber nicht in der Zeichnung). 13 Schütze 24V/230V AC über den gesamten
  Leistungsbereich ergänzt. LVB-Relais: **Metz Connect** als bewusste
  Ausnahme vom Phoenix-Contact-Planungsfabrikat (Phoenix deckt keine echte
  LVB-Funktion ab, nur einfache Koppelrelais). Mehrere Layout-Iterationen
  der Eingabeleiste (3-Blöcke-Layout, Statistik spaltengenau via CSS-Grid
  `display:contents`, Datenpunkttyp-Farbschema `--dp-ai/-ao/-bi/-bo`).
- **Session 42/43 – Zonen-/Kategorie-Korrekturen, Türbauteile:** neue Zone
  `tuer` („Fronttafel/Tür" – KEIN Eintrag in `ALLE_ZONEN`/`ZONE_COLORS`, hat
  keine physische Platzierung/Kapazität, eigener Filter-Chip). Neue
  Kategorie „Fronttafel-/Türeinbau", nutzt das bestehende
  `keine_platzierung_mp`-Feld.
- **Session 44 – Mehrfachzonen für Bauteile:** `einzelbauteile.zone` ist
  jetzt immer ein Array (erster Eintrag = Default), `bt.zone`
  (Baugruppen-Override) bleibt einzelner String. **Bug gefunden+gefixt:**
  Zone galt zunächst item-weit statt pro Hinzufüge-Batch – `zone` wurde Teil
  jedes `batches`-Eintrags (analog `forced`).
- **Session 45/46 – Katalogerweiterung:** 14+7 neue Einträge für HLS/
  Elektro/Sanitär/Sicherheitstechnik (Frequenzumrichter, Zeitrelais,
  Steckdose, Wahlschalter/Not-Halt, FI-Schutzschalter, Netzwerk-Switch,
  Wischrelais, Störquittiertaster, M-Bus-Pegelwandler, Messgeräte/
  Energiezähler). Session-43-Entscheidung „Signalleuchten→leist" in
  Session 46 wieder auf `tuer` zurückgedreht.
- **Session 47 – Türansicht neben Innenansicht:** Türmaße = echte
  Gehäuse-Außenmaße (`m01_B/H`/`m02_B/H`, NICHT der kleinere
  Montagebereich). 5 ergonomische Höhen-Bänder (`TUER_BAND_*`, gestützt
  durch DIN EN 60204-1/DIN 18040), `tuerBand(eb)`/`buildTuerAnsicht()`.
- **Session 48 (größtes Einzelthema) – Mehrfeld-Schaltschränke:** 5
  Feldtypen A–E (`FELDTYP_ZONEN`), `FELDPLAN` je `zone_modus` (1feld/
  je_feld/getrennt_els/einsp_misch), `buildLayoutForFeldtyp()` als
  generische Zeilen-Transformation. **Wandschrank-Sperre:**
  `schrank_typ==='wandschrank'` erzwingt IMMER effektiv `zone_modus='1feld'`
  (`getEffektiveZoneModus()`, identisch in Modul 3 UND 4). `placeInBands()`/
  `placeInKlemmRow()` bekamen `startIdx`+`leftoverDevs`+`nextIdx` für die
  Feld-zu-Feld-Kaskade, `calculateFelder()`-Orchestrator (demand-getriebene
  Folgefelder, `MAX_FELDER=20`-Deckel gegen Endlosschleifen). Türbauteile
  bekamen expliziten Feld-Bezug. `klemm_l` gehört NICHT ins reine
  Einspeisefeld (Typ C, nur wenn im selben Feld auch `leist` existiert).
  Feld-zu-Feld-Maßstab-Bug in Modul 4 gefixt (erstes Feld wurde mit
  falscher Breite gemessen, da das Wrap-Layout beim Messen noch
  unvollständig war – Fix: erst ALLE Wrap-Container anlegen, DANN messen).
- **Session 49 – Baugruppen-Zusammenhalt über Zonen hinweg:**
  `bgInstanceQueue` (Reservierung-vor-Commit-Modell),
  `platziereBaugruppenFuerFeld()` – Zusammenhalt gilt pro
  (Instanz × Feldtyp), NICHT für die ganze Instanz (sonst könnten
  baugruppenübergreifende Feldtyp-Kombinationen wie Leistungsfeld +
  Steuerungsfeld nie gemeinsam platziert werden). Erste
  Automations-Baugruppen (`480_000001` ff., „Reserve"-Datenpunkte für DDC-
  Anschlüsse ohne bekanntes Feldgerät): DDC-Datenpunktbedarf über
  `baugruppen_bauteile.dp_ai/ao/bi/bo`-Override statt am Katalogartikel
  selbst (eine Klemme trägt sonst nie DDC-Bezug). Automatische
  CPU-Ergänzung, sobald ein E/A-Modul gesetzt, aber keine CPU vorhanden ist.
  BI/BO-Zonenkorrektur (beide → `klemm_f`; `klemm_s` nur für analoge
  Sensoren). TXM1.8U-Kapazitätslücke geschlossen (`dp_ai=8`/`dp_ao=8`),
  dabei Unter-Versorgungs-Bug in `computeDdcAutoModules()` gefixt
  (Cross-Typ-Abzug nur noch für den GERADE bearbeiteten Typ, sonst hätte
  ein Mehrzweckmodul bei gleichzeitigem AI+AO-Bedarf zu wenige Käufe
  vorschlagen können). Jede Reserve-Baugruppe trägt 2 Klemmen (Signal +
  Referenz), nicht nur 1.
- **Session 50 – CPU-Katalog korrigiert + Automationsgruppen-Logik:**
  `PXC4.E16` (fälschlich mit Onboard-E/A katalogisiert) → `PXC7.E400.A`
  (echte modulare Variante, 0 Onboard-E/A) korrigiert – widersprach sonst
  dem Prinzip „Verbrauch entsteht ausschließlich an TXM-Modulen". Alle 3
  Desigo-PX-CPU-Typen aufgenommen (`PXC7.E400.A` modular + `PXC4.E16.A`/
  `PXC5.E24.A` kompakt), `auto_ea_cpu`-Flag steuert, welche CPU die
  Auto-Ergänzung nutzt. **Automationsstations-Gruppen:** Netzteil→CPU→
  E/A-Module lückenlos auf einer Hutschienenreihe, `max_ea_module`-
  Obergrenze je CPU löst eine komplett neue Gruppe aus (eigenes Netzteil +
  eigene Sicherung, `groupStart`-Flag erzwingt frische Reihe). Manueller
  „↺ Zurücksetzen"-Button für die DDC-Watermark (Ratchet-Mechanismus,
  Session 28e: einmal ergänzte Auto-Module sinken nie von selbst).

### Modul 7 – Stammdatenpflege (Sessions 35/36, komprimiert)
Vollständiger Sitzungsverlauf archiviert in
`docs/archiv/claude-md-modul4-sessions-35-51.md`.

- Neues Modul `modules/modul-07-stammdatenpflege/index.html` – bewusst
  **rein lesend** (kein Editor, Excel bleibt einzige Schreibstelle).
  Katalog-Browser (Einzelbauteile/Baugruppen) + Datenqualitäts-Leiste
  (`computeDataQuality()`: ungeprüfte Einträge, fehlender Preis, verwaiste
  `artikel_nr`-Referenzen) + Verwendungsnachweis (`USAGE_MAP`,
  Artikel-Nr. → referenzierende Baugruppen).
- **„📋 Liste kopieren"-Button** (`copyList()`): kopiert die aktuell
  gefilterte Liste als Text in die Zwischenablage – Standard-Workflow für
  Katalogpflege seither: Nutzer filtert (z. B. „Fehlender Preis"), kopiert,
  fügt im Chat ein, Claude recherchiert und trägt Werte direkt in
  `ga_komponenten.xlsx` ein, `xlsx_to_json.py` neu ausführen.

### Modul 4 – Belegungshistorie, Zonenfilter, Zentrierung (Sessions 30–34, komprimiert)
Vollständiger Sitzungsverlauf archiviert in `docs/archiv/claude-md-modul4-sessions-30-34.md`. Aktuell gültiger Funktionsstand:

- **`batches`-Modell (final, Session 30):** jeder Belegungseintrag trägt `batches:[{n,forced},...]` (chronologischer Stapel, ältester zuerst). `addEinzelbauteil()` hängt an (`pushBatch()`, verschmilzt mit dem letzten Batch bei gleichem `forced`-Status), `removeEinzelbauteilQty()` reduziert echtes LIFO – immer zuerst der zuletzt hinzugefügte Batch, unabhängig davon ob normal oder erzwungen. `item.menge` wird stets als Summe aller `batch.n` neu berechnet (keine Drift möglich). Ersetzt die verworfenen Vorläufer-Modelle `rowBreak`-Boolean (Session 28g/28h) und `forcedMenge`-Zähler (Session 28i) – alte Einträge werden beim Zugriff transparent migriert (`getBatches()`).
- **`consolidateBelegung()`:** fasst beim Laden sowie am Ende von `addBaugruppe()`/`addEinzelbauteil()` alle Einträge mit gleichem Schlüssel zu genau einem zusammen (Selbstheilung fragmentierter Alt-Daten aus früheren Modellgenerationen).
- **Vertikale Zentrierung (Session 31):** Bauteile in Leistung/Steuerung/Energieverteilung-Reihen werden wie Klemmenzeilen auf die Reihenmitte zentriert (`by0` in `buildSVG()`) – rein optisch, kein Effekt auf Platzbedarf/Platzierungslogik.
- **Zonen-Filter Einzelbauteil-Dropdown (Session 33, final):** die 8 `.fs-mini`-Felder im Füllstand-Streifen sind selbst klickbar (`setEinzelZone()`), plus ein 9. „Alle"-Feld – ersetzt die in Session 32 zuerst gebauten separaten `.zone-tab`-Buttons vollständig.
- **Offene, zurückgestellte Positionierungs-Themen (Session 34, weiterhin unentschieden):**
  1. Gerichtete Mindestabstände zu Nachbarbauteilen nach Herstellerangabe (Wärmeabfuhr) – DBACS kennt aktuell nur `h_mm`/`b_mm`/`te_breite`, keine Abstandsregeln.
  2. Positionierungslogik für hintereinander zu platzierende Bauteile (z. B. DDC-Module) – Verhältnis zur bestehenden Reihen-Logik noch ungeklärt.
  3. Anordnung von Bauteilen innerhalb einer Baugruppe (z. B. Motorschutzschalter über Schütz) – das aktuelle Zwei-Cursor-Platzierungsmodell (Session 28g) stößt hier an seine Grenzen, eine gezielte Bauteil-Auswahl für Reihen-/Positionswechsel wäre nötig statt eines globalen Flags pro Artikel.
  4. Bedarfsbasierte Breiten-/Höhen-Umverteilung auch für `leist`/`steuer` (existiert bisher nur für die drei Klemmleisten-Zonen, `redistributeKlemmBands()`).

  Alle vier Punkte bleiben zurückgestellt bis nach dem Baugruppen-Neuaufbau.

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
- ~~`zone_anordnung` (Nebeneinander/Übereinander) wird disabled wenn `zone_modus === 'je_feld'`~~
  **aufgehoben Session 48 Nachtrag 3** – stammte aus der Zeit vor dem
  Feldtyp-System, als „Mehrere Felder" nur ein unfertiger Platzhalter war.
  `zone_anordnung` bleibt jetzt bei JEDEM `zone_modus` wählbar (Nutzer-Fund:
  „Der Fall Mehrere Felder Leistung und Steuerung nebeneinander fehlt").
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
