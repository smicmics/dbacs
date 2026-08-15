# Archiv: Modul 4/5 – Session 52 (voller Sitzungsverlauf)

Diese Datei enthält den vollständigen, unkomprimierten Sitzungsverlauf von
Session 52 (Lüftungssensoren, Pflichtzubehör-Mechanismus,
Sicherheitsketten-Koppelrelais, Steuerspannungs-Automatik, geteilter
Sicherheitstrafo, diverse Klemmzonen-/Namens-/Artikel-Referenz-Korrekturen).

Die daraus destillierten, dauerhaft gültigen Regeln stehen kompakt in
`CLAUDE.md` unter „## Baugruppen-Modellierungsregeln (verbindlich)". Dieses
Archiv dient nur als Nachschlagewerk für Nutzer-Funde, Root-Cause-Analysen,
verworfene Zwischenstände und Verifizierungsdetails – für die tägliche
Arbeit reicht die kompakte Regel-Fassung in `CLAUDE.md`.

---

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

**Nachtrag (Session 52 Nachtrag 6, siehe unten): 24V AC als gleichwertige
Alternative bestätigt** – beide Spulenspannungsvarianten (230V AC/24V AC)
laufen über einen Sicherheitstrafo, daher kein Unterschied in der
Ausfallsicherheit zwischen ihnen; 230V AC bleibt Standard, weil dabei
längere Kabelstrecken bis zur Anlage zulässig sind als bei 24V AC. Siehe
kompakte Regel in `CLAUDE.md` (Baugruppen-Modellierungsregeln, Punkt 6).

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
(Inzwischen erledigt, siehe Nachtrag 4 unten.)

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
fehlte bei allen 3 Kanalsensoren). Nachgezogen für die älteren
Raumsensor-Baugruppen (Session 51: Raum-CO2/-VOC/-Feuchte-/Kombisensor)
Spannung UND Messbereich (Nutzer-Fund „Messbereich fehlt auch bei
Raumsensoren", per Originaldatenblatt gegengeprüft statt geschätzt):
„Raumtemperatursensor passiv 0...50°C", „Raum-CO2-Sensor 0...2000ppm, 24V
AC/DC", „Raum-VOC-Sensor 0...100% VOC, 24V AC/DC" (Messbereich laut
CE1N1961de tatsächlich 0...100% VOC, kein ppm-Wert), „Raumfeuchtesensor
0...100% r.F., 24V AC/DC", „Raumtemperatur- und Feuchtesensor 0...50°C/
0...100% r.F., 24V AC/DC" (Temperaturbereich = Werkeinstellung R2 der
QPA/QFA-Familie, 3 Bereiche per Steckbrücke wählbar – nicht
QFA2060-spezifisch gegengeprüft, sondern aus dem baugleichen
Schaltungsprinzip der QPA-Family übernommen), „Tauchtemperatursensor
100mm/150mm mit Tauchhülse G1/2" -30...+130°C" (Messbereich laut
Siemens-Originaldatenblatt CE1N1781en: „-30...+130°C other types" – gilt
für LG-Ni1000, nicht NTC).

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
  (Auch das wurde später noch revidiert, siehe Nachtrag 6 unten.)

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
Katalogartikel nutzen. (Das wurde in Nachtrag 6 unten bewusst wieder
aufgehoben – ein gemeinsamer Trafo für CPU+Sensoren, siehe dort.)

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
