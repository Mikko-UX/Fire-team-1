import tkinter as tk
from tkinter import ttk, messagebox
import random
from dataclasses import dataclass
from typing import List, Optional, Literal, Tuple, Dict, Any

# ============================================================
# FIRE TEAM 6.5 - COMPLETE SYSTEM
# ============================================================

Side = Literal["US", "SOVIET"]
Ammo = Literal["HV", "HT", "SAM"]
WeaponType = Literal["GUN", "RKT", "MSL", "SAM"]

@dataclass(frozen=True)
class RangeBand:
    col: int
    rmin: int
    rmax: int

@dataclass(frozen=True)
class WeaponData:
    name: str
    side: Side
    wtype: WeaponType
    firepower_hv: Optional[int] = None
    firepower_ht: Optional[int] = None
    ammo_type: Optional[Ammo] = None
    range_bands: List[RangeBand] = None
    hv_front_armor: int = 0
    hv_flank_armor: int = 0
    ht_front_armor: int = 0
    ht_flank_armor: int = 0

# Weapon Database
WEAPONS_DB: List[WeaponData] = [
    WeaponData("M-1", "US", "GUN", firepower_hv=14, firepower_ht=18, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 7), RangeBand(2, 8, 11), RangeBand(3, 12, 14), RangeBand(4, 15, 18),
                           RangeBand(5, 19, 21), RangeBand(6, 22, 26), RangeBand(7, 27, 32)],
               hv_front_armor=12, hv_flank_armor=6, ht_front_armor=10, ht_flank_armor=5),
    WeaponData("M-60", "US", "GUN", firepower_hv=12, firepower_ht=16, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 6), RangeBand(2, 7, 9), RangeBand(3, 10, 11), RangeBand(4, 12, 13),
                           RangeBand(5, 14, 16), RangeBand(6, 17, 22), RangeBand(7, 23, 30)],
               hv_front_armor=8, hv_flank_armor=3, ht_front_armor=4, ht_flank_armor=2),
    WeaponData("M-2", "US", "GUN", firepower_hv=8, firepower_ht=10, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 11),
                           RangeBand(5, 12, 14), RangeBand(6, 15, 18), RangeBand(7, 19, 22)],
               hv_front_armor=4, hv_flank_armor=2, ht_front_armor=4, ht_flank_armor=2),
    WeaponData("M-113", "US", "GUN", firepower_hv=2, firepower_ht=2, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 3), RangeBand(2, 4, 6), RangeBand(3, 7, 9)],
               hv_front_armor=1, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    WeaponData("M-106", "US", "GUN", firepower_hv=2, firepower_ht=2, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 3), RangeBand(2, 4, 6), RangeBand(3, 7, 9)],
               hv_front_armor=1, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    WeaponData("TOW MSL", "US", "MSL", firepower_ht=15, ammo_type="HT",
               range_bands=[RangeBand(1, 7, 40), RangeBand(2, 6, 6), RangeBand(3, 5, 5), RangeBand(4, 4, 4), RangeBand(6, 2, 3)]),
    WeaponData("Dragon MSL", "US", "MSL", firepower_ht=12, ammo_type="HT",
               range_bands=[RangeBand(3, 3, 10)]),
    WeaponData("Hellfire MSL", "US", "MSL", firepower_ht=18, ammo_type="HT",
               range_bands=[RangeBand(1, 6, 55), RangeBand(2, 5, 5), RangeBand(3, 4, 4), RangeBand(4, 3, 3), RangeBand(5, 2, 2)]),
    WeaponData("AH-64", "US", "GUN", firepower_hv=8, firepower_ht=10, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 11),
                           RangeBand(5, 12, 14), RangeBand(6, 15, 18), RangeBand(7, 19, 22)],
               hv_front_armor=1, hv_flank_armor=1, ht_front_armor=3, ht_flank_armor=2),
    WeaponData("T-80", "SOVIET", "GUN", firepower_hv=13, firepower_ht=17, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 7), RangeBand(2, 8, 11), RangeBand(3, 12, 14), RangeBand(4, 15, 16),
                           RangeBand(5, 17, 19), RangeBand(6, 20, 21), RangeBand(7, 22, 23), RangeBand(8, 24, 26)],
               hv_front_armor=10, hv_flank_armor=4, ht_front_armor=11, ht_flank_armor=4),
    WeaponData("T-72", "SOVIET", "GUN", firepower_hv=13, firepower_ht=17, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 7), RangeBand(2, 8, 11), RangeBand(3, 12, 14), RangeBand(4, 15, 16),
                           RangeBand(5, 17, 19), RangeBand(6, 20, 21), RangeBand(7, 22, 23), RangeBand(8, 24, 26)],
               hv_front_armor=10, hv_flank_armor=4, ht_front_armor=10, ht_flank_armor=4),
    WeaponData("BMP-1", "SOVIET", "GUN", firepower_hv=6, firepower_ht=8, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 4), RangeBand(2, 5, 5), RangeBand(3, 6, 6), RangeBand(4, 7, 7),
                           RangeBand(5, 8, 8), RangeBand(6, 9, 10), RangeBand(7, 11, 12), RangeBand(8, 13, 14)],
               hv_front_armor=2, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),
    WeaponData("BMP-2", "SOVIET", "GUN", firepower_hv=7, firepower_ht=9, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 4), RangeBand(2, 5, 6), RangeBand(3, 7, 8), RangeBand(4, 9, 10),
                           RangeBand(5, 11, 12), RangeBand(6, 13, 14), RangeBand(7, 15, 17), RangeBand(8, 18, 20)],
               hv_front_armor=2, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),
    WeaponData("Mi-24", "SOVIET", "GUN", firepower_hv=7, firepower_ht=9, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 4), RangeBand(2, 5, 6), RangeBand(3, 7, 8), RangeBand(4, 9, 10),
                           RangeBand(5, 11, 12), RangeBand(6, 13, 14), RangeBand(7, 15, 17), RangeBand(8, 18, 20)],
               hv_front_armor=2, hv_flank_armor=1, ht_front_armor=4, ht_flank_armor=2),
]

def get_weapon_by_name(name: str) -> Optional[WeaponData]:
    for w in WEAPONS_DB:
        if w.name == name:
            return w
    return None

def get_all_weapon_names() -> List[str]:
    return sorted([w.name for w in WEAPONS_DB])

@dataclass(frozen=True)
class DiffRow:
    hv_threshold: Optional[int]
    ht_threshold: int
    kills: List[Optional[int]]

KILL_TABLE: List[DiffRow] = [
    DiffRow(hv_threshold=-1, ht_threshold=-1, kills=[1, 1, None, None, None, None, None, None, None, None]),
    DiffRow(hv_threshold=None, ht_threshold=0, kills=[1, 1, 1, 1, 1, None, None, None, None, None]),
    DiffRow(hv_threshold=0, ht_threshold=1, kills=[2, 2, 1, 1, 1, 1, 1, 1, 1, None]),
    DiffRow(hv_threshold=1, ht_threshold=2, kills=[4, 3, 3, 2, 2, 2, 1, 1, 1, None]),
    DiffRow(hv_threshold=2, ht_threshold=3, kills=[5, 5, 4, 4, 3, 2, 2, 1, 1, None]),
    DiffRow(hv_threshold=None, ht_threshold=4, kills=[6, 6, 5, 4, 4, 3, 2, 1, 1, None]),
    DiffRow(hv_threshold=3, ht_threshold=5, kills=[7, 6, 5, 5, 4, 3, 2, 2, 1, 1]),
    DiffRow(hv_threshold=None, ht_threshold=6, kills=[8, 7, 6, 5, 4, 3, 3, 2, 1, 1]),
    DiffRow(hv_threshold=4, ht_threshold=7, kills=[8, 7, 6, 5, 5, 4, 3, 2, 1, 1]),
    DiffRow(hv_threshold=5, ht_threshold=8, kills=[9, 8, 7, 6, 5, 4, 3, 2, 1, 1]),
]

def base_column_for_range(weapon: WeaponData, range_hexes: int) -> Optional[int]:
    if not weapon.range_bands:
        return None
    for band in weapon.range_bands:
        if band.rmin <= range_hexes <= band.rmax:
            return band.col
    return None

def pick_row_index(differential: int, ammo: Ammo) -> Optional[int]:
    if differential < -1:
        return None
    if ammo == "HV":
        hv_rows = [(i, r.hv_threshold) for i, r in enumerate(KILL_TABLE) if r.hv_threshold is not None]
        eligible = [i for i, th in hv_rows if th is not None and th <= differential]
        if not eligible:
            return None
        return max(eligible)
    eligible = [i for i, r in enumerate(KILL_TABLE) if r.ht_threshold <= differential]
    if not eligible:
        return None
    return max(eligible)

def kill_number(weapon: WeaponData, target: WeaponData, target_side: Literal["Front", "Flank"], range_hexes: int, column_shifts: int, leadership: int, fear: int) -> Tuple[Optional[int], Optional[int], Optional[int], Ammo, int, int]:
    if weapon.ammo_type == "HT" or weapon.wtype in ("MSL", "SAM", "RKT"):
        ammo = "HT"
        firepower = weapon.firepower_ht if weapon.firepower_ht else 0
        armor = target.ht_front_armor if target_side == "Front" else target.ht_flank_armor
    else:
        ammo = "HV"
        firepower = weapon.firepower_hv if weapon.firepower_hv else 0
        armor = target.hv_front_armor if target_side == "Front" else target.hv_flank_armor
    
    differential = firepower - armor
    row_index = pick_row_index(differential, ammo)
    if row_index is None:
        return None, None, None, ammo, firepower, armor
    
    base_col = base_column_for_range(weapon, range_hexes)
    if base_col is None:
        return None, None, None, ammo, firepower, armor
    
    total_shifts = column_shifts - leadership + fear
    final_col = base_col + total_shifts
    if final_col > 10:
        return None, base_col, final_col, ammo, firepower, armor
    if final_col < 1:
        final_col = 1
    
    kn = KILL_TABLE[row_index].kills[final_col - 1]
    return kn, base_col, final_col, ammo, firepower, armor

# ============================================================
# INFANTRY FIRE TABLE - UUSI LOGIIKKA JA OHEINEN TAULUKKO
# FIREPOWER → RIVI (pysyy samana)
# DIE ROLL + MODIFIERS → KOLUMNI
#
# Kolumnilogiikka oheisen kuvan mukaan:
# - Die roll + modifiers ≤ 1 → Kolumni B (index 0)
# - Die roll + modifiers 2-4 → Kolumni C (index 1)
# - Die roll + modifiers 5-6 → Kolumni D (index 2)
# - Die roll + modifiers 7-8 → Kolumni E (index 3)
# - Die roll + modifiers 9-10 → Kolumni F (index 4)
# - Die roll + modifiers 11-12 → Kolumni G (index 5)
# - Die roll + modifiers 13+ → Kolumni H (index 6)
# ============================================================

# Firepower values (ROW headers) - määrittää RIVIN
FIREPOWER_ROWS = [2, 4, 6, 8, 10, 12, 14, 16, 18, 21, 24, 28, 32, 36, 48, 60, 80, 100, 120]

# Column headers for display (B, C, D, E, F, G, H)
COLUMN_LETTERS = ['B', 'C', 'D', 'E', 'F', 'G', 'H']

# Infantry Fire Table - OHEISEN TAULUKON MUKAAN
# Key = Firepower (RIVI), Value = List of results for each column (B, C, D, E, F, G, H)
INFANTRY_FIRE_TABLE = {
    # Firepower: [Col B(≤1), Col C(2-4), Col D(5-6), Col E(7-8), Col F(9-10), Col G(11-12), Col H(13+)]
    2:   ["E", "E", "E", "F", "2", "1", "0"],
    4:   ["E", "E", "E", "F", "2", "1", "0"],
    6:   ["E", "E", "F", "F", "2", "1", "0"],
    8:   ["E", "E", "F", "2", "2", "1", "0"],
    10:  ["E", "F", "F", "2", "1", "1", "0"],
    12:  ["E", "F", "F", "2", "1", "0", "0"],
    14:  ["E", "F", "2", "2", "1", "0", "0"],
    16:  ["F", "F", "2", "1", "1", "0", "0"],
    18:  ["F", "F", "2", "1", "0", "0", "0"],
    21:  ["F", "2", "2", "1", "0", "0", "0"],
    24:  ["F", "2", "1", "1", "0", "0", "0"],
    28:  ["F", "2", "1", "0", "0", "0", "0"],
    32:  ["2", "2", "1", "0", "0", "0", "0"],
    36:  ["2", "1", "1", "0", "0", "0", "0"],
    48:  ["2", "1", "0", "0", "0", "0", "0"],
    60:  ["1", "1", "0", "0", "0", "0", "0"],
    80:  ["1", "0", "0", "0", "0", "0", "0"],
    100: ["1", "0", "0", "0", "0", "0", "0"],
    120: ["0", "0", "0", "0", "0", "0", "0"],
}

def get_column_index_from_modified_roll(modified_roll: int) -> int:
    """
    Määrittää kolumni-indeksin nopan ja modifierien yhteistuloksen perusteella.
    Logiikka oheisen kuvan mukaan:
    
    Modified roll → Column index
    ≤ 1   → 0 (Column B)
    2-4   → 1 (Column C)
    5-6   → 2 (Column D)
    7-8   → 3 (Column E)
    9-10  → 4 (Column F)
    11-12 → 5 (Column G)
    13+   → 6 (Column H)
    """
    if modified_roll <= 1:
        return 0  # Column B
    elif modified_roll <= 4:
        return 1  # Column C (covers 2, 3, 4)
    elif modified_roll <= 6:
        return 2  # Column D (covers 5, 6)
    elif modified_roll <= 8:
        return 3  # Column E (covers 7, 8)
    elif modified_roll <= 10:
        return 4  # Column F (covers 9, 10)
    elif modified_roll <= 12:
        return 5  # Column G (covers 11, 12)
    else:
        return 6  # Column H (13+)

def infantry_fire_table_lookup(firepower_input: int, die_roll: int, modifiers: int = 0) -> Dict[str, Any]:
    """
    Infantry Fire Table Lookup - UUSI LOGIIKKA JA OHEINEN TAULUKKO
    
    FIREPOWER → RIVI (ei muutu)
    DIE ROLL + MODIFIERS → KOLUMNI
    """
    # 1. Find nearest firepower row
    chosen_firepower = min(FIREPOWER_ROWS, key=lambda fp: abs(fp - firepower_input))
    
    # 2. Calculate modified die roll (determines COLUMN)
    modified_roll = die_roll + modifiers
    
    # 3. Determine column index based on the new logic
    col_index = get_column_index_from_modified_roll(modified_roll)
    column_letter = COLUMN_LETTERS[col_index]
    
    # Column range description for display
    col_ranges = {
        0: "≤1",
        1: "2-4",
        2: "5-6",
        3: "7-8",
        4: "9-10",
        5: "11-12",
        6: "13+"
    }
    col_range_description = col_ranges[col_index]
    
    # 4. Lookup value from table
    if chosen_firepower in INFANTRY_FIRE_TABLE:
        row_data = INFANTRY_FIRE_TABLE[chosen_firepower]
        # Ensure col_index is within bounds for the row_data
        if col_index < len(row_data):
            raw_value = row_data[col_index]
        else:
            raw_value = "0" # Default to 'No effect' if column index somehow exceeds table data
    else:
        raw_value = "0" # Default to 'No effect' if chosen_firepower is not in table (shouldn't happen with min logic)
    
    # 5. Decode result
    decode_map = {
        "E": "ALL ELIMINATED",
        "F": "FLIP + OFFICER CHECK",
        "2": "ADD 2 FEAR MARKERS",
        "1": "ADD 1 FEAR MARKER",
        "0": "NO EFFECT"
    }
    decoded = decode_map.get(raw_value, raw_value)
    
    return {
        "result": raw_value,
        "raw": raw_value,
        "chosen_firepower": chosen_firepower,
        "die_roll": die_roll,
        "modifiers": modifiers,
        "modified_roll": modified_roll,
        "col_index": col_index,
        "column_letter": column_letter,
        "col_range_description": col_range_description,
        "decoded": decoded,
        "table_coord": f"{column_letter}{FIREPOWER_ROWS.index(chosen_firepower) + 2}" # +2 because row 1 (header) and Firepower is 1st data row.
    }

def explain_infantry_result(result: str) -> str:
    """Explains the infantry combat result in detail"""
    result = result.strip().upper()
    
    explanations = {
        "0": """✅ NO EFFECT (0)

Ei vaikutusta kohteeseen.
Target is unaffected.

Ei pelkomerkkejä, ei vahinkoa.
No fear markers, no damage.""",
        
        "1": """⚠️ ADD 1 FEAR MARKER (1)

Lisää 1 pelkomerkki kohteelle.
Add 1 fear marker to the target unit.

Yksikkö ei käänny, ei eliminoidu.
Unit is not flipped, not eliminated.""",
        
        "2": """⚠️⚠️ ADD 2 FEAR MARKERS (2)

Lisää 2 pelkomerkkiä kohteelle.
Add 2 fear markers to the target unit.

Yksikkö ei käänny, ei eliminoidu.
Unit is not flipped, not eliminated.""",
        
        "F": """💔 FLIP + OFFICER CHECK (F)

Yksikkö käännetään (flip to reduced side)
Flip the unit to its reduced side.

═══════════════════════════════════════
OFFICER CHECK - Jos upseeri on läsnä:
If an Officer is present, roll D10:
═══════════════════════════════════════

🎲 Roll D10:

  • 1-2: ☠️ UPSEERI ELIMINOITU
         Officer is eliminated
         → Lisää +2 Fear markers
         → Add +2 Fear markers to the unit
         
  • 3-10: ✅ UPSEERI SELVISI
          Officer survives
          → Lisää +1 Fear marker
          → Add +1 Fear marker to the unit

═══════════════════════════════════════
Jos ei upseeria: vain +1 Fear marker
If no officer: only +1 Fear marker
═══════════════════════════════════════""",
        
        "E": """🔥💀 ALL ELIMINATED (E)

KAIKKI TUHOTTU!
ALL UNITS ELIMINATED!

═══════════════════════════════════════
Koko yksikkö tuhottu kokonaan!
The entire unit is completely destroyed!

Poista yksikkö pelistä.
Remove the unit from play.

Ei pelkomerkkejä - yksikkö on poissa.
No fear markers - unit is gone.
═══════════════════════════════════════"""
    }
    
    return explanations.get(result, f"Result: {result}")

# ============================================================
# TKINTER GUI
# ============================================================

class TaisteluLaskuriUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FIRE TEAM 6.5 - Taistelulaskuri")
        self.root.geometry("900x1200")
        self.root.configure(bg='#2c3e50')
        self.current_weapon = None
        self.luo_ui()
    
    def luo_ui(self):
        # Header with tabs
        header_frame = tk.Frame(self.root, bg='#34495e', height=60)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        self.btn_ajoneuvotaistelu = tk.Button(
            header_frame, 
            text="AJONEUVOTAISTELU", 
            font=('Arial', 12, 'bold'), 
            bg='#3498db', 
            fg='#000000', 
            relief='flat', 
            cursor='hand2', 
            command=self.ajoneuvotaistelu_valittu
        )
        self.btn_ajoneuvotaistelu.place(x=10, y=10, width=435, height=40)
        
        self.btn_jv = tk.Button(
            header_frame, 
            text="JALKAVÄKITAISTELU", 
            font=('Arial', 12, 'bold'), 
            bg='#2ecc71', 
            fg='#000000', 
            relief='flat', 
            cursor='hand2', 
            command=self.jalkaväki_valittu
        )
        self.btn_jv.place(x=455, y=10, width=435, height=40)
        
        # Scrollable main canvas
        main_canvas = tk.Canvas(self.root, bg='#2c3e50', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = tk.Frame(main_canvas, bg='#2c3e50')
        
        self.scrollable_frame.bind(
            "<Configure>", 
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.ajoneuvotaistelu_valittu()
    
    def tyhjenna_nakyma(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def luo_osio_frame(self, otsikko):
        frame = tk.Frame(self.scrollable_frame, bg=self.bg_color, relief='raised', bd=2)
        frame.pack(pady=10, padx=20, fill='x')
        tk.Label(
            frame, 
            text=otsikko, 
            font=('Arial', 12, 'bold'), 
            bg=self.section_bg, 
            fg=self.text_color, 
            pady=8
        ).pack(fill='x')
        return frame
    
    # ============================================================
    # AJONEUVOTAISTELU (VEHICLE COMBAT)
    # ============================================================
    
    def ajoneuvotaistelu_valittu(self):
        self.tyhjenna_nakyma()
        self.btn_ajoneuvotaistelu.config(bg='#3498db')
        self.btn_jv.config(bg='#95a5a6')
        
        self.bg_color = '#D3D3D3'
        self.section_bg = '#E8E8E8'
        self.text_color = '#000000'
        
        ampuja_frame = self.luo_osio_frame("AMPUJA (SHOOTER)")
        
        tk.Label(ampuja_frame, text="Ase (Weapon)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.ase_var = tk.StringVar()
        self.ase_var.trace('w', self.on_weapon_selected)
        self.ase_combo = ttk.Combobox(ampuja_frame, textvariable=self.ase_var, values=get_all_weapon_names(), font=('Arial', 12), state='readonly', width=50)
        self.ase_combo.pack(pady=5, ipady=8)
        
        tk.Label(ampuja_frame, text="Leadership", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.leadership_var = tk.StringVar(value="0")
        lead_frame = tk.Frame(ampuja_frame, bg=self.section_bg)
        lead_frame.pack(pady=5)
        for i in range(4):
            tk.Radiobutton(lead_frame, text=f"+{i}" if i > 0 else "0", variable=self.leadership_var, value=str(i), font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)
        
        tk.Label(ampuja_frame, text="Fear", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.fear_var = tk.StringVar(value="0")
        fear_frame = tk.Frame(ampuja_frame, bg=self.section_bg)
        fear_frame.pack(pady=5)
        for i in range(3):
            tk.Radiobutton(fear_frame, text=f"+{i}" if i > 0 else "0", variable=self.fear_var, value=str(i), font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)
        
        tk.Label(ampuja_frame, text="Etäisyys (Range in hexes)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.range_var = tk.StringVar()
        self.range_var.trace('w', self.tarkista_valmiudet)
        ttk.Entry(ampuja_frame, textvariable=self.range_var, font=('Arial', 12), width=52).pack(pady=5, ipady=8)
    
    def on_weapon_selected(self, *args):
        weapon_name = self.ase_var.get()
        if not weapon_name:
            return
            
        self.current_weapon = get_weapon_by_name(weapon_name)
        
        if self.current_weapon:
            self.nayta_modifierit()
            self.tarkista_valmiudet()
    
    def nayta_modifierit(self):
        # Clean up old widgets
        if hasattr(self, 'shooter_mod_frame'):
            self.shooter_mod_frame.destroy()
        if hasattr(self, 'target_mod_frame'):
            self.target_mod_frame.destroy()
        if hasattr(self, 'kohde_frame_main'):
            self.kohde_frame_main.destroy()
        if hasattr(self, 'laske_btn'):
            self.laske_btn.destroy()
        if hasattr(self, 'tulos_frame'):
            self.tulos_frame.destroy()
        
        is_missile = self.current_weapon.wtype in ("MSL", "SAM")
        
        # Shooter modifiers
        self.shooter_mod_frame = self.luo_osio_frame("AMPUJAN MODIFIERIT (Shooter Modifiers - Column Shift)")
        
        self.shooter_cautious_move = tk.BooleanVar()
        self.shooter_change_facing = tk.BooleanVar()
        self.shooter_opportunity_fire = tk.BooleanVar()
        self.shooter_moving_fire = tk.BooleanVar()
        self.shooter_out_of_smoke = tk.BooleanVar()
        self.shooter_night = tk.BooleanVar()
        self.shooter_firing_ramp = tk.BooleanVar()
        
        if is_missile:
            tk.Checkbutton(self.shooter_mod_frame, text="Cautious move (+4)", variable=self.shooter_cautious_move, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Change facing (+2)", variable=self.shooter_change_facing, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Opportunity fire (+1)", variable=self.shooter_opportunity_fire, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Label(self.shooter_mod_frame, text="Moving fire: Not allowed", font=('Arial', 10, 'italic'), bg=self.section_bg, fg='#c0392b').pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Out of smoke (+4)", variable=self.shooter_out_of_smoke, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Night (+2)", variable=self.shooter_night, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="In firing ramp (-1)", variable=self.shooter_firing_ramp, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        else:
            tk.Checkbutton(self.shooter_mod_frame, text="Cautious move (+3)", variable=self.shooter_cautious_move, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Change facing (+2)", variable=self.shooter_change_facing, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Opportunity fire (+1)", variable=self.shooter_opportunity_fire, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Moving fire (+3)", variable=self.shooter_moving_fire, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Out of smoke (+3)", variable=self.shooter_out_of_smoke, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Night (+2)", variable=self.shooter_night, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="In firing ramp (-1)", variable=self.shooter_firing_ramp, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        
        # Target selection
        self.kohde_frame_main = self.luo_osio_frame("KOHDE (TARGET)")
        tk.Label(self.kohde_frame_main, text="Kohde (Target)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.kohde_var = tk.StringVar()
        self.kohde_var.trace('w', self.tarkista_valmiudet)
        self.kohde_combo = ttk.Combobox(self.kohde_frame_main, textvariable=self.kohde_var, values=get_all_weapon_names(), font=('Arial', 12), state='readonly', width=50)
        self.kohde_combo.pack(pady=5, ipady=8)
        
        tk.Label(self.kohde_frame_main, text="Osuma-alue (Hit Location)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.target_side_var = tk.StringVar(value="Front")
        side_frame = tk.Frame(self.kohde_frame_main, bg=self.section_bg)
        side_frame.pack(pady=5)
        tk.Radiobutton(side_frame, text="Etu (Front)", variable=self.target_side_var, value="Front", font=('Arial', 11), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=20)
        tk.Radiobutton(side_frame, text="Kylki (Flank)", variable=self.target_side_var, value="Flank", font=('Arial', 11), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=20)
        
        # Target modifiers
        self.target_mod_frame = self.luo_osio_frame("KOHTEEN MODIFIERIT (Target Modifiers - Column Shift)")
        
        self.target_in_buildings = tk.BooleanVar()
        self.target_in_smoke = tk.BooleanVar()
        self.target_in_woods = tk.BooleanVar()
        self.target_defilade_fire_ramp = tk.BooleanVar()
        self.target_cautious_move = tk.BooleanVar()
        
        if is_missile:
            tk.Checkbutton(self.target_mod_frame, text="In buildings (+2)", variable=self.target_in_buildings, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="In smoke (+3)", variable=self.target_in_smoke, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="In woods (+2)", variable=self.target_in_woods, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="Defilade/fire ramp (+1)", variable=self.target_defilade_fire_ramp, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="Cautious move (+1)", variable=self.target_cautious_move, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        else:
            tk.Checkbutton(self.target_mod_frame, text="In buildings (+1)", variable=self.target_in_buildings, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="In smoke (+2)", variable=self.target_in_smoke, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="In woods (+2)", variable=self.target_in_woods, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="Defilade/fire ramp (+2)", variable=self.target_defilade_fire_ramp, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="Cautious move (+1)", variable=self.target_cautious_move, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        
        # Calculate button
        self.laske_btn = tk.Button(self.scrollable_frame, text="LASKE KILL NUMBER", font=('Arial', 14, 'bold'), bg='#cccccc', fg='#000000', relief='flat', command=self.laske_vehicle, state='disabled')
        self.laske_btn.pack(pady=30, ipady=15, ipadx=50)
        
        # Results frame
        self.tulos_frame = tk.Frame(self.scrollable_frame, bg='#1abc9c', relief='solid', bd=3)
        self.tulos_label = tk.Label(self.tulos_frame, text="", font=('Arial', 10, 'bold'), bg='#1abc9c', fg='#000000', justify='left')
        self.tulos_label.pack(pady=20, padx=20)
        
        self.heita_noppa_btn = tk.Button(self.tulos_frame, text="🎲 HEITÄ NOPPAA", font=('Arial', 12, 'bold'), bg='#f39c12', fg='#000000', relief='flat', command=self.heita_noppa_vehicle)
    
    def tarkista_valmiudet(self, *args):
        if hasattr(self, 'ase_var') and hasattr(self, 'kohde_var') and hasattr(self, 'range_var'):
            if self.ase_var.get() and self.kohde_var.get() and self.range_var.get():
                try:
                    int(self.range_var.get())
                    if hasattr(self, 'laske_btn'):
                        self.laske_btn.config(state='normal', bg='#2ecc71')
                except:
                    if hasattr(self, 'laske_btn'):
                        self.laske_btn.config(state='disabled', bg='#cccccc')
            else:
                if hasattr(self, 'laske_btn'):
                    self.laske_btn.config(state='disabled', bg='#cccccc')
    
    def laske_vehicle(self):
        try:
            if not self.current_weapon:
                messagebox.showerror("Virhe", "Valitse ase ensin")
                return
                
            target = get_weapon_by_name(self.kohde_var.get())
            
            if not target:
                messagebox.showerror("Virhe", "Valitse kohde")
                return
            
            range_hexes = int(self.range_var.get())
            leadership = int(self.leadership_var.get())
            fear = int(self.fear_var.get())
            target_side = self.target_side_var.get()
            
            is_missile = self.current_weapon.wtype in ("MSL", "SAM")
            
            column_shifts = 0
            mod_list = []
            
            if self.shooter_cautious_move.get():
                shift_val = 4 if is_missile else 3
                column_shifts += shift_val
                mod_list.append(f"Cautious move +{shift_val}")
                
            if self.shooter_change_facing.get():
                column_shifts += 2
                mod_list.append("Change facing +2")
                
            if self.shooter_opportunity_fire.get():
                column_shifts += 1
                mod_list.append("Opportunity fire +1")
                
            if self.shooter_moving_fire.get():
                if not is_missile:
                    column_shifts += 3
                    mod_list.append("Moving fire +3")
                    
            if self.shooter_out_of_smoke.get():
                shift_val = 4 if is_missile else 3
                column_shifts += shift_val
                mod_list.append(f"Out of smoke +{shift_val}")
                
            if self.shooter_night.get():
                column_shifts += 2
                mod_list.append("Night +2")
                
            if self.shooter_firing_ramp.get():
                column_shifts -= 1
                mod_list.append("In firing ramp -1")
            
            if self.target_in_buildings.get():
                shift_val = 2 if is_missile else 1
                column_shifts += shift_val
                mod_list.append(f"In buildings +{shift_val}")
                
            if self.target_in_smoke.get():
                shift_val = 3 if is_missile else 2
                column_shifts += shift_val
                mod_list.append(f"In smoke +{shift_val}")
                
            if self.target_in_woods.get():
                column_shifts += 2
                mod_list.append("In woods +2")
                
            if self.target_defilade_fire_ramp.get():
                shift_val = 1 if is_missile else 2
                column_shifts += shift_val
                mod_list.append(f"Defilade/fire ramp +{shift_val}")
                
            if self.target_cautious_move.get():
                column_shifts += 1
                mod_list.append("Cautious move +1")
            
            kn, base_col, final_col, ammo, firepower, armor = kill_number(
                self.current_weapon, target, target_side, range_hexes, 
                column_shifts, leadership, fear
            )
            
            self.viimeisin_kill_number = kn
            differential = firepower - armor
            
            mod_text = "\n".join(mod_list) if mod_list else "Ei modifiereita"
            total_shift = column_shifts - leadership + fear
            weapon_type_text = "Missile" if is_missile else "Gun/Rocket"
            
            tulos = f"""AJONEUVOTAISTELU (VEHICLE COMBAT)

Weapon Type: {weapon_type_text}
Weapon: {self.current_weapon.name} ({self.current_weapon.wtype})
Target: {target.name} ({target_side})
Ammo: {ammo}
Range: {range_hexes} hexes

Differential = Firepower - Armor
            = {firepower} - {armor}
            = {differential}

Base Column: {base_col if base_col else "N/A"}

Column Shift Modifiers:
{mod_text}
Modifier Total: {column_shifts:+d}

Leadership: -{leadership}
Fear: +{fear}

Total Column Shift: {total_shift:+d}
Final Column: {base_col if base_col else "N/A"} {total_shift:+d} = {final_col if final_col else "N/A"}

>>> KILL NUMBER: {kn if kn else "N/A"} <<<
"""
            
            self.tulos_label.config(text=tulos)
            self.tulos_frame.pack(pady=10, padx=20, fill='x')
            if kn:
                self.heita_noppa_btn.pack(pady=10)
            else:
                self.heita_noppa_btn.pack_forget()
        except Exception as e:
            messagebox.showerror("Virhe", f"Virhe laskennassa: {str(e)}")
    
    def heita_noppa_vehicle(self):
        if not hasattr(self, 'viimeisin_kill_number'):
            return
        noppa = random.randint(1, 10)
        kn = self.viimeisin_kill_number
        
        result_window = tk.Toplevel(self.root)
        result_window.title("Nopanheitto - Dice Roll")
        result_window.geometry("450x300")
        
        if kn and noppa <= kn:
            result_window.configure(bg='#27ae60')
            tulos = "🎯 TUHOTTU! 💥"
            selite = "Kohde on tuhottu!\nTarget destroyed!"
            vari = '#27ae60'
        else:
            result_window.configure(bg='#c0392b')
            tulos = "❌ EI VAIKUTUSTA"
            selite = "Ei vahinkoa\nNo effect"
            vari = '#c0392b'
        
        tk.Label(result_window, text=f"🎲 Noppa: {noppa}", font=('Arial', 20, 'bold'), bg=vari, fg='white').pack(pady=20)
        tk.Label(result_window, text=f"Kill Number: {kn}", font=('Arial', 14), bg=vari, fg='white').pack(pady=10)
        tk.Label(result_window, text=tulos, font=('Arial', 18, 'bold'), bg=vari, fg='white').pack(pady=10)
        tk.Label(result_window, text=selite, font=('Arial', 12), bg=vari, fg='white').pack(pady=10)
        tk.Button(result_window, text="OK", font=('Arial', 12, 'bold'), command=result_window.destroy, bg='white', fg=vari, width=15).pack(pady=20)
    
    # ============================================================
    # JALKAVÄKITAISTELU (INFANTRY COMBAT) - OHEISEN KUVAN MUKAAN
    # ============================================================
    
    def jalkaväki_valittu(self):
        self.tyhjenna_nakyma()
        self.btn_ajoneuvotaistelu.config(bg='#95a5a6')
        self.btn_jv.config(bg='#2ecc71')
        
        self.bg_color = '#C8E6C9'
        self.section_bg = '#A5D6A7'
        self.text_color = '#000000'
        
        # Info box
        info_frame = tk.Frame(self.scrollable_frame, bg='#FFF9C4', relief='solid', bd=2)
        info_frame.pack(pady=15, padx=20, fill='x')
        info_text = """📊 INFANTRY FIRE TABLE - UUSI LOGIIKKA JA OHEINEN TAULUKKO

✅ FIREPOWER → RIVI (pysyy samana)
   Firepower määrittää RIVIN taulukossa
   
✅ DIE ROLL + MODIFIERS → KOLUMNI
   Modified die roll määrittää KOLUMNIN
   
   Kolumnilogiikka oheisen kuvan mukaan:
   • ≤ 1 → Kolumni B (paras)
   • 2-4 → Kolumni C
   • 5-6 → Kolumni D
   • 7-8 → Kolumni E
   • 9-10 → Kolumni F
   • 11-12 → Kolumni G
   • 13+ → Kolumni H (huonoin)

ESIMERKKEJÄ:
   • Noppa 1 → Kolumni B
   • Noppa 2 → Kolumni C
   • Noppa 3 + 1 fear = 4 → Kolumni C
   • Noppa 5 → Kolumni D
   • Noppa 0 tai alle → Kolumni B

✅ TULOKSET:
   • E = ALL ELIMINATED
   • F = FLIP + OFFICER CHECK
   • 2 = ADD 2 FEAR MARKERS
   • 1 = ADD 1 FEAR MARKER
   • 0 = NO EFFECT"""
        
        tk.Label(info_frame, text=info_text, font=('Arial', 9), bg='#FFF9C4', fg='#000000', justify='left').pack(pady=10, padx=15)
        
        # Firepower input
        ampuja_frame = self.luo_osio_frame("📍 FIREPOWER → RIVI")
        tk.Label(ampuja_frame, text="Syötä Firepower (määrittää RIVIN)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_firepower_var = tk.StringVar()
        ttk.Entry(ampuja_frame, textvariable=self.jv_firepower_var, font=('Arial', 14, 'bold'), width=52, justify='center').pack(pady=5, ipady=10)
        
        # Die roll + modifiers
        noppa_frame = self.luo_osio_frame("📍 DIE ROLL + MODIFIERS → KOLUMNI")
        tk.Label(noppa_frame, text="Modified die roll määrittää KOLUMNIN (B, C, D, E, F, G, H)", font=('Arial', 9, 'italic'), bg=self.section_bg, fg='#1B5E20').pack(pady=(5, 10))
        
        tk.Label(noppa_frame, text="Leadership (vähentää - subtract)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_leadership_var = tk.StringVar(value="0")
        jv_lead = tk.Frame(noppa_frame, bg=self.section_bg)
        jv_lead.pack(pady=5)
        for i in range(4):
            tk.Radiobutton(jv_lead, text=f"-{i}" if i > 0 else "0", variable=self.jv_leadership_var, value=str(i), font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)
        
        tk.Label(noppa_frame, text="Fear (lisää - add)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_fear_var = tk.StringVar(value="0")
        jv_fear = tk.Frame(noppa_frame, bg=self.section_bg)
        jv_fear.pack(pady=5)
        for i in range(3):
            tk.Radiobutton(jv_fear, text=f"+{i}" if i > 0 else "0", variable=self.jv_fear_var, value=str(i), font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)
        
        # Terrain modifiers
        kohde_frame = self.luo_osio_frame("📍 TERRAIN MODIFIERIT")
        
        self.jv_defilade = tk.BooleanVar()
        self.jv_cautious = tk.BooleanVar()
        self.jv_wood_building = tk.BooleanVar()
        self.jv_stone_building = tk.BooleanVar()
        self.jv_woods_direct = tk.BooleanVar()
        self.jv_woods_indirect = tk.BooleanVar()
        self.jv_cover = tk.BooleanVar()
        self.jv_vehicle = tk.BooleanVar()
        self.jv_entrench_direct = tk.BooleanVar()
        self.jv_entrench_indirect = tk.BooleanVar()
        
        tk.Checkbutton(kohde_frame, text="Target in defilade (+2)", variable=self.jv_defilade, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target is cautious moving (+3)", variable=self.jv_cautious, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in wood buildings (+3)", variable=self.jv_wood_building, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in stone buildings (+4)", variable=self.jv_stone_building, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in woods vs. direct fire (+2)", variable=self.jv_woods_direct, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in woods vs. indirect fire (-1)", variable=self.jv_woods_indirect, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in cover (+1)", variable=self.jv_cover, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target is a vehicle (-2)", variable=self.jv_vehicle, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target entrenched vs. direct fire (+2)", variable=self.jv_entrench_direct, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target entrenched vs. indirect fire (+3)", variable=self.jv_entrench_indirect, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)
        
        # Calculate button
        tk.Button(self.scrollable_frame, text="🎲 HEITÄ NOPPAA JA HAE TULOS\nRoll Dice and Get Result", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='#FFFFFF', relief='flat', command=self.laske_infantry, cursor='hand2').pack(pady=30, ipady=15, ipadx=30)
        
        # Results frame
        self.tulos_frame = tk.Frame(self.scrollable_frame, bg='#1abc9c', relief='solid', bd=3)
        self.tulos_label = tk.Label(self.tulos_frame, text="", font=('Arial', 9, 'bold'), bg='#1abc9c', fg='#000000', justify='left')
        self.tulos_label.pack(pady=20, padx=20)
    
    def laske_infantry(self):
        try:
            fp_str = self.jv_firepower_var.get().strip()
            if not fp_str:
                messagebox.showerror("Virhe", "Syötä Firepower-arvo\nEnter Firepower value")
                return
                
            user_firepower = int(fp_str)
            if user_firepower < 1:
                messagebox.showerror("Virhe", "Firepower pitää olla vähintään 1\nFirepower must be at least 1")
                return
            
            leadership = int(self.jv_leadership_var.get())
            fear = int(self.jv_fear_var.get())
            
            die_roll = random.randint(1, 10)
            
            modifiers = 0
            mod_list = []
            
            if leadership > 0:
                modifiers -= leadership
                mod_list.append(f"Leadership -{leadership}")
            
            if fear > 0:
                modifiers += fear
                mod_list.append(f"Fear +{fear}")
            
            if self.jv_defilade.get():
                modifiers += 2
                mod_list.append("Defilade +2")
            if self.jv_cautious.get():
                modifiers += 3
                mod_list.append("Cautious moving +3")
            if self.jv_wood_building.get():
                modifiers += 3
                mod_list.append("Wood buildings +3")
            if self.jv_stone_building.get():
                modifiers += 4
                mod_list.append("Stone buildings +4")
            if self.jv_woods_direct.get():
                modifiers += 2
                mod_list.append("Woods (direct fire) +2")
            if self.jv_woods_indirect.get():
                modifiers -= 1
                mod_list.append("Woods (indirect fire) -1")
            if self.jv_cover.get():
                modifiers += 1
                mod_list.append("Cover +1")
            if self.jv_vehicle.get():
                modifiers -= 2
                mod_list.append("Vehicle -2")
            if self.jv_entrench_direct.get():
                modifiers += 2
                mod_list.append("Entrenched (direct) +2")
            if self.jv_entrench_indirect.get():
                modifiers += 3
                mod_list.append("Entrenched (indirect) +3")
            
            # OHEISEN KUVAN MUKAAN
            lookup_result = infantry_fire_table_lookup(user_firepower, die_roll, modifiers)
            
            result = lookup_result["result"]
            chosen_firepower = lookup_result["chosen_firepower"]
            modified_roll = lookup_result["modified_roll"]
            column_letter = lookup_result["column_letter"]
            col_range_description = lookup_result["col_range_description"]
            decoded = lookup_result["decoded"]
            table_coord = lookup_result["table_coord"]
            
            explanation = explain_infantry_result(result)
            
            mod_text = "\n".join(mod_list) if mod_list else "Ei modifiereita / No modifiers"
            
            if modifiers > 0:
                mod_text_sign = f"+{modifiers}"
            elif modifiers < 0:
                mod_text_sign = f"{modifiers}"
            else:
                mod_text_sign = "±0"
            
            # Result symbol with color coding
            result_symbol = {
                "E": "🔥💀",
                "F": "💔",
                "2": "⚠️⚠️",
                "1": "⚠️",
                "0": "✅"
            }.get(result, "")
            
            tulos = f"""╔═══════════════════════════════════════╗
║   INFANTRY FIRE TABLE - TULOS        ║
╚═══════════════════════════════════════╝

━━━ 1️⃣ FIREPOWER → RIVI ━━━
Firepower: {user_firepower}
→ Lähin firepower: {chosen_firepower}
→ RIVI (pysyy samana)

━━━ 2️⃣ DIE ROLL + MODIFIERS → KOLUMNI ━━━
Die Roll (D10): {die_roll}

Modifiers:
{mod_text}

Total Modifiers: {mod_text_sign}

Modified Die Roll:
{die_roll} {mod_text_sign} = {modified_roll}

→ KOLUMNI: {column_letter} (Modified Roll Range: {col_range_description})

━━━ 3️⃣ TABLE LOOKUP ━━━
Taulukon koordinaatti: {table_coord}
(Firepower {chosen_firepower}, Column {column_letter})

╔═══════════════════════════════════════╗
║  {result_symbol} TULOS: {result}
║  {decoded}
╚═══════════════════════════════════════╝

{explanation}
"""
            
            self.tulos_label.config(text=tulos)
            self.tulos_frame.pack(pady=10, padx=20, fill='x')
            
        except ValueError:
            messagebox.showerror("Virhe", "Syötä kelvollinen Firepower-arvo (numero)\nEnter valid Firepower value (number)")
        except Exception as e:
            messagebox.showerror("Virhe", f"Virhe laskennassa / Calculation error: {str(e)}")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = TaisteluLaskuriUI(root)
    root.mainloop()
