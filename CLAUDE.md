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

## Offene Punkte (Stand Session 51 – vor Beginn der nächsten Sitzung lesen)

1. **Bug, NICHT gesperrt/gelöst:** Baugruppen-Zusammenhalt über Feldgrenzen
   hinweg wird bei Klemmleisten-Zonen manchmal verletzt – zwei Klemmen
   derselben Baugruppen-Instanz landen in unterschiedlichen Feldern. Mit dem
   aktuellen (mm-basierten) Code reproduziert bei 63× Baugruppe
   „Binäreingang (BI) auf Klemmleiste" (Wandschrank, 2 Felder). Ausführliche
   technische Details, bereits ausgeschlossene Ursachen und der nächste
   Debugging-Schritt siehe Abschnitt „Modul 4 – OFFEN: Klemmen-Gruppen-Split"
   unten (steht bewusst ausnahmsweise VOR den gesperrten Entscheidungen).
2. **Punkte 2–4 aus der letzten Sitzung (Doppelstockklemmen, CPU-Typ-
   Dropdown, Klemmenfarbe DDC-Abgänge) sind implementiert**, siehe
   „Modul 4 – Doppelstockklemmen, CPU-Typ-Dropdown, Klemmenfarbe DDC-Abgänge
   (Session 51)" weiter unten. **WICHTIG: Browser-Live-Test steht noch aus**
   – die Preview-Umgebung war in der Implementierungs-Sitzung durchgehend
   nicht erreichbar (Infrastrukturproblem, keine einzige Navigation zu
   `localhost:8099` erfolgreich, >20 Versuche über mehrere Tabs/Server-
   Neustarts). Verifiziert wurde nur per Code-Review + JSON-Strukturprüfung
   (keine doppelten `artikel_nr`, Felder korrekt exportiert). Vor produktivem
   Vertrauen in diese Änderungen: einmal im Browser durchklicken (Doppelstock-
   Checkbox + CPU-Dropdown + neue Klemmen 3210156/3210400/3210567 in der
   Direktbauteil-Auswahl prüfen).

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

### Modul 4 – OFFEN: Klemmen-Gruppen-Split bei mehreren Feldern (Session 51, NICHT gelöst – Fortsetzung nächste Sitzung)
Nutzer-Fund im Anschluss an den Klemmenbreiten-Fix (siehe unten „Modul 4 –
Klemmleisten: reale mm-Breite"): bei einer Baugruppen-Instanz, deren beide
Klemmen (Signal + Referenz, z. B. „Binäreingang (BI) auf Klemmleiste",
`480_000001`) eigentlich atomar zusammen platziert werden müssten
(Session-49-Prinzip, `platziereBaugruppenFuerFeld()`), landen manche Male
beide Klemmen der LETZTEN Instanz in unterschiedlichen Feldern statt
gemeinsam im selben. Nutzer-Einschätzung: „Kann fast nie vorkommen, kam hier
nur wegen der falschen Klemmenbreite" – ist aber nach dem Breiten-Fix
weiterhin reproduzierbar (Screenshot mit 63× `480_000001`, Wandschrank,
2 Felder, `reserve_pct=20%` mit Warndreieck).

**Bereits ausgeschlossen (Session 51, ausführlich getestet, siehe unten):**
- Code-Nachverfolgung von `platziereBaugruppenFuerFeld()`: die
  Instanz-Prüfung testet `confirmed[zn].concat(inst.zonen[zn])` als Ganzes
  je Zone – schlägt eine Klemme fehl (`leftoverDevs.length>0`), wird
  `fitsAll=false` und die GESAMTE Instanz verworfen (`if (!fitsAll) break`,
  VOR dem Commit-Block) – theoretisch kein Partial-Commit möglich.
- Systematischer Breiten-Sweep 60–900mm (5mm-Schritte, 169 Werte) mit
  **17×** `480_000001` allein, Wandschrank, `zone_modus=je_feld`: 0 Treffer.
- Zweiter Sweep (85 Werte, 10mm-Schritte) mit **17×** `480_000001` +
  Automationsstation-Baugruppe (`480_000007`, belegt steuer/leist/evert,
  nicht klemm_f) + zusätzlicher konkurrierender Direktbedarf in `klemm_l`
  (23 Stk.) und `klemm_s` (11 Stk.), um die Breiten-Redistribution
  (`redistributeKlemmBands()`) realistisch mitzubelasten: ebenfalls 0
  Treffer.
- Dritter Sweep (169 Werte) mit **63×** `480_000001` allein (exakte
  Nutzer-Menge aus dem Screenshot): ebenfalls 0 Treffer.

**Noch nicht ausgeschlossen / nächster Schritt:** alle drei Sweeps nutzten
SYNTHETISCHE `m03_*`-Werte (`b_uss=150`, `b_leist=b_steuer=b`, `h_klemm=95`
fest, testweise variiertes `b`) statt eines echten, in sich konsistenten
Modul-1→2→3-Rechenlaufs. Der Nutzer-Screenshot zeigt reale, bisher nicht
bekannte Modul-1/2/3-Werte (Wandschrank-Breite/Höhe, evtl. abweichende
`b_uss`/Kanalbreiten aus einer echten M3-Berechnung) – möglich, dass genau
diese Kombination (nicht die reine Feldbreite `b`) die Bedingung auslöst,
z. B. über eine Wechselwirkung mit `redistributeKlemmBands()`s
`reserveShortfall`-Warnung (im Screenshot sichtbar: `reserve_pct 20 ⚠`) oder
mit der Kanal-Platzierung (`kanalPending`/`H_KANAL`) einer NICHT rein
klemm_f-exklusiven Feldzusammensetzung. **Vorgehen nächste Sitzung:** vom
Nutzer die exakten Modul-1/2/3-Ausgangswerte (Schrankmodell/-maße,
`zone_modus`, `reserve_pct`) erfragen ODER direkt `JSON.stringify(belegung)`
+ alle `m01_*`/`m02_*`/`m03_*`-localStorage-Werte aus seiner laufenden
Session abgreifen lassen, damit eine bit-genaue Reproduktion (statt
Parameter-Sweep) möglich ist – vermutlich schneller zielführend als weiteres
Raten an Eingabewerten.

### Modul 4 – Doppelstockklemmen, CPU-Typ-Dropdown, Klemmenfarbe DDC-Abgänge (Session 51, UMGESETZT ABER NICHT IM BROWSER VERIFIZIERT)
Nutzer-Auftrag „Setze Punkt 2 bis 4 in einem Zug um" (aus der Offene-Punkte-
Liste der letzten Sitzung). **Browser-Preview war während der gesamten
Umsetzung nicht erreichbar** (>20 Navigationsversuche zu `localhost:8099`
über mehrere frische Tabs und Server-Neustarts, `navOk:false`) – nur per
Code-Review und JSON-Struktur-/Duplikatsprüfung kontrolliert. Vor
produktivem Vertrauen einmal im Browser durchklicken.

**Punkt 4 – Klemmenfarbe DDC-Abgänge:** Die Referenzklemme (zweites Bauteil)
aller 6 DDC-Reserve-Baugruppen (`480_000001`–`480_000006`) war `3209523`
(PT 2,5 **BU blau**) – umgestellt auf `3209510` (PT 2,5 **grau**, dieselbe
Klemme wie die Signalklemme). Betrifft `baugruppen_bauteile` – jede
Baugruppe hat jetzt zweimal `3209510` in derselben Zone statt `3209510` +
`3209523`.

**Punkt 2 – Doppelstockklemmen:** Neue Checkbox „Doppelstockklemmen
(DDC-Reserve)" im Block „Grund- & Reserveangaben" (`#doppelstock_aktiv`,
persistiert `localStorage['m04_doppelstock']`, Default AUS – Nutzer muss
aktiv setzen). Neue Funktion `resolveBaugruppenBauteile(bg, doppelstockAktiv)`:
ersetzt bei aktiver Checkbox zwei aufeinanderfolgende Bauteil-Einträge einer
Baugruppe mit identischem `artikel_nr`+Zone (= das jetzt einheitliche
Signal+Referenz-Klemmenpaar aus Punkt 4) durch EINE Doppelstockklemme im
selben mm-Platzbedarf (Auflösung über neues Katalogfeld
`eb.doppelstock_variante_artikel_nr`) – das erste Vorkommen wird ersetzt
(behält seinen `dp_*`/`lvb_erforderlich`-Override), das zweite entfällt.
Aufgerufen sowohl in `buildQueues()` (physische Platzierung) als auch in
`aggregateStueckliste()` (Stückliste) – beide müssen dieselbe Funktion
nutzen, sonst laufen Zeichnung und Stückliste auseinander (unterschiedliche
`artikel_nr` als Schlüssel für `buildIdxMap()`).

**Punkt 3 – CPU-Typ-Dropdown:** Neues `<select id="cpu_typ_override">` im
Statistikfeld unten (Block „Statistik · DDC-Automationseinrichtung"),
Optionen aus `EINZELBAUTEILE_DB.filter(bauteil_typ==='ddc_cpu')` befüllt
(„Automatisch (empfohlen)" als Default plus alle drei CPU-Katalogtypen aus
Session 50, mit „· modular"/„· kompakt"-Suffix aus `auto_ea_cpu`).
Persistiert `localStorage['m04_cpu_typ_override']`. In `buildQueues()` hat
die manuelle Wahl (`gs('cpu_typ_override')`) Vorrang vor `auto_ea_cpu` bei
der `cpuEb`-Ermittlung – alles Nachgelagerte (Netzteil/Sicherung-Auflösung
über `cpuEb.ddc_netzteil_artikel_nr`/`ddc_sicherung_artikel_nr`,
`max_ea_module`-Kapazitätsgrenze) bleibt unverändert generisch und
funktioniert automatisch auch für die beiden Kompaktstationen, da diese
bereits in Session 50 dieselben Zusatzfelder bekommen haben.

**Katalog-Recherche (Phoenix Contact, PT-2,5-Push-in-Reihe, alle grau,
5,2mm Pitch-Breite – identisch zur Standardklemme `3209510`):**
- `3210567` PTTB 2,5 (Doppelstockklemme, 2 Ebenen, 45,8mm hoch, 1,95€) –
  neu angelegt, `doppelstock_variante_artikel_nr` von `3209510` darauf gesetzt.
- `3210156` PT 2,5-MT (Messertrennklemme) – **existierte bereits seit
  Session 27b/44** im Katalog (mit dem Hinweis „Höhe unsicher, zu
  verifizieren"); Höhe jetzt gegen watt24.com-Datenblatt bestätigt (61,93mm,
  nur geringe Abweichung zur alten 62,2mm-Schätzung), Preis ergänzt (1,55€),
  Zone von `klemm_l,klemm_f,klemm_s` auf `klemm_f,klemm_s` eingeschränkt
  (Nutzer-Vorgabe: „im Steuerungsklemmfeld werden nur die grauen Klemmen
  benötigt, Farben sind für Leistungsanschlüsse ab 230V AC" – `klemm_l`
  bleibt den farbigen Leitungsklemmen vorbehalten). **Beim ersten Anlegen
  versehentlich ein Duplikat mit derselben `artikel_nr` erzeugt (nicht
  bemerkt, dass der Artikel schon existierte) – im selben Arbeitsschritt
  gefunden und korrigiert** (Duplikat-Zeile geleert, Original-Zeile
  aktualisiert statt einer zweiten Zeile).
- `3210400` PTTBS 2,5-2MTB (Doppelstock-Trennklemme, 2 Ebenen JE MIT
  Trennmesser, 127,5mm hoch, 10,64€ netto) – neu angelegt,
  `doppelstock_variante_artikel_nr` von `3210156` darauf gesetzt. **Erster
  Versuch war `3210405` (PTTBS 2,5-MTB/TGB)** – vom Nutzer korrigiert
  („Nimm besser die PTTBS 2,5-2MTB"), da MTB/TGB nur EINE Ebene mit
  Trennmesser und die andere nur mit reiner Trenn-/Prüfsteckstelle
  kombiniert, während 2MTB auf BEIDEN Ebenen ein Trennmesser hat – die
  fehlerhafte Zeile wurde auf `3210400` umgeschrieben (keine zusätzliche
  Karteileiche stehen gelassen). Vorsicht: erste gefundene Maßangabe für
  `3210400` (271×72×172mm, shortec.com) war die VERPACKUNGSGRÖSSE einer
  50er-Gebindeeinheit, nicht die Einzelklemme – zweite Quelle
  (wsu-industrials.com) lieferte die korrekten Einzelmaße (5,2×127,5mm).

Backup vor allen Excel-Änderungen dieser Sitzung:
`C:\Users\SMI\Backups\dbacs\excel\
ga_komponenten_vor-doppelstock-cpudropdown-klemmenfarbe_*.xlsx`.
Katalog danach 131 Bauteile, keine doppelten `artikel_nr` (per Skript
geprüft).

## Gesperrte Entscheidungen

Diese Punkte wurden bereits ausführlich diskutiert und entschieden – nicht neu aufgreifen. **Archiv-Hinweis (07.08.2026):** ältere, sehr ausführliche Session-Protokolle wurden zu kompakten Ergebnis-Zusammenfassungen eingedampft (Volltext inkl. Nutzer-Funden/verworfenen Zwischenständen/Verifizierungsdetails liegt in `docs/archiv/claude-md-modul4-sessions-20-29.md` und `docs/archiv/claude-md-modul4-sessions-30-34.md`) – Grund: `CLAUDE.md` wird bei jeder Sitzung vollständig geladen, unabhängig vom Umfang der Aufgabe. Bei künftigen sehr langen Session-Nachträgen ebenso verfahren: verbindliche Regel kompakt in `CLAUDE.md`, ausführliche Vorgeschichte ins Archiv.

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

### Baugruppen-Schema: DIN-276-basierte ID + Feld-Korrektur (Session 37, gesperrt)
Nutzer will die textbasierte `id` in `baugruppen.json` (z. B.
`luefter_1stufig_2kw`) mittelfristig durch ein eindeutiges, kodiertes
Zahlenschema ersetzen, da mit wachsender Katalogzahl zu viele nah beieinander
liegende Text-Ids entstehen. **Zweistufig umgesetzt: Session 37 korrigiert
nur die Feld-STRUKTUR (Excel-Header, Skript, Modul 7), die eigentliche
Inhalts-Migration (neue Id-Werte, `gewerk` auf DIN-276-Codes umstellen,
Modul-4-Tabs anpassen) ist bewusst ein separater Folge-Schritt** –
ausdrücklicher Nutzerwunsch: „Bevor die Excel Tabelle inhaltlich geändert
wird, sollten wir die Felder darin korrigieren."

**Ziel-ID-Schema (vereinbart, noch nicht angewendet):**
`<3-stelliger DIN-276-Gewerke-Code>_<6-stellige fortlaufende Nummer je
Gewerke-Gruppe>`, z. B. `480_000001`. DIN-276-Codes:
```
410 Sanitär                                  445 Beleuchtungsanlagen
420 Wärmeversorgungsanlagen                  450 Informations-/Sicherheitstechnik
430 Raumlufttechnische Anlagen                460 Aufzugsanlagen
434 Kältetechnische Anlagen                   470 Nutzungsspezifische Anlagen
440 Elektroanlagen                            480 Gebäudeautomation
                                               490 Sonstige Anlagen
```
Die 6-stellige Nummer zählt **pro Gewerke-Gruppe** separat hoch (nicht global).

**In dieser Session bereits korrigiert (Feld-Struktur, `baugruppen`-Sheet):**
- Excel-Header umbenannt: `funktionsbereiche` → `funktionsbereich` (Spalte E),
  `automationsfunktionen` → `automationsanbindung` (Spalte G) – via openpyxl
  direkt in `ga_komponenten.xlsx` geschrieben (Lockdatei vorher geprüft,
  keine gehalten). Bestehende Zellwerte unverändert (Spalte G war und ist
  bei allen 15 Zeilen leer).
- `xlsx_to_json.py` `export_baugruppen()`: `funktionsbereich` jetzt einzelner
  Klartext-String (kein Komma-Split mehr zu einem Array – ergab beim
  bisherigen `funktionsbereiche` ohnehin immer genau 1 Wert, deckungsgleich
  mit `gewerk`). `automationsanbindung` jetzt Boolean nach demselben Muster
  wie bei `einzelbauteile.automationsanbindung` (`if rec.get(...): entry[...]
  = True`, Feld fehlt komplett wenn falsy – keine Sonderbehandlung, exakt
  dieselbe Semantik: „wird zur Laufzeit ausgewertet, ob DDC/Automation für
  dieses Objekt berücksichtigt werden muss" – vom Nutzer für beide Ebenen
  (Einzelbauteil UND Baugruppe) explizit bestätigt).
- `data/baugruppen.json` neu exportiert (`funktionsbereiche:[...]` →
  `funktionsbereich:"..."` bei allen 15 Einträgen, `automationsanbindung`
  bei keinem Eintrag gesetzt, da Excel-Spalte durchgehend leer war).
- Modul 7 `FIELD_DEFS_BG` an die neuen Feldnamen/Typen angepasst
  (`funktionsbereich` als einfacher Text statt `v.join(', ')`,
  `automationsanbindung` als Ja/Nein wie bei den Einzelbauteil-Feldern).
- `gewerk`-Spalte selbst **unverändert** (Name UND Werte) – Skript behandelt
  sie ohnehin nur als reinen Text-Durchreicher, keine Anpassung nötig, bis
  die Werte inhaltlich auf DIN-276-Codes umgestellt werden.
- Geprüft: Modul 4 funktioniert unverändert (`filterBaugruppen()` matcht
  weiterhin korrekt auf die bestehenden `gewerk`-Textwerte, da diese noch
  nicht migriert sind); Modul 7 zeigt `funktionsbereich`/`automationsanbindung`
  korrekt im Detail-Panel, alte Feldnamen tauchen nirgends mehr auf.

**Vom Nutzer für den Folge-Schritt (Inhalts-Migration) bereits entschieden,
hier nur dokumentiert – NICHT in dieser Session umgesetzt:**
- `gewerk` wird künftig direkt der numerische DIN-276-Code als Text (z. B.
  `"430"`), nicht mehr ein Kurzname wie `"lueftung"`.
- Modul 4s Funktionsbereich-Tabs werden auf die 11 DIN-276-Kategorien
  angeglichen (neue Tabs „Aufzug" (460) und „Sonstige" (490) ergänzen).
- **Offene Detailfrage, noch nicht vom Nutzer entschieden:** wie sich die
  bestehenden 10 Funktionsbereich-Tabs (`schaltschrank, automation, elektro,
  beleuchtung, netzwerk, lueftung, heizung, kaelte, sanitaer,
  nutzungsspezifisch`, Session 24) exakt auf die 11 DIN-276-Codes abbilden:
  (a) 450 „Informations-/Sicherheitstechnik" hat keine eindeutige
  Entsprechung – am ehesten `netzwerk`, aber nicht vom Nutzer bestätigt;
  (b) der bestehende Tab `schaltschrank` hat KEIN DIN-276-Äquivalent (DIN 276
  kennt keine eigene „Schaltschrank"-Anlagengruppe) – unklar ob er als
  zusätzlicher Nicht-DIN-Tab bestehen bleibt oder entfällt. Vor Umsetzung
  der Modul-4-Tab-Angleichung mit dem Nutzer klären.
- **Sobald `gewerk` auf DIN-276-Codes umgestellt wird, muss `filterBaugruppen()`
  in Modul 4 zwingend auf `b.funktionsbereich` statt `b.gewerk` umgestellt
  werden** (Reihenfolge wichtig!) – sonst zeigen alle Tabs plötzlich 0
  Treffer, weil die Tab-Buttons weiterhin Text-Keys wie `data-gewerk="lueftung"`
  gegen dann-numerische `gewerk`-Werte matchen würden. `funktionsbereich`
  ist laut Nutzer explizit „der Klartext zum Gewerk als Zahl... in den
  Filterbuttons von Modul 4" – d. h. der stabile, für die UI-Filterung
  vorgesehene Text-Key, unabhängig vom numerischen `gewerk`-Code.
- ~~Migration der bestehenden 15 `id`-Werte auf das neue Schema + Anpassung
  der zugehörigen `bg_id`-Referenzen in `baugruppen_bauteile`~~ ✅
  abgeschlossen Session 38, siehe unten.

### Modul 4 – Klemmleisten: reale mm-Breite statt TE-Rundung (Session 51, gesperrt)
Nutzer-Fund: „Das müsste bei einem Standschrank deutlich mehr sein" – in einem
Test passten nur 17 Datenpunkte (34 Klemmen) in eine Klemmenreihe, obwohl die
Zeile physisch deutlich mehr Platz hatte. Ursache: `eb.te_breite =
ceil(b_mm/18)` (xlsx_to_json.py, seit Session 20 für ALLE Bauteile einheitlich
berechnet) rundet eine reale 5,2mm breite Phoenix-Contact-PT-2,5-Klemme auf
eine volle 18mm-TE-Einheit auf – korrekt für Hutschienengeräte in
`leist`/`steuer` (Schütze, Relais, TXM-Module werden tatsächlich in
TE-Vielfachen gefertigt, `placeInBands()` bleibt daher unverändert TE-basiert),
aber falsch für Reihenklemmen, die lückenlos ohne TE-Raster aneinandergereiht
werden. Eine 549mm breite Klemmenreihe bot dadurch nur Platz für
`floor(549/18)=30` TE-Einheiten statt der real möglichen `549/5,2≈105`
Klemmen – Faktor 3,5 Verlust, unabhängig von Zeilenanordnung/-position. Kein
zusätzlicher Zwischenraum zwischen Klemmen war jemals vorgesehen oder
eingerechnet (auf Nutzer-Rückfrage geprüft) – reines Rundungsproblem.

**Fix, beschränkt auf `placeInKlemmRow()` + `redistributeKlemmBands()`**
(also alle Zonen, die 1-Hutschienen-Klemmleisten modellieren: `klemm_e`,
`uss`, `klemm_l`, `klemm_f`, `klemm_s`, sowie `evert` MIT Schienensystem) –
`placeInBands()` (leist/steuer, echte modulare TE-Geräte) bewusst
unverändert gelassen, kein pauschaler Umbau:
- Geräte-Objekte tragen jetzt zusätzlich `b_mm` (reale Katalogbreite, siehe
  `buildQueues()` alle drei Push-Stellen + `autoDev()`), `te` bleibt
  weiterhin für die (unveränderten) Band-Zonen erhalten.
- `placeInKlemmRow()`: Breitenprüfung/-fortschritt läuft jetzt direkt in mm
  (`col + d.b_mm > band.w_mm`) statt in TE-Einheiten; `mm_used` ergibt sich
  direkt aus der Summe der platzierten `b_mm`-Werte statt `te_used*TE_MM`.
  Fällt auf `(d.te||1)*TE_MM` zurück, falls `b_mm` ausnahmsweise fehlt (keine
  Datenlücke soll zum Absturz führen).
- `redistributeKlemmBands()`: Bedarfsberechnung (`demandMM`) summiert jetzt
  ebenfalls reale `b_mm`-Werte statt `te*TE_MM`.
- SVG-Rendering (`row.blocks.forEach`): unterscheidet jetzt `row.mode==='klemm'`
  (nutzt `blk.col`/`blk.b_mm` direkt in mm) von Band-Zeilen (weiterhin
  `blk.col*TE_MM`/`blk.te*TE_MM`) – dieselbe Skalierungsvariable `sc` (aus
  Modul 3s Montagebereich-Maßen, siehe `buildSVG()`) bleibt für beide Modi
  identisch, keine separate/abweichende Skalierung.
- `te_belegt`/`totalDemandTe` (reine Anzeige-Badges „N TE ·") bewusst NICHT
  angefasst – für Klemmen war `te_breite` ohnehin immer genau 1, der Wert
  entspricht dort weiterhin schlicht der Stückzahl, keine Fehlinformation.

Verifiziert direkt im Browser (Standschrank 699×1499mm, `klemm_f`-Zone
549mm breit, 100× Baugruppe „Binäreingang (BI) auf Klemmleiste" = 200
Klemmen angefordert): korrekt 104 Klemmen platziert (`mm_used=540,8mm` =
104×5,2mm exakt), Positionen bei 0/5,2/10,4/...mm lückenlos, kein
Overflow, Füllstand-Anzeige zeigt realistische 99% statt vorher weit zu
früh „voll". Keine Konsolenfehler, keine Regression bei `leist`/`steuer`
(weiterhin TE-basiert, unverändert getestet).

**Nutzer-Gegenprüfung (eigene Recherche):** „Je nach Klemmenbreite passen bis
zu 160 Klemmen in eine komplette Reihe. Bei Klemmen bis 4mm² etwas mehr als
100" – deckt sich mit dem obigen Testergebnis (104 Klemmen bei 5,2mm-PT-2,5-
Klemmen, Querschnitt bis 4mm²) und bestätigt damit unabhängig sowohl die
korrigierte Platzierungslogik als auch den Katalog-Breitenwert (`b_mm=5,2`).

### Katalog-Korrektur: falsche CPU-Baureihe – PXC4.E16 (Kompakt) → PXC7.E400.A (Modular) (Session 50, gesperrt)
Nutzer-Fund direkt nach dem Testen der Automationsgruppen-Logik: „Ich glaube in
der Excel Tabelle ist die falsche CPU gesetzt... Die aktuell gesetzte ist eine
Kompakt CPU mit Datenpunktanschlüssen. Wenn wir aber unsere Konfiguration mit
frei konfigurierbaren E/A Modulen nehmen, kann die CPU nur Datenpunkte
verwalten, bis ihre Datenpunktgrenze erreicht wird. Der eigentliche Verbrauch
entsteht an den E/A Modulen." Recherche bestätigt: Siemens führt Desigo PX in
zwei parallelen, nicht austauschbaren Baureihen – **Kompakt** (`PXC4.E16`,
`PXC5.E24`, ...: eigene Onboard-E/A fest am Gerät, zusätzlich per TXM
erweiterbar) und **Modular** (`PXC7.E400.A`, Datenblatt A6V12957866, Stand
2026-04-03, Order-Nr. S55375-C114, explizit „Modular Automation Station"
geführt: **„Number of inputs/outputs (Onboard): 0"** – ausschließlich über
Island-Bus mit TX-I/O-Modulen verbunden, bis zu 64 TXM-Module / 500
Datenpunkte gesamt). Der bisher katalogisierte `PXC4.E16` war die falsche,
weil onboard-behaftete Baureihe – widerspricht DBACS' durchgängigem Prinzip
„Verbrauch entsteht ausschließlich an separat platzierten TXM-Modulen".
**Ähnlich benannte `PXC5.A`-Baureihe geprüft und verworfen** (eigenes
Datenblatt A6V14319960): trotz „.A"/"Modular"-Namensmuster tatsächlich
weiterhin eine Kompaktstation mit 24 Onboard-Punkten (Typenbezeichnung im
Datenblatt selbst: „PXC5.E24.A Compact 24pt") – nur `PXC7.A` ist in der
aktuellen (3.) Siemens-Generation die echte Nullkomponenten-Variante.

**Korrektur direkt im bestehenden Katalogeintrag** (nicht als neue Zeile
+ Deaktivierung – der alte Eintrag war ein reiner Auswahlfehler, keine
gültige Alternative, siehe Session-41-Präzedenzfall PXA30-x):
`artikel_nr` `PXC4.E16`→`PXC7.E400.A`, `h_mm` 124→90 (b_mm bleibt 198,
korrekte Maße direkt aus der bemaßten Gehäusezeichnung des Datenblatts,
über den dort ebenfalls bemaßten TXM-Modul-Abstand von 64mm/Modul gegen
die bereits katalogisierten TXM-Maße plausibilisiert), `dp_bo` (4, von den
4 Onboard-Relais des PXC4.E16) entfernt – die neue CPU liefert keinerlei
physische Datenpunktkapazität mehr selbst, `max_ea_module` 4→**64**,
`feldbus_protokoll` `modbus_rtu,modbus_tcp`→**`modbus_rtu`** (Modbus TCP im
PXC7.E400.A-Datenblatt nicht erwähnt, nur Modbus RTU über die 4
EIA-485-Schnittstellen – bewusst nicht unbestätigt übernommen), `preis_eur`
entfernt (der bisherige Preis war zum falschen Gerät recherchiert; für
PXC7.E400.A selbst kein Händlerpreis gefunden, nur für die ältere,
nicht-modulare Schwestervariante PXC7.E400M/-S – nicht übertragen).
Referenz in der Baugruppe „Automationsstation (AE)" (`480_000007`,
`baugruppen_bauteile`) sowie deren Beschreibungstext nachgezogen.

**Auswirkung auf die Session-50-Automationsgruppen-Logik:** rein
datengetrieben, kein JS-Codewechsel nötig – `max_ea_module` wird bereits
generisch aus dem Katalogeintrag gelesen (`buildQueues()`), die
Kapazitätsgrenze für „wann beginnt eine neue Gruppe" springt dadurch
automatisch von 4 auf 64 E/A-Module je Automationsstation. `dp_bo`-Wegfall
bedeutet: `dpSupply` erhält keinen physischen Beitrag mehr direkt von der
CPU – ausschließlich TXM-Module liefern jetzt Kapazität, exakt wie vom
Nutzer gefordert. Verifiziert direkt gegen die exportierte
`einzelbauteile.json`: `PXC4.E16` kommt im Katalog nicht mehr vor, neuer
Eintrag trägt alle elf oben genannten Felder korrekt, kein verwaistes
`preis_eur`/`dp_bo`. Backup vor der Korrektur:
`C:\Users\SMI\Backups\dbacs\excel\
ga_komponenten_vor-cpu-korrektur-pxc7_*.xlsx`.

### Katalog: alle Desigo-PX-CPU-Typen aufgenommen, explizite CPU-Auswahl für Auto-Ergänzung (Session 50, gesperrt)
Direkte Fortsetzung der PXC4.E16→PXC7.E400.A-Korrektur, Nutzer-Auftrag: „Nehme
alle CPU-Typen in die Artikeldatenbank auf (mit Maßen für die Platzierung).
Nutze für die Konfiguration mit E/A Modulen die richtige CPU." Zwei weitere
CPU-Typen recherchiert und ergänzt (beide Siemens-Originaldatenblätter, aktuelle
".A"-Generation):
- **`PXC4.E16.A`** (Order-Nr. S55375-C126, Datenblatt A6V12957862): Kompakt,
  16 Onboard-Punkte (12 universell + 4 Relais), bis zu **2** TX-I/O-Module
  (32 weitere Punkte), max. 48 gesamt. Maße 198×90mm (B×H).
- **`PXC5.E24.A`** (Order-Nr. S55375-C120, Datenblatt A6V14319960): Kompakt,
  24 Onboard-Punkte (2 Digitaleingänge + 8 universelle + 8 super-universelle
  Ein-/Ausgänge + 6 Relais), bis zu **6** TX-I/O-Module (96 weitere Punkte),
  max. 120 gesamt. Maße 270×90mm (B×H). **Namens-Falle:** trägt zwar dasselbe
  „.A"-Suffix wie das echte modulare `PXC7.E400.A`, ist aber laut eigenem
  Datenblatt weiterhin explizit „PXC5.E24.A **Compact** 24pt" – keine
  Nullkomponenten-Variante. Das „.A"-Suffix kennzeichnet bei Siemens offenbar
  nur die aktuelle (3.) Hardware-/Firmware-Generation, nicht automatisch
  „modular" – vor jeder künftigen CPU-Ergänzung den tatsächlichen
  Onboard-E/A-Wert im Datenblatt prüfen, nicht vom Namensmuster ableiten.
- Beide wie beim bestehenden `PXC4.E16`-Vorgänger-Muster: nur die FEST
  zugeordneten (nicht-universellen) Punkte als `dp_bi`/`dp_bo` erfasst
  (PXC4.E16.A: `dp_bo=4`; PXC5.E24.A: `dp_bi=2`, `dp_bo=6`) – die universellen
  Kanäle bleiben bewusst unmodelliert (Feldstruktur bildet flexible Kanäle
  nicht ab, siehe Session 41-Konvention bei `TXM1.8U`). Beide bekommen
  ebenfalls `ddc_netzteil_artikel_nr`/`ddc_sicherung_artikel_nr` (dieselben
  Artikel wie bei `PXC7.E400.A`) und ein `max_ea_module`-Limit, sind aber NUR
  als eigenständige Katalogoptionen gedacht (falls ein Projekt bewusst eine
  Kompaktstation statt der modularen Lösung einsetzen will) – sie nehmen NICHT
  automatisch an der DDC-Auto-Ergänzung teil, siehe nächster Punkt.
- Kein bestätigter aktueller Herstellerlistenpreis für beide gefunden (nur
  Distributor-Preise zu den jeweiligen ÄLTEREN Vorgänger-Bestellnummern ohne
  „.A"-Suffix, nicht übertragen, siehe Katalog-Freitext).

**Neues Feld `einzelbauteile.auto_ea_cpu`** (Boolean, nur bei `PXC7.E400.A`
gesetzt): seit es mehrere `ddc_cpu`-Einträge gibt, wäre ein einfaches
`EINZELBAUTEILE_DB.find(bauteil_typ==='ddc_cpu')` von der zufälligen
Katalog-Reihenfolge abhängig – hätte im schlechtesten Fall wieder eine
Kompaktstation für die automatische Netzteil→CPU→E/A-Modul-Ergänzung
ausgewählt (genau der Fehler, der gerade erst behoben wurde). `buildQueues()`
sucht jetzt zuerst gezielt nach `auto_ea_cpu===true`, fällt nur mangels
Treffer auf die erste `ddc_cpu` zurück (Schutz gegen versehentlich fehlendes
Flag, kein Totalausfall der Auto-Ergänzung).

Verifiziert direkt im Browser (echte Katalogdaten, 129 Bauteile, 3 CPU-Typen):
`EINZELBAUTEILE_DB.filter(bauteil_typ==='ddc_cpu')` liefert alle drei
korrekt (`PXC7.E400.A` mit `auto_ea_cpu:true`, die beiden Kompaktstationen
ohne); manuelle Baugruppe „Automationsstation (AE)" + 100× Reserve-BI (8
TXM-Module nötig) → alle 8 hängen sich korrekt direkt an die vorhandene
`PXC7.E400.A` an (keine zweite Gruppe, da 8 ≪ 64 Kapazität – Regressionstest
der Session-50-Automationsgruppen-Logik mit dem jetzt realistischen
Kapazitätswert bestanden). Keine Konsolenfehler. Backup:
`C:\Users\SMI\Backups\dbacs\excel\
ga_komponenten_vor-cpu-korrektur-pxc7_*.xlsx` (deckt auch diese Ergänzung ab,
im selben Arbeitsschritt).

### Modul 4 – Manueller Reset der DDC-Watermark (Session 50, gesperrt)
Nutzer-Fund: der Ratchet-Mechanismus (Session 28e – automatisch ergänzte
DDC-Module sinken nie von selbst, siehe `applyDdcWatermark()`) ließ nach
mehreren Testläufen graue „Automatisch ergänzt"-Reste in Belegung und
Schranksicht zurück, die nicht mehr zum aktuellen Bedarf passten – es gab
keine Möglichkeit, diesen Zustand aus der UI heraus zu löschen. Neuer Button
„↺ Zurücksetzen" in der Kopfzeile von `#ddc-auto-liste`, ruft
`resetDdcWatermark()` auf: löscht `ddcWatermark` (In-Memory +
`localStorage['m04_ddc_watermark']`) und berechnet sofort neu. Der
Ratchet-Grundsatz selbst bleibt unverändert (nur ein manueller Ausweg, kein
automatisches Schrumpfen). Verifiziert direkt im Browser: künstlich erzeugter
Watermark-Rest verschwindet nach Klick vollständig, echter (weiterhin
bestehender) Bedarf erscheint unmittelbar danach wieder korrekt – Ratchet
für aktive Bedarfe bleibt funktionsfähig.

### Modul 4 – Automationsstations-Gruppen: Netzteil → CPU → E/A-Module, Kapazitätsgrenze je CPU (Session 50, gesperrt)
Nutzer-Vorgabe (vor dem Commit der Session-49-Reserve-Baugruppen nachgezogen):
„Wenn Du eine Automationsstation hinzufügst, benötigt sie eine Spannungsversorgung
[...]. Das Netzteil für die Automationsstation gehört jedoch in den
Steuerungsteil und immer direkt vor die Automationsstation." Reihenfolge auf
einer Hutschienenreihe: **Netzteil → Automationsstation (CPU) → E/A-Module**,
lückenlos ohne ein anderes Bauteil dazwischen; reicht eine Reihe nicht, läuft
die Gruppe nahtlos in der nächsten weiter. Wird die Herstellerobergrenze an
E/A-Modulen je CPU überschritten, beginnt eine komplett **neue** Gruppe
(eigenes Netzteil + eigene CPU + eigene Sicherung) – „Jede CPU hat ihr
eigenes Netzteil mit zugehöriger Sicherung."

**Excel-Schema erweitert:**
- `einzelbauteile.max_ea_module` (int, nur bei `ddc_cpu`) – Herstellerobergrenze
  E/A-Module je Automationsstation. `PXC4.E16` = 4 (bereits in Session 41 als
  Freitext dokumentiert, jetzt als echtes Datenfeld nachgezogen).
- `einzelbauteile.ddc_netzteil_artikel_nr` / `ddc_sicherung_artikel_nr` (Text,
  nur bei `ddc_cpu`) – welches Netzteil/welche Sicherung diese CPU beim
  automatischen Ergänzen mitbringt. `PXC4.E16` → `2866690` / `5SL6106-7`
  (dieselben Artikel wie in der Baugruppe „Automationsstation (AE)").
- `baugruppen_bauteile.zeilenumbruch_davor` / `neue_gruppe` (Boolean) – die
  JS-Seite (`bt.rowBreak`) existierte bereits seit Session 44/49, die
  zugehörigen Excel-Spalten fehlten aber bisher komplett (totes Feature,
  nie befüllbar). `neue_gruppe` ist neu: erzwingt IMMER eine frische
  Hutschienenreihe (auch wenn die zuletzt erzwungene Reihe noch Platz hätte)
  – nötig, damit eine neue Automationsgruppe nicht am Ende der vorherigen
  weiterläuft, sondern sauber getrennt beginnt.
- Baugruppe `480_000007` „Automationsstation (AE)": Netzteil `2866690`
  Zone-Override `leist`→`steuer` entfernt (Katalog-Default ist bereits
  `steuer`, siehe Session 49 – die damalige „bewusst abweichende"
  Leistungsbereich-Zuordnung war die jetzt korrigierte Fehlannahme).
  Bauteil-Reihenfolge in `baugruppen_bauteile` getauscht: Netzteil VOR CPU
  (Zeile 14/15 der Excel-Verknüpfungstabelle), Netzteil trägt
  `zeilenumbruch_davor=TRUE`+`neue_gruppe=TRUE`, CPU nur
  `zeilenumbruch_davor=TRUE` (hängt sich an die vom Netzteil erzwungene
  Reihe an, erzwingt selbst keine neue). **openpyxl-Falle beim Editieren:**
  `ws.cell(row,col,value=None)` löscht eine Zelle NICHT (der Parameter wird
  bei `None` schlicht ignoriert) – Löschen erfordert `ws.cell(row,col).value
  = None` als separate Zuweisung. Beim ersten Versuch dadurch fälschlich
  `neue_gruppe=True` auf der CPU-Zeile stehen geblieben, im zweiten Anlauf
  korrigiert.

**JS-Logik (`modul-04-innenaufbau/index.html`):**
- `assignDevicesToRows()`: neues `groupStart`-Flag (zusätzlich zu `rowBreak`)
  – verschärft den bestehenden Zwangs-Zeilenumbruch-Mechanismus (Session 28g)
  so, dass sich das Gerät NIE an eine bestehende erzwungene Reihe anhängt
  (selbst bei freiem Platz), sondern immer eine fabrikneue Reihe direkt
  danach erzwingt. Ohne Aufwand für die übrige Zwei-Durchlauf-Logik
  wiederverwendbar, da nur die bestehende `forcedCursor`-Bedingung um
  `!d.groupStart &&` ergänzt wurde.
- `buildQueues()`: `cpuPresent`/`ioPresent` (Booleans, Session 49) zu
  `cpuCount`/`ioUnitsManual` (Mengen) verallgemeinert. Neue
  Automationsgruppen-Bilanzierung: Gesamtbedarf an E/A-Modul-Einheiten
  (`ioUnitsManual` + automatisch berechnete) gegen die verfügbare
  CPU-Kapazität (`cpuCount × max_ea_module`) aufgerechnet – fehlende
  Kapazität wird als `neededExtraCpus` ermittelt, jede davon bekommt ein
  eigenes Netzteil+CPU+Sicherung-Tripel. **Ratchet-Reihenfolge beachten:**
  die Gruppenzahl wird zuerst aus dem AKTUELLEN (ungeratchten) Bedarf
  ermittelt, dann in `ddcAuto.modules` eingetragen und EINMAL gemeinsam mit
  den E/A-Modultypen geratcht (`applyDdcWatermark()`) – die eigentliche
  Platzierung (welche E/A-Einheiten an die bestehende CPU direkt
  anhängen vs. welche in neue Gruppen wandern) wird ERST DANACH aus den
  geratchten (nicht den rohen) Mengen abgeleitet. Fehler im ersten Anlauf:
  Platzierung lief auf den ungeratchten Mengen, wodurch bereits einmal
  benötigte, aber im aktuellen Lauf nicht mehr gebrauchte Zusatzgruppen in
  der Zeichnung verschwanden, obwohl `ddcAuto.modules`/die Stückliste sie
  (korrekt, Ratchet-Prinzip) weiterhin zeigten – im Test gefunden und
  korrigiert, siehe Verifikation unten.
  Push-Reihenfolge in `queues.steuer`: zuerst die E/A-Einheiten, die noch in
  vorhandene (manuelle) CPU-Kapazität passen (`rowBreak`, kein
  `groupStart`), danach je neuer Gruppe Netzteil (`rowBreak`+`groupStart`)
  → CPU (`rowBreak`) → deren E/A-Module (`rowBreak`). Die Sicherung hat
  keine Ordnungsvorgabe und geht unabhängig davon in `queues.evert`.
- Baugruppen-Bauteile (`bt.groupStart`) analog zum bestehenden
  `bt.rowBreak`-Override ausgelesen.

Verifiziert direkt im Browser (Modul 4, echte Katalogdaten, jeweils mit
frisch geleertem `m04_belegung`/`m04_ddc_watermark` vor jedem Testfall):
(1) reiner Auto-Pfad ohne manuelle Automationsstation (5× Reserve-BI) →
korrekt 1× Netzteil+CPU+Sicherung-Gruppe ergänzt, Reihenfolge
NT→CPU→TXM. (2) manuelle Automationsstation-Baugruppe + kleiner Bedarf
(3× BI, passt in die 4er-Kapazität) → keine Zusatzgruppe, E/A-Modul hängt
sich direkt an die vorhandene CPU an. (3) manuelle Automationsstation +
großer Bedarf (100× BI → 8 TXM-Module nötig) → 4 Module hängen sich an die
vorhandene CPU an, danach exakt 1 neue Gruppe (Netzteil→CPU→4 weitere
Module) – mit `calculateFelder()` (Standschrank, `je_feld`) real platziert:
Gruppe 1 in Feld 1 (Typ A), Gruppe 2 startet korrekt ganz am Anfang von
Feld 2 (Typ B), keine Vermischung. (4) Ratchet-Test: Bedarf nach
Gruppe-2-Erzeugung wieder auf 3× BI reduziert → Gruppe 2 bleibt (Ratchet-
Prinzip, Session 28e) bestehen, bis der in derselben Session ergänzte
„↺ Zurücksetzen"-Button (siehe vorheriger Abschnitt) die Watermark gezielt
leert – danach korrekt nur noch der tatsächlich aktuelle Bedarf. Keine
Konsolenfehler in allen vier Testfällen. Backup vor den Excel-Änderungen:
`C:\Users\SMI\Backups\dbacs\excel\
ga_komponenten_vor-automationsgruppen-reihenfolge_*.xlsx`.

### Erste Automations-Baugruppen: "Reserve"-Punkte + CPU-Vervollständigung (Session 49, gesperrt)
Erste inhaltliche Baugruppen seit dem Neuaufbau (Gewerk Automation/480, wie
vom Nutzer priorisiert). Zweck: den Schaltschrank mit vorbereiteten
DDC-Anschlusspunkten ausstatten können, BEVOR das externe Feldgerät bekannt
ist – Nutzer-Vorgabe: „Funktionen, die zur Ausstattung des Schaltschranks
genutzt werden können, wenn die Feldgeräte noch nicht bekannt sind, aber
die Ein- und Ausgänge der DDC schon einmal für einen externen Anschluss
vorbereitet werden sollen."

**Namens-/ID-Konvention (Nutzer bestätigt):** ID fortlaufend je Gewerke-
Gruppe `480_000001`, `480_000002`, … Name-Schema `<Anlagenteil> ·
<Ansteuerung/Ausführung>` – für die generischen Reserve-Punkte angepasst zu
`Reserve · <Datenpunkttyp>` (kein "Anlagenteil" bekannt, das ist ja der
Zweck dieser Baugruppen).

**2 neue Baugruppen:** `480_000001` „Reserve · Binäreingang (BI)" (1×
Klemme PT 2,5 grau `3209510` in `klemm_s`), `480_000002` „Reserve ·
Binärausgang (BO)" (dieselbe Klemme in `klemm_f`) – Zuordnung Ein-/Ausgang
→ Sensoren-/Feldgeräte-Klemmzone folgt der etablierten Konvention (Sensoren
= Messwerte, die die DDC liest; Feldgeräte = Aktoren, die die DDC
ansteuert). `betriebsmittel`-Feld bewusst LEER (Feldgerät ist ja per
Definition noch nicht bekannt – nur "echte" Baugruppen mit bekanntem
Feldgerät bekommen dort einen Wert).

**Neuer Mechanismus: DDC-Datenpunktbedarf je BAUGRUPPEN-VERWENDUNG statt
je Katalogartikel.** Eine Klemme trägt selbst keinen DDC-Bezug (wird ja
auch ganz ohne DDC verwendet) – der Bedarf entsteht erst durch IHRE
VERWENDUNG in genau dieser Baugruppe. Neue optionale Spalten `dp_ai`/
`dp_ao`/`dp_bi`/`dp_bo` in `baugruppen_bauteile` (analog zum bestehenden
`zone`-Override-Mechanismus, Session 22/44), ausgelesen in
`xlsx_to_json.py`s `export_baugruppen()` in die `bt`-Objekte. In Modul 4s
`buildQueues()` überschreibt ein gesetzter `bt.dp_*`-Wert den entsprechenden
Typ am `eb`-Objekt VOR dem `accumulateDp()`-Aufruf (nicht überschriebene
Typen bleiben `eb`-eigen, `automationsanbindung` wird bei jedem Override
implizit auf `true` gesetzt) – bewusst NICHT auf dem Katalogartikel selbst
gesetzt, sonst würde JEDE Verwendung dieser Klemme (auch außerhalb dieser
Baugruppen) fälschlich DDC-Bedarf erzeugen.

**Neuer Mechanismus: automatische CPU-Ergänzung.** Nutzer-Vorgabe: „Wenn
Du ein E/A-Modul setzt, musst du vorher prüfen, ob schon eine CPU gesetzt
wurde. Ist dies nicht der Fall, musst Du sie mit setzen. CPU und E/A-Modul
sind nicht Bestandteile der Baugruppe, sie werden als eigene Bauteile für
den Abschluss der Baugruppe benötigt." Weder CPU noch E/A-Modul stehen in
`bg.bauteile` – beide entstehen ausschließlich über die bestehende
Auto-Ergänzung (`computeDdcAutoModules()`, Session 28d) bzw. die neue
CPU-Ergänzung. `buildQueues()` erfasst beim Durchlaufen der Belegung
`cpuPresent`/`ioPresent` (ist bereits eine `ddc_cpu`- bzw. `ddc_io`-typisierte
Komponente manuell platziert?). Direkt nach `computeDdcAutoModules()` (und
VOR `applyDdcWatermark()`, damit die CPU wie jedes andere Auto-Modul geratcht
wird – einmal ergänzt, fällt sie nicht wieder weg): fehlt eine CPU, obwohl
ein E/A-Modul gebraucht wird (manuell ODER automatisch ergänzt), wird
GENAU EINE `ddc_cpu`-Komponente (`PXC4.E16`, einzige aktuell im Katalog)
automatisch ergänzt – keine Vervielfachung, wie bei `ddc_cpu` ohnehin schon
für die manuelle Auswahl vorgesehen (Session 41).

**Nutzer-Vorgabe zur Modulwahl:** „Verwende als E/A-Modul vorzugsweise das,
welches nur einen Datenpunkttyp abbilden kann, bevor du auf weitere
zugreifst." Bereits durch die bestehende Katalogstruktur sichergestellt,
keine Code-Änderung nötig: nur `TXM1.8D`/`TXM1.16D` (reine BI-Module) und
`TXM1.6R`/`TXM1.6R-M` (reine BO-Module) tragen `dp_bi`/`dp_bo`-Kapazität im
Schema – die Universalmodule `TXM1.8U`/`TXM1.8U-ML` haben bewusst KEINE
`dp_*`-Werte (Session 41: „Feldstruktur bildet flexible Kanäle nicht ab,
offene Modul-4-Erweiterung"), `computeDdcAutoModules()` kann sie über die
bestehende Kapazitätsprüfung gar nicht als Kandidaten sehen. Damit wählt
der bestehende Mechanismus für BI/BO automatisch die Single-Type-Module.
**Für AI/AO existiert aktuell KEIN Katalogartikel mit Kapazität** – ein
"Reserve · Analogeingang/-ausgang" würde daher dauerhaft unerfüllten Bedarf
zeigen. Bewusst noch NICHT angelegt ([[feedback_grundlage_vor_gruppen]]) –
erst ein AI/AO-fähiges Modul recherchieren/ergänzen (oder die
Universalmodul-Kapazitätslücke schließen), dann nachziehen.

Verifiziert direkt im Browser (echte Katalogdaten, `EINZELBAUTEILE_DB`
frisch geladen): beide Baugruppen im „Automation"-Dropdown korrekt
sichtbar; Platzierung beider Klemmen in `klemm_s`/`klemm_f` korrekt;
`buildQueues()` liefert exakt die erwarteten 3 Auto-Geräte
(`TXM1.16D`+`TXM1.6R`+`PXC4.E16`), `ddcSummary` zeigt `dp_bi:{cap:16,used:1}`/
`dp_bo:{cap:10,used:1}` (10 = 6 aus TXM1.6R + 4 aus der CPU eigenen
Relaisausgängen) – korrekt in der Statistik mitgeführt; isolierter
`placeInBands()`-Test bestätigt: alle 3 Auto-Geräte passen bei
ausreichender Kapazität zusammen in ein Band, keine Regression der
bestehenden Platzierungslogik. Bereits vorhandene CPU verhindert
zuverlässig eine zweite automatische Ergänzung (Ratchet-Verhalten wie bei
TXM-Modulen: einmal ergänzt, fällt nicht wieder weg – bestehende,
gewünschte Semantik seit Session 28e). Keine Konsolenfehler. Backup vor
den Strukturänderungen: `C:\Users\SMI\Backups\dbacs\excel\
ga_komponenten_vor-betriebsmittel-feld_*.xlsx` (deckt auch die
dp_ai/ao/bi/bo-Spalten ab, im selben Arbeitsschritt ergänzt).

### Nachtrag 2: AI/AO-Baugruppen, Automationsstation (AE), zwei Bugfixes (Session 49, gesperrt)
Direkte Fortsetzung, gleicher Tag.

**1. BI-Zonenkorrektur (Nutzer-Fund):** „Bei BI: 2 Klemmen in Feldgeräteleiste,
bei BO auch" – Nutzer stellt klar, dass BEIDE Binärtypen in `klemm_f`
(Feldgeräte) gehören, nicht BI in `klemm_s` (Sensoren) wie zuvor
angenommen. `klemm_s` ist damit ausschließlich für ANALOGE Messwerte
reserviert (klassische „Sensoren" wie Temperatur/Druck), `klemm_f` deckt
sowohl einfache Binärsignale als auch Aktor-Ansteuerung ab. `480_000001`
korrigiert (beide Klemmen `klemm_s`→`klemm_f`).

**2. Drei neue Baugruppen nach demselben Schema** (Nutzer-Vorgabe „Klemmleiste
AO=Feldgeräte, Klemmleiste AI=Sensoren"): `480_000004` „Analogausgang (AO)
auf Klemmleiste" (`klemm_f`), `480_000005` „Analogausgang (AO) mit LVB auf
Klemmleiste" (`klemm_f`, `lvb_erforderlich`), `480_000006` „Analogeingang
(AI) auf Klemmleiste" (`klemm_s`) – je 2 Klemmen wie bei BI/BO.

**3. TXM1.8U-Kapazitätslücke geschlossen (Grundlage für 2., musste zuerst
gelöst werden):** `dp_ai=8`/`dp_ao=8` auf `TXM1.8U`/`TXM1.8U-ML` gesetzt
(8 flexible Punkte laut Desigo-Recherche, siehe Nachtrag 1). Dabei einen
echten Unter-Versorgungs-Bug in `computeDdcAutoModules()` gefunden UND
gefixt, BEVOR er in Erscheinung treten konnte: der bisherige Cross-Typ-Abzug
(`PHYS_DP_TYPES.forEach(t=>{if(chosen[t]) remaining[t]-=chosen[t]*menge})`)
war für Module mit GENAU EINEM `dp_*`-Feld harmlos (bisheriger
Katalogbestand), hätte bei einem echten Mehrzweckmodul wie `TXM1.8U`
(dp_ai UND dp_ao gleichzeitig, aber physisch nur 8 GEMEINSAME Kanäle) bei
gleichzeitigem AI+AO-Bedarf, der die 8 Kanäle in Summe übersteigt, zu wenige
Module vorschlagen können (der erste Kauf für einen Typ hätte fälschlich
die VOLLE Kapazität für den anderen Typ "gratis" gutgeschrieben, wodurch ein
zweiter nötiger Kauf unterblieben wäre). Fix: nur noch der gerade bearbeitete
Typ wird abgezogen (`remaining[type] -= chosen[type]*menge`) – für alle
bisherigen Katalogmodule (genau 1 Feld) bytegleich identisches Verhalten,
für Mehrzweckmodule jetzt sicher (kauft im Zweifel ein Modul zu viel statt
zu wenig). Getestet: AI=1+AO=1 (LVB) gemeinsam ergab korrekt `TXM1.8U`(AI)
+ `TXM1.8U-ML`(AO, wegen LVB) – zwei Module statt optimalerweise einem
möglichen, aber NIE zu wenig.

**4. Neue Baugruppe `480_000007` „Automationsstation (AE)"** – Nutzer-Vorgabe:
„Wenn Du eine CPU setzt, dann benötigt sie auch ein Netzteil (Leistung) und
eine Sicherung (Energievert.). Es macht Sinn, dies auch als Baugruppe OHNE
Abgangsklemmleiste zu definieren." Bauteile: `PXC4.E16` (CPU, Standardzone
`steuer`), `2866690` (QUINT-PS 24VDC/2,5A/60W, Zone-Override `leist` –
Katalog-Standardzone ist `steuer`, hier bewusst abweichend gemäß
Nutzer-Vorgabe), `5SL6106-7` (LSS 1-polig 6A, Standardzone bereits `evert`,
passt ohne Override). Bewusste, dokumentierte Annahmen (nicht mit dem
Nutzer einzeln abgestimmt, da unkritisch/üblich): kleinstes verfügbares
Netzteil (60W, weit ausreichend für 1 CPU + einige TXM-Module), kleinste
LSS-Stufe (6A, Standard-Absicherung eines so kleinen Netzteils).

**Notwendiger Begleit-Fix:** `cpuPresent`/`ioPresent` (siehe Nachtrag 1)
wurden bisher NUR im `typ:'einzel'`-Zweig von `buildQueues()` erfasst –
mit der Automationsstation kann eine CPU jetzt auch über eine Baugruppe
kommen. Ergänzt im Baugruppen-Zweig (vor der zone-Prüfung, damit sie auch
bei ungültiger/fehlender Zone erfasst wird) – sonst hätte die Auto-Ergänzung
fälschlich eine ZWEITE CPU addiert, obwohl die Automationsstation bereits
eine mitbringt. Verifiziert: `steuer` zeigt bei gesetzter Automationsstation
`PXC4.E16` exakt einmal, keine doppelte Ergänzung.

**5. Bugfix (Nutzer-Fund): Gewerk-Tab sprang bei jedem Neuladen auf
„Lüftung" zurück.** `setGewerk('lueftung')` war beim Seitenstart fest
kodiert – die Belegung selbst blieb korrekt (localStorage), aber das
`bg_auswahl`-Dropdown zeigte nach einem Reload nur noch Lüftungs-Baugruppen
(aktuell keine), wodurch sich bereits hinzugefügte Baugruppen anderer
Gewerke (z.B. Automation) nicht mehr auswählen und damit über den
„−"-Button nicht mehr entfernen ließen – NICHT über das „×" in der
Belegungsliste, das ist unabhängig vom Dropdown-Zustand und funktionierte
immer schon zuverlässig (zweite, robustere Löschmethode). Fix: `setGewerk()`
persistiert die Wahl jetzt in `localStorage['m04_gewerk']`, beim Start wird
sie wiederhergestellt (`setGewerk(localStorage.getItem('m04_gewerk') ||
'lueftung')`) – konsistent mit dem bereits bestehenden Muster bei
`m04_schrank_typ`. Verifiziert: Tab UND Dropdown-Optionen bleiben nach
Reload korrekt auf „Automation" stehen, „−"-Button funktioniert wieder.

**6. UX-Fix (Nutzer-Fund): „×" in der Belegungsliste bei langen Namen nicht
erreichbar.** Nutzer: „Ich möchte die Spalte aber nicht unnötig
verbreitern. Hier macht ein Scrollbalken Sinn." `.bel-name` kürzte den
Text bisher per Ellipsis (`overflow:hidden;text-overflow:ellipsis`) – bei
sehr langen Baugruppennamen wie „Binärausgang (BO) mit LVB auf
Klemmleiste" wirkte das in der Praxis nicht zuverlässig genug. Fix:
Ellipsis entfernt, `.bel-zeile` bekommt `width:fit-content` (behält ihre
natürliche, ungestauchte Breite), `#belegung-liste` bekommt
`overflow-x:auto` – lange Zeilen erzeugen jetzt einen horizontalen
Scrollbalken statt abgeschnitten zu werden, der „×"-Button bleibt am
Zeilenende immer erreichbar (ans Scroll-Ende scrollen). Spaltenbreite
selbst unverändert, wie vom Nutzer gefordert.

Verifiziert direkt im Browser (echte Katalogdaten): alle 4 neuen
Baugruppen (AO/AO+LVB/AI/AE) einzeln und gemeinsam mit BI/BO getestet –
korrekte Zonen, korrekte Modulwahl (`TXM1.8U` für AI, `TXM1.8U-ML` für
AO+LVB-Bedarf, CPU/Netzteil/Sicherung korrekt in `steuer`/`leist`/`evert`,
keine doppelte CPU), kein Overflow, keine Konsolenfehler in allen
Testläufen. Backup: `C:\Users\SMI\Backups\dbacs\excel\
ga_komponenten_vor-ai-ao-automationsstation_*.xlsx`.

### Nachtrag: BI/BO umbenannt, 2-Klemmen-Korrektur, LVB-Variante + Desigo-AI/AO-Recherche (Session 49, gesperrt)
Direkte Fortsetzung, gleicher Tag. Drei Aufträge in einem Schritt.

**1. Desigo/TX-I/O-Recherche (Original-Datenblätter direkt als PDF-Text
ausgelesen, `pypdf` in WSL nachinstalliert, da `WebFetch`s eigener
Zusammenfasser an den binär-komprimierten Siemens-PDFs scheiterte):**
Kein dediziertes reines AI- oder AO-Modul in der TX-I/O-Familie – nur
Universalmodule. `TXM1.8U`/`TXM1.8U-ML` (bereits im Katalog) bestätigt:
„8 universal I/O points, individually configurable as: Digital input...
Analog input... Analog output" – Mischbetrieb (einige Kanäle AI, andere
AO, gleichzeitig auf demselben Modul) ist laut Originaldatenblatt
ausdrücklich vorgesehen, Anschlussbilder zeigen alle drei Signalarten als
gültige Konfiguration derselben 8 Punkte. Eine in einem KI-Suchergebnis
behauptete Einschränkung („aktive Ein-/Ausgänge auf unterschiedlichen
Modulen") ließ sich in den zwei erfolgreich ausgelesenen Primärquellen
(Datenblatt CM2N8173 + Funktionshandbuch CM110561) **nicht bestätigen** –
bewusst nicht als Fakt übernommen. Neu gefunden: `TXM1.8X`/`TXM1.8X-ML`
„Super universal module" (zusätzlich 4-20mA-fähig, AO nur an Punkten 5-8,
Datenblatt von 2025 – neuer als unser bereits katalogisiertes `TXM1.8U`),
noch nicht im Katalog – erstmal nicht nötig, da DBACS aktuell keine
4-20mA-Sensorik braucht. Analogpunkte brauchen laut Datenblatt je Punkt
eine EIGENE Referenzklemme (anders als Digitaleingänge, die eine
gemeinsame Klemme teilen dürfen) – bestätigt das vom Nutzer vorgegebene
2-Klemmen-Muster auch für die künftigen AI/AO-Baugruppen.

**2. Umbenennung** (Nutzer-Vorgabe, ID unverändert): `480_000001`
„Reserve · Binäreingang (BI)" → **„Binäreingang (BI) auf Klemmleiste"**,
`480_000002` → **„Binärausgang (BO) auf Klemmleiste"**.

**3. 2-Klemmen-Korrektur (Nutzer-Fund: „Nicht eine"):** jede der beiden
Baugruppen hatte bisher nur 1 Klemme – korrigiert auf 2 (Signal PT 2,5
grau `3209510`, trägt den `dp_bi`/`dp_bo`-Override + Referenz/Common PT
2,5 BU blau `3209523`, ohne DDC-Bezug) – entspricht der realen
Verdrahtung (Signal + Bezugspotential) und ist durch die Desigo-Recherche
zusätzlich bestätigt.

**4. Neue Baugruppe `480_000003` „Binärausgang (BO) mit LVB auf
Klemmleiste"** – gleiche 2-Klemmen-Struktur wie die plain-BO-Baugruppe,
zusätzlich `lvb_erforderlich=true` auf der Signal-Klemme.

**Neuer Mechanismus: `lvb_erforderlich`-Override statt eigenem
Datenpunkt-Pool.** Ein separater `dp_bo_lvb`-Pool hätte riskiert, dieselben
physischen Kanäle eines Moduls doppelt zu zählen (ein `TXM1.6R-M` hat 6
Kanäle INSGESAMT, nicht 6 „normale" + 6 „LVB"). Stattdessen: neue optionale
Spalte `lvb_erforderlich` (Boolean) in `baugruppen_bauteile`, in Modul 4s
`buildQueues()` als `needsLvb[type]` (je `PHYS_DP_TYPES`-Typ) erfasst.
`computeDdcAutoModules(demand, supply, reservePct, needsLvb)` schränkt bei
aktivem `needsLvb[type]` die Kandidatenliste auf Module mit
`eb.lvb_integriert===true` ein (Feld existiert bereits seit Session 41) –
die Mengen-Arithmetik bleibt unverändert EIN gemeinsamer `dp_bo`-Pool.
Bewusste Vereinfachung/Kompromiss: sobald IRGENDEIN BO-Punkt im Projekt
LVB braucht, wird der GESAMTE `dp_bo`-Bedarf nur noch über LVB-fähige
Module gedeckt (auch die plain-BO-Anteile) – im Test genügte dafür ein
einziges `TXM1.6R-M` für beide (1 plain + 1 LVB = 2 von 6 Kanälen genutzt),
bei sehr vielen plain-BO-Punkten wäre das teurer als nötig (LVB-Modul
319€ vs. 275€ für plain, aber i.d.R. vernachlässigbar) – bewusst in Kauf
genommen statt eines fehleranfälligeren Doppel-Pool-Modells.

Verifiziert direkt im Browser (echte Katalogdaten, watermark-frisch
zurückgesetzt): alle 3 Baugruppen korrekt im „Automation"-Dropdown; je
Baugruppe exakt 2 Klemmen in der richtigen Zone platziert
(`klemm_s`×2/`klemm_f`×2/`klemm_f`×2); bei allen drei gleichzeitig gesetzt
wählt die Automatik `TXM1.16D`(BI)+`TXM1.6R-M`(BO, wegen LVB-Bedarf
projektweit)+`PXC4.E16`(CPU) – korrekt, `dp_bo used:2/cap:10`; bei NUR
der plain-BO-Baugruppe (Watermark zurückgesetzt) wählt die Automatik
korrekt das günstigere `TXM1.6R` statt der LVB-Variante – Regression
bestätigt. Keine Konsolenfehler. Backup:
`C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-bi-bo-lvb-2klemmen_*.xlsx`.

**Nachtrag, gleicher Tag: Reihenfolge CPU vor E/A-Modulen.** Nutzer-Vorgabe:
„Die CPU (Desigo Automationsstation) soll am Anfang gesetzt werden, die
E/A-Module folgen danach." Vorher landete die automatisch ergänzte CPU
IMMER am Ende von `ddcAuto.modules` (mein Ergänzungscode lief nach
`computeDdcAutoModules()`, `push()` hängt hinten an) – dadurch erschien sie
im `steuer`-Band nach den TXM-Modulen statt davor. Fix: direkt vor dem
`ddcAuto.modules.forEach(...queues.steuer.push...)`-Aufruf ein stabiler
`sort()`, der `ddc_cpu`-Einträge an den Anfang zieht (relative Reihenfolge
der E/A-Module untereinander bleibt unverändert) – robust unabhängig davon,
ob die CPU über meinen expliziten Check oder über `applyDdcWatermark()`s
Ratchet-Mechanismus in die Liste gelangt. Verifiziert: `steuer`-Zone zeigt
jetzt `PXC4.E16` zuerst, danach `TXM1.16D`/`TXM1.6R-M`. Keine
Konsolenfehler.

**Nächster Schritt (vom Nutzer angekündigt):** die analogen Pendants
(Reserve AI/AO) folgen, sobald diese Recherche steht – jetzt erledigt,
Umsetzung als Folgeschritt offen. Kapazitätsmodellierung für das
Universalmodul `TXM1.8U` (flexible Kanäle, keine feste `dp_ai`/`dp_ao`-
Aufteilung) bleibt die bereits in Session 41 dokumentierte offene Lücke –
muss vor den AI/AO-Baugruppen geklärt werden ([[feedback_grundlage_vor_gruppen]]).

### Modul 4 – Baugruppen-Zusammenhalt über Zonen hinweg (Session 49, gesperrt)
Start des Baugruppen-Neuaufbaus (`baugruppen.json` seit Session 40 leer).
Nutzer-Vorgabe vor jeder inhaltlichen Baugruppen-Arbeit: „In der Praxis
werden zum größten Teil Baugruppen gesetzt, Einzelbauteile nur ergänzend."
Eine Baugruppen-Instanz mit Bauteilen in mehreren Zonen (z. B. Schütz in
`leist` + Abgangsklemme in `klemm_l`) muss deshalb **immer gemeinsam in
einem Feld** landen – die Bauteile werden untereinander verdrahtet, ein
Aufteilen auf zwei Schaltschrankfelder ergibt elektrisch keinen Sinn. Die
bisherige Architektur (`queues[zone]` je Zone unabhängig, Session 48)
konnte das nicht garantieren.

**Lösung „Reservierung vor Commit" pro Instanz:** Baugruppen-Bauteile
landen nicht mehr flach in `queues[zone]`, sondern bleiben in
`bgInstanceQueue` (neu, aus `buildQueues()`) als zusammenhängende Einheit
`{bg_id, ci, zonen:{zone:[device,...]}}` erhalten. Neue Funktion
`platziereBaugruppenFuerFeld()` prüft pro Feld für jede Instanz (FIFO,
kein Vorbeispringen – analog zur bereits akzeptierten Bin-Packing-
Einschränkung bei Einzelbauteilen) per Dry-Run, ob ALLE ihre Zonen noch
Platz haben: `placeInBands()`/`placeInKlemmRow()` sind bereits reine
Funktionen von `(devs, bands, ...)` und melden über `leftoverDevs`, was
nicht mehr passte – ruft man sie mit „bereits bestätigte Geräte + neue
Instanz-Geräte" auf, zeigt ein nicht-leeres `leftoverDevs` zuverlässig,
dass die neuen Geräte nicht passen. Kein Umbau der Reihen-/Bandlogik
nötig. Schlägt IRGENDEINE Zone der Instanz fehl, wird NICHTS von ihr
committed (kein Partial-Commit, auch nicht in Zonen, die für sich allein
gepasst hätten) – die komplette Instanz wandert unverändert ins nächste
Feld. `placeBauteileForField()` platziert bestätigte Baugruppen-Geräte
VOR den Einzelbauteilen derselben Zone (`confirmedBg[zone].concat(queues[zone])`
– Reihenfolge laut Nutzer unkritisch, da Baugruppen praktisch dominieren).
`redistributeKlemmBands()` (Breiten-Umverteilung Klemmleisten) und
`totalDemandTe`/`restOf()` (Füllstand-Anzeige, Folgefeld-Steuerung) zählen
jetzt zusätzlich zu `queues[zn]` auch offene `bgInstanceQueue`-Einträge
mit, sonst würden Baugruppen-Bedarf/Reserve-Umverteilung unterschätzt
bzw. ein nötiges Folgefeld ausbleiben.

**Nachtrag, gleiche Sitzung – Korrektur „Zonen aus unterschiedlichen
Feldtypen" ist kein Randfall, sondern der Normalfall bei Automation:**
Nutzer-Einwand anhand eines konkreten Beispiels (DDC-angesteuerte Pumpe):
Schütz + Abgangsklemme gehören ins Leistungsfeld (Feldtyp D), das
zugehörige DDC-E/A-Modul (inkl. ggf. weiterer Rückmeldungen der Pumpe)
gehört ins Steuerungsfeld (Feldtyp E) – bei `getrennt_els` sind das zwei
verschiedene physische Felder, verbunden über normale Feld-zu-Feld-
Querverdrahtung. Die ursprüngliche Regel „alle Zonen einer Instanz müssen
im selben Feldtyp liegen, sonst wird die Instanz gar nicht erst
betrachtet" hätte genau diesen (in der Automationstechnik alltäglichen)
Fall NIE platziert – sie wäre in keinem Feldtyp je als „relevant"
erkannt worden.

**Korrigierte Regel: Zusammenhalt gilt pro (Instanz × Feldtyp), nicht für
die ganze Instanz.** `platziereBaugruppenFuerFeld()` behandelt jetzt nur
die Teilmenge der Zonen einer Instanz, die zum aktuellen Feldtyp gehören,
als atomare Einheit; committete Zonen werden aus `inst.zonen` gelöscht
(`delete`), die Instanz bleibt mit ihren restlichen Zonen in
`bgInstanceQueue` stehen und wird erst entfernt, wenn wirklich alle ihre
Zonen platziert sind. Dadurch landen Schütz+Klemme atomar zusammen in
einem D-Feld, das DDC-Modul unabhängig davon (ggf. in einem anderen Feld)
atomar für sich in einem E-Feld – beides korrekt, da eine Querverdrahtung
zwischen zwei bereits als separate Felder geplanten Bereichen ohnehin
normale Praxis ist. Bei `1feld`/`je_feld`/`einsp_misch` (Feldtyp A/B
decken `leist` UND `steuer` gemeinsam ab) ändert sich nichts – dort sind
ohnehin immer alle Zonen einer Instanz im selben Feldtyp, die neue Regel
verhält sich dort identisch zur alten.

Verifiziert direkt im Browser (synthetische Testbaugruppen, nicht
committet): (1) isolierter Test von `platziereBaugruppenFuerFeld()` –
5 Instanzen mit knapper Höhenkapazität, korrekt 2 bestätigt/3 zurückgestellt;
zweiter Test beweist Cross-Zonen-Zusammenhalt INNERHALB eines Feldtyps
(eine Instanz, deren `leist`-Zone allein gepasst hätte, wird trotzdem
NICHT committed, weil ihre `klemm_l`-Zone keinen Platz mehr hatte – kein
Partial-Commit); dritter Test (Nachtrag) beweist die Feldtyp-Domänen-
Trennung direkt: nach einem D-Feld-Aufruf bleibt die Instanz mit nur noch
`steuer` in der Queue, nach einem folgenden E-Feld-Aufruf ist sie
vollständig entfernt. (2) Echte Mehrfeld-Pipeline (`je_feld`, Standschrank
400×900mm synthetisch) mit 40 Baugruppen-Instanzen über 4 Felder: in
JEDEM Feld exakt gleich viele `leist`- wie `klemm_l`-Blöcke, nie eine
Instanz gesplittet, 40/40 platziert. (3) Regression reine Einzelbauteile
(60× Testklemme über 6 Felder): 60/60 platziert, unverändert. (4)
Mischbetrieb Baugruppen+Einzelbauteile: Baugruppen zuerst, Einzelbauteile
füllen den Rest. (5) Nachtrag – echte DDC-Pumpen-Baugruppe (`getrennt_els`,
15 Instanzen mit Schütz+Klemme+DDC-Modul): 2× Feldtyp D (11+4, `leist`=
`klemm_l` in jedem Feld) + 1× Feldtyp E (alle 15 DDC-Module zusammen),
15/15/15 vollständig platziert. Keine Konsolenfehler in allen Testläufen.

### Modul 4 – Link zurück zu Modul 3 unter der Belegung (Session 48 Nachtrag 7, gesperrt)
Nutzer-Vorgabe direkt im Anschluss an Nachtrag 6: „Kannst Du unter dem Feld
Belegung noch ein Zurück-zu-Modul-3-Link erstellen, wie du es bereits in
Modul 3 getan hast. Die kann besser genutzt werden, wenn aufgrund der
Belegung ein anderes Modell gewählt werden soll." Modul 3 hat bereits
`gotoParentModul()`/`btn-goto-modul` (verzweigt je nach `schrank_typ` auf
Modul 1 oder 2) – Modul 4 bekommt das Analogon für den eigenen Vorgänger.

Neue Funktion `gotoModul3()` (keine Fallunterscheidung nötig, da Modul 3
für Wand- UND Standschrank derselbe gemeinsame Vorgänger ist – anders als
Modul 3s Verzweigung auf Modul 1/2). Button `<button class="btn-print
btn-nav" onclick="gotoModul3()">← Zurück zu Modul 3 · Architektur</button>`
direkt unter `#belegung-liste`/`#ddc-auto-liste` im linken Panel
(`.panel-in`) platziert – exakt an der Stelle, an der der Nutzer nach dem
Sichten der Belegung/Platzierung entscheidet, ob die Modul-3-Konfiguration
(Feldanzahl, Anordnung, Schienensystem etc.) angepasst werden muss. Neue
CSS-Klasse `.btn-nav` 1:1 aus Modul 2/3 übernommen (grüner Rahmen/Text,
Hover-Invertierung). Ergänzt den bereits bestehenden, aber weniger
prominent platzierten Footer-Link „← Modul 3 · Zonenaufteilung" – bewusst
kein Duplikat-Problem, sondern zwei unterschiedliche Zugriffspunkte
(Footer = generische Modulübersicht, neuer Button = kontextbezogen direkt
bei der Belegung).

Verifiziert direkt im Browser: Button erscheint korrekt unter der
Belegungsliste, `gotoModul3()` navigiert zu `../modul-03-architektur/`,
keine Konsolenfehler.

### Mehrfeld-Schaltschränke Nachtrag 6: Feld-/Tür-Kacheln ohne toten Rand (Session 48, gesperrt)
Direkte Fortsetzung von Nachtrag 5, gleicher Tag – Nutzer-Fund per Screenshot:
die Schranksicht-Kacheln sind deutlich breiter als die eigentliche
Schaltschrank-Zeichnung (viel ungenutzter dunkler Rand links/rechts pro
Kachel), während die Türansicht schon bei nur einem Feld gescrollt werden
muss. Nutzer-Vermutung: bis zu 6 Kacheln (bzw. 3 Felder + zugehörige Türen)
sollten ohne Scrollen passen. Ausdrückliche Vorgabe: „Achte darauf, dass du
nicht die Geometrie der Schränke selbst veränderst – reduziere einfach den
Rand bis zur Kachel."

**Root Cause 1 (toter Rand):** `.feld-svg-wrap`/`.feld-tuer-wrap` sind
bewusst großzügig bemessen (`flex:1 0 260px`), DAMIT `buildSVG()`/
`buildTuerAnsicht()` beim Messen von `wrapEl.clientWidth` genug Breite
vorfinden und der Maßstab zuverlässig von der Höhe bestimmt wird
(Nachtrag-2-Fix „verlässt den Maßstab"). Bei den meist hochformatigen
Schaltschränken bestimmt aber ohnehin die Höhe den Maßstab (`sc =
min(availW/b, availH/h)`, Höhe ist der bindende Faktor) – die vom
Flex-Grow zugewiesene Extra-Breite bleibt ungenutzter Rand um die
Zeichnung. **Fix:** neue Funktion `schrumpfWrapAufInhalt(wrap)`, aufgerufen
NACH dem Zeichnen (Maßstab bereits fest in den SVG-Attributen `width`/
`height` verankert) – setzt `wrap.style.flex` exakt auf die gerenderte
SVG-Breite + 2px (Rahmen). Ändert NICHTS am Maßstab (der ist zu diesem
Zeitpunkt schon fest), entfernt nur den ungenutzten Rand der Kachel selbst.

**Root Cause 2 (Tür-Zeile hart auf 260px gedeckelt):** `.tueren-row` hatte
`flex:0 0 260px` – die GESAMTE Tür-Reihe (nicht nur eine Kachel) war fix auf
260px begrenzt, unabhängig davon wie viele Tür-Kacheln tatsächlich
gezeichnet werden. Fix: `flex:1 1 auto` (wie `.felder-row`).

**Root Cause 3 (dabei aufgedeckt, vorbestehend):** `.panel-mid` und
`.schrank-views-row` hatten kein `min-width:0` – als Grid- bzw. Flex-Item
greift ohne dieses der CSS-Default `min-width:auto`, wodurch die Spalte/
Zeile NICHT unter die Summe ihres Inhalts schrumpfen kann. Bei vielen
Feldern (im Test 10) sprengte das den gesamten mittleren Grid-Bereich über
die Fensterbreite hinaus (`.layout-3col` überlief seitlich, `<body>` bekam
einen Scrollbalken) STATT dass `.felder-row`s eigenes `overflow-x:auto`
griff. Fix: `min-width:0` auf `.panel-mid`, `.schrank-views-row` und
`.tueren-row` ergänzt (`.felder-row` hatte es schon).

**Root Cause 4 (dabei aufgedeckt beim Beheben von Root Cause 3):**
`.felder-row{flex:1}` bedeutet `flex-basis:0%` – als `.tueren-row` (damals
`flex:0 1 auto`, Basis = tatsächliche Inhaltsbreite) bei vielen Tür-Kacheln
allein schon mehr Platz beanspruchte als der Container hatte, ging die
GESAMTE verfügbare Breite an `.tueren-row` (Basis>0 kann schrumpfen,
Basis=0% hat nichts zum Schrumpfen), `.felder-row` kollabierte auf 0px
Breite. Fix: beide Reihen auf `flex:1 1 auto` (gleiche Basis-Art) –
verfügbare Breite wird jetzt proportional zum tatsächlichen Platzbedarf
beider Reihen aufgeteilt (mehr Felder → mehr Platz für Felder, mehr
Türbauteile → mehr Platz für Türen), überschüssiger Inhalt scrollt in der
jeweils eigenen Reihe statt die andere zu verdrängen oder die Seite zu
sprengen.

Verifiziert direkt im Browser (1920×1080, Standschrank mit TXM1.16D-Modulen
+ Hauptschalter-Türbauteilen): Einzelkachel-Breite sank von 258px auf
164–181px (exakt an den SVG-Inhalt angepasst, `wrapWidth === svgWidth`);
3 Felder + 3 zugehörige Türen (6 Kacheln) passen bei 1920px vollständig
ohne jedes Scrollen (`felderRowScrollW === felderRowClientW`); Stresstest
mit 10 Feldern erzeugt korrekt internes Scrollen NUR innerhalb der
jeweiligen Reihe, kein Seiten-Overflow mehr (`body.scrollWidth ===
clientWidth`, vorher 4335px bei 1920px Viewport). Bei kleineren Viewports
(1440px) passen entsprechend weniger Kacheln (rein platzbedingt, kein Bug)
– das Ergebnis skaliert mit der tatsächlichen Fensterbreite. Maßstab der
Zeichnungen selbst unverändert (Vorgabe eingehalten) – nur der Kachelrand
wurde reduziert. Keine Konsolenfehler. **Nebenbefund, nicht Teil dieser
Änderung:** `.panel-right` (Stückliste) überläuft bei 1920px unabhängig
davon um ~209px (`maxRight`-Element-Scan bestätigt `.panel-right` als
Verursacher) – vorbestehend, nicht durch diese Änderung verursacht, nicht
behoben (außerhalb des heutigen Auftrags).

### Mehrfeld-Schaltschränke Nachtrag 5: klemm_l gehört nicht ins Einspeisefeld (Session 48, gesperrt)
Direkte Fortsetzung von Nachtrag 4, gleicher Tag – Nutzer-Korrektur nach
eigener Prüfung: „Wenn das Einspeisefeld alleine sein soll, dann gibt es
dort keine Zone für Klemmenzone für Leistung. Die gibt es nur dort, wo auch
eine Zone Leistung existiert." `FELDTYP_ZONEN.C` enthielt bisher fälschlich
`klemm_l` (Abgangsklemmen Leistung) – fachlich falsch, da ein reines
Einspeisefeld (Typ C) selbst keine Leistungsbaugruppen führt und die
zugehörigen Abgangsklemmen daher dort nichts zu suchen haben; sie gehören
ins Leistungsfeld (Typ D), das `klemm_l` bereits korrekt führt.

**Fix:** `klemm_l` aus `FELDTYP_ZONEN.C` entfernt (`C: ['klemm_e','uss',
'evert']`, vorher zusätzlich `'klemm_l'`). In der Klemmzeilen-Transformation
von `buildLayoutForFeldtyp()` galt bisher hart „klemm_e wächst nie" (fester
physischer Platzbedarf) – das bleibt für alle Feldtypen mit mindestens
einer weiteren Klemmzone (A/B/D/E) unverändert richtig, aber für Typ C ist
`klemm_e` nach der Entfernung von `klemm_l` die EINZIGE verbliebene
Klemmzone in der Zeile. Neue Ausnahme: ist `growIds` (Breiten-Empfänger)
nach dem üblichen Filter leer UND `klemm_e` im Feldtyp enthalten, wird
`klemm_e` selbst zum alleinigen Empfänger – die komplette freiwerdende
Zeilenbreite (vorher zwischen klemm_e und klemm_l aufgeteilt) geht jetzt
vollständig an die Einspeiseklemmen. In Modul 3 UND Modul 4 identisch
angewendet (`redistributeKlemmBands()`/`klemmKeysHier` in Modul 4 brauchten
keine Änderung – beide leiten die relevanten Klemm-Zonen bereits dynamisch
aus `FELDTYP_ZONEN[feldtyp]` ab, `klemm_l` fällt für Typ C damit automatisch
weg).

Verifiziert direkt im Browser (echtes Modul-2-Ergebnis 499×1861mm,
`getrennt_els`, KE oben): `FELDTYP_ZONEN.C` bestätigt ohne `klemm_l`,
Klemmzeile von Typ C enthält nur noch `klemm_e` mit voller Zeilenbreite
(`w:1`), Höhenbilanz weiterhin exakt (1861mm = 1861mm) für alle 5
Feldtypen; Typ A/B/D/E strukturell unverändert (Regressionsschutz).
End-to-End-Platzierungstest in Modul 4 (20× Einspeiseklemme + 50×
Abgangsklemme Leistung in die Belegung gelegt): Feld 1 (Typ C) zeigt nur
noch ein `klemm_e`-Band über die volle Breite, KEIN `klemm_l`-Band mehr;
die Abgangsklemmen Leistung route korrekt in die Leistungsfelder (Typ D,
Felder 2+3) – keine Konsolenfehler.

### Mehrfeld-Schaltschränke Nachtrag 4: Kettentest Modul 2 → Modul 3 → Modul 4 (Session 48, gesperrt)
Direkte Fortsetzung von Nachtrag 3, gleicher Tag – Nutzer-Auftrag: „Meine
Tests gingen alle mit der gerade gespeicherten Variante mit Kabeleinführung
von unten. Kannst Du das auch für die anderen Fälle im Modul 2 testen,
bspw. Kabeleinführung von oben. Ich möchte sicherstellen, dass die
gewählten Konfigurationen beginnend bei Modul 2 über die gesamte Kette bis
zu Modul 4 durchgereicht werden." Wichtiger Fund VOR dem eigentlichen Test:
alle bisherigen Session-48-Tests hatten `b`/`h` direkt synthetisch per
`localStorage.setItem('m02_b_mplatte_mbereich_standschrank_mm', ...)`
gesetzt, statt sie über eine echte Modul-2-Berechnung zu erzeugen – die
Modul-2→Modul-3-Übergabe selbst (`loadFromModul()`, drei Schlüssel:
`m02_b_mplatte_mbereich_standschrank_mm`/`m02_h_...`/`m02_ke_pos`) war
dadurch bisher nie tatsächlich end-to-end durchlaufen worden.

**Vier reale Modul-2→3→4-Ketten getestet** (über die UI-Felder in Modul 2
gesetzt, `calculate()` ausgelöst, dann zu Modul 3/4 navigiert und dort
`schrank_typ` gewählt – kein synthetisches localStorage-Seeding):
1. Rittal VX 8806.000 (800×2000mm), Sockel 100mm aktiv, Zugentlastung ja,
   Kabelkanal ja, **KE oben** (die vom Nutzer benannte Hauptlücke).
2. Rittal VX 8205.000 (1200×2000mm, deutlich breiter), Sockel 200mm, KE
   oben – prüft ob unterschiedliche `b_mb`-Werte (nicht nur `h_mb`) korrekt
   durchgereicht werden.
3. Rittal VX 8604.000 (600×2000mm), **kein Sockel, keine Zugentlastung,
   kein Kabelkanal**, KE unten – prüft ob ein reduziertes `h_ke` (87mm statt
   203mm) korrekt zu einem größeren `h_mb` führt (1861mm statt 1745mm) und
   ob „kein Sockel" sauber durch die Kette läuft.
4. Wie 3, aber KE oben + `zone_modus=getrennt_els` (3 Felder) – prüft das
   Zusammenspiel KE-Position × Mehrfeld-Feldtyp-System.

Bei jedem der vier Fälle geprüft: `b_mb`/`h_mb`/`ke_pos` aus Modul 2 exakt
identisch in Modul 3 UND Modul 4 wiedergefunden; `buildLayout()`/
`buildLayoutForFeldtyp()`-Zeilenreihenfolge korrekt an `ke_pos` angepasst
(KE oben → Klemmzeile zuerst/Energieverteilung zuletzt; KE unten exakt
umgekehrt) – direkt an den gerenderten SVG-Rect-y-Koordinaten in Modul 3
UND Modul 4 verifiziert, nicht nur am rohen Zeilen-Array; Höhenbilanz
(Summe Zeilenhöhen = `h`) exakt bei `uebereinander` in jedem Fall; keine
Konsolenfehler in Modul 3 oder Modul 4 bei irgendeiner der vier Ketten.
**Kein neuer Bug in der Modul-2→3→4-Übergabe selbst gefunden** – die drei
durchgereichten Werte werden in jedem getesteten Fall korrekt übernommen
und korrekt ausgewertet.

**Nebenbefund beim Testen von Fall 1 (führte zur Korrektur eines zu eng
gefassten Nachtrag-2-Befunds):** beim Testen von `nebeneinander` mit einem
ECHTEN Modul-2-Ergebnis (699×1745mm, `schiene='nein'`) trat derselbe
Höhenüberschuss auf wie der in Nachtrag 2 nur für Drehstrom+Schiene+
Nebeneinander dokumentierte Fall (dort 6mm bei 699×1499mm) – hier 5mm bei
699×1745mm, OHNE Schienensystem. Zeigt: der Rundungsfehler ist nicht an
Netztyp/Schiene gebunden, sondern tritt bei JEDER `nebeneinander`-Kombi­
nation auf, bei der `h_verfügbar/2` nicht durch 5 teilbar ist – die
99×1499mm-Kombination aus Nachtrag 2 hatte für andere Netztyp/Schiene-Werte
zufällig einen Rest von 0. CLAUDE.md-Eintrag in Nachtrag 2 entsprechend
korrigiert. Weiterhin bewusst NICHT gefixt (gesperrte Formel, siehe dort).

Verifiziert direkt im Browser (lokaler Server, vier vollständige Ketten
Modul 2 → Modul 3 → Modul 4, echte UI-Eingaben statt synthetischem
localStorage): alle vier Fälle wie oben beschrieben bestätigt.

### Mehrfeld-Schaltschränke Phase 2+3 Nachtrag 3: zone_anordnung-Sperre aufgehoben (Session 48, gesperrt)
Direkte Fortsetzung von Nachtrag 2, gleicher Tag – Nutzer-Fund während der
eigenen Sichtprüfung: „Der Fall Mehrere Felder Leistung und Steuerung
nebeneinander fehlt" (In Modul 3), präzisiert kurz danach: „Der Fall Mehrere
Felder Einspeisefeld separat hat auch keine Steuerung und Leistung
nebeneinander" – d. h. betraf nicht nur `je_feld`, sondern jeden
Mehrfeld-`zone_modus`.

**Root Cause:** zwei unabhängige Stellen sperrten „Nebeneinander" für jede
Mehrfeld-Konfiguration vollständig:
1. `calculateZones()` setzte `document.getElementById('zone_anordnung').disabled
   = isMehreFelder` – eine Alt-Sperre aus der Zeit VOR dem Feldtyp-System
   (damals war „Mehrere Felder" nur ein unfertiger Platzhalter, der dieselbe
   1-Feld-Ansicht N-mal wiederholte, für den `anordnung` keine Rolle spielte).
2. `buildZoneSVG()`s Mehrfeld-Zweig überschrieb die tatsächliche Auswahl in
   der Sidebar-Vorschau IMMER hart auf `anordnung:'uebereinander'`
   (`zpUeber`-Objekt) – selbst wenn die Sperre aufgehoben worden wäre, hätte
   die Vorschau die Nutzerwahl ignoriert.

Beide Sperren stammen aus der Vor-Feldtyp-Ära und sind mit dem seit Session
48 vollständig ausgebauten `buildLayoutForFeldtyp()` nicht mehr nötig – der
eigene Konfigurationssweep (Nachtrag 2, Punkt 4) hatte bereits belegt, dass
alle Feldtypen A–E nebeneinander strukturell korrekt rechnen (0 fehlende
Zonen in allen 40 getesteten Kombinationen). **Fix:** Sperre 1 entfernt,
Sperre 2 durch direkte Verwendung von `zp` (statt `zpUeber`) ersetzt – die
Vorschau zeigt jetzt exakt das, was der Nutzer ausgewählt hat, für jeden
`zone_modus`. Modul 4 brauchte keine Änderung – es liest `anordnung`
ohnehin nur aus `localStorage.getItem('m03_zone_anordnung')`, ohne eigene
Sperre.

Verifiziert direkt im Browser: `zone_anordnung`-Dropdown bleibt bei
`getrennt_els` UND `je_feld` UND `einsp_misch` aktiv bedienbar; Auswahl
„Nebeneinander" bei `getrennt_els` (3 Felder) zeigt korrekt in Feld 1
(Einspeisung, Typ C) zwei nebeneinanderliegende Energieverteilung-Anteile
(da bei Nebeneinander sowohl Leistung ALS AUCH Steuerung aus der ÜSS-Zeile
entfallen, beide werden durch den Nachtrag-2-Fix einzeln durch
Energieverteilung ersetzt), Höhenbilanz weiterhin korrekt; Modul 4 zeigt
dieselbe Konfiguration fehlerfrei (keine Konsolenfehler) mit sichtbarem
Energieverteilung-Streifen in Feld 1.

### Mehrfeld-Schaltschränke Phase 2+3 Nachtrag 2: Maßlinien, Evert-Reclaim, M4-Maßstab (Session 48, gesperrt/teilweise offen)
Direkte Fortsetzung von Phase 2+3, gleicher Tag – Nutzer-Korrekturauftrag
nach eigener Sichtprüfung: „Die Maße fehlen bei den Ansichten mit mehreren
Zonen", „Wir haben nicht alle Fälle berücksichtigt" (4 weitere M3-Optionen
neben `zone_modus` prüfen) und ein bei der Einspeisung (Typ C) frei
werdender Leistungsbereich, der „per Definition" der Energieverteilung
zuzuordnen wäre. Dazwischen ein weiterer Nutzer-Fund: „Die grafische
Darstellung der Schränke verlässt im Gegensatz zu 1 Feld auch den Maßstab"
(Modul 4).

**1. Modul 4 – Feld-zu-Feld-Maßstab reparaifert.** Root Cause: `calculate()`
rief `buildSVG()`/`buildTuerAnsicht()` bisher in EINER Schleife auf, die pro
Iteration sofort einen Wrap-`<div>` anlegte, anhängte UND direkt im selben
Schritt `wrapEl.clientWidth` maß – beim ALLERERSTEN Feld war das Flexbox-
Layout (`#felder-row`/`#tueren-row`) zu diesem Zeitpunkt noch unvollständig
(nur ein Kind vorhanden), wodurch Feld 1 eine andere (zu große) gemessene
Breite bekam als alle Folgefelder (korrekt mit allen Geschwistern gemessen).
Da SVG-Breite/-Höhe als feste Pixelwerte ins Markup geschrieben werden,
„erstarrte" Feld 1 auf einem falschen Maßstab. **Fix:** beide Renderschleifen
zweigeteilt – zuerst ALLE Wrap-Container anlegen und anhängen, danach erst
`buildSVG()`/`buildTuerAnsicht()` aufrufen (liest dann korrekt fertig
gelayoutete Breiten). Verifiziert: 3- und 7-Felder-Testszenario, alle Felder
exakt identische Pixelgröße, keine Konsolenfehler.

**2. Modul 3 – Maßlinien in der Mehrfeld-Sidebar-Vorschau ergänzt.** Der
`modus!=='1feld'`-Zweig von `buildZoneSVG()` zeichnete bisher nur Zonen-
Rahmen + Feldtyp-/Zonen-Label, keine Maßangaben. Ergänzt: Zeilen-Maßwert
(mm) je Feld (da sich Zeilenhöhen zwischen Feldtypen unterscheiden, z. B.
Energieverteilung bei Typ C viel höher als bei Typ A – anders als die
Zonenbeschriftung, die nur bei Feld 1 gezeigt wird), eine gemeinsame
Gesamthöhe-Maßlinie rechts (`H=`, alle Felder identisch hoch) und eine
Breite-Maßlinie unter Feld 1 (`B= ... mm je Feld`). **Fehldiagnose
unterwegs:** der erste Test zeigte scheinbar gar keine der neuen Maß-Texte
im SVG – Ursache war kein Code-Bug, sondern `schrank_typ` (bewusst „kein
Persist", startet nach jedem Reload leer) stand nach einem Reload wieder auf
„— bitte wählen —", wodurch `b`/`h` auf 0 fielen und `buildZoneSVG()` über
den `if(!b||!h) return ''` -Guard sofort einen leeren String lieferte – rein
per UI-Dropdown erneut ausgewählt, waren die Maßlinien korrekt vorhanden.

**3. Typ-C-Bug: freiwerdende Leistungsbreite ging verloren statt an Evert
(Kernauftrag).** In der ÜSS-Zeile (`leist_uss_ueber`/`leist_uss_neben`)
bleibt bei Feldtyp C (Einspeisefeld) die ÜSS-Zone erhalten, während Leistung
(und bei „Nebeneinander" auch Steuerung) entfällt. Die bestehende Schutzregel
„ÜSS wächst selbst NIE" (`growIds = growIds.filter(id => id !== 'uss')`)
leerte in genau diesem Fall `growIds` vollständig – die freiwerdende Breite
hatte dadurch keinen Breiten-Empfänger mehr und verschwand kommentarlos
(sichtbar als unbeschrifteter Leerraum neben der ÜSS). **Fix, Iteration 1
(verworfen):** freiwerdende Breite flächengleich (Breitenanteil × Zeilenhöhe)
in zusätzliche Höhe für das Wachstumsziel (`FELDTYP_GROW_TARGET`, bei Typ C
= `evert`) umrechnen – exakt wie beim vollständigen Zeilenwegfall. **Beim
eigenen Nachrechnen als falsch erkannt, bevor an den Nutzer berichtet
wurde:** anders als beim vollständigen Zeilenwegfall bleibt diese Zeile
selbst mit ihrer FESTEN physischen Höhe (`h_klemm`, Hutschienenhöhe)
bestehen – zusätzliche Höhe an anderer Stelle addieren, OHNE diese Zeile zu
kürzen, hebelt die Höhenbilanz aus: Summe aller Zeilenhöhen überstieg danach
messbar die tatsächliche Feldhöhe `h` (verifiziert: 1566 mm Summe bei
`h=1499 mm`, +67 mm Überschuss). **Fix, finale Fassung:** die freiwerdende
Breite wird NICHT in Höhe umgerechnet, sondern direkt als eigene
Wachstumsziel-Zone (Farbe/Label aus neuer Konstante `GROW_TARGET_LBL`) an
derselben Stelle INNERHALB derselben Zeile eingefügt – physisch plausibel
(Energieverteilung neben der ÜSS auf gleicher Hutschienenhöhe), Zeilenhöhe
bleibt unverändert, Gesamthöhenbilanz exakt erhalten (verifiziert: 1499 mm
Summe bei `h=1499 mm`, uebereinander; 1500 vs. 1499 bei nebeneinander –
1 mm Differenz ist vorbestehendes, unabhängiges ceil5-Rundungsrauschen,
siehe Punkt 4). Betraf ausschließlich Feldtyp C (Typ D/E landen in der
äquivalenten Zeile nie bei leerem `growIds`, da dort `leist` bzw. `steuer`
selbst der verbleibende Breiten-Empfänger ist – geprüft und bestätigt kein
Analogfall). In Modul 3 UND Modul 4 identisch dupliziert (Konventions-Pflicht
für `buildLayoutForFeldtyp()`).

**4. Systematischer Konfigurationstest (Nutzer-Auftrag „alle möglichen
Konfigurationen").** Per Skript alle Kombinationen aus `zone_anordnung`
(übereinander/nebeneinander) × `zone_netztyp` (Drehstrom/Wechselstrom) ×
`zone_schiene` (Ja/Nein, nur bei Drehstrom UI-relevant) ×
`zone_schiene_pol` (3/4/5-polig, nur bei Schiene=Ja) × Feldtyp (A–E) direkt
im Browser durchgerechnet (nicht einzeln per UI-Klick): Zonen-Mitgliedschaft
war in JEDER Kombination korrekt (0 fehlende Zonen). **Ein pre-existing,
von der heutigen Feldtyp-Arbeit unabhängiger Befund:** bei `anordnung=
'nebeneinander'` + `netztyp='drehstrom'` + `schiene='ja'` (alle 3 Pol-
Varianten) überschreitet die Summe aller Zeilenhöhen die Feldhöhe `h` um
6 mm – reproduzierbar auch bei Feldtyp A (Vollfeld/1-Feld-Pass-through, also
NICHT Teil des heutigen Feldtyp-Systems, sondern bereits im ursprünglichen
`calculateZones()`/`buildLayout()`). Ursache: für „Nebeneinander" wird
`h_leist = ceil5(h_verfügbar / 2)` einmal berechnet und für `h_steuer`
identisch übernommen (fachlich richtig – beide Zonen liegen nebeneinander
auf gleicher Höhe) – die Zeilen, die diese Höhe nutzen, verwenden sie aber
EFFEKTIV ZWEIMAL (Summe = `2×h_leist`), wodurch ein `ceil5`-Rundungs-
Überschuss verdoppelt wird (bei den getesteten 699×1499 mm z. B. `h_verfügbar
/2 = 492` → `ceil5→495`, `2×495=990` statt `984`, Differenz 6 mm). **Bewusst
NICHT in dieser Session gefixt** – betrifft eine unter „Modul 3 – Zonenauf­
teilung (gesperrte Entscheidung)" bereits fest dokumentierte Formel
(„Leistung/Steuerung: ... gleiche Höhe je ~50 % b_inner (Nebeneinander)"),
Änderung an einer gesperrten Berechnung ohne explizite Nutzer-Freigabe wäre
eigenmächtig. Nur dem Nutzer zur Kenntnis/Entscheidung vorgelegt (geringe
Praxisrelevanz: 6 mm auf ≈1500 mm ≈ 0,4 %). **Ursprüngliche Eingrenzung
„betrifft ausschließlich Drehstrom+Schienensystem+Nebeneinander" beim
M2→M3→M4-Kettentest (Nachtrag 4) als zu eng erkannt und korrigiert** – das
Muster ist tatsächlich AllGEMEIN für `nebeneinander` (jede `netztyp`/
`schiene`-Kombination), sobald `h_verfügbar/2` nicht exakt durch 5 teilbar
ist; bei 699×1499 mm rundete sich das für andere Kombinationen zufällig auf
0 mm, bei anderen b/h-Werten (z. B. 499×1861 mm, reales Modul-2-Ergebnis
ohne Sockel/Zugentlastung) trat derselbe Fehlerklasse mit 5 mm Überschuss
auf – unabhängig von Netztyp/Schiene. Siehe Nachtrag 4.

Verifiziert direkt im Browser (lokaler Server, Standschrank 699×1499 mm):
Modul-4-Maßstab-Fix mit 3- und 7-Felder-Szenario bestätigt (identische
Pixelgrößen); Modul-3-Maßlinien nach UI-Dropdown-Auswahl korrekt sichtbar
(Zeilen-mm-Werte, `H=1499 mm`, `B=699 mm je Feld`); Typ-C-Fix visuell in
Modul 3 UND Modul 4 bestätigt (Energieverteilung-farbiger Streifen neben
ÜSS in Feld 1, keine Lücke mehr) sowie rechnerisch (Höhensumme exakt =
Feldhöhe); Konfigurationssweep (40 Kombinationen × 5 Feldtypen = 200
Prüfungen) protokolliert, 0 fehlende Zonen, 1 isolierter Altbefund (Punkt 4).
Noch NICHT vom Nutzer selbst gegengeprüft (Nutzer kündigte eigene Prüfung
an, Session pausiert wegen Nutzungslimit) – wie bei Phase 1/2/3 nicht
vorschnell als final/für Baugruppen-Start freigegeben behandeln, bis der
Nutzer das explizit bestätigt.

### Mehrfeld-Schaltschränke Phase 2+3: Fall 3+4 (Session 48 Nachtrag, gesperrt)
Direkte Fortsetzung von Phase 1, gleicher Tag – Nutzer-Vorgabe „Setze sie
direkt um" statt die ursprünglich vorgeschlagene Verschiebung auf eine
Folgesession. Wichtiger Hinweis des Nutzers, der die Reihenfolge
rechtfertigt: „Über die Platzierung der Einzelbauteile, bei denen Zonen
ja zugeordnet sind, kann man das prima testen. Die Baugruppen sind davon
unabhängig" – Fall 3/4 sind über Modul 3s Zonen-Zuordnung und Modul 4s
Einzelbauteil-Platzierung vollständig testbar, ohne auf den noch
ausstehenden Baugruppen-Neuaufbau zu warten.

**`buildLayoutForFeldtyp()` von einer Typ-B-Speziallösung auf eine
einzige generische Zeilen-Transformation umgebaut** (in Modul 3 UND
Modul 4 identisch, wie gehabt dupliziert), die A (Pass-through) und B–E
einheitlich abdeckt:
- Reine Struktur-Kanalzeilen (`kanal_h`/`kanal_ls`/`kanal_ev`/`kanal_ev2`)
  werden über `kanalNochNoetig(kanalId, zoneSet)` behalten oder gestrichen
  – `kanal_h` immer (jeder Feldtyp hat mindestens eine Klemmzone),
  `kanal_ls` nur wenn Leistung UND Steuerung im Feldtyp vorkommen (nie bei
  C/D/E einzeln), `kanal_ev`/`kanal_ev2` nur wenn Energieverteilung
  vorkommt.
- Klemmzeile: Breite entfallender Subzonen geht proportional an die
  verbleibenden (klemm_e wächst nie – fester physischer Platzbedarf,
  unabhängig vom Feldtyp).
- Übrige Zeilen (evert/uss/leist/leist_ext/steuer): entfällt eine Zeile
  KOMPLETT (keine ihrer Zonen bleibt), geht ihre Höhe an
  `FELDTYP_GROW_TARGET[feldtyp]` (`C→evert`, `D→leist`, `E→steuer`, `B`
  braucht keins – dort entfällt nie eine ganze Zeile). Bleibt nur ein Teil
  der Zeile (z. B. ÜSS-Zeile mit Leistung+Steuerung, nur Leistung
  entfällt), wird innerhalb der Zeile umverteilt – mit der bestehenden
  ÜSS-Sonderregel: freier Platz geht ausschließlich an Leistung, nie an
  Steuerung, auch wenn beide dieselbe Zeile teilen und Steuerung selbst
  nicht entfällt (galt bereits für Typ B, gilt jetzt konsistent für alle).
- Regressionsgeprüft: Typ A bytegleich zu `buildLayout()`, Typ B liefert
  exakt dieselben Zeilen wie die alte Speziallösung (verifiziert direkt im
  Browser, Zonenbreiten/-höhen 1:1 verglichen).

**Modul 3:** `zone_modus`-Dropdown um zwei Optionen erweitert:
`getrennt_els` („Einspeisung/Leistung/Steuerung getrennt") und
`einsp_misch` („Einspeisung getrennt, Leistung+Steuerung gemischt").
`buildZoneSection()`-Labels generalisiert (zeigen jetzt die Feldtyp-Kette
aus `FELDPLAN` statt nur „je_feld"-Sonderfall).

**Modul 4:** `redistributeKlemmBands()` bekommt einen `keys`-Parameter
(welche Klemm-Subzonen dieser Feldtyp führt – 1er-Pool `['klemm_l']` bei
Typ C/D, 2er-Pool `['klemm_f','klemm_s']` bei Typ E, Default alle drei für
Alt-Aufrufer/Typ A/B). `placeBauteileForField()` übergibt die zu diesem
Feldtyp passenden Keys statt hart codierter drei Klemmzonen.

**Bug beim ersten Test gefunden+gefixt:** `FELDPLAN['getrennt_els']`
hatte Feldtyp C (Einspeisung) fälschlich `repeat:true`. Da `klemm_l`
sowohl zu Typ C (Einspeisefeld behält Abgangsklemmen Leistung) als auch
zu Typ D (Leistungsfeld) gehört, ließ ein Überlauf in `klemm_l` die
Einspeisung selbst wiederholen (`calculateFelder()`s demand-getriebene
Erweiterung prüft alle Zonen des Feldtyps, `klemm_l` zählte für C mit) –
fachlich falsch, da es nur EINE Netzeinspeisung pro Anlage gibt. Fix: C
ist jetzt `repeat:false` (wie in Fall 4 bereits korrekt), der `klemm_l`-
Rest läuft automatisch an Typ D weiter (dessen `repeat:true` bleibt
unverändert und übernimmt korrekt).

Verifiziert direkt im Browser über Einzelbauteil-Platzierung (Modul 3:
alle drei neuen Feldtypen strukturell geprüft – Typ C/D/E konservieren
die Gesamthöhe exakt, enthalten genau die spezifizierten Zonen, Breiten-
Wachstum an den richtigen Stellen; Sidebar-Vorschau zeigt korrekte
Feldtyp-Labels „F1·Einspeisung/F2·Leistung/F3·Steuerung" bzw.
„F1·Einspeisung/F2·Folgefeld/F3·Folgefeld". Modul 4: Fall 3 mit 100
Klemmen in `klemm_l` + 3 in `klemm_f` erzeugt korrekt `[C,D,D,E]` –
Leistungsfeld erweitert sich unabhängig vom hier nicht überlaufenden
Steuerfeld, Positionsnummern innerhalb `klemm_l` über beide D-Felder
hinweg eindeutig (1–100), Stückliste zeigt zwei getrennte Zeilen mit
korrekten Positionsbereichen. Fall 4 mit 150 Klemmen erzeugt korrekt
`[C,B,B,B,B]` – exakt wie Fall-2-Folgefelder ab Feld 2. Fall 1+2
anschließend erneut gegengeprüft, unverändert. Keine Konsolenfehler in
allen vier Fällen.

**Bewusst nicht Teil dieser Session:** `buildFullLayoutSVG()`
(Druckfunktion) kennt weiterhin nur Einzelfeld-Layout, Mehrfeld-Druck
bleibt niedrige Priorität (Phase 4/Politur). Baugruppen-Platzierung über
mehrere Felder hinweg ungetestet (Baugruppen sind seit Session 40 leer) –
strukturell sollte sie funktionieren, da `placeBauteileForField()`
Baugruppen- und Einzelbauteil-Queues identisch behandelt, aber explizit
unverifiziert.

### Mehrfeld-Schaltschränke Phase 1: gleichartige Folgefelder (Session 48, gesperrt/teilweise offen)
Nutzer-Auftrag direkt im Anschluss an Session 47 (Türansicht): Modul 3
hatte bereits ein `zone_modus`-Dropdown „1 Feld"/„Mehrere Felder" +
Feldanzahl-Eingabe, aber die Zonenberechnung lief immer nur einfeldig –
„Mehrere Felder" wiederholte im Sidebar-Vorschau-SVG nur dasselbe
Einzelfeld-Layout N-mal identisch. Modul 4 las `m03_zone_modus`/
`m03_n_felder` überhaupt nicht. Nutzer-Vorgabe: vollständige Mehrfeld-
Unterstützung mit 4 Fällen (1 Feld / gleichartige Folgefelder /
Einspeisung-Leistung-Steuerung getrennt / Einspeisung getrennt von
Mischfeld) – Umfang und Layout-Fragen per `AskUserQuestion` geklärt
(„Alle 4 Fälle vollständig", „Alle Felder in einer Reihe nebeneinander").
Plan-Mode-Recherche (2 Explore-Agenten + 1 Plan-Agent) ergab: Modul 4
dupliziert `buildLayout()` Byte-für-Byte aus Modul 3 (bestehende
Konvention) – jede Feldtyp-Logik muss identisch in beiden Modulen stehen.
**Diese Session liefert Phase 1 (Fall 1+2), Fall 3+4 folgen als
Phase 2/3.**

**Feldtyp-Modell (5 Typen A–E, nur A/B in Phase 1 implementiert):**
```
A Vollfeld/Erstfeld: alle 8 Zonen
B Folgefeld (Fall 2 ab Feld 2): wie A ohne klemm_e+uss –
  klemm_e-Breite → klemm_l/f/s (proportional), uss-Breite → leist
C Einspeisefeld (Fall 3/4 Feld 1, Phase 2): klemm_e,uss,evert,klemm_l
D Leistungsfeld (Fall 3, Phase 2): leist(+ext),klemm_l
E Steuerfeld (Fall 3, Phase 2): steuer,klemm_f,klemm_s
```
`zone_modus` → Feldsequenz (`FELDPLAN`, `*`=erweitert sich automatisch
bei eigenem Überlauf): `1feld→[A]`, `je_feld→[A,B*]`,
`getrennt_els→[C*,D*,E*]` (Phase 2), `einsp_misch→[C,B*]` (Phase 3 –
Nutzer bestätigt: Feld 1 = Einspeisungsfeld wie Fall 3, ab Feld 2 exakt
Fall-2-Folgefeld, keine neue Berechnungslogik nötig). Fall 3: Leistungs-
und Steuerfeld erweitern sich unabhängig voneinander bei eigenem
Überlauf (Nutzer bestätigt, analog Fall 2).

**Wichtige Architektur-Erkenntnis (spart eine ursprünglich geplante
`m03_feldtypen_json`-Persistenz):** `zp` (Zonenparameter aus
`calculateZones()`) ist für ALLE Feldtypen identisch – jedes Feld ist ein
gleich großes Schaltschrankfeld (Montagebereich B×H aus Modul 1/2), nur
die ZEILEN-Transformation (`buildLayoutForFeldtyp(zp, feldtyp)`)
unterscheidet sich je Typ. Modul 4s `buildZpForFeldtyp()` ist deshalb nur
ein Alias für das bestehende `buildZp()` – keine neuen localStorage-Keys
nötig, die bereits vorhandenen flachen `m03_*`-Keys reichen.

**Modul 3:** `FELDTYP_ZONEN`/`FELDPLAN`/`redistributeRowZones()`/
`buildLayoutForFeldtyp()` neu (nach `buildLayout()`). Typ A = Pass-through
(Regressionsschutz). Typ B: `redistributeRowZones(zones, dropIds,
growIds)` entfernt Sub-Zonen aus einer Layout-Zeile, verteilt ihre Breite
proportional auf die verbleibenden Ziel-Zonen und packt die Zeile
lückenlos neu (x-Positionen) – funktioniert rein auf dem bestehenden
Zeilen-Array, keine Änderung an `buildLayout()` selbst nötig. Wandschrank-
Sperre: `calculateZones()` liest `schrank_typ` selbst, `modusRaw`
(Nutzer-Wahl) wird unverändert persistiert, nur der *effektive* `modus`
(für die Berechnung) wird bei Wandschrank auf `'1feld'` erzwungen – ein
Rückwechsel zu Standschrank stellt die vorherige Mehrfeld-Wahl wieder
her. `buildZoneSVG()` generalisiert: zeigt `expandFeldplan(modus,
n_felder)` (letzte `repeat`-Phase füllt bis n_felder auf) mit Feldtyp-
Label im Spaltenkopf, statt der bisherigen `je_feld`-Sonderbehandlung.

**Modul 4:** `FELDTYP_ZONEN`/`FELDPLAN`/`buildLayoutForFeldtyp()`
identisch dupliziert. `placeInBands()`/`placeInKlemmRow()` bekommen
`startIdx`-Parameter und liefern zusätzlich `leftoverDevs`+`nextIdx` –
ein Zonen-Rest, der in einem Feld nicht mehr passte, läuft so 1:1 als
`devs`-Eingabe ins nächste Feld weiter. `placeBauteile()` aufgeteilt in
`buildQueues()` (unverändert: `belegung` bleibt bewusst NICHT
feldbewusst, reine Artikel-Bestandsliste, Warteschlangen + DDC-Statistik
projektglobal einmal aufgebaut) und `placeBauteileForField(bandsAll,
klemmraum, feldtyp, queues, idxCounters, reservePct, useEvKanal)`
(platziert nur die Zonen dieses Feldtyps, verbraucht `queues[zone]`
destruktiv). Neu `calculateFelder()`: Orchestrator-Schleife über
`FELDPLAN[modus]`, erzeugt je Phase mindestens ein Pflichtfeld, erweitert
`repeat`-Phasen demand-getrieben solange die zugehörigen Zonen noch
Warteschlangenrest haben – Schutz gegen Endlosschleife über
`MAX_FELDER=20`-Deckel und „kein Fortschritt"-Abbruch (z. B. Einzelbauteil
größer als jede Zone), dann bleibt das bestehende rote „!" am letzten
Feld sichtbar statt den Tab einzufrieren.

**Türbauteile bekommen einen expliziten Feld-Bezug (Nutzer-Korrektur
während der Planung):** ursprünglich geplant war „alles in Feld 1
zeichnen" (kein Datenmodell-Aufwand) – der Nutzer wollte stattdessen
echte Feldzuordnung: „Ich ordne ja pro Feld zu. Da gehört dann auch die
Türe zu." `batches`-Einträge mit `zone==='tuer'` bekommen ein `feld`-
Attribut (1-basiert, Default 1), analog zur Session-44-Zonenwahl über
eine neue UI-Zeile `#feld_auf_row` (nur sichtbar bei `zone_modus!=='1feld'`
und Tür-Artikel, Optionen aus `letzteFelder` mit Feldtyp-Label).
`getTuerItems(feldIndex)` filtert jetzt pro Feld, `removeEinzelbauteilQty()`
respektiert bei Türbauteilen zusätzlich das im Dropdown gewählte Feld
(LIFO nur innerhalb dieses Feldes, analog zum bestehenden Zonen-Filter).

**Layout – zwei Panorama-Reihen statt fester Einzel-Container (Nutzer-
Vorgabe: „links werden die Felder nacheinander angezeigt, rechts die
Türen nacheinander... Innen- und Außenansicht wie sie später aussehen
werden"):** `#svg-wrap`/`#tuer-wrap` (feste IDs) ersetzt durch
`#felder-row`/`#tueren-row` (Flex-Reihen mit horizontalem Scroll statt
Stauchen bei vielen Feldern) – `calculate()` erzeugt pro Feld dynamisch
ein `.feld-svg-wrap`- bzw. `.feld-tuer-wrap`-Element, `buildSVG()`/
`buildTuerAnsicht()` nehmen jetzt Container-Elemente statt fester IDs
entgegen (`buildTuerAnsicht(feldIndex, wrap, inner)` gibt `true`/`false`
zurück, ob ein Türbauteil-Panel tatsächlich gezeichnet wurde – Felder
ohne Türbauteile bekommen keinen Block). Füllstand-Streifen und
Stückliste bleiben unverändert (keine Code-Änderung an `buildFuellstand`/
`buildStueckliste` nötig): `calculate()` aggregiert `mm_used`/`mm_total`/
`channels`/`rows` je Zone über alle Felder zu einem einzigen `aggZones`-
Objekt, `te_belegt` kommt aus einer einmaligen Bedarfs-Momentaufnahme
(`totalDemandTe`) vor der ersten Platzierung – Positionsnummern (`idx`)
sind dank fortlaufender `idxCounters` bereits feldübergreifend eindeutig,
`buildIdxMap()`/`aggregateStueckliste()` brauchten keine Änderung.

**Bewusst nicht Teil dieser Session (Phase 2/3):** Fall 3 (Einspeisung/
Leistung/Steuerung getrennt) und Fall 4 (Einspeisung getrennt von
Mischfeld) – Feldtypen C/D/E sind in `FELDTYP_ZONEN`/`FELDPLAN` bereits
als Konstanten angelegt, aber `buildLayoutForFeldtyp()` fällt für sie
noch auf das Vollfeld-Layout zurück (kein neuer `zone_modus`-Dropdown-
Eintrag, daher in der Praxis noch nicht erreichbar). `redistributeKlemmBands()`
braucht für Fall 3 noch einen `keys`-Parameter (1er-Pool bei C/D, 2er-Pool
bei E) – aktuell hart auf `['klemm_l','klemm_f','klemm_s']` codiert, für
A/B ausreichend, da beide immer alle drei Klemmzonen gemeinsam führen.
`buildFullLayoutSVG()` (Druckfunktion) kennt `je_feld` weiterhin nicht –
niedrige Priorität, eigene Politur-Phase.

Verifiziert direkt im Browser (lokaler Server, synthetische Belegung):
`1feld` bleibt bei Wandschrank UND Standschrank 100% identisch zum
Vorzustand (Regressionsnetz, keine Konsolenfehler). `je_feld` mit
künstlich überladener Belegung (150 Klemmen in `klemm_l`) erzeugt
automatisch 5 Felder (1×A + 4×B), alle 150 Positionsnummern global
eindeutig (`#1`–`#150`, keine Duplikate), Füllstand-Streifen zeigt
korrekt aggregierte 88 %, Stückliste zeigt Gesamtmenge 150 mit
zusammenhängendem Positionsbereich `#1–#150`. `klemm_e`/`uss` nur in
Feld 1 (Typ A) vorhanden, alle Folgefelder (Typ B) korrekt ohne. Tür-
Feldzuordnung: Hauptschalter auf Feld 2 zugeordnet erscheint exakt an
Position 2 der Türen-Reihe (Feld 1 ohne Türbauteil bekommt keinen
Block). Endlosschleifen-Schutz: künstliches Bauteil mit `te_breite=280`
(passt in keine Zone) bricht nach 3 Feldern sauber ab (15 ms
Rechenzeit, kein Hänger), rotes „!" bleibt sichtbar. Wandschrank-Sperre
in Modul 3 UND Modul 4 unabhängig verifiziert (`getEffektiveZoneModus()`
liefert `'1feld'` trotz gespeicherter `'je_feld'`-Wahl, sobald
`schrank_typ==='wandschrank'`).

### Modul 4 – Türansicht neben Innenansicht (Session 47, gesperrt)
Nutzer-Idee direkt im Anschluss an Session 46 (Türbauteile jetzt vollständig
katalogisiert): da Zone `tuer` bereits alle Fronttafel-/Türeinbaugeräte
korrekt trägt und deren Maße (`b_mm`/`h_mm`) sowie die echten Gehäuse-
Außenmaße (Modul 1/2) bereits vorhanden sind, fehlt nur noch die
Layoutlogik für eine zweite, separate Ansicht der Tür.

**Türmaße = echte Gehäuse-Außenmaße, nicht der Montagebereich (Nutzer-
Entscheidung, per `AskUserQuestion` bestätigt).** Fund: Modul 1 und Modul 2
schreiben `m01_B`/`m01_H` bzw. `m02_B`/`m02_H` bereits seit Session 19 in
localStorage (`b_gehaeuse_aussen_mm`/`h_gehaeuse_aussen_mm` der
Variablen-Konvention) – **keine Änderung an Modul 1/2 nötig**, nur
`getGehaeuseAussenmasse(typ)` in Modul 4 liest diese Werte passend zum
gewählten `schrank_typ` (`pfx = wandschrank→m01, standschrank→m02`, gleiches
Muster wie `loadMontagebereich()`).

**Ergonomische Höhen-Bänder** (`TUER_BAND_*`, Anteil der Türhöhe von unten,
Nutzer-Vorgabe, gestützt durch Recherche zu DIN EN 60204-1 – Hauptschalter/
Netztrenneinrichtung 0,6–1,9 m, empfohlen <1,7 m – und DIN 18040 –
Bedienhöhe 0,85–1,05 m):
```
HAUPTSCHALTER    0.40   (etwas unterhalb der Türmitte)
PHASENKONTROLLE  0.48   (Signalleuchte weiß, über dem Hauptschalter)
QUITTIERUNG      0.56   (Sammelstörmeldeleuchte rot + Quittiertaster)
HANDSCHALTER     0.68   (Wahlschalter/Not-Halt + Betriebsmeldeleuchte grün)
MESSGERAET       0.85   (oberes Drittel, Gesichtshöhe – Energiezähler/Touchpanel)
```
`tuerBand(eb)` klassifiziert bewusst grob nach `bauteil_typ` (+ Bezeichnungs-
Text bei `signalleuchte` zur Farbunterscheidung weiß/rot/grün) – keine
Zuordnung zu einem bestimmten Stromkreis, da dafür keine Datengrundlage
existiert.

**Zentrierte Reihen-Anordnung, gruppiert strikt nach Band (nicht nach
Bauteiltyp):** alle Bauteile desselben Bandes bilden EINE gemeinsame, um die
Türmitte (`b/2`) zentrierte Reihe – wichtig für das Quittierungs-Band, das
sowohl die rote Signalleuchte als auch den Quittiertaster enthält; eine
Gruppierung nach Bauteiltyp hätte dort zwei sich überlappende Zeilen an
derselben Höhe erzeugt (im Design vor dem Schreiben erkannt und vermieden).
Reihenfolge/Position einzelner Bauteile innerhalb eines Bandes ist die
Einfüge-Reihenfolge aus `belegung` – keine explizite Links-Mitte-Rechts-
Steuerung für z. B. „3 Phasenkontrollleuchten, mittlere zuerst".

**Datenquelle `getTuerItems()`:** durchsucht `belegung` nach
`typ:'einzel'`-Einträgen, deren Katalogeintrag `keine_platzierung_mp===true`
UND `zone.includes('tuer')` ist – identische Zwei-Feld-Prüfung wie in
`placeBauteile()`, nur zusätzlich auf die Tür-Zone eingeschränkt. Baugruppen-
Bauteile (`bt`) bewusst nicht berücksichtigt (Baugruppen sind weiterhin leer,
Session 40).

**Neuer `bauteil_typ` `hauptschalter`** (vorher `sonstige`, zu generisch für
die Bandzuordnung) für `3LD2504-0TK51` – einzige Inhaltsänderung im Katalog
dieser Session, `kurzLabel()` um `hauptschalter:'HS'` ergänzt.

**UI:** `.panel-mid` zeigt jetzt `#svg-wrap` (Schranksicht) und `#tuer-wrap`
(Türansicht, fix 260px breit) nebeneinander in `.schrank-views-row`
(`display:flex`). `buildTuerAnsicht()` wird am Ende von `calculate()`
aufgerufen (nach `buildSVG()`) und blendet `#tuer-wrap` per
`display:none`/`flex` selbst ein/aus – **kein Zusatzcode in der frühen
Rückkehr von `calculate()` bei fehlenden Montagebereich-Daten war nötig**
(dort wird `#tuer-wrap` ebenfalls explizit auf `none` gesetzt, analog zu
`#svg-msg`/`#svg-inner`). Ohne Türbauteile in der Belegung bleibt die
gesamte Ansicht ausgeblendet (Nutzer-Vorgabe „Haben wir keine
Türeinbaugeräte, entfällt die Anzeige").

Verifiziert direkt gegen die produktiven Funktionen im Browser (lokaler
Server, synthetische Belegung mit Hauptschalter + 3× weiße Signalleuchte +
rote Signalleuchte + Quittiertaster + Energiezähler UMG 96RM, Wandschrank
800×2000mm): SVG-Koordinaten der gerenderten Rects direkt ausgelesen und
gegen die erwarteten Bänder geprüft – Hauptschalter unterhalb der 3
Phasenkontrollleuchten, diese wiederum unterhalb der Quittierungs-Reihe
(rote Leuchte + Taster nebeneinander in EINER Zeile, wie gefordert),
Energiezähler nahe der Türoberkante; alle Bauteile korrekt um die Türmitte
zentriert (x-Mittelpunkte ≈ 106 bei 212,8px Türbreite). Leere Belegung →
`#tuer-wrap` korrekt `display:none`; kein `schrank_typ` gewählt → ebenfalls
`none`. Keine Konsolenfehler.

### Katalog: Zone-Korrektur Türbauteile + Signalleuchte weiß, Wischrelais, Störquittiertaster, M-Bus-Pegelwandler, Energiezähler (Session 46, gesperrt/teilweise offen)
Direkte Fortsetzung von Session 45 – Nutzer korrigiert die Zonen-Zuordnung und ergänzt weitere Bauteile.

**Zonen-Korrektur (Nutzer-Vorgabe, widerruft Session 43):** alle `Fronttafel-/Türeinbau`-Bauteile (Signalleuchte grün/rot, Wahlschalter, Not-Halt) `zone` `leist`→`tuer`. Session 43 hatte explizit „Signalleuchten gehören in Leistung" entschieden – der Nutzer hat das jetzt bewusst umgekehrt: „Die Fronttafel Türeinbau Geräte gehören nicht in Leistung sondern in Tür." Der Hauptschalter (`3LD2504-0TK51`) war bereits korrekt `tuer`.

- **Signalleuchte weiß** (`3SU1102-6AA60-3AA0`, Siemens SIRIUS ACT, gleiche Baureihe wie grün/rot) – löst die in Session 42 offene Frage: als Phasenkontrollleuchte L1/L2/L3 sind es schlicht drei Einzellampen, je eine direkt über den jeweiligen Strompfad angesteuert – kein eigenes 3-Phasen-Überwachungsgerät.
- **Gateway-Kategorie zurückkorrigiert** (`HD67812-KNX-XXX-B2`): `Netzwerkeinrichtung`→`DDC-Automationseinrichtung`. **Offene Architekturfrage (Nutzer-Vorgabe „müssen wir noch klären"):** das Gateway verbraucht wie eine CPU Datenpunkte, aber nur kommunikative – `isDdcSupplyTyp()` kennt aktuell nur `ddc_io`/`ddc_cpu` als Supply-Typen, die beide implizit AUCH physische Kapazität mitbringen (oder zumindest dafür vorgesehen sind). Ein rein-kommunikativer Supply-Typ (liefert nur `dp_fb_*`-Kapazität, keine `dp_*`) existiert im Schema noch nicht – bewusst nicht in dieser Session gelöst, da eine Schema-Änderung an einer zentralen, bereits mehrfach genutzten Funktion (`accumulateDp()`) nicht ohne Abstimmung sinnvoll ist.
- **Wischrelais** (`RE22R2HMR`, **Schneider Electric** Zelio Time) – Planungsfabrikat-Ausnahme analog LVB-Relais/Metz Connect (Session 41 Nachtrag 2): kein Phoenix-Contact-Produkt gefunden, das explizit als „Wischrelais" geführt wird, RE22R2HMR wird im deutschen/Schweizer Fachhandel durchgängig so bezeichnet. Einschaltwischende Funktion (aktiv bei Anlegen der Versorgungsspannung, z. B. nach Netzwiederkehr) – für automatische Störungsquittierung nach Spannungsausfall.
- **Störquittiertaster** (`3SU1152-0AB50-1BA0`, Siemens SIRIUS ACT, blau) – kein eigener Bestellschlüssel für „Störquittierung" gefunden (SIRIUS ACT ist modular, Funktionsbeschriftung separates Schild), Farbe Blau nach IEC 60073/DIN EN ISO 13850-Konvention für Quittier-/Reset-Funktionen gewählt.
- **M-Bus-Pegelwandler** (neuer `bauteil_typ:'pegelwandler'`, Kategorie `DDC-Automationseinrichtung`, Zone `steuer`) – **Relay GmbH** als Planungsfabrikat (in Deutschland etablierter Standardhersteller). Nutzer nannte Größen „6/20/50/100" – die tatsächlich bei Relay verifizierte Produktreihe führt **3/20/60/100(/250)** Teilnehmer, keine „PW6"/„PW50"-Variante gefunden. Nächstliegende reale Größen (PW20/PW60/PW100) verwendet statt eine nicht existente Variante zu erfinden – Abweichung im `quelle_hinweis` dokumentiert, bitte gegenprüfen.
- **Messgeräte/Energiezähler** (neue Kategorie, neuer `bauteil_typ:'messgeraet'`) – liefern überwiegend kommunikative Datenpunkte, `automationsanbindung`/`dp_fb_*` bewusst NICHT gesetzt (hängt an derselben ungelösten Architekturfrage wie das Gateway – wie viele „Datenpunkte" ein Multifunktions-Energiezähler mit dutzenden Registern im vereinfachten DBACS-Schema repräsentieren soll, ist nicht seriös zu beziffern ohne Rücksprache). Planungsfabrikate wie vom Nutzer vorgegeben: **Janitza UMG 96RM** (Türeinbau, 96×96mm, 3 Protokollvarianten RTU/M-Bus/`-PN` für Modbus TCP) und **Schneider Electric Acti9 iEM3000** (Montageplatte/Hutschiene, `iEM3135` M-Bus + `iEM3350` Modbus RTU) – für Modbus TCP auf der Montageplatte kein passendes Schneider-Hutschienengerät gefunden (deren Ethernet-Zähler der PowerLogic-PM5000-Reihe sind Fronttafelgeräte, kein Hutschienenformat), bewusst nicht falsch zugeordnet.

`kurzLabel()` um `quittiertaster`/`pegelwandler`/`messgeraet` ergänzt. `planungsfabrikate`-Sheet um 4 Zeilen ergänzt. Katalog jetzt 127 aktive Bauteile.

Verifiziert direkt im Browser: alle 4 zonenkorrigierten Artikel + alle 7 neuen Artikel mit korrekter Zone/Kategorie/`bauteil_typ` geladen (das inaktive Gateway korrekt nicht im JSON, da weiterhin `aktiv=false` wegen unverifizierter Maße – nur die Kategorie im Rohdatensatz korrigiert); keine Konsolenfehler.

### Katalog: GA-Schaltschrank-Bauteile für HLS/Elektro/Sanitär + Sicherheitstechnik-Schnittstellen (Session 45, gesperrt)
Nutzer-Auftrag (autonom, „ohne Rückfrage", 1-2h Recherche): Katalog um typische Komponenten für GA-Schaltschränke ergänzen. Anwendungskontext vom Nutzer vorgegeben: Überwachung/Steuerung von HLS+Elektro+Sanitär in Büro-/Verwaltungs-/Rechenzentrum-/Labor-/Schulgebäuden, zusätzlich Schnittstellen zu sicherheitsrelevanten Fremdsystemen (BMA, ZUKO, Videoüberwachung, Gaslöschanlagen). Fokus explizit auf Bauteile, die in Schaltschrank ODER Tür eingebaut werden (keine Feldgeräte/Sensoren/Aktoren außerhalb des Schranks). Planungsfabrikat Automation bleibt Siemens (bestehende Entscheidung, keine weiteren Automationshersteller).

**14 neue Katalogeinträge, 3 neue Kategorien:**
- **Frequenzumrichter** (neu) – Siemens SINAMICS G120C für Pumpen-/Lüfterantriebe mit Drehzahlregelung, 4 Baugrößen über den typischen HLK-Leistungsbereich: 0,75kW (FSAA), 3kW (FSA), 5,5kW (FSB, mit verifiziertem RS-Preis), 15kW (FSC). `bauteil_typ:'frequenzumrichter'`, zone `leist`.
- **Zeitrelais** (neu) – Phoenix Contact ETD-Serie, Multifunktion 0,05s–1h. `bauteil_typ:'zeitrelais'`, zone `steuer`.
- **Steckdose/Zubehör** (neu) – Phoenix Contact SD-D/SC Hutschienen-Schuko-Steckdose für Wartungszwecke. `bauteil_typ:'steckdose'`, zone `evert`.
- **Fronttafel-/Türeinbau erweitert:** Wahlschalter Hand-0-Automatik (SIRIUS ACT 3-Stufen-Komplettgerät – Beschriftung selbst ist ein separates Schild ohne eigenen Bestellschlüssel) + Not-Halt-Pilzdrucktaster (SIRIUS ACT, Drehentriegelung nach DIN EN ISO 13850). Beide `keine_platzierung_mp`, neue `bauteil_typ`-Werte `wahlschalter`/`nothalt`.
- **Koppelrelais erweitert:** 2-Wechsler-Variante (Phoenix PLC-RSC-24DC/21-21) ergänzend zum bestehenden 1-Wechsler-Modell – für Fälle mit höherem Kontaktbedarf (z. B. gleichzeitig Sammel- und Einzelmeldung aus einem Fremdsystem).
- **Energieverteilung-Schutzeinrichtungen erweitert:** 2× FI-Schutzschalter (Siemens SENTRON 5SV3, 25A/40A, neuer `bauteil_typ:'fi_schutzschalter'`) – **ersetzt inhaltlich** die in Session 40 wegen Datenqualitätsproblemen (falsche Artikelnummer/Nennstrom-Zuordnung) komplett gelöschten `reiheneinbaugeraete`-Altdaten, diesmal mit neu verifizierten Bestellnummern direkt in `einzelbauteile`.
- **Netzversorgung/Transformatoren erweitert:** größeres Netzteil (Phoenix QUINT-PS, 20A/480W, für hohen DDC-Punktzahl-/Modulbedarf) + **3-phasiger Steuertrafo** (Siemens 4AP2142-8BC40-0HA0, 1000VA) – löst die in Session 43 zurückgestellte Frage eigenständig: die 4AP-Baureihe hat mehrere Primär-/Sekundär-Anzapfungen (u. a. 400V-Sekundärabgriff verfügbar), deckt damit sowohl den ursprünglich gefragten „400V/400V"-Trennfall als auch klassische Steuerspannungserzeugung ab.
- **Netzwerkeinrichtung:** Phoenix Contact FL SWITCH SFNB 5TX ergänzt – löst das seit Session 40 offene Planungsfabrikat-TODO auf (Phoenix Contact, konsistent zu Klemmen/Netzteilen/Koppelrelais). Der bereits vorhandene, verifizierte Moxa EDS-205 (Session 42) bleibt zusätzlich aktiv (beide Hersteller in Deutschland gängig für Industrie-Switches).

**`kurzLabel()` in Modul 4** um alle 7 neuen `bauteil_typ`-Werte ergänzt (plus das bisher fehlende `signalleuchte` aus Session 43 nachgetragen).

**`planungsfabrikate`-Sheet aktualisiert:** Netzwerktechnik-TODO aufgelöst, 4 neue Zeilen für die neuen Kategorien ergänzt (alle konsistent zu den bereits etablierten Herstellern Siemens/Phoenix Contact – keine neuen Marken eingeführt, wie vom Nutzer gefordert „keine Exoten").

**Bewusst NICHT ergänzt (Datenlage zu dünn, keine geratenen Werte):**
- **DIN-Schienen-USV** (Phoenix QUINT-UPS) – keine verlässlichen Abmessungen gefunden.
- **RJ45-Patchpanel** (Phoenix FL-PP-RJ45) – keine verlässlichen Abmessungen/Preise gefunden.

**Preise:** nur bei 4 von 14 Einträgen ein Preis eingetragen (Frequenzumrichter 5,5kW, Koppelrelais 2W, Zeitrelais, Netzteil 20A, Steckdose) – bei den übrigen ausschließlich Gebrauchtmarkt-/Auktionspreise gefunden, nicht übernommen (Nutzer-Vorgabe „keine Börsen/Gebrauchtmärkte"). Bleibt offene Folgeaufgabe wie der Rest der ~70 preislosen Bestandsartikel.

Verifiziert direkt im Browser: 116/116 aktive Bauteile geladen, alle 10 stichprobenartig geprüften neuen Artikel mit korrekter Zone/Kategorie/Maßen; 5 davon real platziert (Belegung → Stückliste), jeweils in der erwarteten Zone gelandet; keine Konsolenfehler.

### Modul 4 – Mehrfachzonen-Bug behoben + Zonen-Auswahl umplatziert (Session 44 Nachtrag, gesperrt)
Zwei Nutzer-Funde direkt nach dem Test der Session-44-Funktion:

- **Bug: Zone galt item-weit statt pro Hinzufüge-Aktion.** `addEinzelbauteil()` schrieb die gewählte Zone auf `ex.zone` (item-weit, analog zu `ddcPhysisch`) – wurde dieselbe Klemme erst mit 5 Stück in `klemm_l`, dann mit 3 Stück in `klemm_s` hinzugefügt, sprang rückwirkend die GESAMTE Menge (alle 8) nach `klemm_s`. Anders als eine DDC-Eigenschaft (beschreibt eine feste technische Eigenschaft des Artikels) ist die Zone pro Hinzufüge-Aktion potenziell unterschiedlich – das „gilt item-weit"-Muster passte hier nicht.
- **Fix: `zone` ist jetzt Teil jedes einzelnen `batches`-Eintrags**, gleichrangig mit `forced`. `pushBatch(batches, n, forced, zone)` verschmilzt nur noch, wenn sowohl `forced` als auch `zone` mit dem letzten Batch übereinstimmen. `placeBauteile()`/`aggregateStueckliste()` iterieren beim direkten Einzelbauteil-Zweig jetzt je Batch (statt einmal item-weit) und lösen die Zone pro Batch auf (`b.zone`, Fallback `eb.zone[0]`) – dadurch können in einem Belegungseintrag gleichzeitig Mengen in mehreren Zonen koexistieren, korrekt getrennt in Platzierung und Stückliste.
- **`removeEinzelbauteilQty()` jetzt zonenbewusst:** bei Mehrfachzonen-Artikeln zieht „−" nur von Batches der aktuell im Zonen-Dropdown gewählten Zone ab (LIFO innerhalb dieser Zone), nicht mehr blind vom zeitlich letzten Batch unabhängig von dessen Zone. Einzelzonen-Artikel verhalten sich unverändert (reines LIFO wie seit Session 30).
- **Layout-Fund:** die Zonen-Auswahl-Zeile (`#zone_auf_row`) saß als eigene Zeile in der Eingabeleiste und schob die Schranksicht bei jedem Erscheinen nach unten. **Verlegt in den Füllstand-Streifen, rechts neben „Alle"** (`.fuellstand-strip`, `flex-wrap:wrap` hat dort bei normaler Fensterbreite noch Platz) – erscheint weiterhin nur bei Mehrfachzonen-Artikeln (`updateZoneAuswahlUI()`), ändert aber nie die Streifenhöhe oder die Position der Schranksicht darunter. Kompakte eigene CSS-Klasse `.fs-zone-auswahl` statt der bisherigen `.ddc-auf-row`-Wiederverwendung.

Verifiziert direkt im Browser (1920px): 5×Klemme in `klemm_l` + 3×dieselbe Klemme in `klemm_s` → zwei getrennte Batches, zwei getrennte Stückliste-Zeilen (5/3), keine Vermischung; „−2" mit Zonen-Auswahl auf `klemm_s` reduziert korrekt nur `klemm_s` (3→1), `klemm_l` bleibt bei 5 unangetastet; Zonen-Auswahl erscheint exakt auf gleicher Höhe/rechts neben „Alle", Füllstand-Streifen-Höhe (40,25px) und Schranksicht-Position identisch mit und ohne sichtbare Zonen-Auswahl; keine Konsolenfehler.

**Nachtrag (Komfort, gleicher Tag):** Ist beim Öffnen der Zonen-Auswahl bereits ein Klemmleisten-Filter aktiv (`einzelZoneFilter`, z. B. „Sensoren"), wird dieser automatisch als Vorauswahl übernommen (`updateZoneAuswahlUI()`), sofern er zu den erlaubten Zonen des gewählten Artikels gehört – bei „Alle" oder unpassendem Filter bleibt der bisherige Default (`eb.zone[0]`). Bleibt jederzeit manuell änderbar. Verifiziert: Filter „Sensoren" → Vorauswahl `klemm_s`; Filter „Feldgeräte" → `klemm_f`; Filter „Alle" → Default `klemm_l`.

### Modul 4 – Mehrfachzonen für Bauteile (Session 44, gesperrt)
Nutzer-Verständnisfrage: Baugruppen können pro Bauteil-Eintrag schon länger eine Zone überschreiben (`bt.zone || eb.zone`, Session 22). Für direkt ausgewählte Einzelbauteile fehlte das – eine Klemme mit Katalog-Default `klemm_l` ließ sich nicht direkt in `klemm_f`/`klemm_s` platzieren, ohne die Katalogzeile zu verdreifachen (bereits in Session 32 „Teil 2" als offener Punkt notiert). Nutzer-Vorschlag: `zone` als Array modellieren, erster Eintrag = Default.

- **`einzelbauteile.zone` ist jetzt immer ein Array**, auch bei nur einer Zone (Excel-Zelle bleibt eine einfache oder Komma-getrennte Liste, `xlsx_to_json.py` splittet immer, damit Modul 4 nie zwischen Skalar/Array unterscheiden muss). `bt.zone` (Baugruppen-Override) bleibt bewusst ein einzelner String je Verwendung – kein Array, da dort schon immer eine explizite Einzelentscheidung pro Baugruppen-Bauteil-Eintrag getroffen wird.
- **Neue UI-Zeile `#zone_auf_row`** (Muster identisch zur DDC-Aufschaltungs-Zeile, Session 41 Nachtrag): erscheint nur, wenn `eb.zone.length > 1`, lässt die Zone für die gerade hinzugefügte Menge explizit wählen (`updateZoneAuswahlUI()`, `getSelectedEinzelZone()`). Belegungseintrag (`typ:'einzel'`) bekommt ein eigenes `zone`-Feld – gilt **item-weit wie `ci`/`ddcPhysisch`, nicht pro Batch** (bewusst dieselbe Vereinfachung wie bei der DDC-Aufschaltung: erneutes Hinzufügen mit anderer Wahl aktualisiert die Zone für den gesamten Eintrag).
- **`populateEinzelAuswahl()`** filtert jetzt mit `e.zone.includes(einzelZoneFilter)` statt `===` – ein Mehrfachzonen-Artikel erscheint dadurch korrekt unter allen seinen erlaubten Zonen-Filtern im Füllstand-Streifen.
- **Zonen-Auflösung überall konsistent umgestellt:** `placeBauteile()` (Direktbauteile: `item.zone || eb.zone[0]`, mit Gültigkeitsprüfung gegen `eb.zone`; Baugruppen: `bt.zone || eb.zone[0]`, unverändertes Verhalten nur an die Array-Form angepasst) und `aggregateStueckliste()` (beide Zweige analog) – die aggregierte Stückliste speichert weiterhin die aufgelöste **einzelne** Zone, kein Array.
- **16 PT-Klemmen** (Phoenix Contact, Session 27b) probeweise auf `klemm_l,klemm_f,klemm_s` gesetzt – der konkrete Anlassfall. Die Messertrennklemme PT 2,5-MT hatte abweichend `klemm_f` als bisherigen Default; ihr Default ist durch die Vereinheitlichung jetzt `klemm_l` (erster Array-Eintrag) – bei Bedarf über die neue Zonen-Auswahl weiterhin gezielt auf `klemm_f` setzbar.
- **Nebeneffekt (bewusst, kein neuer Bug):** die `zone_bezeichnung`-VLOOKUP-Formel in Excel (gegen das `zonen`-Referenz-Sheet) findet für Mehrfachzonen-Zellen wie `"klemm_l,klemm_f,klemm_s"` keinen Treffer und zeigt leer (IFERROR-Fallback) – rein kosmetisch, keine Fehlermeldung, nicht behoben (würde eine kompliziertere Split-Formel brauchen, außerhalb des heutigen Auftrags).

Verifiziert direkt im Browser: PT-Klemme erscheint jetzt unter allen drei Zonen-Filtern; Zonen-Auswahl-Zeile erscheint nur bei Mehrfachzonen-Artikeln (Einzelzonen-Artikel wie `EDS-205` bleiben unverändert, Zeile bleibt versteckt); explizite Wahl `klemm_s` für die PT-Klemme wird korrekt in Belegung, Platzierung (`queues.klemm_s`) und Stückliste übernommen; keine Konsolenfehler.

### Modul 4 – Zone "Fronttafel/Tür" + Kategorie-Korrekturen (Session 43, gesperrt)
Direkte Fortsetzung von Session 42 – Nutzer prüft die Zone-Filterung („Automation = Steuerung") und findet weitere Fehlzuordnungen. **Klärung der 3-Felder-Verwirrung (Nutzerfrage):** `bauteil_typ` wird nur für zwei Dinge ausgewertet – (1) `isDdcSupplyTyp()` unterscheidet DDC-Kapazität (`ddc_io`/`ddc_cpu`) von -Bedarf, (2) `kurzLabel()` liefert das SVG-Kurzlabel. **Hat keinerlei Einfluss auf die Dropdown-Filterung** – die läuft ausschließlich über `kategorie` (Optgroup) + `zone` (Zonen-Filter-Chips), verifiziert direkt gegen `populateEinzelAuswahl()`.

- **Neue Zone `tuer` („Fronttafel/Tür")** für Bauteile ohne Montageplatten-Platzbedarf (`keine_platzierung_mp`). Bewusst NICHT in `ALLE_ZONEN`/`ZONE_LABELS`/`ZONE_COLORS` aufgenommen – diese Konstanten sind laut Kommentar „einzige Quelle" für physische Zonen mit SVG-Rects/Füllstand-Kapazität, `tuer` hat keine. Eigener, unabhängiger Filter-Chip `#fs-tuer-mini` (Muster wie `#fs-alle-mini`, kein Balken) im Füllstand-Streifen, nutzt den bereits generischen `setEinzelZone()`-Mechanismus (matcht nur `data-zone`, keine Abhängigkeit von `ALLE_ZONEN`) – keine Änderung an `placeBauteile()`/`buildFuellstand()`/`buildLegend()` nötig oder gewünscht. Referenz-Sheet `zonen` um `tuer`/„Fronttafel/Tür" ergänzt.
- `3LD2504-0TK51` (Hauptschalter Fronttafeleinbau): `zone` `evert`→`tuer`.
- `BXT BAS`/`BXT ML4 BE24` (Blitzductor): eigene `kategorie` „Überspannungsschutz" statt der bisherigen „...& Vorsicherung" – hat keine eigene Vorsicherung wie die Haupt-ÜSS-Zeile (952300/5SG1812, die behält die alte Kategorie).
- `EDS-205` + Wachendorff-Gateway (`HD67812-KNX-XXX-B2`): `kategorie` `DDC-Automationseinrichtung`→`Netzwerkeinrichtung` (Netzwerk-/Kommunikationsgeräte, keine DDC-I/O-Kapazität – Prinzip vom Nutzer nur für den Switch genannt, hier konsequent auch aufs Gateway angewendet).
- Signalleuchte grün/rot: `zone` `steuer`→`leist` (funktionale statt physische Zuordnung – bei `keine_platzierung_mp` ohnehin ohne SVG-Auswirkung), `bauteil_typ` `sonstige`→neuer Wert `signalleuchte` (bündelt künftig auch die noch offene Phasenkontrollleuchte).
- LVB-Relais (`110661`, `110730`) + Koppelrelais (`PLC-RSC-24DC/21`) in einer `kategorie` „Koppelrelais" zusammengeführt – `lvb_integriert` bleibt die technische Unterscheidung, kein Informationsverlust.

**Bewusst zurückgestellt (Nutzer-Vorgabe „erst morgen, wegen Kontingentverbrauch"):** ein „Info-Feature", das `keine_platzierung_mp` in der Excel-Tabelle selbst sichtbar/erkennbar macht (aktuell nur im `quelle_hinweis`-Freitext erkennbar) – noch nicht spezifiziert, nächste Sitzung.

Verifiziert direkt im Browser: Zonen-Filter „Tür" zeigt korrekt genau den Hauptschalter; alle 9 geänderten Einträge gegen `EINZELBAUTEILE_DB` geprüft (zone/kategorie/bauteil_typ wie vorgesehen); neue Kategorien „Netzwerkeinrichtung"/„Überspannungsschutz" erscheinen, „LVB-Relais (Vorrangbedienung)" als eigene Kategorie korrekt verschwunden; keine Konsolenfehler.

### Katalog: Zonen-/Kategorie-Korrekturen + erste Türbauteile (Session 42, gesperrt/teilweise offen)
Nutzer geht die Excel-Tabelle händisch durch und meldet gezielte Korrekturen + neue Bauteile.

**Korrekturen (umgesetzt):**
- `3RH2911-1FA22` (Hilfsschalterblock): `bauteil_typ` `sonstige`→`schuetz` – funktioniert nur zusammen mit einem Schütz, gehört fachlich dorthin.
- `BXT BAS`/`BXT ML4 BE24` (Dehn BLITZDUCTOR XT): `zone` `uss`→`steuer` – Feinschutz für Einzeladern sitzt im Automationsfeld (Steuerbaugruppe/DDC), nicht an der Haupteinspeisung/ÜSS.
- Wachendorff-Gateway `HD67812-KNX-XXX-B2`: `kategorie` ergänzt (`DDC-Automationseinrichtung`) – Zone war bereits korrekt `steuer`.
- Moxa-Switch: `EDS-208A`→`EDS-205` umbenannt (vom Nutzer explizit benanntes Modell), Maße jetzt verifiziert (moxa.com: 24,9×100×74mm B×T×H), `aktiv=true`. Preis weiterhin offen (nicht auf moxa.com gelistet).
- 7× Leitungsschutzschalter (`5SL6...`): `zone` `leist`→`evert` – gehören zur Energieverteilung, nicht zur Leistungsbaugruppe.

**Neue Kategorie `Fronttafel-/Türeinbau`** + Konzept „Türbauteile": Bauteile, die im Türblatt statt auf der Montageplatte sitzen, nutzen das bestehende `keine_platzierung_mp`-Feld (Session 41 Nachtrag 4/5, ursprünglich für den aufgesteckten Hilfsschalterblock gedacht) – kein neues Schema nötig, gleiche Semantik: keine SVG-Platzierung, erscheint aber in der Stückliste.

**3 neue Katalogeinträge (umgesetzt):**
- `3LD2504-0TK51` (Siemens Hauptschalter 3-polig 63A/22kW, Fronttafeleinbau mit Drehantrieb) – 90×106×110,5mm, 65,69€ inkl. MwSt (alles-mit-stecker.de, kein bestätigter Siemens-Listenpreis), `keine_platzierung_mp=true`.
- `3SU1102-6AA40-3AA0`/`3SU1102-6AA20-3AA0` (Siemens SIRIUS ACT Signalleuchte 22mm grün/rot, 24V AC/DC) – `b_mm`/`h_mm`=22 (Ausschnitt-Ø, keine reale Rechteckgröße), grün mit Preis (27,48€ exkl. MwSt, best4automation.com), rot ohne Preis (Bestellnummer nach Siemens-Nomenklaturmuster abgeleitet, nicht einzeln gegengeprüft).

**Bewusst NICHT hinzugefügt (Datenlage zu dünn, keine geratenen Werte):**
- **Touchscreen:** Kandidat Siemens SIMATIC KTP400 Basic PN (`6AV2123-2DB03-0AX0`) gefunden, aber weder Maße noch Herstellerlistenpreis bestätigt (nur ein Gebrauchtmarkt-Preis) – nicht übernommen.
- **Phasenkontrollleuchte weiß:** technische Unklarheit ungelöst – ein einfacher weißer Meldeleuchtenkopf (z. B. Metzler, 22mm, ~6,49–6,99€) ist etwas anderes als ein echtes 3-Phasen-Kontrollgerät (z. B. „RK Phasenkontrollleuchte ATK 25"); welches der Nutzer meint, ist offen.
- **Störentriegelungstaster:** Kandidat Siemens SIRIUS ACT Leuchtdrucktaste gelb `3SU1156-0AB30-1BA0` gefunden, Preis nicht verifiziert.
- **Phasenwächter:** Kandidat Siemens `3UG4512-2AR20`, Maße nur von einem verwandten 3UG4-Modell (3UG4815, andere Bauform) übernommen, nicht für dieses Modell einzeln bestätigt.
- **Hauptschalter Grundplattenmontage mit Welle zur Fronttür:** nur Zubehörteile gefunden (Türkupplungsdrehantrieb `3LD9343-2CA`, Verlängerungsachse 600mm `3LD9345-1C`, ~22,83€/Stk aus 5er-Pack), der eigentliche Grundplatten-Schalterkörper (mit Montageplatten-Platzbedarf, wie vom Nutzer gefordert) noch nicht identifiziert.
- **3-phasiger Steuertrafo 400V/400V:** kein bestätigtes Siemens-Katalogprodukt gefunden – Siemens-4AP-Baureihe sind Stufentransformatoren (z. B. 400V→230V/115V), kein 1:1-Trenntransformator; unklar ob der Nutzer tatsächlich ein 1:1-Trenntransformator (galvanische Trennung, dann ggf. Planungsfabrikat-Ausnahme wie beim LVB-Relais nötig) oder einen Stufentrafo meint.
- **Bediengerät vs. Touchscreen:** beide Begriffe vom Nutzer als zwei getrennte Positionen genannt, aber unklar was ein "Bediengerät" ohne Touch/Display konkret sein soll (Siemens führt aktuell kaum noch einfache Nicht-Touch-Basic-Panels).

**Preisrecherche „fast überall fehlt der Preis":** 70 von 98 damals aktiven Bauteilen ohne `preis_eur` – bewusst NICHT in dieser Session pauschal abgearbeitet (zu großer Umfang für eine Sitzung, Risiko oberflächlicher/falscher Recherche). Größter Einzelblock: 41 Phoenix-Contact-UT/PT-Klemmen (nur ~10 tatsächliche Preis-Lookups nötig, da Farbvarianten derselben Baugröße meist gleich bepreist sind). Verbleibt offene Folgeaufgabe.

Verifiziert: `xlsx_to_json.py` neu exportiert (102 aktive Bauteile), alle 9 geänderten/neuen Einträge per Skript gegen die JSON-Ausgabe gegengeprüft, Modul 4 im Browser fehlerfrei geladen (102/102 im Dropdown, keine Konsolenfehler).

### Modul 4 – Statistik-Chips: Mindestbreite gegen Prozent-Überlauf (Session 41 Nachtrag 8, gesperrt)
Nutzer-Fund unmittelbar nach Nachtrag 7: die Prozentangaben in den Statistik-Chips liefen über den Chip-Rahmen hinaus. Ursache: `grid-template-columns:auto repeat(4,minmax(0,1fr))` – der explizite `0`-Mindestwert überschreibt für Grid-Spalten die sonst übliche inhaltsbasierte Mindestgröße, wodurch die Spalte schmaler werden kann als der `white-space:nowrap`-Chip-Text, der dadurch sichtbar über die Spaltengrenze hinausläuft (Chip-Hintergrund/-Rahmen bleiben schmal, Text ragt heraus).
- **Fix:** `minmax(0,1fr)` → `minmax(108px,1fr)` – 108px wurde direkt im Browser gegen den ungünstigsten realistischen Chip-Inhalt gemessen (`"BO 999/999 · 100%"`, dreistelliger Datenpunktwert, 100% als vom Nutzer vorgegebener Auslastungs-Höchstwert), 103,86px gemessen + Puffer aufgerundet.
- **`.eb-block-statistik` von `flex:0 1 380px` auf `flex:0 0 600px`** (fix, kein Schrumpfen mehr) – 380px reichte nicht für 5 Spalten (Label + 4×108px + 4×8px Gap ≈ 573px Bedarf). Nutzer-Vorgabe: das Eingabefeld darf dafür schmaler werden, „da ist ja Platz genug" – `.eb-block-eingabe` (`flex:1 1 420px`) gibt automatisch nach, ohne dass Funktionsbereich-Tabs, Baugruppen- oder Einzelbauteil-Auswahl umbrechen (bei 1920px verifiziert: Eingabe-Block schrumpft von ~1144px auf 824px, alle Elemente bleiben einzeilig und innerhalb des Blocks).
- Verifiziert direkt im Browser: synthetischer Extremfall (alle 16 Chips auf `used:999,cap:999` gesetzt) → `overflowingCount:0` (vorher 16/16 liefen über); reale Werte (TXM-Modul-Test) unverändert korrekt dargestellt; kein horizontaler Overflow der gesamten Eingabeleiste bei 1920px.

### Modul 4 – Statistik spaltengenau ausgerichtet, Datenpunkttyp-Farbschema, Eingabeleiste kompakter (Session 41 Nachtrag 7, gesperrt)
Nutzer-Fund per Screenshot bei 1920px (direkte Fortsetzung von Nachtrag 6): das 3-Blöcke-Layout funktionierte, aber drei Feinheiten störten – Statistik hatte deutlich mehr Breite reserviert als sie brauchte, die letzte Zeile der Grundeingaben ließ sich noch einsparen, und die 4 Statistik-Gruppen (Physikalisch + 3× Kommunikativ) standen als lose Flex-Zeilen nicht spaltengenau untereinander.

**Spaltengenaue Statistik-Tabelle:** `.ddc-summary-row` von `flex-direction:column` (Nachtrag 6) auf `display:grid;grid-template-columns:auto repeat(4,minmax(0,1fr))` umgestellt. Jede der 4 Gruppen (`.ddc-summary-grp`) bekommt `display:contents` – dadurch werden ihre Kinder (Gruppenlabel + 4 Chips AI/AO/BI/BO) direkte Grid-Items der Elternzeile und richten sich automatisch spaltengenau an allen 4 Zeilen aus, ganz ohne echtes `<table>`-Markup. `ddcChip()`/`updateDdcSummary()` unverändert in der Aufrufreihenfolge, nur das umgebende Markup nutzt jetzt diese Grid-Struktur.

**Datenpunkttyp-Farbschema, zentral gespeichert – gilt für Rahmen UND Text, unabhängig ob physikalisch oder kommunikativ:**
```
--dp-ai: #A374E0  Violett      --dp-bi: #4E8FE0  Blau
--dp-ao: #E07BB0  Rosa         --dp-bo: #DE5B54  Rot
```
Als CSS-Variablen in `:root` UND als JS-Konstante `DP_TYPE_COLORS` (identische Werte, `:root` ist die primäre Quelle, JS-Konstante nur für den Fall künftiger JS-seitiger Nutzung) – `.dp-ai/.dp-ao/.dp-bi/.dp-bo`-Klassen setzen `border-color`+`color`. `ddcChip()` leitet die Klasse aus dem übergebenen Label ab (`'dp-' + lbl.toLowerCase()`), greift dadurch identisch für alle 4 Gruppen. **Status (Warn/Overflow) bewusst getrennt von der Typfarbe:** `.ddc-chip-warn`/`.ddc-chip-over` färben nicht mehr Rahmen/Text um, sondern nur `background`-Tönung + `font-weight` – sonst wäre ein überlasteter BO-Chip (Typfarbe bereits Rot) nicht von der allgemeinen Überlastungs-Warnung unterscheidbar gewesen.

**Eingabeleiste kompakter – echte Ursache war ein Zeilenumbruch, nicht nur die Zeilenanzahl:** „Reserve Datenpunkte (%)" aus der bisherigen 3. Zeile des Grund-Blocks in die 2. Zeile verschoben (jetzt Klemmraum + Reserve Schaltschrank + Reserve Datenpunkte in einer Zeile) – das allein änderte die Gesamthöhe der Eingabeleiste zunächst NICHT (`leisteHeight` blieb bei 257px), weil `.eb-block-grund` mit `flex:0 0 360px` zu schmal war, um 3 Felder nebeneinander zu zeigen (Breitenbedarf 433px gegen verfügbare 339px) – die Zeile brach dadurch intern um zwei Zeilen, der vermeintlich eingesparte Zeilenumbruch wanderte nur innerhalb des Blocks statt zu verschwinden. **Fix:** `.eb-block-grund` von 360px auf 460px verbreitert (misst 3 nebeneinanderstehende Felder plus Blockpadding), wodurch Zeile 2 wieder einzeilig wird. `.eb-block-statistik` bleibt bei `flex:0 1 380px` (kein Wachstum über den tatsächlichen Bedarf hinaus), `.eb-block-eingabe` bleibt `flex:1 1 420px` (wächst weiter mit dem verbleibenden Platz).

Verifiziert direkt gegen die produktiven Funktionen im Browser (1920px, synthetisches Testgerät `TEST-PUMPE` mit physikalischem + kommunikativem Modbus-RTU-Bedarf, plus TXM1.6R für reale Statistik-Werte): Grid-Spaltenausrichtung exakt (`aiLeftsAligned:true`, `boRightsAligned:true` – linke/rechte Kante aller 4 AI- bzw. BO-Chips pixelgleich); Chip-Klassen korrekt (`ddc-chip dp-ai ddc-chip-ok` usw.); Gesamthöhe `.eingabeleiste` sinkt durch den Breiten-Fix von 257px auf 201,75px – die vom Nutzer gewünschte zusätzliche Zeile für die Schranksicht ist damit real vorhanden (nicht nur verschoben). Bei 1280px Breite bleibt der bereits in Nachtrag 6 dokumentierte, unabhängige `.panel-mid`-Overflow bestehen (nicht Teil dieser Änderung, weiterhin bewusst nicht behoben).

### Modul 4 – Eingabeleiste 3-Blöcke-Layout (Session 41 Nachtrag 6, gesperrt)
Nutzer-Fund per Screenshot: die neue, 16 Chips umfassende DDC-Statistik (Session 41 Nachtrag) hat die Baugruppen-/Einzelbauteil-Auswahl aus dem sichtbaren Bereich gedrängt – derselbe Grundfehler wie schon bei den Funktionsbereich-Tabs in Session 40 (eine Grid-Spalte mit `max-content`-Breite lässt Flex-Wrap-Kinder nicht wirklich umbrechen, die Spalte wächst stattdessen unbegrenzt).

**Fix – komplette Neuordnung der `.eingabeleiste` auf 3 feste Blöcke nebeneinander** (löst das 2-zeilige Grid aus Session 28f endgültig ab):
- `.eingabeleiste{display:flex;flex-wrap:wrap}` statt `display:grid` mit `max-content`-Spalte.
- Jeder Block (`.eb-block`) ein Flex-Kind mit `min-width:0` und eigenem `flex-basis` (`eb-block-grund` fest 360px, `eb-block-statistik`/`eb-block-eingabe` flexibel mit Mindestbreite) – das ist der eigentliche Fix: Flex-Kinder mit `min-width:0` respektieren die Elternbreite und brechen intern um, eine `max-content`-Grid-Spalte tut das nicht.
- **Block 1 „Grund- & Reserveangaben":** Schranktyp, Montagebereich, Klemmraum, Reserve Schaltschrank, Reserve Datenpunkte – in 3 Zeilen (2+2+1) gruppiert, Blockbreite 360px so gewählt, dass genau 2 Felder pro Zeile nebeneinanderpassen (erster Versuch mit 300px brach jedes Feld einzeln um, dadurch 5 statt 3 Zeilen – zu hoch).
- **Block 2 „Statistik":** DDC-Automationseinrichtung – `.ddc-summary-row` von `flex-wrap` auf `flex-direction:column` umgestellt, jede der 4 Gruppen (Physikalisch + 3× Kommunikativ) bekommt jetzt ihre eigene Zeile statt gemeinsam zu fließen – bleibt dadurch unabhängig von der Blockbreite lesbar.
- **Block 3 „Eingabe · Funktionsbereich":** Funktionsbereich-Tabs, Baugruppe, Einzelbauteile (inkl. DDC-Aufschaltungs-Zeile) – jetzt untereinander statt nebeneinander in eigener Spalte.
- Alle IDs unverändert (`schrank_typ`, `bg_auswahl`, `einzel_auswahl`, `ddc-summary-row` usw.) – reine HTML-Umgruppierung/CSS-Neubau, keine JS-Änderungen nötig.

Verifiziert im Browser (1920px, mit synthetischem Testgerät + TXM-Modul für realistische DDC-Daten): alle 3 Blöcke nebeneinander, keiner überschreitet den Viewport (`allWithinViewport:true` für Funktionsbereich-Tabs, Baugruppe-Feld, Einzelbauteil-Feld, „−"-Button); die 4 Statistik-Gruppen stapeln sich korrekt einzeln (top-Werte 180/208/236/264px), Inhalt (701px) passt in den Block (742px). Bei 1920px und 1280px kein horizontaler Overflow durch die Eingabeleiste selbst.

**Nebenbefund, nicht behoben (außerhalb des heutigen Auftrags):** bei 1280px Breite überschreitet `.panel-mid` (Schranksicht/SVG-Bereich) den Viewport unabhängig von der Eingabeleiste und auch mit leerer Belegung – vorbestehendes, von der heutigen Änderung unabhängiges Verhalten, nicht weiter untersucht.

### Schütz-Zubehör: Hilfsschalterblock als automatische Grundausstattung, Motorschutzschalter ergänzt, S0-Maße korrigiert (Session 41 Nachtrag 4+5, gesperrt)
Direkte Fortsetzung. Nutzer-Fund: die neu ergänzten Schütze haben nur Leistungs- und Spulenanschlüsse, keine Hilfskontakte – für eine DDC-Rückmeldung (Betrieb/Störung) wird aber mindestens ein Hilfskontakt gebraucht. Lösung ist ein aufsteckbarer Hilfsschalterblock, der laut Nutzer nur in der Höhe aufbaut und keinen eigenen Platz auf der Montageplatte braucht – „soll nicht dargestellt werden, taucht nur in der Bauteilliste auf".

**Verifizierte S0-Maße nachgetragen:** `3RT2023-1BB40`/`3RT2025-1BB40` (bestehend) sowie alle 6 in Nachtrag 3 neu ergänzten S0-Schütze (`3RT2024`/`3RT2025`/`3RT2026`/`3RT2027`, je AB00/AP00-Variante) von der ursprünglichen Näherung (54×80mm) bzw. vorläufigen Schätzung (45×85mm) auf **45×102mm** korrigiert – direkt am eigenen Katalogeintrag `3RT2025-1BB40` verifiziert (102×45×97mm B×H×T, RS Components/Conrad-Datenblatt).

**Neues Feld `keine_platzierung_mp`** (Boolean, `einzelbauteile`): Bauteil wird auf ein anderes Bauteil aufgesteckt, braucht kein eigenes TE-Feld auf der Montageplatte. In Modul 4 (`placeBauteile()`) wird ein so geflaggtes Bauteil **nicht** in `queues[zone]` eingereiht (keine SVG-Grafik), erscheint aber unverändert in der Stückliste – `aggregateStueckliste()` baut ohnehin unabhängig von der Platzierung direkt aus `belegung`/`baugruppen` auf (Session 28j), daher kein Sonderfall dort nötig. Erster Eintrag: `3RH2911-1FA22` (Hilfsschalterblock, 2S+2Ö, frontseitig aufsteckbar, baugrößenunabhängig für S00/S0/S2 – EIN Bestellnummer deckt alle unsere Schütz-Baugrößen ab), Maße 36×37,5mm.

**Kurskorrektur während der Umsetzung (Nutzer):** statt den Hilfsschalterblock manuell auswählbar zu machen, soll er **automatisch jedes Schütz begleiten** („Grundausstattung") – Begründung: DDC-Anbindung funktioniert dann immer, unbenutzte Kontakte sind kein Problem, und das Tool ermittelt ohnehin nur Platzbedarf/Preis, keinen vollständigen Stromlaufplan. Umsetzung:
- Neues Feld `zubehoer_artikel_nr` (Text, `einzelbauteile`) – bei allen 18 Schützen auf `3RH2911-1FA22` gesetzt.
- Neue Funktion `syncZubehoer(eb, delta)`: legt bei positivem `delta` einen eigenen `belegung`-Eintrag für das Zubehör an/erhöht ihn (gleiche Menge wie das Hauptbauteil, ohne eigene UI-Interaktion – kein rowBreak, keine DDC-Aufschaltungs-Wahl, da das Zubehör selbst nicht automationsfähig ist), bei negativem `delta` reduziert/entfernt sie ihn passend (LIFO wie die bestehende Batch-Logik).
- Aufgerufen in `addEinzelbauteil()` (positiv), `removeEinzelbauteilQty()` (negativ, mit der tatsächlich entfernten Menge `menge - remaining`, nicht der angeforderten) und `removeBelegungItem()` (negativ, beim direkten Löschen einer Zeile aus der Belegungsliste – dort zusätzlich `belegung.indexOf(item)` statt des ursprünglichen Index `i` verwendet, da `syncZubehoer` das Array vorher mutieren kann).
- **Bewusst nicht Teil dieser Session:** dieselbe automatische Mitführung für Baugruppen-Bauteile (`bg.bauteile`) – aktuell nicht testbar, da alle Baugruppen leer sind (Session 40); beim Neuaufbau der Baugruppen nachziehen, sobald ein Schütz erstmals wieder Teil einer Baugruppe ist.

**5 neue Motorschutzschalter** (Siemens 3RV2, passend zu den in Nachtrag 3 ergänzten Schütz-Leistungsstufen, bisher endete der Katalog bei 4kW/10A): `3RV2021-4AA20` (10–16A, 5,5kW), `3RV2021-4BA10` (13–20A, 7,5kW, Preis 74,44€ verifiziert), `3RV2021-4DA10` (18–25A, 11kW – Herstellerangabe „Bemessungsbetriebsleistung 11kW" direkt bestätigt, Preis 89,00€), `3RV2031-4EA10` (22–32A, 15kW), `3RV2041-4HA10` (36–50A, 22kW, Maße nicht einzeln bestätigt, von benachbarter Baugröße übernommen).

Verifiziert im Browser: 2× Schütz hinzugefügt → automatisch 2× Hilfsschalterblock in der Belegung; Schütz landet im Schrankbild, Hilfsschalterblock nicht (`placedInSvg:false`); beide korrekt in der Stückliste (`aggregateStueckliste()`). Katalog jetzt 98 aktive Bauteile.

### Schütze vervollständigt: 24V AC + 230V AC über den gesamten Leistungsbereich (Session 41 Nachtrag 3, gesperrt)
Nutzer-Fund: von 5 Schützen im Katalog hatten nur die ersten beiden (3RT2015, 3kW) eine Wahl zwischen AC- und DC-Spule; die übrigen (4/5,5/7,5 kW) nur 24V DC. In der Gebäudeautomation werden Schütze aber überwiegend mit Wechselspannung (24V AC oder 230V AC) angesteuert, 230V AC fehlte komplett. Nutzer-Vorgabe: auf Basis 230V (und 24V) Leistungen bis ~25kW schaltbar machen, Recherche bei Siemens (Planungsfabrikat).

**Recherchiert (Siemens SIRIUS 3RT2), 13 neue Katalogeinträge:**
- **S00-Baugröße** (36×70mm, wie bestehende 3RT2015/3RT2016): `3RT2015-1AP01` (3kW, 230V AC), `3RT2016-1AB01` (4kW, 24V AC), `3RT2016-1AP01` (4kW, 230V AC) – alle Bestellnummern direkt bestätigt.
- **S0-Baugröße** (45×85mm, aus zwei unabhängigen Quellen für unterschiedliche Leistungsstufen übereinstimmend bestätigt): `3RT2024-1AB00`/`3RT2024-1AP00` (5,5kW), `3RT2025-1AB00`/`3RT2025-1AP04` (7,5kW) – direkt bestätigt; `3RT2026-1AB00`/`3RT2026-1AP00` (11kW), `3RT2027-1AB00`/`3RT2027-1AP00` (15kW) – Bestellnummer teils nach dem bei 3RT2024/3RT2025 bestätigten Suffix-Muster abgeleitet, nicht für jede einzeln direkt verifiziert (im `quelle_hinweis` vermerkt, vor Bestellung gegenprüfen).
- **S2-Baugröße** (55×130mm, nur eine Quelle mit unklarer Achsbeschriftung, nicht gegengeprüft): `3RT2036-3AB00`/`3RT2036-3AP00` (22kW – der nächste Standard-Leistungsschritt bei Siemens nach 22kW ist 30kW, „25kW" existiert nicht als exakte Kataloggröße).
- **Wichtiger Fund, nicht rückwirkend korrigiert:** die neu bestätigten S0-Maße 45×85mm weichen von den bestehenden `3RT2023-1BB40`/`3RT2025-1BB40`-Einträgen (54×80mm) ab – deren Maße waren von Anfang an nur aus der TE-Breite genähert (`„b_mm = te_breite*18, Näherung"`, Session 20), nie real verifiziert. Nur dokumentiert, nicht angefasst (außerhalb des heutigen Auftrags).
- Alle neuen Einträge: `kategorie:"Schütze"`, `zone:"leist"`, `geprueft:false`.
- Katalog jetzt 92 aktive Bauteile (18 Schütze insgesamt). Verifiziert im Browser: 92/92 im Modul-4-Dropdown, keine Dubletten.

### LVB-Relais: Metz Connect als Ausnahme vom Phoenix-Contact-Planungsfabrikat (Session 41 Nachtrag 2, gesperrt)
Nutzer-Fund: `PLC-RSC-24DC/21` (Phoenix Contact, aktuell einziges aktives Koppelrelais im Katalog) ist ein **einfaches** Koppelrelais – kein LVB-Relais (Lokale Vorrangbedienung). Es fehlen Handschalter und die Rückmeldekontakte, mit denen der Handbetrieb an die DDC zurückgemeldet wird. Ursache: Session-40-Entscheidung „Koppelrelais → Phoenix Contact" wurde zu pauschal getroffen, ohne zu prüfen, ob Phoenix diese spezielle LVB-Funktion überhaupt abdeckt – dabei wurden die zuvor schon im Katalog vorhandenen, passenden Metz-Connect-Einträge `110661`/`110730` fälschlich deaktiviert.
- **Recherche (Session 41):** kein Phoenix-Contact-Äquivalent gefunden (allgemeine Koppelrelais-Palette, RIFLINE-Reihe, direkte Wettbewerber-Suche – alle ohne Treffer für Hand/Auto-Schalter + DDC-Rückmeldung, weder binär noch analog).
- **Fix:** `110661` (KRS-E06, digitale/binäre LVB) und `110730` (KMA-F8, analoge LVB 0–10V) wieder auf `aktiv=true` gesetzt – beide waren bereits korrekt mit Maßen/Beschreibung/Quellenangabe hinterlegt (Session 27, „Nachfolger des BTR-Relais"), nur die Aktivierung fehlte. Beide bekommen jetzt `kategorie:"LVB-Relais (Vorrangbedienung)"` (vorher `None`) und `lvb_integriert:true` (neues Feld aus dem DDC-Aufschaltungs-Feature, siehe oben – konsequent auch hier verwendet).
- **`planungsfabrikate`-Sheet aktualisiert:** bestehende Koppelrelais-Zeile präzisiert auf „Koppelrelais (einfache Schnittstelle, keine LVB-Funktion)" → weiterhin Phoenix Contact; neue eigene Zeile „LVB-Relais (Vorrangbedienung binär/analog...)" → **Metz Connect**, mit Begründung der Ausnahme im Hinweisfeld.
- Katalog jetzt 79 aktive Bauteile (77+2). Verifiziert im Browser: beide Metz-Connect-Einträge korrekt geladen, 79/79 im Modul-4-Dropdown sichtbar.

### Modul 4 – DDC-Aufschaltung physikalisch/kommunikativ je Bauteil, Kommunikative-Datenpunkte-Übersicht (Session 41 Nachtrag, gesperrt)
Direkte Fortsetzung. Nutzer-Vorgabe: die bestehende „DDC-Automationseinrichtung"-Übersicht in der Eingabeleiste zeigte nur physikalische Datenpunkte (AI/AO/BI/BO) – kommunikative fehlten komplett, obwohl das Schema (`dp_fb_*` + `feldbus_protokoll`, Session 41 vormittags) sie bereits trägt. Ziel: prüfbar machen, ob die CPU/Gateway-Kapazität je Protokoll für die Gesamt-Datenpunktmenge reicht, praxisnah je Einzelbauteil entscheidbar (Beispiel Nutzer: „Pumpe 1-stufig" – physikalische Rückmeldung Betrieb/Störung UND/ODER kommunikatives Auslesen von Energiedaten über Modbus RTU).

**Neue UI in der „Spezifische Auswahl Einzelbauteile"-Zeile** (`#ddc_auf_row`, nur sichtbar wenn das gewählte Bauteil `automationsanbindung=true` hat und selbst KEIN DDC-Modul/CPU ist – Module liefern Kapazität, werden nicht „an DDC angeschlossen"):
- Checkbox „DDC physikalisch" – standardmäßig **aktiviert**, abwählbar.
- Checkbox „DDC kommunikativ" – standardmäßig **deaktiviert**.
- Protokoll-`<select>` (M-Bus/Modbus RTU/Modbus TCP/IP) – **nur sichtbar, wenn „kommunikativ" aktiv ist** (`updateDdcProtokollVisibility()`), vorbelegt mit dem ersten in `feldbus_protokoll` des Katalogeintrags genannten Protokoll falls vorhanden.
- Beide Checkboxes unabhängig wählbar: eins, beide oder keins – exakt wie vom Nutzer gefordert.

**Datenmodell:** `belegung`-Einträge (`typ:'einzel'`) bekommen `ddcPhysisch`/`ddcKommunikativ`/`ddcProtokoll` – gilt je Artikel für die **gesamte** Menge (wie `ci`/Farbe), nicht pro Batch; erneutes Hinzufügen mit anderer Checkbox-Wahl überschreibt die Wahl für den ganzen Eintrag (bewusste Vereinfachung, analog zu anderen Item-weiten Feldern). Baugruppen-Bauteile (`bt`) bekommen (noch) keine eigene Aufschaltungs-Wahl – Baugruppen sind aktuell leer, dieselbe Erweiterung (analog zum bestehenden `bt.zone`-Override-Muster) ist ein natürlicher Folge-Schritt sobald Baugruppen wieder existieren.

**`accumulateDp()` grundlegend umgebaut:**
- Neue Konstanten `PHYS_DP_TYPES` (dp_ai/ao/bi/bo) und `FB_DP_TYPES` (dp_fb_ai/ao/bi/bo) statt der bisherigen gemeinsamen `DP_TYPES`-Liste für Kapazitäts-/Bedarfsrechnung. `DP_TYPES`/`DP_LABELS` bleiben für `updateDdcAutoDisplay()`s Label-Lookup bestehen.
- `isDdcSupplyTyp(t)` – neuer Helper (`t==='ddc_io'||t==='ddc_cpu'`), jetzt zentral genutzt in `accumulateDp()` UND `updateDdcAufschaltungUI()`/`addEinzelbauteil()` (vorher war die gleiche Prüfung an zwei Stellen dupliziert).
- Supply-Seite (DDC-Module/CPU): physikalische Kapazität wie bisher in `dpSupply`; kommunikative Kapazität NEU in `fbSupply[protokoll][typ]` – geroutet über `eb.feldbus_protokoll` (Komma-getrennt möglich, jedes genannte Protokoll bekommt die volle Kapazität gutgeschrieben – bewusste Vereinfachung für Module, die mehrere Transportwege am selben Punktepool anbieten, dokumentierte Grenze: kein Modul im Katalog hat aktuell echte `dp_fb_*`-Werte, daher noch nicht in der Praxis relevant).
- Demand-Seite (Feldgeräte): `opts.physisch`/`opts.kommunikativ`/`opts.protokoll` aus dem Belegungseintrag steuern, ob `dpDemand` (physikalisch) und/oder `fbDemand[protokoll]` (kommunikativ) erhöht werden. Baugruppen-Bauteile ohne `opts` verhalten sich wie bisher (physisch immer, kommunikativ nie – mangels Protokoll-Angabe).

**`computeDdcAutoModules()` auf `PHYS_DP_TYPES` beschränkt** (vorher liefen dp_fb_* mit durch die Funktion, obwohl `dpDemand`/`dpSupply` dafür gar keine Werte mehr hatten – hätte sonst zu einer dauerhaften Fehlwarnung „kein passendes Modul" für alle vier Feldbus-Typen geführt). **Bewusst keine automatische Modul-Ergänzung für kommunikative Datenpunkte** – dafür gibt es noch keine verifizierten Gateway-Kapazitätsdaten im Katalog; die neue Summen-Anzeige liefert die nötige Sichtbarkeit (rot/amber/ok wie gehabt), der Nutzer wählt bei Bedarf manuell ein passendes Modul.

**`updateDdcSummary()` zeigt jetzt 4 Gruppen** statt einer: „Physikalisch" (wie bisher AI/AO/BI/BO) + `FB_SUMMARY_GROUPS` („Komm. M-Bus", „Komm. Modbus RTU", „Komm. Modbus TCP/IP", je AI/AO/BI/BO) – 16 Chips gesamt, in eigene `.ddc-summary-grp`-Container mit `.ddc-grp-lbl`-Gruppenbeschriftung gruppiert (der äußere Flex-Container umbricht ganze Gruppen zeilenweise). `ddcChip()`-Hilfsfunktion aus der bisherigen Inline-Logik extrahiert, jetzt von allen 4 Gruppen wiederverwendet.

**Excel-Schema:** neues Feld `dp_beschreibung` (Freitext-Bemerkungsfeld, `einzelbauteile`) – erklärt in Klartext, welche konkreten Datenpunkte sich hinter den `dp_*`/`dp_fb_*`-Zahlen verbergen (Nutzer-Vorgabe, Beispiel: „physikalisch: BI=Rückmeldung Betrieb, BI=Rückmeldung Störung; kommunikativ (Modbus RTU): AI=Wirkleistung"). Noch bei keinem Katalogeintrag befüllt (keine echten Feldgeräte mit Datenpunkt-Bedarf im Katalog – nur die Supply-Seite TXM/PXC existiert bisher).

**Bewusst nicht Teil dieser Erweiterung:** automatische Modul-Ergänzung für kommunikative Kapazität (s. o.); DDC-Aufschaltung auf Baugruppen-Bauteil-Ebene (`baugruppen_bauteile`); ein Bauteil mit MEHREREN gleichzeitig unterstützten Protokollen (aktuell genau ein Protokoll pro Belegungseintrag wählbar).

Verifiziert im Browser mit einem synthetischen Test-Feldgerät (nicht committet, nur In-Memory): 2× physikalische BI + 1× kommunikative AI über Modbus RTU, 3-fach hinzugefügt. Ergebnis exakt wie erwartet: „Physikalisch BI 6/16 · 38%" (Kapazität automatisch durch TXM-Module gedeckt, Regression von `computeDdcAutoModules()` bestätigt funktionsfähig), „Komm. Modbus RTU AI 3/0 · 100%" korrekt rot (`ddc-chip-over`, Bedarf ohne verfügbare Kapazität – genau das gewünschte Signal „hier fehlt noch Kapazität"), M-Bus und Modbus TCP/IP korrekt unberührt bei 0/0. UI-Sichtbarkeits-/Checkbox-Verhalten (Zeile erscheint nur bei DDC-fähigen Feldgeräten, Protokoll-Auswahl nur bei aktivem „kommunikativ") einzeln bestätigt. Keine Konsolenfehler.

### Siemens Desigo PX – Architektur verstanden, PXA30-x korrigiert, TX-I/O-Familie ergänzt (Session 41, gesperrt)
Direkte Fortsetzung von Session 40. Nutzer wollte vor dem Neuaufbau der Baugruppen prüfen, ob das Siemens-Architekturverständnis ausreicht, um Einzelbauteile korrekt zuzuordnen.

**Architektur (recherchiert, vom Nutzer bestätigt):**
- **Ebene 1 – Automationsstation/CPU:** Serie `PXC` (aktuelle Generation PXC3/4/5/7, z. B. `PXC5.E24`, `PXC7.E400L`). Unterscheidet sich in Kommunikationsfähigkeit (nativ BACnet/IP, BACnet/SC, BACnet MS/TP; RS485 für Modbus RTU/TCP eingebaut, bis 500 Punkte) und Datenpunkt-Verarbeitungsumfang (im Namen kodiert, z. B. E400L=400 Punkte, E400S=100 Punkte). Hat **keine eigenen Feld-Anschlussklemmen**.
- **Ebene 2 – Ein-/Ausgabemodule: TX-I/O-Familie (`TXM1.x`), NICHT `PXA30-x`.** Wichtigster Korrekturfund: `PXA30-N` ("Modul für BACnet über Ethernet/IP") und `PXA30-W2` ("Erweiterungsmodul für grafische Web-Funktionen") sind Kommunikations-/HMI-Zusatzkarten für die CPU selbst – **keine physischen I/O-Quellen**, obwohl der alte Katalogeintrag `PXA30-W2` fälschlich "8DI/8DO/4AI/4AO" + `dp_ai/dp_ao/dp_bi/dp_bo`-Kapazität auswies. **Beide Einträge gelöscht.**
- **Datenpunkttyp-Kombination bei TXM-Modulen** genau wie vom Nutzer beschrieben: manche verarbeiten nur einen Typ (`TXM1.8D`/`TXM1.16D` = nur DI, `TXM1.6R`/`TXM1.6R-M` = nur DO), manche sind universell/kombiniert (`TXM1.8U`/`TXM1.8U-ML`, jeder Kanal einzeln als AI/AO/DI/DO konfigurierbar).
- **LVB-Unterscheidung bestätigt** (LVB = „Lokale Vorrangbedienebene", Siemens-eigene TX-I/O-Bedienungsanleitung zitiert): Basisvariante ohne LVB (`TXM1.6R`) vs. `-M`/`-ML`-Suffix **mit** integriertem Wippenschalter Hand/Auto je Kanal (`TXM1.6R-M`, `TXM1.8U-ML`) – bei LVB-Varianten kein externes Koppelrelais (Phoenix PLC-RSC) nötig, sonst schon.
- **Alle TXM1.x-Module dieser Baugröße teilen sich dasselbe Gehäuse** 64×77,5mm (B×H, über zwei unabhängige Quellen bestätigt) – unabhängig vom Datenpunkttyp/-anzahl.

**Neue Felder `einzelbauteile` (Session 41):**
- `feldbus_protokoll` (Text, z. B. "modbus_rtu,modbus_tcp") – ergänzt `dp_fb_ai/ao/bi/bo`: welches Protokoll dieser Bedarf/diese Kapazität nutzt. **Noch nicht in Modul 4 ausgewertet** (Modul pausiert) – Nutzer-Vorgabe: das Protokoll muss künftig zur Laufzeit auswählbar sein, damit das richtige Kommunikationsmodul platziert wird. Modbus-Bedarf darf nur durch Modbus-Kapazität gedeckt werden, nicht durch M-Bus o. ä. (analog zur bereits bestehenden Regel „Feldbus-Typ muss exakt passen", Session 28d – hier zusätzlich noch die Protokoll-Dimension).
- `lvb_integriert` (Boolean) – nur bei Ausgabe-fähigen ddc_io-Modulen relevant.
- 6 neue `einzelbauteile`-Zeilen: `TXM1.8D`, `TXM1.16D`, `TXM1.6R` (275€, Siemens-HIT-Listenpreis AT), `TXM1.6R-M` (319€), `TXM1.8U` (404€, universelle Kapazität bewusst NICHT in dp_ai/ao/bi/bo aufgeteilt – Feldstruktur bildet flexible Kanäle nicht ab, offene Modul-4-Erweiterung), `TXM1.8U-ML`.

**Bewusst offen gelassen, nicht geraten:**
- **M-Bus-Modul für aktuelle PXC5/7-Generation:** nur für die ältere `PXC..D`-Baureihe ein Modul (`PXA40-RS`) gefunden, für die aktuelle Generation keine Bestätigung – nicht hinzugefügt.
- **PXC-Controller selbst:** keine Gehäusemaße auffindbar (HIT-Portal weiterhin nicht per WebFetch nutzbar, mehrere Versuche über verschiedene URL-Pfade, alle 403/leere JS-Hülle) – noch nicht im Katalog. Muss vor der ersten Baugruppen-Neuanlage nachgeholt werden (jede Baugruppe mit DDC-Anbindung braucht mindestens 1 CPU + passende TXM-Module).

**Katalog-Strukturaudit (76 aktive Bauteile nach dieser Session):** 0 doppelte `artikel_nr`, 0 fehlende `zone`/`b_mm`/`h_mm` (strukturell vollständig), **51 ohne `preis_eur`**, **0 mit `geprueft=true`** (noch kein einziges Bauteil von Menschenhand verifiziert).

**Nachtrag (gleicher Tag): PXC-Controller ergänzt.** Nutzer bestätigt: eine Datenpunkt-Sammlung über I/O-Module braucht zwingend eine Ebene-1-CPU. `PXC5.E24` blieb trotz vieler weiterer Versuche (HIT-Portal, support.industry.siemens.com, sid.siemens.com, cache.industry.siemens.com, eibabo.com – durchgehend 403/blockiert oder nur unlabeled/widersprüchliche Zahlenkolonnen in Suchergebnissen) unverifizierbar. Stattdessen **`PXC4.E16`** aufgenommen – Gehäusemaße 198×124×71mm über mehrere unabhängige, sauber beschriftete Quellen bestätigt. Neuer `bauteil_typ`-Wert **`ddc_cpu`** (getrennt von `ddc_io`): liefert wie TXM-Module Datenpunkt-Kapazität, wird aber in `computeDdcAutoModules()` bewusst NICHT als Auto-Platzierungs-Kandidat geführt (keine automatische CPU-Vervielfachung – eine CPU wird einmal manuell gewählt). **Dabei Bug gefunden+gefixt:** `accumulateDp()` prüfte nur `bauteil_typ==='ddc_io'` für die Supply/Demand-Zuordnung – ohne Fix wären die 4 Onboard-Relaisausgänge der CPU fälschlich als Bedarf statt Kapazität gezählt worden. Jetzt `['ddc_io','ddc_cpu'].includes(...)`. `kurzLabel()` um `ddc_cpu:'CPU'` ergänzt. 12 der 16 Onboard-Punkte sind „universell" (gleiche dp_*-Einschränkung wie `TXM1.8U`, bewusst nicht aufgeteilt) – nur die 4 festen Relaisausgänge als `dp_bo=4` erfasst. Unterstützt bis zu 4 TXM-Module / max. 40 I/O-Punkte gesamt – Kapazitätsgrenze pro CPU, relevant für spätere Modul-4-Logik. Preis 1.159,26€ von einem Elektro-Distributor (etoh24.de), **kein bestätigter Siemens-Herstellerlistenpreis** wie bei den TXM-Modulen. Verifiziert im Browser: 77/77 Bauteile im Dropdown, `accumulateDp()`-Fix mit Testaufruf bestätigt (dp_bo zählt korrekt als Supply).

**Nachtrag (gleicher Tag): `kategorie`-Lücke geschlossen.** Nutzer-Vorgabe: „Wenn die Kategorie wichtig ist, sollte sie zuerst befüllt werden. Sonst können wir die Daten ja nicht nutzen." Alle 17 betroffenen Bauteile (5× Schütze, 4× Motorschutzschalter, 7× Leitungsschutzschalter, 1× Koppelrelais) haben jetzt eine `kategorie` – neue Kategorienamen `Schütze`, `Motorschutzschalter`, `Leitungsschutzschalter`, `Koppelrelais` ergänzt (bisherige Kategorien deckten diese Bauteilarten nicht ab). Verifiziert im Browser: `populateEinzelAuswahl()`-Dropdown zeigt jetzt korrekt 76/76 Bauteile (vorher fehlten diese 17 wegen des Session-40-Funds `filter(e => e.kategorie && ...)` komplett).

**Preisrecherche – Qualitätsunterschied dokumentiert, bewusst nicht pauschal aufgefüllt:** Siemens-Preise über HIT-Portal als echte Herstellerlistenpreise erreichbar (3 TXM-Module damit bepreist). Für Phoenix Contact/Dehn nur Händler-Straßenpreise (inkl. MwSt./Handelsspanne) auffindbar, kein öffentliches Herstellerpreisportal gefunden – nicht unter `preis_eur` eingetragen, um Preisqualitäten nicht zu vermischen. Verbleibt offene Aufgabe, u. a. 25 UT-Einspeiseklemmen (5 Baugrößen), diverse Dehn-/Siemens-Einzelteile.

### Excel-Feldklärungen, Klartext-Spalten, Planungsfabrikate, erste Katalogbereinigung (Session 40, gesperrt)
Direkte Fortsetzung von Session 39 – Nutzer hat sich die Excel-Datei angesehen und gezielt zu einzelnen Feldern nachgefragt.

**Feldklärungen `einzelbauteile` (verifiziert gegen den tatsächlichen Code, nicht aus dem Gedächtnis):**
- `bauteil_typ` ist erforderlich – zwei konkrete Verwendungen in Modul 4: (1) unterscheidet DDC-Kapazität von DDC-Bedarf (`bauteil_typ==='ddc_io'`), (2) liefert das Kurz-Label auf dem platzierten Block (`kurzLabel()`). Fund: 4 von 11 `bauteil_typ`-Werten (`ddc_io`, `lasttrenner`, `ueberspannung`, `sicherung`) hatten kein Label und fielen auf die ersten 4 Zeichen der Bezeichnung zurück – ergänzt (DDC/LT/ÜSS/Sich.).
- `kategorie` ≠ `zone` – `kategorie` ist eine rein optische `<optgroup>`-Gruppierung im Direktbauteil-Dropdown (Modul 4), unabhängig von der physischen Platzierungszone. **Fund:** `populateEinzelAuswahl()` filtert Bauteile OHNE `kategorie` komplett aus dem Dropdown heraus (`filter(e => e.kategorie && ...)`), nicht nur ungruppiert – betraf 20 von 76 Bauteilen (v. a. Schütze, Motorschutzschalter, LSS, Koppelrelais), bisher folgenlos, da diese Typen nur über Baugruppen verwendet werden. Muss bei der geplanten Katalogbereinigung mit behoben werden (jedes Bauteil braucht eine `kategorie`).
- `einbaulage` ist rein beschreibend, wird nirgends in der Berechnung ausgewertet (nur Anzeige in Modul 7 falls vorhanden), aktuell 0/76 befüllt. Nicht erforderlich.
- `automationsanbindung` ist eine Katalogeigenschaft („nimmt an der DDC-Datenpunkt-Bilanz teil"), keine Laufzeitentscheidung – die automatische DDC-Modul-Ergänzung läuft bereits vollautomatisch (`computeDdcAutoModules()`, Session 28d). Nur 1 von 76 Bauteilen hat das Flag gesetzt (PXA30-W2) – reine Datenlücke, kein Design-Mangel.

**Inline-Klartext-Spalten ergänzt (VLOOKUP-Formeln, keine Auswirkung auf `xlsx_to_json.py` – 0 Diff verifiziert):**
- `einzelbauteile.zone_bezeichnung`, `baugruppen_bauteile.zone_bezeichnung` (gegen `zonen`-Sheet)
- `baugruppen.funktionsbereich_bezeichnung` (gegen `funktionsbereiche`-Sheet)
- Wert erscheint live beim Öffnen in Excel (Formel, keine statischen Werte) – kein manuelles Neu-Berechnen nötig (Excel-Standardeinstellung „Automatisch").

**Neues Referenz-Sheet `planungsfabrikate`:** Kategorie → bevorzugter Hersteller, dokumentiert die bereits gelebte Praxis (Rittal/Schaltschränke, Siemens/Automation+Schütze+Sicherungen, Phoenix Contact/Klemmen+Netzteile, Dehn/Überspannungsschutz) plus die in dieser Session geklärte Zuordnung Koppelrelais/Schnittstellenmodule → **Phoenix Contact** (Nutzer-Entscheidung, Metz-Connect-Bestandsartikel KRS-E06/KMA-F8 auf `aktiv=false` gesetzt statt gelöscht).

**Erste Katalogbereinigung – `reiheneinbaugeraete` vs. `einzelbauteile`:**
- Keine echten Dubletten *innerhalb* von `einzelbauteile` (0 doppelte `artikel_nr` – die scheinbaren „Dopplungen" gleicher Maße sind legitime Farb-/Pol-Varianten, z. B. UT-Klemmen L1/L2/L3/N/PE, nicht anfassen).
- Aber 3 echte Dubletten *zwischen* den Sheets gefunden: Siemens-LSS `5SL6106-7`/`5SL6110-7`/`5SL6116-7` existierten identisch in `reiheneinbaugeraete` UND (besser modelliert, mit echten mm-Maßen + Preis) in `einzelbauteile` – aus `reiheneinbaugeraete` entfernt (24→21 Zeilen).
- Neuer, recherchierter Katalogeintrag `5SL6316-7` (Siemens LSS 3-polig 16 A) in `einzelbauteile` ergänzt – dabei einen Fehler in der Alt-Quelle korrigiert: dort stand „Charakteristik B", mehrere unabhängige Händlerquellen (elektro4000.de u. a.) bestätigen übereinstimmend „Charakteristik C". `h_mm=90` weicht von den bereits vorhandenen 1-/2-poligen 5SL6-Einträgen (`h_mm=81`, ebenfalls `geprueft=false`) ab – Diskrepanz bewusst nicht stillschweigend angeglichen, im `quelle_hinweis` vermerkt.
- **Weiterer Fund (nicht korrigiert, nur dokumentiert):** die verbliebenen `reiheneinbaugeraete`-Altdaten für Siemens `5SV3316-6` (FI-Schutzschalter) tragen `nennstrom_a: 16`, mehrere unabhängige Händlerquellen zeigen aber übereinstimmend 63 A für diese Bestellnummer – Artikelnummer und Stromangabe passen nicht zusammen. Bewusst nicht blind überschrieben (Gefahr, echte Fertigungsdaten falsch zu setzen), siehe „Nächster Schritt" unten.
- **Bewusst nicht abgeschlossen:** die vollständige Ersetzung der übrigen ~18 Eaton-Einträge (Sicherungshalter D01/D02, Hilfskontakte, FI-Schutzschalter) durch Siemens-Äquivalente (Nutzer-Entscheidung: „Ersetzen durch Siemens") – für einige Siemens-Ersatzteile (5SG7113/5SG7133 Neozed-Lasttrennschalter, exakte FI-Schutzschalter-Höhe, 2×Hilfsschalter 5ST3010/5ST3011) konnten keine ausreichend verlässlichen mm-Maße aus Web-Recherche gewonnen werden – bewusst nicht geraten (gesperrte Konvention seit Session 27: „mangels verifizierter Abmessungen aktiv=false statt geraten"). `reiheneinbaugeraete`-Sheet bleibt vorerst bestehen (weiterhin von keinem Modul geladen, daher risikofrei), bis diese Recherche fortgesetzt wird.

**Nachtrag Session 40 (gleicher Tag, direkte Fortsetzung):** Nutzer-Entscheidung „unsichere Funde löschen, nicht auf Verdacht stehen lassen" – die restlichen ~18 Eaton/Siemens-Einträge in `reiheneinbaugeraete` (Sicherungshalter, Hilfskontakte, FI-Schutzschalter) wurden nie von einer einzigen Baugruppe referenziert und blieben trotz weiterer Recherche (Siemens HIT-Portal erneut versucht – weiterhin nicht per WebFetch nutzbar, liefert nur eine leere JS-Hülle bzw. 403 auf die PDF-Datenblatt-Route) mit unsicheren/unauffindbaren Maßen. Statt einzeln weiterzurecherchieren: **Sheet `reiheneinbaugeraete` komplett gelöscht** (inkl. `reiheneinbaugeraete.json`, `export_reiheneinbaugeraete()` aus `xlsx_to_json.py` entfernt) – unverifizierte, nie genutzte Session-20-Altlast. Dabei zusätzlicher Fund: `5SV3316-6` war nicht nur falsch verortet (Dublette), sondern auch mit falschem Nennstrom beschriftet (16 A statt real 63 A) – das echte 16-A-2-polige Pendant heißt `5SV3311-6`, ein 16-A-4-poliges Pendant existiert in der SENTRON-5SV3-Reihe nicht (Baureihe startet 4-polig bei 25/40 A). `kategorie`-Lücke (20 Bauteile ohne Kategorie, dadurch unsichtbar im Modul-4-Dropdown) bleibt offen für die anstehende volle Katalogüberarbeitung.

**Baugruppen komplett gelöscht (Session 40, Nutzer-Entscheidung):** `baugruppen`- und `baugruppen_bauteile`-Sheets geleert (nur Kopfzeile), `baugruppen.json` exportiert jetzt `[]`. Grund: Nutzer baut die Baugruppen von Grund auf neu, nachdem der Einzelbauteile-Katalog sauber/vollständig/verifiziert ist – alle Platzierungslogik in Modul 4 hängt an korrekten Einzelbauteil- und Baugruppen-Definitionen nach Schaltungsverständnis, daher bewusst zuerst die Datengrundlage. Backup vor der Löschung: `C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-baugruppen-loeschung_*.xlsx`. Modul 4 mit leerem `baugruppen.json` noch nicht im Browser gegengetestet (Modul bleibt ohnehin pausiert) – bei Wiederaufnahme prüfen, ob leere Baugruppen-Dropdowns sauber behandelt werden.

### Excel-Konsistenzpflege: fehlende Sheets rekonstruiert, Feldnamen vereinheitlicht, 2 Referenz-Sheets (Session 39, gesperrt)
Nutzer-Entscheidung: Claude pflegt `ga_komponenten.xlsx` ab jetzt direkt (statt nur Recherchewerte zuzuliefern), Nutzer arbeitet nur noch bei Bedarf selbst darin. Ausgangspunkt war eine Nutzerfrage zum Zweck der 7 damaligen Arbeitsblätter – dabei fiel eine strukturelle Lücke auf.

**Begriffsklärung Funktionsbereich vs. Zone (wichtig, wird an mehreren Stellen
durcheinandergebracht – auch vom Nutzer in der Ausgangsfrage):**
- **Funktionsbereich** (`baugruppen.funktionsbereich`/`gewerk`) = DIN-276-Kategorie
  einer ganzen Baugruppe (z. B. „Lüftung"). Existiert NUR bei Baugruppen, nicht bei
  Einzelbauteilen – dasselbe Bauteil (z. B. eine Klemme) wird in ganz
  unterschiedlichen Funktionsbereichen verwendet.
- **Zone** (`einzelbauteile.zone`, `baugruppen_bauteile.zone` als Override) = die
  physische Platzierungszone IM SCHRANK (`klemm_e`/`uss`/`evert`/`leist`/`steuer`/
  `klemm_l`/`klemm_f`/`klemm_s`), unabhängig vom Funktionsbereich. Was der Nutzer in
  seiner Ausgangsfrage bei `einzelbauteile`/`baugruppen_bauteile` als
  „Funktionsbereich, wo das Bauteil platziert werden muss" bezeichnete, ist
  tatsächlich die Zone.

**Kritischer Fund: 4 Datenbanken waren von der Excel-Pipeline abgekoppelt.**
Die Sheets `standschraenke`, `sockel`, `bodenbleche`, `reiheneinbaugeraete`
existierten in `ga_komponenten.xlsx` schlicht nicht mehr (nur noch 6 Sheets
vorhanden), obwohl die zugehörigen JSON-Dateien weiterhin committed sind und
`standschraenke.json`/`sockel.json` produktiv von Modul 2 geladen werden. Diese
4 DBs waren dadurch nur noch per Hand-Edit der JSON-Datei pflegbar – Verstoß
gegen die gesperrte Architekturregel „Excel ist Source of Truth". Ursache nicht
mehr rekonstruierbar (vermutlich beim Anlegen eines neuen `ga_komponenten.xlsx`
zwischenzeitlich nicht mitgenommen). **Fix:** alle 4 Sheets 1:1 aus den bereits
committeten JSON-Dateien rekonstruiert (11/8/4/24 Zeilen) – reine
Wiederherstellung, keine inhaltliche Änderung. `bodenbleche`/`reiheneinbaugeraete`
werden aktuell von keinem Modul geladen (geprüft), sind aber Teil der
dokumentierten Dateistruktur und jetzt wieder korrekt pflegbar.

**Feldnamen-Konsistenz hergestellt (nur Excel-Spalten, JSON-Ausgabeschema
bewusst unverändert – siehe unten):**
- `bestellnummer` (wandschraenke, kabelzugschellen, + die 4 wiederhergestellten
  Sheets) → **`artikel_nr`**, vereinheitlicht mit `einzelbauteile`.
- `preis_stueckpreis_eur` (dieselben Sheets) → **`preis_stueck_eur`**,
  vereinheitlicht mit `einzelbauteile`.
- `aktiv` in `kabel_nym_j`/`kabelzugschellen` war als 1/0 statt Boolean
  gespeichert (funktional identisch, aber uneinheitlich) → auf `True`/`False`
  normalisiert, wie in allen anderen Sheets.
- **Bewusste Entscheidung:** die JSON-Ausgabeschlüssel selbst (`bestellnummer`,
  `preis_stueckpreis_eur`) bleiben unverändert – nur `xlsx_to_json.py`s
  Lese-Seite (`rec['artikel_nr']` statt `rec['bestellnummer']` usw.) wurde
  angepasst. Damit bleibt die Vereinheitlichung auf die Excel-Datei begrenzt,
  ohne Modul-1/2/4/7-JS-Code anzufassen oder JSON-Konsumenten zu brechen. Falls
  gewünscht, ist eine spätere Angleichung auch der JSON-/Modul-Feldnamen ein
  separater, größerer Folge-Schritt (nicht Teil dieser Session).
- Referenzielle Integrität geprüft: 0 verwaiste `artikel_nr` in
  `baugruppen_bauteile` (51/51 lösen auf), 0 verwaiste `bg_id` (bereits bei der
  Session-38-Migration verifiziert).

**Zwei neue reine Referenz-Arbeitsblätter (keine Datenquelle für
`xlsx_to_json.py`, nur Klartext-Nachschlagewerk für die Excel-Pflege von Hand):**
- `funktionsbereiche`: `code` (DIN-276, z. B. `430`), `funktionsbereich`
  (Text-Key wie in `baugruppen.funktionsbereich`, z. B. `lueftung`),
  `bezeichnung` (Klartext, z. B. „Raumlufttechnische Anlagen") – 11 Zeilen,
  siehe Session 38 für die Zuordnung.
- `zonen`: `zone` (Code wie in `einzelbauteile.zone`, z. B. `klemm_l`),
  `bezeichnung` (Klartext aus `ZONE_LABELS` in Modul 3/4, z. B. „Abg.-Kl.
  Leistung") – 8 Zeilen.
- Beide Sheets sind bewusst reine Lese-Hilfen: die Variable/der Code bleibt in
  den Datenspalten (`gewerk`, `funktionsbereich`, `zone`) die tatsächliche
  Datengrundlage; die Klartext-Spalte dient nur der menschlichen Lesbarkeit
  beim manuellen Editieren in Excel.

**Sicherung vor dem Eingriff:** Kopie von `ga_komponenten.xlsx` nach
`C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-konsistenzpflege_*.xlsx`
(die Datei ist nicht git-versioniert, kein anderes Sicherheitsnetz vorhanden).

Verifiziert: `xlsx_to_json.py` neu ausgeführt, alle 9 JSON-Dateien gegen den
committeten Stand geprüft – `wandschraenke.json`, `kabelzugschellen.json`,
`einzelbauteile.json`, `baugruppen.json`, `kabel_nym_j.json` bytegleich (0
Diff trotz Spalten-Umbenennung, bestätigt die chirurgische Read-Side-Änderung);
`standschraenke.json`/`sockel.json`/`bodenbleche.json` nur fehlender
Zeilenumbruch am Dateiende (kosmetisch); `reiheneinbaugeraete.json` verliert
das nie exportierte `aktiv`-Feld (jetzt konsistent mit allen Sibling-DBs) und
zeigt `nennstrom_a` jetzt als Float (`16.0` statt `16`, entspricht dem im
Skript immer schon vorgesehenen `float()`-Cast) – ohne Modul-Ladezugriff ohne
jede Auswirkung. Modul 2 im Browser gegen den lokalen Server getestet: alle 11
Standschränke + beide Sockelhöhen laden korrekt, keine Konsolenfehler, keine
fehlgeschlagenen Requests.

### Baugruppen-Schema: DIN-276-Inhaltsmigration abgeschlossen (Session 38, gesperrt)
Löst den in Session 37 zurückgestellten Folge-Schritt ein: `gewerk` trägt jetzt
den numerischen DIN-276-Code als Text, `id` folgt dem Zielschema
`<Code>_<6-stellig>`. `funktionsbereich` bleibt unverändert der Text-Key für
die Modul-4-Tab-Filterung (war für alle 15 Bestandszeilen ohnehin schon
identisch zum alten `gewerk`-Kurznamen, brauchte keine Änderung).

**Vom Nutzer geklärte offene Fragen aus Session 37:**
- `450 Informations-/Sicherheitstechnik` → Funktionsbereich `netzwerk`. Deckt
  laut Nutzer nicht nur Netzwerktechnik, sondern auch Sicherheitstechnik
  (Brandmelde-/Gefahrenmeldeanlagen) ab – dafür sind aktuell noch keine
  Baugruppen angelegt.
- Der bestehende `schaltschrank`-Tab entfällt ersatzlos, geht inhaltlich in
  `480 Gebäudeautomation` (Funktionsbereich `automation`) auf.
- Nutzer-Hinweis (informativ, keine Code-Konsequenz in dieser Session):
  Gebäudeautomation (480) kann inhaltlich auch Netzwerk-Aspekte umfassen –
  Übereinstimmungen zwischen `automation` und `netzwerk` sind also möglich
  und kein Modellierungsfehler.
- Der in Session 28j als ungeklärt notierte Punkt „Farbe Energieverteilung
  wirkt im Screenshot abweichend von der Legende" ist vom Nutzer als
  erledigt/nicht weiter zu verfolgen bestätigt (Code war bereits korrekt,
  vermutlich reiner Wahrnehmungseffekt) – aus dem offenen Backlog gestrichen.

**Migration `gewerk` → DIN-276-Code (alle 15 Bestandszeilen, per Skript in
`ga_komponenten.xlsx` geschrieben, `~$`-Lockdatei vorher geprüft):**
`lueftung→430` (6×), `heizung→420` (4×), `sanitaer→410` (1×),
`beleuchtung→445` (2×), `elektro→440` (2×). Kein Bestandseintrag trug bisher
`schaltschrank` oder `automation` – die beiden Fälle betreffen aktuell keine
existierenden Baugruppen, nur die Tab-Struktur.

**Migration `id` → `<Code>_<6-stellig>`, Nummerierung je Code fortlaufend in
Blattreihenfolge, `baugruppen_bauteile.bg_id` 1:1 nachgezogen (51 Zeilen):**
```
luefter_1stufig_2kw     → 430_000001    pumpe_1kw       → 420_000001
luefter_1stufig_5kw     → 430_000002    pumpe_3kw       → 420_000002
ventilantrieb_on_off    → 430_000003    pumpe_betr_stoer→ 420_000003
ventilantrieb_stetig    → 430_000004    ventilantrieb_hkl → 420_000004
sensor_passiv_rlt       → 430_000005    pumpe_san_1kw   → 410_000001
sensor_aktiv_24v        → 430_000006    beleuchtung_schaltkreis → 445_000001
lss_abzweig_1p          → 440_000001    dali_segment    → 445_000002
netzteil_24v_60w        → 440_000002
```
`xlsx_to_json.py` brauchte keine Codeänderung (`gewerk`/`id` werden ohnehin
nur als Text durchgereicht) – nur `python3 xlsx_to_json.py` neu ausgeführt.

**Modul 4 – 11 Funktionsbereich-Tabs statt 10, DIN-276-Reihenfolge:**
`sanitaer(410)`, `heizung(420)`, `lueftung(430, weiterhin Default-Tab)`,
`kaelte(434)`, `elektro(440)`, `beleuchtung(445)`, `netzwerk(450)`,
**`aufzug(460)` neu**, `nutzungsspezifisch(470)`, `automation(480)`,
**`sonstige(490)` neu** – `schaltschrank`-Tab entfernt. Jeder Button trägt
zusätzlich ein `title`-Tooltip mit vollem DIN-276-Code+Name. `filterBaugruppen()`
matcht jetzt zwingend `b.funktionsbereich` statt `b.gewerk` (wie in Session 37
als Reihenfolge-Voraussetzung dokumentiert – Tabs zuerst umgestellt, danach
diese Änderung, sonst hätten alle Tabs 0 Treffer gezeigt).

**Bug gefunden + gefixt (unabhängig von der DIN-276-Migration selbst):**
`.gewerk-tabs` nutzte ein festes CSS-Grid (`grid-template-columns:repeat(6,auto)`).
Bei 11 statt 10 Tabs war die Summe der Spaltenbreiten größer als der
320px-Container – CSS Grid mit `auto`-Spalten wraps NICHT automatisch in eine
neue Zeile, wenn der Inhalt nicht passt, sondern überläuft breitenmäßig.
Ergebnis: 5 Tabs (Kälte, Elektro, Beleuchtung, Automation, Sonstige) waren
zwar im DOM vorhanden, aber unsichtbar/nicht klickbar außerhalb des
sichtbaren Bereichs. Fix: `.gewerk-tabs` auf `display:flex;flex-wrap:wrap`
umgestellt – Tabs verteilen sich jetzt automatisch auf so viele Zeilen wie
nötig, unabhängig von der genauen Tab-Anzahl (robuster für künftige
Tab-Änderungen als ein fest kodiertes Spaltenraster).

**Bewusst nicht Teil dieser Session:** Baugruppen für die weiterhin leeren
Funktionsbereiche (`kaelte`, `netzwerk`/Sicherheitstechnik, `aufzug`,
`nutzungsspezifisch`, `automation`, `sonstige`) anlegen – reine
Struktur-/ID-Migration, keine neuen Inhalte. Modul 4 bleibt wie in Session 34
festgelegt pausiert, bis diese Datengrundlage weiter ausgebaut ist.

Verifiziert direkt gegen die produktiven Funktionen im Browser (lokaler
Server, `.claude/launch.json`): alle 11 Tabs im DOM, bei ausreichender
Fensterbreite (≥1920px) alle in einer Zeile sichtbar, bei schmalerer Breite
korrekt mehrzeilig umgebrochen; `filterBaugruppen()` liefert je Tab exakt die
erwarteten Trefferzahlen (sanitaer 1, heizung 4, lueftung 6, elektro 2,
beleuchtung 2, alle sechs neuen/leeren Bereiche 0); End-to-End-Test
`addBaugruppe('430_000001')` platziert korrekt (Belegung, Schranksicht,
Stückliste mit Preisen), keine Konsolenfehler.

### Modul 7 – Fehlerliste kopieren + Recherche-/Korrektur-Workflow (Session 36, gesperrt)
Nutzer-Vorschlag: die Datenqualitäts-Chips (Session 35) zeigen zwar Probleme
an, aber es fehlte ein Weg, eine konkrete Trefferliste (z. B. „Fehlender
Preis") aus dem Browser heraus an Claude zu übergeben, damit dieser dazu im
Netz recherchiert und die Werte direkt in `ga_komponenten.xlsx` einträgt.
- **Neuer Button `📋 Liste kopieren`** (`copyList()`, neben `result-count`):
  kopiert die aktuell gefilterte Liste (respektiert Tab, aktiven DQ-Chip,
  Suche und alle Dropdown-Filter über das bereits vorhandene
  `getFilteredList()`) als einfachen Text in die Zwischenablage. Format:
  Kopfzeile mit Werkzeug-/Filterbezeichnung (`currentFilterLabel()`, baut
  aus `activeFilter`/Suchbegriff/aktiven Selects einen lesbaren Satz wie
  „Fehlender Preis" oder „Zone: Abg.-Kl. Sensoren · Hersteller: Siemens"),
  dann Trefferzahl, dann eine Pipe-getrennte Tabelle (Einzelbauteile:
  Artikel-Nr./Bezeichnung/Hersteller/Bauteil-Typ/Zone – Baugruppen:
  ID/Name/Gewerk/Anzahl Bauteile) – bewusst kein CSV-Datei-Download (wie
  Modul 4s `exportCSV()`), sondern direkt zwischenablage-fähiger Text zum
  Einfügen in den Chat, das ist der eigentliche Anwendungsfall.
- **Zwischenablage-Zugriff zweistufig:** `navigator.clipboard.writeText()`
  zuerst, bei Fehlschlag (z. B. fehlender Fokus/Berechtigung)
  `document.execCommand('copy')` über ein verstecktes Textarea als Fallback
  (`fallbackCopy()`). Beide Pfade im Browser gegen die produktive Funktion
  getestet – die moderne Clipboard-API schlägt in automatisierten
  Testkontexten grundsätzlich mit „Document is not focused" fehl (Browser-
  Sicherheitsmechanismus, kein Bug), der Fallback greift dort zuverlässig;
  bei echter Nutzerinteraktion (Klick im eigenen Browser) hat das Dokument
  Fokus, `writeText()` funktioniert direkt.
- **Vorgesehener Workflow, ab jetzt Standardvorgehen für Katalogpflege:**
  1. Nutzer wählt in Modul 7 einen DQ-Chip oder eigene Filter, klickt
     „Liste kopieren", fügt den Text hier im Chat ein.
  2. Claude recherchiert zu den genannten Artikeln im Netz (WebSearch/
     WebFetch – Herstellerseiten/Distributoren, siehe Session-27-Hinweis:
     Siemens-HIT-Portal funktioniert nicht per WebFetch, auf
     Distributor-Datenblätter ausweichen).
  3. Claude trägt recherchierte Werte **direkt in `ga_komponenten.xlsx`**
     ein (Python/openpyxl, wie schon in Session 27 für neue Katalogeinträge
     praktiziert) – vorher immer auf die `~$ga_komponenten.xlsx`-Lockdatei
     prüfen (Excel-Datei muss geschlossen sein, sonst `PermissionError`).
  4. `python3 xlsx_to_json.py` in WSL ausführen, alle 9 JSON-Dateien neu
     exportieren, committen.
  5. In Modul 7 verifizieren, dass der entsprechende DQ-Chip-Zähler
     gesunken ist (z. B. „Fehlender Preis" von 49 auf einen kleineren Wert).
  Das ändert nichts an der gesperrten Session-35-Architektur (Modul 7
  bleibt rein lesend) – der Schreibzugriff läuft weiterhin außerhalb des
  Browsers, jetzt nur mit einem definierten Übergabeformat statt loser
  Zuruf-Liste.
- Verifiziert direkt gegen die produktiven Funktionen: Filter „Fehlender
  Preis" aktiviert → `currentFilterLabel()` liefert „Fehlender Preis",
  `getFilteredList()` liefert korrekt 49 Treffer; erzeugter Text-Block
  geprüft (Kopfzeilen + Pipe-Tabelle, erste 3 Zeilen inhaltlich korrekt
  gegen die echten Datensätze abgeglichen); Button-Feedback „✓ Kopiert"
  erscheint nach Aufruf über den `execCommand`-Fallback-Pfad.

### Modul 7 – Stammdatenpflege Artikeldaten (Session 35, gesperrt)
Neues Modul, direkt im Anschluss an die Session-34-Pause von Modul 4 gebaut.
**Titel:** „Modul 7 · Stammdatenpflege · Artikeldaten"
**Datei:** `modules/modul-07-stammdatenpflege/index.html`

**Architektur-Entscheidung (mit dem Nutzer geklärt, zentral für dieses
Modul):** Modul 7 ist **rein lesend**. `data/ga_komponenten.xlsx` bleibt die
einzige Stelle, an der Artikel-/Baugruppendaten geändert werden – Modul 7
lädt nur die von `xlsx_to_json.py` bereits exportierten
`einzelbauteile.json`/`baugruppen.json` per `fetch()`, exakt wie jedes
andere DBACS-Modul. Das widerspricht **nicht** der gesperrten
Session-27-Entscheidung „Pflegewerkzeug bleibt Excel, kein eigenes
Editor-Modul" – Modul 7 editiert nichts, es macht nur sichtbar, was in Excel
noch nachgetragen/korrigiert werden sollte. Kein Eingriff in
`xlsx_to_json.py` oder die Excel-Datei.

**Umfang:** nur `einzelbauteile.json` (73 Einträge) + `baugruppen.json`
(15 Einträge) – nicht die übrigen 7 Datenbanken (bewusst zurückgestellt,
falls später gewünscht).

**Drei kombinierte Facetten in einem Werkzeug** (Nutzer: „keine Präferenz"
zwischen den drei Vorschlägen → zu einem Tool kombiniert statt drei
getrennte Screens):
1. **Katalog-Browser:** zwei Tabs (Einzelbauteile/Baugruppen), Volltextsuche
   (Artikel-Nr./Bezeichnung/Hersteller bzw. ID/Name) + Dropdown-Filter
   (Zone/Hersteller/Kategorie/Bauteil-Typ bzw. Gewerk).
2. **Datenqualitäts-Leiste** (`#dq-bar`, `computeDataQuality()`, einmalig
   client-seitig berechnet, keine neue Datenquelle): ungeprüfte
   Einzelbauteile/Baugruppen (`geprueft:false`), Einzelbauteile ohne
   `preis_eur`, verwaiste `artikel_nr`-Referenzen in `baugruppen[].bauteile[]`
   (Artikel, der in keiner `einzelbauteile.json` mehr existiert), Zonen ohne
   Katalogeintrag. Jeder Chip ist zugleich Filter (`applyDQFilter()`) – Klick
   wechselt bei Bedarf den Tab und setzt alle übrigen Filter zurück, damit
   die im Chip genannte Zahl exakt der gefilterten Trefferliste entspricht.
   **Wichtig:** da zum Zeitpunkt des Baus 73/73 Einzelbauteile
   `geprueft:false` waren, ist das bewusst NICHT als Zeile-für-Zeile-
   Warnfarbe umgesetzt (wirkt sonst wie ein kaputtes Modul), sondern nur als
   aggregierte Kennzahl + dezenter grauer `flag-dot` (nicht rot/amber) je
   Zeile. Rot (`flag-dot err`) ist echten Defekten vorbehalten (verwaiste
   Referenz), Amber (`flag-dot warn`) fehlendem Preis.
3. **Verwendungsnachweis:** `USAGE_MAP` (Artikel-Nr. → Liste der
   Baugruppen, die ihn referenzieren, mit Menge/Zone-Override), einmalig in
   `computeDataQuality()` aufgebaut. Detail-Panel eines Einzelbauteils zeigt
   die Liste, jede Zeile klickbar (`jumpTo('baugruppen', bg_id)`) und springt
   zur Baugruppe; deren Detail zeigt umgekehrt die aufgelöste
   Bauteile-Tabelle (Lookup `artikel_nr` → `EINZELBAUTEILE_DB`). Ein nicht
   auflösbarer Eintrag (Orphan) wird direkt dort rot mit „⚠ Nicht im
   Einzelbauteile-Katalog gefunden" markiert – macht den Datenqualitäts-Fall
   exakt an der Stelle sichtbar, wo die fehlerhafte Referenz liegt.

**Feld-Definitionen datengetrieben, nicht hartcodiert pro Objekt:**
`FIELD_DEFS_EB`/`FIELD_DEFS_BG` (Array aus `{k, l, f}` – Key, Label,
optionale Formatierfunktion), `renderFieldTable()` rendert eine Zeile **nur
wenn das Feld im jeweiligen Datensatz vorhanden ist** – viele Felder aus dem
`einzelbauteile`-Schema sind optional (`dp_*`, `preis_*`, `klemmen_zusatz`,
`einbaulage`) und werden nie als erfundene „0"/„–"-Platzhalterzeile
gerendert, wenn sie im konkreten Datensatz fehlen.

**Struktur wiederverwendet, nicht neu erfunden** (verifiziert gegen die
echten Dateien vor dem Bauen): `:root`-Theme-Tokens, Header/`.proj-fields`,
`saveProjFields()`/`loadProjFields()`/`updateDocNr()` (Modul-Suffix `M07`),
`printErgebnis()` (`@page`-Injection außerhalb `@media print`) 1:1 aus
Modul 4 übernommen (Modul 4 statt Modul 3 als Vorlage gewählt, weil Modul 4
zusätzlich den Session-19-Fix hat, `proj-docnr` auch direkt in localStorage
zu schreiben). `ZONE_LABELS`/`ZONE_COLORS`/`ALLE_ZONEN` identisch zu
Modul 3/4 (gesperrte modulübergreifende Konvention) – keine neuen Zonenfarben
erfunden. Header-Link bleibt `../../index.html`, Footer-Link
`../../web/index.html` – Inkonsistenz existiert identisch in allen
bestehenden Modulen, hier bewusst repliziert statt einseitig „repariert".

**Druck:** `printErgebnis()` druckt die aktuell gefilterte Tabellenansicht
(nicht das Detail-Panel) – Hauptnutzen ist eine Abarbeitungsliste gegen
Excel (z. B. „alle Einträge ohne Preis"), ein einzelnes Detail mit
klickbarer Navigation eignet sich nicht für einen statischen Ausdruck.
`@media print` blendet `.dq-bar`/`.toolbar`/`.panel-detail`/`.btn-row`/
`.site-footer` aus, Corporate-Header-Druck-CSS aus Modul 3/4 übernommen.

**Landing Page (`web/index.html`):** neue `module-card--active` zwischen
Modul-04-Karte und dem Modul-05-Platzhalter eingefügt (Modul 05/06 bleiben
`--planned`-Platzhalter, unverändert), `hero-stats` „4"→„5" bei „Module
aktiv". Die vorbestehende, veraltete „Softwarearchitektur/
Datenbankstrategie"-Sektion der Startseite (beschreibt ein SQLite/sql.js-
Pipeline-Konzept, das nicht der Realität entspricht) wurde bewusst NICHT im
Rahmen dieses Moduls korrigiert – unabhängiges Aufräum-Thema, siehe
Backlog.

**Bewusst nicht Teil dieser Session:** die Anwendung dieses Browser-Konzepts
auf die übrigen 7 JSON-Datenbanken; irgendeine Form von Schreibzugriff/Edit-
UI (auch nicht für `geprueft` allein); das in Session 28i/28g bereits
zurückgestellte Thema „Zonen-Override für Einzelbauteile außerhalb von
Baugruppen" (eigenes Datenschema-Thema, keine Auswirkung auf dieses rein
lesende Modul).

Verifiziert direkt gegen die produktiven Funktionen im Browser: Datenqualitäts-
Zahlen exakt wie gegen die committeten JSON-Dateien vorab per PowerShell
berechnet (73/73 ungeprüft, 49/73 ohne Preis, 0/15 Baugruppen ungeprüft, 0
Referenzen verwaist, Zonenlücke `klemm_s`); Suche nach echter Artikel-Nr.
liefert genau 1 Treffer; Zonenfilter `klemm_e`→25/`klemm_s`→0 Treffer;
Verwendungsnachweis für `3209510` zeigt korrekt `Lüftermotor 1-stufig bis
2 kW`/Menge 4/Zone `klemm_l`, Klick springt zur Baugruppe und löst dort alle
5 Bauteile ohne Orphan-Warnung auf; synthetischer In-Memory-Test (nicht
committet) bestätigt Orphan-Erkennung: injizierte ungültige Artikel-Nr.
erhöht den DQ-Zähler korrekt auf 1, färbt die betroffene Zeile/den
Detail-Eintrag rot, nach Entfernen wieder 0; Startseite zeigt die neue
Modul-07-Karte korrekt zwischen 04 und dem Platzhalter, Link löst auf
`modules/modul-07-stammdatenpflege/` auf, `hero-stats` zeigt „5".
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
