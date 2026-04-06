# GA-Planungstool · Projektdokumentation Session 1

## Projektziel

Webbasiertes Planungswerkzeug für das Gewerk **Gebäudeautomation (GA)** zur Unterstützung
in verschiedenen Leistungsphasen nach HOAI. Die Anwendung besteht aus einer Startseite
(GitHub Pages) mit mehreren aufrufbaren Modulen. Entwicklung wird kontinuierlich erweitert.

---

## Softwarearchitektur (Übersicht)

```
/index.html                  ← Startseite · Modulübersicht · Navigation
/assets/                     ← CSS · JS · Fonts
/data/
  ga_komponenten.db          ← SQLite-Datenbank (aus Excel generiert)
  ga_komponenten.xlsx        ← Primäres Pflegewerkzeug (Source of Truth)
/modules/
  modul-01-schaltschrank/    ← Modul 1: Schaltschrank-Dimensionierung
  modul-02-.../              ← weitere Module (zukünftig)
```

### Datenbankstrategie

- **Pflegewerkzeug:** Excel (.xlsx), ein Tabellenblatt pro Komponentenkategorie
- **Produktivdatenbank:** SQLite (.db), generiert via Python-Konvertierungsskript
- **Zugriff im Browser:** sql.js (SQLite in WebAssembly, kein Server nötig)
- **Konvertierung:** `python convert.py` → liest alle Blätter → schreibt ga_komponenten.db

```python
# Konvertierungsskript (Grundstruktur)
import pandas as pd, sqlite3
EXCEL = "data/ga_komponenten.xlsx"
DB    = "data/ga_komponenten.db"
blaetter = ["schraenke_wand", "schraenke_boden", "schuetze", ...]
conn = sqlite3.connect(DB)
for blatt in blaetter:
    df = pd.read_excel(EXCEL, sheet_name=blatt)
    df.to_sql(blatt, conn, if_exists="replace", index=False)
conn.close()
```

### Pflegeworkflow

1. Excel öffnen → Wert ändern / Zeile ergänzen → Speichern
2. `python convert.py`
3. `git add data/ && git commit -m "Preise aktualisiert"`
4. `git push` → GitHub Pages zeigt neue Daten

---

## Modul 1 – Schaltschrank-Dimensionierung

### Aufgabe

Abschätzung der erforderlichen Schaltschrankgröße auf Basis von Eingabedaten.
Ausgabe: Abmessungen, Schrankanzahl/-gruppe, Kostenschätzung, schematische Aufbauzeichnung.

### Eingabedaten (geplant)

- HOAI-Leistungsphase
- Anlagengruppen + Anzahl (RLT, Heizkreise, Kälte, Elektroverteilungen)
- Datenpunktquelle (aus Datenbank)
- Kundenvorgaben Schrankgröße
- Lokale Vorrangbedienung (LVB) ja/nein
- Aufbauart (Einspeisung / Leistung / Steuerung / LVB / Tür / Montageplatte)
- Kabeleinführung oben oder unten

### Aufbau-Varianten (Montageplatte)

- **Variante 1:** Freie Montagewahl (alle Komponenten gemischt)
- **Variante 2:** Leistung und Steuerung getrennt (unterschiedliche Zonenhöhen)

---

## Erarbeitete Grundlagen: Kabeleinführungszone h_ke

### Formel (universell für Wand- und Standschrank)

```
h_ke = h_handling_ke + h_zug_ke + h_kabel_bieg + h_kanal_ke
```

### Variablen-Referenz

| Variable | Bezeichnung | Wert Wandschrank |
|---|---|---|
| `b_mplatte_abstand_ssiw` | Seitl. Abstand MP zur Schrank-Innenwand (beidseitig) | ≈ 30 mm |
| `h_mplatte_abstand_ssiw` | Abstand Schrank-Innenwand oben zur OK Montageplatte | ≈ 15 mm |
| `h_handling_ke` | Freie Kabellänge nach PG bis Biegung beginnt | 15 mm |
| `h_zug_ke` | Zugentlastung intern (Kabelabfangschiene auf Hutschiene) | **0 mm** (Wandschrank) |
| `durchmesser_kabel_aussen_max` | Außen-∅ des dicksten Kabels im Schrank | 16 mm (NYM-J 5×6 mm²) |
| `h_kabel_bieg` | Mindestbiegeradius: 4 × durchmesser_kabel_aussen_max (VDE 0298-4) | 64 mm |
| `h_kanal_ke` | Höhe des horizontalen Kabelkanals | 60 mm |
| **`h_ke`** | **Gesamte Kabeleinführungszone auf der Montageplatte** | **139 mm** |

### Hinweise zur Formel

- **h_zug_ke = 0** beim Wandschrank: PG-Zugentlastung erfolgt außen am Gehäuse.
- **h_zug_ke ≈ 35 mm** beim Standschrank: Kabelabfangschiene wird auf Hutschiene
  aufgeklipst und festgeschraubt (wird in separater Session erarbeitet).
- **h_handling_ke** liegt in `h_mplatte_abstand_ssiw`: kein zusätzlicher Platzbedarf
  auf der Montageplatte – wird dennoch konservativ in h_ke eingerechnet.
- **h_kabel_bieg** gilt für den Normalfall (ein Biegeradius). Sonderfall
  „türseitiger Einzug" (zwei Biegungen) wird als Ausnahme nicht bemessen.
- **VDE 0298-4:** r_min = 4 × ∅_außen für fest verlegte NYM-J Leitungen.
- **Maximalkabel Wandschrank:** NYM-J 5×6 mm² (Drehstrom), ∅_außen = 16 mm.
- **h_ke gilt** für KE von oben und KE von unten gleichermaßen.
  Bei KE von unten liegt h_ke am unteren Rand der Montageplatte;
  die Einspeisegruppe bleibt immer oben.

### Beispiel: Rittal AX 1213.000 (1000 × 1200 × 300 mm)

- Montageplatte: 945 × 1175 mm
- b_mplatte_abstand_ssiw: (1000 − 945) / 2 = 27,5 mm → gerundet **30 mm**
- h_mplatte_abstand_ssiw: (1200 − 1175) / 2 = 12,5 mm → gerundet **15 mm**
- h_ke = 0 + 15 + 64 + 60 = **139 mm**

---

## Erläuterungszeichnung (Datei)

Die HTML-Datei `wandschrank_frontansicht_v7.html` enthält:
- SVG-Frontansicht mit korrekten Proportionen (Beispiel 1000×1200 mm)
- Zonendarstellung: h_handling_ke, h_kabel_bieg, h_kanal_ke, h_ke
- Maßkette mit Variablennamen (keine Zahlenwerte in der Zeichnung)
- Maßkette b_mplatte_abstand_ssiw oben am Schrank
- Erläuterungstabelle unterhalb der Zeichnung

---

## Excel-Tabellenstruktur: Blatt `schraenke_wand`

Pflichtfelder (PF) in jedem Blatt:

| DB-Feldname | Typ | PF | Beschreibung |
|---|---|---|---|
| `id` | Text | ✓ | Eindeutiger Schlüssel, Präfix WS |
| `bezeichnung_kurz` | Text | ✓ | Vollname für Listenfeld (z.B. „Wandschrank 500×400×210 Stahl RAL7035") |
| `hersteller` | Text | – | z.B. Rittal, Spelsberg, generisch |
| `aktiv` | Int | ✓ | 1 = aktiv, 0 = veraltet |
| `preis_datum` | Datum | ✓ | YYYY-MM |

Geometrische Felder (Auswahl):

| DB-Feldname | Einheit | Beschreibung |
|---|---|---|
| `aussen_breite_mm` | mm | Außenmaß B |
| `aussen_hoehe_mm` | mm | Außenmaß H |
| `aussen_tiefe_mm` | mm | Außenmaß T |
| `montageplatte_breite_mm` | mm | Nutzbreite MP |
| `montageplatte_hoehe_mm` | mm | Nutzhöhe MP |
| `b_mplatte_abstand_ssiw_mm` | mm | Seitl. Abstand MP–Innenwand |
| `h_mplatte_abstand_ssiw_mm` | mm | Oberer Abstand MP–Innenwand |
| `b_kabelkanal_vertikal_mm` | mm | Breite vert. Kabelkanal |
| `h_kabelkanal_horizontal_mm` | mm | Höhe horiz. Kabelkanal zw. Reihen |
| `h_reserve_oben_mm` | mm | Einspeisezone oben |
| `h_reserve_unten_mm` | mm | Klemmenzone unten |
| `te_pro_reihe_mit_kanal` | TE | Berechnet: (MP-Breite − b_kanal_v) / 18 |
| `he_reihen_var1_gesamt` | HE | Berechnet |

Schrank-spezifische Felder (nur Wandschrank):

| DB-Feldname | Typ | Beschreibung |
|---|---|---|
| `opt_leuchte_tuerschalter` | Int | 0/1/2 (nein / standard / EX) |
| `opt_thermostat_luefter` | Int | 0/1/2 |
| `opt_heizung` | Int | 0/1 |
| `opt_aufhaengung_typ` | Text | z.B. „4× Wandwinkel" |
| `opt_montageplatte_konfig` | Text | „1×MP vollflächig" / „2×MP geteilt" |
| `ke_position` | Text | „oben" / „unten" |
| `ke_kabel_d_max_mm` | mm | ∅ Außen Maximalkabel |
| `h_zug_ke_mm` | mm | 0 (Wandschrank) |
| `h_handling_ke_mm` | mm | 15 mm Standard |
| `h_kabel_bieg_mm` | mm | Berechnet: 4 × ke_kabel_d_max_mm |
| `h_kanal_ke_mm` | mm | 60 mm Standard |
| `h_ke_mm` | mm | Berechnet: Summe |

Preisfelder: `preis_schrank_eur`, `preis_montageplatte_eur`,
`preis_ke_einf_set_eur`, `preis_pg_set_eur`, `preis_aufhaengung_eur`,
`preis_leuchte_tuersch_eur`, `preis_gesamt_schrank_eur` (Summe)

DL-Felder: `dl_zusammenbau_std`, `dl_wandmontage_std`, `dl_lieferung_eur`

---

## Nächste geplante Schritte

1. **Excel-Datei anlegen** mit Blatt `schraenke_wand` und 3–5 Mustergeräten
2. **Einspeisezone h_einsp** erarbeiten (analog zu h_ke)
3. **Klemmenzone h_klemm** erarbeiten
4. **TE-Berechnung** pro Reihe und Gesamtkapazität
5. **Standschrank** erarbeiten (h_zug_ke ≈ 35 mm, andere Zonen)
6. **Modul 1 UI** und Berechnungslogik (logic.js)
7. **Startseite** (index.html) mit Modulübersicht

---

## Offene Fragen / Entscheidungen

- Kabelkanal-Größe für Wandschrank: **60 mm** fixiert als Standard.
  Für Standschrank ggf. 80 mm (mehr Kabel, größere Querschnitte).
- Biegeradius-Faktor: **4 × ∅_außen** (VDE 0298-4, fest verlegt).
  Nicht 6× (das gilt für flexible Leitungen).
- TE-Berechnung: Berechnungsformel statt fester Wert im Schema,
  Eingabeparameter (b_kabelkanal_vertikal_mm, etc.) pro Schrank.
- Preise: **Listenpreise**, Datum-Feld für Preispflege.
  Aktiv-Flag (0/1) für veraltete Datensätze – keine Löschung.

---

*Erstellt: Session 1 · Gewerk GA · Modul 1 Grundlagen Wandschrank*
