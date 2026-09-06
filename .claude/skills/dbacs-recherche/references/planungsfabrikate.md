# Planungsfabrikate je Kategorie

Bei neuer Bauteil-/Feldgeräte-Kategorie zuerst hier nachsehen; ist die Kategorie
neu, den Nutzer nach dem Planungsfabrikat fragen und diese Datei ergänzen.
Reihenfolge der Recherche: **Originaldatenblatt des Planungsfabrikats → 1–2
Alternativen mit Link + Begründung, wenn der Standard nicht passt → Freigabe**.

| Kategorie | Planungsfabrikat | Datenblatt-/Preis-Fundstelle | Anmerkung |
|---|---|---|---|
| Reihenklemmen (Einspeisung / Abgänge) | Phoenix Contact | phoenixcontact.com Produktdetail; Preise über Distributor (RS, Automation24, elektro4000) | UT-Reihe (Schraub) für Einspeisung, PT-Reihe (Push-in) für alle drei Abgangs-Klemmenzonen |
| Raum-/Kanal-/Tauch-Sensoren (Temp, Feuchte, CO2, VOC, Δp) | Siemens (Symaro) | hit.sbt.siemens.com, support.industry.siemens.com; PDF binär → `pypdf` in WSL | aktive Analogsignale ⇒ `benoetigt_steuerspannung`; passive ⇒ keine |
| Ventil-/Klappenantriebe | Siemens Acvatix; Belimo wo Siemens nichts führt | Siemens HIT; belimo.com | Stellsignal + Rückmeldung beide auf `klemm_f` (Regel 9) |
| Energiezähler / Netzanalysatoren (Elektro) | Janitza (UMG-Reihe); Schneider Acti9 iEM als Alternative | janitza.de; schneider-electric.de | kommunikativ: `dp_fb_ai` + `feldbus_protokoll`, keine physische Platzierung |
| Wärme-/Kälte-/Wasserzähler | Aquametro / Aquametro-Integra | aquametro.com; Preise DN50/DN100 oft nicht öffentlich → offener Punkt | kein Modbus-TCP-Modul ⇒ „Dual" = M-Bus + Modbus RTU |
| Umwälzpumpen + Kommunikationsmodule | Wilo | wilo.com Katalog; Artikelnummern der CIF-/IF-Module | PICO signallos (Koppelrelais-Pattern), MAXO/-Z mit Signalklemmen |
| Mechanische Druck-/Temperaturschalter, Sicherheitsbegrenzer | Honeywell / FEMA | products.ecc.emea.honeywell.com; FEMA-Katalog-PDF | Siemens führt diese Kategorie nicht; potentialfrei ⇒ keine eigene Steuerspannung |
| Wassermangelsicherung | SYR / Hans Sasserath | syr.de | Herstellerabweichung, dokumentiert im `quelle_hinweis` |
| Kanalrauchmelder | Oppermann | oppermann-rwm.de | DIBt-Zulassung zur direkten Klappenansteuerung |
| Luftstromwächter | KRIWAN (INT511-Nachfolge) | kriwan.com | Siemens-Original abgekündigt |
| DDC – CPU (Automationsstation) | Siemens Desigo PX | Siemens-Datenblätter 02–03/2026; SIPATEC für Netto-Straßenpreise | aktuelle Revision: PXC4.E16-2 / PXC5.E24-N / PXC7.E400L-N (nicht mehr `.A`) |
| DDC – I/O-Module | Siemens TX-I/O (`TXM1.x`) | Siemens-Datenblätter Rev. 03/2026 | `TXM1.8U` deckt AI **und** AO (gemeinsamer Analog-Pool) |
| DDC – Lokale Vorrangbedienebene (LVB) | Metz Connect | metz-connect.com | Ausnahme vom Phoenix-Standard; `110730` KMA-F8 (AO) / `110661` KRS-E06 (BO) |
| Koppelrelais / Schaltrelais | Phoenix Contact (PLC-RSC-Reihe) | phoenixcontact.com | `2967099` 230V-Spule, `2967073` 24V-AC-Spule |
| M-Bus-Pegelwandler | Relay GmbH (PW-Reihe) | relay.de | `MR006` (PW20) bis 20 Zähler, `MR004C` (PW60) darüber |
| Ethernet-Switch (Schaltschrank) | Phoenix Contact FL SWITCH | phoenixcontact.com | `2891021` (5-Port, 24V AC); 1 Port für Uplink ⇒ 4 freie Ports je Switch |
| Netzteile / USV (Schaltschrank) | Phoenix Contact QUINT; Siemens SITOP als Alternative | phoenixcontact.com | Marken-Konsistenz zu bestehendem 24V-DC-Netzteil |
| Schränke / Sockel / Bodenbleche | Rittal | rittal.com Katalog | AX (Wand), VX25 (Stand) |

## Preisrecherche – Konvention

- Herstellerlistenpreis bevorzugt; sonst namhafter Großhandel/Distributor.
- Gebrauchtbörsen ausgeschlossen.
- Alle Werte **netto**, Stichmonat notieren (`~MM/YYYY`).
- Provenienz je Eintrag additiv in `quelle_hinweis`:
  `[Preisrecherche MM/YYYY] <Wert> netto, Quelle <Distributor/URL>, ggf. aus Brutto zurückgerechnet`.
- Abgekündigte Artikel ohne öffentlichen Preis ⇒ offener Punkt „Herstelleranfrage
  nötig", nicht schätzen.
