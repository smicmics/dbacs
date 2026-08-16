# Archiv: Modul 4/5 – Sessions 53–54 (voller Sitzungsverlauf)

Diese Datei enthält den vollständigen, unkomprimierten Sitzungsverlauf von
Session 53 (Kanal-CO2/VOC-Fühler, Luftstromwächter, Baugruppen-Dropdown
nach Kategorie) und Session 54 (weitere Lüftungswächter/-sensoren,
Heizung/Kälte/Sanitär-Sensorik, PE-Klemmen-Regel, Schaltschrank-USV).
Kompakte Ergebnis-Zusammenfassung siehe `CLAUDE.md`.

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

