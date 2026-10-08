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

> **Nachtrag Session 70 Teil 9 (08.10.2026) – Breite Verifikation des neuen
> `zone_modus` „einsp_leist_misch" (Teil 8) gegen den gesamten Katalog,
> Nutzer-Auftrag: „Nutze die bereits vereinbarten Testroutinen... rechner-
> gestützte Tests statt Handkontrolle":**
> Neue Hilfsfunktion `testBaugruppeUnterModus(bgId, modus, menge)`
> (Browser-Konsole, analog `testBaugruppe()`, aber mit erzwungenem
> `m03_zone_modus` statt dem festen `1feld`-Referenzaufbau) – **alle 215
> Baugruppen einzeln (Menge 1) unter `einsp_leist_misch` getestet: 0
> Fehler** (kein `fehlendPlatziert`, kein `overflow`). Zusätzlich 2
> Stresstests mit hoher Menge zur gezielten Prüfung der Mehrfeld-Kaskade:
> 300× `430_000056` (BSK) → Feldfolge **F,G,G,E,E** (2× zusätzliches
> Leistungsfeld, 2× zusätzliches Steuerungsfeld, unabhängig voneinander
> demand-getrieben), 500× `480_000001` (Automations-Reserve) → **F,G,E** –
> beide 0 Fehler. Bestätigt: die in Teil 8 nur mit einem Baugruppentyp
> (50× BSK) verifizierte Feldtyp-Logik hält auch katalogweit und über
> mehrstufige Überlauf-Kaskaden. Zusätzlich optische Kontrolle (Browser-
> Screenshot, 50×-BSK-Testfall): Feld 1 (Typ F) zeigt Einspeiseklemmen-
> Header, große + kleine Leistungszone, Abgangsklemmen unten; Feld 2 (Typ
> E) zeigt Steuerbaugruppe (CPU+TX-I/O-Module) + Energieverteilung; direkte
> DOM-Abfrage bestätigt `letzteFelder[0].zones` exakt `{leist,klemm_e,uss,
> klemm_l,klemm_f,evert}` und `letzteFelder[1].zones` exakt `{steuer,
> klemm_f,klemm_s,evert}` – deckungsgleich mit `FELDTYP_ZONEN.F`/`.E`,
> Legende/Farben korrekt, keine Überlappungen. Vollständiger
> Standard-Regressionstest (fester `1feld`-Referenzaufbau, unabhängig vom
> neuen Modus) erneut bestanden: `testKatalogScan()` 0 verwaist,
> `testBaugruppe()` 215/215, `testAnlage()` 31/31, keine Konsolenfehler.

> **Nachtrag Session 70 Teil 8 (07.10.2026) – Neuer `zone_modus`
> „Einspeisung+Leistung gemischt, Steuerung getrennt" (Modul 3 + Modul 4),
> Nutzer-Vorgabe – fehlende Feldaufteilungs-Variante ergänzt:**
> Spiegelbild zum bestehenden `einsp_misch` (dort: Einspeisung getrennt,
> Leistung+Steuerung gemischt). Neuer Wert `einsp_leist_misch` im
> `#zone_modus`-Dropdown (Modul 3). 2 neue Feldtypen (identisch in beiden
> Modulen dupliziert, wie der gesamte FELDTYP-Mechanismus):
> - **F** (Erstfeld, `repeat:false` wie C – nur eine Netzeinspeisung):
>   `['klemm_e','uss','evert','leist','leist_ext','klemm_l','klemm_f']` –
>   Einspeisung UND Leistung in einem Feld, OHNE `steuer`/`klemm_s`.
> - **G** (Folge-Leistungsfeld bei Überlauf, `repeat:true`, ohne
>   Einspeisung): `['evert','leist','leist_ext','klemm_l','klemm_f']`.
> - `FELDPLAN.einsp_leist_misch = [{ft:'F',repeat:false},{ft:'G',repeat:true},
>   {ft:'E',repeat:true}]` – Feld 2 nutzt das bereits bestehende Typ E
>   (Steuerung, aus `getrennt_els`) unverändert wieder; weitere Leistungs-
>   (G) bzw. Steuerungsfelder (E) entstehen demand-getrieben über den
>   bereits bestehenden Mehrphasen-Mechanismus in `calculateFelder()` –
>   keine Änderung an der Kernlogik nötig.
> - `FELDTYP_GROW_TARGET.F = FELDTYP_GROW_TARGET.G = 'leist'`: entfällt die
>   komplette Steuer-Zeile (+ der dann unnötige Zonentrennkanal `kanal_ls`,
>   von `kanalNochNoetig()` automatisch erkannt, da `steuer` nicht mehr im
>   Feldtyp vorkommt), wächst die GROSSE Leistungszone (`leist_ext`)
>   automatisch um deren Höhe – exakt die Nutzer-Vorgabe "aus Leistung UND
>   Steuerung UND dem kleinen Leistungsfeld wird ein großes Leistungsfeld
>   UND das kleine Leistungsfeld [bleibt unverändert]". Die kleine, mit ÜSS
>   geteilte Leistungszeile (`leist`, fest auf `h_klemm`) bleibt unberührt.
>   Klemmzeile: `klemm_s` entfällt, seine Breite verteilt sich proportional
>   auf `klemm_l`+`klemm_f` (Nutzer-Begründung: "Rückmeldeleitungen auf
>   Leistungsbauteile wie Relais") – alles über den bereits bestehenden,
>   vollständig generischen `buildLayoutForFeldtyp()`-Transformationsmechanismus
>   (Session 48), ohne jede Änderung an dessen Kernlogik – nur Daten-
>   deklarationen (Zonenmengen, Wachstumsziel, Label, Feldplan) ergänzt.
> **Browser-Verifikation:** 50×-BSK-Testfall (Standschrank 699×1545mm,
> Reserve 0%, Doppelstock, neuer Modus) – Feld 1 (Typ F) nimmt jetzt
> **alle 50 Instanzen auf einmal** auf (`leist` 1070mm Gesamthöhe statt
> 515mm, `klemm_f` 260/260mm = 100%, kein Overflow), Feld 2 (Typ E) enthält
> CPU/TX-I/O-Module (`steuer` 519mm belegt) – Steuerspannungs-Trafo bleibt
> bewusst in Feld 1 bei den anderen 24V-AC-Verbrauchern (Typ E hat gar
> keine `leist`-Zone, ein Trafo kann dort strukturell nie stehen – entspricht
> der bereits etablierten Cross-Field-Verdrahtung wie bei `getrennt_els`).
> Vollständiger Katalog-Regressionstest (bestehender, von diesem neuen Modus
> unabhängiger Referenzschrank-Testaufbau): `testKatalogScan()` 0 verwaist,
> `testBaugruppe()` 215/215 bestanden, `testAnlage()` 31/31 bestanden, keine
> Konsolenfehler.

> **Nachtrag Session 70 Teil 7 (07.10.2026) – Letzte Hutschienenreihe einer
> Zone braucht keinen eigenen Verdrahtungskanal mehr, wenn direkt im
> Anschluss bereits ein Zonentrennkanal existiert (Nutzer-Fund per
> Screenshot: DDC-Modulreihe in `steuer` passte optisch noch – Rest nach 3
> TXM-Reihen 135mm, eine 4. Reihe braucht nur 118mm Gerätehöhe –, scheiterte
> aber an den zusätzlichen 40mm des vorangestellten Verdrahtungskanals,
> obwohl direkt im Anschluss an die Zone ohnehin schon der Zonentrennkanal
> zu `leist` (`kanal_ls`) folgt):**
> **Fix:** `getZoneBands()` markiert jedes Band jetzt mit
> `followedByKanal` – true, wenn direkt NACH der zugehörigen Layout-Zeile
> (aus `buildLayoutForFeldtyp()`) bereits eine reine Struktur-Kanalzeile
> folgt (z. B. `kanal_ls`). `placeInBands()` bekommt einen neuen
> Fallback-Zweig: passt die aktuelle Reihe OHNE ihren eigenen 40mm-
> Verdrahtungskanal in den Rest des Bandes UND ist das Band als
> `followedByKanal` markiert, wird sie ohne vorangestellten Kanal platziert
> – der bereits vorhandene Zonentrennkanal übernimmt die Zugänglichkeit für
> diese letzte Reihe. Greift NUR für die tatsächlich letzte, grenzende
> Reihe (durch die Bedingung selbst sichergestellt: die normale Prüfung mit
> Kanal ist vorher bereits gescheitert, sonst würde der normale Zweig
> greifen) – alle vorherigen Reihen bleiben unverändert mit regulärem
> Zwischenraum-Kanal.
> **Browser-Verifikation:** isolierter Funktionstest von `placeInBands()`
> (synthetisches Band, 28 Geräte à 7 je Reihe, 135mm Rest nach 3 Reihen) –
> MIT `followedByKanal:true` passen alle 4 Reihen (0 Overflow, 4. Reihe
> ohne Zwischen-Kanal direkt an Reihe 3 anschließend); MIT
> `followedByKanal:false` (Regressions-Gegenprobe) bleibt die 4. Reihe
> korrekt unplatziert (Overflow, wie vor dem Fix) – Flag greift also
> gezielt nur im vorgesehenen Fall. Vollständiger Katalog-
> Regressionstest: `testKatalogScan()` 0 verwaist, `testBaugruppe()`
> 215/215 bestanden, `testAnlage()` 31/31 bestanden, keine Konsolenfehler.

> **Nachtrag Session 70 Teil 6 (07.10.2026) – Teil-5-Ansatz korrigiert:
> nur die TATSÄCHLICH grenzüberschreitende Hutschienenreihe wird schmaler,
> nicht mehr die ganze Zone (Nutzer-Fund per Screenshot: "Alle Hutschienen
> wurden nach rechts versetzt bis zum Beginn der kleinen Leistungszone...
> zu viel Platz verschenkt"):**
> Teil 5 hatte `getZoneBands()` lückenlos übereinanderliegende Bänder
> DERSELBEN Zone (z.B. `leist_ext` + die mit ÜSS geteilte `leist`-Zeile)
> PAUSCHAL zu einem einzigen, auf die schmalere Schnittmengenbreite
> verengten Band zusammengelegt – das machte zwar mehr Kapazität nutzbar
> (18→24 Instanzen am 50×-BSK-Testfall), rückte aber JEDE Hutschienenreihe
> der Zone auf die schmalere Breite ein, auch die, die nie in den
> schmaleren Bereich hineinragen (sichtbar im Schrankbild: alle Reihen
> bündig auf Höhe des ÜSS-Zeilenanfangs, obwohl der größte Teil der Zone
> deutlich breiter ist) – unnötig verschenkter Platz, vom Nutzer per
> Screenshot direkt erkannt.
> **Korrigierter Ansatz** (Nutzer-Vorgabe: "die Platzierung... geht immer so
> wie bisher und bis es nicht mehr passt. bevor der nächste Schaltschrank
> erstellt wird erfolgt eine Prüfung ob noch eine Zone anschließt. wenn ja,
> wird am Anfang nur dieser Zone die Hutschiene gesetzt"): `getZoneBands()`
> gibt die Bänder wieder UNVERÄNDERT/getrennt zurück (kein Vor-Zusammenlegen
> mehr, `mergeContiguousBands()` entfernt). Stattdessen direkt in
> `placeInBands()`: jede Reihe wird zuerst normal gegen das AKTUELLE Band mit
> dessen EIGENER (oft breiterer) Breite geprüft – passt sie dort, bleibt
> alles wie bisher, keine Einengung. Passt sie NICHT mehr allein in den Rest
> des aktuellen Bandes, wird NUR FÜR DIESE EINE REIHE geprüft, ob das
> nächste Band lückenlos anschließt (`bandsContiguous()`) und der
> KOMBINIERTE Rest (aktuelles Restband + volles nächstes Band) reicht – wenn
> ja, bekommt NUR diese eine, grenzüberschreitende Reihe die schmalere
> Schnittmengenbreite (`intersectBandW()`, inkl. Sicherheitsprüfung, dass die
> tatsächliche Geräte-TE-Zahl der Reihe dort überhaupt noch passt), alle
> bereits platzierten UND alle nachfolgenden Reihen behalten die volle,
> eigene Breite ihres jeweiligen Bandes.
> **Browser-Verifikation:** 50×-BSK-Testfall (Standschrank 699×1545mm,
> Reserve 0%, Doppelstock, `zone_modus='je_feld'`) – Feld 1 nimmt jetzt
> **28 statt 24 (Teil 5) bzw. 18 (vor jeder Korrektur) Instanzen** auf
> (`leist` 87% belegt) – BESSER als der verworfene Teil-5-Ansatz, weil Reihe
> 1+2 (138mm/115mm hoch) weiterhin die volle 619mm-Breite nutzen (24/34
> Geräte je Reihe statt künstlich auf 28 TE begrenzt) und nur Reihe 3
> (115mm) auf die schmalere 511mm-Schnittmenge eingeht – per
> `letzteFelder[0].zones.leist.rows` direkt nachgewiesen: Reihe 1/2
> `x_mm:40, w_mm:619` (unverändert voll), Reihe 3 `x_mm:148, w_mm:511`
> (nur diese schmaler). Vollständiger Katalog-Regressionstest:
> `testKatalogScan()` 0 verwaist, `testBaugruppe()` 215/215 bestanden,
> `testAnlage()` 31/31 bestanden, keine Konsolenfehler.

> **Nachtrag Session 70 Teil 5 (07.10.2026, ÜBERHOLT – siehe Teil 6 oben) –
> Lückenlos übereinanderliegende
> Bänder derselben Zone werden jetzt zusammengelegt statt Restkapazität zu
> verschenken (Nutzer-Fund beim Nachfragen zur BSK-Feldaufteilung: "die
> kleine Leistungszone über der Klemmreihe... wäre zusammen mit der großen
> in der Lage, weitere BSK-Gruppen aufzunehmen. Es passiert aber nicht,
> weil die große Zone allein ausschlaggebend ist"):**
> **Root Cause:** `buildLayout()` erzeugt für die `leist`-Zone bei
> `ke_pos='unten'` zwei direkt aufeinanderfolgende Zeilen OHNE Kanal
> dazwischen: `leist_ext` (Hauptteil der berechneten Höhe, volle
> Innenbreite) und die mit ÜSS geteilte `leist`-Zeile (fest auf
> `h_klemm`=95mm, schmaler, da ÜSS links Platz beansprucht). `getZoneBands()`
> gab daraus bisher 2 völlig unabhängige Bänder an `placeInBands()` weiter –
> reichte eine neue Hutschienenreihe weder in den Rest des einen NOCH in das
> andere Band allein, wurde sie verworfen, obwohl beide Restflächen
> ZUSAMMEN genug Höhe geboten hätten (am 50×-BSK-Testfall: 127mm Rest im
> großen Band + 95mm im kleinen Band = 222mm, eine weitere Reihe hätte nur
> 155mm gebraucht).
> **Fix:** neue Funktion `mergeContiguousBands()` (`modules/modul-04-
> innenaufbau/index.html`) legt in `getZoneBands()` lückenlos
> übereinanderliegende Bänder DERSELBEN Zone zu einem zusammen – Breite ist
> dabei der ÜBERSCHNEIDUNGSBEREICH (x-Intersection) beider Bänder (ein
> durchgehender Gerätestapel darf nur die Breite nutzen, die über die
> GESAMTE kombinierte Höhe sicher frei ist, z.B. nicht in den Bereich
> hineinragen, den im schmaleren Band eine Nachbarzone wie ÜSS belegt – die
> breitere Zeile verschenkt dadurch etwas Randbreite, bleibt aber garantiert
> kollisionsfrei). Nur angewendet auf Zonen, die tatsächlich über
> `placeInBands()` (Reihen-/Kanal-Modell) laufen: `leist`/`steuer` immer,
> `evert` nur ohne Schienensystem – `klemm_e/uss/klemm_l/klemm_f/klemm_s`
> sowie `evert` MIT Schienensystem nutzen `placeInKlemmRow()`, dort ist
> jedes Band eine eigenständige Hutschienenreihe und darf nicht verschmolzen
> werden. Löst nebenbei die seit Session 48 bekannte Einschränkung
> "TE-Passt-Prüfung nutzt nur die Breite des ERSTEN Bandes" sauber auf, da
> `bands[0]` nach dem Zusammenlegen bereits die schmalste sicher nutzbare
> Breite trägt.
> **Browser-Verifikation:** 50×-BSK-Testfall (Reserve 0%, Doppelstock,
> Standschrank 699×1699mm) – Feld 1 nimmt jetzt **24 statt 18 Instanzen**
> auf (`leist`-Füllstand 57%→87%), Feld 2 entsprechend weniger (26 statt
> 32) – die zuvor gestrandete Kapazität wird jetzt genutzt. Vollständiger
> Katalog-Regressionstest: `testKatalogScan()` 0 verwaist, `testBaugruppe()`
> 215/215 bestanden, `testAnlage()` 31/31 bestanden, keine Konsolenfehler.

> **Nachtrag Session 70 Teil 4 (07.10.2026) – Doppelstock-PE-Klemme
> `3210596` ergänzt, löst die offene Mischmontage-Frage aus Teil 1/Phase F
> dieser Sitzung:** Nutzer wusste nicht, ob eine Doppelstockklemme
> (`3210567`) direkt neben einer Standard-PE-Klemme (`3209536`) montiert
> werden darf (abweichende Bauhöhe, Hersteller-Recherche fand keine
> explizite Freigabe/Ablehnung für Mischmontage) – Vorgabe: wenn nicht
> eindeutig bestätigt, müsste Leistung (`klemm_l`) für Doppelstock gesperrt
> werden. Alternative (vom Nutzer gewählt): **Phoenix Contact PTTB 2,5-PE
> (`3210596`)** als eigene PE-Variante der PTTB-2,5-Doppelstock-Baureihe neu
> katalogisiert – dimensionsgleich zu `3210567` (b_mm/h_mm identisch), löst
> die Mischmontage-Frage auf, da L/N UND PE bei aktiver Doppelstock-Option
> jetzt beide innerhalb derselben Baureihe/Bauhöhe bleiben, keine
> Standardklemme mehr danebensteht. `3209536.doppelstock_variante_
> artikel_nr` auf `3210596` gesetzt (vorher nicht vorhanden – PE blieb bei
> Doppelstock bisher IMMER unpaarig, siehe Session 70 Teil 2). **Kein
> Herstellerlistenpreis gefunden**, als offener Punkt im `quelle_hinweis`
> vermerkt. Export einzelbauteile 225→**226**. Backup:
> `ga_komponenten_vor-doppelstock-pe_20261007_212448.xlsx`.
> **Browser-Verifikation:** 50× `430_000056` (BSK, L/N/PE-Motoranschluss)
> – Doppelstock/DS-Trenn liefern jetzt korrekt **25× `3210596`** (vorher
> 50× `3209536` unpaarig), Standard/Trenn weiterhin unverändert 50×
> `3209536`; vollständiger Katalog-Regressionstest danach erneut
> durchlaufen: `testKatalogScan()` 0 verwaist, `testBaugruppe()` 215/215
> bestanden, `testAnlage()` 31/31 bestanden, keine Konsolenfehler.

> **Nachtrag Session 70 Teil 3 (07.10.2026) – Steuerspannungs-Trafo+LSS
> landete im falschen Feld, obwohl die CPU/DDC daneben im richtigen Feld
> saß (Nutzer-Fund: „Energieverteilung und Trafos... gehören in Feld 1").
> Reproduziert am 50×-BSK-Testfall (Reserve 0%, Doppelstock, Standschrank
> 699×1745, `zone_modus='je_feld'`): Feld 1 hatte `evert` komplett leer
> (0/300mm) und `steuer` zu 100% mit der CPU belegt, während die
> automatisch ergänzte Steuerspannungs-Baugruppe (Trafo in `leist` + LSS in
> `evert`) komplett in Feld 2 landete – obwohl Feld 2 gar keine CPU
> enthielt, die sie hätte versorgen müssen.
> **Root Cause:** die Steuerspannungs-Baugruppe läuft (anders als die
> CPU/TXM-Module, die direkt in `queues.steuer` geschrieben werden und
> dadurch zuverlässig als Erstes in Feld 1 landen) über `bgInstanceQueue`
> und wurde dort bisher ganz ANS ENDE angehängt (`push()`, nach allen
> Baugruppen aus der Belegung). `platziereBaugruppenFuerFeld()` versucht
> pro Feld JEDE Instanz in `bgInstanceQueue`-Reihenfolge – reserviert also
> zuerst für die 50 BSK-Instanzen Platz in `leist` (Koppelrelais), und erst
> danach für die Steuerspannungs-Instanz. Baugruppen-Zusammenhalt (Session
> 49) ist atomar: `evert` (LSS) UND `leist` (Trafo) müssen GEMEINSAM in
> einem Feld passen. War `leist` in Feld 1 durch die zuerst bedienten
> BSK-Instanzen bereits so voll, dass die 2 Trafo-Geräte nicht mehr
> hineinpassten, scheiterte die GESAMTE Instanz dort – auch der
> `evert`-Teil (LSS), obwohl `evert` in Feld 1 noch komplett leer war – und
> rutschte komplett ins nächste Feld, wo wieder frischer `leist`-Platz war.
> **Fix:** die Steuerspannungs-Instanz wird jetzt per `unshift()` statt
> `push()` an den ANFANG von `bgInstanceQueue` gestellt (`buildQueues()`,
> `modules/modul-04-innenaufbau/index.html`) – sie bekommt dadurch als
> Erste Gelegenheit, sich in Feld 1 (wo auch die CPU sitzt) einzureservieren,
> bevor andere Baugruppen `leist`/`evert` dort vollpacken. Die übrigen
> Baugruppen packen sich danach um die bereits reservierten Trafo/LSS-
> Geräte herum – minimal weniger Restkapazität in Feld 1 für sie, aber
> korrekt co-lokalisiert mit der CPU, die sie versorgt.
> **Browser-Verifikation:** derselbe 50×-BSK-Testfall zeigt jetzt Feld 1
> `evert` 161/300mm (4× LSS) + `leist` inkl. beider Trafos (`4AM4042-
> 5AN00-0EA0`/`-5AT10-0FA0`) neben der CPU (`steuer` weiterhin 479mm/100%),
> Feld 2 `evert` korrekt 0/300mm (leer) und `leist` nur noch die
> Koppelrelais – `overflow:[]` in beiden Feldern. Vollständiger Katalog-
> Regressionstest nach dem Fix: `testKatalogScan()` 0 verwaist,
> `testBaugruppe()` 215/215 bestanden, `testAnlage()` 31/31 bestanden
> (inkl. aller Wärmepumpen-Anlagen mit bis zu 136 Options-Kombinationen),
> keine Konsolenfehler.

> **Nachtrag Session 70 Teil 2 (07.10.2026) – Klemmleisten-Umverteilung
> + 2 echte Doppelstock-Bugs gefunden+behoben, ausgiebig katalogweit
> getestet. Auslöser: Nutzer-Test mit 50× Brandschutzklappenantrieb
> (`430_000056`) zeigte `klemm_f`/`klemm_l` als limitierenden Faktor,
> obwohl `leist`/`steuer`/`evert` noch viel Platz hatten:**
> 1. **`redistributeKlemmBands()` korrigiert** (`modules/modul-04-
>    innenaufbau/index.html`): verteilte den knappen Überschuss bisher
>    proportional zum absoluten mm-**Defizit** jeder Klemmleisten-Zone
>    (`klemm_l`/`klemm_f`/`klemm_s`) – bei Zonen, die von DENSELBEN
>    Baugruppen-Instanzen gespeist werden (gekoppelter Bedarf, z. B. 4×
>    `klemm_f`- + 3× `klemm_l`-Klemmen je BSK-Antrieb), bevorzugte das
>    systematisch die Zone mit dem größeren Defizit und ließ die
>    gekoppelte Partnerzone mit Breite zurück, die mangels passender
>    Instanzen nie gefüllt werden konnte (Baugruppen-Zusammenhalt).
>    Neue Logik verteilt im Shortfall-Fall den **gesamten** Pool der
>    Defizit-Zonen proportional zum tatsächlichen **Bedarf** (`demandMM`),
>    mit Sicherung, dass keine Zone unter ihren rohen (reserve-freien)
>    Platzbedarf gedrückt wird (Katastrophenfall-Fallback ohne
>    Untergrenze, falls selbst die rohen Bedarfe nicht in den Pool
>    passen). Ergebnis am Testfall (1099×1745-Standschrank, 20% Reserve):
>    vorher 20 von 50 BSK-Instanzen passten ins erste Feld, danach 28 –
>    `klemm_f`/`klemm_l` werden jetzt gleichzeitig limitierend statt
>    einer die andere auszubremsen.
> 2. **Doppelstock-Bug #1 – `resolveBaugruppenBauteile()`:** die
>    ursprüngliche Logik ging von GENAU 2 gleichartigen Zeilen (1
>    Signal+Referenz-Paar) je Baugruppe aus und verwarf bei einem
>    dritten/vierten Vorkommen (`seen[key]`) einfach ALLES weitere – bei
>    `430_000056` mit 4 `klemm_f`-Zeilen (2 getrennte Meldungen: Endlage
>    Auf + Endlage Zu, an unterschiedlichen Stellen der Klappe) gingen so
>    3 von 4 Klemmen verloren (Stückliste zeigte nur 25 statt 200 nötige
>    `klemm_f`-Positionen für 50 Instanzen). Betraf jede Baugruppe mit
>    mehr als einem Signal+Referenz-Paar im selben Zone/Artikel, nicht
>    nur BSK. Fix: PAARWEISE statt „erstes gewinnt" – 1./2. Vorkommen = 1.
>    Doppelstockklemme, 3./4. Vorkommen = eine WEITERE eigene
>    Doppelstockklemme usw.
> 3. **Doppelstock-Bug #2 – äußere Instanzen-Paarung in `buildQueues()`
>    UND `aggregateStueckliste()`:** beide behandelten im Doppelstock-
>    Modus pauschal die GANZE Baugruppe als paarbar (`sub===0`-Platzier-
>    Logik bzw. `Math.ceil(item.menge/2)` auf ALLE Bauteile) – Artikel
>    OHNE eigene Doppelstock-Variante (z. B. Schutzleiterklemme
>    `3209536`, die laut Katalog keine `doppelstock_variante_artikel_nr`
>    hat – Nutzer-Nachfrage „gibt's eine Kombiklemme für L/N/PE?"
>    bestätigt: nein, nur Einzelklemmen je Leiter) wurden dadurch
>    FÄLSCHLICH halbiert, bei `leist`-Zone-Bauteilen (Koppelrelais
>    `2967099`/`2967073`, gar keine Klemmen) wäre das sogar in der
>    Stückliste falsch gewesen. Fix: neues Flag `bt._dsPairable` (von
>    `resolveBaugruppenBauteile()` gesetzt, true nur wenn der Artikel
>    tatsächlich eine Doppelstock-Variante hat) – Instanzen-Paarung
>    (`geraetPlatzieren`/`geraeteAnzahl`) greift jetzt bauteilweise statt
>    baugruppenweit.
> **Referenz-Fakt (Nutzer-Nachfrage, in Code-Kommentar übernommen):**
> eine Doppelstockklemme hat 2 Ebenen zu je 2 Anschlüssen = 4 Adern
> gesamt = Platz für 2 vollständige Signal+Referenz-Paare.
> **Browser-Verifikation:** 50× `430_000056` über alle 4 Klemmenvarianten
> (Standard/Doppelstock/Trennklemme/DS-Trennklemme) getestet – `leist`
> (Koppelrelais) bei JEDER Variante unverändert 100/50/1/1 in der
> Stückliste; `klemm_f`/`klemm_l` bei Standard/Trenn identisch
> (200/100+50 Klemmen, nur anderer Artikel bei Trenn); bei Doppelstock/
> DS-Trenn korrekt 50/(25+50) – PE bleibt unpaarig bei 50, L/N korrekt
> gepaart bei 25 –, dabei passen jetzt ALLE 50 Instanzen ohne Overflow in
> 1 Feld. Regressionstest klassischer 2-Zeilen-Fall (`480_000001`
> Binäreingang, menge 10/11): Doppelstock liefert weiterhin exakt 5 bzw.
> 6 Klemmen (ungerade Anzahl: letzte halbgenutzt), BI-Zählung unverändert
> – kein Verhaltensunterschied zum Stand vor dem Fix. **Vollständiger
> Katalog-Regressionstest** (Standard-Klemmenvariante, da nur die
> betrifft alle bestehenden Anlagen standardmäßig): `testKatalogScan()`
> 0 verwaist, `testBaugruppe()` 215/215 bestanden, `testAnlage()` 31/31
> bestanden (inkl. aller 8 neuen Wärmepumpen-Anlagen mit bis zu 136
> Options-Kombinationen), keine Konsolenfehler.
> **Noch offen (zurückgestellt, Nutzer-Vorgabe „das muss ich probieren,
> bevor wir die Architektur der Klemmen anpacken"):** die grundsätzliche
> Frage, ob `klemm_f`/`klemm_l`/`klemm_s` bei Bedarf mehrreihig werden
> sollen (zusätzliche Hutschienenreihen aus freier `leist`/`steuer`-Höhe
> ziehen) – mit den jetzt behobenen Bugs kann der Nutzer Doppelstock-
> klemmen zunächst gezielt manuell einsetzen, wo er Engpässe bemerkt,
> statt die Architektur zu erweitern.

> **Nachtrag Session 70 (07.10.2026) – Wärmepumpen/Kältemaschinen bis
> 250 kW: Fork-Recherche (5 Forks: Viessmann/Buderus/Carrier/Skadec+
> Mitsubishi/generische Normen+Sensorik) + 8 neue Anlagen „Wärmepumpe bis
> 250 kW" fertig umgesetzt. Volle Herleitung in
> `scratchpad/waermepumpen_datenpunkte_synthese.md` +
> `scratchpad/waermepumpen_anlagen_freigabe_vorlage.md`, hier nur
> Kurzfassung:**
> 1. **Recherche-Ergebnis (Kernbefund):** keiner der 4 geprüften Hersteller
>    (Viessmann Vitocal, Buderus Logatherm, Carrier AquaSnap/30RQM/30WG,
>    „Scadec" = SKADEC SH-Baureihe) veröffentlicht eine vollständige Modbus-
>    Registerliste – alle verweisen auf eine projekt-/anfragespezifische
>    Datenpunktliste. Nur Mitsubishi Electric liefert über das generische
>    BEMS-Interface **MELCOBEMS MINI (A1M+)** eine öffentlich belegte
>    Komplettliste (4 schreibende + 7 lesende Punkte, ca. 11 gesamt).
>    Physische Klemmen sind bei Viessmann/Buderus/Carrier dagegen gut aus
>    Original-Planungsunterlagen belegt. **AMEV „Technisches Monitoring
>    2020"** (frei verfügbar) liefert eine echte offizielle GLT-Prüfgrößen-
>    tabelle für Wärmepumpen ≥50 kWth (keine eigene Tabelle für
>    Kälteanlagen) – VDMA 24247 ist dagegen **keine** GLT-Punkteliste,
>    sondern reine Energieeffizienz-Kennzahlen-Normenreihe (Vorab-Annahme
>    der Aufgabenstellung korrigiert).
> 2. **Physische + kommunikative Datenpunktliste final vom Nutzer
>    vorgegeben** (nicht aus der Recherche übernommen): physisch immer
>    AI VL-/RL-Temperatur sekundärseitig (Tauchfühler passiv, nutzt
>    bestehende Baugruppe `430_000006`), BI Betriebsmeldung, BI
>    Sammelstörmeldung, BO Freigabe/Sperre, BO Umschalten Heizen/Kühlen (nur
>    reversibel), AO Sollwertvorgabe 0…10V, AO Sollwertverstellung/
>    Leistungsbegrenzung – alle potentialfrei auf `klemm_f` (Regel 1).
>    Kommunikativ (Modbus RTU, auf der Buskabel-Klemmenzeile): Hochdruck-/
>    Niederdruckwächter, Abtaubetrieb (L-W)/Frostschutzwächter Sole (W-W),
>    Außentemperatur (**immer, auch Wasser-Wasser** – dient der Heizkurve
>    der internen Regelung, Nutzer-Bestätigung), VL-/RL-Temperatur intern,
>    aktueller Sollwert, elektrische Leistung, Volumenstrom, Wärmeleistung,
>    bei reversiblen Anlagen zusätzlich Kälteleistung, je nach Pumpenkonzept
>    zusätzlich Pumpe sekundär Betrieb/Störung (nur „interne Pumpe") bzw.
>    Pumpe primär Betrieb/Störung (**nur Wasser-Wasser, immer** – Nutzer-
>    Korrektur: „Quellenpumpe" und „Primärpumpe" sind dasselbe Bauteil,
>    keine 2 Pumpen auf der Primärseite).
> 3. **Nutzer-Korrektur Klemmenbedarf:** eine Modbus-RTU-Anbindung braucht
>    trotz „kein Schaltschrankplatz für die Datenpunkte selbst" mindestens
>    **2 zusätzliche `klemm_f`-Klemmen** für das RS485-Buskabel (A/B) – als
>    generischer, herstellerübergreifender Default angenommen (Modbus TCP
>    würde stattdessen den bestehenden Kommunikationsbauteil-Ratchet
>    nutzen, hier nicht gewählt).
> 4. **8 neue Anlagen** `420_A00018`–`420_A00025` (Kategorie „Waermepumpen",
>    `funktionsbereich` `heizung_anlagen` bzw. zusätzlich `kaelte_anlagen`
>    bei reversiblen Varianten) + **8 neue DDC-Kern-Baugruppen**
>    `420_000057`–`420_000064` (eine je Kombination Typ×Reversibel×
>    Pumpenkonzept) + **2 neue Feldgeräte-Platzhalter** `WP-LW-250`/
>    `WP-WW-250` (generisch, herstellerübergreifend – Nutzer-bestätigt
>    ausreichend für Platz-/Stücklistenbestimmung, kein Stromlaufplan-
>    Anspruch). Jede Anlage bündelt: 2× Tauchfühler `430_000006` (VL+RL),
>    1× DDC-Kern-Baugruppe, bei externer Sekundärpumpe zusätzlich Pflicht-
>    Dropdown `gruppe:'pumpenleistung'` (mittel=`420_000023` Stratos MAXO/
>    Default, groß=`420_000025` Stratos GIGA2.0 – beide bereits „inkl.
>    Rep.-Schalter", kein Zusatzbauteil nötig), sowie 2 optionale Dropdowns
>    (`gruppe_optional`, volle Auswahl statt Ohne/Ja-Schalter, Nutzer-
>    Vorgabe „nimm das Dropdown-Feld"): „Externer Wärmemengenzähler"
>    (nicht-reversibel: 8 Varianten `420_000029`–`036`; reversibel:
>    zusätzlich 8 Kälte-Pendants `420_000037`–`044`) und „Externer
>    Elektroenergiezähler" (3 Varianten `440_000001`–`003`).
> 5. **Namensregel angewendet:** jeder Anlagen-Name lässt „Wärmepumpe" +
>    grobe Ausstattung erkennen (z. B. „Wasser-Wasser-Waermepumpe
>    reversibel Heizen/Kuehlen, externe Sekundaerpumpe (Pumpengroesse
>    mittel/gross waehlbar)"), keine abgekürzten Jargon-Labels.
> **Export:** baugruppen 207→**215**, feldgeraete 109→**111**, anlagen
> 23→**31**, einzelbauteile unverändert 225 (keine neuen Schrankbauteile,
> nur Referenzen auf bereits vorhandene Klemmen/Baugruppen). Backup:
> `ga_komponenten_vor-waermepumpen-anlagen_20261007_135611.xlsx`.
> **Browser-Verifikation:** alle 8 Anlagen per `testAnlage()` über JEDE
> Kombination der Optionsfelder getestet (36–136 Kombinationen je Anlage,
> abhängig von reversibel/nicht) – durchgängig `pass:true`, 0 `overflow`,
> 0 `fehlendPlatziert`, 0 verwaiste Referenzen; `testKatalogScan()`
> katalogweit ebenfalls 0 Treffer. Live-Test der komplexesten Variante
> (`420_A00025`, Wasser-Wasser reversibel extern, Standschrank 1200×2000)
> bestätigt Statistik exakt wie von Hand berechnet (physisch 2 AI/3 AO/5
> BI/3 BO = 13 gesamt; kommunikativ 7 AI M-Bus + 8 AI/5 BI Modbus RTU + 17
> AI Modbus TCP = 37 gesamt), keine Konsolenfehler.
> **Nächster Schritt:** Kesselkreis (Fork 2 „Heizung erzeugerseitig")
> sowie Kälte-/Lüftungs-Anlagen (Fork 4/5) weiterhin offen (siehe Session-
> 69-Nachtrag unten). Offene Punkte aus der Wärmepumpen-Recherche selbst:
> keine öffentliche Modbus-Registerliste bei Viessmann/Buderus/Carrier/
> Skadec (nur auf Anfrage erhältlich); keine eigene AMEV-Prüfumfangstabelle
> für Kältemaschinen (nur Wärmepumpe) – falls eine reine „Kältemaschine
> bis 250kW"-Anlage ohne Wärmepumpenfunktion künftig gebraucht wird, siehe
> `scratchpad/waermepumpen_datenpunkte_synthese.md` Abschnitt 3 für ASHRAE-
> Guideline-13-Alternative.

> **Nachtrag Session 69 (06.10.2026) – „Heizkreise Verteilung" fertig +
> erweitert auf Wärmeübertrager/Wärmeerzeuger, neue Testroutine in Modul 4,
> 2 echte Bugs gefunden+behoben. Volle Herleitung in Memory
> `project_anlagenbaugruppen.md` Abschnitt 6–10 + Abschnitt „SITZUNGSENDE
> Session 69", hier nur die Kurzfassung:**
> 1. **9 Anlagen „Heizkreise Verteilung"** fertiggestellt (`420_A00001`–
>    `009`): Heizkreis Beimischschaltung / Zubringerkreis, ungeregelt /
>    Fußbodenheizkreis-Zubringer zum Verteiler je klein (Wilo PICO)/mittel
>    (MAXO)/groß (GIGA2.0) + Regelkreis Fußbodenheizungsverteiler (je
>    Raumkreis, Oventrop Kleinventilantrieb). VL/RL-Fühler-Lücke bei allen
>    nachträglich geschlossen (Zubringerkreis hatte zunächst gar keinen
>    Fühler, Annahme „WMZ liefert die Werte mit" galt nur für den
>    WMZ-gewählten Fall).
> 2. **Neue generische `gruppe_optional`-Mechanik** (Excel-Spalte in
>    `anlagen_baugruppen`, Export in `xlsx_to_json.py`, UI-Logik in
>    `updateAnlageVariantenUI()`/`modul-04-innenaufbau/index.html`): ein
>    `gruppe`-Dropdown kann jetzt zusätzlich eine „Ohne"-Option anbieten
>    (leerer Wert, matcht keine `bg_id`, `addAnlage()` brauchte dafür keine
>    Änderung). Reduziert eine sonst kombinatorisch explodierende
>    Anlagenzahl (36→9 bei den Heizkreisen) auf echte Dropdown-Auswahl
>    (Busanbindung Modbus RTU/Ethernet, Wärmemengenzähler) statt
>    Dutzender Einzel-Anlagen. Wiederverwendbar für künftige Anlagen.
> 3. **12 weitere Anlagen** in neuen Kategorien: „Heizungsverteiler-/
>    Sammler" (2: vollständig mit Druck+Nachspeisung / Basis nur
>    Temperatur), „Wärmeübertrager" (3: Geregelter Wärmetauscher,
>    Hydraulische Weiche – nur die 4 Messstellen, Weiche selbst bleibt
>    Fremdbauteil Regel 7 –, Pufferspeicher mit 3 Speichersensoren),
>    „Wärmeerzeuger" (1: Fernwärmeübergabestation, Regelventil zwingend
>    Federrücklauf stromlos zu statt einfachem Ventil). Je 1 zusätzliche
>    Pumpen-Variante für Wärmetauscher UND Fernwärmeübergabe (neue Gruppe
>    `pumpenleistung`, Pflichtfeld klein/mittel/groß, `menge:2` derselben
>    Pumpen-Baugruppe für primär+sekundär symmetrisch) + optionaler WMZ.
>    Gesamt jetzt **23 Anlagen**.
> 4. **Neue Namensregel** (siehe Memory `feedback_anlagen_namensregel.md`,
>    verbindlich für alle künftigen Anlagen): der `name` muss die fest
>    enthaltene Ausstattung erkennen lassen (z. B. „Heizkreis
>    Beimischschaltung, klein (Pumpe PICO 3...45 W, Regelventil 200N,
>    VL/RL-Temperatur)"), keine reinen Konfigurationsnummern. Rückwirkend
>    auf alle 9 Heizkreis-Anlagen angewendet.
> 5. **Neue Selbsttest-Routine direkt in `modules/modul-04-innenaufbau/
>    index.html`** (Browser-Konsole, siehe Memory
>    `project_dbacs_testroutine.md` für Details): `testBaugruppe(bgId)` /
>    `testAnlage(anlageId)` / `testKatalogScan()` / `testAlles()` – prüfen
>    Platzbedarf (Artikel-für-Artikel je Zone, nicht nur Summen),
>    Katalog-Referenzen (Regel 7), tatsächliche Positionierung im
>    Referenzschrank (`fehlendPlatziert`/Overflow) und Reserve-Konsistenz
>    (Soll-Modulzahl unabhängig aus der Formel gerechnet) – nicht-
>    destruktiv (sichert/stellt Belegung+Zonenwerte automatisch wieder
>    her). Nutzer-Vorgabe: „Die Menge an Bauteilen ist für den Menschen
>    nur aufwändig nachvollziehbar, das geht über den Rechner viel
>    einfacher und schneller." Ersetzt ab sofort die von Hand geschriebene
>    Herleitungstabelle nach jeder Baugruppen-/Anlagen-Neuanlage.
>    **Betriebshinweis:** bei >~20 Anlagen kann ein einzelner
>    `testAlles()`-Aufruf in einen Tool-Timeout laufen – dann
>    `testKatalogScan()`+Baugruppen-Schleife und Anlagen-Schleife in 2
>    getrennten Aufrufen fahren.
> 6. **2 echte Bugs gefunden (durch die neue Testroutine) + behoben:**
>    (a) der Doppeleinspeisung-Dropdown-Filter in `populateAnlagenAuswahl()`
>    blendete bei `m03_doppeleinspeisung='ja'` fälschlich ALLE Anlagen in
>    JEDEM Nicht-Automation-Gewerk aus (nicht nur die eigentlich gemeinten
>    ASP-Doppeleinspeisung-Varianten) – Fix: Filter greift jetzt nur noch
>    in Gewerke-Tabs, die überhaupt eine `doppeleinspeisung_bindung='ja'`-
>    Variante anbieten. (b) `g(id) || 20`-Muster (3 Stellen: `reserve_pct`,
>    `ddc_reserve_pct`, `klemmraum_mm`) behandelte eine bewusst
>    eingegebene **0** wie ein leeres Feld (0 ist falsy in JS) und
>    ersetzte sie fälschlich durch den Default 20 – eine explizit auf 0%
>    gesetzte Reserve wurde also leise mit 20% gerechnet. Fix: neue
>    `gOrDefault(id, def)`-Funktion, die nur bei wirklich leerem Feld
>    (`value===''`) auf den Default zurückfällt.
> 7. **Neuer „↺ Schrank leeren"-Button** direkt neben der „Belegung"-
>    Überschrift in Modul 4 (`resetSchrankKomplett()`) – löscht Belegung
>    UND automatisch ergänzte Module in einem Klick (bisher musste der
>    Nutzer das für Testzwecke manuell wiederholt tun).
> **Vollständig Browser-verifiziert** (Standschrank 1200×2000, Drehstrom/
> Schiene 3-polig/1feld, via `testAlles()`/Einzelaufrufe): 207/207
> Baugruppen, 23/23 Anlagen bestanden, 0 verwaiste Referenzen, keine
> Konsolenfehler. Alles committet + nach GitHub gepusht.
> **Nächster Schritt:** Kesselkreis selbst (Fork 2 „Heizung erzeugerseitig")
> fehlt noch – Weiche/Puffer/Wärmetauscher/Fernwärmeübergabe sind die
> „Erzeugerseite drumherum" bereits fertig. Danach Kälte-Anlagen (Fork 4,
> 7 Kreistypen) und Lüftungs-/RLT-Anlagen (Fork 5, Baukasten-Ansatz) –
> Schritt 1+2 (Recherche) für beide bereits komplett, Schritt 3 noch nicht
> begonnen. Offene Einzelentscheidungen A–E aus Schritt 2 (Chiller-
> Schnittstelle/CRAH-Nachprüfung, Frostthermostat-Rohrmontage, Kondensat-
> wächter ohne Artikel, Condair/Carel-Fabrikatabweichung, 230V/25Nm-
> Klappenantrieb) weiterhin offen.

> **Nachtrag Session 68 (04.10.2026, Fortsetzung 3) – Heizung/Kälte/Lüftung-
> Anlagen: Schritt 1+2 (Fork-Recherche) komplett, Schritt 3 (Zusammensetzen)
> für „Heizkreise Verteilung" begonnen, NOCH KEINE EXCEL-ÄNDERUNG. Volle
> Herleitung in Memory `project_anlagenbaugruppen.md` Abschnitt 5, hier nur
> Kurzfassung + was beim Weiterarbeiten zuerst zu tun ist:**
> 1. **Schritt 1 (5 Forks)** lieferte 18 Anlagen-Vorschläge über 3 Gewerke
>    (Heizung/Kälte/Lüftung) + 11 Katalog-Lücken. Rohdaten:
>    `scratchpad/fork_1..5_*_ergebnis.md`.
> 2. **Nutzer-Entscheidungen zu Schritt 1:** Außentemperaturfühler = 1x pro
>    Schrank, zentral in Heizung+Kälte+Lüftung wählbar, Produkt **Siemens
>    QAC34** (→ echte Bestellnr. `QAC34/101`); zusätzlich Außenfeuchtefühler
>    nur für Kälte+Lüftung; hydraulische Weiche bleibt Fremdbauteil (Regel 7),
>    aber Sensoren an der Weiche sollen **4 Positionen** haben (Primär-/
>    Sekundär-Ein-/Austritt), nicht nur 2; Lüftungs-Baukasten-Ansatz (Fork 5,
>    6 `gruppe`-Achsen) „i.O. für ersten Ansatz"; Leistungsklasse (Pumpen-
>    /Ventilgröße) ist reine `bg_id`-Auswahl ohne DP-Unterschied – NICHT bei
>    Ventilatoren (dort ändert Anlaufart die DP-Zahl).
> 3. **Schritt 2 (3 Forks)** schloss die 11 Lücken größtenteils mit
>    konkreten Produkten: QAC34/101 + QFA3100/AQF3100 (Außensensoren,
>    `scratchpad/fork_schritt2_a_*`), Siemens QBE63-DP1 (Differenzdruck
>    flüssig), ATAGO CM-800α-EG (Glykolsensor), ALRE JTF (Frostthermostat,
>    unbestätigte Rohrmontage), Chiller-Schnittstelle nur 2 Hardwarepunkte
>    sicher frei (Freigabe braucht Koppelrelais nach Regel 15 – **stellt die
>    bestehende CRAH-Baugruppe `430_000026`/`027` infrage, noch nicht
>    gegengeprüft**), Kondensatwächter ohne festen Bestellcode
>    (`scratchpad/fork_schritt2_b_*`); GLB161.1E/GLB361.1E/GBB161.1E
>    (modulierender Klappenantrieb, 230V/25Nm fehlt), Klingenburg KR
>    MicroMax 370 (Rotor-WT-Antrieb), Condair RS (Dampfbefeuchter, Fernmelde-
>    platine optional!), Carel humiFog direct (Sprühbefeuchter)
>    (`scratchpad/fork_schritt2_c_*`).
> 4. **Offene Einzelentscheidungen A–E** (dem Nutzer vorgelegt, noch keine
>    Antwort): A) CRAH-Baugruppe gegen reales Schneider-Datenblatt
>    nachprüfen? B) Frostthermostat trotz unbestätigter Rohrmontage
>    aufnehmen? C) Kondensatwächter trotz fehlendem Artikel aufnehmen/
>    Alternative suchen/zurückstellen? D) Condair RS/Carel-Abweichungen
>    akzeptieren? E) 230V/25Nm-Klappenantrieb weglassen oder bei Belimo
>    suchen?
> 5. **Schritt 3 begonnen für „Heizkreise Verteilung"** (Kategorie-Name):
>    Nutzer-Vorschlag statt Hydraulik-Vorauslegung – Anlagen werden nach
>    **Leistungsbezug** (klein=PICO 420_000022/mittel=MAXO 420_000023) UND
>    **Ausstattungsbezug** (konventionell/mit Busanbindung+Wärmemengenzähler)
>    benannt und als **vollständig eigenständige Anlagen** angelegt (kein
>    `gruppe`-Dropdown mehr nötig). Draft-Matrix (7 Anlagen, NICHT final):
>    Heizkreis Beimischschaltung (klein-konv./mittel-konv./mittel-Bus+WMZ),
>    Zubringerkreis (klein-konv./mittel-Bus+WMZ+Sensoren), Fußbodenheizkreis
>    (klein-konv./mittel-Bus+WMZ, mit Federrückl.-Antrieb 420_000015 + STB
>    420_000011 + TW 420_000010/012). **Bestätigt: bestehende Baugruppen
>    bleiben unverändert, nur neue `anlagen`/`anlagen_baugruppen`-Zeilen.**
> 6. **Nächster Schritt beim Fortsetzen:** offene Frage klären, ob
>    „Bus+WMZ" auch bei „klein" angeboten wird; 3 Arbeitsannahmen bestätigen
>    lassen (siehe Memory-Abschnitt 5 für den genauen Wortlaut: „statische
>    Heizung"=Radiator+nur Beimischschaltung, nur klein+mittel-Leistungs-
>    stufen für Verteilkreise, „TW"=Temperaturwächter) – danach die
>    Heizkreis-Verteilkreis-Anlagen tatsächlich in Excel eintragen. Kessel-
>    kreis/Weiche/Puffer (Fork 2) sowie Kälte-/Lüftungs-Anlagen (Fork 4/5)
>    folgen danach, noch nicht begonnen.

> **Nachtrag Session 68 (04.10.2026, Teil 4) – Phase 5-7 abgeschlossen: alle
> 5 Fork-Blöcke aus Teil 3 in `ga_komponenten.xlsx` eingetragen, exportiert,
> Browser-verifiziert. 23 neue Baugruppen, 4 neue Einzelbauteile, 13 neue
> Feldgeräte. Export: einzelbauteile 221→**225**, baugruppen 184→**207**,
> feldgeraete 96→**109**.**
> 1. **Block 1 – Absperrklappen Heizung/Kälte** `420_000053`–`056` (Siemens
>    Acvatix SAL31.00T10/SAL81.00T10 + Zubehör ASC10.51, `funktionsbereich:
>    [heizung,kaelte]`). Y1/Y2-Fahrbefehle in `klemm_f` (Nutzer-Entscheidung).
>    230V-Variante nutzt 2× Koppelrelais `2967073` mit Override auf der
>    Koppelrelais-Zeile (Regel 12, NICHT wie im ursprünglichen Fork-1-
>    Vorschlag auf einer Klemme).
> 2. **Block 2 – Lüftungsklappen-Antriebe** `430_000045`–`052` (Siemens
>    Acvatix GLB146.1E/GLB346.1E 10Nm + GBB146.1E/GBB346.1E 25Nm, je
>    meldend/schaltend). Gleiche Regel-12-Korrektur wie Block 1 bei den
>    230V-Koppelrelais-Varianten (Fork 2 hatte das bereits richtig
>    vorgeschlagen).
> 3. **Block 3 – Brandschutzklappen konventionell** `430_000053`–`058`
>    (TROX FK2-EU, Z02/Z03/Z43/Z45, Belimo-OEM-Antriebe BFL/BFN) – erste
>    produktive Anwendung der neuen **Regel 17** (Koppelrelais mit
>    durchgeschleifter Steuerspannung, 1 Relais je Endlagenschalter). PE-
>    Klemme bleibt bei den Antrieben Teil der Klemmleiste (Schutzklasse II,
>    Regel 11), nur unbelegt. Entriegelungstaster am Schaltschrank bewusst
>    NICHT modelliert (keine TROX-Antriebsfunktion, eigener Folgeschritt).
> 4. **Block 4 – ASi-Bus-Brandschutzklappen** `430_000059`–`061`, nach
>    Nutzer-Vorgabe als **3 unabhängig wählbare Baugruppen** statt
>    automatischem Ratchet umgesetzt (volle Flexibilität, Nutzer verwaltet
>    die 62-Teilnehmer-Grenze selbst):
>    - `430_000059` „Grundsystem" (einmalig): 1× Controller `TNC-A1412` +
>      2× Netzteil `TNC-A1258` (Doppelmaster-Standard) je mit eigenem
>      LSS+Hilfsschalter-BI (Netzteil hat laut Datenblatt keine eigene
>      Störmeldung – Nutzer-Lösung: Hilfskontakt am ohnehin nötigen
>      vorgeschalteten LSS) + 2 Feldklemmen für den AS-i-Busabgang. 2× BI.
>    - `430_000060` „BMA-Kopplung + Störentriegelung" (optional, einmalig):
>      Meldemodul `TNC-Z0094` + 2 rein kommunikative DP (`KOMM-FB`,
>      `dp_fb_bi:1`+`dp_fb_bo:1`, `modbus_tcp`) – „spielt sich komplett im
>      Schaltschrank ab" (Nutzer-Vorgabe), keine physischen Klemmen.
>    - `430_000061` „BSK hinzufügen" (beliebig oft, menge = Klappenzahl):
>      rein kommunikativer Mehrbedarf, `KOMM-FB` mit `dp_fb_bi:2` je
>      Instanz (Platzhalter-Annahme Auf/Zu analog zur konventionellen
>      Endlagenmeldung, da die exakte TROX-Modbus-Registerbelegung je
>      Klappe nicht öffentlich dokumentiert ist – **offener Punkt**, vor
>      Projekteinsatz mit TROX-Punkteliste abgleichen). Referenziert
>      `A00000018487` (AS-EM-Feldmodul) als Feldgerät.
>    Der bestehende Kommunikationsbauteil-Ratchet (Session 58) hat beim
>    Browser-Test korrekt automatisch einen Ethernet-Switch `2891021`
>    ergänzt, da die `modbus_tcp`-Datenpunkte aus Block 4 mitzählen – keine
>    Sonderbehandlung nötig, bestehender Mechanismus greift nahtlos.
> 5. **Block 5 – Steuerkoppler** `450_000001`/`002` (BMA/Gaslöschanlage,
>    Sicherheitsrelais `2981978`, SIL3/Kat.4, da ein einfaches Koppelrelais
>    nicht zwangsgeführt/zertifiziert ist). Koppler selbst bewusst ohne
>    Katalogzeile (Fremdbauteil, Regel 7).
> **Neue Einzelbauteile:** `TNC-A1412`, `TNC-A1258`, `TNC-Z0094`, `2981978`.
> **Wichtige Einschränkung:** Abmessungen von `TNC-A1412`/`TNC-A1258` sind
> NICHT aus dem Originaldatenblatt belegt (nur Masszeichnung als Grafik,
> kein Zahlenwert extrahierbar) – Platzhalter-Schätzungen (`TNC-A1412`
> von der baugleichen, real vermessenen Produktfamilie `TNC-Z0094`
> übernommen; `TNC-A1258` grobe Schätzung vergleichbarer 8A-Netzteile),
> klar im `quelle_hinweis` markiert. Vor echtem Projekteinsatz an
> Originalzeichnung/Bemusterung verifizieren.
> **Kleiner Bug behoben:** doppeltes „Kommunikativ ausgelesen:"-Präfix bei
> `A00000018487` (Modul 5 ergänzt das Präfix bereits selbst) – in der
> Excel-Quelle korrigiert.
> **Browser-Verifikation** (9 Baugruppen gleichzeitig platziert, Standschrank
> 1200×2000): BI 13/32, BO 5/12 physikalisch – exakt wie von Hand
> vorausberechnet; Komm. Modbus TCP/IP BI 11/BO 1 – exakt wie vorausberechnet;
> Feldgeräte gesamt 11 – exakt wie vorausberechnet; `overflow:[]`,
> `fehlendPlatziert:[]`; vollständiger Katalog-Scan (Regel 7, alle 207
> Baugruppen) zeigt 0 neue verwaiste Referenzen (nur die 16 bereits
> dokumentierten Alt-Lücken, siehe „Offene Punkte" unten); Modul 5 aggregiert
> alle Feldgeräte korrekt inkl. Mengen-Summierung über mehrere Baugruppen
> hinweg (z. B. SAL31.00T10 2× aus zwei verschiedenen Baugruppen); keine
> Konsolenfehler in Modul 4 oder 5.
> **Restliste:** Preise fehlen für `ASC10.51`, `GLB346.1E`, `GBB146.1E`,
> `TNC-A1412`, `TNC-A1258`, `TNC-Z0094`, `2981978`, `A00000018487`
> (keine eindeutige/datierte Quelle gefunden, siehe Einzelbauteil-/
> Feldgeräte-`quelle_hinweis`); exakte AS-i-Modbus-Registerbelegung je
> Brandschutzklappe unbestätigt (Platzhalter 2× BI); Entriegelungstaster
> Sicherheitskette am Schaltschrank noch nicht modelliert; `TNC-A1412`/
> `TNC-A1258`-Abmessungen unverifiziert (s. o.).

> **Nachtrag Session 68 (04.10.2026, Teil 3) – Fork-Recherche für fehlende
> Baugruppen (Absperr-/Lüftungsklappen, Brandschutzklappen, Steuerkoppler
> BMA/Gaslöschanlage) abgeschlossen, Alt-Bug in 420_000020/021 korrigiert,
> neue Regel 17, mehrere Nutzer-Entscheidungen. Excel-Eintrag selbst erfolgte
> direkt im Anschluss, siehe Teil 4 oben:**
> 1. **Echter Bugfix `420_000020`/`420_000021`** (Thermische 230V-
>    Ventilantriebe mit Koppelrelais, Session 55 – vor Formalisierung von
>    Regel 12 in Session 56 gebaut): der `dp_bo`-Override für den DDC-
>    Schaltbefehl saß auf einer eigenen `3209510`-Klemmenzeile statt auf der
>    `2967073`-Koppelrelais-Zeile, dazu 2 überzählige `klemm_f`-Klemmen für
>    die (laut Regel 12 klemmenlose) Verbindung DDC-BO→Koppelrelais-Spule.
>    Gefunden beim Vergleich mit der neuen, Regel-12-konformen Modellierung
>    aus der Lüftungsklappen-Fork-Recherche (Punkt 3 unten). Fix: Override auf
>    die `2967073`-Zeile verschoben, die beiden überzähligen Klemmen entfernt
>    (`klemm_f`-Bedarf je Baugruppe 4→2 Klemmen, BO-Zählung unverändert 1).
>    Browser-verifiziert: BO weiterhin 2/6 bei beiden Baugruppen zusammen,
>    `klemm_f` korrekt 4 (2×2) statt vorher 8, `overflow:[]`,
>    `fehlendPlatziert:[]`, keine Konsolenfehler.
> 2. **Neue Regel 17** aufgenommen (siehe „Baugruppen-Modellierungsregeln"
>    oben): Koppelrelais mit durchgeschleifter Steuerspannung für
>    Doppelfunktion Sicherheitskette+BI – **zwingend ein eigenes Relais je
>    Feldkontakt**, nie mehrere Feldkontakte in Serie auf ein gemeinsames
>    Relais (Nutzer-Begründung: sonst keine Einzelmeldung mehr möglich,
>    welche von mehreren Brandschutzklappen ausgelöst hat – erst 1:1
>    Feldkontakt↔Relais trennt Steuerspannungs-Durchschleifung und
>    Einzelmeldung sauber).
> 3. **5 Fork-Rechercheergebnisse vorliegend, noch nicht in Excel
>    übernommen** (Rohdaten `scratchpad/fork_1..5_*_ergebnis.md`):
>    - Absperrklappen Heizung/Kälte (Siemens Acvatix SAL.., nicht GDB wie
>      ursprünglich vermutet – GDB ist für Kugelhähne, hat keine
>      Endlagenschalter-Option) – 4 Baugruppen.
>    - Lüftungsklappen-Antriebe (Siemens Acvatix GLB../GBB.., 10/25 Nm ×
>      24V/230V × meldend/schaltend) – 8 Baugruppen. Wichtiger Fund (gilt
>      für beide Klappen-Blöcke): „schaltend" braucht **2× BO**, nicht 1×
>      (Antriebe haben getrennte Y1/Y2-Fahrbefehlseingänge, keinen
>      gemeinsamen Wechsel-Ausgang).
>    - Brandschutzklappen konventionell (TROX FK2-EU, Belimo-OEM-Antriebe)
>      – 6 Baugruppen, kein neues Koppelrelais nötig (`2967099` deckt die
>      Doppelfunktion ab).
>    - Brandschutzklappen ASi-Bus (TROX TROXNETCOM AS-i) – Infrastruktur
>      statt Baugruppe-je-Klappe: `TNC-A1412` (Controller = Gateway +
>      „BSK-Zentrale" in einem Gerät, 62 Teilnehmer/Doppelmaster),
>      `TNC-A1258` (Netzteil, laut Datenblatt ohne eigenen Meldekontakt),
>      `TNC-Z0094` (Meldemodul, busgespeist), `TNC-HCM2-A` (ab >62 Klappen).
>      Modellierung als Baugruppen-Aufteilung noch in Diskussion, siehe
>      unten.
>    - Steuerkoppler BMA/Gaslöschanlage – Koppler selbst ohne Katalogzeile
>      (Fremdbauteil, Regel 7). Braucht **neues Bauteil**: einfaches
>      Koppelrelais reicht nicht (nicht zwangsgeführt/zertifiziert) –
>      stattdessen Phoenix Contact Sicherheitsrelais `PSR-SCP-24DC/FSP/1X1/
>      1X2`, Art. **2981978** (SIL 3/Kat. 4, 1 TE). BMA = 1× Relais/1× BI,
>      Gaslöschanlage = 2× Relais/2× BI (ein FSP-Modul hat nur 1 Eingang).
> 4. **Nutzer-Entscheidungen zu den offenen Punkten aus Teil 3 der Fork-
>    Auswertung:**
>    - Fahrbefehle (Y1/Y2 bei Absperr-/Lüftungsklappen) → **`klemm_f`**
>      (Klemmleiste Feldgerät), nicht `klemm_l`.
>    - Doppelmaster (62 Teilnehmer) als **Standardannahme** für den
>      ASi-Ratchet (nicht Einzelmaster/31).
>    - ASi-Netzteil-Störmeldung gelöst: das `TNC-A1258` braucht ohnehin ein
>      vorgeschaltetes LSS (Spannungsversorgung ASi-BSK-Bussystem,
>      analog Regel 5) – an **dieses LSS** einen Hilfsschalter ergänzen und
>      als BI melden (Muster wie `5ST3010` an den bestehenden LSS/FI-
>      Kombinationen), statt eine fehlende Meldefunktion am Netzteil selbst
>      zu suchen.
> 5. **Noch offen – Modellierung der ASi-Brandschutzklappenanlage als
>    Baugruppe(n):** Nutzer-Vorschlag, in 3 unabhängige Baugruppen
>    aufzuteilen, damit die Stückzahl variabel bleibt:
>    1. **Grundsystem** – stattet den Schaltschrank komplett für den
>       Aufbau eines ASi-Bus-Systems aus (Controller, Netzteil+LSS+
>       Hilfskontakt) + 2 Feldklemmen für den 2-poligen ASi-Bus-Abgang.
>    2. **BMA-Kopplung + Störentriegelung über ASi** – setzt das
>       Meldemodul (`TNC-Z0094`) mit 2 kommunikativen Datenpunkten (spielt
>       sich komplett im Schaltschrank ab).
>    3. **BSK hinzufügen** – je Instanz +1 kommunikativer Datenpunkt
>       (Modbus), bis zur Vollauslastung (62 Teilnehmer, Ratchet greift
>       dann für ein 2. Grundsystem).
>    Nutzer favorisiert diesen 3-Baugruppen-Weg wegen der Variabilität.
>    Konsequenz für die spätere Anlagenkonfiguration (noch zu klären): dort
>    bräuchte es vermutlich 2 neue Eingabefelder (Anzahl BSK, Anzahl
>    Eingänge) plus den BMA-Koppler, der auf Baugruppenebene ohnehin separat
>    gesetzt wird. **Nutzer-Nachricht endete nach „1." unvollständig** – auf
>    Nachfrage als Tippfehler bestätigt, keine weitere Ergänzung. Die 2
>    Anlagen-Eingabefelder (Anzahl BSK, Anzahl Eingänge) für die spätere
>    Anlagenkonfiguration sind noch NICHT umgesetzt, nur die 3 Baugruppen
>    selbst (siehe Teil 4).
> **Umsetzung erfolgte direkt im Anschluss, siehe Teil 4 oben.**

> **Nachtrag Session 68 (04.10.2026, Teil 2) – Beschreibungs-Klarstellung
> „ASP hohe Verfügbarkeit" + echter Katalogfehler gefunden: 4 schrankinterne
> Automation-Baugruppen faelschlich als Feldgeraet markiert (Nutzer-Fund bei
> Stückliste-Kontrolle):**
> 1. **`480_A00003`/`480_A00006` Beschreibung ergänzt** (`data/anlagen.json`
>    via `ga_komponenten.xlsx`/Sheet `anlagen`): Nutzer-Vorgabe – der
>    Unterschied zu „ASP mit Bedienpanel – größere Anlage" (`480_A00002`/
>    `480_A00005`, ohne USV) war aus der Beschreibung allein nicht klar
>    genug erkennbar. Vorangestellter Satz: „Zentraler Unterschied zu 'ASP
>    mit Bedienpanel...': zusätzliche Schaltschrank-USV (480_000011), die
>    AUSSCHLIESSLICH die Automationsstation (DDC) selbst bei Netzausfall
>    kurzzeitig puffert (nicht die gesamte Anlage/angeschlossene
>    Feldgeräte)." Reiner Text-Zusatz, keine Funktionsänderung.
> 2. **Echter Bugfix – `betriebsmittel`-Feld bei 4 schrankinternen
>    Automation-Baugruppen entfernt** (Nutzer-Fund: „Das TouchPanel ist kein
>    Feldgerät, sondern Bestandteil der Stückliste für den Schaltschrank.
>    Siehe Modul 5 Feldgeräte"): `aggregateFeldgeraete()`/`sumFeldgeraete()`
>    zählen JEDE Baugruppe mit gesetztem `bg.betriebsmittel` als externes
>    Feldgerät – unabhängig davon, ob sie tatsächlich außerhalb des
>    Schranks installiert wird. Katalog-Scan (alle `betriebsmittel`-Treffer
>    in `baugruppen.json` durchgesehen) deckte auf, dass **4 Baugruppen**
>    fälschlich markiert waren, obwohl sie laut eigener Zonen-Zuordnung
>    (`zone:'tuer'`/`'steuer'`/`'leist'`, `keine_platzierung_mp`) eindeutig
>    schrankintern sind: `480_000015`/`480_000016` (TouchPanel PXM40/50,
>    Türeinbau), `480_000017` (Ethernet-Switch, Regel 12 schrankintern laut
>    eigener Session-63-Doku), `480_000018` (Schaltschrank**steckdose**,
>    der Name sagt es bereits). Zum Vergleich: die strukturell identischen
>    `480_000012`–`014` (UMG Türeinbau) und `480_000036` (Innenleuchte)
>    hatten `betriebsmittel` korrekt NIE gesetzt – das bestätigt, dass die 4
>    betroffenen Baugruppen vom etablierten Muster abwichen, kein
>    Grundsatzproblem der Systematik. Fix: `betriebsmittel`-Zellen für alle
>    4 IDs in `ga_komponenten.xlsx`/Sheet `baugruppen` geleert, `xlsx_to_json.py`
>    neu exportiert (baugruppen 184, einzelbauteile 221, feldgeraete 96,
>    anlagen 6 – Zahlen nur durch Punkt 1 oben an `anlagen.json` betroffen,
>    keine Zeilen hinzu-/weggefallen). Kein Backup nötig (reine Feldänderung,
>    kein Strukturwechsel). **Browser-Verifikation:** alle 4 Baugruppen in
>    Modul 4 platziert – `sumFeldgeraete()` jetzt `0` (vorher hätte es sie
>    mitgezählt), Modul 5 zeigt korrekt „Keine Feldgeräte"; Schaltschrank-
>    Stückliste (Modul 4, `aggregateStueckliste()`) führt alle 4 weiterhin
>    korrekt (TouchPanel-Gehäuse `zone:tuer`, Web-Schnittstelle `zone:steuer`,
>    Switch `zone:steuer`, Steckdose `zone:leist`), `overflow:[]`,
>    `fehlendPlatziert:[]`, keine Konsolenfehler.

> **Nachtrag Session 68 (03.10.2026) – Drei kosmetische Korrekturen nach
> Doppeleinspeisungs-Review (Nutzer-Fund per Screenshot): Zonengrundmaß
> ÜSS/Einspeiseklemmen korrigiert, Hauptschalter/Phasenleuchten bei
> Doppeleinspeisung als getrennte Cluster dargestellt, Stückliste-
> Spaltenbreiten fixiert:**
> 1. **ÜSS-/Einspeiseklemmen-Zonengrundmaß (Drehstrom) korrigiert**
>    (`modules/modul-03-architektur/index.html`): Nutzer-Fund „sehr viel
>    ungenutzter Platz in der Einspeisung bei Doppeleinspeisung, Grundmaß
>    evtl. falsch". Nachrechnung ergab zwei unabhängige Ursachen:
>    - `TE_USS_DS` (ÜSS+Sicherung, Drehstrom) stand auf **4 TE**, reserviert
>      für ein nie katalogisiertes hypothetisches 4-poliges ÜSS-Gerät (z. B.
>      Dehn DG S 4P 275). Die tatsächlich verwendete Baugruppe `480_000033`
>      nutzt für BEIDE Netztypen denselben 3-poligen Artikel `952305`
>      (54mm/3TE) + `5SG1812` (44mm/3TE) = 98mm/6TE – identisch zur bereits
>      in Session 67 Teil 9 korrigierten Wechselstrom-Zeile. Auf **3 TE**
>      angeglichen (7TE/126mm → 6TE/108mm Grundmaß, bei Doppeleinspeisung
>      216mm statt 252mm).
>    - `TE_KLEMME_ES_DS`/`_WS` (Einspeiseklemmen) waren mit 5TE/3TE nie
>      gegen eine reale Klemmengröße gerechnet worden (Kommentar im Code:
>      „Platzhalter, später nach Kabelquerschnitt"). Nachgerechnet gegen den
>      größtmöglichen in Modul 1/2 wählbaren Kabelquerschnitt (16mm²,
>      Dropdown `querschnitt_mm2`) → benötigt eine Phoenix Contact UT 16
>      (12,2mm/Klemme, real vermessen): 5×12,2mm=61mm (Drehstrom) bzw.
>      3×12,2mm=36,6mm (Wechselstrom). Drehstrom auf die nächstgrößere volle
>      TE-Stufe reduziert: **5TE(90mm)→4TE(72mm)**, 11mm Marge. Wechselstrom
>      blieb bei 3TE(54mm) – war bereits die engstmögliche TE-Stufe über dem
>      Bedarf (17mm Marge), keine Änderung nötig.
>    - Die real verwendeten Platzhalter-Klemmen selbst (`480_000037`/`038`,
>      Phoenix UT 2,5, 5,2mm/Klemme) bleiben unverändert („DBACS bilanziert
>      keine reale Anschlussleistung", Session 67 Teil 5) – das war nie die
>      Ursache des ungenutzten Platzes, nur das Zonen-Grundmaß war zu groß.
>    - Freigewordener Platz (36mm bei Doppeleinspeisung für uss, 36mm für
>      klemm_e) kommt automatisch der Leistungs-Erweiterungsfläche
>      (`leist_ext`) bzw. den Abgangsklemmen-Zonen (`klemm_l`/`klemm_f`/
>      `klemm_s`, über `redistributeKlemmBands()`) zugute – keine weitere
>      Code-Änderung nötig, beide Mechanismen haben die Restfläche schon
>      vorher automatisch verteilt.
>    - Browser-verifiziert (1200×2000 Standschrank, Drehstrom/Schiene
>      3-polig, Doppeleinspeisung ja, `480_A00004`): ÜSS-Füllstand 78%→**91%**,
>      Einsp.-Kl. 29%→**36%**, `klemm_l`-Kapazität 459mm→**477mm**,
>      `klemm_f`/`klemm_s` je 230mm→**239mm**, weiterhin `overflow:[]` und
>      `stuecklisteVsPlatzierungCheck()` 21=21/`fehlendPlatziert:[]`, keine
>      Konsolenfehler.
> 2. **Hauptschalter/Phasenkontrollleuchten bei Doppeleinspeisung als
>    getrennte Cluster** (`modules/modul-04-innenaufbau/index.html`,
>    `buildTuerAnsicht()`): Nutzer-Fund „Hauptschalter und Phasenleuchten
>    stehen bei Doppeleinspeisung direkt nebeneinander, in der Praxis bilden
>    Schalter+Leuchten je Einspeisung aber eine räumlich getrennte Gruppe".
>    Neue Logik: die (breitere) Phasenkontrollleuchten-Reihe wird in
>    3er-Gruppen zerlegt (= 1 Gruppe je Einspeisung, eine 3-polige
>    Einspeisung hat immer genau 3 Phasenleuchten) und als eigene Cluster
>    mit 16mm Zusatzabstand (`EINSP_GRUPPEN_GAP`) symmetrisch um die
>    Türmitte verteilt; der schmalere Hauptschalter je Einspeisung übernimmt
>    denselben X-Mittelpunkt wie seine zugehörige Leuchtengruppe (Referenz
>    ist die Leuchtenreihe, da breiter als der Schalter – Nutzer-Vorgabe).
>    Bei nur einer Einspeisung (1 Cluster) bleibt das Verhalten unverändert
>    identisch zum bisherigen, einfach zentrierten Rendering (Fallback greift
>    zusätzlich, falls die Anzahl Hauptschalter/Leuchten-Cluster nicht
>    übereinstimmt, z. B. Hauptschalter ohne zugehörige Leuchten auf der
>    Tür). Die Zeichenroutine selbst wurde dafür aus der Bandschleife in eine
>    wiederverwendbare `tuerBauteilSVG()`-Funktion extrahiert (keine
>    Verhaltensänderung für alle anderen Türbänder). Browser-verifiziert:
>    bei `480_A00004` liegen beide Hauptschalter exakt mittig unter ihrem
>    jeweiligen 3er-Leuchten-Cluster (Zentren deckungsgleich auf Pixel genau
>    nachgerechnet), 16mm Lücke zwischen den beiden Clustern; Regressionstest
>    Einfacheinspeisung (1 Hauptschalter + 3 Leuchten) weiterhin exakt mittig
>    zentriert wie vor der Änderung, keine Konsolenfehler.
> 3. **Stückliste-Spaltenbreiten fixiert** (`modules/modul-04-innenaufbau/
>    index.html`, CSS + `buildStueckliste()`): Nutzer-Fund „Stückzahl nur
>    nach horizontalem Scrollen erkennbar, mehrzeilige Bezeichnung zu breit".
>    `#stueckliste-wrap table` auf `table-layout:fixed` mit festen
>    Spaltenbreiten (`<colgroup>`: Pos 18px/Hst. 50px/Mge 26px/€-Stk 44px/
>    Gesamt 48px, Bezeichnung nimmt den Rest) umgestellt – die Bezeichnung
>    bricht dadurch öfter um (mehr Zeilen), Pos/Hersteller/Menge bleiben
>    garantiert ohne Scrollen sichtbar. Auf der Standard-Panelbreite (340px
>    − 28px Padding = 312px) passen bei den gewählten Spaltenbreiten sogar
>    BEIDE Preisspalten ohne jedes Scrollen (312px Summe exakt getroffen);
>    nur bei der schmaleren Panel-Variante (300px, <1200px Fensterbreite)
>    greift `min-width:260px` und erzwingt minimales Scrollen – dort dürfen
>    laut Nutzer-Vorgabe die Preisspalten im Scrollbereich liegen.
>    Browser-verifiziert (Desktop-Breite): `#stueckliste-wrap.scrollWidth ===
>    clientWidth` (297px, kein Scrollbalken), alle 6 Spalten inkl. Mge/Preis/
>    Gesamt sichtbar.

> **Nachtrag Session 67 (30.09.2026, Teil 12) – „Nur kleines TouchPanel
> wählbar"-Fund aufgeklärt: korrektes Verhalten, kein Bug (knappe 7mm auf
> 800×1800-Standschrank):** Nutzer-Reproduktion mit exakter Schrankgröße
> (800×1800 Standschrank) bestätigt den Fund, aber die Ursache ist die
> bereits bestehende, absichtliche Kollisionsprüfung
> (`touchpanelPasstMitMessgeraetHoehen()`, Session 64) – kein neuer Bug.
> Rechnung: verfügbarer Abstand TouchPanel-/Messgerät-Band =
> `(TUER_BAND_TOUCHPANEL − TUER_BAND_MESSGERAET) × H` = `0,11 × 1800mm` =
> **198mm**. Das große PXM50 (270mm) braucht mit Messgerät (96mm) + 22mm
> Mindeststeg **205mm** – **7mm zu knapp**, daher korrekt ausgeblendet. Das
> kleine PXM40 (198mm) braucht nur 169mm und bleibt wählbar. Auf der bisher
> für alle TouchPanel-Tests verwendeten Referenzgröße (1200×2000
> Standschrank, 220mm verfügbar) trat der Fall nie auf. **Nutzer-Entscheidung:
> so belassen** – die Prüfung schützt korrekt vor einer echten Kollision,
> 800×1800 ist für das große Bedienpanel schlicht zu kurz. Keine
> Code-Änderung. Merksatz für künftige TouchPanel-Tests: der verfügbare
> Abstand hängt linear von der Schrank-Außenhöhe ab – unterhalb von ca.
> 1863mm (205mm / 0,11) wird das große PXM50 grundsätzlich ausgeblendet,
> unabhängig vom Schranktyp.

> **Nachtrag Session 67 (30.09.2026, Teil 11) – TouchPanel/UMG-Auswahl
> vertikal korrekt ausgerichtet (Nutzer-Korrektur zu Teil 10):** die in
> Teil 10 gebaute Nebeneinander-Platzierung saß eine Zeile zu tief, weil
> jedes `.anlage-variante-lbl` Beschriftung+Select intern stapelte
> (`flex-direction:column`), während das „Baugruppe · Anlage"-Label nur
> EINMAL über dem gesamten Feld steht – dadurch begann `#anlage_varianten`
> eine Textzeile tiefer als der `bg_auswahl`-Select. Fix: Beschriftung und
> Select in zwei eigene, parallele Container aufgeteilt –
> `#anlage_varianten_labels` (neben dem „Baugruppe · Anlage"-Label, gleiche
> Höhe/Schriftstil wie `.eb-field label`) und `#anlage_varianten` (neben dem
> `bg-add-row`, nur noch nackte `<select class="anlage-variante-select">`
> ohne eigenes Label). `updateAnlageVariantenUI()` befüllt jetzt beide
> Container synchron. Browser-verifiziert: TouchPanel-Größe/Messgerät-
> Protokoll stehen jetzt exakt auf Höhe von „Baugruppe · Anlage" (Label) bzw.
> dem Anlagen-Dropdown (Select), Funktionalität (Auswahl „groß" landet
> korrekt in `belegung`) unverändert bestätigt, kollabiert weiterhin sauber
> bei Baugruppen ohne Varianten, keine Konsolenfehler.

> **Nachtrag Session 67 (30.09.2026, Teil 10) – Doppeleinspeisung-Filterung
> im Anlagen-Dropdown, 2 fehlende Doppeleinspeisung-Varianten ergänzt,
> TouchPanel/UMG-Auswahl umplatziert (Nutzer-Fund: „ich kann eine
> Doppeleinspeisung wählen, obwohl in Modul 3 diese Option nicht angewählt
> wurde"):**
> 1. **Neue Spalte `doppeleinspeisung_bindung`** (ja/nein) im Excel-Sheet
>    `anlagen` (+Export in `xlsx_to_json.py`) – steuert, ob eine Anlage nur
>    bei Einfach- oder nur bei Doppeleinspeisung im Modul-4-Dropdown
>    erscheint. `populateAnlagenAuswahl()` filtert jetzt zusätzlich nach
>    `(a.doppeleinspeisung_bindung==='ja') === (m03_doppeleinspeisung==='ja')`
>    – beide Listen sind dadurch disjunkt, nicht nur eine Teilmenge
>    zusätzlich anzeigend (Nutzer-Vorgabe: „bei Auswahl Einfacheinspeisung
>    stehen auch nur diese Modelle zur Verfügung, bei Mehrfacheinspeisung
>    nur jene").
> 2. **2 fehlende Doppeleinspeisung-Varianten ergänzt** (Nutzer-Vorgabe:
>    „wir können die 3 bisher definierten ASP für Einfacheinspeisung auch für
>    Doppeleinspeisung auswählen") – bisher gab es nur `480_A00004` (①
>    verdoppelt). Neu: **`480_A00005`** (② „mit Bedienpanel" verdoppelt) und
>    **`480_A00006`** (④a „hohe Verfügbarkeit" verdoppelt), jeweils 1:1 aus
>    dem Einfacheinspeisung-Vorbild dupliziert mit derselben Einspeisegruppe
>    ×2 (Hauptschalter/ÜSS/Phasenkontrollleuchten/Phasenüberwachung/
>    Einspeiseklemmen) wie bei `480_A00004`. TouchPanel/UMG-Protokoll
>    (beide) und – bei ④a – die interne USV (`480_000011`) bleiben bewusst
>    einfach (unabhängig von der Einspeisezahl). Export: anlagen 4→**6**.
>    Browser-verifiziert: alle 3 Doppeleinspeisung-Varianten (`A00004`-`006`)
>    auf dem Standschrank-Referenzfall (Drehstrom/1feld UND Wechselstrom/
>    getrennt_els) `fehlendPlatziert:[]`/`overflow:[]`, `belegung` zeigt
>    korrekt `menge:2` nur für die 5 Einspeisegruppen-Mitglieder, Rest
>    `menge:1`, keine Konsolenfehler.
> 3. **Layout: TouchPanel-Größe/Messgerät-Protokoll umplatziert** (Nutzer-
>    Vorgabe: „wir verlieren eine komplette Ansichtsreihe für die
>    Schaltschrankansicht... verkürze den Balken für Baugruppe/Anlage, dann
>    geht es auch daneben rechts" – generelles Prinzip: „Ausnutzung der
>    Platzverhältnisse im Bedienfeld, damit die Schaltschrankansicht nicht
>    immer kleiner wird"). `#anlage_varianten` stand bisher als eigene volle
>    Zeile UNTER dem Baugruppe·Anlage-Feld (drückte Einzelbauteil-Auswahl/
>    Zonen-Füllstand/Schranksicht jeweils eine Zeile nach unten). Fix: neuer
>    Flex-Wrapper `.bg-anlage-row` – `.bg-add-row` (Anlage-Dropdown+Menge+
>    Buttons) bekommt `flex:1 1 220px` statt voller Breite,
>    `#anlage_varianten` sitzt jetzt kompakt DANEBEN auf derselben Zeile
>    (`flex:0 0 auto`, `.anlage-variante-lbl` auf feste 130px begrenzt).
>    Kein Zeilenverlust mehr, wenn eine Anlage mit Varianten gewählt wird;
>    kollabiert sauber auf volle Breite, wenn keine Varianten vorhanden sind
>    (normale Baugruppe oder Anlage ohne `gruppe`-Mitglieder). Browser-
>    verifiziert (Screenshot-Vergleich vorher/nachher), TouchPanel-Auswahl
>    (klein/groß) weiterhin voll funktionsfähig in der neuen Position,
>    keine Konsolenfehler.
> 4. **TouchPanel-Auswahl selbst („ich kann bei Standschränken nur das
>    kleine TouchPanel auswählen") konnte trotz gezielter Nachstellung NICHT
>    reproduziert werden:** exakt der vom Nutzer gezeigte Standschrank
>    (Montagebereich 1099×1745, entspricht der 1200×2000-Referenz) mit ②/④a
>    getestet – `#anlage_variante_touchpanel` enthält beide Optionen
>    (`480_000015`/`480_000016`), beide sind laut
>    `touchpanelPasstMitMessgeraetHoehen()`-Rechnung zulässig (benötigt
>    205mm, verfügbar 220mm auf 2000mm-Türhöhe), Auswahl per echtem
>    Formular-Input + Klick auf „+" bestätigt: `480_000016` (groß) landet
>    korrekt in `belegung`. Keine Code-Änderung an der Auswahllogik
>    vorgenommen (nichts Falsches gefunden) – die Layout-Änderung in Punkt 3
>    macht die beiden Felder jetzt aber deutlich sichtbarer/eindeutiger als
>    eigenständige Dropdowns (vorher als eigene, etwas unauffällige Zeile
>    unter dem Anlagen-Feld). Falls das Problem weiterhin auftritt: bitte
>    exakte Reihenfolge der Klicks + ob vorher schon ein Messgerät auf
>    derselben Tür stand (das würde die Rechnung zulässigerweise ändern)
>    mitteilen.
> **Weiterhin offen:** die AV/SV/USV-Auswertung in Modul 4 (welche Anlage
> bei welcher Einspeisungsart-Kombination sinnvoll ist) ist unverändert nur
> Vorschlag, noch nicht umgesetzt (siehe Teil 7).

> **Nachtrag Session 67 (30.09.2026, Teil 9) – ②/④a zusätzlich auf dem
> großen Wandschrank (1000×1200) bestätigt, exaktes Lehrbuch-Beispiel für
> „Ausnahme Wandschrank" + Bugfix-Wirkung gefunden:** Ergänzend zu Teil 8:
> `480_A00002` (mit Bedienpanel) passt auf 1000×1200/Drehstrom/1feld
> vollständig (`fehlendPlatziert:[]`, `overflow:[]`) – `480_A00003` (hohe
> Verfügbarkeit) dagegen NICHT: die zusätzliche USV (`2320225`/`2320296`)
> passt nicht mehr in die `leist`-Zone dieses Wandschranks, und da
> Wandschrank strukturell keine Folgefelder kennt, bleiben beide Artikel
> unplatziert. **Vor dem Teil-8-Fix wäre das lautlos passiert** (Stückliste
> hätte die USV geführt, Zeichnung nicht, ohne jede Markierung) – jetzt
> korrekt `overflow:["leist"]` UND `fehlendPlatziert:["2320225","2320296"]`
> gleichzeitig gemeldet. Genau das vom Nutzer erwartete Verhalten („Alle
> anderen Anlagen setzen darauf auf und vergrößern lediglich die
> Schaltanlage um weitere Felder, Ausnahme Wandschrank" – ④a braucht hier
> de facto einen Standschrank oder einen größeren Wandschrank). Keine
> weitere Korrektur nötig, reine Bestätigung. Keine Konsolenfehler.

> **Nachtrag Session 67 (29.09.2026, Teil 8) – Echter Overflow-Erkennungs-
> Bug gefunden + behoben, `480_A00004` Doppeleinspeisung vollständig Ende-
> zu-Ende verifiziert (Nutzer-Auftrag: „Teste alle ASP-Varianten und
> Einspeiseformen intensiv... Die Grundausstattung eines ASP muss passen"):**
> Systematischer Testlauf (①②④a + neu `480_A00004`, je Standschrank/
> Wandschrank × Drehstrom/Wechselstrom × alle 4 `zone_modus` ×
> Doppeleinspeisung ja/nein, mit `stuecklisteVsPlatzierungCheck()` +
> Overflow-Auswertung je Konfiguration) deckte einen echten, bisher
> unbemerkten Bug in `calculateFelder()` auf:
> **Bug:** die Overflow-Bereinigung am Ende von `calculateFelder()`
> (`if (!z.overflow) return;`) übersprang jede Zone, deren EIGENER
> `placeInBands()`/`placeInKlemmRow()`-Aufruf in diesem Feld bereits mit
> `overflow:false` zurückkam – das passiert immer dann, wenn in einem Feld
> gar keine Bauteile für diese Zone zur Platzierung anstanden (0 von 0
> „platziert"), weil die zugehörige(n) Baugruppen-Instanz(en) schon im
> Reservierungs-Dry-Run (`platziereBaugruppenFuerFeld()`) für JEDE ihrer
> Zonen gescheitert sind und dadurch nie in `queues[zn]` (und damit nie in
> `placeInBands()`) ankamen. In einem `repeat:false`-Feldtyp (z. B. Typ A
> „Vollfeld" bei `zone_modus='1feld'`, oder Typ C „Einspeisung" bei JEDEM
> Modus) gibt es kein Folgefeld, das die Instanz nachträglich aufnehmen
> könnte – sie blieb bis zum Sitzungsende sang- und klanglos in
> `bgInstanceQueue` hängen, **ohne jede Warnung**: kein rotes „!" in der
> Zeichnung, keine Overflow-Markierung, nur eine unvollständige Stückliste-
> vs-Platzierung, die man erst mit dem neuen Cross-Check-Tool bemerkt.
> Gefunden am konkreten Fall: `480_A00001` „ASP Standard" (Drehstrom) auf
> einem sehr kleinen 600×600-Wandschrank – `evert`/`leist`/`steuer` waren
> faktisch zu klein (Montagebereich reicht nicht für Drehstrom-Energie-
> verteilung + Rest), aber `platziert:19` statt `stueckliste:21`,
> `fehlendPlatziert:["RE22R2HMR","3UG5616-1CR20"]`, **`overflow:[]` – keine
> einzige Zone war markiert**, obwohl 2 Artikel komplett fehlten. Sehr
> wahrscheinlich dieselbe Fehlerklasse wie der in Session 67 Teil 6
> dokumentierte, nie reproduzierte „ÜSS wieder 0%"-Nutzerfund (dort vermutet
> als reiner Client-Altzustand – könnte stattdessen genau dieser Bug
> gewesen sein, wenn der Nutzer eine Konfiguration nahe der Kapazitätsgrenze
> hatte).
> **Fix (zwei Stellen in `modul-04-innenaufbau/index.html`):**
> 1. `calculateFelder()`: die Overflow-Neuberechnung am Ende läuft jetzt
>    UNBEDINGT für jede Zone in jedem Feld (kein `if (!z.overflow) return;`
>    mehr) – `z.overflow` wird für jede Zone im JEWEILS LETZTEN sie
>    zeigenden Feld frisch aus dem tatsächlichen Rest abgeleitet
>    (`queues[zn].length>0` ODER eine offene `bgInstanceQueue`-Instanz für
>    diese Zone), unabhängig vom ursprünglichen Wert.
> 2. `calculate()`: die über alle Felder aggregierte `aggZones`-Ansicht
>    (`letzteAggZones`, Grundlage für `stuecklisteVsPlatzierungCheck()` UND
>    `buildFuellstand()`) hatte das `overflow`-Feld bisher komplett
>    unterschlagen (`aggZones[zn] = {te_belegt, mm_total, mm_used, channels,
>    rows}` – kein `overflow`-Schlüssel) – jetzt per OR über alle Felder
>    ergänzt.
> **Browser-Verifikation des Fixes:** derselbe 600×600-Wandschrank-Fall
> zeigt jetzt korrekt `overflow:["evert","leist","steuer"]` bei weiterhin
> `fehlendPlatziert:["RE22R2HMR","3UG5616-1CR20"]` – Stückliste-Lücke UND
> Overflow-Warnung stimmen jetzt überein. Regressionscheck: ein künstlicher
> Stresstest (`480_A00003` mit `bg_menge=4` auf `zone_modus='je_feld'`)
> zeigt weiterhin korrekt NUR `klemm_e`/`uss` als Overflow (Einspeisung ist
> strukturell `repeat:false`, kann keine 4-fache Menge in einem einzigen
> Feld aufnehmen – exakt das erwartete Verhalten, keine Überkorrektur).
> **Vollständiger Testlauf `480_A00004` „ASP Standard mit Doppeleinspeisung"
> Ende-zu-Ende** (vorher nur die Modul-3-Zonenverdopplung isoliert
> getestet, jetzt erstmals mit der Anlage selbst kombiniert): Standschrank ×
> {Drehstrom/Wechselstrom} × {1feld, getrennt_els, einsp_misch, je_feld},
> plus Wandschrank 600×600 (Wechselstrom – overflow korrekt erkannt, Schrank
> schlicht zu klein) und Wandschrank 1000×1200 (Wechselstrom – passt
> vollständig, 0 Abweichungen) – **in JEDER Standschrank-Kombination sowie
> im ausreichend großen Wandschrank**: `belegung` zeigt korrekt `menge:2`
> für Hauptschalter/ÜSS/Phasenkontrollleuchten/Phasenüberwachung/
> Einspeiseklemmen und `menge:1` für Störquittiertaster+SSM/Innenleuchte,
> `fehlendPlatziert:[]`, `overflow:[]`, 0 Konsolenfehler. Regressionscheck
> „Doppeleinspeisung in Modul 3 aktiv, aber nicht-verdoppelte Anlage (①) in
> Modul 4 gewählt": kein Absturz, Zone bleibt einfach unterausgelastet.
> **Grundausstattung ①②④a zusätzlich regressionsgeprüft** (Standschrank ×
> Drehstrom/Wechselstrom × 1feld/getrennt_els/einsp_misch, Wandschrank
> 600×600 Drehstrom): durchgängig `fehlendPlatziert:[]`, `overflow:[]`
> außer dem oben beschriebenen, jetzt korrekt erkannten Wandschrank-
> Kapazitätsfall – bestätigt die Grundausstattung ist über alle getesteten
> Varianten hinweg weiterhin korrekt (keine Regression durch die
> Doppeleinspeisung/AV-SV-USV-Ergänzungen).
> **Bestätigt (Nutzer-Erwartung „Ausnahme Wandschrank"):** ein zu kleiner
> Wandschrank überläuft korrekt sichtbar statt mehr Felder zu bekommen
> (Wandschrank erzwingt strukturell `zone_modus='1feld'`, keine Folgefeld-
> Kaskade) – ein ausreichend großer Wandschrank (1000×1200) verkraftet auch
> die verdoppelte Einspeisegruppe anstandslos.

> **Nachtrag Session 67 (29.09.2026, Teil 7) – Einspeisungsart AV/SV/USV als
> Modul-3-Grundlage ergänzt (Nutzer-Vorgabe zur Doppeleinspeisungs-
> Klassifikation):** Nutzer-Feedback zum vorherigen Vorschlag (AV/NEA,
> AV/USV, NEA/USV als Paarungstypen): AV/NEA verhält sich bauteilseitig
> identisch zu AV/AV – keine Sonderbehandlung nötig, nur die Unterscheidung
> „gepuffert (USV) vs. nicht gepuffert (AV/NEA)" ist für die Bauteilauswahl
> relevant. Daraus abgeleitete, vom Nutzer vorgeschlagene 3-Typen-
> Klassifikation je Einspeisung: **AV** (Allgemeine Versorgung), **SV**
> (Sicherheitsversorgung/NEA-gestützt – bauteilseitig identisch zu AV, nur
> Dokumentationswert) und **USV** (bereits vorgelagert batteriegepuffert).
> **Umgesetzt in Modul 3:** zwei neue Selects `zone_einspeisung1_typ`
> (immer sichtbar) und `zone_einspeisung2_typ` (nur sichtbar wenn
> `zone_doppeleinspeisung='ja'`, per `updateZoneVisibility()` ein-/
> ausgeblendet), Optionen AV/SV(NEA)/USV, Default `av`, Persistenz
> `m03_einspeisung1_typ`/`m03_einspeisung2_typ` über `saveZoneInputs()`/
> `loadZoneInputs()`. **Bewusst ohne Einfluss auf die Zonenmaße** (reine
> Klassifikation/Dokumentation, ausführlicher Code-Kommentar in
> `calculateZones()`) – die eigentliche Auswertung (welche Modul-4-Anlage
> passt) ist noch NICHT implementiert, siehe unten. Browser-verifiziert:
> Felder rendern, Persistenz über echten `change`-Event-Durchlauf bestätigt
> (`sv`/`usv` gesetzt → localStorage korrekt → Reload stellt Werte korrekt
> wieder her), Sichtbarkeits-Toggle bei Doppeleinspeisung nein/ja korrekt,
> keine Konsolenfehler. Nach dem Test wieder auf Default (`av`/`av`)
> zurückgesetzt.
> **Noch offen (nächster Schritt):** die Auswertung in Modul 4 fehlt noch.
> Kernidee (Nutzer-Aussagen aus dieser und der vorherigen Nachricht
> zusammengeführt): AV und SV benötigen bauteilseitig **keine** eigene
> Pufferung – die bestehende Anlage „ASP … hohe Verfügbarkeit" (④a, mit
> interner USV `2320225`/`2320296`) bleibt die richtige Wahl, wenn KEINE der
> (ggf. zwei) Einspeisungen bereits USV ist. Ist mindestens eine Einspeisung
> vom Typ USV, ist die Redundanz bereits vorgelagert vorhanden – die
> interne USV wäre überflüssige Doppelpufferung. Da der elektrische
> Anschluss am Schrank dabei aussieht wie eine normale Wechselstromquelle
> (DBACS bilanziert keine Schaltung, nur Platzbedarf/Bauteile), ist in
> diesem Fall vermutlich **kein neues Bauteil** nötig, sondern nur eine
> zusätzliche, klar beschriftete Anlagen-Variante im Modul-4-Dropdown (z. B.
> „ASP … hohe Verfügbarkeit (externe USV)" = inhaltlich identisch zu
> ①/②, aber mit erklärendem Namen, damit der Nutzer nicht versehentlich die
> teurere interne-USV-Variante wählt, wenn die Redundanz schon vorgelagert
> existiert) – vor Umsetzung mit dem Nutzer bestätigen, da dies eine reine
> Katalog-/UX-Entscheidung ist, kein technischer Zwang. Die STS-
> Umschaltung bleibt weiterhin explizit zurückgestellt (eigener Fork bei
> Bedarf). Die separate „Einspeisung als eigenes Feld"-Variante (Feldtyp-C-
> `repeat`) bleibt ebenfalls zurückgestellt. Das bereits fertige `480_A00004`
> („ASP Standard mit Doppeleinspeisung") ist von dieser AV/SV/USV-
> Klassifikation unberührt – es bleibt die Anlage für den Fall „zwei
> gleichwertige, ungepufferte Einspeisungen" (AV/AV, AV/SV, SV/SV) und noch
> nicht Ende-zu-Ende in Modul 4 getestet (siehe Teil 5/6 oben – Grundlage
> aus Modul 3 wurde bereits verifiziert, die Anlage selbst in Modul 4 noch
> nicht mit `zone_doppeleinspeisung='ja'` kombiniert platziert).

> **Nachtrag Session 67 (29.09.2026, Teil 2) – Zonen-Korrektur FI/LSS
> (evert statt leist), Cache-Falle beim lokalen Testen behoben, Einspeise-
> klemmen-Katalog-Lücke bestätigt:**
> Nutzer-Fund per Screenshot: obwohl der Platzierungs-Bug (s. o.) behoben
> war, saßen FI/LSS/Hilfsschalter in `480_000036` (neue Innenleuchte) UND
> `480_000018` (heute editierte Steckdose) fälschlich in Zone `leist` statt
> `evert` – ich hatte mich am alten „im Leistungsfeld"-Präzedenzfall von
> `480_000018` orientiert statt gegen die etablierte Regel zu prüfen (die 11
> LSS/FI-Baugruppen aus Session 63, Gewerk 440, nutzen durchgängig `evert`).
> **Fix:** `5SV3321-4` (FI) + `5SL6116-6` (LSS) + beide `5ST3010`-
> Hilfsschalter in beiden Baugruppen auf `evert` verschoben (8 Zeilen in
> `baugruppen_bauteile`). Die Steckdose/Leuchte selbst (kein Schutzorgan)
> bleibt bewusst in `leist`.
> **Wichtiger Nebenfund – Cache-Falle beim lokalen Testen:** der statische
> Python-Devserver (`http.server`) schickt keine Cache-Control-Header –
> nach einer Code-/Katalogkorrektur lieferte der Browser bei normalem
> Reload wiederholt die VORHERIGE Version von `baugruppen.json` **und sogar
> der HTML/JS-Dateien selbst** aus dem HTTP-Cache aus (sah wie ein neuer
> Bug aus, war nur veraltete Daten). Fix: `fetch(...,{cache:'no-store'})`
> für die drei Katalog-JSONs in `loadData()` (Modul 4) ergänzt – deckt aber
> NICHT das HTML/JS-Dokument selbst ab. **Merksatz für künftige Sessions:**
> nach jeder Code-Änderung beim lokalen Testen einen Hard-Refresh (Strg+
> Shift+R) machen bzw. eine Cache-Bust-Query (`?cb=1`) an die URL hängen,
> sonst können Verifikationsergebnisse falsch-negativ oder falsch-positiv
> ausfallen.
> **Bestätigte Katalog-Lücke (nicht neu, aber jetzt sichtbar):** vollständiger
> Scan über alle 181 Baugruppen zeigt **0 Baugruppen, die jemals etwas in
> Zone `klemm_e` (Einspeiseklemmen) platzieren** – es gibt schlicht noch
> keine Einspeiseklemmen-Baugruppe im Katalog (Planungsfabrikat Phoenix
> Contact UT-Reihe laut Modul-4-Architekturregeln vorgesehen, aber nie
> angelegt). Betrifft nicht nur Automation/ASP, sondern den gesamten
> Katalog. Noch nicht behoben – Nutzer-Rückfrage, ob das jetzt als Teil von
> „ASP Standard" ergänzt wird oder als eigener Folgeschritt.
> **Browser-Verifikation:** alle 3 Anlagen (①②④a) in Wechselstrom mit
> erzwungenem Cache-Bust neu getestet – ÜSS 91%, Energievert. 30–38%,
> Leistung 30–34%, Steuerung 52–77%, keine Nullen, 0 verwaiste Referenzen,
> beide Baugruppen zeigen FI/LSS/Hilfsschalter korrekt in `evert`, keine
> Konsolenfehler.
>
> **Nachtrag Session 67 (29.09.2026, Teil 3) – Vollständiger Audit + Test
> aller 3 Anlagen (Nutzer-Auftrag „Prüfe und platziere komplett"):**
> Zusätzliche ②/④a-Bauteile (TouchPanel `015`/`016`, Web-Schnittstelle
> `S55842-Z117`, UMG `012`/`013`/`014` + LSS `5SL6316-7`, USV `2320225`/
> `2320296`) gegen die Modellierungsregeln geprüft – **keine weiteren
> Zonenfehler gefunden** (LSS der UMG-Baugruppen war schon seit Session 58
> korrekt in `evert`; USV-Netzteil/Batterie korrekt in `leist`, kein
> Schutzorgan enthalten). Danach alle 3 Anlagen systematisch durchgetestet:
> Drehstrom×Schiene ja/nein, Wechselstrom, alle TouchPanel-/UMG-
> Protokoll-Varianten (10 Kombinationen) – **durchgängig korrekt platziert,
> 0 verwaiste Referenzen, keine Konsolenfehler.** Dabei einen eigenen
> Testfehler gefunden und korrigiert (kein App-Bug): direktes Pokern von
> `m03_zone_schiene` per `localStorage` ohne Modul 3 neu zu durchlaufen
> lässt abhängige Werte wie `m03_h_evert` veraltet stehen (zeigte
> fälschlich `evert:0%`) – nach echtem Modul-3-Durchlauf korrekt.
> **Bestätigte, bereits bekannte Lücke (keine Regression):** die
> TouchPanel-Größenauswahl (`tuerTouchpanelPasstAufTuer()`) sieht das im
> selben Anlagen-Aufruf gleichzeitig hinzukommende Messgerät noch nicht,
> weil dessen Zonen-Zugehörigkeit erst bei `addAnlage()` selbst entsteht –
> auf einem sehr kleinen 600×600-Wandschrank blieben rechnerisch beide
> TouchPanel-Größen wählbar (Default „klein" landet aber sicher, kein
> aktives Problem, nur bei manueller Wahl der großen Variante relevant).
> Bleibt als dokumentierte Einschränkung bestehen (siehe Restliste
> „Tür-Bündel-Kollisionsprüfung").
>
> **Nachtrag Session 67 (29.09.2026, Teil 4) – Prüfroutine um Mehrfeld-/
> Zonenmodi erweitert (Nutzer-Vorgabe: „auch für getrennte Schränke oder
> Zonen sicherstellen"):** Wandschrank erzwingt immer `zone_modus='1feld'`
> (bestehende Regel), Mehrfeld ist daher nur am Standschrank relevant.
> Alle 4 `zone_modus`-Werte mit ④a (Superset aller Anlagen-Mitglieder)
> getestet:
> - `1feld` × nebeneinander (Drehstrom): korrekt, bereits übereinander
>   vorher getestet.
> - `je_feld`: bei 1×/4× Menge bleibt es bei 1 Feld (Demand passt), bei 8×
>   korrekt 2 Felder (A+B), Folgefeld-Kaskade funktioniert, kein Overflow.
> - `getrennt_els` (Einspeisung/Leistung/Steuerung als 3 eigene Felder C/D/
>   E): korrekt – eine Instanz mit Zonen in unterschiedlichen Feldtypen
>   (z.B. Hauptschalter tuer+steuer, nur in Feld E) wartet automatisch bis
>   zum passenden Feld, alle Zonen befüllt, kein Overflow.
> - `einsp_misch` (Einspeisung getrennt C, Leistung+Steuerung gemischt B),
>   zusätzlich mit Wechselstrom kombiniert: korrekt, 2 Felder (C+B), auch
>   mit 3× Menge (Folgefeld-Druck) weiterhin fehlerfrei.
> Über alle Kombinationen: 0 verwaiste Referenzen, kein unerwarteter
> Overflow, keine Konsolenfehler. Die Anlagen-Engine ist damit gegen alle
> vier Modul-3-Zonenmodi UND beide Schranktypen verifiziert.
>
> **Nachtrag Session 67 (29.09.2026, Teil 5) – Beide Restlücken geschlossen
> (Nutzer-Vorgabe: „außer Doppeleinspeisung, das machen wir separat"):**
> 1. **NEU `480_000037`/`480_000038` „Einspeiseklemmen Drehstrom
>    (L1/L2/L3/N/PE)"/„...Wechselstrom (L/N/PE)"** (Kategorie neu:
>    „Einspeisung", Zone `klemm_e`) – **keine neuen Einzelbauteile nötig**,
>    die Phoenix Contact UT-2,5-Reihe war bereits seit Session 27b
>    katalogisiert, nur nie referenziert (0/181 Baugruppen nutzten bisher
>    `klemm_e`, jetzt bestätigt behoben). UT2,5 als kleinste/repräsentative
>    Baugröße gewählt (DBACS bilanziert keine reale Anschlussleistung).
>    Farbschema L1 braun/L2 schwarz/L3 grau/N blau/PE grün-gelb folgt dem
>    Standard-Phoenix-Schema – die in Session 52 aufgeworfene Grundsatzfrage
>    „in der Praxis oft nur grau" bleibt bewusst unentschieden, nur
>    dokumentiert. Beide neuen Baugruppen zusätzlich in `anlagen_baugruppen`
>    für ①②④a verankert (`netztyp_bindung` wie bei der Phasenüberwachung,
>    automatische Auflösung nach Projekt-Netztyp, keine manuelle Auswahl).
> 2. **Tür-Bündel-Kollisionsprüfung erweitert:** `tuerTouchpanelPasstAufTuer()`
>    in `touchpanelPasstMitMessgeraetHoehen()` (reine Distanzformel) +
>    Wrapper extrahiert; neue `tuerTouchpanelPasstAufTuerInAnlage(bg, anlage)`
>    berücksichtigt zusätzlich Messgeräte, die über DIESELBE Anlage
>    gleichzeitig hinzukommen (z.B. die `umg_protokoll`-Gruppe), nicht nur
>    bereits in der Belegung stehende – schließt die beim Bau der
>    Anlagen-Engine dokumentierte Lücke. `updateAnlageVariantenUI()`
>    nutzt jetzt diese Variante für den TouchPanel-Options-Filter.
> **Browser-Verifikation:** ① mit `480_000037` (Drehstrom) korrekt
> aufgelöst, `klemm_e` 29% befüllt (vorher 0%), keine verwaisten
> Referenzen. TouchPanel-Filter: auf 1200×2000-Standschrank bleiben
> beide Größen wählbar (Regressionscheck bestanden); auf einem sehr
> kleinen 600×600-Wandschrank werden jetzt **beide** Größen korrekt
> ausgeblendet (rechnerisch passt selbst PXM40 nicht mehr neben das
> gleichzeitig hinzukommende UMG96-Messgerät – Distanzformel bestätigt:
> 169mm nötig vs. 66mm Bandabstand verfügbar). **Bekannte Rand-Einschränkung
> (kein Crash, aber UX-Lücke):** ist die Options-Liste dadurch leer, wählt
> `addAnlage()` gar kein TouchPanel aus (leerer `<select>`-Wert passt zu
> keiner `bg_id`) – die Anlage wird trotzdem anstandslos ohne TouchPanel
> hinzugefügt, ohne Warnhinweis für den Nutzer. Kein Fehlverhalten (keine
> Bauteile verschwinden unbemerkt, kein Overlap entsteht), aber ein
> stummes Weglassen ohne Rückmeldung – bei Bedarf später um einen
> sichtbaren Hinweistext ergänzen. Keine Konsolenfehler in beiden Fällen.
>
> **Nachtrag Session 67 (29.09.2026, Teil 6) – Stückliste-vs-Platzierung-
> Cross-Check + stark erweiterte Prüfroutine, Nutzer-Fund „ÜSS wieder 0%"
> nicht reproduzierbar:**
> Nutzer meldete per Screenshot erneut ÜSS=0% trotz Stückliste-Eintrag
> (Klemmraum 20, LVB gefordert, Wechselstrom, Standschrank 699×1499).
> **Trotz exaktem Nachstellen aller sichtbaren Einstellungen (inkl.
> vollständigem `localStorage.clear()`) sowie der Hypothese „Anlage
> mehrfach ohne Leeren hinzugefügt" (menge=3 getestet) ließ sich der Fehler
> nicht reproduzieren** – uss platzierte in jedem Versuch korrekt (78–91%).
> Deutet auf clientseitigen Alt-Zustand (Cache/localStorage) im Nutzer-
> Browser hin, nicht auf einen weiterhin bestehenden Code-Fehler.
> **Neues, dauerhaftes Verifikationswerkzeug** `stuecklisteVsPlatzierungCheck
> (aggZones)` (Modul 4, nahe `buildFuellstand()`): vergleicht die Artikel-
> menge aus der Stückliste (`belegung` + `resolveBaugruppenBauteile()`) mit
> den tatsächlich in Zonen/Tür/Automatik-Ergänzungen platzierten Artikeln –
> deckt genau die Fehlerklasse „Stückliste hat es, Zeichnung nicht" ab.
> Dafür neue globale `letzteAggZones` (Ergebnis des letzten `calculate()`-
> Laufs, analog `letzteFelder`) eingeführt. **Erweiterte Prüfroutine**
> (Nutzer-Vorgabe: alle Modul-3-Design-Varianten inkl. „Leistung/Steuerung
> getrennt/allein/oben-unten/nebeneinander, mehrere Schränke" + Folgefeld-
> Abschlusstest) – 8 Konfigurationen durchgetestet, je mit ①/②/④a und dem
> neuen Cross-Check:
> - Drehstrom+Schiene ja: `1feld` übereinander/nebeneinander, `getrennt_els`,
>   `einsp_misch` übereinander/nebeneinander
> - Wechselstrom: `getrennt_els` (+ Abschlusstest 8× und 25× ④a – 25×
>   erzeugt korrekt **10 Felder** C+7×D+2×E, Folgefeld-Kaskade robust)
> - Wandschrank (Wechselstrom)
> Durchgängig: `fehlendPlatziert: []` (Cross-Check 0 Abweichungen), 0
> verwaiste Referenzen, kein unerwarteter Overflow, keine Konsolenfehler.
> **Empfehlung an den Nutzer bei erneutem Auftreten:** kompletten
> `localStorage` leeren (oder Browser-Profil/Inkognito-Fenster testen) und
> Modul 1/2 → Modul 3 → Modul 4 einmal komplett frisch durchklicken, bevor
> erneut gemeldet wird – die bisherigen zwei ähnlichen Fälle waren beide
> auf clientseitige Altzustände zurückzuführen (Cache bzw. nicht neu
> durchlaufenes Modul 3).

> **Nachtrag Session 67 (29.09.2026) – Zwei echte Platzierungs-Bugs durch
> Anlagen-Praxistest gefunden + behoben (Nutzer-Fund: „ASP Standard" zeigte
> in der Zeichnung ÜSS/Energieverteilung/Leistung leer, obwohl in der
> Stückliste vorhanden):**
> Nutzer-Hinweis, der zum Fund führte: „Baugruppen mit all ihren
> funktionierenden Setzmechanismen müssen jetzt nacheinander aufgerufen
> werden, um eine Anlage zu bauen – das müssen wir gut testen." Genau das
> deckte zwei unabhängige, vorher nie in dieser Kombination getestete Bugs
> auf (ASP ist die erste Anlage überhaupt):
> 1. **Bug 1 (Datenfehler, Modul 3):** `TE_USS_WS`/`TE_SICH_WS` (ÜSS-Zonen-
>    breite Wechselstrom) standen noch auf `2`/`2` TE (72mm) – Restwert aus
>    einer frühen Session, bevor die echten Session-66-Artikel `952305`
>    (DEHNguard M TNC 275 FM) und `5SG1812` (Sicherungssockel D03) gewählt
>    wurden, beide real 3TE/44–54mm, zusammen 98mm. Auf `3`/`3` TE (108mm)
>    angehoben.
> 2. **Bug 2 (echter Logikfehler, Modul 4, wichtiger):**
>    `platziereBaugruppenFuerFeld()` brach die GESAMTE
>    Baugruppen-Instanz-Warteschlange ab (`break`), sobald EINE Instanz in
>    EINER ihrer Zonen nicht mehr passte – dadurch wurden auch alle
>    NACHFOLGENDEN Instanzen für völlig andere, noch freie Zonen (z.B.
>    Leistung/Energieverteilung) verworfen. Eine zu volle ÜSS-Zone ließ so
>    den kompletten Rest der Anlage unsichtbar bleiben, obwohl dort reichlich
>    Platz war. Fix: `break` → `continue` (nur die eine nicht passende
>    Instanz wird übersprungen/bleibt für ein Folgefeld vorgemerkt, alle
>    anderen werden weiter versucht; Add-Reihenfolge je Zone bleibt gewahrt,
>    da `confirmed[zn]` weiter sequenziell wächst). Dieser Bug war nicht
>    anlagen-spezifisch (jede manuelle Mehrfach-Baugruppen-Auswahl mit
>    Zonen-Overflow hätte ihn auch ausgelöst), wurde aber erst durch die
>    Anlagen-Bündelung (6+ Baugruppen gleichzeitig über mehrere Zonen)
>    praktisch sichtbar.
> **Browser-Verifikation:** alle 3 Anlagen (①②④a) je in Drehstrom UND
> Wechselstrom getestet (6 Kombinationen) – alle Zonen mit tatsächlichem
> Inhalt zeigen jetzt korrekt >0% (vorher bei Wechselstrom durchgängig
> ÜSS/Energievert./Leistung = 0% trotz gefüllter Stückliste), 0 verwaiste
> Referenzen, keine Konsolenfehler. Regressionscheck: Drehstrom-Zonenmaße
> unverändert (126mm ÜSS), Overflow-Erkennung funktioniert weiterhin
> korrekt (8× ④a gleichzeitig → `steuer`-Zone korrekt als Overflow markiert,
> nicht wieder blackout). Keine Excel-/Katalogänderung nötig, reiner
> Code-Fix in `modul-03-architektur/index.html` + `modul-04-innenaufbau/
> index.html`.

> **Sitzungsstand Session 67 (27.09.2026) – Start des Anlagen-Features
> (Schritt 1/2 für Automation), neue Baugruppe Schaltschrank-Innenleuchte,
> Normenlücken-Korrektur an `480_000018`:**
> Nutzer-Entscheidung zum Anlagen-Konzept (siehe Memory
> `project_anlagenbaugruppen.md`): eine Anlage bündelt bestehende `bg_id`s,
> Schranktyp/Feldaufteilung/Netzanschluss bleiben außerhalb der Anlagen-
> Definition (kommen aus Modul 1–3), CPU (`480_000007`) und Energieversorgung
> (`480_000008`–`010`) werden nicht explizit gelistet (automatischer Ratchet),
> LVB bleibt global. 3-Schritte-Ablauf: (1) Fork recherchiert praxisnahe
> Konfigurationen, (2) Katalog-Vollständigkeit prüfen/nachbessern, (3) Anlage
> zusammensetzen (Excel-Sheets `anlagen`/`anlagen_baugruppen` + `addAnlage()`
> – **Schritt 3 noch nicht umgesetzt**, diese Session deckt nur 1+2 für die
> Automation-Anlagen ab).
> **3 Automation-Anlagen-Vorschläge (Schritt 1, Fork-Recherche, Quellen:
> Werksnorm 8 GLT-Standard + UKT-Krankenhaus-TGA-Standard V3.0):**
> - **① „ASP Standard"**: Hauptschalter (`019`), ÜSS mit Fernmeldung (`033`),
>   Phasenüberwachung (`034`/`035`, automatisch nach Projekt-Netztyp),
>   Phasenkontrollleuchten (`020`), Störquittiertaster mit Sammelstörungsleuchte
>   (`021`) – **plus NEU Schaltschrank-Innenleuchte (`480_000036`, s.u.)**.
>   Bewusst OHNE generische Betriebs-/Störmeldeleuchte (`028`–`031`) – die
>   kommt erst mit einer konkreten Fach-Anlage dazu (Default dann
>   DDC-Ansteuerung).
> - **② „ASP mit Bedienpanel"**: ① + TouchPanel (`015` klein/`016` groß,
>   echte Auswahl) + UMG96 (`012`/`013`/`014`, Protokollauswahl zwingend) als
>   fester Bestandteil. Reiner Größen-/Komplexitäts-Tier, unabhängig von
>   Nutzungstyp/Verfügbarkeit.
> - **④ „ASP Krankenhaus/Labor/Rechenzentrum – hohe Verfügbarkeit"**: ④a = ②
>   + USV (`011`), sofort umsetzbar. ④b (externe USV = Doppeleinspeisung)
>   zurückgestellt – **Doppeleinspeisung ist strukturell NICHT vorgesehen**
>   (Feldtyp C in `FELDPLAN` ist `repeat:false`, Code-Kommentar bestätigt „es
>   gibt nur EINE Netzeinspeisung pro Anlage"), bräuchte einen neuen
>   Modul-3-Schalter, der `uss`/`klemm_e` innerhalb desselben Feldes verdoppelt
>   (funktioniert dann auch im Wandschrank) – eigener Folgeschritt, inkl.
>   Fachfrage ob eine Netzumschalt-/Verriegelungseinrichtung nötig ist.
> - Alte „③ Krankenhaus/Labor" entfällt als eigener Vorschlag (Inhalt jetzt in
>   ②/④ verteilt). Not-Halt (`032`) und die Doppel-CPU bleiben frei wählbare
>   Einzelentscheidungen, keiner Anlage fest zugeordnet.
> - Platzbedarf je Anlage wurde je Zone anhand echter `b_mm`/`h_mm`-Summen
>   berechnet (nicht grob geschätzt, Nutzer-Vorgabe) – Details in
>   `scratchpad/anlage_automation_fork_ergebnis.md`.
> - **Bekannte Lücke:** Tür-Kollisionsprüfung ist bisher nur als gezielter
>   Einzelfall-Filter vorhanden (`tuerTouchpanelPasstAufTuer()`, Session 64),
>   kein generischer Check für ein komplettes Anlagen-Bündel auf beliebigen
>   Schrankgrößen – muss für Schritt 3 erweitert werden (Prüfung des GESAMTEN
>   Bündels gegen die echten Türmaße, nicht nur TouchPanel isoliert).
> **NEU `480_000036` „Schaltschrank-Innenleuchte mit Servicesteckdose, FI Typ
> B + LSS mit Hilfskontakten, Magnetmontage, 230V AC"** (Kategorie neu:
> „Beleuchtung", `bauteil_typ` neu: `innenleuchte`): Phoenix Contact PLD E 608
> W 315/F (`2702226`, 685lm/9,8W LED, Schuko bis 16A, IP20, Schutzklasse I,
> Bewegungsmelder integriert) + Magnet-Set (`2702315`) + Anschlusskabel
> (`2702302`), alle `keine_platzierung_mp:true` (magnetisch an der
> Gehäuseoberkante, kein Montageplattenbedarf). Fork-Recherche (Rittal/Phoenix/
> Siemens/weitere geprüft): **keine** Leuchte+Steckdose+FI-Kombi am Markt
> existent – Phoenix Contact gewählt (etabliertes Fabrikat für Steckdosen).
> **Wichtiger Normen-Fund:** der bereits katalogisierte FI `5SV3321-4` ist ein
> reiner FI (RCD), **kein** FI/LS-Kombigerät – bietet keinen
> Überlast-/Kurzschlussschutz (VDE-0100-430-Lücke), betraf auch die
> bestehende `480_000018`. Siemens führt **keinen** Typ-B-FI/LS-Kombischalter
> (komplette 5SU1-Baureihe nur Typ A, Original-Bestellauswahlhilfe SIEP-T10061
> geprüft) – Fabrikatsabweichung zu Doepke (`DRCBO 4 B16/0,03/1N-B SK`,
> `09949104`, echter 1P+N-Typ-B-RCBO) wurde dem Nutzer vorgeschlagen, aber
> **explizit abgelehnt** – Nutzer-Vorgabe: bei Siemens/Typ B bleiben, FI
> (`5SV3321-4`) + LSS (`5SL6116-6`, 1-polig B16A, bereits katalogisiert) als
> zwei getrennte Bauteile. **Modellierung Ruhestromkette (neu, wiederverwendbar
> für ähnliche Fälle):** beide Schutzorgane bekommen je einen Hilfsschalter
> (`5ST3010`), BEIDE Öffnerkontakte in Reihe auf denselben DDC-Eingang – nur
> EIN `dp_bi:1`-Override (auf der ersten Hilfsschalter-Zeile), die zweite
> Hilfsschalter-Zeile trägt bewusst KEIN dp – Auslösung von FI ODER LSS meldet
> zuverlässig einen Ausfall, ohne die Datenpunktzahl zu erhöhen. Gleiche
> Korrektur (LSS `5SL6116-6` + 2. Hilfsschalter, Ruhestromkette) rückwirkend
> auch auf `480_000018` angewendet (schließt dieselbe Normenlücke dort).
> **Export:** einzelbauteile 218→**221** (`2702226`/`2702315`/`2702302`),
> baugruppen 181→**182** (`480_000036` neu, `480_000018` bearbeitet),
> feldgeraete unverändert 96. Backup:
> `ga_komponenten_vor-innenleuchte-fi-ls_20260927_*.xlsx`. Browser-Verifikation
> (Standschrank, beide Baugruppen gleichzeitig platziert): vollständiger
> Katalog-Scan (Regel 7) 0 verwaiste Referenzen, Stückliste zeigt korrekt 4×
> Hilfsschalter/2×FI/2×LSS/1×Leuchte/1×Magnet-Set/1×Kabel, `ddcSummary` bestätigt
> exakt `dp_bi.used:2` (1 je Baugruppe trotz je 2 Hilfsschaltern), keine
> Konsolenfehler.
> **Restliste:** keine Preise für `2702226`/`2702315`/`2702302` gefunden
> (Distributoranfrage nötig); Doppeleinspeisung (④b) strukturell offen (s.o.);
> Schritt 3 (Anlagen-Engine: `anlagen`/`anlagen_baugruppen`-Sheets,
> `addAnlage()`, Tür-Bündel-Kollisionsprüfung) noch nicht begonnen; „Wartungs-
> meldeleuchte gelb" (aus Fork-Recherche) auf Nutzer-Wunsch bewusst NICHT
> umgesetzt (individuelle Nachrüstentscheidung). Rohdaten in
> `scratchpad/anlage_automation_fork_ergebnis.md`,
> `scratchpad/innenbeleuchtung_fork_ergebnis.md`,
> `scratchpad/fi_ls_kombi_fork_ergebnis.md`.
>
> **Nachtrag Session 67 – Schritt 3 umgesetzt: Anlagen-Engine fertig,
> Standard-Anlage korrigiert, hohe-Verfügbarkeit-Anlage umbenannt:**
> Nutzer-Korrektur vor Schritt 3: `480_000018` (Hutschienensteckdose)
> entfällt aus „ASP Standard" – die Innenleuchte (`480_000036`) bringt
> bereits eine Servicesteckdose mit, eine zweite ist im Standard unnötig
> (bleibt als eigenständige Baugruppe im Katalog wählbar). ④a umbenannt zu
> „ASP Labor/Rechenzentrum/Krankenhaus – hohe Verfügbarkeit" (Reihenfolge).
> **Neue Excel-Sheets `anlagen` (id/name/gewerk/beschreibung/
> funktionsbereich/kategorie) + `anlagen_baugruppen`
> (anlage_id/bg_id/menge/`gruppe`/`variante_label`/`ist_default`/
> `netztyp_bindung`)** – Join-Muster identisch zu `baugruppen`/
> `baugruppen_bauteile`, `xlsx_to_json.py` um `export_anlagen()` erweitert
> → `data/anlagen.json` (3 Anlagen: `480_A00001`/`A00002`/`A00003`, IDs mit
> „_A"-Marker statt „_0" um Anlagen von Baugruppen zu unterscheiden).
> **Modul 4 (`modul-04-innenaufbau/index.html`):** `ANLAGEN_DB` per fetch
> geladen; `filterBaugruppen()` verzweigt bei `gew.endsWith('_anlagen')` in
> neue `populateAnlagenAuswahl()` (identisches `#bg_auswahl`-Element,
> Options-Value-Präfix `anlage:<id>` unterscheidet von normalen `bg_id`s);
> `updateAnlageVariantenUI()` rendert je `gruppe` aus `mitglieder` ein
> `<select>` (neuer Container `#anlage_varianten`) – TouchPanel-Optionen
> laufen dabei durch die bereits bestehende `tuerTouchpanelPasstAufTuer()`,
> damit auf zu kurzen Türen weiterhin nur die kleine Variante erscheint
> (kein neuer Kollisions-Code nötig, bestehende Prüfung wiederverwendet);
> `addBaugruppe()` verzweigt bei `anlage:`-Präfix in neues `addAnlage()`,
> das jedes Mitglied auflöst (fix immer / `netztyp_bindung` nach
> `m03_zone_netztyp`, automatisch / `gruppe` nach Nutzerwahl im Select) und
> über die aus `addBaugruppe()` extrahierte `addBaugruppeById()` in die
> normale Belegung schreibt – **keine Verschachtelung**, `belegung` bleibt
> nach dem Hinzufügen einer Anlage von manuell einzeln hinzugefügten
> Baugruppen ununterscheidbar (Architektur-Entscheidung Session 64
> bestätigt funktionsfähig).
> **Browser-Verifikation:** ② mit Drehstrom+Default-Varianten →
> `480_000034` (nicht 035) + `480_000015`+`480_000012`, kein `480_000018`;
> ② mit Wechselstrom+großem Panel+M-Bus manuell gewählt → korrekt
> `480_000035`+`480_000016`+`480_000013`; ④a → zusätzlich `480_000011`
> (USV); vollständiger Katalog-Scan 0 verwaiste Referenzen; Tür-Ansicht +
> Stückliste rendern korrekt (1200×2000-Standschrank, Drehstrom, Schiene
> 3-polig); keine Konsolenfehler.
> **Restliste:** ④b (Doppeleinspeisung) weiterhin zurückgestellt; die
> Tür-Bündel-Kollisionsprüfung bleibt auf den TouchPanel-Einzelfall
> beschränkt (kein genereller Check für beliebige Bündel-Kombinationen auf
> beliebigen Schrankgrößen); `removeBaugruppeQty()` kennt Anlagen nicht
> (Minus-Klick auf eine gewählte Anlage tut nichts – Mitglieder werden
> stattdessen einzeln über die Belegungsliste entfernt, konsistent mit der
> bestehenden „kein Korrektur-Komfort"-Philosophie).

> **Sitzungsstand Session 66 (14.09.2026) – Weitere Automation-Baugruppen:
> Wischrelais-Ergänzung, FI-Typ-B-Korrektur, ÜSS-Zuleitung + 2× Phasen-/
> Spannungsüberwachung:**
> Vier Recherche-Themen (3 Hintergrund-Forks + 1 direkte Ergänzung),
> alle Original-Datenblätter (Siemens TEDatasheet-API, Dehn-PDFs) geprüft.
> **Nützlicher Fund für künftige Siemens-Recherchen:** `format=pdf&caller=SIOS`
> (statt `format=html`) an der TEDatasheet-API liefert zuverlässig das
> Original-PDF, danach lokal mit `pdftotext -layout`
> (`C:\Program Files\Git\mingw64\bin\pdftotext.exe`) auslesen – deutlich
> zuverlässiger als der WebFetch-eigene PDF-Zusammenfasser, der an
> Siemens-PDFs regelmäßig scheitert.
> 1. **`480_000021` (Störquittiertaster mit Sammelstörungsleuchte) ergänzt**
>    um `RE22R2HMR` (Zelio-Time-Wischrelais, bereits katalogisiert) – für
>    Netzausfall-Erkennung, löst ebenfalls eine Störquittierung aus. Nutzer-
>    Vorgabe: „nur als Bauteil hinzufügen" – keine zusätzliche DP-Zeile,
>    Zone `leist` (Katalog-Default).
> 2. **`480_000018` (Schaltschranksteckdose) korrigiert:** LSS `5SL6110-6`
>    entfernt, ersetzt durch NEU `5SV3321-4` (Siemens SENTRON 5SV3,
>    2-polig/1P+N, **Typ B**, 16A/30mA, SIGRES, 4TE, 90×72×70mm) – Nutzer-
>    Vorgabe: „heute Pflicht" für Schutzkontaktsteckdosen. Wichtiger
>    Recherche-Befund (widerlegt Ausgangsannahme): Siemens führt sehr wohl
>    2-polige Typ-B-FIs in der bereits katalogisierten SENTRON-5SV3-Familie
>    – **keine Planungsfabrikat-Abweichung nötig**. Hilfsschalter `5ST3010`
>    bleibt unverändert (laut Session-63-Recherche bereits explizit auch für
>    5SV3-FIs geeignet), DP unverändert 1×BI.
> 3. **NEU `480_000033` „Überspannungsschutz Schaltschrankzuleitung mit
>    Fernmeldung":** `5SG1812` (Sicherungssockel D03, bereits katalogisiert,
>    Vorsicherung) + NEU **`952305`** (DEHNguard M TNC 275 **FM**, NICHT
>    `952300`!) in Zone `uss`. Wichtiger Recherche-Befund: `952300` hat
>    **keine** nachrüstbare Fernmeldefunktion und **kein** steckbares
>    Zubehör dafür – die Fernmeldevariante ist eine komplett eigenständige
>    Bestellvariante mit eigener Artikelnummer, gleiche Maße (3TE,
>    54×90×66mm), kein Mehrplatzbedarf. 1×BI auf der `952305`-Zeile
>    (potentialfreier Wechsler, kein Koppelrelais nötig, Regel 12).
> 4. **NEU `480_000034` „Phasenüberwachung 400V AC (3~) mit
>    Störmeldekontakt":** `3UG5616-1CR20` (Siemens SIRIUS 3UG5, aktuelle
>    Generation, digital einstellbar, Phasenfolge/-ausfall/Asymmetrie/
>    Frequenz/Über-Unterspannung, 2 potentialfreie Wechsler, 3×90-760V AC
>    eigenversorgt, 22,5×100×90mm). Zone `leist` (Nutzer-Vorgabe „Zone
>    Leitung"). 1×BI Phasenausfall (Ruhestromprinzip, kein Koppelrelais).
>    Alternative geprüft, nicht gewählt: `3UG4616-1CR20` (Vorgänger-
>    generation, 178,59€ netto bestätigt, aber bei einem Distributor als
>    Auslaufprodukt markiert) – Nutzer hat sich für die aktuelle Generation
>    entschieden, Preis bleibt dafür offen.
> 5. **NEU `480_000035` „Phasenüberwachung 230V AC (1~) mit
>    Störmeldekontakt":** `3UG4631-1AW30` (Siemens SIRIUS 3UG4, 1
>    potentialfreier Wechsler, Über-/Unterspannung inkl. Netzausfall,
>    24-240V AC/DC eigenversorgt, 22,5×92×91mm, 231€ netto RS Online).
>    Funktional ein Spannungsüberwachungsrelais (1~ kennt keine
>    Phasenfolge), vom Nutzer aber als „Phasenüberwachung 230V AC" benannt.
>    Zone `leist`. 1×BI.
> **Browser-Verifikation:** alle 5 Baugruppen gleichzeitig platziert
> (`buildQueues()` direkt geprüft) – alle Artikel lösen auf, `480_000018`
> zeigt jetzt `5SV3321-4` statt `5SL6110-6`, `480_000021` zeigt zusätzlich
> `RE22R2HMR`, BI 5/16 · BO 1/6 exakt wie von Hand berechnet, vollständiger
> Katalog-Scan (Regel 7) bestätigt 0 verwaiste Artikelreferenzen, keine
> Konsolenfehler.
> **Export:** einzelbauteile 214→**218** (4 neu: `952305`, `5SV3321-4`,
> `3UG5616-1CR20`, `3UG4631-1AW30`), baugruppen 178→**181** (3 neu, 2
> bearbeitet), feldgeraete unverändert 96.
> **Restliste (Nutzer-Vorgabe „Preise können wir später recherchieren"):**
> keiner der 4 neuen Artikel hat einen bestätigten Herstellerlistenpreis –
> nur Distributor-Näherungen im `quelle_hinweis` vermerkt (`952305`
> ~142€, `5SV3321-4` ~185-200€, `3UG4631-1AW30` 231€ RS Online) bzw. für
> `3UG5616-1CR20` gar kein belastbarer Wert gefunden. Bei Bedarf später
> gezielt nachrecherchieren. Neuer `bauteil_typ` `phasenwaechter` (für
> `3UG5616-1CR20`/`3UG4631-1AW30`) – noch kein eigenes Kurzlabel in
> `kurzLabel()` hinterlegt (fällt auf Bezeichnungs-Fallback zurück, kein
> Fehler, nur optisch weniger prägnant).

> **Sitzungsstand Session 65 (13.09.2026) – Erste 14 ASP-Grundausstattungs-
> Baugruppen (Automation) für die geplante Anlagen-Funktion + wichtiger
> Bugfix physische DP auf Tür-Bauteilen:**
> Vorarbeit für die erste Anlage „ASP · Schaltschranktür" (Nutzer-Vorgabe:
> „Wir starten mit Automation... die Grundausstattung des ASP in mehreren
> Varianten"). Alle 14 Baugruppen sitzen komplett auf der Schaltschranktür
> DESSELBEN Schranks wie die DDC – Nutzer-Vorgabe ausdrücklich „Es werden
> keine Klemmen benötigt, weil sich alles im Schaltschrank abspielt" →
> durchgängig Regel 12 (schrankintern, DP-Override direkt auf der
> Bauteilzeile, keine `3209510`-Klemme), `zone:'tuer'`.
> **Neue Baugruppen** `480_000019`–`480_000032`, Gewerk 480, Kategorien
> „Fronttafel-/Türeinbau" (8) und neu „Handschalter" (6):
> - `019` Hauptschalter mit Stellungsmeldung: `3LD2504-0TK51` + NEU
>   `3LD9200-5B` (Hilfsschalter 1Ö+1S, Original-Siemens-Bestellauswahlhilfe
>   SIEP-T10353 – einzige für Frontbefestigung erhältliche Variante,
>   `3LD9200-6C` nur für Bodenbefestigung). 2×BI (Ein/Aus, ein Bauteil
>   liefert beide Kontakte).
> - `020` Phasenkontrollleuchten 3× weiß + Einzelsicherung: 3×
>   `3SU1102-6AA60-3AA0` + 3× `5SL6106-6` (bereits katalogisierter LSS,
>   bewusst OHNE `5ST3010`-Hilfsschalter – Nutzer-Vorgabe „nimm die normale
>   Sicherung, das wird in der Praxis auch so gemacht", kein Meldekontakt
>   nötig da kein DP). 0 Datenpunkte.
> - `021` Störquittiertaster mit Sammelstörungsleuchte: `3SU1152-0AB50-1BA0`
>   (1×BI Quittierung) + `3SU1102-6AA20-3AA0` (1×BO Sammelstörung).
> - `022`/`024`/`027` Handschalter Aus-Ein-Auto/Aus-Stufe1-Stufe2/
>   Zu-Auf-Auto (je 3-stufig, `3SU1100-2BL60-3NA0` wiederverwendet – bereits
>   real vermessener Tür-Wahlschalter aus Session 64, 32,3mm): je 2×BI.
> - `023`/`026` Handschalter Hand-Auto/Zu-Auf (je 2-stufig, NEU
>   `3SU1100-2BF60-3BA0` als Tür-Einzelbauteil angelegt – Artikel bereits
>   als Elektro-Feldgerät `440_000027`/`030` bekannt [Session 63], dort ohne
>   Abmessungen; hier b_mm/h_mm 32,3mm vom 3-stufigen Familienmitglied
>   übernommen, nicht separat vermessen): je 1×BI.
> - `025` Handschalter Aus-Stufe1-Stufe2-Auto (4-stufig, NEU
>   `3SU1100-4-UNVERIFIZIERT` als Tür-Einzelbauteil – wie Elektro-Pendant
>   `440_000029` weiterhin keine fertige SIRIUS-ACT-Einheit gefunden): 3×BI.
> - `028`/`030` Betriebsmeldeleuchte grün / Störmeldeleuchte rot, **über
>   Schaltschranksteuerung** (Nutzer-Korrektur: nicht „ohne DDC-Anbindung"
>   nennen): nur die bloße Leuchte, 0 DP – Ansteuerung erfolgt über eine zum
>   Auswahlzeitpunkt noch unbekannte Betriebsmittel-Baugruppe; „DBACS baut
>   keine Schaltung, sondern erfasst Platzbedarf und Bauteile" (Nutzer-
>   Zitat), daher irrelevant welcher Kontakt später tatsächlich schaltet.
> - `029`/`031` Betriebsmeldeleuchte grün / Störmeldeleuchte rot, DDC-
>   Ansteuerung (BO): gleiche Leuchte, 1×BO (TXM1.6R liefert 24V AC/DC
>   direkt, kein Koppelrelais nötig).
> - `032` Not-Halt mit Auslösemeldung: `3SU1100-1HB20-1CH0` (hat bereits 1Ö
>   lt. Katalog), 1×BI.
> **3-Stellungen-Frage (Nutzer-Rückfrage, geklärt):** ein 3-stufiger SIRIUS-
> ACT-Wahlschalter („komplette Einheit") hat nur 2 physische Kontakte – die
> Nullstellung ergibt sich aus „kein Kontakt aktiv" (Siemens-Bauart, bereits
> in Session 63 am Datenblatt verifiziert), daher `Kontaktzahl =
> Schaltstellungen − 1`. Die 3. Stellung wird DDC-seitig aus „kein Kontakt
> aktiv" hergeleitet (virtueller Software-Punkt) – Nutzer bestätigt „das ist
> Siemens-spezifisch und i.O.", keine Katalogänderung nötig.
> **Wichtiger Bugfix in `buildQueues()` (Modul 4):** physische DP-Overrides
> (`dp_ai/ao/bi/bo`) auf Baugruppen-Bauteilen mit `zone:'tuer'` wurden
> bisher **komplett verworfen**, weil die Zeile
> `accumulateDp(dpQuelle, bt.menge)` NACH dem Guard `if(!queues[zone])
> return;` stand – `'tuer'` ist keine reguläre Platzierungszone
> (`ALLE_ZONEN`/`queues`), die Zeile wurde also übersprungen, BEVOR der
> Datenpunkt gezählt wurde. Für kommunikative `dp_fb_*`-Datenpunkte war das
> bereits in Session 58 korrigiert (Zählung sitzt dort schon vor dem Guard,
> mit exakt demselben Begründungskommentar) – für **physische** `dp_bi/bo`
> fehlte dieselbe Korrektur, weil es bis zu dieser Session keine Baugruppe
> gab, die genau dieses Muster (physischer DP direkt auf einem
> Tür-Bauteil, Regel 12) tatsächlich nutzte. Fix: die komplette
> `dpUeberschrieben`/`dpQuelle`/`accumulateDp()`/`lvb_erforderlich`-Passage
> vor den `queues[zone]`-Guard verschoben (analog zur bereits davor
> stehenden Feldbus-Passage). **Fund per systematischem Test:** beim
> Verifizieren summierte sich `BI` bei mehreren gleichzeitig platzierten
> ASP-Baugruppen nicht (blieb bei „2" statt korrekt zu steigen) – isoliert
> auf `zone:'tuer'`-Bauteile eingegrenzt (der Hauptschalter-Hilfsschalter
> mit `zone:'steuer'` zählte von Anfang an richtig, alle `zone:'tuer'`-
> Bauteile nie). Nach dem Fix direkt gegen `buildQueues()` verifiziert: alle
> 14 Baugruppen gleichzeitig → BI 15/32 · BO 3/6 (exakt wie von Hand
> berechnet), Regressionscheck bestehende `dp_fb_*`-Baugruppe (`480_000012`,
> UMG-Türeinbau) weiterhin korrekt (17 kommunikative AI unverändert), keine
> Konsolenfehler.
> **Browser-Verifikation:** alle 14 Baugruppen gleichzeitig platziert,
> Türansicht zeigt korrekt 17 Bauteile (Hilfsschalter unsichtbar wie
> gewollt, `zone:'steuer'`+`keine_platzierung_mp`), Stückliste löst alle
> Artikel korrekt auf (inkl. automatisch ergänzter Steuertrafo+2×LSS für die
> DDC-CPU-Steuerspannung), keine verwaisten Referenzen, keine Konsolenfehler.
> **Export:** einzelbauteile 211→**214** (3 neu: `3LD9200-5B`,
> `3SU1100-2BF60-3BA0`, `3SU1100-4-UNVERIFIZIERT`), baugruppen 164→**178**
> (14 neu), feldgeraete unverändert 96. Kein Backup nötig (keine
> strukturelle Änderung, nur neue Zeilen).
> **Restliste:** `3LD9200-5B`-Preis nur Distributor-Richtwert (11,54€ netto,
> Elektro4000.de), kein Siemens-Listenpreis; Abmessungen `3LD9200-5B` vom
> Schwestertyp `-5C` übernommen; `3SU1100-2BF60-3BA0`/`3SU1100-4-
> UNVERIFIZIERT` Tür-Abmessungen (32,3mm) vom 3-stufigen Familienmitglied
> übernommen, nicht einzeln vermessen; kein Preis für die beiden neuen
> Wahlschalter-Varianten recherchiert; 4-stufiger Wahlschalter weiterhin
> ohne verifizierte Hardware. **Nächster Schritt (Nutzer-Ankündigung):**
> Baugruppennamen-Konvention für Anlagen nochmal besprechen (Grundbauteile,
> die immer dazugehören, sollen NICHT im Auswahltext auftauchen, aber für
> Claude nachvollziehbar bleiben) – noch keine Entscheidung getroffen, ob
> dafür ein neues Stammdatenpflege-Modul (analog Modul 7) für Anlagen
> gebaut wird oder ob es bei einmaliger Erstellung durch Claude + späteren
> Anpassungen auf Zuruf bleibt.

> **Sitzungsstand Session 64 Nachtrag 6 (13.09.2026) – Quittiertaster bekommt
> eigenes Band, Störmeldung/Betriebsmeldung-Steg halbiert, Messgerät/
> Touchpanel-Restpunkt bestätigt unlösbar auf kleiner Tür:**
> Nutzer-Review per Browser-Screenshot (Wandschrank) ergab: die "rote Reihe"
> unter der grünen war durch die eingemischten blauen Quittiertaster-Kacheln
> nicht rein rot – Nachtrag-5-Entscheidung (Störmeldung+Quittiertaster
> teilen sich ein Band) war ein Fehlgriff. Nutzer-Korrektur: **Quittiertaster
> bekommt eine eigene, exklusive Ebene zwischen Phasenleuchten und Not-Halt**
> (nicht mehr im Störmeldung-Band). Störmeldung bleibt unverändert bei 0,53,
> jetzt aber ALLEIN, direkt unter Betriebsmeldung. Um Platz für die neue
> Zwischenebene zu schaffen, sind Hauptschalter (0,30→**0,25**) und
> Phasenleuchten (0,41→**0,355**) nach unten gerutscht (Nutzer-Hinweis:
> "Phasenleuchten können noch tiefer gesetzt werden, wenn der Platz benötigt
> wird" – reichlich Freiraum zwischen Hauptschalter und Türunterkante
> vorhanden). Neue Konstante `TUER_BAND_QUITTIERTASTER = 0.41` (eigenständig,
> nicht mehr Alias von `TUER_BAND_STOERMELDUNG`).
> **Zusätzlich** auf Nutzer-Vorgabe der Mindest-Steg zwischen Störmeldung
> (rot) und Betriebsmeldung (grün) halbiert (Nutzer: "können auch mit der
> Hälfte des aktuellen Abstands gesetzt werden, weil sie funktional
> zusammengehören") – 12mm-Standard-Steg → **6mm** nur für dieses Paar,
> `TUER_BAND_BETRIEBSMELDUNG` 0,585→**0,577** (Störmeldung-Band selbst
> unverändert). Physischer Kollisionsschutz bleibt gewahrt (36,75mm nötig,
> 37,6mm tatsächlich auf dem bindenden 800mm-Wandschrank).
> **Browser-Verifikation** (direkte SVG-Rect-Kollisionsprüfung, alle 9
> Türbauteile gleichzeitig auf BEIDEN Referenztüren): Standschrank 1200×2000
> weiterhin 0 Überlappungen; Wandschrank 800×800 weiterhin NUR die eine
> bereits dokumentierte Randkombination (Messgerät UMG96 + Touchpanel PXM50
> gleichzeitig, 96mm Überlappung, unverändert). Neue Bandreihenfolge korrekt
> unten→oben: Hauptschalter(0,25) < Phasenleuchten(0,355) <
> Quittiertaster(0,41) < Not-Halt(0,47) < Störmeldung(0,53) <
> Betriebsmeldung(0,577) < Handschalter(0,64) < Messgerät(0,74) <
> Touchpanel(0,85). Keine Konsolenfehler.
> **Rechnerisch bestätigt (Nutzer-Anfrage "prüfe die Abstandsregel Messgerät/
> Touchpanel"): der Messgerät→Touchpanel-PXM50-Restpunkt auf dem 800mm-
> Wandschrank ist mit dem Prozentband-Ansatz NICHT lösbar, unabhängig davon
> wie stark andere Bänder gestaucht werden.** Rechnung: benötigter Abstand
> für 22mm-Steg = 48+135+22 = 205mm; selbst wenn ALLE 6 Stege zwischen
> Hauptschalter und Handschalter auf 0mm gesetzt würden, wären nur ca. 85mm
> zusätzlicher Spielraum gewinnbar (real gemessen: 84,8mm Summe aller
> aktuellen Kanten-Lücken) – bei weitem nicht genug, und ein Verschieben
> von Messgerät/Handschalter nach unten würde zudem entweder die Reihenfolge
> Handschalter<Messgerät<Touchpanel verletzen oder Touchpanels fixierte
> Kopfhöhe (0,85 = 1700mm auf dem 2000mm-Standschrank) aufgeben.
> **Nutzer-Entscheidung zur Auflösung: statt Bänder zu stauchen, wird die
> WÄHLBARE Touchpanel-Baugröße von der Tür abhängig gemacht** (neue Funktion
> `tuerTouchpanelPasstAufTuer()`, eingehängt in `filterBaugruppen()`) – auf
> zu kurzen Türen verschwindet die große Variante (PXM50) aus dem
> Baugruppen-Dropdown, nur die kleine (PXM40) bleibt wählbar. Bewusst NICHT
> gegen das größte katalogisierte Messgerät (Worst Case) geprüft, sondern
> NUR gegen ein auf der jeweiligen Tür bereits tatsächlich platziertes
> Messgerät (`getTuerItems()`) – ein erster Versuch mit Worst-Case-Prüfung
> (gegen UMG96, 96mm) hätte auf JEDEM Wandschrank (max. 1200mm It.
> `wandschraenke.json`) auch PXM40 gesperrt, weil UMG96+PXM40 dort nie den
> 22mm-Steg schaffen – vom Nutzer als zu aggressiv abgelehnt ("nur gegen
> tatsächlich platziertes Messgerät" statt Worst-Case). Solange auf einer
> Tür (noch) kein Messgerät steht, ist die Touchpanel-Wahl frei (beide
> Varianten wählbar), unabhängig von der Türhöhe. **Bekannte Lücke:** die
> Prüfung läuft nur beim Aufbau des Baugruppen-Dropdowns (Gewerke-Tab-
> Wechsel), nicht bei jeder Belegungsänderung – wird NACH einer bereits
> getroffenen Touchpanel-Wahl noch ein zu großes Messgerät auf dieselbe Tür
> ergänzt, wird das nicht rückwirkend erkannt/verhindert (Nutzer-Vorgabe
> akzeptiert diese Lücke ausdrücklich als Kompromiss gegenüber Worst-Case).
> Browser-verifiziert (Simulation via `tuerTouchpanelPasstAufTuer()` direkt
> in der Konsole, `filterBaugruppen('automation')` fehlerfrei): kein
> Messgerät auf der Tür → beide Varianten wählbar (jede Türgröße); UMG96 auf
> 800mm- oder 1200mm-Wandschrank → beide Varianten gesperrt; UMG96 auf
> 1200×2000-Standschrank → beide weiterhin wählbar (37mm Marge, wie bereits
> in der Kollisionsprüfung oben bestätigt). Keine Konsolenfehler.

> **Sitzungsstand Session 64 Nachtrag 5 (13.09.2026) – Türband-Reihenfolge
> final korrigiert (Rot direkt unter Grün) + Mindest-Stegmaß für Blechtür-
> Ausschnitte eingeführt:**
> Nachtrag 4 hatte Störmeldung+Quittiertaster fälschlich ZWISCHEN
> Phasenleuchten und Not-Halt platziert (Fehlinterpretation der Nachtrag-3-
> Vorgabe). Nutzer-Korrektur per Browser-Screenshot: die rote Signalleuchten-
> Reihe muss direkt UNTER der grünen sitzen (keine Ebene dazwischen) – das
> war schon in der allerersten Korrekturliste so vorgegeben. Finale
> Reihenfolge unten→oben: Hauptschalter < Phasenleuchten (weiß) < Not-Halt
> (exklusiv) < Störmeldung (rot) + Quittiertaster < Betriebsmeldung (grün) <
> Handschalter < Messgerät < Touchpanel/Romutec-Ebene.
> **Neue Randbedingung (Nutzer-Hinweis, fertigungsrelevant):** die Bänder
> bestimmen auch, wo später Ausschnitte in die ~1,5mm starke Blechtür
> gefräst werden – zwischen zwei Ausschnitten muss genug Steg-Blech stehen
> bleiben (Nutzer-Fund: „Messgerät ist immer noch sehr nah am Touchpanel").
> Der bisherige 5mm-Rechenpuffer war dafür zu knapp – jetzt **12mm**
> Mindest-Steg als Standard, **22mm** für den größeren Übergang
> Messgerät→Touchpanel. Alle 7 Bandabstände (bis auf den einen bekannten
> Restpunkt) auf BEIDEN Referenztüren (800×800 Wandschrank, 1200×2000
> Standschrank) mit 1–8mm Marge auf dem bindenden Wandschrank-Fall
> verifiziert. Touchpanel/Romutec-Ebene liegt jetzt bei **exakt 1700mm**
> auf dem Standschrank (Nutzer-Ziel „ca. 1,7m Kopfhöhe" bestätigt).
> Neue Bandwerte: `TUER_BAND_NOTHALT` 0,53→**0,47**,
> `TUER_BAND_STOERMELDUNG`/`QUITTIERTASTER` 0,465→**0,53**,
> `TUER_BAND_BETRIEBSMELDUNG` 0,595→**0,585**, `TUER_BAND_HANDSCHALTER`
> 0,655→**0,64**, `TUER_BAND_MESSGERAET` 0,76→**0,74**,
> `TUER_BAND_TOUCHPANEL` 0,87→**0,85** (Hauptschalter/Phasenleuchten
> unverändert bei 0,30/0,41).
> Zusätzlich Label „Baugruppe" → **„Baugruppe · Anlage"** über der
> Baugruppen-Auswahl (Nutzer-Vorgabe: dasselbe Dropdown wird künftig für
> beides genutzt, je nach aktivem Button in der zweiten Gewerke-Reihe).
> **Browser-Verifikation:** Reihenfolge auf beiden Referenztüren korrekt
> (Touchpanel→Messgerät→Handschalter→Grün→Rot+Quittiertaster→Not-Halt→
> Weiß→Hauptschalter), Standschrank 0 Überlappungen, Wandschrank nur noch
> die eine bekannte Randkombination (Messgerät+Touchpanel PXM50
> gleichzeitig auf sehr kleiner Tür – Wahlschalter überlappt jetzt NICHT
> mehr, da der größere Steg auch dort mehr Abstand erzwingt). Keine
> Konsolenfehler.

> **Sitzungsstand Session 64 Nachtrag 4 (13.09.2026) – Türband-Reihenfolge
> final korrigiert + 2 weitere Bohrung-statt-Bauteil-Katalogfehler:**
> Nutzer-Review per Browser-Screenshot ergab zwei strukturelle Korrekturen
> an der Session-64-Bandreihenfolge:
> 1. **Störmeldung (rot) + Quittiertaster** sitzen jetzt zwischen
>    Phasenleuchten und Not-Halt (vorher darüber).
> 2. **Handschalter und Messgerät sind wieder getrennte Bänder** – der
>    Nachtrag-3-Versuch, beide ein Band teilen zu lassen, war ein
>    Fehlgriff (Nutzer-Fund: "Schalter sind mit in der Ebene, benötigen
>    aber eine eigene").
> Finale Reihenfolge unten→oben: Hauptschalter < Phasenleuchten <
> Störmeldung+Quittiertaster < Not-Halt < Betriebsmeldung < Handschalter <
> Messgerät < Touchpanel/Romutec-Ebene.
> **2 weitere Katalogkorrekturen** (gleiches Bohrung-statt-Bauteil-Muster
> wie zuvor bei Not-Halt/Signalleuchten, Original-Siemens-Datenblätter
> direkt gelesen): Handschalter (Wahlschalter `3SU1100-2BL60-3NA0`,
> Nutzer-Fund "scheint nur die Bohrung zu sein") 22mm→**32,3mm**
> (Außendurchmesser des Betätigungselements); Quittiertaster
> (`3SU1152-0AB50-1BA0`) 22mm→**29,5mm** (gleiches Betätigungselement wie
> die Signalleuchten). Export einzelbauteile unverändert 211 (reine
> Feldänderung).
> **Bandwerte neu berechnet** (Δband ≥ (halbe Höhe unten + halbe Höhe oben +
> 5mm Puffer)/H_mm, gegen H=800mm als bindende Randbedingung geprüft, s.
> Code-Kommentar in `tuerBand()`-Block für die genauen Zahlen):
> `TUER_BAND_HAUPTSCHALTER` 0,35→**0,30**, `TUER_BAND_PHASENKONTROLLE`
> 0,48→**0,41** (Nutzer-Vorgabe: möglichst nah an Hauptschalter, siehe
> Restpunkt unten), `TUER_BAND_STOERMELDUNG`/`QUITTIERTASTER` 0,62→**0,465**,
> `TUER_BAND_NOTHALT` 0,55→**0,53**, `TUER_BAND_BETRIEBSMELDUNG`
> 0,67→**0,595**, `TUER_BAND_HANDSCHALTER` 0,76→**0,655**,
> `TUER_BAND_MESSGERAET` (jetzt wieder eigenständig) →**0,76**,
> `TUER_BAND_TOUCHPANEL` 0,86→**0,87**. Touchpanel/Romutec-Ebene liegt damit
> bei **1740mm** auf dem 2000mm-Standschrank (Nutzer-Ziel „ca. 1,7m
> Kopfhöhe" bestätigt).
> **Restpunkt (Nutzer-Vorgabe nicht 1:1 umsetzbar):** Nutzer wollte den
> Abstand Hauptschalter→Phasenleuchten genauso groß wie den Abstand
> zwischen grüner und roter Signalleuchte – wörtlich kopiert wäre das auf
> dem 800mm-Wandschrank zu wenig für den 90×106mm großen Hauptschalter
> (bräuchte 72,8mm, ein 1:1 kopierter Leuchten-Abstand liefert dort nur
> ~35mm). Stattdessen der knappstmögliche Abstand gewählt, der auf BEIDEN
> Referenztüren nicht überlappt.
> **Browser-Verifikation:** alle 9 Türbauteile (Hauptschalter, 3×
> Signalleuchte, Not-Halt, Quittiertaster, Handschalter, Messgerät,
> Touchpanel PXM50) gleichzeitig auf BEIDEN Referenztüren geprüft
> (direkte SVG-Rect-Kollisionsprüfung) – 800×800 Wandschrank: 0
> Überlappungen außer der bereits dokumentierten Randkombination
> (Messgerät/Handschalter + Touchpanel PXM50 gleichzeitig auf einer sehr
> kleinen Tür); 1200×2000 Standschrank: 0 Überlappungen. Reihenfolge von
> oben nach unten im Browser bestätigt (Touchpanel → Messgerät →
> Handschalter → Betriebsmeldung → Not-Halt → Störmeldung+Quittiertaster →
> Phasenleuchten → Hauptschalter). Keine Konsolenfehler.

> **Sitzungsstand Session 64 Nachtrag 3 (13.09.2026) – Touchpanel-Kopfhöhe
> tatsächlich korrigiert (Nutzer-Fund: "Touchpanel ist immer noch oben"):**
> Die Session-64-Bandumsortierung hatte nur die REIHENFOLGE der übrigen
> Bänder korrigiert – `TUER_BAND_TOUCHPANEL` selbst blieb bei 0,93 (1860mm
> auf dem 2000mm-Standschrank), die ursprüngliche Beschwerde ("muss in etwa
> Kopfhöhe sein") war damit nie tatsächlich behoben. Fix: Handschalter und
> Messgerät teilen sich jetzt bewusst dasselbe Band (0,76, nebeneinander in
> einer Reihe, wie schon Störmeldung+Quittiertaster) – spart eine Ebene in
> der Abstandskette und erlaubt dem Touchpanel-Band, auf **0,86** zu sinken
> (1720mm statt 1860mm auf dem 2000mm-Standschrank – spürbar näher an
> realistischer Kopf-/Augenhöhe). Nachgerechnet und per Browser-Test auf
> BEIDEN Referenzschränken (800×800 Wandschrank, 1200×2000 Standschrank)
> verifiziert: 0 Überlappungen auf dem Standschrank, auf dem Wandschrank nur
> die bereits dokumentierte Randkombination (Messgerät/Handschalter +
> Touchpanel PXM50 gleichzeitig auf einer sehr kleinen Tür).
> **Zusätzlicher Bugfix in `buildTuerAnsicht()`** (beim Verifizieren
> gefunden): die Row-Layout-Cursor-Fortschaltung rechnete mit dem realen
> `b_mm`, während die Zeichenbreite auf mind. 3px hochgeklemmt wird – bei
> einem sehr kleinen Bauteil (Handschalter 22mm) neben einem sehr großen
> (Messgerät 96mm) im selben Band reichte die reale Lücke dann nicht mehr
> aus, minimale Überlappung. Fix: Cursor-Fortschaltung nutzt jetzt dieselbe
> effektive (geklemmte) Breite wie die Zeichnung (`effW()`-Helper) – betrifft
> alle Mehrfach-Bauteil-Bänder, nicht nur diesen Fall. Keine Konsolenfehler.

> **Sitzungsstand Session 64 (13.09.2026) – Türbänder neu sortiert +
> Pilztaster-/Signalleuchten-Maßkorrektur + Bandwerte kollisionssicher
> nachgerechnet:**
> 1. **Türband-Reihenfolge neu** (Nutzer-Korrektur: Touchpanel-Position war
>    nicht ergonomisch – "muss vom Menschen bedient werden, sollte in
>    Kopfhöhe sein"): neue Reihenfolge unten→oben in `modul-04-innenaufbau/
>    index.html` (`tuerBand()`): Hauptschalter < Phasenleuchten (weiß) <
>    Not-Halt (exklusiv, jetzt direkt über den Phasenleuchten statt oben
>    beim Handschalter) < Sammelstörmeldeleuchte (rot) + Quittiertaster
>    (gemeinsames Band – Quittierung gehört funktional zur Störmeldung) <
>    Betriebsmeldeleuchte (grün, weiterhin eigene Reihe, NICHT mit der
>    Störmeldung zusammengelegt – ausdrückliche Nutzer-Vorgabe) < Handschalter
>    < Messgeräte < Touchpanel/künftige Romutec-LVB-Ebene (oberste, exklusive
>    Ebene, Kopfhöhe – beide sollen später auf derselben Ebene sitzen).
> 2. **Katalogkorrektur Not-Halt + 3 Signalleuchten** (Nutzer-Fund: „Pilztaster
>    zu klein dargestellt"): `b_mm`/`h_mm` waren bei allen vier SIRIUS-ACT-
>    22mm-Bauteilen nur der Einbaudurchmesser/Bohrung (22mm), nicht das reale
>    Bauteil. Original-Siemens-Datenblätter direkt gelesen (PDF, nicht der
>    Web-Zusammenfasser – der scheitert an Siemens-PDFs zuverlässig):
>    `3SU1100-1HB20-1CH0` Not-Halt-Pilzdrucktaster → **40×40mm**
>    („Außendurchmesser des Betätigungselements", OHNE das gelbe
>    Unterlegschild-Warnschild Ø75mm – Nutzer-Vorgabe: Schilder zählen nicht
>    zum Platzbedarf); `3SU1102-6AA20/-6AA40/-6AA60-3AA0` (rot/grün/weiß
>    Signalleuchten) → je **29,5×29,5mm** (alle drei unabhängig am
>    Originaldatenblatt bestätigt, identisches Betätigungselement, nur
>    LED-Farbe unterschiedlich). Backup nicht nötig (reine Feldänderung, kein
>    Strukturwechsel). Export unverändert **einzelbauteile 202** (nur Werte
>    geändert). Restliste: dasselbe Muster (Katalogwert = Bohrung statt
>    Bauteilmaß) vermutlich auch bei Quittiertaster/Wahlschalter – noch nicht
>    geprüft.
> 3. **Bandwerte kollisionssicher nachgerechnet** (Browser-Test deckte durch
>    die Maßkorrektur zwei echte Überlappungen auf): auf dem 1200×2000-
>    Standschrank überlappten sich Messgerät (UMG96, 96×96mm) und Touchpanel
>    PXM50 (419×270mm) – Bandabstand 0,08×2000mm=160mm, gebraucht 96/2+270/2
>    =183mm. Auf dem 800×800-Wandschrank überlappten sich zusätzlich
>    Störmeldung/Betriebsmeldung/Handschalter (Bandabstand 0,03×800mm=24mm
>    Pitch, gebraucht 29,5mm für zwei gleich hohe Leuchten). Nutzer-Vorgabe:
>    Hauptschalter darf weiter nach unten rücken, um der oberen Gruppe Raum
>    zu verschaffen – alle Bänder gegen die realen Katalogmaße (größte real
>    verwendete Variante je Typ) mit Sicherheitsmarge neu bemessen:
>    `TUER_BAND_HAUPTSCHALTER` 0,40→**0,35**, `TUER_BAND_BETRIEBSMELDUNG`
>    0,65→**0,67**, `TUER_BAND_HANDSCHALTER` 0,68→**0,715**,
>    `TUER_BAND_MESSGERAET` 0,85→**0,83** (Phasenkontrolle/Not-Halt/
>    Störmeldung/Touchpanel unverändert). Verifiziert per direkter
>    SVG-Rect-Kollisionsprüfung (JS, alle Paare paarweise auf Achsen-Überlappung
>    getestet) auf BEIDEN Referenzschränken (800×800 Wandschrank UND
>    1200×2000 Standschrank, je mit allen 9 Türbauteilen gleichzeitig
>    platziert: Hauptschalter, 3× Signalleuchte, Not-Halt, Quittiertaster,
>    Wahlschalter, Messgerät, Touchpanel PXM50) – auf dem Standschrank 0
>    Überlappungen, auf dem Wandschrank nur noch die eine bewusst nicht
>    abgedeckte Randkombination (siehe unten). Keine Konsolenfehler.
>    **Bewusst nicht gelöst (Restpunkt):** Messgerät + Touchpanel PXM50
>    GLEICHZEITIG auf einem sehr kleinen Wandschrank oder einem Standschrank
>    <1800mm Höhe überlappen weiterhin (reine Prozentbänder können das nicht
>    für jede Türhöhe garantieren) – laut Nutzer unrealistische Kombination
>    (Touchpanel ist auf Wandschränken „gar nicht oder nur klein vorhanden"),
>    daher zurückgestellt statt mit einer dynamischen mm-basierten
>    Mindestabstandslogik gelöst.
> **Sitzungsstand Session 64 Nachtrag (13.09.2026) – Romutec-LVB (Türeinbau)
> implementiert, `computeLvbRomutecDevices()`-Stub aufgelöst:**
> Dritte LVB-Realisierung neben DDC-Modul/Metz jetzt funktionsfähig
> (`#lvb_realisierung` Option „Türeinbau · Romutec" nicht mehr disabled).
> Recherche per 3 Hintergrund-Forks zu romutec.de (Original-Datenblätter
> direkt gelesen) + Nutzer-Korrekturen ergaben folgende Architektur:
> - **Ausgänge (AO/BO):** wie Metz – DDC-Seite bleibt normales E/A-Modul,
>   zusätzlich EIN Romutec-Gerät seriell zwischen DDC und Koppelrelais/Aktor.
>   ANDERS als Metz: kein separates Koppelrelais nötig (steckt im Modul
>   selbst), UND die Module sind mehrkanalig (nicht 1 Gerät je Punkt):
>   `RAG2020` (00003417, 4× AO 0-10V/Karte, rein analog, kein Bus) und
>   `RKS3030` (00001215, 6× BO/Karte, generisches Schaltmodul) decken den
>   aktuellen Bedarf. Aktortyp-spezifische Module `RKK2020-H0` (Klappen,
>   00001706), `RLK1010-H0` (Motor 2-stufig, 00001729), `RPK2020-H0` (Motor
>   1-stufig, 00001451) sind bereits katalogisiert, aber noch nicht in
>   `computeLvbRomutecDevices()` verdrahtet (fehlende Aktortyp-Zuordnung je
>   Baugruppen-Bauteil – eigener nächster Schritt, siehe Restliste).
> - **Eingänge (BI):** bewusst UNVERÄNDERT – bleiben immer direkt an der DDC
>   (Nutzer-Vorgabe: „wir benötigen zur Sicherstellung der Bedienfähigkeit
>   bei Ausfall der DDC eine direkt wirksame Lösung" – ein Bus wäre bei
>   DDC-Ausfall wirkungslos; zusätzlich keine Doppelverdrahtung aus
>   Sicherheitsgründen ohne galvanische Trennung). Die Positions-/Zustands-
>   anzeige der LVB-Module selbst kommt über einen **zusätzlichen, aber
>   elektrisch eigenständigen** Hilfskontakt desselben Koppelrelais/Schützes
>   (z. B. 2S+2Ö-Hilfsschalterblock) – kein Risiko, da zwei getrennte
>   Kontaktsätze statt einer Doppelverdrahtung auf einen Kontakt.
> - **Neuer Ratchet „LVB-Trägerrahmen"** (gleiches Prinzip wie DDC-/
>   Steuerspannungs-/Kommunikationsbauteil-Ratchet, sinkt nie): zählt die
>   benötigten Romutec-Kartenplätze (RAG2020+RKS3030, je nach Kanalzahl/
>   Karte), wählt den kleinsten ausreichenden Trägerrahmen (`RTR4050S`
>   00002861/6 Plätze · `RTR4084S` 00002620/10 Plätze · `RTR7050S` 00002761/
>   12 Plätze – durchgängig die abschließbare IP54-„S"-Variante, Nutzer-
>   Vorgabe „wird es meist werden") und füllt unbestückte Plätze mit
>   `RLA8000`-Leerplatten (00001223) auf.
> - **Neue Pseudo-Zone `lvb_modul`** (nicht in `ALLE_ZONEN`, nicht `tuer`):
>   die einzelnen Romutec-Module + Leerplatten brauchen keinen eigenen
>   Montageplatten-Platz UND werden nicht einzeln in der Tür gezeichnet (nur
>   der eine Trägerrahmen), erscheinen aber korrekt in der Stückliste (neuer
>   Sonderblock in `aggregateStueckliste()`, analog `letzteKommAuto`).
> - **Grafik:** Trägerrahmen wird auf der Tür als **2 verschachtelte
>   Rechtecke** gezeichnet (außen Rahmen, innen Sichthaube/Fenster, ~12%
>   Inset) – Nutzer-Vorgabe „das reicht aus, um den Platzbedarf zu
>   berücksichtigen". Teilt sich das Touchpanel-Türband (`TUER_BAND_
>   TOUCHPANEL`), beide Bauteiltypen liegen im selben Band nebeneinander
>   (bestehender Mehrfachbauteil-pro-Band-Mechanismus deckt das ab).
> **Katalog:** 9 neue `einzelbauteile` (3 Trägerrahmen + Leerplatte + 5
> Module) – **einzelbauteile 202→211**. Alle ohne `kategorie` (bewusst nicht
> manuell im Modul-4-Dropdown wählbar, nur automatisch über den Ratchet).
> Alle ohne Preis (Nutzer: „können wir später recherchieren").
> **Browser-Verifikation:** Testszenario 30× BO-Reserve + 10× AO-Reserve
> (480_000002/480_000004) bei `lvb_anforderung=gefordert`+
> `lvb_realisierung=romutec` (20% Datenpunkt-Reserve) → 4× RAG2020 + 7×
> RKS3030 = 11 Kartenplätze → korrekt `RTR7050S` (12 Plätze) + 1×
> `RLA8000` gewählt; 2 verschachtelte Rechtecke korrekt neben dem Touchpanel
> platziert, keine Überlappung (direkte SVG-Rect-Kollisionsprüfung), keine
> Konsolenfehler. Testdaten danach wieder entfernt.
> **Restliste:** Aktortyp-spezifische Zuordnung (`RKK2020-H0`/`RLK1010-H0`/
> `RPK2020-H0` statt generischem `RKS3030`) braucht ein neues Feld auf
> `baugruppen_bauteile`-Ebene, sobald konkrete Baugruppen mit Romutec-LVB
> angelegt werden – eigener nächster Schritt (Nutzer-Ankündigung). Keine
> Preise recherchiert. `RAG2020`/RKS3030/RKK.../RLK.../RPK...-Datenblätter
> haben teils nur eingebettete Grafik-Klemmenpläne (Text-Extraktion
> unvollständig) – vor echter Feldverdrahtung im Projekt Original-PDF am
> Bildschirm prüfen.

> **Sitzungsstand Session 62 (12.09.2026) – Sanitär-Baugruppen Reflex/Viega
> (Nachspeise-/Druckhaltetechnik + Hygienetechnik), erster 4-20mA-Anwendungsfall:**
> 6 neue Baugruppen `410_000001`–`410_000006` (Gewerk 410 Sanitär, neu
> angelegt – vorher leer –, `funktionsbereich` je `[sanitaer,heizung,kaelte]`
> außer der reinen Trinkwasser-Baugruppe `006` nur `[sanitaer]`), Kategorien
> „Nachspeise-/Druckhaltetechnik" (`001`–`005`) und „Hygienetechnik" (`006`).
> Alle als externe Betriebsmittel modelliert (wie Wilo-Pumpen/Schneider-CRAH),
> mit realen Reflex-/Viega-Bestellnummern (kein Platzhalter nötig, alle 6
> Artikel öffentlich verifiziert) + `feldgeraete`-Zeilen für Modul 5:
> - **`410_000001`** Reflex Fillset Compact Twist M-Bus (Art. `6811855`):
>   rein mechanisch, keine Steuerspannung. M-Bus-Wasserzähler kommunikativ
>   ausgelesen nach Session-58-Muster (`dp_fb_ai:1` auf 2. Klemme, zieht
>   `MR006`-Pegelwandler automatisch). Spannungsversorgung des M-Bus-Moduls
>   selbst NICHT im öffentlichen Datenblatt dokumentiert – als busgespeist
>   angenommen (Analogie zu `420_000029`ff.), nicht bestätigt.
> - **`410_000002`** Reflex Fillcontrol Smart (Art. `6813500`): 230V AC <100W
>   ab Schrank (LSS B6A `5SL6106-7` + Reparaturschalter `3813635`, L/N/PE
>   Regel 11). Potentialfreier Wechsler „Sammelstörmeldung" (max. 230V/2A)
>   direkt als BI (kein Koppelrelais nötig). 1× BI.
> - **`410_000003`** Reflex Reflexomat XS (Art. `8800100`, kompressorgesteuert):
>   230V AC (LSS B6A + Rep.-Schalter). Externe Nachspeiseanforderung P3/P4
>   erwartet ein **230V-Signal über L+N** (kein potentialfreier Kontakt) →
>   Koppelrelais `2967073` (Regel 10): Kontakt schaltet L zu P3, N direkt zu
>   P4. Potentialfreier Sammelstörkontakt (max. 230V/8A) direkt als BI. 1×
>   BO + 1× BI. RS485/Modbus RTU bereits im Grundgerät integriert, aber kein
>   Analogausgang zur GLT vorhanden (Prozesswerte nur digital) – nicht Teil
>   der Baugruppe.
> - **`410_000004`** Reflex Variomat Touch VS 2 (Referenz-Baugröße VS 2-1/35,
>   Steuerung Art. `8910110`, pumpengesteuert): 230V AC max. 16A (LSS
>   2-polig C16A `5SL6216-7` + Rep.-Schalter `3813635`, 20A deckt 16A).
>   Externe Nachspeiseanforderung (Klemme 22b/43) ist eine **geräteeigene
>   24V-Schleife, die extern nur potentialfrei gebrückt werden darf** (keine
>   externe Spannung) → ebenfalls Koppelrelais `2967073`, jetzt nach neuer
>   **Regel 15** (Erweiterung Regel 10: TXM liefert Spannung, Ziel will
>   potentialfreie Brücke). Eigener potentialfreier Sammelstörkontakt UND
>   eigener potentialfreier Trockenlaufschutz-Kontakt (Klemme 13, getrennt)
>   direkt als 2× BI. **Analoge Ausgänge Druck (Klemme 19) und Niveau
>   (Klemme 21) sind ausdrücklich 4-20mA („Standard 4-20mA"), NICHT 0-10V** –
>   erster 4-20mA-Fall im Katalog. 1× BO + 2× BI + 2× AI.
>   **Grundsätzliche Katalogerweiterung:** neue `ddc_io`-Einzelbauteile
>   `TXM1.8X`/`TXM1.8X-ML` (analog `TXM1.8U`/`-ML`, gleiches Gehäuse,
>   dp_ai=8/dp_ao=8, Preise SIPATEC 358,40€/544,60€) für 4-20mA-Punkte
>   angelegt. **WICHTIGER GRUNDSÄTZLICHER OFFENER PUNKT:** DBACS'
>   automatische DDC-Modul-Ergänzung (`computeDdcAutoModules()`) unterscheidet
>   aktuell NICHT nach Signalart und wählt für jeden AI/AO-Bedarf immer
>   `TXM1.8U` – im Browser-Test bestätigt (Variomat-Baugruppe bekam
>   automatisch `TXM1.8U` statt `TXM1.8X`). Für `410_000004` muss der Nutzer
>   die 2 AI-Punkte aktuell manuell auf `TXM1.8X` umstellen. Eine
>   signalart-bewusste Ratchet-Erweiterung ist eine eigene Modul-4-Aufgabe,
>   nicht Teil dieser Session. Zusätzlich unklar (Kurzbeschreibung, nicht am
>   Originaldatenblatt verifiziert): ob `TXM1.8X` AO evtl. nur auf Kanal 5-8
>   statt allen 8 kann. Baugrößen-Hinweis: größere VS-2-Baugrößen können laut
>   Klemmenplan-Textauszug 400V/20A statt 230V/16A benötigen (Referenz bewusst
>   die kleinste Baugröße).
> - **`410_000005`** Reflex Servitec S (Art. `8832000`, Vakuum-Sprührohr-
>   entgasung mit Nachspeisung): 230V AC 0,2kW (LSS B6A + Rep.-Schalter).
>   Identisches P3/P4-230V-Signal-Anschlussschema wie Reflexomat (Koppelrelais
>   `2967073`, Regel 10). Potentialfreier Sammelstörkontakt (max. 230V/8A)
>   direkt als BI. 1× BO + 1× BI. Vollständiger 18-Positionen-Klemmenplan aus
>   der Betriebsanleitung (Rev. B, 28.08.2019) ausgewertet.
> - **`410_000006`** Viega Trinkwasser-Hygiene-Spülstation 2241.10 (Herst.-
>   Art.-Nr. `762216`): externes Steckernetzteil 230V AC→12V DC max. 15,6W
>   (LSS B6A + Rep.-Schalter). Potentialfreier Alarmkontakt (Klemme 1/2, max.
>   24V DC/0,5A, Arbeitskontakt) direkt als BI. Reset-Eingang (Klemme 3/4) ist
>   wie beim Variomat eine geräteeigene Spannungsschleife, die nur
>   potentialfrei gebrückt werden darf → Koppelrelais `2967073` (Regel 15).
>   1× BI + 1× BO. Optionales GLT-Modul `2241.87` (8 potentialfreie Eingänge
>   + 12 Relaisausgänge) NICHT Teil der Grundbaugruppe (Viega-Produktseite
>   dafür aktuell 404, Daten nur aus Distributor-Snippets).
> **Neue Regel 15** (Koppelrelais auch wenn TXM nur Spannung liefert, Ziel
> aber potentialfreie Brücke erwartet) unter „Baugruppen-Modellierungsregeln"
> ergänzt.
> **Item „kurzer Siemens-Tauchfühler ohne Tauchhülse" NICHT umgesetzt:**
> vollständige Recherche der QAE21../QAE317x-Familie ergab, dass eine kürzere
> G½"-Direkteinschraubvariante ohne Tauchhülse aktuell nicht existiert – das
> einzige historische Produkt dieser Art (`QAE2122.013` + `AQE2102`,
> einstellbar bis 130mm) ist abgekündigt, der Nachfolgetyp `QAE2121.015`
> braucht wieder eine separate 150mm-Tauchhülse. Analog zur bereits
> dokumentierten Erkenntnis beim Stabfühler mit Flansch (siehe unten) bewusst
> NICHT mit einem abgekündigten Artikel katalogisiert – bei Bedarf
> Alternativhersteller recherchieren (siehe Restliste).
> **Export:** baugruppen 113→**119** · einzelbauteile 190→**192** ·
> feldgeraete 61→**67**. Backup vor Schreibzugriff:
> `C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-sanitaer-reflex-viega_*.xlsx`.
> Browser-Verifikation (Standschrank 1200×2000, Drehstrom 3~/Schiene
> 3-polig, alle 6 Baugruppen im Sanitär-Tab platziert): Statistik zeigt AI
> 2/8 (Variomat, via TXM1.8U statt TXM1.8X – siehe offener Punkt oben), BI
> 6/16, BO 4/6, Komm. M-Bus AI 1/0; Stückliste zählt korrekt 4× Koppelrelais,
> 5× Reparaturschalter, 15 Klemmen `klemm_l` (5×L/N/PE), 25 Klemmen `klemm_f`,
> 7 LSS (5×B6A + 1×C16A + 1× automatisch ergänzte Steuertrafo-Sekundärsicherung
> B10A); Modul 5 zeigt alle 6 Feldgeräte mit realen Bestellnummern, Preis wo
> vorhanden sonst „–"; keine Konsolenfehler. **Restliste:** Nettopreise fehlen
> für `6811855`/`6813500`/`8832000`/`762216` (nur unklare/divergierende
> Distributor-Bruttopreise gefunden); `8800100`/`8910110` mit Preis, aber
> Stand-Datum unsicher; Fillset-M-Bus-Modul-Spannungsversorgung unbestätigt;
> Variomat-Baugrößen-Spannung (230V/16A vs. 400V/20A) nicht eindeutig einer
> Baugröße zuordenbar; `TXM1.8X`-AO-Kanalbeschränkung (evtl. nur Kanal 5-8)
> nicht am Originaldatenblatt verifiziert; DDC-Ratchet signalart-blind
> (grundsätzliche Lücke, s.o.); Viega-GLT-Modul `2241.87` technische Daten
> nur aus Distributor-Snippets (Originalseite 404); kürzerer Siemens-
> Tauchfühler nicht katalogisiert (s.o.). Herleitungstabellen je Baugruppe im
> Session-Abschlussbericht (Chat), Rohdaten `scratchpad/fork_1..5_*_ergebnis.md`.

> **Sitzungsstand Session 63 Nachtrag 2 (12.09.2026) - Gruppe Automation
> erweitert (TouchPanel, Switch, USV-Korrektur, Schaltschranksteckdose):**
> 1. **2x TouchPanel-Baugruppen** (`480_000015`/`016`, Siemens Desigo
>    PXM40 10,1"/PXM50 15,6", Original-Datenblaetter CM1N9292/9293
>    bestaetigt: 24V AC/DC SELV, 14VA/26VA, 1x Ethernet RJ45 je Panel) +
>    Web-Schnittstelle **PXG3.W100-1** (`S55842-Z117`, DIN-Schiene, 24V
>    AC/DC, **2 eingebaute Ethernet-Ports** - deckt Panel+Uplink meist ohne
>    externen Switch ab, zur Inbetriebnahme zwingend erforderlich). Reines
>    Bediengeraet ohne DP/Klemmen. Neuer `bauteil_typ` `touchpanel` +
>    **neues, exklusives Tuerband** `TUER_BAND_TOUCHPANEL=0.93` (Code-
>    Aenderung `modul-04-innenaufbau/index.html`, `tuerBand()`/`tuerFarbe()`/
>    `kurzLabel()`) - notwendig, da die Panels (bis 419x270mm) um ein
>    Vielfaches groesser sind als alle bisherigen Tuerbauteile und sonst
>    zwangslaeufig mit Nachbarbaendern (Abstand nur 0,03-0,06) kollidieren
>    wuerden. Browser-verifiziert: PXM50 rendert exklusiv im obersten
>    Bereich der Tuer, keine Ueberschneidung.
> 2. **Ethernet-Switch als eigenstaendige Automation-Baugruppe**
>    (`480_000017`): Nutzer wollte den bereits katalogisierten Switch
>    (`2891021`, 24VAC) auch einzeln waehlbar mit Stoerungs-Hilfskontakt -
>    dabei Konflikt gefunden: `2891021` ist 24VAC-**only**, fuer USV-Betrieb
>    (24V-DC-Batteriepufferung) braucht es die **DC-Schwestervariante
>    `2891152`** (9...32V DC) - neu katalogisiert und fuer diese Baugruppe
>    verwendet statt `2891021`. Eingebauter Signalkontakt (Relais, Power-/
>    Verbindungsausfall, generelle FL-SWITCH-SFN-Familieneigenschaft) direkt
>    als BI, schrankintern (Regel 12), `benoetigt_steuerspannung:'24vdc'`.
> 3. **USV-Baugruppe `480_000011` korrigiert:** die 3 Meldekontakte (Original-
>    Datenblatt 104658_en_02 bestaetigt: **13/14 Alarm, 23/24 Batteriebetrieb,
>    33/34 Batterieladung** - Nutzer-Rueckfrage-Vorschlag „Batteriefehler/
>    Sammelstoerung/Netzbetrieb/USV-Betrieb" deckt sich exakt mit diesen 3,
>    nur anders benannt: Batteriefehler=Sammelstoerung=Alarm(13/14),
>    Netzbetrieb=Kehrwert von Batteriebetrieb, USV-Betrieb=Batteriebetrieb -
>    **keine 4 getrennten Signale vorhanden**) sassen bisher faelschlich auf
>    6 Klemmen `klemm_f` - Regel 12 (schrankintern, USV+DDC im selben Schrank)
>    korrigiert: Klemmen entfernt, `dp_bi:3` direkt auf der QUINT-UPS-Zeile
>    (`2320225`, analog `TXM1.8U`: 1 Bauteil, mehrere Signalkanaele in einem
>    dp-Feld). DP-Gesamtsumme unveraendert (3x BI), nur Klemmenbedarf entfaellt.
> 4. **Schaltschranksteckdose Hutschiene** (`480_000018`): Phoenix Contact
>    `0804038` (EO-CF/PT, Schutzkontakt, 250V/16A, DIN-Schiene) + LSS 1-polig
>    B10A (`5SL6110-6`, bereits vorhanden) + Hilfsschalter `5ST3010`, Montage
>    **im Leistungsfeld** (Nutzer-Vorgabe). Schrankinterne Steckdose (kein
>    Feldkabel) - Ausloese-BI direkt auf der Hilfsschalter-Zeile, keine Klemme
>    (Regel 12). Datenpunktbedarf 1x BI.
> **Export:** baugruppen 160->**164** (4 neu, 1 korrigiert) · einzelbauteile
> 197->**202** (5 neu: `S55623-H119/-H120`, `S55842-Z117`, `2891152`,
> `0804038`). Backup: `ga_komponenten_vor-automation-touchpanel-usv_20260912.xlsx`.
> Browser-Verifikation: alle 4 neuen + die korrigierte USV-Baugruppe aus
> `baugruppen.json` gegen `accumulateDp()` nachgerechnet (USV weiterhin 3x BI
> ohne Klemmen, Switch 1x BI, Steckdose 1x BI, TouchPanels 0 DP) - keine
> verwaisten Referenzen; PXM50-Baugruppe live in Modul 4 platziert (volle
> Pipeline inkl. `m02_B/H` fuer die Tuer-Aussenmasse noetig, nicht nur
> Montagebereich) -> Steuerspannungs-Automatik ergaenzt automatisch Trafo,
> Stueckliste loest Touch Panel + Web-Schnittstelle korrekt auf, Tuer-Ansicht
> zeigt das Panel exklusiv im obersten Bereich ohne Ueberschneidung, keine
> Konsolenfehler.
> **Noch offen (Nutzer-Ankuendigung):** "Danach muessen wir unsere
> Baugruppen ein wenig umorganisieren" - noch keine konkrete Anweisung,
> welche Kategorien/Gruppen betroffen sind - bei naechster Gelegenheit
> nachfragen bzw. vom Nutzer konkretisieren lassen.

> **Sitzungsstand Session 63 Nachtrag (12.09.2026) - MS/NS-Schaltanlagen
> als Feldgeraete (Nur Monitoring), Ergebnis des Fork-Vorschlags umgesetzt:**
> Nutzer-Entscheidung nach Pruefung des Fork-Vorschlags: **10 neue
> Feldgeraet-Baugruppen** `440_000032`-`440_000041` (Gewerk 440, Kategorie
> „Schaltanlagen-Komponenten") - die Geraete stehen in EINER FREMDEN
> Elektro-Unterverteilung/Schaltanlage (nicht in diesem Schrank), DBACS
> holt nur die Meldekontakte ab: kein LSS, keine Energieversorgung, nur
> `klemm_f`-Klemmen (Regel 14, je BI 2 Klemmen, potentialfrei, kein
> Koppelrelais).
> **Recherche „Was geht wirklich?" (Original-Siemens-Bestellkatalog LV13
> 10/2022 fuer 3WA, Zubehoerdatenblatt fuer 3KF/EFM10 geprueft):**
> - **3WA Leistungsschalter:** Ein/Aus ueber den Standard-Hilfsschalterblock
>   (2 Schliesser + 2 Oeffner, im Grundgeraet OHNE Aufpreis enthalten,
>   je 1 Kontakt getrennt fuer Ein/Aus). **Ausgeloest** ueber den „Ersten
>   Ausgeloestmeldeschalter S24" (1 Wechsler) - **werkseitig bei JEDEM
>   Leistungsschalter mit Ausloeseeinheit (ETU) standardmaessig eingebaut**,
>   nicht optional (Ersatzteil-Referenz `3WA9111-0AH02`). **Trennstellung**
>   nur bei Einschubtechnik ueber Positionsmeldeschalter PSS321
>   (`3WA9111-0AH11`, 3x Wechsler Betriebs-/2x Test-/1x Trennstellung) -
>   optionales Zubehoer, hier als Standardausstattung angenommen (Nutzer
>   wollte Trennstellung explizit als eigenes Signal). **Keine separate
>   Sammelstoerung**: es gibt keinen eigenen Sammelstoerkontakt als
>   Standard - S24 deckt das ab (ein Ausloesevorgang IST die Stoerungs-
>   meldung); ein echtes zusaetzliches Alarmsignal gaebe es nur ueber das
>   optionale digitale I/O-Modul IOM230 (3 frei parametrierbare Ausgaenge
>   "zum Melden von Ereignissen, Zustaenden, Ausloesungen oder Alarmen") -
>   bewusst NICHT Teil der Baugruppe (Nutzer-Ruecksprache: kein Standard-
>   kontakt, waere ein separates Zusatzmodul). => **4x BI je 3WA-Baugruppe**
>   (Ein, Aus, Ausgeloest, Trennstellung).
> - **3KF Lasttrennschalter:** reines mechanisches Schaltgeraet - Ein/Aus
>   ueber 3KF9-Hilfsschalter (Standardzubehoer). **Ausgeloest** nur als
>   Sicherungsausfall-Anzeige ueber die elektronische Sicherungsueberwachung
>   EFM10 (`3KF9010-1AA00`, 1 Wechsler) - nur vorhanden wenn das Geraet mit
>   Sicherungen bestueckt ist (hier als Standardfall angenommen, da 3KF in
>   der Praxis meist als Sicherungslasttrennschalter eingesetzt wird).
>   **Kein Verriegelt-Signal gefunden** (nur mechanische Tuerkupplungs-/
>   Schluesselverriegelung als Sicherheitsfunktion, kein elektrischer
>   Meldekontakt dafuer im Zubehoerkatalog). **Keine Stoerungselektronik**
>   (reines Trenngeraet). => **3x BI je 3KF-Baugruppe** (Ein, Aus,
>   Ausgeloest).
> **Leitungsreihen** (Nutzer: „Berechnung egal, nur Richtwert gemeint",
> Abstufung bestaetigt): je 5 Stufen pro Familie, `feldgeraet_artikel_nr`
> als repraesentativer Platzhalter (echte Bestellnummer haengt von ETU/
> Antrieb/Sicherungseinsatz/Baugroesse ab, Siemens-Konfigurator noetig):
>   - 3KF: 32-63A (BG1) · 100-160A (BG2) · 200-250A (BG2/3) · 315-400A
>     (BG3/4) · 630-800A (BG5)
>   - 3WA: 630A · 1250A · 2000A · 3200A · 5000A (BG1-3)
> **Export:** baugruppen 150->**160** (10 neu) · feldgeraete 86->**96**
> (10 neu, einzelbauteile unveraendert 197 - reine Feldgeraet-Baugruppen
> ohne neue Schrank-Bauteile). Backup:
> `ga_komponenten_vor-schaltanlagen-feldgeraete_20260912.xlsx`. Browser-
> Verifikation: alle 10 Baugruppen aus `baugruppen.json` gegen
> `accumulateDp()` nachgerechnet (3KF exakt 3x BI, 3WA exakt 4x BI, keine
> verwaisten Referenzen, alle `feldgeraet_artikel_nr` aufloesbar),
> `440_000039` (3WA 2000A) live platziert -> BI 4/16, keine Konsolenfehler.

> **Sitzungsstand Session 63 (12.09.2026) - Gruppe Elektro befuellt (LSS/FI
> mit Hilfskontakt, Handschalter) + katalogweite LSS-Artikelnummer-Korrektur:**
> **1. Wichtiger Bugfund (Siemens-Originaldatenblaetter geprueft):** bei der
> 5SL6-Reihe kennzeichnet der Suffix **`-6` die B-Charakteristik, `-7` die
> C-Charakteristik** - das war im DBACS-Katalog vertauscht. `5SL6106-7`,
> `5SL6110-7`, `5SL6116-7`, `5SL6206-7`, `5SL6210-7` waren als "B6/B10/B16"
> katalogisiert, sind laut Siemens-TeDatasheet aber tatsaechlich **C6/C10/C16**
> - betraf 11 bestehende Baugruppen (Pumpen `420_000022`-`026`,
> Steuerspannungs-Baugruppen `480_000008`-`010`, Sanitaer `410_000002`-`006`).
> Korrigiert: alle 5 Artikel auf die echten B-Artikelnummern umbenannt
> (`5SL6106-6` usw.), Abmessungen identisch (90x18x76mm bei allen Suffix-
> Varianten, per Datenblatt bestaetigt), betroffene `baugruppen_bauteile`-
> Referenzen automatisch mit umbenannt (13 Zeilen). Bestehende C16/C32/C40-
> Artikel (`5SL6216-7`, `5SL6316-7`, `5SL6332-7`, `5SL6340-7`) waren
> bereits korrekt C-gekennzeichnet, unveraendert. `5SL6325-6` (B25) war
> ebenfalls schon korrekt.
> **2. Neue Einzelbauteile:** `5SL6216-6` (B16, 2-polig, Luecke in der
> Reihe geschlossen), `5SL6316-6` (B16, 3-polig), `5SV3644-6` (FI 40A/
> 300mA Typ A), `5SV3744-6` (FI 40A/500mA Typ A) - alle 4 per Original-
> Siemens-Datenblatt verifiziert. Bestehender Hilfsschalter `5ST3010`
> laut Distributor-Beleg explizit auch fuer FI-Schutzschalter 5SV3/5SU1
> geeignet ("universell aufsteckbar") - kein separater FI-Hilfsschalter
> noetig.
> **3. 11 schrankinterne "LSS/FI mit Hilfskontakt"-Baugruppen**
> (`440_000004`-`014`, Gewerk 440 Elektro, Kategorie „Schutzorgane mit
> Meldekontakt"): je LSS/FI + `5ST3010`-Hilfsschalter, Zone `evert`,
> `dp_bi:1` direkt auf der Hilfsschalter-Zeile (Regel 12 - Hilfsschalter
> und DDC-Modul sitzen beide im selben Schrank, keine Klemme noetig).
> Abdeckung: 1-/2-/3-polig B6/B10/B16 + 3-polig C16 + FI 30/300/500mA.
> **4. 11 Feldgeraet-Varianten derselben Elemente** (`440_000015`-`025`):
> gleiche Hardware, aber in einer EXTERNEN Elektro-Unterverteilung/
> Schaltanlage eingebaut (Nutzer-Vorgabe: „Energieversorgung fuer die
> Sicherungen ist nicht Aufgabe des Schaltschranks") - nur 2 Klemmen
> `klemm_f` fuer die Ausloese-BI (Regel 14), kein LSS/keine Energieklemmen
> in dieser Baugruppe selbst. Je ein neues `feldgeraete`-Katalogobjekt
> (Artikel-Suffix `-FELD`) angelegt, damit Modul 5 sie fuehren kann.
> **5. 6 Handschalter-Feldgeraete** (`440_000026`-`031`, Siemens SIRIUS ACT,
> Tuereinbau in EXTERNEN Tableaus/Schaltanlagen): Kontaktzahl = Anzahl
> Schaltstellungen minus 1 (Standard-Siemens-„komplette Einheit" - die
> Grundstellung ergibt sich aus „kein Kontakt aktiv"), je Kontakt 2 Klemmen
> `klemm_f`, potentialfrei, kein Koppelrelais:
>   - Aus-Ein-Auto (3-stufig, `3SU1100-2BL60-1NA0`, 2NO) -> 2x BI
>   - Hand-Auto (2-stufig, `3SU1100-2BF60-3BA0`, SPST) -> 1x BI
>   - Aus-Stufe1-Stufe2 (3-stufig, gleiche Hardware wie Aus-Ein-Auto) -> 2x BI
>   - Aus-Stufe1-Stufe2-Auto (4-stufig) -> 3x BI. **ACHTUNG unverifiziert:**
>     keine fertige SIRIUS-ACT-„komplette Einheit" fuer 4 Stufen im Katalog
>     gefunden (Siemens bietet dort augenscheinlich nur 2-/3-stufige
>     Fertigeinheiten an) - Platzhalter-Artikel `3SU1100-4-UNVERIFIZIERT`
>     gesetzt, vor Projekteinsatz das SIRIUS-ACT-Systemhandbuch pruefen
>     (vermutlich Betaetiger + 3 separate Kontaktelemente aus dem
>     Baukastensystem statt einer fertigen Einheit).
>   - Zu-Auf (2-stufig, gleiche Hardware wie Hand-Auto) -> 1x BI
>   - Zu-Auf-Auto (3-stufig, gleiche Hardware wie Aus-Ein-Auto) -> 2x BI
> **Export:** baugruppen 122->**150** (28 neu) · einzelbauteile 193->**197**
> (4 neu) · feldgeraete 72->**86** (14 neu: 11 LSS/FI + 3 Handschalter-
> Artikel, `3SU1100-2BL60-1NA0`/`3SU1100-2BF60-3BA0` je einmal fuer
> mehrere Baugruppen wiederverwendet). Backups:
> `ga_komponenten_vor-lss-artikelnr-fix_20260912.xlsx` und
> `ga_komponenten_vor-elektro-lss-fi-handschalter_20260912.xlsx`. Browser-
> Verifikation: alle 28 neuen Baugruppen aus `baugruppen.json` gegen die
> echte `accumulateDp()`-Formel nachgerechnet (DP-Werte exakt wie oben),
> `440_000010` (LSS 3-polig B16, schrankintern) live platziert -> BI 1/16,
> `440_000029` (4-Stufen-Wahlschalter) live platziert -> BI 3/16,
> vollstaendiger Katalog-Scan (Regel 7) bestaetigt keine neuen verwaisten
> Artikelreferenzen (nur bereits dokumentierte Alt-Luecken wie Wilo-Pumpen/
> Siemens-Aktoren-Platzhalter), keine Konsolenfehler.
> **Parallel-Fork (Vorschlag, NICHT umgesetzt) zu Mittelspannungs-/
> Niederspannungs-Schaltanlagen** (Lasttrennschalter, Leistungsschalter,
> Planungsfabrikat Siemens) lieferte Ergebnis - Kernpunkte: Leitreihen
> **3KL/3KM sind abgekuendigt**, Nachfolger **3KF** (NS-Lasttrennschalter
> bis 800A, Hilfsschalter separates Zubehoer `3KF9…`, keine Kommunikation
> moeglich, max. 1x BI Stellungsmeldung); **3WL abgeloest durch 3WA**
> (Leistungsschalter 630A-6300A, gestaffelte Auslöseeinheiten ETU300/
> ETU600, `ready4COM`+Kommunikationsmodul `COM190` fuer Strom-/Spannungs-/
> Leistungsmesswerte + Condition Monitoring; ohne Kommunikationsmodul nur
> potentialfrei: Stellung/Ausgeloest/Federspeicher-Bereit als BI, Fern-Ein/
> Fern-Aus/Ruecksetzen als BO ueber Einschalt-/Ausloese-/Ruecksetzmagnet).
> Noch NICHT im Katalog angelegt - wartet auf Nutzer-Entscheidung zu:
> 3KF- vs. 3KD-Leitreihe (Strombereich), ob 3WA-Ausstattungsstufen als
> getrennte Baugruppen-Familie (wie CRAH „Nur Monitoring"-Muster) modelliert
> werden sollen, Standard-Spulenspannung fuer Fern-Ein/Aus (24VDC direkt vs.
> Koppelrelais), DIN-276-Zuordnung (vermutlich 440 Elektro). Details im
> Session-Chat-Bericht des Forks.

> **Sitzungsstand Session 62 Nachtrag 3 (12.09.2026) - Reparaturschalter-
> Korrektur, Buerdewiderstand statt TXM1.8X-Zwang, Hilfskontaktblock-Luecke
> bei Ventilatoren (3 Nutzer-Funde in einer Sitzung):**
> 1. **Reparaturschalter entfaellt bei 5 Sanitaer-Baugruppen** (Nutzer-Frage
>    "warum Reparaturschalter, wird doch gar nicht benoetigt" zu
>    `410_000002`): Original-Betriebsanleitungen geprueft - `410_000002`
>    Fillcontrol Smart ("Spannungsversorgung ueber Schuko-Stecker"),
>    `410_000003` Reflexomat XS ("Netzkabel mit Stecker im Lieferumfang"),
>    `410_000005` Servitec S ("Spannungsversorgung 230V ueber Kabel mit
>    Netzstecker, werkseitig"), `410_000006` Viega 2241.10 (externes
>    Steckernetzteil) haben ALLE einen werkseitigen Netzstecker.
>    Nutzer-Vorgabe: LSS + L/N/PE-Klemmen bleiben unveraendert (der
>    Schaltschrank versorgt weiterhin eine Aufputz-Schutzkontaktsteckdose
>    vor Ort, in die das Geraet eingesteckt wird) - nur der Reparaturschalter
>    entfaellt (Ausstecken = Spannungsfreiheit, redundant). Neues
>    Pflichtzubehoer-Feldgeraet `2CKA002083A0368` (Busch-Jaeger 2300 EWSI,
>    Schutzkontaktsteckdose Aufputz IP44) ueber `zubehoer_feldgeraet_artikel_nr`
>    an alle 4 betroffenen Feldgeraete gehaengt. `410_000004` Variomat VS 2
>    ist dagegen laut Anleitung ECHT klemmenbasiert fest verdrahtet
>    (Kabeldurchfuehrungen, Einspeiseklemme X0/1) - hat aber einen eigenen
>    Hauptschalter im Anschlussteil eingebaut (gleicher Effekt:
>    Spannungsfreiheit vor Ort herstellbar) -> Reparaturschalter ebenfalls
>    entfernt, LSS bleibt (dabei Rating korrigiert: reale Anschlussleistung
>    laut Datenblatt nur 230V/5A, nicht 16A wie urspruenglich angenommen -
>    `5SL6216-7` 2-polig C16A -> `5SL6106-7` 1-polig B6A). Als Regel 16
>    verallgemeinert. `name`-Felder der 4 Steckdosen-Baugruppen um "...mit
>    Netzstecker" ergaenzt (Nutzer-Vorgabe: Bezug zur Steckdose in der
>    Feldgeraeteliste ohne Rueckfrage nachvollziehbar).
> 2. **Buerdewiderstand statt TXM1.8X-Zwang** (Nutzer-Vorgabe: "kein
>    DDC-Modul manuell auswaehlen muessen"): `computeDdcAutoModules()` waehlt
>    fuer jeden Analog-Bedarf (AI+AO-Pool) ohnehin IMMER `TXM1.8U`/`-ML`
>    (hartcodiert, siehe Code-Kommentar dort) - `TXM1.8X` wird von der
>    automatischen DDC-Modulwahl nie ausgewaehlt und kann es auch nicht
>    (kein Code-Pfad dafuer). Nutzer-Hinweis: ein 4-20mA-Signal wird mit einem
>    500-Ohm-Praezisionswiderstand parallel an der Klemme zu einem 2-10V-Signal
>    gewandelt (4mA*500R=2V, 20mA*500R=10V) und liegt damit im
>    0-10V-Eingangsbereich von `TXM1.8U` - neues generisches Einzelbauteil
>    `BUERDE-500R` (kein Hersteller-Artikel ermittelt) ergaenzt bei allen 3
>    echten 4-20mA-Punkten (Variomat `410_000004` Druck+Niveau, AquaVip
>    `410_000009` Durchfluss - NICHT bei der passiven Pt1000-Temperatur der
>    AquaVip, die braucht keine Wandlung). `TXM1.8X`/`-ML` bleiben im Katalog
>    als rein manuelle Alternative, werden aber nie automatisch vorausgesetzt
>    - der zuvor dokumentierte "offene Punkt DDC-Ratchet signalart-blind" ist
>    damit erledigt/hinfaellig.
> 3. **Hilfskontaktblock-Luecke in allen 15 Ventilator-Baugruppen behoben**
>    (Nutzer-Fund beim Nachrechnen der Variomat-Klemmen: "Reparaturschalter
>    = 1 BI 2 Klemmen" als Erwartung; beim Quer-Check ueber alle Baugruppen
>    mit Reparaturschalter gefunden): die Pumpen-Baugruppen (`420_000022`ff.)
>    fuehren korrekt einen Hilfskontaktblock (`0319691`/`0758478`) als eigene
>    Bauteilzeile neben dem Reparaturschalter (Regel-2-konform, macht die
>    Rueckmelde-BI-Klemme physikalisch plausibel). Alle 15 Ventilator-
>    Baugruppen (`430_000028`-`430_000042`, Session 59) zaehlten zwar
>    korrekt 1 BI "Stellung" (Regel 14, 2 Klemmen), hatten aber KEINEN
>    Hilfskontaktblock als Bauteil - gleicher Reparaturschalter-Artikel
>    (`3813635`/`3813641`) wie bei den Pumpen, also dieselbe physikalische
>    Situation, nur ohne das Bauteil in der Stueckliste. Ergaenzt:
>    `3813635`/`3813641`/`KG32-T204` -> `0319691`, `KG41-T204`/`KG64-T204` ->
>    `0758478` (analog Pumpen-Muster). `KG80-T204` hat noch kein passendes
>    Gegenstueck im Katalog - aktuell von keiner Baugruppe verwendet, bei
>    Bedarf nachrecherchieren. Betrifft NICHT die 5 Sanitaer-Baugruppen aus
>    Punkt 1 (dort entfaellt der Reparaturschalter ja komplett).
> **Export:** baugruppen 122 (unveraendert, nur bearbeitet) · einzelbauteile
> 192->**193** (`BUERDE-500R`) · feldgeraete 71->**72**
> (`2CKA002083A0368`). Backups:
> `ga_komponenten_vor-buerdewiderstand_20260912.xlsx` und
> `ga_komponenten_nach-reparaturschalter-fix_20260912.xlsx`. Browser-
> Verifikation: alle 5 Sanitaer-Baugruppen + `410_000009` + Ventilator-
> Stichproben (`430_000028`/`032`/`033`/`034`/`036`/`038`/`042`, KG10 bis
> KG64) direkt aus `baugruppen.json` gegen die echte `accumulateDp()`-Formel
> nachgerechnet - Werte exakt wie oben; `410_000004` zusaetzlich live in
> Modul 4 platziert (Statistik AI 2/8 · BI 2/16 · BO 1/6, `5SL6106-7` statt
> `5SL6216-7` in der Stueckliste, kein Reparaturschalter mehr), keine
> Konsolenfehler.
> **Korrektur direkt im Anschluss (Nutzer-Fund per Screenshot):**
> `BUERDE-500R` hatte faelschlich eigenen Montageplatten-Platzbedarf
> (b_mm/h_mm gesetzt) - der Buerdewiderstand wird aber OHNE eigene Klemme
> direkt an den 2 bestehenden Signalklemmen schrankintern verdrahtet, braucht
> keinen Extra-Platz. Fix: `keine_platzierung_mp:true` gesetzt (b_mm/h_mm auf
> None), analog zu aufgestecktem Schuetz-Zubehoer - bleibt in der Stueckliste
> sichtbar, entfaellt aber in der Zeichnung/Platzbedarfsrechnung. Zusaetzlich
> klargestellt (Nutzer-Regel fuer 4-20mA-Klemmenzahl, bereits korrekt
> umgesetzt): ein 4-20mA-Signal braucht wie ein passiver AI genau 2 Adern
> (Signal + Ruecklauf/GNDA), WENN das Feldgeraet seine Elektronik selbst
> versorgt (z. B. Variomat-Stationsausgaenge Druck/Niveau, dort sogar GNDA
> zwischen beiden Signalen geteilt -> nur 3 Klemmen fuer 2 AI, passend zum
> Original-Klemmenplan). NUR bei separat zu versorgenden Gebern (z. B.
> AquaVip-Durchflusssensor, braucht eigene 24V-Einspeisung lt. Datenblatt)
> kommen 2 weitere Klemmen fuer die Versorgung dazu (bei `410_000009` bereits
> so modelliert: 2 Signal + 2 Versorgung = 4 Klemmen fuer den 4-20mA-Punkt).
> Export einzelbauteile unveraendert 193 (nur Feldaenderung). Browser:
> `410_000004` erneut platziert - AI/BI/BO unveraendert (2/2/1), Kl.-Feld.-
> Fuellstand sinkt sichtbar (Bespiel-Schrank 37%->10%), Buerdewiderstand
> weiterhin 2x in der Stueckliste; `410_000009` AI 2/8 · BI/BO 0 bestaetigt;
> keine Konsolenfehler.

> **Sitzungsstand Session 62 Nachtrag (12.09.2026) – Kategorie-Umbenennung +
> Viega-Trinkwassersensoren:** Nutzer-Vorgabe zur Kategoriestruktur: die 5
> Fork-Baugruppen `410_000001`–`005` von „Nachspeise-/Druckhaltetechnik" →
> **„Druckhaltung und Nachspeisung"** umbenannt, `410_000006` von
> „Hygienetechnik" → **„Trinkwasserhygiene"**. Dazu 3 neue Baugruppen
> (Kategorie **„Sensoren flüssiges Medium"**, wie die bestehenden
> Heizungs-Tauchfühler `430_000006`/`007`) für den vom Nutzer angefragten
> kurzen Trinkwasser-Temperaturfühler – Recherche-Ergebnis: Siemens Symaro
> QAE21.. hat KEINE Variante, die wirklich ohne Tauchhülse auskommt (auch die
> „ohne Schutzrohr im Lieferumfang"-Typen brauchen laut Original-Datenblatt
> CE1N1781de zwingend ein separates Schutzrohr, Mindestlänge/-eintauchtiefe
> bleibt bei 100mm/60mm) – auf Nutzer-Hinweis stattdessen **Planungsfabrikat-
> Abweichung zu Viega** (bereits Fabrikat der Spülstation `410_000006`):
> - **`410_000007`/`008`** Viega Multifunktionssensor 2245.62 (Art. `734855`
>   G½×13,5mm / `735173` G½×25,5mm), Pt1000 passiv, schraubt DIREKT in ein
>   Viega-T-Stück Rp½ (Raxofix/Sanfix/Sanpress) – kein Schutzrohr/Tauchhülse
>   nötig, damit für dünne Pressrohre geeignet (vs. dem 100mm-Schweißanschluss
>   der Heizungsvariante). 2 Klemmen `klemm_s`, 1× AI, `menge:1` je Zeile
>   (Regel 14 beachtet).
> - **`410_000009`** Viega AquaVip-Durchfluss-/Temperatursensor 5841.50 DN20
>   (Art. `792480`, 5...85 l/min; Baureihe auch DN10 `792473`/DN32 `792497`,
>   nur DN20 auf Nutzer-Wunsch katalogisiert): Pt1000 (passiv, 1× AI) +
>   Durchfluss 4-20mA (aktiv, 1× AI) + 24V-Einspeisung (2 Klemmen ohne dp),
>   alle in `klemm_s` (Regel 1 – auch der aktive 4-20mA-Sensor bleibt
>   Messsensor, keine `klemm_f`). `benoetigt_steuerspannung:'24vdc'`
>   (Steuerspannungs-Ratchet zieht automatisch ein 24V-DC-Netzteil nach,
>   Browser bestätigt). Braucht Zubehörkabel `5841.531` (als
>   `zubehoer_feldgeraet_artikel_nr`) zur Signal-Ausleitung als konventionelle
>   Punkt-zu-Punkt-Signale statt über Viegas eigenes AquaVip-CAN-Bus-System.
>   **Wichtiger offener Punkt (bereits als Grundsatzlücke bekannt):** die
>   4-20mA-Signale brauchen `TXM1.8X`, DBACS' Auto-Modulwahl schlägt aber
>   weiterhin `TXM1.8U` vor (signalart-blind, siehe Session-62-Haupteintrag) –
>   Nutzer muss manuell umstellen.
> Export: baugruppen 119→**122** · feldgeraete 67→**71**. Backups:
> `ga_komponenten_vor-kategorie-rename-sanitaer_20260912.xlsx` und
> `ga_komponenten_vor-viega-sensoren_20260912.xlsx`. Browser-Verifikation
> (Standschrank, `410_000009` platziert): Statistik AI 2/8 · 25%, BI/BO/AO 0,
> 24V-DC-Netzteil automatisch ergänzt, Stückliste löst Klemmen korrekt auf,
> keine Konsolenfehler. Preise für `734855` nur unsicher aus Distributor-
> Bruttopreis hochgerechnet (35,72€ netto), `735173`/`792480`/`5841.531` ohne
> Preis gefunden.

> **Sitzungsstand Session 61 Teil 2 (12.09.2026) – DP-Zählungs-Bug in allen 15
> Ventilator-Baugruppen behoben (Nutzer-Fund):** beim Nachfragen, warum
> `430_000028` 4 statt der in der Beschreibung genannten 3 BI zeigte, Root
> Cause im Code gefunden: `accumulateDp()` in Modul 4 rechnet
> `demand[t] += (bt.dp_xx ?? eb.dp_xx) * bt.menge` – der dp-Override wird also
> mit der Klemmenanzahl (`menge`) DERSELBEN Zeile multipliziert. Bei den
> Session-59-Ventilator-Baugruppen saßen die 2 (bzw. 3) Klemmen einer
> Signalverbindung durchgängig in EINER `baugruppen_bauteile`-Zeile
> (`menge:2`/`3` + `dp_xx`-Override), statt wie bei den etablierten Pumpen-
> Baugruppen (`420_000022`ff.) auf mehrere Einzelzeilen mit je `menge:1`
> aufgeteilt zu sein (nur eine davon trägt den Override) – das hat den
> physikalischen Datenpunktbedarf durchgängig verdoppelt (bei den beiden
> EC-Ventilator-Wechsler-Zeilen mit `menge:3`/`dp_bi:2` sogar auf das
> 3-Fache verzerrt statt der beabsichtigten 2 BI). **Fix:** jede betroffene
> Klemmenzeile (Artikel `3209510`, Zone `klemm_f`, `menge`>1, mit dp-Override)
> in `ga_komponenten.xlsx`/Sheet `baugruppen_bauteile` aufgeteilt – je
> dp-Einheit eine Zeile `menge:1` mit dem Override, die restlichen Klemmen als
> eigene `menge:1`-Zeile(n) ohne dp (Gesamt-Klemmenzahl/Platzbedarf je Zone
> unverändert). Betrifft `430_000028`–`430_000042` (alle 15), 74 neue Zeilen
> durch die Aufteilung (544→583 Datenzeilen im Sheet). Ergebnis je Baugruppe
> (Soll laut Beschreibung = jetzt Ist):
> - `028`/`029` (1-stufig): BI 4→**3**, BO 1 (unveraendert)
> - `030`/`031` (Direktanlauf): BI 5→**4**, BO 1
> - `032`–`034` (Stern-Dreieck): BI 5→**4**, BO 1
> - `035`/`036` (Dahlander): BI 6→**5**, BO 2 (unveraendert)
> - `037`/`038` (FU-geregelt): AO 2→**1**, BI 6→**3**, BO 2→**1**
> - `039`–`042` (EC-Ventilator): AO 2→**1**, BI 8→**3**, BO 2→**1**
> Export **baugruppen 113 · einzelbauteile 190 · feldgeraete 61** (Zahlen
> unveraendert). Backup vor der strukturellen Änderung:
> `C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-ventilator-klemmen-split_20260912.xlsx`.
> Verifikation: (1) direkte Nachrechnung der `accumulateDp()`-Formel gegen
> `baugruppen.json` im Browser (JS-Konsole) für alle 15 IDs – Ist-Werte exakt
> wie oben; (2) Live-UI-Test in Modul 4 (Standschrank, Montagebereich
> 699×1499, `430_000028` bzw. `430_000037` einzeln platziert) – Statistik
> zeigt jetzt BI 3/16 bzw. AO 1/8 · BI 3/16 · BO 1/6, keine Konsolenfehler.
> Klemmen-Gesamtbreite je Zone (Platzbedarf) vor/nach Fix identisch geprüft.
> **Als Regel zu ergänzen:** DDC-Datenpunkt-Overrides (`dp_ai/ao/bi/bo`) auf
> einer Klemmenzeile IMMER mit `menge:1` versehen – trägt ein Signal mehrere
> Klemmen (Gegenader/gemeinsamer Leiter), gehören die zusätzlichen Klemmen auf
> eine SEPARATE Zeile ohne dp-Override (Vorbild: Pumpen-Baugruppen
> `420_000022`ff.). Ein `bt.dp_xx`-Override wird von der App IMMER mit
> `bt.menge` derselben Zeile multipliziert (`accumulateDp()`), nie geteilt.

> **Sitzungsstand Session 61 Teil 1 (12.09.2026) – Auswahltext-Namen der 15
> Ventilator-
> Baugruppen `430_000028`–`430_000042` ergänzt:** Nutzer-Fund per Screenshot –
> im Baugruppen-Dropdown war für z. B. „Ventilator 1-stufig, Kleinventilator
> bis 1,5 kW, 230V AC 1~" nicht erkennbar, wie die Aufschaltung erfolgt (BI/BO-
> Belegung) und ob der Reparaturschalter enthalten ist, obwohl die Statistik
> bereits 4 BI/1 BO zeigte. Nach Vorbild der Pumpen-Baugruppen (`420_000022`ff.,
> Namensmuster `<Bauteil> <Leistungsband>, <Funktion 1>, <Funktion 2>, ...,
> inkl. Rep.-Schalter, <Spannung>`) alle 15 `name`-Felder in
> `ga_komponenten.xlsx` umgestellt, `beschreibung` unverändert (war bereits
> ausführlich). Funktionsteil je Baugruppen-Familie aus den tatsächlichen
> `dp_bi/bo/ao`-Overrides der Bauteile abgeleitet, nicht neu erfunden:
> - 1-stufig 230V (`028`/`029`): „Schalten Ein/Aus, Betrieb, Stoerung"
> - Direktanlauf 3~ (`030`/`031`): „Schalten Ein/Aus, Betrieb, Stoerung MSS,
>   Stoerung PTC" (MSS-Hilfsschalter und PTC melden getrennt, Regel 13c)
> - Stern-Dreieck (`032`–`034`): „Schalten Ein/Aus, Betrieb, Stoerung
>   Ueberlast, Stoerung PTC"
> - Dahlander 2-Touren (`035`/`036`): „Schalten Stufe 1/2 (verriegelt), Betrieb
>   Stufe 1/2, Sammelstoerung Ueberlast, Stoerung PTC" (2× BO/2× BI Betrieb,
>   da beide Drehzahlstufen eigene Schütz-Hilfskontakte haben)
> - FU-geregelt/EC-Ventilator (`037`–`042`): „Freigabe, Sollwertfuehrung
>   0...10V, Betrieb, Stoerung" (Enable statt Schalten Ein/Aus, da FU/EC-
>   Elektronik selbst schaltet); bei `039`–`042` das redundante „0-10V" aus
>   dem Bauteil-Präfix entfernt (steht jetzt nur noch im Funktionsteil).
> Kommunikationsmodule `430_000043`/`044` unverändert (keine eigene
> Aufschaltung, sind Zusatzbausteine zu einer physischen Baugruppe).
> Export **baugruppen 113 · einzelbauteile 190 · feldgeraete 61** (Zahlen
> unverändert, reine Textänderung). Backup vor Schreibzugriff:
> `C:\Users\SMI\Backups\dbacs\excel\ga_komponenten_vor-ventilator-namen_20260912.xlsx`.
> Browser-Verifikation: alle 15 neuen Namen erscheinen korrekt im Lüftungs-
> Dropdown, `430_000032` testweise platziert → Belegung/Stückliste lösen
> weiterhin korrekt auf, keine Konsolenfehler.

> **Sitzungsstand Ende Session 60 (08.09.2026) – Zonen-Korrektur Ventilator-
> Baugruppen `430_000028`–`430_000036` (9 BG, Asynchronmotor):** auf Nutzer-
> Vorgabe zur korrekten Platzbedarf-Verteilung angepasst. (1) **PTC-Auslösegerät
> `3RN2012-1BW30`** (Thermistor-Motorvollschutz) gehört zum Leistungsschutz →
> `bt.zone` `steuer` → `leist` in allen 9 BG; zusätzlich Katalog-Default
> `einzelbauteile.zone` `['steuer']` → `['leist']` (Artikel nur hier verwendet,
> macht die Overrides redundant). `dp_bi:1` bleibt als Override auf der
> Bauteilzeile (PTC-Störmeldung → DDC-BI, Regel 12, keine eigene Klemme).
> (2) **Koppelrelais `2967073`** in denselben 9 BG `bt.zone` `steuer` → `leist`
> (Katalog-Default war schon `leist`; Angleichung an die Pumpen-Baugruppen
> `420_000022`). (3) **NICHT geändert – bewusst:** die PTC-Fühlerklemmen (2×
> `3209510`, ohne dp) bleiben in `klemm_f`; der **Motorschutzschalter `3RV20xx`**
> bleibt in `leist`, obwohl keine der 9 BG eine vorgeschaltete Sicherung hat und
> der MSS damit den Leitungsschutz übernimmt (nach der Regel „MSS ohne
> Vorsicherung → `evert`" gehörte er zu den LSS) – für das eine Bauteil je BG
> akzeptiert der Nutzer die Vereinfachung, spart 7+2 Zonen-Overrides und den
> Overflow-Sonderfall in einer `evert`-Zone ohne Schienensystem (nur ~105 mm
> hoch). Der Hilfsschalter `3RV2901-1E` bleibt entsprechend in `leist`.
> Export unverändert **baugruppen 113 · einzelbauteile 190 · feldgeraete 61**.
> Browser-Verifikation (Standschrank 1200×2000, Drehstrom 3~/Schiene 3-polig,
> BG `430_000032` platziert): `aggregateStueckliste()` + `resolveBaugruppen-
> Bauteile()` für alle 9 BG bestätigen `thermistorrelais`/`koppelrelais`/
> `motorschutz` → `leist`; Stückliste zeigt PTC + Koppelrelais unter „L", nur
> die DDC-Auto-Module unter „S", PTC-Fühlerklemmen unter „KF"; Zonen-Füllstand
> Energievert. 54 % · Leistung 29 % · Steuerung 33 %, kein Overflow, keine
> Konsolenfehler. Writer/Analyse im Session-Scratchpad.
> **Als Regel destilliert (→ Regel 13 unter „Baugruppen-Modellierungsregeln"):**
> PTC-Auslösegerät + Koppelrelais gehören in die Leistungszone; MSS-Zonenwahl
> hängt von der Vorsicherung ab (mit → `leist`, ohne → grundsätzlich `evert`,
> Ausnahme pro Einzelfall zulässig).

> **Sitzungsstand Ende Session 59 (07.09.2026) – Lüftung: Ventilator-Baugruppen:**
> 17 neue Ventilator-Baugruppen `430_000028`–`430_000044` angelegt (11 Familie A
> Asynchronmotor: 2× 230 V 1-stufig · 2× Direktanlauf · 3× Stern-Dreieck-
> Anlaufschaltung · 2× Dahlander 2-Touren D1/D2 · 2× FU-geregelt [FU als
> Feldgerät am Gerät, nicht im Schrank]; 4 Familie B EC-Ventilator drehzahl-
> geregelt; 2 Kommunikationsmodule „Modul Modbus RTU / TCP/IP"). Dazu 43 neue
> Einzelbauteile (3RV2-MSS-Lücken, Schütze 3RT2017/18/28/35, Stern-Dreieck-
> Kombis `3RA24…`, Überlastrelais `3RU2…`, PTC-Auslösegerät `3RN2012-1BW30`,
> mech. Verriegelung `3RA29…`, LSS C32/C40 3-pol, Reparaturschalter KG32/41/64/80
> + Hilfskontakte `0319691`/`0758478`) und 9 Feldgeräte (EC-Ventilatoren +
> AC-/FU-Platzhalter). Bestand-Korrekturen: Hilfskontakt-Fehlpaarung `0758484`
> (K2) → `0319691` (K0) bei `3813635`/`3813641` **und** den Pumpen-Baugruppen
> `420_000022`–`026`; `3RV2011`-Maße 54×77→45×97, Einstellbereich-Texte; `3RV2041`
> = S3. **Neu:** `kategorie` „Stern-Dreieck-Kombination"/„Überlastrelais"/
> „Motorschutz"/„Schützzubehör"/„Kommunikationsmodule"; `bauteil_typ`
> `ueberlastrelais`/`thermistorrelais`/`schuetzkombination`/`verriegelung`.
> Motorvollschutz durchgängig **nur PTC + Auslösegerät** (2. Kontakt hart in
> Schützspule, 1. Kontakt → BI); bei DOL/Y-D getrennte BI für MSS **und** PTC.
> DDC-BO → Schützspule **immer über Koppelrelais `2967073`** (Siemens-Triac
> bauartbedingt). Stern-Dreieck: fertige `3RA24`-Kombi, Sternzeit einstellbar
> 0,5–60 s (für Lüfterlast ~10–20 s). Dahlander: diskret, 3 Schütze + mech.
> Verriegelung + 2 getrennte `3RU2` + Austrudelzeit 30–60 s (`2905814`/DDC-
> Totzeit). EC-Ventilator: nur 1 Onboard-Melderelais → Wechsler beidseitig
> ausgelesen (BI Betrieb + BI Störung), Enable direkt vom `TXM1.6R`.
> Export ok: **baugruppen 113 · einzelbauteile 190 · feldgeraete 61**.
> Browser: Dropdown-Gruppierung „Ventilatoren"/„Kommunikationsmodule" im
> Lüftungs-Tab korrekt, alle 17 laden, Bauteile/DP-Overrides/Stückliste
> resolven, keine Konsolenfehler. **Nachtrag (07.09.2026, volle Platzierungs-/
> Ratchet-Prüfung mit konfiguriertem Schrank – jetzt erledigt):** Standschrank
> 800×2000, Drehstrom 3~/Schiene 3-polig (Modul 1–3) → alle 17 Baugruppen in
> Modul 4 gesetzt, keine JS-Fehler/Konsolenfehler, kein `undefined`/`NaN` in
> Stückliste (52 Positionen). DDC-Ratchet korrekt: 2× TXM1.8U (AI/AO-Pool),
> 7× TXM1.8D-16 (BI), 5× TXM1.6R (BO), 1× PXC7.E400L-N + Steuertrafo 24V +
> Sicherheits-/Trenntrafo 230V + LSS. Kommunikationsbauteil-Ratchet korrekt:
> 1× Ethernet-Switch `2891021` nur für das Modbus-TCP/IP-Modul (kein
> M-Bus-Pegelwandler, da kein M-Bus-Gerät gesetzt). Im 800mm-Schrank
> erwartungsgemäß harter Overflow (rote „!"-Markierung, Steuerbaugr.-Zone) –
> 17 Motor-/EC-Ventilator-Baugruppen sprengen einen einzelnen 800mm-Schrank,
> das ist die korrekt arbeitende Überlauferkennung, kein Bug. Mit 1200×2000
> (Standschrank) passt alles ohne Overflow (Leistung 65%, Steuerung 87%,
> Kl.-Feldgeräte 93%). Modul 5 aggregiert alle 15 Feldgeräte-Zeilen korrekt
> (Platzhalter `AC-VENT-1PH`/`AC-VENT-3PH`/`FU-VENT-EXT` gruppiert + 4
> EC-Ventilator-Einzelzeilen), zeigt „–" statt Fehler für die noch fehlenden
> Preise. Details Katalogrecherche:
> `scratchpad/ventilatoren_katalog_final.md` + `fork_1..9_*_ergebnis.md`.
> **Restliste (→ unten):** viele Preise/Maße Distributor-Näherung bzw. offen;
> 3RV2-/3RU2-Buchstabenstaffel interpoliert; K&N-Reparaturschalter mit
> DBACS-internem Schlüssel (`KG32-T204` …) statt echter K&N-Bestellnr.;
> 1-poliger C-LSS (C10/C13) noch nicht angelegt (230-V-Abgang nutzt `5SL6216-7`);
> Dahlander-kW-Paare Richtwerte; Modbus-TCP-Gateway noch kein Feldgerät;
> `3RN2012` `benoetigt_steuerspannung`=`230vac` gesetzt (Weitbereich, ggf. 24vac).
>
> **Sitzungsstand Ende Session 58 (05.09.2026):**
> Alle Session-58-Arbeiten (kommunikative Datenpunkte an Baugruppen, Belimo
> Energy Valve, 22 Wärme-/Kälte-/Wasserzähler, 2 Wilo-CIF-Module, CRAH
> +Betrieb/Nur-Monitoring, 3 Elektro-Energiezähler, 3 Automation-UMG-
> Türeinbau) sind implementiert, in `ga_komponenten.xlsx` eingetragen, per
> `xlsx_to_json.py` als JSON exportiert (baugruppen 96 · einzelbauteile 147 ·
> feldgeraete 52) und im Browser verifiziert. Zuletzt behoben: der
> `tuer`-Zone-an-Baugruppen-Bug (Zähler erscheint jetzt in der Türansicht,
> siehe „Modul 4/5 – Session 58").

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
│   ├── anlagen.json                             Anlagen-Katalog (Bündel bestehender bg_ids, committed, Modul 4 seit Session 67)
│   └── xlsx_to_json.py                          Konvertierungsskript Excel → JSON (10 Datensheets + 2 reine Referenz-Sheets `funktionsbereiche`/`zonen`, `einzelbauteile`/`baugruppen`+`baugruppen_bauteile`-Verknüpfungstabelle seit Session 27, `anlagen`+`anlagen_baugruppen`-Verknüpfungstabelle seit Session 67)
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
13. **Motorschutz-Bauteile: Zonenzuordnung (Session 60, verbindlich):**
    a) **PTC-Auslösegerät / Thermistor-Motorschutzrelais** (z. B. `3RN2012-1BW30`,
       `bauteil_typ='thermistorrelais'`) gehört funktional zum Motor-/Leistungs-
       schutz (wie MSS, Überlastrelais, Schütz) → Zone **`leist`**, nicht
       `steuer`, obwohl sein Meldekontakt als BI zur DDC geht (die Zone richtet
       sich nach der Bauteilfunktion, nicht nach dem BI-Ziel – vgl. Regel 1).
       Der `dp_bi`-Override sitzt auf der Bauteilzeile, keine eigene Klemme
       (Regel 12).
    b) **Koppelrelais zwischen DDC-BO und Schützspule** (z. B. `2967073`) sitzt
       ebenfalls in der Leistungsbaugruppe → Zone **`leist`** (Katalog-Default).
    c) **Motorschutzschalter** (`3RV2…`, `bauteil_typ='motorschutz'`): sitzt in
       der Baugruppe eine **Vorsicherung** vor dem MSS → MSS in **`leist`**.
       Fehlt die Vorsicherung (nicht erforderlich), übernimmt der MSS zugleich
       den Leitungsschutz → er gehört grundsätzlich in die Energieverteilung
       **`evert`** zu den LSS/Sicherungen. **Pragmatische Ausnahme pro
       Einzelfall zulässig:** bei nur einem MSS je Baugruppe und einer `evert`-
       Zone, die ihn ohne Schienensystem sprengen würde (≈105 mm), darf der MSS
       zur Vermeidung eines Zonen-Overflows in `leist` bleiben (so in
       `430_000030`–`036` entschieden, Session 60). Der seitliche MSS-Hilfs-
       schalter (`3RV2901-1E`) folgt immer der Zone seines MSS.
    d) **PTC-Fühlerklemmen** (Thermistorschleife aus der Motorwicklung, 2×
       `3209510` ohne dp): bleiben in **`klemm_f`** (Feldkabel-Abgangsklemmen),
       nicht `klemm_l` – Session-60-Entscheidung des Nutzers.
14. **DP-Override auf Klemmenzeilen immer mit `menge:1` (Session 61,
    verbindlich):** `accumulateDp()` in Modul 4 multipliziert einen
    `dp_ai/ao/bi/bo`-Override IMMER mit der `menge` derselben
    `baugruppen_bauteile`-Zeile (`demand[t] += dp_xx * menge`) – nie
    aufteilen/anteilig denken. Braucht ein Feldsignal mehrere Klemmen (z. B.
    2 Adern für einen potentialfreien Kontakt, oder 3 für einen beidseitig
    ausgelesenen Wechsler), MUSS jede Klemme eine eigene Zeile mit `menge:1`
    bekommen – nur die Zeile(n), die tatsächlich ein Signal führen, tragen
    den dp-Override, die übrigen (Gegenader/gemeinsamer Leiter) bleiben
    `menge:1` ohne dp. Eine einzelne Zeile mit `menge:2`+`dp_bi:1` zählt sonst
    2 BI statt 1. Vorbild: Pumpen-Baugruppen `420_000022`ff. Fehlerbild bei
    Verstoß: Session 59 hatte alle 15 Ventilator-Baugruppen
    (`430_000028`–`430_000042`) mit zusammengefassten Klemmenzeilen gebaut –
    dadurch war der BI/BO/AO-Bedarf durchgängig 2× (teils 3×) zu hoch, in
    Session 61 korrigiert (siehe Sitzungsstand oben).
15. **Koppelrelais auch wenn TXM nur einen spannungsbehafteten Ausgang, das
    Ziel aber einen potentialfreien Kontakt/Bruecke erwartet (Session 62,
    verbindlich, Erweiterung von Regel 10):** Regel 10 deckte bisher den Fall
    „DDC-BO muss eine hoehere Spannung schalten" ab. Ebenso ein Koppelrelais-
    Fall ist: das externe Geraet erwartet an seinem Steuereingang **keine
    Spannung von aussen**, sondern nur einen **potentialfreien Schalter-/
    Relaiskontakt**, der eine geraeteeigene (oft eigene 24V-)Schleife
    bruecken/schliessen soll (z. B. Reflex Variomat Klemme 22b/43 „External
    make-up request", Viega 2241.10 Klemme 3/4 „Reset" – die Station liefert
    die Spannung fuer die Schleife jeweils selbst). `TXM1.8T` liefert nur
    einen spannungsbehafteten 24V-AC-Ausgang, **keinen** potentialfreien
    Kontakt – ihn direkt auf eine geraeteeigene Spannungsschleife zu legen,
    wuerde zwei Spannungsquellen kurzschliessen. Auch hier: Koppelrelais 24V-
    AC-Spule (`2967073`), DDC-BO speist die Spule (keine eigene Klemme,
    Regel 12), der potentialfreie Relaiskontakt bruecke die externe Schleife
    OHNE dass DBACS-seitig eine Spannung eingespeist wird. Gilt genauso fuer
    den bereits laenger bekannten Fall „Ziel erwartet 230V L+N am Eingang"
    (Reflex P3/P4 bei Reflexomat/Servitec, ebenfalls Regel 10) – Kernkriterium
    ist in beiden Faellen: der TXM-Ausgang liefert etwas anderes (Spannung
    vs. Kontakt, oder falsche Spannungshoehe) als das Ziel braucht, also immer
    Koppelrelais zwischen DDC-BO und externem Anschluss.
16. **Reparaturschalter entfällt bei Netzstecker-Anschluss oder geräteeigenem
    Hauptschalter (Session 62, verbindlich):** Der externe Reparaturschalter
    ist normativ (EN 60204-1/VDE 0113) nur für **fest verdrahtete**
    Betriebsmittel gefordert, zur allpoligen Freischaltung außerhalb der
    Sichtweite der Hauptabsicherung. Hat ein Feldgerät laut Datenblatt
    **ausschließlich einen werkseitig konfektionierten Netzstecker** (Schuko
    o. ä.) zur Spannungsversorgung, entfällt der Reparaturschalter – Ausstecken
    erfüllt exakt denselben Zweck (Spannungsfreiheit), ein zusätzlicher
    Schalter wäre redundant. Die Versorgung selbst ändert sich dadurch NICHT:
    LSS + L/N/PE-Klemmen (Regel 11) bleiben, der Schaltschrank versorgt
    stattdessen eine **Aufputz-Schutzkontaktsteckdose vor Ort**, in die das
    Gerät eingesteckt wird – diese Steckdose wird als eigenes
    Pflichtzubehör-Feldgerät (`zubehoer_feldgeraet_artikel_nr`, Referenz
    Busch-Jaeger 2300 EWSI `2CKA002083A0368`) ergänzt, damit sie in Modul 5
    sichtbar/bepreisbar ist. Gleiches gilt, wenn ein fest verdrahtetes Gerät
    einen **eigenen, bereits eingebauten Hauptschalter** besitzt (z. B. Reflex
    Variomat Touch VS 2, Hauptschalter im Anschlussteil) – auch hier ist die
    Funktion „Spannungsfreiheit vor Ort herstellbar" bereits geräteseitig
    erfüllt. Der Hinweis auf die Anschlussart gehört in den Auswahltext
    (`name`, z. B. „...230V AC mit Netzstecker...") UND in die `beschreibung`,
    damit der Bezug zur zusätzlichen Steckdose in der Feldgeräteliste (Modul 5)
    ohne Rückfrage nachvollziehbar bleibt.
17. **Koppelrelais mit durchgeschleifter Steuerspannung für Doppelfunktion
    Sicherheitskette+BI, je Feldkontakt ein eigenes Relais (Session 68,
    verbindlich):** hat ein Feldgerät nur 1 potentialfreien Meldekontakt, der
    sowohl in eine hardwareseitige Sicherheitskette (Serienschaltung mehrerer
    Feldgeräte, führt zur Abschaltung/Verriegelung einer Anlage – z. B.
    Brandschutzklappen-Endlagenschalter) als auch als DDC-BI eingebunden
    werden soll, wird die Steuerspannung (Standard 230 V AC, Regel 6) **durch
    den Feldkontakt hindurchgeführt** (Zuleitung + Rückleitung = 2 Klemmen
    `klemm_f`, der Feldkontakt liegt in Reihe mit der Koppelrelais-Spule, nicht
    parallel dazu wie in Regel 6) und erregt damit ein Koppelrelais mit mind.
    2 Wechslern (z. B. `2967099`) – ein Kontakt speist die Sicherheitskette,
    der andere den BI (Regel 12, kein Klemmenbedarf für die beiden Kontakte
    selbst, beide bleiben schrankintern). **Zwingend ein eigenes Koppelrelais
    je Feldkontakt, nie mehrere Feldkontakte auf ein gemeinsames Relais in
    Serie** (Nutzer-Vorgabe, Session 68): eine Serienschaltung mehrerer
    Feldkontakte auf nur einem Relais (das bei JEDER Unterbrechung abfällt)
    würde zwar ebenfalls die Sicherheitskette korrekt öffnen, aber keine
    Einzelmeldung mehr zulassen (die DDC könnte nicht unterscheiden, WELCHE
    Brandschutzklappe gefallen ist) – erst die 1:1-Zuordnung Feldkontakt ↔
    Koppelrelais trennt Steuerspannungs-Durchschleifung und Einzelmeldung
    sauber. Ursprung: Fork-Recherche Brandschutzklappen (konventionell, TROX
    FK2-EU) – gilt aber generisch für jeden Anwendungsfall mit diesem Muster,
    nicht nur Brandschutzklappen.

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
