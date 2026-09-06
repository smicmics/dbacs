#!/usr/bin/env python3
"""
DBACS – Muster-Writer für ga_komponenten.xlsx
=============================================
Kopie in scratchpad/xlsx_write_<zweck>.py legen, NEUE_ZEILEN / PREIS_UPDATES
befüllen, dann aus der Repo-Wurzel per WSL ausführen:

    MSYS_NO_PATHCONV=1 wsl bash -lc \
      "cd /mnt/c/users/smi/cowork/dbacs && python3 scratchpad/xlsx_write_<zweck>.py"

Grundsätze (siehe references/excel-pipeline.md):
- Erst NACH Freigabe durch den Nutzer ausführen.
- ~$ga_komponenten.xlsx darf nicht existieren (Excel geschlossen).
- Spalten werden über die Header-Zeile adressiert, nie über feste Indizes.
- quelle_hinweis wird additiv ergänzt, nie überschrieben.
- Neue Zeilen: aktiv=1, geprueft=0/leer.
- Nach dem Lauf: data/xlsx_to_json.py ausführen und Zählzeilen prüfen.
"""

from pathlib import Path
import datetime
import openpyxl

XLSX = Path(__file__).resolve().parents[1] / "data" / "ga_komponenten.xlsx"
LOCK = XLSX.with_name("~$ga_komponenten.xlsx")

# ── 1) Neue Zeilen: Sheet-Name -> Liste von {Spaltenname: Wert} ──────────────
# Nur Spalten angeben, die gesetzt werden sollen; der Rest bleibt leer.
NEUE_ZEILEN: dict[str, list[dict]] = {
    # "einzelbauteile": [
    #     {
    #         "aktiv": 1,
    #         "artikel_nr": "0000000",
    #         "bezeichnung": "Beispiel",
    #         "hersteller": "Hersteller",
    #         "bauteil_typ": "klemme",
    #         "b_mm": 5.2, "h_mm": 42.0,
    #         "zone": "klemm_f",
    #         "kategorie": "Reihenklemmen",
    #         "preis_stueck_eur": 1.23,
    #         "quelle_hinweis": "[Preisrecherche MM/YYYY] 1,23 netto, Quelle ...",
    #         "geprueft": 0,
    #     },
    # ],
    # "baugruppen": [ ... ],
    # "baugruppen_bauteile": [ {"bg_id": "420_000053", "artikel_nr": "3209510", "menge": 2}, ... ],
    # "feldgeraete": [ ... ],
}

# ── 2) Feld-Updates an bestehenden Zeilen (z.B. Preisnachtrag) ───────────────
# Sheet -> Liste von (Suchspalte, Suchwert, {Zielspalte: Wert}).
# quelle_hinweis-Werte werden an den vorhandenen Text ANGEHÄNGT.
FELD_UPDATES: list[tuple[str, str, str, dict]] = [
    # ("einzelbauteile", "artikel_nr", "3RT2026-1AB00",
    #  {"preis_stueck_eur": 34.90,
    #   "quelle_hinweis": "[Preisrecherche MM/YYYY] 34,90 netto, Quelle ..."}),
]

ADDITIV = {"quelle_hinweis"}  # Spalten, die angehängt statt ersetzt werden


def hdr(ws):
    return {c.value: i for i, c in enumerate(next(ws.iter_rows(min_row=1, max_row=1))) if c.value}


def main():
    if LOCK.exists():
        raise SystemExit(f"ABBRUCH: {LOCK.name} existiert – Excel schließen.")
    if not XLSX.exists():
        raise SystemExit(f"ABBRUCH: {XLSX} nicht gefunden.")

    wb = openpyxl.load_workbook(XLSX)  # data_only=False – wir schreiben
    stamp = datetime.date.today().strftime("%m/%Y")
    changed = 0

    for sheet, zeilen in NEUE_ZEILEN.items():
        ws = wb[sheet]
        h = hdr(ws)
        for z in zeilen:
            unbekannt = set(z) - set(h)
            if unbekannt:
                raise SystemExit(f"{sheet}: unbekannte Spalten {unbekannt}")
            r = ws.max_row + 1
            for col, val in z.items():
                ws.cell(row=r, column=h[col] + 1, value=val)
            changed += 1
            print(f"+ {sheet}: {z.get('artikel_nr') or z.get('id') or z.get('bg_id')}")

    for sheet, such_col, such_val, ziel in FELD_UPDATES:
        ws = wb[sheet]
        h = hdr(ws)
        hit = False
        for row in ws.iter_rows(min_row=2):
            if str(row[h[such_col]].value) != str(such_val):
                continue
            hit = True
            for col, val in ziel.items():
                cell = row[h[col]]
                if col in ADDITIV and cell.value:
                    cell.value = f"{cell.value} | {val}"
                else:
                    cell.value = val
            changed += 1
            print(f"~ {sheet}: {such_val} -> {list(ziel)}")
        if not hit:
            raise SystemExit(f"{sheet}: {such_col}={such_val} nicht gefunden")

    if not changed:
        raise SystemExit("Nichts zu tun – NEUE_ZEILEN/FELD_UPDATES leer.")

    wb.save(XLSX)
    print(f"\n{changed} Änderung(en) geschrieben ({stamp}). Jetzt data/xlsx_to_json.py ausführen.")


if __name__ == "__main__":
    main()
