# DBACS – Revisionsstand

> **Sitzung pausiert (Nutzer-Auftrag „Speichere den Zustand, wir machen
> morgen weiter", 10.10.2026, Ende Session 76).** Alles bis hier beschrieben
> ist bereits in `ga_komponenten.xlsx` eingetragen, exportiert, committet
> und Browser-verifiziert – kein Excel-Schreibschritt steht aus. Beim
> Fortsetzen offen (keine Reihenfolge vorgegeben):
> 1. **RKW-Datenpunkt-Rückfrage:** Nutzer behauptete, das adiabatische
>    Rückkühlwerk habe weniger Datenpunkte als das trockene – live nicht
>    reproduzierbar (adiabatisch hat durchgängig gleich viele oder mehr).
>    Nutzer nach der genauen verglichenen Konfiguration/Ansicht fragen.
> 2. **Pumpen/Ventile bei der Kältemaschine** (`420_A00038`) ergänzen –
>    vom Nutzer bewusst zurückgestellt, bis geklärt ist, welcher Kreislauf
>    gemeint ist (Kaltwasser-Verdampferkreis? Kondenswasser-/Glykolkreis
>    zum Rückkühlwerk? Beides?).
> 3. **Weitere Kälte-Korrekturen** nach Bedarf (der ursprüngliche Auftrag
>    „Bevor wir an der Kälte korrigieren" war nur ein Platzhalter ohne
>    vorab festgelegten Gesamtumfang – bisher abgearbeitet: Ausstattungs-
>    Dokumentation, RKW-Größen-Eingabefelder, Klemmen-Fehler-Scan. Ob damit
>    "die Kälte-Korrektur" insgesamt erledigt ist, mit dem Nutzer klären).
> Danach zurück zum ursprünglich (Session 74) angekündigten nächsten Thema,
> falls noch relevant.

**Stand:** 10. Oktober 2026 – Session 76 Teil 2: Klemmen-Fehler gefunden+
behoben. Nutzer-Fund: AO/BO/BI brauchen IMMER 2 Klemmen (Signal+Referenz/
Rückleitung) – bei der Kältemaschine/RKW-Kern/Glykolwarnanlage fehlte die
Referenzklemme komplett (nur 1 statt 2 je Signal). Katalogweiter Scan nach
demselben Muster: 6 Baugruppen betroffen (`420_000065`/`068`/`071`/`080`,
`420_000005`, `430_000039`–`042`), alle korrigiert. Pumpen/Ventile/Klappen
auf Nutzer-Bitte ebenfalls geprüft – dort bereits alles korrekt, keine
Änderung nötig. 2 Sensor-Baugruppen mit dokumentiertem geteiltem
Referenzschema (QAA27, Raum-CO2-Kombifühler) bewusst unverändert gelassen.
Zweite Nutzer-Frage (RKW adiabatisch habe weniger Datenpunkte als trocken)
live nachgerechnet – **nicht reproduzierbar**, adiabatisch hat durchgängig
gleich viele oder mehr Datenpunkte. Rückfrage an Nutzer offen. Details:
`CLAUDE.md` → „Offene Punkte" Nachtrag Session 76 Teil 2.

Vorheriger Stand – Session 76 Teil 1: Kälte-Korrektur begonnen. Nutzer-
Fund „Ausstattung der Kältemaschine/Rückkühlwerke im Auswahltext nicht
erkennbar" – Dokumentation der aktuellen Ausstattung (vereinbarte Vorlage)
vorgelegt, bestätigt dass die 3 Anlagen (`420_A00038`–`040`) bewusst reine
Monitoring-Schnittstellen sind (Regel 7). **Pumpen/Ventile bei der
Kältemaschine bleiben zurückgestellt** (Nutzer: erst fachlich klären,
welcher Kreislauf gemeint ist). **Rückkühlwerk-Größe umgesetzt:** neue
generische Engine-Fähigkeit „Mengenfeld" (`anlagen_baugruppen.mengenfeld`,
Zahlenfeld statt Dropdown, kombinierbar mit `gruppe`) – „Anzahl Kühlreihen"
+ „Anzahl Motoren" sind jetzt echte Eingabefelder bei `420_A00039`/`040`,
steuern automatisch die Menge der Lüfterdrehzahl-/Lüfter-Einzelmeldung-/
Magnetventil-Datenpunkte. Browser-verifiziert, keine Regression. Details:
`CLAUDE.md` → „Offene Punkte" Nachtrag Session 76. **Nächster Schritt:**
Pumpen/Ventile-Frage klären, dann weitere Kälte-Korrekturen nach Bedarf.

Vorheriger Stand – Session 75: RLT-Anlagen (Lüftung) **eingetragen**
(Freigabe erteilt: „Lege die RLT-Anlagen an"). 9 neue Baugruppen
`430_000062`–`070`, 8 neue `feldgeraete`-Zeilen, **7 neue Anlagen**
`430_A00001`–`007` – die 4 ursprünglich geplanten komponierten RLT-Anlagen
(Abluftanlage einfach, Zuluftanlage einfach, Zu-/Abluftanlage ohne WRG,
Vollklimaanlage-Baukasten) **plus 3 neue standalone Register-Anlagen**
(Vorerhitzer/Nacherhitzer/Luftkühler, `430_A00005`–`007`) auf Nutzer-Wunsch,
damit Register auch manuell zu beliebigen Lüftungsanlagen zusammengesetzt
werden können. Dafür Anlagen-Engine erweitert (`gruppe`-Optionen können
jetzt mehrere bg_ids bündeln, per `variante_label` statt `bg_id` gematcht –
nötig, da Register wie „Vorerhitzer, klein" aus mehreren eigenständigen
Baugruppen bestehen) + dabei gefundenen Escaping-Bug behoben (Options-
Erzeugung jetzt per DOM-Konstruktion statt String-Interpolation).
Browser-vollständig verifiziert (`testKatalogScan`/`testBaugruppe`/
`testAnlage`, inkl. Regressionstest bestehender Anlagen mit `gruppe`-
Varianten). Export: baugruppen 234→243, feldgeraete 116→124, anlagen 46→53.
Details: `CLAUDE.md` → „Offene Punkte" Nachtrag Session 75.
**Im Anschluss (selbe Sitzung):** Nutzer-Fund „keine Sicherung bei
Wärmepumpe ergänzt" führte zu neuen Elektro-Baugruppen „Leistungsabgänge
Schaltschrank" (Wechsel-/Drehstrom generisch + Drehstrommotor-Direktanlauf).
Erste Fassung nutzte Anlagen mit Meldung-Dropdown – Nutzer-Korrektur („eher
als Baugruppe, weil überschaubar – Anlagen sind Kombinationen mehrerer
Baugruppen") führte zum Rückbau: **finaler Stand 24 plain Baugruppen**
`440_000042`–`052`/`055`–`067` (je Kernschritt + „mit Meldung"-Zwilling),
inkl. nachträglich ergänztem 6A-Wechselstrom-Schritt (Nutzer-Fund).
Dabei einen Engine-Bug gefunden+behoben, der die GESAMTE bestehende
Anlagen-Engine betraf (HTML-Escaping in `updateAnlageVariantenUI()`, siehe
CLAUDE.md – bleibt als Fix erhalten, unabhängig vom verworfenen Anlagen-
Ansatz). Export (finaler Stand): baugruppen 243→**267**, anlagen netto
unverändert **53** (11 Anlagen wieder entfernt). Alles Browser-verifiziert.
**Danach weiterhin:** zurück zur angekündigten Kälte-Korrektur
(ursprüngliche Nutzer-Ankündigung, noch nicht begonnen).

Vorheriger Stand – Session 74 (RLT-Anlagen-Planung vor Freigabe) siehe
`CLAUDE.md`-Archiv der Session-Nachträge.

Stand davor – Session 73 (Modul 4,
`modules/modul-04-innenaufbau/index.html`): Hinweis bei Klemmleisten-
getriebenem Feldwechsel. Nutzer-Praxistest (mehrere Baugruppen-/Anlagen-
Kombinationen, insbes. Motor-Brandschutzklappenantriebe in hoher Stückzahl)
zeigte, dass Feldwechsel bei Mehrfeld-Schränken oft erfolgen, obwohl
Leistungs-/Steuerzone noch deutlich unterausgelastet sind – limitierender
Faktor ist fast immer die Abgangsklemmleiste (klemm_l/klemm_f). Eine zweite
Klemmleistenreihe wurde geprüft und verworfen (Kabelüberlappung bei
Neuanlage). Stattdessen: `platziereBaugruppenFuerFeld()` liefert jetzt
`blockedZones` (welche Zone den Dry-Run-Fit-Check einer Baugruppen-Instanz
tatsächlich blockierte), `calculateFelder()` setzt daraus `feld.klemmHinweis`
nur wenn AUSSCHLIESSLICH klemm_l/klemm_f/klemm_s blockierten (nicht
leist/steuer) – UI zeigt das als kompaktes amber „!"-Badge (mit Tooltip) in
der Ecke der betroffenen Feld-Zeichnung, analog zum bestehenden Reserve-
Warndreieck (`#reserve-warn`), absolut positioniert ohne Einfluss auf das
Flex-Layout (ein erster Zwischenstand mit einer eigenen Banner-Zeile hatte
die Schranksicht-Größe kaputtgemacht – gefunden per Nutzer-Screenshot,
behoben/verworfen zugunsten des Badge-Ansatzes). Browser-verifiziert
(50×/300×-BSK-Testfall, Hinweis korrekt nur bei reinem Klemmleisten-Engpass,
Schranksicht-Größe unverändert), vollständiger
Katalog-Regressionstest: `testKatalogScan()` sauber, `testBaugruppe()`
234/234, `testAnlage()` 46/46, keine Konsolenfehler. Zusätzlich Nutzer-
gemeldete scheinbare Inkonsistenz untersucht (60→61× BSK verschob ein
ganzes zusätzliches Paar statt nur der neuen Instanz) – Ursache gefunden
(`redistributeKlemmBands()` berechnet Klemmleisten-Breiten global statt
lokal neu, direkt gemessen: klemm_f-Band 312,0mm→304,6mm), Baugruppen-
Zusammenhalt NICHT verletzt (29 vollständige Paare je Zone deckungsgleich
nachgewiesen). Nutzer-Entscheidung nach Vor-/Nachteil-Abwägung: bewusst
NICHT beheben, aktuelles Verhalten akzeptiert (Hauptgrund: Fix würde die
in derselben Sitzung bestätigte Reihenfolgenunabhängigkeit gefährden).
Details: `CLAUDE.md` → „Offene Punkte" Nachtrag Session 73.

Vorheriger Stand – Session 72 (Modul 4 Katalog,
`data/ga_komponenten.xlsx`): Fork-Recherche Kältemaschinen/Rückkühlwerke/
Glykol-/Gaswarnanlage (Session 71) nach Nutzer-Feedback finalisiert und
eingetragen. 3 neue Anlagen: Kältemaschine ≥250kW, Rückkühlwerk trocken
≥250kW, Rückkühlwerk adiabatisch ≥250kW (je mit Modbus-RTU/TCP-
Pflichtdropdown). Kernkorrekturen ggü. der Freigabe-Vorlage: Economizer-
Punkt bei der Kältemaschine entfernt; Rückkühlwerk bekommt zusätzlich die
Eintrittstemperatur physisch (2. Tauchfühler); „Betriebsmeldung Ventilator"
zur Sammelmeldung umbenannt; Lüfterdrehzahl-Sollwert (je Bank/Reihe) und
Lüfter-Einzelmeldung Betrieb/Störung (je Ventilator) als eigenständige,
frei mehrfach hinzufügbare Baugruppen modelliert – darüber werden auch sehr
große Rückkühlwerke (viele Bänke/Ventilatoren) allein über die Mengen-
eingabe abgedeckt, ohne neue UI; bei der adiabatischen Variante zusätzlich
ein Magnetventil-Zubehör je Bank (Auf/Zu, keine Pumpe). Glykolwarnanlage
jetzt als eigenständige, mehrfach verwendbare Baugruppe (230V AC, eigener
FI/LSS-Abgang mit Ruhestromketten-Hilfsschalter) statt eigener Anlage – als
Standardmitglied in beiden Rückkühlwerk-Anlagen gebündelt. Gaswarnanlage-
Schnittstelle ebenfalls als eigenständige Baugruppe (Gewerk 450, analog
BMA/Gaslöschanlage). 19 neue Baugruppen, 5 neue Feldgeräte, 3 neue Anlagen.
Export: baugruppen 215→234, feldgeräte 111→116, anlagen 43→46,
einzelbauteile unverändert 226. Vollständig regressionsgetestet:
`testKatalogScan()` sauber, `testBaugruppe()` 234/234, `testAnlage()`
46/46, plus End-to-End-Integrationstest (Rückkühlwerk + 2 Lüfterbänke +
20 Einzelventilatoren) ohne Overflow/fehlende Platzierung. Details:
`CLAUDE.md` → „Offene Punkte" Nachtrag Session 72.

Vorheriger Stand – Session 71 (Modul 4 Katalog,
`data/ga_komponenten.xlsx`): Anlagengruppe Kälte – 12 neue Anlagen durch
Duplikation bestehender Heizungs-Anlagen (Kältekreis Verteilung,
Kälteverteiler-/Sammler, Kälteübertrager), zugrundeliegende Baugruppen
unverändert wiederverwendet, nur Namen/Kategorie/Kältemengenzähler-
Referenzen angepasst. Fußbodenheizkreise und Wärmeerzeuger (Fernwärme)
bewusst nicht dupliziert (kein Kälte-Pendant). Export anlagen 31→43.
Vollständig regressionsgetestet: alle 12 neuen Anlagen einzeln
`testAnlage()`-geprüft, 215/215 Baugruppen, 43/43 Anlagen gesamt,
`testKatalogScan()` sauber. Details: `CLAUDE.md` → „Offene Punkte" Nachtrag
Session 71.

Vorheriger Stand – Session 70 Teil 9 (Modul 4, Verifikation):
neuer `zone_modus` „einsp_leist_misch" (Teil 8) rechnergestützt gegen den
gesamten Katalog geprüft statt nur den einen BSK-Testfall – alle 215
Baugruppen einzeln 0 Fehler, 2 Mengen-Stresstests (300×/500×) bestätigen
die Mehrfeld-Kaskade (F→G→G→E→E bzw. F→G→E) sauber demand-getrieben ohne
Overflow. Optische Kontrolle + DOM-Abgleich bestätigt Feld-Zonen exakt
deckungsgleich mit `FELDTYP_ZONEN.F`/`.E`. Standard-Regressionstest erneut
bestanden (215/215 Baugruppen, 31/31 Anlagen, `testKatalogScan()` sauber).
Details: `CLAUDE.md` → „Offene Punkte" Nachtrag Session 70 Teil 9.

Vorheriger Stand – Session 70 Teil 8 (Modul 3 +
`modules/modul-04-innenaufbau/index.html`): neuer `zone_modus`
„Einspeisung+Leistung gemischt, Steuerung getrennt" (`einsp_leist_misch`) –
Spiegelbild zum bestehenden `einsp_misch`. 2 neue Feldtypen F (Erstfeld:
Einspeisung+Leistung, kein steuer/klemm_s) und G (Folge-Leistungsfeld bei
Überlauf, ohne Einspeisung); Feld 2+ nutzt das bestehende Typ E
(Steuerung) unverändert. Komplett über den bereits bestehenden generischen
`buildLayoutForFeldtyp()`-Mechanismus (Session 48) umgesetzt – nur
Zonenmengen/Wachstumsziel/Label/Feldplan ergänzt, keine Kernlogik-
Änderung. Verifiziert: 50×-BSK-Testfall passt jetzt komplett (alle 50
Instanzen) in Feld 1, Feld 2 enthält CPU/DDC; 215/215 Baugruppen, 31/31
Anlagen, `testKatalogScan()` sauber. Details: `CLAUDE.md` → „Offene
Punkte" Nachtrag Session 70 Teil 8.

Vorheriger Stand – Session 70 Teil 7 (Modul 4,
`modules/modul-04-innenaufbau/index.html`): letzte Hutschienenreihe einer
Zone (z. B. DDC-Module in `steuer`) braucht keinen eigenen 40mm-
Verdrahtungskanal mehr, wenn direkt im Anschluss an die Zone bereits ein
Zonentrennkanal existiert (Nutzer-Fund per Screenshot: eine Reihe passte
von der Gerätehöhe her noch, scheiterte aber am zusätzlichen
Zwischen-Kanal, obwohl direkt danach ohnehin schon ein Kanal zur
Nachbarzone folgt). Neues `followedByKanal`-Flag je Band
(`getZoneBands()`) + neuer Fallback-Zweig in `placeInBands()`. Isoliert
funktional verifiziert (mit Flag: alle Reihen passen; ohne Flag:
Regressions-Gegenprobe bleibt korrekt bei Overflow) + vollständiger
Katalog-Regressionstest: 215/215 Baugruppen, 31/31 Anlagen,
`testKatalogScan()` sauber. Details: `CLAUDE.md` → „Offene Punkte"
Nachtrag Session 70 Teil 7.

Vorheriger Stand – Session 70 Teil 6 (Modul 4,
`modules/modul-04-innenaufbau/index.html`): Teil-5-Ansatz korrigiert
(Nutzer-Fund per Screenshot: pauschales Zusammenlegen lückenlos
übereinanderliegender Bänder rückte ALLE Hutschienenreihen einer Zone auf
die schmalere Breite ein, nicht nur die tatsächlich grenzüberschreitende –
unnötig verschenkter Platz). Jetzt in `placeInBands()`: jede Reihe prüft
zuerst normal gegen das aktuelle Band mit dessen EIGENER Breite; passt sie
dort nicht mehr, bekommt NUR diese eine Reihe (falls das nächste Band
lückenlos anschließt und der kombinierte Rest reicht) die schmalere
Schnittmengenbreite – alle anderen Reihen bleiben unverändert breit.
Verifiziert: 50×-BSK-Testfall nimmt jetzt 28 Instanzen in Feld 1 auf
(besser als der verworfene Teil-5-Ansatz mit 24, und deutlich besser als
die ursprünglichen 18); 215/215 Baugruppen, 31/31 Anlagen,
`testKatalogScan()` sauber. Details: `CLAUDE.md` → „Offene Punkte"
Nachtrag Session 70 Teil 6.

Vorheriger Stand – Session 70 Teil 5 (verworfen/korrigiert, siehe Teil 6
oben) – Session 70 Teil 4 (Modul 4 Katalog,
`data/ga_komponenten.xlsx`): neue Phoenix-Contact-Klemme `3210596` (PTTB
2,5-PE, Doppelstock-PE-Variante, dimensionsgleich zu `3210567`) ergänzt und
als `doppelstock_variante_artikel_nr` an `3209536` (Standard-PE-Klemme)
gehängt – löst die offene Frage, ob eine Doppelstockklemme neben einer
Standard-PE-Klemme montiert werden darf (keine Mischmontage mehr nötig,
beide Typen bleiben in derselben Baureihe). Export einzelbauteile
225→226. Verifiziert: 50×-BSK-Testfall liefert jetzt 25× `3210596` bei
Doppelstock statt 50× unpaariger `3209536`; 215/215 Baugruppen, 31/31
Anlagen, `testKatalogScan()` sauber. Details: `CLAUDE.md` → „Offene
Punkte" Nachtrag Session 70 Teil 4.

Vorheriger Stand – Session 70 Teil 3 (Modul 4,
`modules/modul-04-innenaufbau/index.html`): Steuerspannungs-Trafo+LSS
landete bei Mehrfeld-Schränken im falschen Feld, getrennt von der CPU, die
er versorgt (Nutzer-Fund: „Energieverteilung und Trafos gehören in Feld
1"). Root Cause: die automatisch ergänzte Steuerspannungs-Baugruppe wurde
in `bgInstanceQueue` ans Ende angehängt statt an den Anfang – andere
Baugruppen (z. B. 50× Brandschutzklappenantrieb) belegten dadurch in Feld 1
bereits die `leist`-Zone, bevor der Trafo (atomar mit der LSS in `evert`,
Baugruppen-Zusammenhalt) sein Platzgesuch stellen konnte, und rutschte
komplett – inkl. der LSS, obwohl `evert` in Feld 1 noch leer war – ins
nächste Feld. Fix: `unshift()` statt `push()`, die Steuerspannungs-Instanz
reserviert sich jetzt als Erste Platz in Feld 1. Regressionsgetestet:
215/215 Baugruppen, 31/31 Anlagen, `testKatalogScan()` sauber. Details:
`CLAUDE.md` → „Offene Punkte" Nachtrag Session 70 Teil 3.

Vorheriger Stand – Session 70 Teil 2 (Modul 4,
`modules/modul-04-innenaufbau/index.html`): Klemmleisten-Umverteilung
(`redistributeKlemmBands()`) von Defizit- auf Bedarfs-proportionale
Verteilung umgestellt (löst „klemm_f/klemm_l limitieren, obwohl leist/
steuer noch Platz haben" bei vielen gleichartigen Baugruppen-Instanzen) +
2 echte Doppelstock-Bugs gefunden und behoben (`resolveBaugruppenBauteile()`
verwarf bei >2 gleichartigen Zeilen je Baugruppe zu viele Klemmen statt
paarweise zu gruppieren; `buildQueues()`/`aggregateStueckliste()` halbierten
pauschal die GESAMTE Baugruppe statt nur tatsächlich doppelstockfähige
Artikel – z. B. Schutzleiterklemmen/Koppelrelais wurden fälschlich
halbiert). Vollständig regressionsgetestet: 215/215 Baugruppen, 31/31
Anlagen, `testKatalogScan()` sauber, 4 Klemmenvarianten × 50er-Stresstest
verifiziert. Details: `CLAUDE.md` → „Offene Punkte" Nachtrag Session 70
Teil 2.

Vorheriger Stand – Session 70 Teil 1 (Modul 4 Katalog,
`data/ga_komponenten.xlsx`): Wärmepumpen/Kältemaschinen bis 250 kW –
5-Fork-Recherche (Viessmann/Buderus/Carrier/Skadec+Mitsubishi/generische
Normen+Sensorik, Kernbefund: keine öffentliche Modbus-Registerliste bei
den 4 Herstellern, nur Mitsubishi A1M+ liefert eine belastbare komplette
Punkteliste; AMEV „Technisches Monitoring 2020" als beste Normengrundlage
für Wärmepumpen-GLT-Punkte) + 8 neue Anlagen „Wärmepumpe bis 250 kW"
(`420_A00018`–`025`, Luft-Wasser/Wasser-Wasser × monovalent/reversibel ×
interne/externe Sekundärpumpe) mit Nutzer-vorgegebener physischer +
kommunikativer Datenpunktliste (Modbus RTU, 2 Buskabel-Klemmen zusätzlich
zu den DP). 8 neue DDC-Kern-Baugruppen `420_000057`–`064` + 2 generische
Feldgeräte-Platzhalter `WP-LW-250`/`WP-WW-250`. Export: baugruppen
207→215, feldgeraete 109→111, anlagen 23→31. Vollständig Browser-
verifiziert (`testAnlage()` über alle Optionsfeld-Kombinationen, 0
Fehler, 0 Overflow, 0 verwaiste Referenzen), alles committet + gepusht.
**Nächster Schritt:** Kesselkreis (Fork 2) weiterhin offen, danach Kälte-/
Lüftungs-Anlagen. Details: `CLAUDE.md` → „Offene Punkte" Nachtrag Session
70 + `scratchpad/waermepumpen_datenpunkte_synthese.md` +
`scratchpad/waermepumpen_anlagen_freigabe_vorlage.md`.

Vorheriger Stand – Session 69 (06.10.2026, Modul 4 Katalog,
`data/ga_komponenten.xlsx` + `modules/modul-04-innenaufbau/index.html`):
„Heizkreise Verteilung" fertiggestellt und erweitert – inzwischen 23
Anlagen gesamt: Heizkreise Verteilung (9), Heizungsverteiler-/Sammler (2),
Wärmeübertrager (3: Wärmetauscher/Weiche/Puffer, 1 Pumpen-Variante),
Wärmeerzeuger (2: Fernwärmeübergabestation, 1 Pumpen-Variante). Neue
generische `gruppe_optional`-Mechanik (Ohne/Mit-Dropdowns in Anlagen, z. B.
Busanbindung/WMZ). Neue, direkt in Modul 4 eingebaute Testroutine
(`testBaugruppe`/`testAnlage`/`testAlles`, Browser-Konsole) – prüft
Platzbedarf, Katalog-Referenzen, Positionierung und Reserve-Konsistenz
automatisiert; fand dabei 2 echte Bugs (Doppeleinspeisung-Filter blendete
fälschlich alle Nicht-Automation-Anlagen aus; `0`-Reserve-Eingabe wurde
durch Falsy-Check fälschlich auf 20% zurückgesetzt), beide behoben. Neuer
„↺ Schrank leeren"-Button in Modul 4. Namensregel „Ausstattung muss im
Namen erkennbar sein" eingeführt und rückwirkend angewendet. Vollständig
Browser-verifiziert (207/207 Baugruppen, 23/23 Anlagen, 0 Fehler), alles
committet + gepusht. **Nächster Schritt:** Kesselkreis (Fork 2) fehlt noch,
danach Kälte-/Lüftungs-Anlagen (Fork 4/5, Recherche bereits fertig).
Details: `CLAUDE.md` → „Offene Punkte" + Memory `project_anlagenbaugruppen.md`
Abschnitt 5–10 + „SITZUNGSENDE Session 69".

Vorheriger Stand – Session 67 (Modul 4 Katalog,
`data/ga_komponenten.xlsx`): Start des Anlagen-Features (Schritt 1+2 für die
Automation-Anlagen ①/②/④a/④b, Details `CLAUDE.md` → „Offene Punkte"). Neue
Baugruppe `480_000036` „Schaltschrank-Innenleuchte mit Servicesteckdose, FI
Typ B + LSS, Magnetmontage" (Phoenix Contact PLD E 608 W 315/F) + Korrektur
`480_000018` (LSS `5SL6116-6` ergänzt, schließt VDE-0100-430-Normenlücke des
reinen FI `5SV3321-4` – Siemens hat keinen Typ-B-FI/LS-Kombischalter, Doepke-
Alternative vom Nutzer abgelehnt, zwei Siemens-Bauteile + Ruhestromketten-
Hilfsschalter stattdessen). Export: einzelbauteile 218→221, baugruppen
181→182, feldgeraete unverändert 96. Danach Schritt 3 fertig umgesetzt:
neue Sheets `anlagen`/`anlagen_baugruppen` + `data/anlagen.json`,
`addAnlage()`/Varianten-Auswahl (TouchPanel-Größe, UMG-Protokoll,
Netztyp-Auto-Auflösung) in Modul 4 – 3 Automation-Anlagen jetzt im
„Anlage"-Tab wählbar (`480_A00001` Standard ohne die Hutschienensteckdose
`480_000018`, `A00002` mit Bedienpanel, `A00003` hohe Verfügbarkeit mit
USV). Browser-verifiziert, keine Konsolenfehler. Details: `CLAUDE.md` →
„Offene Punkte" Sitzungsstand Session 67 + Nachtrag.

Vorheriger Stand – Session 66 (14.09.2026, Modul 4,
`modules/modul-04-innenaufbau/index.html`): weitere Automation-Baugruppen für
die ASP-Grundausstattung. `480_000021` um Wischrelais `RE22R2HMR` ergänzt;
`480_000018` (Schaltschranksteckdose) von LSS auf FI Typ B `5SV3321-4`
korrigiert (heute Pflicht, keine Planungsfabrikat-Abweichung nötig); 3 neue
Baugruppen: Überspannungsschutz Schaltschrankzuleitung (`480_000033`, DEHNguard
`952305` MIT Fernmeldung statt `952300`), Phasenüberwachung 400V AC
(`480_000034`, `3UG5616-1CR20`) und 230V AC (`480_000035`, `3UG4631-1AW30`).
Export: einzelbauteile 214→218, baugruppen 178→181. Details: `CLAUDE.md` →
„Offene Punkte" Sitzungsstand Session 66.

Vorheriger Stand – Session 65 (Modul 4,
`modules/modul-04-innenaufbau/index.html`): erste 14 ASP-Grundausstattungs-
Baugruppen (Automation, Vorarbeit für die Anlagen-Funktion) angelegt –
Hauptschalter mit Stellungsmeldung, Phasenkontrollleuchten, Störquittiertaster
mit Sammelstörungsleuchte, 6 Handschalter-Varianten, Betriebs-/Störmeldeleuchte
je „über Schaltschranksteuerung" und „DDC-Ansteuerung (BO)", Not-Halt mit
Auslösemeldung. Alle schrankintern ohne Klemmen (Regel 12). Dabei wichtigen
Bugfix in `buildQueues()` gefunden+behoben: physische DP-Overrides auf
Tür-Bauteilen (`zone:'tuer'`) wurden vor dem Fix komplett verworfen (Guard
`if(!queues[zone]) return` stand vor der Datenpunkt-Zählung). Export:
einzelbauteile 211→214, baugruppen 164→178. Details: `CLAUDE.md` → „Offene
Punkte" Sitzungsstand Session 65.

Vorheriger Stand – Session 64, Nachtrag 6 (Modul 4,
`modules/modul-04-innenaufbau/index.html`): Quittiertaster bekam eine eigene
Ebene zwischen Phasenleuchten und Not-Halt (teilte sich vorher fälschlich
das Band mit der roten Störmeldung, Nachtrag-5-Fehlgriff), Störmeldung/
Betriebsmeldung-Steg auf Nutzer-Wunsch halbiert (funktional zusammengehörig).
Auf beiden Referenztüren kollisionsfrei verifiziert. Der Messgerät+
Touchpanel-Restpunkt (rechnerisch bestätigt unlösbar per Bänder-Stauchen)
ist jetzt gelöst, indem die wählbare Touchpanel-Baugröße (PXM40/PXM50) im
Dropdown von der Türhöhe UND einem tatsächlich bereits platzierten
Messgerät abhängt (`tuerTouchpanelPasstAufTuer()`), statt Worst-Case gegen
das größte Katalog-Messgerät zu prüfen. Details: `CLAUDE.md` → „Offene
Punkte" Sitzungsstand Session 64 Nachtrag 6.

Vorheriger Stand – Session 64, finaler Stand nach 5 Nachträgen:

1. **Türband-Reihenfolge final** (mehrfache Nutzer-Korrektur per Browser-
   Review, Ausgangspunkt: "Touchpanel muss in Kopfhöhe bedienbar sein"):
   unten→oben Hauptschalter < Phasenleuchten (weiß) < Not-Halt (exklusiv) <
   Störmeldung (rot) + Quittiertaster < Betriebsmeldung (grün) <
   Handschalter < Messgerät < Touchpanel/Romutec-LVB-Ebene. Werte:
   `TUER_BAND_HAUPTSCHALTER` 0,30 · `PHASENKONTROLLE` 0,41 · `NOTHALT` 0,47 ·
   `STOERMELDUNG`/`QUITTIERTASTER` 0,53 · `BETRIEBSMELDUNG` 0,585 ·
   `HANDSCHALTER` 0,64 · `MESSGERAET` 0,74 · `TOUCHPANEL` 0,85 (=exakt
   1700mm auf dem 2000mm-Standschrank, Nutzer-Ziel "ca. 1,7m Kopfhöhe"
   bestätigt).
2. **Katalogkorrektur, 4 Bauteile** (Original-Siemens-Datenblätter direkt
   gelesen statt der unzuverlässigen Web-Zusammenfassung; wiederkehrendes
   Muster "Katalogwert = Einbau-/Bohrungsdurchmesser statt reales
   Bauteilmaß"): Not-Halt-Pilzdrucktaster `3SU1100-1HB20-1CH0` 22→40mm,
   Signalleuchten `3SU1102-6AA20/-40/-60-3AA0` (rot/grün/weiß) je 22→29,5mm,
   Handschalter/Wahlschalter `3SU1100-2BL60-3NA0` 22→32,3mm, Quittiertaster
   `3SU1152-0AB50-1BA0` 22→29,5mm.
3. **Mindest-Stegmaß für reale Blechtür-Ausschnitte eingeführt** (Nutzer-
   Hinweis: Bänder bestimmen auch, wo später in die ~1,5mm-Blechtür
   gefräst wird – zwischen Ausschnitten muss Steg-Blech stehen bleiben):
   12mm Standardpuffer, 22mm für den größeren Übergang Messgerät→
   Touchpanel, statt der ursprünglichen 5mm.
4. **Verifiziert auf BEIDEN Referenztüren** (800×800 Wandschrank, 1200×2000
   Standschrank, alle 9 Türbauteile gleichzeitig, direkte SVG-Rect-
   Kollisionsprüfung): Standschrank 0 Überlappungen; Wandschrank nur noch
   die eine bewusst zurückgestellte Randkombination Messgerät+Touchpanel-
   PXM50 gleichzeitig auf sehr kleiner Tür (Touchpanel dort laut Nutzer
   "gar nicht oder nur klein vorhanden"). Keine Konsolenfehler.
5. **Romutec-LVB (dritte Realisierung neben DDC-Modul/Metz) implementiert:**
   `computeLvbRomutecDevices()`-Stub aufgelöst, DDC-Seite bleibt normal,
   RAG2020 (AO, 4 Kanäle/Karte)/RKS3030 (BO generisch, 6 Kanäle/Karte)
   seriell zwischen DDC und Koppelrelais/Aktor – kein separates
   Koppelrelais nötig (steckt im Romutec-Modul). Neuer LVB-Trägerrahmen-
   Ratchet (RTR4050S/RTR4084S/RTR7050S + RLA8000-Leerplatten für
   unbestückte Plätze), Trägerrahmen als 2 verschachtelte Rechtecke auf dem
   Touchpanel-Türband gezeichnet. BI bleibt bei Romutec bewusst unverändert
   direkt an der DDC (Nutzer-Vorgabe: Fail-Operational-Anforderung bei
   DDC-Ausfall, kein Bus, keine Doppelverdrahtung). 9 neue Katalogeinträge
   (einzelbauteile 202→211).
6. **Gewerke-Tabs neu strukturiert:** zweite Button-Reihe „Anlagen" (8
   Gewerke, gestrichelter Rahmen, orange bei Auswahl) direkt unter der
   regulären Baugruppen-Reihe, identische Schriftgröße/Spaltenbreite für
   exakte Spaltenausrichtung; Label über der Auswahl auf „Baugruppe ·
   Anlage" geändert (dasselbe Dropdown wird künftig für beides genutzt).
   **Datenmodell noch nicht umgesetzt** – siehe unten, nächster Schritt.

Export unverändert **einzelbauteile 202→211** (9 neue Romutec-Teile), **9
neue Baugruppen NICHT enthalten** (Anlagen-Feature startet erst als
nächstes). Vor Beginn der Anlagenbaugruppen-Arbeit Backup nach
`C:\Users\SMI\Backups\dbacs\excel\` gezogen (siehe unten). Details:
`CLAUDE.md` → „Offene Punkte" Sitzungsstand Session 64 + Nachträge 1–5.

**Nächster Schritt (bereits besprochen, noch nicht implementiert):**
Anlagenbaugruppen – eine Anlage referenziert mehrere bestehende, bereits
verifizierte Baugruppen und fügt sie beim Hinzufügen als normale
`{typ:'baugruppe', bg_id, menge}`-Einträge in die Belegung ein (keine
Verschachtelung im Datenmodell, keine Änderung an Platzierung/Stückliste/
DP-Logik nötig – siehe Memory `project_anlagenbaugruppen.md`). Fehlbedienung
(falsche Anlage gewählt) wird nicht automatisch rückgängig gemacht, Nutzer
löscht die einzelnen Baugruppen manuell oder beginnt neu – kein Ziel der
Anwendung, Korrekturkomfort zu bieten.)

Vorherige Session 62 (12.09.2026): 6 neue Sanitär-Baugruppen
`410_000001`–`410_000006`, Gewerk 410 vorher leer: Reflex Nachspeise-/
Druckhaltetechnik – Fillset Compact Twist M-Bus, Fillcontrol Smart, Reflexomat
XS, Variomat Touch VS 2, Servitec S – + Viega Hygiene-Spülstation 2241.10.
Erster 4-20mA-Anwendungsfall im Katalog (Variomat Druck/Niveau) → neue
`TXM1.8X`/`TXM1.8X-ML`-Katalogzeilen; DDC-Ratchet ist noch signalart-blind
(offener Punkt). Neue Regel 15 (Koppelrelais auch bei geräteeigener
potentialfreier Brücken-Anforderung). Kurzer Siemens-Tauchfühler ohne
Tauchhülse recherchiert, aber NICHT katalogisiert (kein aktives Produkt).
Export baugruppen 113→119 · einzelbauteile 190→192 · feldgeraete 61→67.
Details: `CLAUDE.md` → „Offene Punkte" Sitzungsstand Session 62.)

Vorherige Session 60 (08.09.2026): Zonen-Korrektur Ventilator-Baugruppen
`430_000028`–`430_000036`: PTC-Auslösegerät `3RN2012-1BW30` und Koppelrelais
`2967073` von Zone `steuer` → `leist` in allen 9 Asynchronmotor-Baugruppen +
Katalog-Default `3RN2012-1BW30` `steuer` → `leist`. Motorschutzschalter bleibt
in `leist` (Nutzer-Vereinfachung), PTC-Fühlerklemmen bleiben `klemm_f`.
Export unverändert baugruppen 113 · einzelbauteile 190 · feldgeraete 61.
Neue verbindliche **Regel 13** in `CLAUDE.md`. Details: `CLAUDE.md` → „Offene
Punkte" Sitzungsstand Session 60.)

Vorherige Session 59 (07.09.2026): Lüftung: 17 Ventilator-Baugruppen
`430_000028`–`430_000044` – Asynchronmotor 230 V/400 V mit Direktanlauf,
Stern-Dreieck-Anlaufschaltung, Dahlander 2-Touren und FU-geregelt; EC-Ventilatoren
drehzahlgeregelt; 2 Kommunikationsmodule Modbus RTU/TCP. + 43 Einzelbauteile
(3RV2-/3RT2-Lücken, Stern-Dreieck-Kombis 3RA24, Überlastrelais 3RU2, PTC-
Auslösegerät 3RN2012, Reparaturschalter KG32–KG80) + 9 Feldgeräte.
Bestand-Korrektur Hilfskontakt 0758484→0319691 auch bei Pumpen 420_000022–026.
Export: baugruppen 113 · einzelbauteile 190 · feldgeraete 61. Details in
`scratchpad/ventilatoren_katalog_final.md`. Maßgeblich: `CLAUDE.md` → „Offene Punkte".

Vorherige Session 58 (05.09.2026): kommunikative Datenpunkte an Baugruppen +
Kommunikationsbauteil-Ratchet; Belimo Energy Valve, 22 Wärme-/Kälte-/Wasserzähler,
2 Wilo-CIF-Module, Schneider CRAH, 3 Elektro-Energiezähler, 3 Automation-UMG-
Türeinbau; `tuer`-Zone-an-Baugruppen-Bugfix in `getTuerItems()`.

> **Diese Datei ist NICHT mehr die maßgebliche laufende Doku.** Seit ~Session 30
> wird der Projektfortschritt vollständig in **`CLAUDE.md`** geführt
> (Abschnitt „Offene Punkte" + die je Themenblock komprimierten Session-
> Zusammenfassungen), ausführliche Session-Protokolle liegen in
> `docs/archiv/claude-md-modul4-sessions-*.md`. Maßgeblich für den echten
> Projektstand ist immer der letzte Commit + `CLAUDE.md`. Der Body unten
> (Modul 1–3, Datenbanken, gesperrte Entscheidungen) ist weiterhin als
> Referenz für die abgeschlossenen Module 1–3 gültig, der Abschnitt
> „Offene Punkte" darin ist überholt.

**Pausiert – Fortsetzung nächste Sitzung ("wir machen morgen weiter").**
Alle Session-58-Arbeiten implementiert, in `ga_komponenten.xlsx` eingetragen,
als JSON exportiert (baugruppen 96 · einzelbauteile 147 · feldgeraete 52) und
im Browser verifiziert. Keine bekannten offenen Bugs. Nächster Schritt und
Restlisten (Preisrecherche, fehlende Feldgeräte-Katalogzeilen) siehe
`CLAUDE.md` → „Offene Punkte (Stand Session 58)".

**Meilenstein:** Git-Tag `meilenstein-2026-07-04-modul4-design` (Sessions 22–24) + Git-Tag `meilenstein-2026-07-05-modul4-abgeschlossen` (Sessions 25–26, Modul 4 Design/Darstellung fertig, vor Beginn der Bauteile/Funktionsgruppen-Integration) – je vollständiges Backup (ZIP, Git-Bundle, Claude-Gedächtnis) unter `C:\Users\SMI\Backups\dbacs\`.

**Hinweis Deployment (Session 24+26):** GitHub-Pages-Deploy ist nun dreimal im „deploy"-Job fehlgeschlagen (Commits `0bef940`, `4f93b7b` in Session 24, `6a62c2e` in Session 26 – Build jeweils erfolgreich, nur der Pages-Deploy-Schritt). Session 26: Nutzer hat den Job manuell über GitHub Actions neu gestartet; `Last-Modified`-Header der Live-Seite bestätigte vor dem Neustart den veralteten Stand (04.07., Session 25). Bei erneutem Auftreten den Workflow (`.github/workflows/*.yml`) selbst prüfen statt weiter als reine Instabilität zu werten.

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
│   ├── modul-03-architektur/index.html     Modul 3 – TE-Berechnung + Zonenaufteilung ✅
│   └── modul-04-innenaufbau/index.html     Modul 4 – Baugruppen · Innenaufbau ✅
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
│   ├── einzelbauteile.json                 Einzelbauteile-DB M4 (35 Einträge, 4 Hersteller) ← Session 20
│   ├── baugruppen.json                     Baugruppen-DB M4 (15 GA-Funktionsgruppen) ← Session 20
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
| Live-URL Modul 4 | https://smicmics.github.io/dbacs/modules/modul-04-innenaufbau/ |
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
7. ~~Modul 4 – Grundstruktur~~ ✅ abgeschlossen Session 20
8. ~~Modul 4 – Physikalische Reihenplatzierung (Klemmraum + Verdrahtungskanal)~~ ✅ abgeschlossen Session 21
9. ~~Modul 4 – Granulare Zonen (8 statt 3), Direktbauteile, Bauteil-Indizierung~~ ✅ abgeschlossen Session 22
9a. ~~Modul 4 – Layout-Neuordnung (Schranksicht dominant, skaliert wie M3, Eingabeleiste + Füllstand-Streifen volle Breite)~~ ✅ abgeschlossen Session 23
9b. ~~Modul 4 – Funktionsbereich-Taxonomie (10 statt 5 Bereiche), Design-Feinschliff~~ ✅ abgeschlossen Session 24
9c. ~~Modul 4 – Bedarfsbasierte Breiten-Umverteilung Klemmleisten (klemm_l/f/s)~~ ✅ abgeschlossen Session 25
9d. ~~Modul 4 – Fortlaufender Verdrahtungskanal je Bauteilreihe (Leistung/Steuerung, über- und nebeneinander)~~ ✅ abgeschlossen Session 26 – Bug: Kanal wurde nur vor der ersten Reihe je Band gesetzt statt vor jeder Reihe; Fix per bandübergreifendem `kanalPending`-Flag. **Nachkorrektur (Session 26, Live-Screenshot des Nutzers):** erster Fix setzte fälschlich zusätzlich einen Kanal vor Reihe 1 (dort existiert bereits eine feste M3-Kanalzone) – `kanalPending` startet jetzt mit `false`, siehe CLAUDE.md
9e. ~~Modul 4 – Zonenbeschriftung: Vordergrund-Ebene + robuster Zeilenumbruch~~ ✅ abgeschlossen Session 26 – Zonentext wurde von Bauteil-Blöcken überdeckt (Zeichenreihenfolge) und lief bei schmalen Zonen (Nebeneinander) rechts aus dem Feld (wortbasierter Umbruch konnte einzelne lange Wörter wie „Steuerbaugr./DDC" nicht brechen). Fix: Beschriftungen werden in `buildSVG()` erst nach Kanälen/Bauteilen gezeichnet (eigene Vordergrund-Ebene, simuliert über Zeichenreihenfolge, plus heller Textumriss), `wrapSVGText()` bricht zusätzlich hart um, siehe CLAUDE.md
9f. ~~Modul 4 – Zonen-Legende + sichtbare Bauteil-Nummerierung~~ ✅ abgeschlossen Session 26 – Legende (`ZONE_LABELS`/neue `ZONE_COLORS`-Konstante, `buildLegend()`) unter der Schranksicht erklärt die 8 Zonenfarben; Bauteil-Blöcke zeigen jetzt zusätzlich zur Kurzbezeichnung ihre Positionsnummer (`#idx`, dreistufig je nach Platzangebot), sodass sich Stückliste (`#3–#5, #7`) und Schrankbild direkt abgleichen lassen. Nummerierung bleibt bewusst pro Zone (keine Änderung an Platzierung/Stückliste). Kein neues Druck-Layout nötig – Stückliste druckt bereits vollständig mit, siehe CLAUDE.md
9g. ~~Zonenfarben-Konsolidierung + Korrektur (Modul 4 → Modul 3)~~ ✅ abgeschlossen Session 26 – `ZONE_COLORS`-Konstante jetzt einzige Quelle in beiden Modulen (vorher Hex-Werte mehrfach dupliziert). Einspeisung/ÜSS waren identisch, Sensoren-Klemme zu gelblich – jetzt klar unterscheidbar (Sensoren: Magenta; Einspeisung: blasses Gelb; ÜSS: kräftiges Gelb – Zuordnung nach Nutzer-Feedback innerhalb der Session einmal getauscht, finaler Stand siehe CLAUDE.md). Modul 4: Zonentext im Schrankbild nur auf dem Bildschirm ausgeblendet (Legende übernimmt das), im Ausdruck weiterhin sichtbar (reine CSS-Lösung); dynamisch erzeugte Verdrahtungskanäle jetzt optisch wie die statischen Modul-3-Kanäle (grau, ohne "Kanal"-Text). Modul 3: nur Farbwerte angeglichen, keine Legende/Textausblendung (dort nicht erforderlich). **Nachtrag:** Zonennamen im Füllstand-Streifen (Modul 4) waren fest verdrahtet und liefen von `ZONE_COLORS` auseinander – `buildFuellstand()` färbt die Labels jetzt ebenfalls dynamisch ein, siehe CLAUDE.md
9h. ~~Modul 4 – Höhenprüfung Hutschienen-Zonen + Beschriftung schmaler Bauteile~~ ✅ abgeschlossen Session 26 – Bug 1: `placeInKlemmRow()` (6 Hutschienen-Zonen inkl. Energieverteilung ohne Schienensystem) prüfte nur Breite, nie Höhe; ein NH00-Lasttrennschalter (für Schienensystem gedacht) wurde dadurch fälschlich in der kompakten Zone "platziert" statt als Overflow erkannt. Fix: Höhenprüfung `d.h_mm <= band.h_mm` ergänzt, zu hohe Bauteile werden übersprungen (Overflow), Warteschlange läuft weiter. Schienensystem-Kennzeichnung einzelner Katalogeinträge bewusst in die nächste Sitzung verschoben. Bug 2: schmale Bauteile hatten keine Rückfallebene mehr für die Positionsnummer – neue Funktion `idxLabelSVG()` dreht die Nummer bei Bedarf um 90° (erste SVG-Textrotation im Projekt); Klemmen-Zeilen zeigen jetzt nur noch Anfang/Ende eines zusammenhängenden Bauteil-Laufs (`markFirstLastOfRun()`), keine Einzelbeschriftung mehr je Klemme. Siehe CLAUDE.md
9i. **Modul 4 – Idee 2 (zurückgestellt): Höhen-Umverteilung Leistung/Steuerung** mit verschiebendem
    Kabelkanal, analog zur Klemmleisten-Umverteilung. Energieverteilung bleibt fix. Braucht eigene
    Abstimmung: Mindesthöhe `h_leist ≥ h_klemm`, separater Rechenweg „Nebeneinander" (Breite) vs.
    „Übereinander" (Höhe).
9j. ~~Modul 4 – Bauteil-Datenbasis über Excel-Pipeline nachgezogen~~ ✅ abgeschlossen Session 27 – `einzelbauteile.json`/`baugruppen.json` liefen als einzige DBs bisher nicht über Excel; jetzt neue Sheets `einzelbauteile`/`baugruppen`/`baugruppen_bauteile` (Verknüpfungstabelle). Schema erweitert: `b_mm` (reale Breite) jetzt Hauptfeld statt `te_breite` (wird abgeleitet), `datenpunkt_typ`/`-anzahl`/`klemmen_zusatz` (Datenfelder für spätere DDC-Kapazitätslogik, noch unausgewertet), `funktionsbereiche`/`automationsfunktionen`/`geprueft` bei Baugruppen. 18 neue Katalogeinträge recherchiert (Klemmen Phoenix/Wago mit Querschnittsbereich, ÜSS-Vorsicherung D03/100A statt NH00, Dehn-Feinschutz, Siemens-Steuertrafos mit Spannungsangabe, Desigo PXC100-D, Metz Connect KRS-E06/KMA-F8 als LVB-Nachfolger des alten BTR-Relais). Dabei Bug gefunden+gefixt: `buildStueckliste()`/`exportCSV()` stürzten bei fehlendem `preis_eur` ab (neue unbepreiste Einträge) – zeigen jetzt „–". Siehe CLAUDE.md für Details.
9k. ~~Modul 4 – Klemmen-Herstellerbereinigung auf Phoenix Contact~~ ✅ abgeschlossen Session 27b – Nutzer hat alle bisherigen Klemmen-Zeilen (gemischte Hersteller) selbst in Excel gelöscht und Phoenix Contact als alleiniges Planungsfabrikat festgelegt: UT-Reihe (Schraubanschluss, 5 Größen × 5 Farben inkl. eigener `-PE`-Schutzleitervariante) für Einspeisung, PT-Reihe (Push-in, 5 Größen × 3 Farben, gleicher Typ für alle drei Abgangsklemmen-Zonen) + Messertrennklemme PT 2,5-MT für Feldgeräte/Sensoren – 41 neue Katalogzeilen. Bestehende Baugruppen-Referenzen auf die gelöschten Weidmüller-Artikel (19 Zeilen in `baugruppen_bauteile`) wurden auf die neuen Phoenix-Äquivalente ungemappt, damit keine Baugruppe unbemerkt ein Bauteil verliert. Siehe CLAUDE.md für Details.
9l. ~~Modul 4 – Nutzer-Gegenprüfung Klemmen + `geprueft`-Feld für einzelbauteile~~ ✅ abgeschlossen Session 27c – Nutzer hat die 41 Klemmen gegen die Phoenix-Contact-Seite geprüft: Farbcode-Suffix fehlte in der Typbezeichnung (korrigiert), mehrere Höhen waren falsch (vermutlich Höhe/Tiefe vertauscht, korrigiert). Neue Spalte `geprueft` (Boolean) im `einzelbauteile`-Sheet ergänzt (analog zu `baugruppen`), da der Nutzer mangels Tag von Hand Zellen grün eingefärbt hatte – das wäre beim nächsten Excel-Export verloren gegangen. Siehe CLAUDE.md.
10. **Modul 4 – Grundlagenarbeit Bauteildaten/Baugruppen:** ⏳ Session 27
    begonnen – 18 neue Einzelbauteile recherchiert + über die Excel-Pipeline
    eingepflegt (siehe 9j/15). **Noch offen:** vier Einträge mit unverifizierten
    Abmessungen final klären (Schirmklemme, Moxa-Switch, Wachendorff-Gateway,
    alte Steuertrafo-Variante); Maße/Zonen der ursprünglichen 44 Bauteile
    gegenprüfen; Baugruppen für die neuen Funktionsbereiche
    `schaltschrank`/`automation`/`netzwerk`/`kaelte`/`nutzungsspezifisch`
    anlegen (aktuell leer) – noch nicht begonnen.
12. **Modul 4 – Typische Installationsaufbauten in Baugruppen berücksichtigen:**
    MSS und zugehöriger Schütz werden üblicherweise untereinander montiert (kurze Kabelwege).
    Konzept: Baugruppen-Definition steuert Anordnung (z. B. Feld „anordnung: untereinander|nebeneinander"),
    oder Geräteklassen mit Affinität zueinander werden beim Platzieren gruppiert.
    → Abstimmung mit Nutzer vor Implementierung erforderlich.
13. **Modul 4 – DDC-Modul-Packlogik:** Hersteller/Serie final festlegen, dann Belegung bis zur
    Datenpunkte-Kapazitätsgrenze eines Moduls (inkl. Kunden-Reserve), erst danach neues Modul setzen –
    inkl. Auswirkung auf Anzahl Abgangsklemmen. Aktuell: 1 Baugruppe = 1 eigenes DDC-Modul (kein Teilen).
14. Modul 4 – Erweiterungen: Drag&Drop-Repositionierung, Integritätsprüfung Baugruppen-Instanz, Mehrfeld-Schränke, Bauteil-Icons, GAEB/AVA-Export
15. ~~Modul 4 – Datenbank: Bauteile + Baugruppen über Excel pflegen (xlsx_to_json.py erweitern)~~ ✅ abgeschlossen Session 27 – neue Sheets `einzelbauteile`/`baugruppen`/`baugruppen_bauteile`, siehe CLAUDE.md
16. Modul 5 – Klemmenzone h_klemm (Anzahl Klemmen je Gruppe)

**Später**
17. Außendurchmesser NYM-J mit echten Herstellerdaten verifizieren
18. Startseite: Screenshot-Vorschau je Modul ergänzen
17. Neue Modul-4-Katalogeinträge (DDC-Module, Lasttrennschalter, ÜSS-Geräte) sind Best-effort-Platzhalter – reale Herstellerdatenblätter (Maße, Bestellnummern) noch zu verifizieren

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
