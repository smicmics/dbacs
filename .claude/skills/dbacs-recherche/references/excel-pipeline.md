# Excel-Pipeline: Schema, Eintrag, Export, Verifikation

`data/ga_komponenten.xlsx` ist die **einzige** Schreibstelle. Die 9 JSON-Dateien
werden ausschließlich von `xlsx_to_json.py` erzeugt und committet; die Excel-Datei
selbst ist **nicht** git-versioniert (`.gitignore: data/*.xlsx`) → vor
strukturellen Änderungen Backup nach `C:\Users\SMI\Backups\dbacs\excel\`.

Nur Zeilen mit `aktiv` = wahr werden exportiert. `geprueft` (Boolean) markiert vom
Nutzer gegengeprüfte Zeilen – bei Neuanlage `FALSE`/leer lassen.

## Relevante Sheets

### `einzelbauteile` → `einzelbauteile.json`
Schaltschrank-Bauteile (Klemmen, Schütze, DDC-Module, Relais, Netzteile …).

Pflicht: `aktiv`, `artikel_nr` (echte Bestellnummer, nie Typbezeichnung),
`bezeichnung`, `hersteller`, `bauteil_typ`, `b_mm`, `h_mm`, `zone` (Komma-Liste
erlaubter Zonen, erster = Default), `kategorie` (**ohne `kategorie` fehlt das
Bauteil komplett im Modul-4-Dropdown**).

`te_breite` wird aus `b_mm` abgeleitet (`ceil(b_mm/18)`) – nicht selbst setzen.

Optionale Felder je nach Bauteil: `einbaulage`, `automationsanbindung` (+ dann
`dp_ai/dp_ao/dp_bi/dp_bo` bzw. `dp_fb_ai/…` + `feldbus_protokoll` ∈
`mbus|modbus_rtu|modbus_tcp`), `dp_beschreibung` (Klartext), `keine_platzierung_mp`,
`zubehoer_artikel_nr` (Grundausstattung, z. B. Hilfsschalterblock am Schütz),
`lvb_integriert`, `benoetigt_steuerspannung` ∈ `24vac|24vdc|230vac`,
`doppelstock_variante_artikel_nr`, `trennklemme_variante_artikel_nr`,
`drehstrom_variante_artikel_nr`, `klemmen_zusatz`.
Nur `bauteil_typ='ddc_cpu'`: `max_ea_module`, `ddc_netzteil_artikel_nr`,
`ddc_sicherung_artikel_nr`, `ddc_sicherung2_artikel_nr`, `auto_ea_cpu`.
Preis/Aufwand: `preis_stueck_eur` (→ JSON `preis_eur`), `preis_lieferung_eur`,
`montage_minuten`, `preis_gesamt_eur`. Provenienz-Freitext: `quelle_hinweis`.

### `baugruppen` + `baugruppen_bauteile` → `baugruppen.json`
`baugruppen` = Kopf, `baugruppen_bauteile` = Verknüpfungstabelle (eine Zeile je
Bauteil-in-Baugruppe).

`baugruppen` Pflicht: `aktiv`, `id` (`<3-stelliger DIN-276-Gewerke-Code>_<6-stellig>`,
z. B. `420_000053`), `name`, `gewerk` (numerischer DIN-276-Code als Text),
`beschreibung`, `kategorie` (Dropdown-Gruppierung – **Pflicht, sonst unsichtbar**),
`funktionsbereich` (Komma-Liste der Gewerke-Tabs, in denen die Baugruppe
auswählbar ist).
Optional: `betriebsmittel` (Freitext externes Gerät), `feldgeraet_artikel_nr`
(→ `feldgeraete`-Zeile für Modul 5), `automationsanbindung`,
`benoetigt_steuerspannung`.

`baugruppen_bauteile` Pflicht: `bg_id` (= `baugruppen.id`), `artikel_nr`
(= echte `einzelbauteile.artikel_nr`), `menge`.
Optional-Overrides je Verwendung: `zone` (einzelner String, überschreibt den
Katalog-Default), `zeilenumbruch_davor` (→ `rowBreak`), `neue_gruppe` (→
`groupStart`, erzwingt frische Hutschienenreihe – Automationsgruppe), physische
DP-Overrides `dp_ai/dp_ao/dp_bi/dp_bo`, kommunikative DP-Overrides
`dp_fb_ai/dp_fb_ao/dp_fb_bi/dp_fb_bo` + `feldbus_protokoll`, `lvb_erforderlich`.

Kommunikative Datenpunkte sitzen konventionell auf einer ohnehin vorhandenen
`3209510`-Klemmenzeile der Baugruppe (kein eigenes Träger-Bauteil).

### `feldgeraete` → `feldgeraete.json`
Externe Betriebsmittel außerhalb des Schranks (Pumpen, Feldsensoren/-aktoren).
**Kein** `b_mm/h_mm/zone` (werden nicht platziert).

Pflicht: `aktiv`, `artikel_nr`, `bezeichnung`, `hersteller`, `kategorie`.
Optional: `preis_stueck_eur` (→ `preis_eur`), `quelle_hinweis`,
`kommunikative_datenpunkte` (Klartext – „Kommunikativ ausgelesen: …" in Modul 5),
`zubehoer_feldgeraet_artikel_nr` (+ `zubehoer_menge`, Default 1) für
Pflichtzubehör wie Montagekonsolen.

## Eintrag – Reihenfolge

1. **Lock:** sicherstellen, dass `data/~$ga_komponenten.xlsx` nicht existiert
   (Excel muss geschlossen sein).
2. **Backup** (nur bei strukturellen Änderungen – neue Sheets/Spalten):
   ```
   cp "C:/users/smi/cowork/dbacs/data/ga_komponenten.xlsx" \
      "C:/Users/SMI/Backups/dbacs/excel/ga_komponenten_vor-<zweck>_$(date +%Y%m%d_%H%M%S).xlsx"
   ```
3. **Writer-Skript:** `scripts/xlsx_write_template.py` in den Projekt-Scratchpad
   (`scratchpad/`, gitignored) kopieren, Zeilen-Dicts eintragen, ausführen:
   ```
   MSYS_NO_PATHCONV=1 wsl bash -lc "cd /mnt/c/users/smi/cowork/dbacs && python3 scratchpad/xlsx_write_<zweck>.py"
   ```
   - Neue Zeilen anhängen (Header der ersten Zeile als Feld-Referenz nehmen –
     Spaltenreihenfolge nie annehmen).
   - `quelle_hinweis` **additiv** ergänzen (bestehenden Text lesen, `[Preisrecherche
     MM/YYYY] …` anhängen), nie überschreiben.
   - `openpyxl` nur mit `data_only=False` schreiben; danach speichern.

## Export

```
MSYS_NO_PATHCONV=1 wsl bash -lc "cd /mnt/c/users/smi/cowork/dbacs/data && python3 xlsx_to_json.py"
```

Ausgabe endet je Sheet mit einer Zähl-Zeile („N Baugruppen exportiert → …").
Diese Zahlen gegen die Erwartung nach dem Eintrag abgleichen (Referenz Session 58:
baugruppen 96 · einzelbauteile 147 · feldgeraete 52 – bei jeder neuen Zeile +1).
Alle geänderten JSON-Dateien werden vom Stop-Hook committet.

## Browser-Verifikation (Phase 7)

Server: `preview_start` mit `name: "dbacs-static"` (WSL `python3 -m http.server 8099`,
Repo-Wurzel). URLs:
- Modul 4: `http://localhost:8099/modules/modul-04-innenaufbau/`
- Modul 5: `http://localhost:8099/modules/modul-05-feldgeraete/`
- Modul 7: `http://localhost:8099/modules/modul-07-stammdatenpflege/`

Checkliste je nach Änderung:
- **Neue Baugruppe:** erscheint im richtigen Gewerke-Tab, in der richtigen
  `kategorie`-Gruppe des Dropdowns; Testbelegung ergibt die erwartete Klemmenzahl,
  Zonen-Zuordnung, Datenpunkte in der DDC-Statistik (physisch vs. „Komm. …").
- **Steuerspannung/Kommunikation:** `benoetigt_steuerspannung` bzw. `dp_fb_*` zieht
  den erwarteten Ratchet-Eintrag nach (Trafo/Netzteil bzw. Pegelwandler/Switch).
- **Neues Einzelbauteil:** im Direktbauteil-Dropdown der erlaubten Zone sichtbar;
  Platzbedarf (`b_mm`/`h_mm`) plausibel im Schrankbild.
- **Preis/Feldgerät:** Modul 5 zeigt den Preis in der Feldgeräte-Stückliste;
  Modul 7 „Fehlender Preis"-Filter enthält die Zeile nicht mehr.
- **Immer:** keine Konsolenfehler (`read_console_messages`).
- Screenshot des relevanten Zustands an den Nutzer.
