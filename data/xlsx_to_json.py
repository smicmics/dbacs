"""
DBACS – Excel → JSON Konvertierung
===================================
Liest das Sheet 'kabel_nym_j' aus ga_komponenten.xlsx
und schreibt kabel_nym_j.json (nur aktive Einträge).

Aufruf (aus data/-Verzeichnis):
    python xlsx_to_json.py

Abhängigkeit:
    pip install openpyxl
"""

import json
import openpyxl
from pathlib import Path

EXCEL_FILE = Path(__file__).parent / 'ga_komponenten.xlsx'
JSON_FILE  = Path(__file__).parent / 'kabel_nym_j.json'
SHEET_NAME = 'kabel_nym_j'

def main():
    if not EXCEL_FILE.exists():
        print(f'FEHLER: {EXCEL_FILE} nicht gefunden.')
        return

    wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
    if SHEET_NAME not in wb.sheetnames:
        print(f'FEHLER: Sheet "{SHEET_NAME}" nicht in der Excel-Datei.')
        return

    ws = wb[SHEET_NAME]
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not any(row):          # Leerzeile überspringen
            continue
        rec = dict(zip(headers, row))
        if not rec.get('aktiv'):  # inaktive Einträge überspringen
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

    print(f'{len(rows)} Einträge exportiert → {JSON_FILE.name}')

if __name__ == '__main__':
    main()
