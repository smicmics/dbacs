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

## Offene Punkte (Stand Session 58 – vor Beginn der nächsten Sitzung lesen)

> **Sitzungsstand Ende Session 58 (05.09.2026) – „wir machen morgen weiter":**
> Alle Session-58-Arbeiten (kommunikative Datenpunkte an Baugruppen, Belimo
> Energy Valve, 22 Wärme-/Kälte-/Wasserzähler, 2 Wilo-CIF-Module, CRAH
> +Betrieb/Nur-Monitoring, 3 Elektro-Energiezähler, 3 Automation-UMG-
> Türeinbau) sind implementiert, in `ga_komponenten.xlsx` eingetragen, per
> `xlsx_to_json.py` als JSON exportiert (baugruppen 96 · einzelbauteile 147 ·
> feldgeraete 52) und im Browser verifiziert. Zuletzt behoben: der
> `tuer`-Zone-an-Baugruppen-Bug (Zähler erscheint jetzt in der Türansicht,
> siehe „Modul 4/5 – Session 58"). `git status` = nur `CLAUDE.md` +
> `modul-04-innenaufbau/index.html` offen (Stop-Hook committet+pusht). Keine
> bekannten offenen Bugs – die Punkte unten sind Recherche-/Katalog-Restlisten,
> keine Blocker.
> **Nächster sinnvoller Schritt:** vom Nutzer offene Preis-/Katalogpunkte
> (siehe unten „Session 57 – Preisrecherche" + „Feldgeräte-Katalogzeilen
> fehlen") abarbeiten oder die vom Nutzer angekündigte weitere Elektro-Feldgerät-
> Erfassung (FU-/Motorstatus kommunikativ) beginnen.

- **Session 59 – Anlagen-/Makro-Baugruppen (Baugruppe aus Baugruppen) – Konzept
  offen, wird für Lüftung/Kälte/Heizung gebraucht:** Ziel ist, aus bereits
  katalogisierten, geprüften Baugruppen/Einzelbauteilen eine übergeordnete
  Anlagen-Baugruppe zusammenzusetzen (Beispiel Nutzer: „statischer Heizkreis mit
  Referenzraumsensor" → Pumpe + Ventil + Vorlauf-/Rücklauf-/Raumsensor, alle
  schon in der DB) und diese selbst als Baugruppe in die DB aufzunehmen –
  greift auf vorhandene, verifizierte Daten zu, spart die Einzelableitung.
  **Blocker:** `baugruppen_bauteile` verknüpft eine Baugruppe bisher nur mit
  `einzelbauteile` (Artikelnummern), es gibt keinen „Baugruppe enthält
  Baugruppen"-Mechanismus (in Session 51 Nachtrag 7 als
  `grundschaltung`/`zusatzbaustein`/`standalone` angedacht, zurückgestellt).
  Nötige Schritte: (1) Darstellung entscheiden – neues Sheet
  `baugruppen_baugruppen`, oder `typ`/`bg_id`-Referenz auf `baugruppen_bauteile`,
  oder Auflösung/Flattening beim Export; (2) `xlsx_to_json.py` + Modul 4/5
  anpassen (Stückliste, Feldgeräteliste, DDC-/Steuerspannungs-/Kommunikations-
  Statistik müssen enthaltene Baugruppen mitzählen); (3) 1–2 Beispiele von Hand
  bauen; (4) danach eigener Skill `dbacs-anlagenbaugruppe` (zerlegt eine
  Anlagenfunktion, mappt Teilfunktionen auf vorhandene Katalogeinträge, reicht
  fehlende Teile an `dbacs-recherche` weiter, setzt zusammen, fährt die
  Pipeline). Der bestehende `dbacs-recherche`-Skill (`.claude/skills/`,
  Session 59 angelegt) bleibt unverändert der „Lücke-füllen"-Baustein.
- **Session 57 – Desigo-PX auf aktuelle Revision umgestellt (ERLEDIGT):**
  Frage „abgekündigt?" geprüft – Desigo PX ist **NICHT** abgekündigt, nur
  die alte **„PX Classic"-Generation** (PXC00 / PXC64-U / PXC128-U /
  `PXC..-E.D`, BACnet/**LonTalk**, Engineering XWorks Plus) ist im Phase-out
  (Ankündigung Nov/Dez 2024, Servicephase 01.04.2026–31.12.2032). Der
  verwaiste Katalog-Alteintrag `PXC100-D` ist jetzt **`aktiv=0`** (fällt aus
  dem JSON). Die 3 `ddc_cpu`-Zeilen wurden von der `.A`- auf die aktuelle
  Revision umgestellt (Siemens-Datenblätter 02–03/2026), Modellierungslogik
  unverändert (dp-Felder, `auto_ea_cpu`, 24V AC):
  - `PXC4.E16.A → PXC4.E16-2` (ASN S55375-C150), Onboard 12 UIO + 4 Relais
    (unverändert), onboard+TXM bis 50 E/A, `max_ea_module` 2→4, Preis 875 €.
  - `PXC5.E24.A → PXC5.E24-N` (ASN S55375-C154), Onboard 2 DI + 8 UIO +
    8 XIO + 6 Relais (unverändert), bis 80 E/A / 120 DP, `max_ea_module`
    6→7, Preis 1407 € (**SIPATEC-Seite noch „PXC5.E24", -N-Zuordnung
    unbestätigt**).
  - `PXC7.E400.A → PXC7.E400L-N` (ASN S55375-C155, `auto_ea_cpu`),
    0 Onboard-Regel-E/A (1 DI, bewusst nicht als dp modelliert), bis 400
    E/A / 600 DP, `max_ea_module` 64→50, Preis 1932→**3535 €** (der alte
    Wert galt für die kleinere E400M/250-DP-Variante).
  - `h_mm` aller 3 von 90 auf **124** korrigiert (aktuelle Datenblätter).
  - `TXM1.x`-I/O-Module unverändert aktiv (Datenblatt-Rev. 03/2026, keine
    Nachfolgereihe). Desigo Optic / Building X = Leit-/Cloud-Ebene, **kein**
    Ersatz auf Automationsstationsebene.
  - Im Browser verifiziert (CPU-Dropdown, Auto-Ergänzung PXC7.E400L-N,
    Onboard-Deckung PXC4.E16-2 / PXC5.E24-N, keine Konsolenfehler).
  - **Rest-Unsicherheit:** `max_ea_module` aus Punktesummen abgeleitet
    (Datenblätter nennen keine Modulzahl); Preise sind SIPATEC-Netto
    (kein öffentlicher Siemens-Listenpreis); `PXC4.M16-2`/`E16S-2` (MS/TP-
    bzw. reine SC-Variante) nicht angelegt.
- **Session 57 – Preisrecherche (neu):** kompletter Bauteilkatalog per
  4 Hintergrund-Forks bepreist (Herstellerlistenpreis bevorzugt, sonst
  namhafter Großhandel/Distributor; Gebrauchtbörsen ausgeschlossen; alle
  netto, Stand ~08/2026, Provenienz je Eintrag als `[Preisrecherche
  08/2026] …`-Zusatz im `quelle_hinweis`). **Ergebnis: Einzelbauteile
  141/146, Feldgeräte 32/36 mit `preis_eur`.** Viele Werte sind
  Distributor-/Straßenpreise (echte Siemens/Phoenix-Listenpreise nur nach
  Login), teils aus Brutto zurückgerechnet – siehe `quelle_hinweis`.
  **Noch ohne Preis (Herstelleranfrage nötig):**
  Einzelbauteile `3RT2026-1AB00`, `4AP2142-8BC40-0HA0`,
  `4AM4042-5AN00-0EA0` (alle abgekündigt/Auslauf), `PW100` (Relay GmbH);
  Feldgeräte `20N842S021` (KRIWAN INT511 24V-Variante), `PST010RG12S`,
  `TWP1F`, `STB1F` (Honeywell/FEMA, teils abgekündigt).
  (Die damaligen `.A`-CPU-Näherungspreise sind mit der PXC-Umstellung oben
  überholt – jetzt `PXC4.E16-2` 875 €, `PXC5.E24-N` 1407 €, `PXC7.E400L-N`
  3535 €.)
- **Session 57 – DDC-Modul-Katalog:** `TXM1.8U-ML` jetzt bepreist
  (433,30 €). **`TXM1.8X`/`TXM1.8X-ML` bewusst NICHT angelegt** – reales
  `TXM1.8U` kann bereits 0–10V-AO, `TXM1.8X` unterscheidet sich nur durch
  4–20 mA; erst anlegen, wenn ein 4–20-mA-Feldgerät in den Katalog kommt
  (dann als `nicht_auto`-Manuell-Option).
- **Session 57 – Türeinbau-LVB Romutec** noch nicht umgesetzt –
  `computeLvbRomutecDevices()` ist ein `return []`-Stub, Options-Eintrag
  „Türeinbau · Romutec – folgt" disabled. Recherche-Stand: Serie **RAG**
  (analog 0–10V, z. B. RAG3030, 8 TE, 24V AC/DC) + **romod 4DO-R** (binär,
  Modbus RTU) + IBGTflex-Trägerrahmen; für „1× AO + 1× Relais" zwei
  getrennte Geräte, konkrete Türmodul-Artikelnummern/Preise nicht gefunden.
- **Feldgeräte-Katalogzeilen fehlen (nicht nur Preise):** die von
  Baugruppen referenzierten `feldgeraet_artikel_nr` `SAX61.03`,
  `SSB161.05HF`, `SQV91P30`(+`ASP1.1`), `STA121`/`STA321`/`STP121`/
  `STP321.L20`, `1012726` (Oventrop) sowie die Wilo-Pumpen (`Yonos/Stratos
  PICO`, `Stratos MAXO`/`MAXO-Z`/`GIGA2.0`, `CronoLine-E`) und `HDCV`
  (Schneider) existieren **nur als Platzhalter-String**, nicht als eigene
  `feldgeraete`-Katalogzeile – Modul 5 kann sie daher nicht bepreisen. Vor
  einer Feldgeräte-Kalkulation müssen diese Zeilen erst angelegt werden
  (Abmessungen/Kategorie/Preis je Gerät), das ist eine Katalog-Aufgabe,
  keine reine Preissuche.
- **Session 56 (neu):** Baugruppen `420_000022` (Umwälzpumpe Wilo Yonos/
  Stratos PICO) und `430_000026` (Umluftkühlgerät Schneider Uniflair HDCV)
  sowie die neuen Bauteile `2900934`/`2903686` (Phoenix Contact
  Relaissockel+Steckrelais REL-IR4/L-24AC/4X21) und `5ST3010` (Siemens
  LSS-Hilfsschalter) haben noch **keinen Preis** eingetragen. Beide
  Baugruppen tragen nur Platzhalter-`feldgeraet_artikel_nr` (kein
  konkreter Wilo-/Schneider-Bestellcode für eine repräsentative
  Baugröße). `5ST3010`-Höhe (81mm) von der 5SL6-LSS-Reihe übernommen,
  nicht eigenständig verifiziert. Schneider-Baugruppe basiert auf dem
  allgemeinen Carel-pCO5+-Handbuch, kein HDCV-spezifischer
  Original-Klemmenplan gefunden (nur Bild-Scans). Wilo-Baugruppen
  MAXO/MAXO-Z (mit SSM/SBM/DI/AI-Signalklemmen) sind noch **nicht**
  angelegt, nur PICO (signallos, Koppelrelais-Pattern) ist fertig.
- **STP121** (`420_000019`, 24V thermischer Ventilantrieb, stromlos auf) –
  Artikelnummer nicht über eine eigene Distributor-Listung verifiziert,
  nur per Namenskonvention vom bestätigten Paar STA321/STP321 auf die
  24V-Baureihe übertragen – vor Verwendung im Projekt am HIT-Portal
  gegenprüfen.
- **Oventrop 1012726** (`420_000017`, Fußbodenheizungs-Antrieb) –
  Klemmenbelegung (G/G0/Y/U-Analogie zu den Siemens-Antrieben) ist eine
  plausible Annahme, kein vollständiges Anschlussschema geprüft (vom
  Nutzer in Session 55 ausdrücklich als ausreichend akzeptiert) – bei
  Bedarf später anhand des Original-Datenblatts nachprüfen.
- **SQV91P30 + Zusatzmodul ASP1.1** (230V-Variante, `420_000016`) – genaue
  Klemmenbezeichnung des Zusatzmoduls nicht verifiziert, nur als
  24V-Analogie modelliert.
- **Koppelrelais 24V-Spule `2967073`** – Abmessungen (b_mm/h_mm) vom
  230V-Schwesterartikel `2967099` übernommen statt eigenständig
  verifiziert (eine abweichende Distributor-Angabe 14×80mm gefunden,
  nicht eindeutig derselben Baureihe zuordenbar).
- Starrer Stabtemperaturfühler mit Flansch für den Lüftungskanal: existiert in
  der europäischen Symaro-Reihe nicht (nur biegsame Kapillare, auch bei
  QAM2120.040). Alternativen anderer Hersteller sind noch zu recherchieren
  (Nutzer-Vorgabe: „Wir werden noch Alternativen suchen").
- Grundsatzfrage farbige L1/L2/L3-Klemmen (UT-Reihe Einspeisung) vs. Praxis
  (Nutzer-Hinweis Session 52: „in der Praxis werden die farbigen Klemmen für
  L1 L2 und L3 meist gar nicht eingesetzt") – ggf. später auf grau+PE
  umstellen, noch nicht entschieden.
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
- **Session 58 (neu) – kommunikative Datenpunkte an Baugruppen (Systematik +
  Portfolio):** Neue Systematik implementiert (siehe „Modul 4/5 – Session 58"
  weiter unten), im Browser verifiziert. Neu angelegt:
  - **Belimo Energy Valve** `420_000027`/`028` (Kat. „Ventilantriebe",
    `[heizung,lueftung,kaelte]`), Feldgeräte `EV050R2+KBAC`/`EV100F+KBAC`,
    Hybrid analog + IP (`modbus_tcp`).
  - **Wärme-/Kälte-/Wasserzähler** `420_000029`–`420_000050` (22 Baugruppen,
    Kat. „Energie und Zählwerteinrichtungen"): je DN15–25 / DN50 / DN100 ×
    {M-Bus busgespeist, M-Bus + 24 V, Dual M-Bus + Modbus RTU (nur Wärme/Kälte
    DN50/DN100)}. 24 V: Kompakt/Wasser → `24vac`, getrennte Rechenwerke DN50/
    DN100 → `24vdc` (Namenszusatz „Rechenwerk getrennte DC-Versorgung").
    Aquametro hat **kein Modbus-TCP-Modul** → Dual = M-Bus + Modbus RTU.
  - **Wilo Pumpen-Kommunikationsmodule** `420_000051`/`052` (Kat.
    „Umwälzpumpen", hinter den Pumpen): CIF-Modul Modbus RTU (Art. 2190368,
    339 €) + CIF-Modul Ethernet Modbus TCP/BACnet-IP (Art. 2211408, 717 €);
    IF-Modul 2097809 für CronoLine-E/IL-E im `quelle_hinweis`.
  - **Elektro-Energiezähler / Netzanalysatoren** `440_000001`–`003` (gewerk
    440, `[elektro]`, Kat. „Energie und Zählwerteinrichtungen"): Modbus RTU /
    M-Bus / Modbus TCP, je 17 AI kommunikativ, Referenzgeräte Janitza UMG 96RM
    (`5222001`/`5222069`/`UMG96RM-PN`) bzw. Schneider Acti9 iEM33xx. Keine
    Steuerspannung (Versorgung am Einbauort in der Elektro-Verteilung).
  - **Schneider CRAH `430_000026`** um Betriebsmeldung (BI) ergänzt (jetzt
    1× BO + 3× BI + 1× AO, 10 Klemmen); reduzierte Variante `430_000027`
    „… Nur Monitoring" (nur 3× BI).
  - **Automation-UMG „Türeinbau" `480_000012`–`014`** (gewerk 480,
    `[automation]`, Kat. „Messgerät/Energiezähler"): die 3 Janitza UMG 96RM
    (`5222001` RTU / `5222069` M-Bus / `UMG96RM-PN` TCP) als
    Schaltschrank-Bestandteil (kein Feldgerät) – `bt.zone:'tuer'` (erscheint
    in der Türansicht), `dp_fb_ai:17` je Protokoll, plus 1× LSS `5SL6316-7`
    (C16 3-polig) in `evert`. Dazu Bugfix `getTuerItems()`: löst jetzt auch
    Baugruppen mit `bt.zone==='tuer'` auf (siehe „Modul 4/5 – Session 58").
  Offen: Belimo DN100 `kvs`/VA unbestätigt; `2891021`-Preis Richtwert 125 €;
  Aquametro-Preise DN50/DN100 nicht öffentlich; `MR006` (PW20) evtl.
  abgekündigt; Rohfakten in `scratchpad/fork_*_ergebnis.md`.
- **Elektro-Medium**: Energiezähler erledigt (s. o.); weitere Elektro-Feldgeräte
  (z. B. FU-/Motorstatus kommunikativ) bei Bedarf analog.

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
9. **Aktoren mit Stellsignal + Rückmeldung (Session 55, verbindlich):**
   ein Ventil-/Klappenantrieb mit analogem Rückmeldesignal (z. B. 0…10V
   Ist-Hub) ist trotz Analogsignal **kein** Messsensor im Sinne von Regel 1
   – `klemm_s` bleibt echten Messsensoren vorbehalten. Stellsignal-Eingang
   UND Rückmeldesignal-Ausgang eines Aktors gehören zusammen auf
   `klemm_f`. Datenpunktbedarf: 1× AO (Stellsignal von der DDC) + 1× AI
   (Rückmeldung zur DDC) je Antrieb.
10. **Koppelrelais auch für Ausgangsrichtung (Session 55, verbindlich):**
    Regel 6 beschreibt das Koppelrelais für Sicherheitsketten
    (Sensor-Wechsler → Relais → 2 getrennte Ausgänge). Das gleiche
    Bauteilprinzip gilt auch andersherum: schaltet ein DDC-Binärausgang
    (BO) eine Last, die die TXM-Module nicht direkt schalten können (z. B.
    230V-Verbraucher, TXM1.8T ist nur für 24V AC vorgesehen), wird ein
    Koppelrelais mit **24V-AC-Spule** (kompatibel zum TXM1.8T-BO-Ausgang)
    zwischengeschaltet; der Kontakt schaltet die höhere Spannung zum
    Verbraucher. Neues Bauteil `2967073` (Phoenix Contact
    PLC-RSC-24UC/21-21, baugleiche Baureihe wie die 230V-Spulen-Variante
    `2967099` aus Regel 6, nur andere Spulenspannung).
11. **PE bei Leistungsklemmen für externe Betriebsmittel (Session 56,
    verbindlich):** verlässt eine Leistungsversorgung den Schaltschrank zu
    einem externen Betriebsmittel (z. B. Pumpe), wird die Klemmleiste immer
    komplett mit Schutzleiter angelegt – **L, N, PE** (1~) bzw. **L1, L2,
    L3, N, PE** (3~) – unabhängig von der Schutzklasse des Zielgeräts. Hat
    ein Gerät Schutzklasse II (kein PE-Anschluss), bleibt die PE-Klemme
    einfach unbelegt; der zusätzliche Platzbedarf ist für DBACS
    vernachlässigbar. Vereinfacht die Klemmenzahl-Vorhersage, da nicht pro
    Gerät recherchiert werden muss, ob ein PE-Anschluss vorhanden ist.
12. **Schrankinterne Verdrahtung ohne Klemme (Session 56, verbindlich):**
    sitzen zwei Bauteile einer Baugruppe **beide innerhalb desselben
    Schaltschranks** (z. B. Koppelrelais und DDC-Modul, oder ein
    Hilfsschalter am LSS und das DDC-Modul), braucht die Verbindung
    zwischen ihnen **keine eigene Klemme** – das ist reine
    Schrankinnenverdrahtung, kein Feldkabel. Der Datenpunkt (`dp_ai/ao/
    bi/bo`) wird trotzdem verzeichnet, aber direkt als Override auf der
    jeweiligen Bauteil-Zeile (z. B. dem Koppelrelais oder dem
    Hilfsschalter) statt auf einer eigenen `3209510`-Klemmenzeile. Klemmen
    in `klemm_l/f/s` sind ausschließlich für Verbindungen reserviert, die
    den Schrank tatsächlich verlassen (Feldgerät, externes Betriebsmittel).
    Beispiel: Baugruppe „Umwälzpumpe Yonos/Stratos PICO" (`420_000022`) –
    DDC-BO speist die Koppelrelais-Spule direkt, der Betriebsmeldekontakt
    des Relais sowie der Störkontakt des LSS-Hilfsschalters gehen direkt
    auf die DDC-BI-Klemmen, ohne dass irgendeine dieser drei Verbindungen
    eine eigene `3209510`-Klemme braucht – nur der tatsächliche
    Leistungsabgang zur Pumpe (L/N/PE, siehe Regel 11) bekommt Klemmen.

### Referenz: Motorleistungsreihe & Schaltgerätekonzept Drehstrommotoren (Session 56)

Recherchiert als Entscheidungsgrundlage für künftige Baugruppen mit
Drehstrommotoren (nicht nur Pumpen). Vollständige IEC-60072-Normreihe
(kW): `0,75 · 1,1 · 1,5 · 2,2 · 3,0 · 4,0 · 5,5 · 7,5 · 11 · 15 · 18,5 ·
22 · 30 · 37 · 45 · 55 · 75 · 90 · 110 · 132 ...`

| Leistung | I_N ca. (400V 3~) | Anlaufart | MSS-Bereich | Schützgröße (SIRIUS) |
|---|---|---|---|---|
| 1,5 kW | ≈3,4 A | Direktanlauf | 2,5–4,0 A | S00 |
| 2,2–4 kW | ≈4,9–8,6 A | Direktanlauf | 4,0–10 A | S00 |
| 5,5–7,5 kW | ≈11,5–15 A | Direktanlauf/erste Stern-Dreieck-Fälle | 10–16 A | S0 |
| 11 kW | ≈22,5 A | Stern-Dreieck/Sanftstarter/FU üblich | 20–25 A | S2 |
| 15 kW | ≈30 A | Stern-Dreieck/Sanftstarter/FU | 25–32 A | S3 |
| 18,5 kW | ≈37 A | Stern-Dreieck/Sanftstarter/FU | 32–40 A | S3 |
| 22 kW | ≈43 A | Stern-Dreieck/Sanftstarter/FU | 40–50 A | S3/S6 |

**Wichtig – MSS statt LSS bei echten Motorabgängen:** ein klassischer
Drehstrommotor-Abgang (Direktanlauf über Schütz, KEINE eigene
Antriebselektronik) braucht einen **Motorschutzschalter** (IEC
60947-4-1, z. B. Siemens 3RV) statt eines einfachen Leitungsschutz-
schalters (IEC 60898) – der Motor-Anlaufstrom (6–8× I_N) erfordert eine
speziell abgestimmte Auslösecharakteristik, die ein LSS nicht bietet.
Ein reiner LSS reicht nur bei sehr kleinen Hilfsantrieben.
**Ausnahme:** Motoren mit **integriertem Frequenzumrichter/Sanftanlauf**
(z. B. Wilo Stratos GIGA2.0/CronoLine-E, `420_000025`/`026`) haben
keinen klassischen Direktanlauf-Einschaltstrom – hier reicht ein LSS,
analog zum bestehenden Frequenzumrichter-Baugruppen-Muster (Session 45,
SINAMICS G120C: auch dort nur LSS/Leistungsschalter eingangsseitig,
kein MSS, da der FU selbst den Motorschutz übernimmt).
Die 4–5,5-kW-Schwelle Direktanlauf→Stern-Dreieck/Sanftstarter/FU ist
**keine feste Norm**, sondern Praxis-Faustregel, abhängig von den TAB
(Technische Anschlussbedingungen) des jeweiligen Netzbetreibers.

---

### Modul 4/5 – Kommunikative Datenpunkte an Baugruppen + Kommunikationsbauteil-Ratchet (Session 58, komprimiert)

Neues Muster für Feldgeräte, die **über einen Bus gelesene Werte** liefern, die
**keinen Schaltschrankplatz verbrauchen** (Energiezähler, Belimo Energy Valve …):

- **`dp_fb_ai/ao/bi/bo` + `feldbus_protokoll` jetzt auch je
  `baugruppen_bauteile`-Verknüpfungszeile** (xlsx_to_json + Modul 4). Die
  Overrides sitzen auf einer ohnehin vorhandenen `3209510`-Klemmenzeile der
  Baugruppe (kein eigenes Träger-Bauteil) – analog zu den physischen
  `dp_*`-Overrides der DDC-Reserve-Baugruppen. In `buildQueues()` landen sie in
  `fbDemand[protokoll]` (mbus / modbus_rtu / modbus_tcp), NICHT in `dpDemand` →
  Statistik-Gruppen „Komm. …", keine physische Platzierung.
- **Kommunikationsbauteil-Ratchet** (neu, `kommWatermark` /
  `m04_komm_watermark`, Muster = `steuerspannungWatermark`, sinkt nie): je nach
  Bus wird automatisch ein schrankinternes Bauteil in `steuer` ergänzt:
  - `mbus` → M-Bus-Pegelwandler **`MR006`** (PW20, 24 V AC/DC) – **präsenz-
    basiert, 1 Stück** (bei >20 Zählern manuell `MR004C` = PW60).
  - `modbus_tcp` (inkl. **BACnet/IP** – kein eigener Gruppen-Key) → Ethernet-
    Switch **`2891021`** (Phoenix Contact FL SWITCH SFN 5TX-24VAC) –
    **MENGENBASIERT**: 5 Ports, 1 Port für die Automationsstation bzw. den
    Uplink zum vorherigen Switch → 4 freie Ports je Switch → `ceil(n / 4)`
    Switches bei `n` IP-Teilnehmern (5. Teilnehmer ⇒ 2. Switch). `n` zählt
    **alle** `modbus_tcp`-Träger – interne (z. B. UMG in der Tür) UND externe
    (Belimo, Wilo CIF-ETH, künftig CRAH mit Schnittstelle) sowie direkt
    platzierte kommunikative Einzelbauteile. Watermark speichert
    `ip_switches` (Zahl).
  - `modbus_rtu` → **nichts** (RS485 direkt an einen CPU-Port).
  Manuell platzierte `MR006`/`MR004C`/`PW100` gelten als M-Bus vorhanden;
  manuelle `2891021`/`2891001`/`EDS-205` liefern je 4 Ports Kapazität
  (`switchesAuto = ceil(n/4) − manuelle`). `resetDdcWatermark()` leert auch
  `kommWatermark`. `MR006`/`MR004C`/`2891021` haben `benoetigt_steuerspannung:
  '24vac'` → der Steuerspannungs-Ratchet zieht den Trafo automatisch nach.
- **Modul 5** zeigt je Feldgerät `kommunikative_datenpunkte` (neue
  `feldgeraete`-Freitextspalte) als „Kommunikativ ausgelesen: …".
- **Belimo Energy Valve** (`420_000027`/`028`): Hybridmodus analog + IP – 4
  `klemm_f`-Klemmen (2× 24 V + Y + U), 1 AO + 1 AI physisch, dazu auf der
  U-Klemmenzeile `dp_fb_ai:9, dp_fb_bi:1, dp_fb_ao:2` @ `modbus_tcp`. `+KBAC` =
  SuperCap-Notstellung (Auf/Zu wählbar). Schutzklasse III/PELV → **kein PE**.
  1 Belimo-Baugruppe je Baugröße (BACnet/IP vs. Modbus TCP ist Gerätekonfig,
  kein Portfolio-Split).
- **Automation-UMG „Türeinbau" (`480_000012`–`014`, Kat. „Messgerät/
  Energiezähler", gewerk 480):** die 3 Janitza-UMG-96RM (`5222001` RTU /
  `5222069` M-Bus / `UMG96RM-PN` TCP) als **Schaltschrank-Bestandteil** (kein
  Feldgerät, kein Modul-5-Eintrag) – `bt.zone:'tuer'` (`keine_platzierung_mp`,
  erscheint in der **Türansicht**), `dp_fb_ai:17` je Protokoll, plus 1× LSS
  `5SL6316-7` (C16 3-polig) in `evert` für die Messspannungs-Eingänge.
- **`tuer`-Zone an Baugruppen (Bugfix, Nutzer-Fund „Zähler nicht in der Türe
  platziert"):** `getTuerItems(feldIndex)` durchlief bisher nur
  `belegung`-Einträge mit `typ==='einzel'` – ein `bt.zone==='tuer'`-Bauteil in
  einer Baugruppe kam nie in die Türansicht (die Baugruppen-Bauteil-Schleife
  in `buildQueues()` bricht bei `if(!queues[zone]) return;` ab, `tuer` ist
  nicht in `ALLE_ZONEN`). Fix: `getTuerItems()` löst jetzt zusätzlich (nur
  `feldIndex===1`, Baugruppen haben keine feldweise Tür-Zuordnung) alle
  `typ==='baugruppe'`-Einträge über `resolveBaugruppenBauteile()` auf und
  sammelt `bt.zone==='tuer'`-Bauteile (× `item.menge` × `bt.menge`). Die
  kommunikativen Datenpunkte selbst wurden schon vorher korrekt gezählt (die
  fb-Routing-Zeile steht bewusst **vor** dem `queues[zone]`-Guard).

Alles im Browser verifiziert (dp_fb-Zählung in „Komm. Modbus TCP/IP" bzw.
„Komm. M-Bus", Switch 1× geteilt über n Ventile, `480_000013` 1×/2× → 1/2
UMG-Symbole in der Türansicht, LSS in `evert`, Klemmen/Stückliste/
Steuerspannung stimmen, Modul 5 zeigt Auslese-Liste, keine Konsolenfehler).

---

### Modul 4 – DDC-Modul-Auto-Ergänzung: Shared-Pool + globale LVB-Auswahl (Session 57, komprimiert)

Nutzer-Fund per Screenshot: 1 AI + 1 AO ergaben **2× TXM1.8U**, weil
`computeDdcAutoModules()` je Datenpunkttyp einen eigenen 8er-Pool rechnete.

- **Analog-Shared-Pool (verbindlich):** In der Siemens-TX-I/O-Familie gibt es
  **kein dediziertes AI- oder AO-Modul für 0–10V** – beides läuft über das
  Universalmodul `TXM1.8U` (bzw. `TXM1.8U-ML` mit LVB), dessen 8 Punkte frei
  zwischen AI und AO aufteilbar sind. `computeDdcAutoModules()` zählt daher
  `remaining.dp_ai + remaining.dp_ao` zusammen und wählt EIN Modul in
  `ceil(summe/8)` Stück (1 AI + 1 AO = **1** Modul). BI (`TXM1.8D`/`16D`)
  und BO (`TXM1.6R`/`TXM1.6R-M`) bleiben je genau ein dediziertes Modul,
  ohne Cross-Credit-Problem. `TXM1.8X`/`TXM1.8X-ML` (nur Unterschied:
  4–20mA) bewusst **nicht** im Katalog – siehe Offene Punkte.
- **Globale LVB-Auswahl:** 2 Selects in `#cpu_lvb_row` neben CPU-Typ.
  `#lvb_anforderung` (`ohne` = Standard/Verhalten wie bisher / `gefordert`)
  und `#lvb_realisierung` (`ddc` / `metz` / `romutec` disabled), zweites
  Feld gesperrt solange Anforderung = `ohne`. Persistenz
  `m04_lvb_anforderung`/`m04_lvb_realisierung`.
  - `gefordert` + `ddc` → `needsLvb.dp_ao = needsLvb.dp_bo = true` (in
    `buildQueues()` global gesetzt, zusätzlich zum bestehenden
    baugruppenweisen `bt.lvb_erforderlich`): AO → `TXM1.8U-ML`,
    BO → `TXM1.6R-M`.
  - `gefordert` + `metz` → **Schaltschrank-LVB**: DDC-Seite bleibt normal
    (`TXM1.8U`/`TXM1.6R`), `computeLvbMetzDevices()` ergänzt **je
    Ausgangspunkt** ein Metz-Handebene-Gerät in Reihe – `110730` KMA-F8
    (AO, 0–10V-Analogwertgeber) / `110661` KRS-E06 (BO, Relais-
    Schnittstelle). 1 Gerät je Punkt (nicht je 8), inkl. gleicher
    DDC-Reserve. Fester Konstant `LVB_METZ_ART = {dp_ao:'110730',
    dp_bo:'110661'}` mit Load-Guard. Geräte laufen über `ddcAuto.modules`
    → Ratchet + Stückliste (`letzteDdcAuto`) automatisch, Platzierung als
    eigenständige Hutschienengeräte in `queues.steuer` (kein `ddc_io`-
    Filter, keine CPU-Gruppe).
  - `romutec` → `computeLvbRomutecDevices()` ist `return []`-Stub.
- **Kompaktstation + LVB:** Onboard-E/A der PXC4/PXC5 hat **keine** LVB.
  Bei `gefordert` + `ddc` wird der Onboard-`dp_ao`/`dp_bo`-Beitrag NICHT
  in `dpSupplyEffective` angerechnet (manuell platzierte CPU: über
  `cpuOnboardOut`-Tracking in `accumulateDp()` wieder abgezogen; auto-CPU:
  in der `cpuBenoetigt`-Schleife für AO/BO übersprungen). Onboard-AI/BI
  bleiben anrechenbar. Bei `metz` darf Onboard decken (Handebene sitzt
  extern dahinter).
- **Katalog:** `420_000015`/`420_000016` „(Fail Open)" → „(Fail
  Open/Close)" + Beschreibung („in die konfigurierte Notstellposition, per
  Konfiguration") – Gerät kann beide Notstellrichtungen, **keine**
  Schaltungsänderung (Abschaltung sitzt im Frostschutz-Koppelrelais,
  Regel 6). Metz `110661` von falschen 22,5mm auf **17,5mm / 1 TE**
  korrigiert (Recherche-Fund).
- Alle Szenarien im Browser verifiziert (ohne LVB / ddc / metz / Kompakt-
  CPU je Richtung, Stückliste + Zeichnung + Positionsnummern + Watermark
  konsistent, keine Konsolenfehler). Recherche per Subagent (Web,
  Siemens-TX-I/O-Datenblätter + Metz + Romutec).
- **Preisrecherche im selben Zug:** kompletter Bauteil- + Feldgeräte-Katalog
  per 4 Hintergrund-Forks bepreist (Einzelbauteile 141/146, Feldgeräte
  32/36), Werte + Provenienz in `ga_komponenten.xlsx` (`preis_stueck_eur`
  + `[Preisrecherche 08/2026] …`-Zusatz im `quelle_hinweis`, nicht-
  destruktiv an bestehende Hinweise angehängt). Restliste + fehlende
  Feldgeräte-Katalogzeilen siehe „Offene Punkte" oben. Writer-Skripte:
  `scratchpad/xlsx_write_prices.py`, Rohdaten `scratchpad/prices_fork*.txt`.

---

### Modul 4/5 – Ventilantriebe Heizung/Kälte/Lüftung (Session 55, komprimiert)

Erste **Aktoren** im Baugruppenkatalog (bisher ausschließlich Sensoren/
Schaltgeräte) – 9 neue Baugruppen `420_000013`–`420_000021` + neues
Einzelbauteil `2967073`, neue Kategorie „Ventilantriebe":

- **Stellantriebe mit Stellsignal 0…10V + Positionsrückmeldung:**
  Siemens Acvatix SAX61.03 (800N, `420_000013`) und SSB161.05HF
  (200N, kompakt, vom Nutzer „Ventilantrieb Zonenregelung" genannt,
  `420_000014`) – beide nur als 24V-AC/DC-Variante, da 230V+0…10V bei
  keinem geprüften Hersteller (Siemens/Belimo) existiert (durchgängiges
  Baureihen-Prinzip, kein Einzelfall).
- **Notstellantrieb (Federrücklauf/SuperCap) Fail Open:** Siemens Acvatix
  SQV91P30 für Combi-Ventile VPF43../VPF53.. (PICV), 1100N, mit
  Rückmeldung – 2× angelegt lt. Nutzer-Wunsch: 24V-Standard
  (`420_000015`) und mit optionalem 230V-Zusatzmodul ASP1.1
  (`420_000016`, Klemmenbezeichnung des Moduls nicht verifiziert).
- **Fußbodenheizungs-Antrieb:** Oventrop Aktor M ST L (1012726, mit
  Stellungsrückmeldung) – Siemens führt keine M30×1,5-Verteilerantriebe,
  bewusste Herstellerabweichung (`420_000017`).
- **Thermische Ein/Aus-Antriebe** (2-Punkt, kein Analogsignal): Siemens
  STA121/STP121 (24V, NC/NO, `420_000018`/`019`) und STA321/STP321.L20
  (230V, NC/NO, `420_000020`/`021`) – 230V-Varianten schalten auf
  Nutzer-Vorgabe über ein **24V-Spulen-Koppelrelais** (neues Bauteil
  `2967073`, siehe Regel 10), da DDC-BO-Ausgänge (TXM1.8T) nur 24V AC
  direkt schalten.
- **2 neue Modellierungsregeln** aus dieser Session destilliert (siehe
  Regel 9/10 oben): Aktor-Rückmeldesignale bleiben auf `klemm_f` (nicht
  `klemm_s`, Regel 9); Koppelrelais-Pattern gilt auch für die
  Ausgangsrichtung mit 24V-Spule (Regel 10).
- Recherche per Fork-Subagent (Web), Herleitungstabelle vor Excel-Eintrag
  mit dem Nutzer abgestimmt. Alle 10 neuen Katalogeinträge ohne
  bestätigten Preis, `STP121` ohne eigene Distributor-Verifizierung,
  Oventrop-Klemmenbelegung als vom Nutzer akzeptierte plausible Annahme
  – siehe „Offene Punkte" oben. Browser-Verifizierung diese Session nicht
  möglich (Chrome-Tools nicht aktiviert) – vor Produktivnutzung in Modul 4
  nachholen.

### Modul 4/5 – Sessions 53–54 (komprimiert)
Vollständiger Sitzungsverlauf (Nutzer-Funde, Root-Cause-Analysen,
Verifizierungsdetails) archiviert in
`docs/archiv/claude-md-modul4-sessions-53-54.md`. Ergebnisse:

- **Session 53:** 4 neue Lüftungsbaugruppen `430_000017`–`430_000020`
  (Siemens Symaro QPM11../QPM21.. Kanal-CO2/-VOC-Fühler + Kombifühler;
  Luftstromwächter als Herstellerabweichung **KRIWAN** `20N842S021`, da
  Siemens-Original INT511 abgekündigt) – erster Test der Session-51/52-
  Modellierungsregeln, keine Korrekturen nötig. Baugruppen-Dropdown nach
  Kategorie gruppiert: neues Feld `baugruppen.kategorie` (rein optisch,
  analog Einzelbauteile Session 27/40), `<optgroup>` alphabetisch
  sortiert, `BG_SORT_PRIORITY` bleibt Sortierung *innerhalb* einer
  Kategorie. Baugruppe ohne `kategorie` fehlt komplett im Dropdown
  (gleiche strikte Regel wie bei Einzelbauteilen).
- **Session 54, Lüftung:** 5 weitere Baugruppen `430_000021`–`430_000025`
  (Siemens Symaro): Frostschutzwächter QAF64.2-J (nur Schaltkontakt
  verdrahtet, Koppelrelais-Pattern Regel 6), Differenzdrucksensor 0-300Pa
  QBM3020-3, Kanalfühler Feuchte+Temp QFM2160, Raumtemperatursensor mit
  Sollwertversteller QAA27 (±3K, B/M/R-Klemmen), Raum-CO2/Feuchte/Temp
  QPA2062. Bestehendes `430_000013` und neues `430_000022` auf
  einheitlichen Namen „Differenzdrucksensor Kanaldruck..." angeglichen und
  im Dropdown hintereinander einsortiert (Dropdown-Reihenfolge ohne
  `BG_SORT_PRIORITY`-Eintrag = Zeilenreihenfolge im Excel-Sheet).
- **Session 54, Heizung/Kälte/Sanitär:** 12 neue Baugruppen
  `420_000001`–`420_000012` für die bis dahin leeren Gewerke 410/420/434,
  Kategorien „Sensoren flüssiges Medium" (Analogsignal) / „Wächter
  flüssiges Medium" (Schaltkontakt) – Tauchfühler `430_000006`/`007` in
  „Sensoren flüssiges Medium" aufgelöst. Zweite Planungsfabrikat-Ebene
  **Honeywell/FEMA** für mechanische Druck-/Temperaturschalter und
  Sicherheitsbegrenzer (Siemens führt diese Gerätekategorie nicht) –
  Siemens QBE1900-P7/QBE2003-P/QVE1901 für reine Druck-/Strömungssensorik,
  Honeywell/FEMA SDBAM6/TWP1F/STB1F/STB+TWF für Sicherheitstechnik,
  **SYR/Hans Sasserath 933.1** als dritte Herstellerabweichung für
  Wassermangelsicherung. „Druckwächter Max/Min" als EIN Gerätetyp für
  beide Rollen via Kontaktwahl – Namenskonvention „(p-Max)"/„(p-Min)" am
  Beschreibungsende gilt als Vorlage für künftige Wächter-Paare. Alle
  mechanischen Schalter potentialfrei, keine eigene Steuerspannung nötig;
  nur elektronische Sensoren/Transmitter brauchen
  `benoetigt_steuerspannung`.
- **PE-Klemmen-Regel** eingeführt nach Nutzer-Nachfrage „haben
  Druckwächter/Strömungswächter wirklich keine Versorgungsspannung" (siehe
  Regel 8) – `420_000001`/`002` (Schutzklasse I, Datenblatt weist eigene
  Erdungsklemme aus) nachträglich um Schutzleiterklemme `3209536` ergänzt;
  alle anderen Session-54-Geräte gezielt gegengeprüft, keine Änderung
  nötig (Datenblatt-Klemmenplan entscheidet, nicht die Schutzklasse
  allein).
- **`480_000011` „Schaltschrank-USV"** (Phoenix Contact
  QUINT-UPS/24DC/24DC/10 `2320225` + UPS-BAT/VRLA/24DC/1,3AH `2320296`, 3
  potentialfreie Meldekontakte 13/14 Alarm, 23/24 Batteriebetrieb, 33/34
  Batterieladung) – gleiches Planungsfabrikat wie bestehendes
  24V-DC-Netzteil `480_000009`, obwohl Siemens SITOP UPS500S/1600
  ebenfalls passende Alternativen mit Meldekontakten bietet (Nutzer-
  Entscheidung für Marken-Konsistenz). `benoetigt_steuerspannung:'24vdc'`
  ergänzt bei Bedarf automatisch das 24V-DC-Netzteil.
- **Nutzer-Feedback:** nach jeder Baugruppen-Neuanlage eine
  Herleitungstabelle (Klemmen lt. Datenblatt → DBACS-Klemmen/Zone →
  Datenpunkte) mitliefern, siehe Memory `feedback_baugruppen_herleitung.md`.

Alle Baugruppen jeweils direkt im Browser verifiziert (korrekte
Dropdown-Gruppierung/-Sichtbarkeit je Gewerke-Tab, Stückliste/DDC-
Statistik/Steuerspannungs-Automatik stimmen exakt), keine Konsolenfehler –
Details siehe Archiv.

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
- **Onboard-Kapazität der Kompaktstationen** (Artikelnr. seit Session 57
  `PXC4.E16-2`/`PXC5.E24-N`, s. o.) **berücksichtigt:** `buildQueues()`
  entschied bisher über externe TX-I/O-Module BEVOR die gewählte CPU
  aufgelöst war – deren Onboard-Kapazität konnte nie angerechnet werden.
  CPU-Auflösung jetzt vor `computeDdcAutoModules()`; die kompakte
  16-E/A-Station bekam `dp_ai=12`/`dp_ao=12`, die 24-E/A-Station
  `dp_ai=16`/`dp_ao=16`, `dp_bi=2`, `dp_bo=6` (analog zur
  `TXM1.8U`-Konvention: universelle Punkte nur
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

### Modul 4/5 – Session 51 Nachtrag 7–11 (komprimiert)
Vollständiger Sitzungsverlauf archiviert in
`docs/archiv/claude-md-modul4-sessions-35-51.md`. Ergebnisse:

- **Nachtrag 7 – Feldgeräte-Katalog + Modul 5:** Baugruppen-Modularisierung
  (`grundschaltung`/`zusatzbaustein`/`standalone`) diskutiert, aber
  zurückgestellt. Stattdessen neues Excel-Sheet `feldgeraete` (externe
  Betriebsmittel außerhalb des Schaltschranks) + eigenständiges,
  rein lesendes Modul 5 (Struktur wie Modul 7, liest `m04_belegung` +
  beide Kataloge neu ein, aggregiert nach `feldgeraet_artikel_nr`/
  `betriebsmittel`-Freitext). Planungsfabrikat Pumpen: **Wilo**.
  Datenblätter bewusst nicht lokal gespeichert (öffentliches Repo,
  Urheberrecht) – nur Fakten + Quelle-URL in `quelle_hinweis`.
- **Nachtrag 8 – erste 4 Feldgeräte-Baugruppen** (Planungsfabrikat
  Sensoren: **Siemens**): `430_000001`–`004` Raumtemperatursensor passiv
  (QAA24), Raum-CO2 (QPA2000), Raum-VOC (QPA1000), Raumfeuchte (QFA2000) –
  alle `klemm_s`, Klemme `3209510` auch bei aktiven Sensoren (SELV-
  Leitungen brauchen keine Farbcodierung). QAA2071 (aktiv, phase-out) und
  QFA3160 (zu industrielle Optik) bewusst nicht angelegt.
- **Nachtrag 9 – `funktionsbereich` als Array:** Baugruppen können
  mehreren Gewerken gleichzeitig zugeordnet sein (analog
  `einzelbauteile.zone`, Session 44) – `gewerk` selbst bleibt einwertig
  (führendes Gewerk). IDs `480_000008`–`011` → `430_000001`–`004`
  umbenannt (ID kodiert das führende Gewerk).
- **Nachtrag 10 – CO2/VOC-Korrektur + Kombifühler:** CO2/VOC-Sensoren nur
  `lueftung` (nicht heizung/kaelte). Neu `430_000005` Raumtemperatur- und
  Feuchtesensor QFA2060.
- **Nachtrag 11 – Tauchtemperaturfühler:** `430_000006`/`007`, Siemens
  QAE2120.010/.015 (100mm/150mm – einzige real existierenden Baulängen
  dieser Baureihe, vom Nutzer vorgeschlagene 3. Größe existiert nicht).

Alle Schritte direkt im Browser verifiziert (Testbelegungen mit korrekter
Klemmenzahl/DP/Stückliste/Modul-5-Summe je Schritt), keine Konsolenfehler
– Details siehe Archiv.

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

Diese Punkte wurden bereits ausführlich diskutiert und entschieden – nicht neu aufgreifen. **Archiv-Hinweis (16.08.2026, 2. Durchlauf):** ausführliche Session-Protokolle werden zu kompakten Ergebnis-Zusammenfassungen eingedampft (Volltext inkl. Nutzer-Funden/verworfenen Zwischenständen/Verifizierungsdetails liegt in `docs/archiv/claude-md-modul4-sessions-20-29.md`, `docs/archiv/claude-md-modul4-sessions-30-34.md`, `docs/archiv/claude-md-modul4-sessions-35-51.md` (inkl. Nachtrag 7–11), `docs/archiv/claude-md-modul4-session-52.md` und `docs/archiv/claude-md-modul4-sessions-53-54.md`) – Grund: `CLAUDE.md` wird bei jeder Sitzung vollständig geladen, unabhängig vom Umfang der Aufgabe. 1296→902 Zeilen bei diesem Durchlauf (Sessions 53/54 + Session-51-Nachtrag 7–11 ausgelagert, per `sed`-Zeilenbereiche statt Abtippen). Bei künftigen sehr langen Session-Nachträgen ebenso verfahren: verbindliche Regel kompakt in `CLAUDE.md`, ausführliche Vorgeschichte sofort ins Archiv statt erst bei der nächsten Aufräumrunde. Die aus Session 51/52 destillierten Baugruppen-Modellierungsregeln stehen dauerhaft unter „## Baugruppen-Modellierungsregeln (verbindlich)" weiter oben.

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
