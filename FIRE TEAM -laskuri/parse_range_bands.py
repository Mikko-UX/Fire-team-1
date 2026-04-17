#!/usr/bin/env python3
import openpyxl

def parse_range(range_str):
    """Parse a range string like '7-40' or '5' into (min, max)"""
    if range_str is None:
        return None
    range_str = str(range_str).strip()
    if not range_str or range_str == '0':
        return None
    if '-' in range_str:
        parts = range_str.split('-')
        return (int(parts[0]), int(parts[1]))
    else:
        val = int(range_str)
        return (val, val)

# Load the Excel file
wb = openpyxl.load_workbook('Range bands.xlsx')
ws = wb['Sheet1']

# Parse the data
weapons_data = {}
rows = list(ws.iter_rows(values_only=True))

for row in rows:
    if not row[0]:
        continue
    
    weapon_name = row[0]
    side = row[1]
    
    # Skip header rows
    if weapon_name == 'Weapon' and side == 'Side':
        continue
    if weapon_name == 'Weapon' or side == 'Range 1':
        continue
    
    # Extract range bands from columns 2-11 (indices 2-11)
    range_bands = []
    for col_idx in range(2, 12):  # Range1 to Range10
        cell_value = row[col_idx] if col_idx < len(row) else None
        if cell_value is not None:
            parsed = parse_range(cell_value)
            if parsed:
                col_num = col_idx - 1  # Convert to 1-based column number (so col 2 = RangeBand col 1)
                range_bands.append({
                    'col': col_num,
                    'min': parsed[0],
                    'max': parsed[1]
                })
    
    if weapon_name and side:
        key = (weapon_name.strip(), side.strip())
        weapons_data[key] = range_bands

# Display the parsed data as Python code for copying into the main file
print("=== COPY THESE TO TAISTELULASKURI_UI.PY ===\n")
for (weapon, side), bands in sorted(weapons_data.items()):
    if bands:
        bands_str = ", ".join([f"RangeBand({b['col']}, {b['min']}, {b['max']})" for b in bands])
        print(f'    WeaponData("{weapon}", "{side}", ..., range_bands=[{bands_str}]),')
    else:
        print(f'    WeaponData("{weapon}", "{side}", ..., range_bands=None),  # NO RANGE BANDS')

print("\n\n=== DETAILED DISPLAY ===\n")
for (weapon, side), bands in sorted(weapons_data.items()):
    bands_str = ', '.join([f"col {b['col']}: {b['min']}-{b['max']}" for b in bands]) if bands else "NONE"
    print(f"{weapon:20} ({side:8}): {bands_str}")

