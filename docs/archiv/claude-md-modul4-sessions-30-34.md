# CLAUDE.md-Archiv: Modul 4 – Belegungshistorie, Zonenfilter, Zentrierung, Sessions 30–34

Ausgelagert aus `CLAUDE.md` am 07.08.2026, um das Hauptdokument schlank zu halten (Kontextfenster-Auslastung).
Vollständiger, unveränderter Original-Wortlaut der damaligen "Gesperrte Entscheidungen"-Abschnitte.
Der aktuell gültige, komprimierte Funktionsstand steht weiterhin in `CLAUDE.md` unter
"Modul 4 – Belegungshistorie, Zonenfilter, Zentrierung (Sessions 30–34, komprimiert)".

---

### Modul 4 – pausiert vor Modul 7: offene Punkte Bauteil-Positionierung (Session 34, notiert – keine Entscheidung, kein Code)
Nutzer pausiert Modul 4 nach den erfolgreichen Einzelbauteil-Platzierungstests
(Sessions 29–33), um mit Modul 7 (Stammdatenpflege Artikeldaten) zu beginnen.
Vor der Pause explizit benannte, noch offene Positionierungs-Themen für
Modul 4 – bewusst nur dokumentiert, nicht entschieden oder umgesetzt:
1. **Abstandslogik zu allen Seiten nach Herstellerangabe** (z. B. Schütze,
   Leistungsschalter, alle wärmeerzeugenden Bauteile). Deckt sich mit dem
   bereits in Session 28g als Folgephase notierten "Abstands-/
   Positionierungs-Datenschema (Herstellervorgaben oben/unten/links/rechts,
   Wärmeabfuhr)". Aktuell kennt DBACS je Katalogeintrag nur `h_mm`/`b_mm`/
   `te_breite`, keine gerichteten Mindestabstände zu Nachbarbauteilen.
2. **Positionierungslogik für hintereinander zu positionierende Bauteile**
   (z. B. DDC-Module). Neuer Punkt, noch nicht im Detail spezifiziert –
   Verhältnis zur bestehenden Reihen-Logik (`placeInBands()`/
   `assignDevicesToRows()`, Session 28g) muss noch geklärt werden.
3. **Positionierungslogik für die Anordnung von Bauteilen innerhalb einer
   Baugruppe** (z. B. Motorschutzschalter über Schütz). Deckt sich mit dem
   bereits im Memory festgehaltenen Punkt "Baugruppen-'neue Reihe'-
   Generalisierung" (05.08.2026), dem `zeilenumbruch_davor`-Datenfeld aus
   Session 28c und dem ursprünglichen Backlog-Punkt 12 aus
   `docs/revison_session.md`. Nutzer-Einschätzung vom 05.08.: das aktuelle
   Zwei-Cursor-Platzierungsmodell stößt hier an seine Grenzen – eine
   gezielte Bauteil-Auswahl für Reihen-/Positionswechsel wäre nötig, statt
   eines globalen Flags pro Artikel.
4. **Bedarfsbasierte Breiten-/Höhen-Umverteilung auch für Leistung und
   Steuerung.** Existiert bereits für die drei Klemmleisten-Zonen
   (`redistributeKlemmBands()`, Session 25: `klemm_l`/`klemm_f`/`klemm_s`
   teilen sich eine feste Gesamtbreite, jede Zone wächst nach TE-Bedarf,
   Rest proportional verteilt) – fehlt für `leist`/`steuer` noch. Deckt sich
   mit der bereits in Session 25 als "Idee 2" zurückgestellten Idee (dort
   als Höhen-Umverteilung mit wanderndem Kabelkanal skizziert, Energie-
   verteilung bleibt fix). Nachträglich vom Nutzer ergänzt (Session 34,
   nachdem der Sicherungspunkt schon gesetzt war) – braucht eigene
   Abstimmung: Mindesthöhe `h_leist ≥ h_klemm`, separater Rechenweg
   Nebeneinander (Breite) vs. Übereinander (Höhe), Verhältnis zum
   `placeInBands()`-Kanal/Klemmraum-Modell (anders als das reine
   Breiten-Modell der Klemmleisten).

Alle vier Punkte bleiben zurückgestellt, bis Modul 7 eine saubere
Datengrundlage geschaffen hat. Sicherungspunkt für diese Pause: Git-Tag
`meilenstein-2026-08-06-modul4-pause-vor-modul7` (siehe Memory für Details
zum Backup).

### Modul 4 – Zonen-Filter über den Füllstand-Streifen statt eigener Buttons (Session 33, gesperrt)
Nutzer-Vorschlag direkt nach Session 32: die separaten `.zone-tab`-Buttons
sind redundant, da der Füllstand-Streifen die 8 Zonen (inkl. Farbe/Kurzlabel)
ohnehin schon anzeigt. Besser: die bestehenden `.fs-mini`-Felder selbst
klickbar machen und nur ein zusätzliches "Alle"-Feld (ohne Prozentangabe,
Standard) ans Ende stellen – spart die zweite UI-Ebene komplett.
- **Ablösung, nicht Ergänzung:** `.zone-tabs`/`.zone-tab`-CSS, das
  `#einzel-zone-tabs`-Element und `buildEinzelZoneTabs()` aus Session 32
  sind vollständig entfernt (kein toter Code). `einzelZoneFilter` (globaler
  State) und der Filter in `populateEinzelAuswahl()` (`e.zone ===
  einzelZoneFilter`) bleiben unverändert – nur die Bedienoberfläche wurde
  getauscht.
- **Umsetzung:** jedes der 8 `.fs-mini`-Felder bekommt `data-zone="…"` +
  `onclick="setEinzelZone('…')"`. Ein 9. Feld `#fs-alle-mini`
  (`.fs-mini.fs-mini-alle`, `data-zone="alle"`, initial `class="active"`)
  ohne Balken/Prozentanzeige steht am Ende der Zonenliste, vor dem
  Kanal-Info-Text (`.fs-kanal-mini`, der ohnehin per `margin-left:auto`
  ganz rechts bleibt, unabhängig von der DOM-Position). `setEinzelZone()`
  toggelt jetzt `.active` auf `.fs-mini[data-zone]` statt auf `.zone-tab`.
  CSS: `.fs-mini{cursor:pointer;padding:3px 6px;margin:-3px -6px}` (Klick-
  fläche vergrößert, visueller Fußabdruck durch das negative Margin
  unverändert) + `.active{background:var(--bg4);border-color:var(--blue)}`.
- **Kompatibilität mit `buildFuellstand()` geprüft:** die Funktion setzt bei
  jedem `calculate()` nur `.title`/`.style.color`/Balkenbreite, fasst
  `classList` nicht an – der Zonen-Filter-Zustand bleibt über beliebig viele
  Neuberechnungen hinweg stabil (verifiziert: Klick auf `Kl. Leist.` →
  `calculate()` erneut ausgeführt → Feld weiterhin aktiv, Tooltip trotzdem
  korrekt aktualisiert).
- Verifiziert im Browser: Default „Alle" aktiv (56 Einträge), Klick auf
  „Steuerung" filtert auf 7 Treffer und aktiviert/deaktiviert die Felder
  korrekt gegenseitig, Klick zurück auf „Alle" stellt 56 wieder her; kein
  Layout-Überlauf im Streifen (10 Elemente inkl. Kanal-Info, Streifenhöhe
  unverändert ~40px).

### Modul 4 – Zonen-Filter für Einzelbauteil-Auswahl (Session 32, gesperrt – Bedienoberfläche in Session 33 abgelöst, Filterlogik selbst unverändert)
Nutzer-Feedback: das Dropdown "Spezifische Auswahl Einzelbauteile" zeigte
immer alle ~56 Katalogeinträge ungefiltert (nur nach `kategorie` in
Optgroups sortiert) – bei wachsendem Katalog unübersichtlich. Zusätzlich
auffällig: Klemmen lassen sich als Direktbauteil nur in ihre Katalog-Zone
setzen (z. B. PT-Klemmen alle `zone:"klemm_l""), nicht in `klemm_f`/`klemm_s`,
obwohl es dieselbe physische Klemme ist.
- **Begriffsklärung (wichtig):** "Funktionsbereich" ist im UI bereits die
  Bezeichnung der 10 Baugruppen-Tabs (`gewerk` aus `baugruppen.json`,
  Session 24). Die vom Nutzer gemeinten "Sensorbereich"/"Feldgerätebereich"/
  "Leistung" sind die 8 physikalischen Platzierungszonen aus
  `ZONE_LABELS`/`ZONE_COLORS` (identisch zur Legende, Session 26). Neue
  Filter-Ebene bewusst als "Zone" benannt (`.zone-tab`, eigene CSS-Klasse),
  um nicht mit den bestehenden Funktionsbereich-Tabs zu kollidieren.
- **Umsetzung (nur Teil 1 des Nutzervorschlags – Filter, kein Zonen-
  Override):** `buildEinzelZoneTabs()` rendert 9 Buttons ("Alle" +
  `ALLE_ZONEN`, Farbpunkt + Kurzlabel identisch zum Füllstand-Streifen: z. B.
  "Kl. Feld.", "Kl. Sens.") in `#einzel-zone-tabs`, oberhalb des
  `einzel_auswahl`-Dropdowns in der 320px-Spalte. `setEinzelZone(zone)`
  setzt `einzelZoneFilter` (globaler State, Default `'alle'`) und ruft
  `populateEinzelAuswahl()` neu auf. `populateEinzelAuswahl()` filtert
  `EINZELBAUTEILE_DB` zusätzlich auf `e.zone === einzelZoneFilter` (bei
  `'alle'` keine Einschränkung), Kategorie-Optgroups wie bisher. Aktuelle
  Auswahl bleibt beim Zonenwechsel erhalten, wenn der Artikel im neuen
  Filter noch vorkommt, sonst wird zurückgesetzt.
- **Bewusst NICHT umgesetzt (Teil 2, vom Nutzer explizit auf später
  vertagt):** eine Klemme (oder ein anderes Bauteil) manuell in eine andere
  als ihre Katalog-Zone setzen. Das erfordert ein neues Datenbankfeld (z. B.
  welche Zonen ein Artikel zusätzlich zulässt) und soll im Rahmen von
  Modul 7 (Stammdatenpflege Artikeldaten, siehe Memory) sauber mitgeplant
  werden statt jetzt als Übergangslösung.
- Verifiziert im Browser: 9 Tabs gerendert, Filter auf `klemm_s` liefert
  korrekt 0 Treffer (kein Katalogeintrag hat aktuell diese Zone als
  Default – bestätigt exakt das vom Nutzer beschriebene Problem), Filter auf
  `steuer` liefert 7 Treffer, `alle` wieder 56; keine Layout-Überläufe
  innerhalb der 320px-Spalte (Buttons brechen sauber um); Auswahl bleibt
  über einen Zonenwechsel hinweg erhalten, wenn der Artikel weiterhin im
  gefilterten Ergebnis ist, sonst korrekt zurückgesetzt.

### Modul 4 – Vertikale Zentrierung in Leist./Steuer./Evert-Reihen (Session 31, gesperrt)
Nutzer-Fund per Screenshot beim Testen: in Klemmenzeilen (`placeInKlemmRow()`)
werden Bauteile bereits vertikal zentriert dargestellt, in Leistung/Steuerung/
Energieverteilung-mit-Schiene (`placeInBands()`, mode `row`) dagegen bisher
immer bündig nach dem oberen Klemmraum ausgerichtet. Bei mehreren Geräten
unterschiedlicher Höhe in derselben Reihe (Reihenhöhe = höchstes Gerät +
2×Klemmraum) saßen niedrigere Geräte dadurch sichtbar "zu hoch" statt an der
gemeinsamen Hutschienen-Mitte. Nutzerfrage: ist mittige Platzierung wegen der
Klemmraum-Definition komplex? Antwort: nein – reine Formel-Anpassung.
- **Fix in `buildSVG()`:** `by0` für `row.mode !== 'klemm'` zentriert jetzt
  ebenfalls: `row.y_mm + row.klemmraum + (row.h_mm - 2*row.klemmraum -
  blk.h_mm)/2` statt `row.y_mm + row.klemmraum`. Alle Geräte einer Reihe
  teilen sich dadurch dieselbe vertikale Mitte (= angenommene
  Hutschienen-Position in der Zeilenmitte), unabhängig von ihrer
  individuellen Höhe.
- **Rein visuell, kein Effekt auf Platzbedarf/Platzierungslogik:**
  `h_row = h_dev + 2×Klemmraum` (Session 21) bleibt unverändert – nur WO
  innerhalb dieses bereits reservierten Raums das Gerät gezeichnet wird,
  ändert sich. `placeInBands()`/`assignDevicesToRows()` unangetastet.
- Verifiziert im Browser: zwei Geräte unterschiedlicher Höhe (90 mm und
  130 mm) in derselben Steuerung-Reihe – berechnete Blockmitten stimmen
  exakt überein (beide bei der halben Reihenhöhe), im gerenderten SVG
  bestätigt (Rundungsdifferenz < 0,1 px durch `toFixed(1)`).
- **Offen:** echte Hutschienen-Befestigungspunkte sind nicht bei jedem
  Bauteil exakt die geometrische Mitte (kann herstellerabhängig variieren) –
  DBACS modelliert aktuell keinen expliziten Rail-Attachment-Offset pro
  Katalogeintrag, geometrische Mitte ist eine bewusste Vereinfachung.

### Modul 4 – Belegungs-Historie als LIFO-Stapel (`batches`-Modell, Session 30, gesperrt)
Löst den in Session 29 unvollständig behobenen Bug endgültig: der Nutzer stellte
fest, dass Minus weiterhin nicht zuverlässig "das zuletzt platzierte Modul"
entfernte, sondern je nach Reihenfolge der Hinzufüge-Aktionen (normal/"neue
Reihe") das falsche entfernen konnte.
- **Ursache (grundsätzlich):** `menge` + `forcedMenge` sind nur zwei
  Summen-Zähler ohne Zeitachse. Damit lässt sich nicht rekonstruieren, ob
  zuletzt eine normale oder eine erzwungene Menge hinzugefügt wurde, sobald
  beide Aktionstypen abwechselnd vorkommen (z. B. normal→erzwungen→normal).
- **Fix – neues Feld `batches`:** ersetzt `forcedMenge` durch einen
  chronologischen Stapel `[{n, forced}, ...]` (ältester Eintrag zuerst) je
  Belegungseintrag. `addEinzelbauteil()` hängt bei jedem Hinzufügen einen
  neuen Batch an (`pushBatch()` – verschmilzt mit dem letzten Batch, wenn
  dieser denselben `forced`-Status hat, sonst neuer Eintrag).
  `removeEinzelbauteilQty()` entfernt jetzt echtes LIFO: reduziert immer erst
  den LETZTEN Batch, springt bei Erschöpfung zum davorliegenden – unabhängig
  vom `forced`-Status. `item.menge` wird danach als Summe aller
  `batch.n`-Werte neu berechnet (keine Drift möglich).
- **`getBatches(item)`** migriert alte Einträge (ohne `batches`, nur
  `forcedMenge` aus Session 28i oder `rowBreak`-Boolean aus Session 28g/28h)
  transparent beim ersten Zugriff – exakt wie schon die bestehende
  `consolidateBelegung()`-Selbstheilung, nur eine Modellgeneration weiter.
- **`consolidateBelegung()`** verkettet beim Zusammenführen mehrerer
  Einträge desselben Artikels deren Batches in `belegung`-Reihenfolge
  (chronologisch korrekt, da neue Einträge immer ans Ende von `belegung`
  gepusht werden) statt nur die `forcedMenge`-Zahlen zu addieren.
- **`placeBauteile()`-Queue-Aufbau unverändert in der Logik** (erst alle
  normalen, dann alle erzwungenen Einheiten einer Zone/eines Artikels als
  ein Block, siehe Session 28i) – berechnet die dafür nötige
  Gesamtsumme der erzwungenen Einheiten jetzt aber aus
  `getBatches(item).filter(b=>b.forced)` statt aus dem entfernten
  `forcedMenge`-Zähler. Kein Effekt auf `placeInBands()`/
  `assignDevicesToRows()` (Session 28g) selbst.
- Verifiziert direkt gegen die produktiven Funktionen im Browser, zwei
  Szenarien: (1) erzwungen(3)→normal(5), dann "−2" → entfernt korrekt vom
  normalen (zuletzt hinzugefügten) Anteil, `batches` danach
  `[{n:3,forced:true},{n:3,forced:false}]` – der zuvor fehlerhafte Fall aus
  Session 29 ist jetzt korrekt. (2) normal(2)→erzwungen(3)→normal(4), dann
  "−5" → verbraucht den letzten Batch (4 normal) vollständig und danach 1
  aus dem davorliegenden erzwungenen Batch, Ergebnis
  `[{n:2,forced:false},{n:2,forced:true}]` – LIFO über mehrere Batches
  hinweg bestätigt. End-to-End über `calculate()` fehlerfrei, Stückliste
  und Belegungsliste zeigen konsistente Mengen, keine Konsolenfehler.

