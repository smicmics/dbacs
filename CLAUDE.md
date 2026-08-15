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

## Offene Punkte (Stand Session 52 – vor Beginn der nächsten Sitzung lesen)

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

Sonst keine offenen Punkte – alle Session-51-Themen implementiert UND im Browser
verifiziert. Details siehe „Modul 4 – Session 51 (komprimiert)" unter
„Formel-Referenz" weiter unten bzw. `docs/archiv/claude-md-modul4-sessions-35-51.md`
für den vollen Sitzungsverlauf.

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

### Lüftungssensoren + Pflichtzubehör-Mechanismus + Sicherheitsketten-Koppelrelais (Session 52, gesperrt)
9 neue Baugruppen `430_000008`–`430_000016` (alle `funktionsbereich: ['lueftung']`),
Siemens-Leitfabrikat, Rauchmelder bewusst **Oppermann** (analog zur bereits
bestehenden Metz-Connect-Ausnahme bei LVB-Relais): Kanaltemperaturfühler
0,4m/2,0m (Siemens QAM2120.040/.200, LG-Ni1000 – **Kennlinie bewusst Ni1000,
weil nativ vom Siemens-Automationssystem unterstützt**; QAM2120.200 ist
bereits der Kapillar-Mittelwertfühler, keine eigene "QAM2129"-Typkennung
bei Siemens, ganze QAM21-Baureihe biegsame Kupferkapillare, kein starrer
Stab), Kanalfeuchtefühler (QFM2100, 3-Leiter), 2× Differenzdruckwächter
(QBM81-3 Filterüberwachung direkt auf DDC, QBM81-10 Ventilatorüberwachung
sicherheitsrelevant), Drucksensor Kanaldruck (QBM3020-10, 0-10V/3-Leiter),
Kanalhygrostat (QFM81.21, IP55, Sicherheitsfunktion), 2× Kanalrauchmelder
(Oppermann KRM-2-DZ 24V / KRM-1-DZ 230V, DIBt-Zulassung zur direkten
Klappenansteuerung – DIBt-Nummer selbst bewusst nicht im Auswahltext).

**Neuer Mechanismus: Pflichtzubehör bei Feldgeräten (`feldgeraete.json`).**
Analog zu `einzelbauteile.zubehoer_artikel_nr`/`syncZubehoer()` (Modul 4,
Session 41 – dort für Schaltschrank-Bauteile wie Schütz→Hilfsschalterblock),
aber auf Feldgeräte-Ebene: neues Feld `zubehoer_feldgeraet_artikel_nr`
(+ `zubehoer_menge`, Default 1) referenziert ein zweites `feldgeraete.json`-
Entry, das NICHT selbst als Baugruppe wählbar ist (taucht in Modul 4 also
nicht in der Baugruppen-Dropdown auf), aber automatisch mit in Modul 5s
Feldgeräte-Stückliste einfließt, sobald das Hauptgerät gewählt wird
(`aggregateFeldgeraete()` in Modul 5, zweiter Aggregationsdurchlauf über
`zubehoerNr`/`zubehoerMenge`). Zählt bewusst NICHT in
`sumFeldgeraete()`/„Feldgeräte gesamt" (Modul 4) – diese Zählung basiert
weiterhin rein auf Baugruppen-Instanzen aus `m04_belegung`, die
Zubehör-Zeile entsteht erst nachgelagert in Modul 5. Erster Anwendungsfall:
Montagekonsole `KS` (Oppermann, kein Preis gefunden) an beiden
Kanalrauchmelder-Baugruppen. **Vom Nutzer explizit als wiederkehrendes
Muster angekündigt** – weitere Feldgeräte mit funktionsfremdem Pflichtzubehör
sind zu erwarten, derselbe Mechanismus ist wiederverwendbar.

**Sicherheitsketten-Pattern (Koppelrelais):** QBM81 und QFM81.2x haben nur
**1 Wechsler** (ein gemeinsamer COM-Kontakt) – reicht nicht, um gleichzeitig
eine Leistungssteuerung (Abschaltung) UND eine getrennte DDC-Meldung zu
speisen. Baugruppen mit Sicherheitsfunktion (Ventilatorüberwachung,
Kanalhygrostat) schalten daher über ein zwischengeschaltetes Koppelrelais:
Sensor-Wechsler (klemm_s, 2 Klemmen) → Relaisspule (Zone `steuer`) → 2
galvanisch getrennte Ausgänge: Kontakt 1 → klemm_s mit `dp_bi` (DDC-Meldung,
nur mit der DDC-Referenzspannung beaufschlagt), Kontakt 2 → klemm_l
(Leistungssteuerung/Abschaltung, kein DDC-Bezug). **Spulenspannung bewusst
230V AC, nicht 24V DC** (Nutzer-Entscheidung, Grundsatz): eine 24V-DC-Spule
bräuchte ein zusätzliches Netzteil/einen Trafo als weiteren Ausfallpunkt in
der Sicherheitskette – bei 230V AC schaltet der Feldgerätekontakt direkt,
ohne zusätzliche Spannungswandlung. Neues Bauteil `2967099` (Phoenix Contact
PLC-RSC-230UC/21-21, 230VAC/220VDC-Spule, 2 Wechsler, sonst baugleich zum
bereits vorhandenen 24VDC-Pendant `2967060`) – **Koppelrelais-Bezeichnung
trägt immer die Spulenspannung im Klartext** (Konvention, kein eigenes
Schema-Feld). Ein Relais mit mehreren Wechslerkontakten kann pro Kontakt
unterschiedliche Spannungsebenen führen (galvanisch getrennt) – das war die
Kernfrage, die die Machbarkeit des Patterns bestätigt hat. Der
Kanalrauchmelder (KRM-DZ) braucht dieses Pattern NICHT: sein Alarmrelais hat
bereits 2 native, getrennte Kontakte (Umschalter Kl.11/12/13 + Öffner
Kl.14/15) – Umschalter direkt auf klemm_s/dp_bi (Sammelalarm), Öffner direkt
auf klemm_l (Klappenansteuerung). Verschmutzung/Systemstörung/Luftströmung
(3 weitere Störmeldekontakte der DZ-Version) je eigener `dp_bi` auf klemm_s.

**230V-Versorgung farbig, Meldekontakte bleiben grau:** beim 230V-Rauchmelder
(KRM-1-DZ) sind nur die 3 echten Versorgungsklemmen (L/N/PE) farbig (`3209510`
grau=L, `3209523` blau=N, `3209536` grün-gelb=PE, klemm_l) – alle
Relais-/Meldekontakt-Klemmen bleiben Standard-grau (`3209510`), auch wenn sie
zone `klemm_l` liegen (Nutzer-Klarstellung Session 52: Farbe kennzeichnet nur
echte Bus-/Versorgungsanschlüsse, nicht jede Klemme in der Leistungszone).

Verifiziert direkt im Browser (Wandschrank, 600×800mm, ohne Modul 1/3 direkt
über Modul 4s eigene Schranktyp/Montagebereich-Felder): Testbelegung
(1× Differenzdruckwächter Ventilatorüberwachung + 1× Kanalrauchmelder 24V)
liefert korrekt `BI 5/16` (1+4), Koppelrelais `2967099` korrekt in Zone
Steuerung platziert, Klemmenzonen korrekt verteilt (klemm_s 14×, klemm_l 4×),
automatische DDC-Ergänzung (TXM1.16D + PXC7.E400.A + Netzteil + LSS) greift
korrekt. Modul 5 zeigt beide Feldgeräte unbepreist plus die Montagekonsole
als dritte Zeile („aus: Zubehör zu: Kanalrauchmelder 24V") – Modul 4s
„Feldgeräte gesamt" bleibt korrekt bei 2 (Konsole nicht mitgezählt). Keine
Konsolenfehler. Backup vor der Excel-Änderung:
`C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-lueftungssensoren_*.xlsx`.

### Koppelrelais-Zonenkorrektur + Steuerspannungs-Baugruppen mit Netztyp-Automatik (Session 52 Nachtrag, gesperrt)
Nutzer-Korrektur direkt im Anschluss an die Lüftungssensoren-Session: das
230VAC-Koppelrelais (`2967099`) schaltet in den Sicherheitsketten-Baugruppen
(Ventilatorüberwachung, Kanalhygrostat) einen Starkstromkreis zur
Befeuchter-/Ventilatorabschaltung und wird auch aus dem Leistungskreis
versorgt – gehört daher in Zone `leist`, nicht `steuer` (Katalog-Default von
`2967099` entsprechend geändert, Baugruppen-Bauteile-Zeilen korrigiert).

**Neue Erkenntnis: jedes Feldgerät mit eigener Versorgungsspannung braucht
eine passende, abgesicherte Steuerspannungsquelle** (230V AC → Sicherung
+ **immer über einen Trenntransformator** nach DIN EN 60204-1, auch wenn
Quelle und Zielspannung identisch sind, nicht direkt von der Einspeisung
abgegriffen; 24V AC → Steuertrafo + Sicherung; 24V DC → Netzteil +
Sicherung – jeweils nur anlegen, falls in dem Projekt noch nicht
vorhanden). 3 neue Baugruppen `480_000008`–`010` (Gewerk 480, Automation):
„Steuerspannung 24V AC"/„24V DC"/„230V AC", alle Zone `leist`. Trafos:
Siemens 4AM40-Baureihe, 250VA (Standardgröße oberhalb des Zielwerts
~200VA) – `4AM4042-4TN00-0EA0` (230V/24V) und `4AM4042-4TT10-0FA0`
(230V/230V, Sicherheits-/Trenntrafo). Netzteil/Sicherungen wiederverwendet
aus dem Bestandskatalog (`QUINT-PS/1AC/24DC/2.5`, `5SL6106-7` B6A primär,
`5SL6116-7` B16A sekundär bei 24V-Ausgang ~10,4A). Bei Trafos IMMER 2
Sicherungen (primär+sekundär), beim Netzteil nur 1 (primärseitig, analog
zum bestehenden `ddc_netzteil_artikel_nr`/`ddc_sicherung_artikel_nr`-Muster
der DDC-CPUs).

**Neuer Mechanismus: `drehstrom_variante_artikel_nr`** (Feld auf
`einzelbauteile`, analog zu `doppelstock_variante_artikel_nr`/
`trennklemme_variante_artikel_nr`) – verweist von der Wechselstrom-Ausführung
(230V-Primärseite) auf die Drehstrom-Ausführung (400V-Primärseite)
desselben Trafos. **Automatische Auflösung** in Modul 4 über
`resolveNetztypArtikel()`, angewendet als letzter Schritt in JEDEM
Rückgabepfad von `resolveBaugruppenBauteile()` (Pflicht: identisch in
`buildQueues()` UND `aggregateStueckliste()`, sonst laufen Zeichnung und
Stückliste auseinander – exakt dieselbe Disziplin wie beim
Klemmenvarianten-Mechanismus). Liest `m03_zone_netztyp` direkt aus dem
localStorage-Kontrakt von Modul 3 (Feld existiert dort bereits seit Session
19) – **kein neues UI-Element in Modul 4 nötig**, keine manuelle
Doppelauswahl. Nutzer-Vorgabe/Prinzip: „Die gesamte Applikation basiert auf
einem schrittweisen Aufbau der Automationsanlage – wir sollten alle
bekannten Informationen nutzen." Damit sind es bewusst nur 3 Baugruppen
(nicht 6) trotz zweier Primärspannungsvarianten je Trafo-Baugruppe.

Verifiziert direkt im Browser: `m03_zone_netztyp='wechselstrom'` →
Stückliste zeigt `4AM4042-4TN00-0EA0` (230V/24V); nach Umschalten auf
`'drehstrom'` (Reload) automatisch `4AM4042-5AN00-0EA0` (400V/24V), ohne
manuellen Eingriff. Koppelrelais-Zonenkorrektur ebenfalls bestätigt
(Stückliste zeigt `L PLC-RSC-230UC/21-21...` statt vorher `S`). Keine
Konsolenfehler.

### Steuerspannungs-Auto-Ergänzung + Zonenkorrektur Hygrostat + Namensregel (Session 52 Nachtrag 3, gesperrt)
**Bug (Nutzer-Fund im Browser-Test):** ein 230VAC-Koppelrelais wurde platziert
(z. B. über „Kanalhygrostat"), aber die dafür nötige „Steuerspannung 230V
AC"-Baugruppe fehlte im Schrank, wenn der Nutzer sie nicht zusätzlich manuell
auswählte. Nutzer-Prinzip: „Alles nach Erfordernis" – ist die passende
Steuerspannung schon vorhanden (manuell gesetzt), nichts tun; sonst
automatisch ergänzen. **Neuer Mechanismus in Modul 4**, strukturell parallel
zur DDC-Auto-Modul-Ergänzung (Session 28e/50), aber präsenz- statt
kapazitätsbasiert: neues Feld `einzelbauteile.benoetigt_steuerspannung`
(`'24vac'`/`'24vdc'`/`'230vac'`, aktuell nur auf `2967099` gesetzt) +
`STEUERSPANNUNG_BG_VON_TYP`/`STEUERSPANNUNG_TYP_VON_BG`-Konstanten +
`steuerspannungWatermark` (eigener Ratchet, persistiert als
`m04_steuerspannung_watermark`, teilt sich den „↺ Zurücksetzen"-Button mit
dem DDC-Watermark). Läuft in `buildQueues()` über `bgInstanceQueue` (wie eine
normale Baugruppen-Instanz, inkl. `applyNetztypResolution()` für die
Trafo-Wahl) statt über den DDC-Weg (raw `queues[zone].push()`), da die
Steuerspannungs-Baugruppen selbst ganz normale Baugruppen sind. Panel
„AUTOMATISCH ERGÄNZT (DDC)" zeigt jetzt beide Kategorien gemeinsam (Header
ohne „(DDC)"-Zusatz). Verifiziert: nur Kanalhygrostat platziert → Trafo+2
Sicherungen erscheinen automatisch; zusätzlich manuell „Steuerspannung 230V
AC" hinzugefügt → keine Dopplung (Auto-Ergänzung verschwindet aus der
Anzeige, Stückliste bleibt bei 1× Trafo).

**Zonenkorrektur Kanalhygrostat (Nutzer-Fund):** die 2 Klemmen des
Hygrostat-Feldkabels (Sensorschleife zur Relaisspule) lagen in `klemm_s`
(Sensoren) – falsch, der Hygrostat ist als Schaltgerät ein **Feldgerät**,
keine Sensor im engeren Sinn → jetzt `klemm_f`. Grundsatz (Nutzer-Vorgabe,
gilt für künftige Baugruppen): **1 Kabel = zusammenhängende Klemmen in
EINER Zone, mehrere Kabel = Aufteilung auf mehrere Zonen zulässig.** Der
Hygrostat hat 3 separate Leitungen (Feldkabel zum Sensor → jetzt `klemm_f`;
Relais→DDC-Meldung → `klemm_s`; Relais→Leistungssteuerung → `klemm_l`) –
das bleibt zulässig aufgeteilt, nur die Feldkabel-Klemmen selbst waren
falsch zugeordnet. **Offen:** dieselbe Schaltgerät-vs-Sensor-Frage betrifft
vermutlich auch die beiden Differenzdruckwächter-Baugruppen (`430_000011`/
`012`, QBM81 ist ebenfalls ein Schaltgerät) und die Kanalrauchmelder
(`430_000015`/`016`) – noch nicht angepasst, mit dem Nutzer abzustimmen.

**Namensregel (Nutzer-Vorgabe):** Auswahltext-Suffix-Reihenfolge, jeweils
nur falls zutreffend: `Text Bauteil → Messbereich → Versorgungsspannung →
Zulassungen/Zertifizierungen`. Bereits vorher korrekt (Kanalrauchmelder:
Spannung+Zulassung; Differenzdruckwächter: Messbereich). Nachgezogen:
„Kanalfeuchtefühler 24V AC/DC" (QFM2100 war ohne Spannungsangabe),
„Drucksensor Kanaldruck 0...1000 Pa, 24V AC/DC" (QBM3020 fehlte die
Spannung), „Kanalhygrostat 15...95% r.F." (Messbereich ergänzt),
„Kanaltemperaturfühler 0,4m (Kapillar, Punktmessung) -50...+80°C",
„Kanaltemperaturfühler 2,0m (Kapillar-Mittelwert) -50...+80°C",
„Kanalfeuchtefühler 0...100% r.F., 24V AC/DC" (Nutzer-Fund: Messbereich
fehlte bei allen 3 Kanalsensoren). **Offen:**
die älteren Raumsensor-Baugruppen (Session 51: Raum-CO2/-VOC/-Feuchte-/
Kombisensor) haben Spannung UND Messbereich nachträglich erhalten (Nutzer-Fund
„Messbereich fehlt auch bei Raumsensoren", per Originaldatenblatt
gegengeprüft statt geschätzt): „Raumtemperatursensor passiv 0...50°C",
„Raum-CO2-Sensor 0...2000ppm, 24V AC/DC", „Raum-VOC-Sensor 0...100% VOC, 24V
AC/DC" (Messbereich laut CE1N1961de tatsächlich 0...100% VOC, kein
ppm-Wert), „Raumfeuchtesensor 0...100% r.F., 24V AC/DC",
„Raumtemperatur- und Feuchtesensor 0...50°C/0...100% r.F., 24V AC/DC"
(Temperaturbereich = Werkeinstellung R2 der QPA/QFA-Familie, 3 Bereiche
per Steckbrücke wählbar – nicht QFA2060-spezifisch gegengeprüft, sondern
aus dem baugleichen Schaltungsprinzip der QPA-Family übernommen),
„Tauchtemperatursensor 100mm/150mm mit Tauchhülse G1/2" -30...+130°C"
(Messbereich laut Siemens-Originaldatenblatt CE1N1781en: „-30...+130°C
other types" – gilt für LG-Ni1000, nicht NTC).

### Klemmzonen-Grundsatzregel: Sensor vs. Feldgerät (Session 52 Nachtrag 4, gesperrt)
Nutzer-Klarstellung, ab sofort verbindlich für alle künftigen Baugruppen:
**`klemm_s` (Sensoren-Klemmleiste) ist für echte Messsensoren reserviert**
(meist < 50V SELV) – **sowohl passiv** (Widerstandsmessung ohne
Hilfsenergie, z. B. QAA24/QAM2120/QAE2120 – Korrektur, ursprünglich fälschlich
auf "Sensoren mit analogem Ausgang" verengt) **als auch aktiv mit
Analogausgang** (Raumsensoren, Kanalfühler, Drucksensor mit Analogausgang).
**Jedes Schaltgerät (binärer Kontakt/Relaisausgang, kein Analogsignal) ist
ein Feldgerät und gehört auf `klemm_f`**,
auch wenn sein Signal am Ende als BI an die DDC geht – die Zone richtet
sich nach der Signalart am Gerät, nicht nach dem Ziel. Nur echte
Leistungs-/Netzanschlüsse (230V-Versorgung, Leistungssteuerungs-Ausgang zu
einem Aktor) bleiben `klemm_l`. Umgesetzt (26 Klemmen-Zeilen über 5
Baugruppen von `klemm_s` auf `klemm_f`):
- `430_000011`/`012` (Differenzdruckwächter): alle Klemmen jetzt `klemm_f`
  (Filterüberwachung komplett; Ventilatorüberwachung: Sensorschleife +
  DDC-Meldung-Ausgang – nur der Leistungssteuerungs-Ausgang bleibt `klemm_l`).
- `430_000014` (Kanalhygrostat): zusätzlich zur bereits korrigierten
  Sensorschleife jetzt auch der DDC-Meldung-Ausgang auf `klemm_f`.
- `430_000015`/`016` (Kanalrauchmelder): Versorgung (nur 24V-Variante, die
  230V-L/N/PE-Versorgung bleibt bewusst `klemm_l`, siehe Session-52-Regel
  „Farben für Leistungsanschlüsse ab 230V AC"), Alarm-Umschalter,
  Verschmutzung/Systemstörung/Luftströmung – alle auf `klemm_f`. Nur der
  Alarm-Öffner (Klappenansteuerung/Leistungssteuerung) bleibt `klemm_l`.

Verifiziert direkt im Browser (Ventilatorüberwachung + Kanalrauchmelder
230V zusammen platziert): Stückliste zeigt korrekt keine `klemm_s`-Zeile
mehr für diese Baugruppen, `klemm_f` grau ×12, `klemm_l` grau/blau/
grün-gelb ×5/1/1 – exakt die erwartete Verteilung. Keine Konsolenfehler.

### Desigo PX auf 24V-AC-Versorgung umgestellt + Steuerspannungs-Auto-Ergänzung auf Baugruppen-Ebene (Session 52 Nachtrag 5, gesperrt)
**Bug (Nutzer-Fund):** Raum-CO2-Sensor (und die anderen aktiven Raumsensoren)
lösten die Steuerspannungs-Auto-Ergänzung nicht aus, obwohl sie 24V-Versorgung
brauchen. Ursache: `benoetigt_steuerspannung` saß bisher nur am Katalogartikel
(einzig sinnvoll für einen eindeutigen Artikel wie das 230VAC-Koppelrelais) –
die Sensoren hängen aber an ganz gewöhnlichen grauen Klemmen (`3209510`), die
überall verwendet werden und daher kein artikel-eigenes Merkmal tragen
können. **Fix:** neues Feld `baugruppen.benoetigt_steuerspannung` (gleicher
Wertebereich `'24vac'`/`'24vdc'`/`'230vac'`), in Modul 4 zusätzlich zum
bestehenden Artikel-Check ausgewertet (`buildQueues()`, direkt bei
`BAUGRUPPEN_DB.find(...)` im Baugruppen-Zweig). Gesetzt auf die 6 aktiven
Sensoren mit AC/DC-Doppelspannung: CO2/VOC/Feuchte-/Kombisensor,
Kanalfeuchtefühler, Drucksensor Kanaldruck.

**Spannungswahl 24V AC (nicht DC) – Nutzer-Vorgabe nach Recherche-Auftrag:**
recherchiert, wie Desigo-PX-Automationsstationen typischerweise versorgt
werden (Siemens-Originaldatenblatt PXC5.E24, A6V13187283en). Ergebnis:
PXC-Stationen akzeptieren beides (AC oder DC 24V), aber **nur bei AC-Speisung
liefert die Station selbst bis zu 2A AC 24V an die TX-I/O-Feldgeräteklemme
V~** (bei DC-Speisung ist auch V~ nur DC) – zusätzlich funktioniert das
**Triac-Modul TXM1.8T nur bei AC-Versorgung der Station**. 24V AC ist damit
die flexiblere/funktional überlegene Wahl, nicht nur Konvention. **Deshalb
wurden auch die 3 Desigo-PX-CPU-Katalogeinträge umgestellt**
(`ddc_netzteil_artikel_nr` von `2866690`/QUINT-PS-Netzteil-DC auf
`4AM4042-4TN00-0EA0`/Siemens-4AM40-Steuertrafo-AC, 250VA – dieselbe Baugröße
wie bei den Steuerspannungs-Baugruppen, siehe oben). Ein Trafo braucht
IMMER 2 Sicherungen (primär+sekundär, Session-52-Grundsatz) – neues Feld
`einzelbauteile.ddc_sicherung2_artikel_nr` (analog zu
`ddc_sicherung_artikel_nr`), Modul 4 (`buildQueues()`/`ddcAutoZone()`/
`aggregateStueckliste()`) entsprechend um eine zweite Sicherung erweitert.
Primär `5SL6106-7` (B6A, unverändert), sekundär neu `5SL6110-7` (B10A – nach
Siemens-Datenblattvorgabe „External supply line fusing: max 10A slow-blow
oder 13A Leitungsschutzschalter" für die 24V-Seite, passt besser als die bei
den Sensor-Baugruppen verwendete B16A).

Jeder Verbraucher bekommt weiterhin seine **eigene** Spannungsversorgung
(Nutzer-Grundsatz, nicht geteilt): die DDC-CPU-Versorgung (Zone `steuer`,
Teil der bestehenden Automationsstations-Gruppen-Logik) und die
Feldgeräte-Steuerspannung (Zone `leist`, Baugruppe „Steuerspannung 24V AC")
sind zwei separate Transformatoren, auch wenn beide zufällig denselben
Katalogartikel nutzen.

**Offen, nicht entschieden:** der bereits länger im Katalog stehende große
„Steuertrafo 1-ph., 230V/24V, 2,5kVA" (`4AM5742-4TT10-0FA0`, `bauteil_typ:
'sonstige'`) ist NICHT der hier verwendete – deutlich überdimensioniert für
den tatsächlichen Bedarf (Desigo-PX-Volllast lt. Datenblatt 88VA, der neu
verwendete 250VA-Trafo hat bereits reichlich Reserve). Bleibt vorerst
unangetastet im Katalog, falls für einen anderen (größeren) Zweck gedacht –
mit dem Nutzer zu klären.

Verifiziert direkt im Browser: CO2-Sensor allein platziert (kein manueller
Zusatzschritt) → zwei automatisch ergänzte Trafo-Gruppen erscheinen
korrekt getrennt: 1× Steuertrafo+2 Sicherungen in `steuer`/`evert` (für die
automatisch ergänzte Desigo-PX-CPU) UND 1× Steuertrafo+2 Sicherungen in
`leist` (für den Sensor, aus der Baugruppe „Steuerspannung 24V AC"). Keine
Konsolenfehler.

### Geteilter Sicherheitstrafo für DDC-CPU + 24V-AC-Sensoren im Leistungsfeld (Session 52 Nachtrag 6, gesperrt)
**Nutzer-Vorgabe (Siemens-Vorschrift):** Sensoren mit 24V AC an der DDC
sollen denselben Sicherheitstrafo nutzen wie die DDC-CPU selbst – eine
einmal gesetzte CPU hat die 24V-AC-Steuerspannung damit implizit „an
Board", ein zusätzlicher Sensor löst KEINEN zweiten Trafo mehr aus. Der
Trafo selbst wandert vom Steuerungsfeld (direkt vor der CPU) ins
Leistungsfeld.

**Architektur-Umbau:** die CPU hat kein eigenes dediziertes Netzteil mehr
(`ddc_netzteil_artikel_nr`/`ddc_sicherung_artikel_nr`/
`ddc_sicherung2_artikel_nr` auf den 3 Desigo-PX-Katalogeinträgen geleert,
Modul-4-Code dafür entfernt) – stattdessen tragen die CPUs jetzt
`benoetigt_steuerspannung: '24vac'` (dasselbe Feld wie beim
230VAC-Koppelrelais) und laufen durch **denselben** Steuerspannungs-Auto-
Mechanismus wie die Feldgeräte-Sensoren (Session 52 Nachtrag 2/5). Dafür
musste die Reihenfolge in `buildQueues()` getauscht werden: der
Steuerspannungs-Block läuft jetzt NACH der CPU-Gruppen-Auflösung
(`neededExtraCpus`), nicht mehr davor – sonst hätte eine automatisch
ergänzte CPU ihren eigenen Bedarf nie anmelden können. Die
Netzteil→CPU-„lückenlos auf derselben Hutschiene"-Regel (Session 50)
ist damit für das Netzteil **aufgehoben** (bewusster Bruch, Nutzer-
Vorgabe) – die reine E/A-Modul-Reihenfolge (CPU→ihre TXM-Module
lückenlos) bleibt unverändert bestehen, nur ohne vorangestelltes
Netzteil.

**Bewusst KEINE Kapazitäts-/VA-Bilanzierung** (Nutzer-Vorgabe): der Trafo
wird nie ein zweites Mal automatisch ergänzt, nur weil viele Verbraucher
an einem hängen – 250VA gilt pauschal als ausreichend für CPU+Feldgeräte
eines Schranks (DBACS ermittelt Platzbedarf, plant nicht bis ins Detail
durch). Bestätigt: der verwendete Trafo (`4AM4042-4TN00-0EA0`, 24V
sekundär) ist nach Siemens' eigener Definition immer ein
Sicherheitstransformator nach EN 61558-2-6 („Netztransformatoren mit
≤50V auf der Ausgangsseite sind bei SIRIUS-Transformatoren immer als
Sicherheitstransformatoren ausgeführt").

Verifiziert im Browser (frischer Tab): CO2-Sensor allein platziert →
genau EIN gemeinsamer „Steuertransformator 1-ph. 230V/24V, 250VA" +
2 Sicherungen erscheinen, Zone `leist` (nicht mehr `steuer`), sowohl für
die automatisch ergänzte CPU als auch den Sensor. Keine Konsolenfehler.

**Nachkorrektur (2 Nutzer-Funde beim Testen, direkt im Anschluss):**
1. Die 2 Sicherungen der 3 Steuerspannungs-Baugruppen (`480_000008`–`010`)
   lagen fälschlich in `leist` – Sicherungen gehören wie überall sonst im
   Projekt nach `evert` (Energieverteilung), nur der Trafo/das Netzteil
   selbst bleibt in `leist`.
2. Die Sekundärsicherung von `480_000008` (Steuerspannung 24V AC) war noch
   `5SL6116-7` (B16A) aus der ursprünglichen Sensor-Berechnung
   (250VA/24V≈10,4A) – seit der Trafo die CPU mitversorgt, gilt aber die
   Siemens-Vorgabe „max. 10A träge" für die 24V-AC-Versorgungsleitung der
   CPU. Korrigiert auf `5SL6110-7` (B10A). Primärsicherung (B6A) sowie die
   Sicherungen von `480_000009`/`010` (nicht CPU-relevant) unverändert.

Erneut verifiziert (frischer Tab, Raumtemperatursensor passiv – bewusst ein
Fall ohne eigenen Steuerspannungsbedarf, nur die automatisch ergänzte CPU
löst die Auto-Ergänzung aus): Stückliste zeigt `EV LSS B6A` + `EV LSS B10A`
+ `L Steuertransformator`, exakt wie erwartet. Keine Konsolenfehler.

**Weitere Korrektur (Nutzer-Fund, Schaltungsverständnis Koppelrelais):**
`430_000012`/`014` hatten fälschlich je 4 zusätzliche „Landeklemmen" für
die beiden Kontaktstrecken des Koppelrelais (DDC-Meldung + Leistungs-
steuerung) – überflüssig, das Koppelrelais hat für beide Kontaktstrecken
bereits eigene Schraubklemmen, keine separaten Klemmenblöcke nötig. Nur
die 2 Klemmen für das eingehende Feldkabel (Sensor-Schaltkontakt steuert
über diese 2 Adern die Relaisspule an) bleiben. `dp_bi` sitzt jetzt direkt
auf der Koppelrelais-Zeile statt auf einer eigenen Klemmenzeile. Beide
Baugruppen dadurch von 7 auf 3 Bauteile reduziert (2 Klemmen + 1
Koppelrelais). Verifiziert im Browser: Stückliste zeigt korrekt nur noch
`KF Durchgangsklemme ×2` (kein `klemm_l` mehr) für die QBM81-10-Baugruppe,
plus getrennt und korrekt beide ausgelösten Steuerspannungs-Trafos (24V AC
für die CPU, 230V AC für das Koppelrelais – zwei unterschiedliche
Bedarfsträger, beide zu Recht separat). Keine Konsolenfehler.

**Kanalrauchmelder (Nutzer-Fund, direkt im Anschluss):** der Alarm-Öffner
(Klappenansteuerung/Leistungssteuerung) lag noch in `klemm_l` – falsch,
der Rauchmelder ist als Ganzes ein Feldgerät, nicht „teils Leistung".
Jetzt auf `klemm_f` umgestellt (`430_000015`: alle 12 Klemmen `klemm_f`;
`430_000016`: nur noch die echte 230V-L/N/PE-Netzversorgung bleibt
`klemm_l`, die restlichen 10 Klemmen `klemm_f`). Nutzer-Hinweis: in der
Praxis werden die 6 Adernpaare vermutlich als max. 2 reale Kabel geführt
(kein weiterer Modellierungsschritt nötig, da alle Klemmen bereits in
derselben Zone liegen – die 1-Kabel-Regel betrifft nur Zonen-Grenzen).
Verifiziert im Browser: Stückliste zeigt `KL` nur noch für L/N/PE (3),
`KF` für alle übrigen 10 Klemmen. Keine Konsolenfehler.

**Nachtrag (Nutzer-Korrektur):** auch die 230V-L/N/PE-Netzversorgung von
`430_000016` kann aus der Feldgeräte-Klemmleiste versorgt werden – Farbe
(grau/blau/grün-gelb) bleibt erhalten, nur die Zone wechselt final von
`klemm_l` auf `klemm_f`. Damit liegt `430_000016` jetzt komplett (alle 13
Klemmen) in `klemm_f` – `klemm_l` wird für diese Baugruppe nicht mehr
verwendet. Zeigt: 230V-Versorgung ist nicht per se ein Ausschlusskriterium
für `klemm_f` – die frühere Session-52-Regel „Farben für Leistungs-
anschlüsse ab 230V AC" bezieht sich nur auf die Klemmenfarbe, nicht auf
die Zonenwahl. Verifiziert im Browser: alle 13 Klemmen zeigen `KF`
(11× grau, 1× blau, 1× grün-gelb). Keine Konsolenfehler.

**Nachtrag (Nutzer-Fund, echter Bug):** `430_000016` selbst hatte kein
`benoetigt_steuerspannung` gesetzt – die L/N/PE-Klemmen hingen dadurch
„in der Luft", ohne dass die Baugruppe selbst je die 230V-Trenntrafo-
Auto-Ergänzung auslöste (ein vorheriger Test zeigte den Trafo nur zufällig
durch einen noch nicht zurückgesetzten Watermark-Rest aus einem anderen
Testlauf – Verwechslungsgefahr beim manuellen Testen mit `localStorage`,
das sich mehrere Browser-Tabs derselben Origin teilen). Jetzt
`benoetigt_steuerspannung: '230vac'` auf `430_000016` gesetzt. Verifiziert
mit vollständig geleertem `localStorage` (nicht nur den beiden Watermark-
Keys): Rauchmelder allein platziert → `Sicherheits-/Trenntransformator
230V/230V` (ausgelöst vom Rauchmelder selbst) UND `Steuertransformator
230V/24V` (ausgelöst von der automatisch ergänzten CPU wegen 4× BI-Bedarf)
erscheinen beide korrekt getrennt. Keine Konsolenfehler.

### Zwei Nachzügler-Bugs bei der Trafo-Umstellung (Session 52 Nachtrag 7, gesperrt)
Zwei vom Nutzer gefundene Bugs, beide Folgefehler der Nachtrag-6-Umstellung
(geteilter Steuerspannungs-Trafo):

1. **Baugruppe „Automationsstation (AE)" (`480_000007`)** hatte weiterhin
   das alte 24V-DC-Netzteil (`2866690`) + dessen Sicherung (`5SL6106-7`)
   fest in ihrer eigenen `bauteile`-Liste eingebaut – ein Überbleibsel aus
   Session 49/50, das beim Nachtrag-6-Umbau nicht mitgezogen wurde. Die
   CPU (`PXC7.E400.A`) trägt bereits `benoetigt_steuerspannung:'24vac'`
   und löst die neue geteilte Automatik selbst korrekt aus – das alte
   Netzteil lief dadurch DOPPELT (alt fest verbaut + neu automatisch
   ergänzt). Fix: die beiden alten Bauteil-Zeilen aus `480_000007`
   entfernt, nur noch die CPU bleibt übrig.
2. **Baugruppe „Steuerspannung 24V DC" (`480_000009`)**: die
   `baugruppen_bauteile`-Zeile für das Netzteil referenzierte fälschlich
   die **Typbezeichnung** `QUINT-PS/1AC/24DC/2.5` statt der echten
   Katalog-Artikelnummer `2866690` (die Typbezeichnung steht nur in
   `bezeichnung`, nicht in `artikel_nr`). Der `EINZELBAUTEILE_DB.find()`-
   Lookup lief dadurch ins Leere; da `buildQueues()`/`aggregateStueckliste()`
   bei `!eb` einfach `return` machen, wurde das Netzteil OHNE Fehlermeldung
   komplett übersprungen – nur die Sicherung erschien. Vollständiger Katalog-
   Scan (`baugruppen[].bauteile[].artikel_nr` gegen alle
   `einzelbauteile[].artikel_nr`) bestätigt: einzige kaputte Referenz im
   gesamten Katalog, jetzt auf `2866690` korrigiert.

Verifiziert im Browser (beide Fälle einzeln, `localStorage` vorher
geleert): „Automationsstation (AE)" zeigt nur noch 1× CPU + 1× geteilter
Trafo + 2 Sicherungen (kein doppeltes Netzteil mehr); „Steuerspannung 24V
DC" zeigt jetzt korrekt Netzteil (`L`) + Sicherung (`EV`) zusammen. Keine
Konsolenfehler.

## Gesperrte Entscheidungen

Diese Punkte wurden bereits ausführlich diskutiert und entschieden – nicht neu aufgreifen. **Archiv-Hinweis (14.08.2026):** ausführliche Session-Protokolle werden zu kompakten Ergebnis-Zusammenfassungen eingedampft (Volltext inkl. Nutzer-Funden/verworfenen Zwischenständen/Verifizierungsdetails liegt in `docs/archiv/claude-md-modul4-sessions-20-29.md`, `docs/archiv/claude-md-modul4-sessions-30-34.md` und `docs/archiv/claude-md-modul4-sessions-35-51.md`) – Grund: `CLAUDE.md` wird bei jeder Sitzung vollständig geladen, unabhängig vom Umfang der Aufgabe. Bei künftigen sehr langen Session-Nachträgen ebenso verfahren: verbindliche Regel kompakt in `CLAUDE.md`, ausführliche Vorgeschichte ins Archiv.

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
