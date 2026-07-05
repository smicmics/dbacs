"""
DBACS – Excel → JSON Konvertierung
===================================
Exportiert folgende Sheets aus ga_komponenten.xlsx:
  - kabel_nym_j           → kabel_nym_j.json           (nur aktive Einträge)
  - wandschraenke         → wandschraenke.json          (nur aktive Einträge)
  - kabelzugschellen      → kabelzugschellen.json       (nur aktive Einträge)
  - standschraenke        → standschraenke.json         (nur aktive Einträge)
  - sockel                → sockel.json                 (nur aktive Einträge)
  - bodenbleche           → bodenbleche.json            (nur aktive Einträge)
  - reiheneinbaugeraete   → reiheneinbaugeraete.json    (nur aktive Einträge)
  - einzelbauteile        → einzelbauteile.json         (nur aktive Einträge)
  - baugruppen +
    baugruppen_bauteile   → baugruppen.json             (nur aktive Baugruppen;
                                                          bauteile[] aus der
                                                          Verknüpfungstabelle
                                                          zusammengebaut)

Aufruf (aus data/-Verzeichnis):
    python3 xlsx_to_json.py

Abhängigkeit:
    pip install openpyxl
"""

import json
import math
import openpyxl
from pathlib import Path

EXCEL_FILE = Path(__file__).parent / 'ga_komponenten.xlsx'


def export_kabel_nym_j(wb):
    SHEET = 'kabel_nym_j'
    JSON_FILE = Path(__file__).parent / 'kabel_nym_j.json'

    if SHEET not in wb.sheetnames:
        print(f'FEHLER: Sheet "{SHEET}" nicht in der Excel-Datei.')
        return

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        rows.append({
            'typ':             str(rec['typ']),
            'n_adern':         int(rec['n_adern']),
            'querschnitt_mm2': float(rec['querschnitt_mm2']),
            'd_aussen_mm':     float(rec['d_aussen_mm']),
            'bezeichnung':     str(rec['bezeichnung']),
        })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Kabeleintraege exportiert → {JSON_FILE.name}')


def export_wandschraenke(wb):
    SHEET = 'wandschraenke'
    JSON_FILE = Path(__file__).parent / 'wandschraenke.json'

    if SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{SHEET}" nicht gefunden – uebersprungen.')
        return

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        rows.append({
            'hersteller':            str(rec['hersteller']),
            'bezeichnung':           str(rec['bezeichnung']),
            'bestellnummer':         str(rec['bestellnummer']),
            'b_gehaeuse_aussen_mm':  int(rec['b_gehaeuse_aussen_mm']),
            'h_gehaeuse_aussen_mm':  int(rec['h_gehaeuse_aussen_mm']),
            't_gehaeuse_aussen_mm':  int(rec['t_gehaeuse_aussen_mm']),
            'b_mplatte_mm':          int(rec['b_mplatte_mm']),
            'h_mplatte_mm':          int(rec['h_mplatte_mm']),
            'preis_stueckpreis_eur': float(rec['preis_stueckpreis_eur']) if rec.get('preis_stueckpreis_eur') is not None else None,
            'preis_lieferung_eur':   float(rec['preis_lieferung_eur'])   if rec.get('preis_lieferung_eur')   is not None else None,
            'preis_montage_eur':     float(rec['preis_montage_eur'])     if rec.get('preis_montage_eur')     is not None else None,
            'preis_gesamt_eur':      float(rec['preis_gesamt_eur'])      if rec.get('preis_gesamt_eur')      is not None else None,
        })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Wandschraenke exportiert → {JSON_FILE.name}')


def export_kabelzugschellen(wb):
    SHEET = 'kabelzugschellen'
    JSON_FILE = Path(__file__).parent / 'kabelzugschellen.json'

    if SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{SHEET}" nicht gefunden – uebersprungen.')
        return

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        rows.append({
            'hersteller':          str(rec['hersteller']),
            'bezeichnung':         str(rec['bezeichnung']),
            'bestellnummer':       str(rec['bestellnummer']),
            'd_kabel_min_mm':      float(rec['d_kabel_min_mm']),
            'd_kabel_max_mm':      float(rec['d_kabel_max_mm']),
            'h_schelle_mm':        float(rec['h_schelle_mm']),
            'b_schelle_mm':        float(rec['b_schelle_mm']),
            't_schelle_mm':        float(rec['t_schelle_mm']),
            'preis_stueckpreis_eur': float(rec['preis_stueckpreis_eur']) if rec.get('preis_stueckpreis_eur') is not None else None,
            'preis_lieferung_eur':   float(rec['preis_lieferung_eur'])   if rec.get('preis_lieferung_eur')   is not None else None,
            'preis_montage_eur':     float(rec['preis_montage_eur'])     if rec.get('preis_montage_eur')     is not None else None,
            'preis_gesamt_eur':      float(rec['preis_gesamt_eur'])      if rec.get('preis_gesamt_eur')      is not None else None,
        })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Kabelzugschellen exportiert → {JSON_FILE.name}')


def export_standschraenke(wb):
    SHEET = 'standschraenke'
    JSON_FILE = Path(__file__).parent / 'standschraenke.json'

    if SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{SHEET}" nicht gefunden – uebersprungen.')
        return

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        rows.append({
            'hersteller':            str(rec['hersteller']),
            'bezeichnung':           str(rec['bezeichnung']),
            'bestellnummer':         str(rec['bestellnummer']),
            'b_gehaeuse_aussen_mm':  int(rec['b_gehaeuse_aussen_mm']),
            'h_gehaeuse_aussen_mm':  int(rec['h_gehaeuse_aussen_mm']),
            't_gehaeuse_aussen_mm':  int(rec['t_gehaeuse_aussen_mm']),
            'b_mplatte_mm':          int(rec['b_mplatte_mm']),
            'h_mplatte_mm':          int(rec['h_mplatte_mm']),
            'preis_stueckpreis_eur': float(rec['preis_stueckpreis_eur']) if rec.get('preis_stueckpreis_eur') is not None else None,
            'preis_lieferung_eur':   float(rec['preis_lieferung_eur'])   if rec.get('preis_lieferung_eur')   is not None else None,
            'preis_montage_eur':     float(rec['preis_montage_eur'])     if rec.get('preis_montage_eur')     is not None else None,
            'preis_gesamt_eur':      float(rec['preis_gesamt_eur'])      if rec.get('preis_gesamt_eur')      is not None else None,
        })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Standschraenke exportiert → {JSON_FILE.name}')


def export_sockel(wb):
    SHEET = 'sockel'
    JSON_FILE = Path(__file__).parent / 'sockel.json'

    if SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{SHEET}" nicht gefunden – uebersprungen.')
        return

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        rows.append({
            'hersteller':            str(rec['hersteller']),
            'bezeichnung':           str(rec['bezeichnung']),
            'bestellnummer':         str(rec['bestellnummer']),
            'b_gehaeuse_aussen_mm':  int(rec['b_gehaeuse_aussen_mm']),
            'h_sockel_mm':           int(rec['h_sockel_mm']),
            'preis_stueckpreis_eur': float(rec['preis_stueckpreis_eur']) if rec.get('preis_stueckpreis_eur') is not None else None,
            'preis_lieferung_eur':   float(rec['preis_lieferung_eur'])   if rec.get('preis_lieferung_eur')   is not None else None,
            'preis_montage_eur':     float(rec['preis_montage_eur'])     if rec.get('preis_montage_eur')     is not None else None,
            'preis_gesamt_eur':      float(rec['preis_gesamt_eur'])      if rec.get('preis_gesamt_eur')      is not None else None,
        })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Sockel exportiert → {JSON_FILE.name}')


def export_bodenbleche(wb):
    SHEET = 'bodenbleche'
    JSON_FILE = Path(__file__).parent / 'bodenbleche.json'

    if SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{SHEET}" nicht gefunden – uebersprungen.')
        return

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        rows.append({
            'hersteller':            str(rec['hersteller']),
            'bezeichnung':           str(rec['bezeichnung']),
            'bestellnummer':         str(rec['bestellnummer']),
            'b_gehaeuse_aussen_mm':  int(rec['b_gehaeuse_aussen_mm']),
            'anzahl_platten':        int(rec['anzahl_platten']),
            'preis_stueckpreis_eur': float(rec['preis_stueckpreis_eur']) if rec.get('preis_stueckpreis_eur') is not None else None,
            'preis_lieferung_eur':   float(rec['preis_lieferung_eur'])   if rec.get('preis_lieferung_eur')   is not None else None,
            'preis_montage_eur':     float(rec['preis_montage_eur'])     if rec.get('preis_montage_eur')     is not None else None,
            'preis_gesamt_eur':      float(rec['preis_gesamt_eur'])      if rec.get('preis_gesamt_eur')      is not None else None,
        })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Bodenblech-Saetze exportiert → {JSON_FILE.name}')


def export_reiheneinbaugeraete(wb):
    SHEET = 'reiheneinbaugeraete'
    JSON_FILE = Path(__file__).parent / 'reiheneinbaugeraete.json'

    if SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{SHEET}" nicht gefunden – uebersprungen.')
        return

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        rows.append({
            'hersteller':            str(rec['hersteller']),
            'bezeichnung':           str(rec['bezeichnung']),
            'bestellnummer':         str(rec['bestellnummer']),
            'kategorie':             str(rec['kategorie']),
            'n_te':                  int(rec['n_te']),
            'nennstrom_a':           float(rec['nennstrom_a'])        if rec.get('nennstrom_a')        is not None else None,
            'n_pole':                int(rec['n_pole'])               if rec.get('n_pole')               is not None else None,
            'ausloesekennlinie':     str(rec['ausloesekennlinie'])    if rec.get('ausloesekennlinie')    is not None else None,
            'preis_stueckpreis_eur': float(rec['preis_stueckpreis_eur']) if rec.get('preis_stueckpreis_eur') is not None else None,
            'preis_lieferung_eur':   float(rec['preis_lieferung_eur'])   if rec.get('preis_lieferung_eur')   is not None else None,
            'preis_montage_eur':     float(rec['preis_montage_eur'])     if rec.get('preis_montage_eur')     is not None else None,
            'preis_gesamt_eur':      float(rec['preis_gesamt_eur'])      if rec.get('preis_gesamt_eur')      is not None else None,
        })

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Reiheneinbaugeraete exportiert → {JSON_FILE.name}')


def export_einzelbauteile(wb):
    SHEET = 'einzelbauteile'
    JSON_FILE = Path(__file__).parent / 'einzelbauteile.json'

    if SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{SHEET}" nicht gefunden – uebersprungen.')
        return

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        b_mm = float(rec['b_mm']) if rec.get('b_mm') is not None else None
        entry = {
            'artikel_nr':  str(rec['artikel_nr']),
            'bezeichnung': str(rec['bezeichnung']),
            'hersteller':  str(rec['hersteller']),
            'bauteil_typ': str(rec['bauteil_typ']),
            'b_mm':        b_mm,
            'te_breite':   math.ceil(b_mm / 18) if b_mm is not None else None,
            'h_mm':        float(rec['h_mm']) if rec.get('h_mm') is not None else None,
            'zone':        str(rec['zone']) if rec.get('zone') is not None else None,
        }
        if rec.get('kategorie') is not None:
            entry['kategorie'] = str(rec['kategorie'])
        if rec.get('einbaulage') is not None:
            entry['einbaulage'] = str(rec['einbaulage'])
        if rec.get('datenpunkt_typ') is not None:
            entry['datenpunkt_typ'] = str(rec['datenpunkt_typ'])
        if rec.get('datenpunkt_anzahl') is not None:
            entry['datenpunkt_anzahl'] = int(rec['datenpunkt_anzahl'])
        if rec.get('klemmen_zusatz') is not None:
            entry['klemmen_zusatz'] = int(rec['klemmen_zusatz'])
        if rec.get('preis_stueck_eur') is not None:
            entry['preis_eur'] = float(rec['preis_stueck_eur'])
        if rec.get('preis_lieferung_eur') is not None:
            entry['preis_lieferung_eur'] = float(rec['preis_lieferung_eur'])
        if rec.get('montage_minuten') is not None:
            entry['montage_minuten'] = float(rec['montage_minuten'])
        if rec.get('preis_gesamt_eur') is not None:
            entry['preis_gesamt_eur'] = float(rec['preis_gesamt_eur'])
        entry['geprueft'] = bool(rec.get('geprueft'))
        rows.append(entry)

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Einzelbauteile exportiert → {JSON_FILE.name}')


def export_baugruppen(wb):
    SHEET = 'baugruppen'
    JOIN_SHEET = 'baugruppen_bauteile'
    JSON_FILE = Path(__file__).parent / 'baugruppen.json'

    if SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{SHEET}" nicht gefunden – uebersprungen.')
        return
    if JOIN_SHEET not in wb.sheetnames:
        print(f'HINWEIS: Sheet "{JOIN_SHEET}" nicht gefunden – uebersprungen.')
        return

    # Verknüpfungstabelle einmal einlesen und nach bg_id gruppieren
    join_ws = wb[JOIN_SHEET]
    join_headers = [cell.value for cell in next(join_ws.iter_rows(min_row=1, max_row=1))]
    bauteile_je_bg = {}
    for row in join_ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(join_headers, row))
        bg_id = rec.get('bg_id')
        if not bg_id or not rec.get('artikel_nr'):
            continue
        bt = {'artikel_nr': str(rec['artikel_nr']), 'menge': int(rec['menge'])}
        if rec.get('zone') is not None:
            bt['zone'] = str(rec['zone'])
        bauteile_je_bg.setdefault(str(bg_id), []).append(bt)

    ws = wb[SHEET]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):
            continue
        entry = {
            'id':          str(rec['id']),
            'name':        str(rec['name']),
            'gewerk':      str(rec['gewerk']),
            'beschreibung': str(rec['beschreibung']),
            'bauteile':    bauteile_je_bg.get(str(rec['id']), []),
        }
        if rec.get('funktionsbereiche') is not None:
            entry['funktionsbereiche'] = [s.strip() for s in str(rec['funktionsbereiche']).split(',') if s.strip()]
        if rec.get('automationsfunktionen') is not None:
            entry['automationsfunktionen'] = [s.strip() for s in str(rec['automationsfunktionen']).split(',') if s.strip()]
        entry['geprueft'] = bool(rec.get('geprueft'))
        rows.append(entry)

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f'{len(rows)} Baugruppen exportiert → {JSON_FILE.name}')


def main():
    if not EXCEL_FILE.exists():
        print(f'FEHLER: {EXCEL_FILE} nicht gefunden.')
        return

    wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
    export_kabel_nym_j(wb)
    export_wandschraenke(wb)
    export_kabelzugschellen(wb)
    export_standschraenke(wb)
    export_sockel(wb)
    export_bodenbleche(wb)
    export_reiheneinbaugeraete(wb)
    export_einzelbauteile(wb)
    export_baugruppen(wb)


if __name__ == '__main__':
    main()
