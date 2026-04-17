import tkinter as tk
from tkinter import ttk, messagebox
import random
from dataclasses import dataclass, field
from typing import List, Optional, Literal, Dict, Any, NamedTuple

# ============================================================
# FIRE TEAM 6.5 - COMPLETE SYSTEM
# ============================================================

# --- Style Constants ---

FONT_HEADER = ('Arial', 12, 'bold')
FONT_SUBHEADER = ('Arial', 11, 'bold')
FONT_BODY = ('Arial', 10)
FONT_BODY_ITALIC = ('Arial', 10, 'italic')
FONT_SMALL = ('Arial', 9)
FONT_SMALL_BOLD = ('Arial', 9, 'bold')
FONT_SMALL_ITALIC = ('Arial', 9, 'italic')
FONT_LARGE = ('Arial', 14, 'bold')
FONT_ENTRY = ('Arial', 12)
FONT_ENTRY_LARGE = ('Arial', 14, 'bold')
FONT_DICE = ('Arial', 20, 'bold')
FONT_RESULT_TITLE = ('Arial', 18, 'bold')
FONT_RESULT_DETAIL = ('Arial', 14)
FONT_RADIOBUTTON = ('Arial', 11)

COLOR_BG_MAIN = '#2c3e50'
COLOR_HEADER_BG = '#34495e'
COLOR_BTN_VEHICLE = '#3498db'
COLOR_BTN_INFANTRY = '#2ecc71'
COLOR_BTN_INACTIVE = '#95a5a6'
COLOR_BTN_DISABLED = '#cccccc'
COLOR_BTN_ENABLED = '#2ecc71'
COLOR_RESULT_BG = '#1abc9c'
COLOR_DICE_BTN = '#f39c12'
COLOR_SUCCESS = '#27ae60'
COLOR_FAIL = '#c0392b'
COLOR_INFO_BG = '#FFF9C4'
COLOR_INFANTRY_BTN_BG = '#4CAF50'
COLOR_INFANTRY_HINT = '#1B5E20'
COLOR_TEXT_BLACK = '#000000'
COLOR_TEXT_WHITE = 'white'

VEHICLE_BG = '#D3D3D3'
VEHICLE_SECTION_BG = '#E8E8E8'

INFANTRY_BG = '#C8E6C9'
INFANTRY_SECTION_BG = '#A5D6A7'

# --- Type Definitions ---

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
    range_bands: Optional[List[RangeBand]] = field(default=None)
    hv_front_armor: int = 0
    hv_flank_armor: int = 0
    ht_front_armor: int = 0
    ht_flank_armor: int = 0

# --- Weapon Database ---

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

_WEAPONS_BY_NAME: Dict[str, WeaponData] = {w.name: w for w in WEAPONS_DB}
_SORTED_WEAPON_NAMES: List[str] = sorted(w.name for w in WEAPONS_DB)

def get_weapon_by_name(name: str) -> Optional[WeaponData]:
    return _WEAPONS_BY_NAME.get(name)

def get_all_weapon_names() -> List[str]:
    return _SORTED_WEAPON_NAMES

# --- Vehicle Combat Kill Table ---

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
        eligible = [i for i, th in hv_rows if th <= differential]
        if not eligible:
            return None
        return max(eligible)
    eligible = [i for i, r in enumerate(KILL_TABLE) if r.ht_threshold <= differential]
    if not eligible:
        return None
    return max(eligible)

class KillResult(NamedTuple):
    kill_number: Optional[int]
    base_col: Optional[int]
    final_col: Optional[int]
    ammo: str
    firepower: int
    armor: int

def kill_number(weapon: WeaponData, target: WeaponData, target_side: Literal["Front", "Flank"], range_hexes: int, column_shifts: int, leadership: int, fear: int) -> KillResult:
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
        return KillResult(None, None, None, ammo, firepower, armor)

    base_col = base_column_for_range(weapon, range_hexes)
    if base_col is None:
        return KillResult(None, None, None, ammo, firepower, armor)

    total_shifts = column_shifts - leadership + fear
    final_col = base_col + total_shifts
    if final_col > 10:
        return KillResult(None, base_col, final_col, ammo, firepower, armor)
    if final_col < 1:
        final_col = 1

    kn = KILL_TABLE[row_index].kills[final_col - 1]
    return KillResult(kn, base_col, final_col, ammo, firepower, armor)

# ============================================================
# INFANTRY FIRE TABLE - LOPULLINEN VERSIO (14 RIVIÄ)
# ============================================================

# Kolumnikirjaimet B-T (19 kolumnia)
COLUMN_LETTERS = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

# Infantry Fire Table - 19 kolumnia, 14 riviä (modified die roll 1-14)
INFANTRY_FIRE_TABLE = {
    1:  ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "1"],
    2:  ["E", "E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1"],
    3:  ["E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1"],
    4:  ["E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1", "1"],
    5:  ["E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "0", "0", "0"],
    6:  ["E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1", "0", "0", "0"],
    7:  ["E", "E", "E", "E", "1", "1", "1", "F", "F", "F", "F", "2", "2", "1", "1", "1", "0", "0", "0"],
    8:  ["E", "E", "E", "F", "F", "F", "F", "F", "F", "2", "2", "2", "1", "1", "1", "0", "0", "0", "0"],
    9:  ["E", "E", "E", "F", "F", "F", "F", "2", "2", "2", "2", "1", "1", "1", "0", "0", "0", "0", "0"],
    10: ["E", "E", "E", "F", "F", "F", "F", "2", "2", "2", "2", "1", "1", "1", "0", "0", "0", "0", "0"],
    11: ["E", "E", "F", "F", "F", "F", "2", "2", "2", "2", "1", "1", "0", "0", "0", "0", "0", "0", "0"],
    12: ["F", "F", "F", "F", "F", "2", "2", "2", "2", "2", "1", "0", "0", "0", "0", "0", "0", "0", "0"],
    13: ["F", "F", "F", "F", "F", "2", "2", "2", "2", "2", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    14: ["F", "F", "F", "F", "F", "2", "2", "2", "2", "2", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
}

# Kolumnien firepower-alueet
COL_FP_RANGES = {
    0: "FP > 120",        # B
    1: "FP 100-119",      # C
    2: "FP 80-99",        # D
    3: "FP 60-79",        # E
    4: "FP 48-59",        # F
    5: "FP 36-47",        # G
    6: "FP 32-35",        # H
    7: "FP 28-31",        # I
    8: "FP 24-27",        # J
    9: "FP 21-23",        # K
    10: "FP 18-20",       # L
    11: "FP 16-17",       # M
    12: "FP 14-15",       # N
    13: "FP 12-13",       # O
    14: "FP 10-11",       # P
    15: "FP 8-9",         # Q
    16: "FP 6-7",         # R
    17: "FP 4-5",         # S
    18: "FP 2-3",         # T
}

# Tulosten selitykset
DECODE_MAP = {
    "E": "ALL ELIMINATED",
    "F": "FLIP + OFFICER CHECK",
    "2": "ADD 2 FEAR MARKERS",
    "1": "ADD 1 FEAR MARKER",
    "0": "NO EFFECT"
}

RESULT_SYMBOLS = {
    "E": "🔥💀",
    "F": "💔",
    "2": "⚠️⚠️",
    "1": "⚠️",
    "0": "✅"
}

INFANTRY_EXPLANATIONS = {
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

Lisää 2 pelkomerkkejä kohteelle.
Add 2 fear markers to the target unit.

Yksikkö ei käänny, ei eliminoidu.
Unit is not flipped, not eliminated.""",

    "F": """💔 FLIP + OFFICER CHECK (F)

Yksikkö käännetään (flip to reduced side)
Flip the unit to its reduced side.

════════════════════════════════════════
OFFICER CHECK - Jos upseeri on läsnä:
If an Officer is present, roll D10:
════════════════════════════════════════

🎲 Roll D10:

  • 1-2: ☠️ UPSEERI ELIMINOITU
         Officer is eliminated
         → Lisää +2 Fear markers
         → Add +2 Fear markers to the unit
         
  • 3-10: ✅ UPSEERI SELVISI
          Officer survives
          → Lisää +1 Fear marker
          → Add +1 Fear marker to the unit

════════════════════════════════════════
Jos ei upseeria: vain +1 Fear marker
If no officer: only +1 Fear marker
════════════════════════════════════════""",

    "E": """🔥💀 ALL ELIMINATED (E)

KAIKKI TUHOTTU!
ALL UNITS ELIMINATED!

════════════════════════════════════════
Koko yksikkö tuhottu kokonaan!
The entire unit is completely destroyed!

Poista yksikkö pelistä.
Remove the unit from play.

Ei pelkomerkkejä - yksikkö on poissa.
No fear markers - unit is gone.
════════════════════════════════════════"""
}

def get_column_index_from_firepower(firepower: int) -> int:
    """Määritä kolumni Firepower-arvon perusteella"""
    if firepower > 120:
        return 0
    elif firepower >= 100:
        return 1
    elif firepower >= 80:
        return 2
    elif firepower >= 60:
        return 3
    elif firepower >= 48:
        return 4
    elif firepower >= 36:
        return 5
    elif firepower >= 32:
        return 6
    elif firepower >= 28:
        return 7
    elif firepower >= 24:
        return 8
    elif firepower >= 21:
        return 9
    elif firepower >= 18:
        return 10
    elif firepower >= 16:
        return 11
    elif firepower >= 14:
        return 12
    elif firepower >= 12:
        return 13
    elif firepower >= 10:
        return 14
    elif firepower >= 8:
        return 15
    elif firepower >= 6:
        return 16
    elif firepower >= 4:
        return 17
    else:
        return 18

def infantry_fire_table_lookup(firepower_input: int, die_roll: int, modifiers: int = 0) -> Dict[str, Any]:
    """
    Infantry Fire Table Lookup
    1. FIREPOWER → KOLUMNI (B-T)
    2. DIE ROLL D10 + MODIFIERS → RIVI (1-14)
    3. Hae arvo suoraan taulukosta
    """
    col_index = get_column_index_from_firepower(firepower_input)
    column_letter = COLUMN_LETTERS[col_index]
    
    modified_roll = die_roll + modifiers
    
    # Rajoita rivi välille 1-14
    if modified_roll < 1:
        modified_roll = 1
    elif modified_roll > 14:
        modified_roll = 14
    
    raw_value = INFANTRY_FIRE_TABLE[modified_roll][col_index]
    decoded = DECODE_MAP.get(raw_value, raw_value)
    
    return {
        "result": raw_value,
        "chosen_row_key": modified_roll,
        "firepower_input": firepower_input,
        "die_roll": die_roll,
        "modifiers": modifiers,
        "modified_roll": modified_roll,
        "col_index": col_index,
        "column_letter": column_letter,
        "col_range_description": COL_FP_RANGES[col_index],
        "decoded": decoded,
        "table_coord": f"{column_letter}{modified_roll}"
    }

def explain_infantry_result(result: str) -> str:
    """Palauta yksityiskohtainen selitys tulokselle"""
    return INFANTRY_EXPLANATIONS.get(result.strip().upper(), f"Result: {result}")

# --- Vehicle Combat Modifier Definitions ---

SHOOTER_MODIFIERS = [
    ("Cautious move", "shooter_cautious_move", {"gun": 3, "msl": 4}),
    ("Change facing", "shooter_change_facing", {"gun": 2, "msl": 2}),
    ("Opportunity fire", "shooter_opportunity_fire", {"gun": 1, "msl": 1}),
    ("Moving fire", "shooter_moving_fire", {"gun": 3, "msl": None}),
    ("Out of smoke", "shooter_out_of_smoke", {"gun": 3, "msl": 4}),
    ("Night", "shooter_night", {"gun": 2, "msl": 2}),
    ("In firing ramp", "shooter_firing_ramp", {"gun": -1, "msl": -1}),
]

TARGET_MODIFIERS = [
    ("In buildings", "target_in_buildings", {"gun": 1, "msl": 2}),
    ("In smoke", "target_in_smoke", {"gun": 2, "msl": 3}),
    ("In woods", "target_in_woods", {"gun": 2, "msl": 2}),
    ("Defilade/fire ramp", "target_defilade_fire_ramp", {"gun": 2, "msl": 1}),
    ("Cautious move", "target_cautious_move", {"gun": 1, "msl": 1}),
]

# ============================================================
# TKINTER GUI
# ============================================================

class TaisteluLaskuriUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FIRE TEAM 6.5 - Taistelulaskuri")
        self.root.geometry("900x1200")
        self.root.configure(bg=COLOR_BG_MAIN)
        self.current_weapon = None
        self.luo_ui()

    def luo_ui(self):
        # Header napit
        header_frame = tk.Frame(self.root, bg=COLOR_HEADER_BG, height=60)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)

        self.btn_ajoneuvotaistelu = tk.Button(
            header_frame,
            text="AJONEUVOTAISTELU",
            font=FONT_HEADER,
            bg=COLOR_BTN_VEHICLE,
            fg=COLOR_TEXT_BLACK,
            relief='flat',
            cursor='hand2',
            command=self.ajoneuvotaistelu_valittu
        )
        self.btn_ajoneuvotaistelu.pack(side='left', expand=True, fill='both', padx=(5, 2), pady=5)

        self.btn_jv = tk.Button(
            header_frame,
            text="JALKAVÄKITAISTELU",
            font=FONT_HEADER,
            bg=COLOR_BTN_INFANTRY,
            fg=COLOR_TEXT_BLACK,
            relief='flat',
            cursor='hand2',
            command=self.jalkaväki_valittu
        )
        self.btn_jv.pack(side='left', expand=True, fill='both', padx=(2, 5), pady=5)

        # Scrollable main area
        self.main_canvas = tk.Canvas(self.root, bg=COLOR_BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg=COLOR_BG_MAIN)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=scrollbar.set)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Aloita ajoneuvotaistelulla
        self.ajoneuvotaistelu_valittu()

    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _validate_int(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def tyhjenna_nakyma(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def luo_osio_frame(self, otsikko):
        frame = tk.Frame(self.scrollable_frame, bg=self.bg_color, relief='raised', bd=2)
        frame.pack(pady=10, padx=20, fill='x')
        tk.Label(
            frame,
            text=otsikko,
            font=FONT_HEADER,
            bg=self.section_bg,
            fg=self.text_color,
            pady=8
        ).pack(fill='x')
        return frame

    def _create_modifier_checkboxes(self, parent, modifiers, mode_key):
        """Luo checkbox-lista modifiereille"""
        mod_vars = {}
        for label, attr_name, values in modifiers:
            var = tk.BooleanVar()
            mod_vars[attr_name] = var
            shift_val = values[mode_key]
            if shift_val is None:
                tk.Label(parent, text=f"{label}: Not allowed",
                         font=FONT_BODY_ITALIC, bg=self.section_bg, fg=COLOR_FAIL
                         ).pack(anchor='w', padx=20, pady=2)
            else:
                sign = "+" if shift_val >= 0 else ""
                tk.Checkbutton(parent, text=f"{label} ({sign}{shift_val})", variable=var,
                               font=FONT_BODY, bg=self.section_bg, fg=self.text_color,
                               selectcolor=self.bg_color
                               ).pack(anchor='w', padx=20, pady=2)
        return mod_vars

    def _calculate_modifier_shifts(self, mod_vars, modifiers, mode_key):
        """Laske yhteen valitut modifierit"""
        total = 0
        descriptions = []
        for label, attr_name, values in modifiers:
            if mod_vars[attr_name].get():
                shift_val = values[mode_key]
                if shift_val is not None:
                    total += shift_val
                    sign = "+" if shift_val >= 0 else ""
                    descriptions.append(f"{label} {sign}{shift_val}")
        return total, descriptions

    # ============================================================
    # AJONEUVOTAISTELU
    # ============================================================

    def ajoneuvotaistelu_valittu(self):
        self.tyhjenna_nakyma()
        self.btn_ajoneuvotaistelu.config(bg=COLOR_BTN_VEHICLE)
        self.btn_jv.config(bg=COLOR_BTN_INACTIVE)

        self.bg_color = VEHICLE_BG
        self.section_bg = VEHICLE_SECTION_BG
        self.text_color = COLOR_TEXT_BLACK

        # Ampuja
        ampuja_frame = self.luo_osio_frame("AMPUJA (SHOOTER)")

        tk.Label(ampuja_frame, text="Ase (Weapon)", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.ase_var = tk.StringVar()
        self.ase_var.trace_add('write', self.on_weapon_selected)
        ttk.Combobox(ampuja_frame, textvariable=self.ase_var, values=get_all_weapon_names(), font=FONT_ENTRY, state='readonly', width=50).pack(pady=5, ipady=8)

        tk.Label(ampuja_frame, text="Leadership", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.leadership_var = tk.StringVar(value="0")
        lead_frame = tk.Frame(ampuja_frame, bg=self.section_bg)
        lead_frame.pack(pady=5)
        for i in range(4):
            tk.Radiobutton(lead_frame, text=f"+{i}" if i > 0 else "0", variable=self.leadership_var, value=str(i), font=FONT_BODY, bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)

        tk.Label(ampuja_frame, text="Fear", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.fear_var = tk.StringVar(value="0")
        fear_frame = tk.Frame(ampuja_frame, bg=self.section_bg)
        fear_frame.pack(pady=5)
        for i in range(3):
            tk.Radiobutton(fear_frame, text=f"+{i}" if i > 0 else "0", variable=self.fear_var, value=str(i), font=FONT_BODY, bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)

        tk.Label(ampuja_frame, text="Etäisyys (Range in hexes)", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.range_var = tk.StringVar()
        self.range_var.trace_add('write', self.tarkista_valmiudet)
        vcmd = (self.root.register(self._validate_int), '%P')
        ttk.Entry(ampuja_frame, textvariable=self.range_var, font=FONT_ENTRY, width=52, validate='key', validatecommand=vcmd).pack(pady=5, ipady=8)

    def on_weapon_selected(self, *args):
        weapon_name = self.ase_var.get()
        if not weapon_name:
            return

        self.current_weapon = get_weapon_by_name(weapon_name)

        if self.current_weapon:
            self.nayta_modifierit()
            self.tarkista_valmiudet()

    def nayta_modifierit(self):
        # Poista vanhat
        for attr in ('shooter_mod_frame', 'target_mod_frame', 'kohde_frame_main', 'laske_btn', 'tulos_frame'):
            if hasattr(self, attr):
                getattr(self, attr).destroy()

        mode_key = "msl" if self.current_weapon.wtype in ("MSL", "SAM") else "gun"

        # Ampujan modifierit
        self.shooter_mod_frame = self.luo_osio_frame("AMPUJAN MODIFIERIT (Shooter Modifiers - Column Shift)")
        self.shooter_mod_vars = self._create_modifier_checkboxes(self.shooter_mod_frame, SHOOTER_MODIFIERS, mode_key)

        # Kohde
        self.kohde_frame_main = self.luo_osio_frame("KOHDE (TARGET)")
        tk.Label(self.kohde_frame_main, text="Kohde (Target)", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.kohde_var = tk.StringVar()
        self.kohde_var.trace_add('write', self.tarkista_valmiudet)
        ttk.Combobox(self.kohde_frame_main, textvariable=self.kohde_var, values=get_all_weapon_names(), font=FONT_ENTRY, state='readonly', width=50).pack(pady=5, ipady=8)

        tk.Label(self.kohde_frame_main, text="Osuma-alue (Hit Location)", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.target_side_var = tk.StringVar(value="Front")
        side_frame = tk.Frame(self.kohde_frame_main, bg=self.section_bg)
        side_frame.pack(pady=5)
        tk.Radiobutton(side_frame, text="Etu (Front)", variable=self.target_side_var, value="Front", font=FONT_RADIOBUTTON, bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=20)
        tk.Radiobutton(side_frame, text="Kylki (Flank)", variable=self.target_side_var, value="Flank", font=FONT_RADIOBUTTON, bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=20)

        # Kohteen modifierit
        self.target_mod_frame = self.luo_osio_frame("KOHTEEN MODIFIERIT (Target Modifiers - Column Shift)")
        self.target_mod_vars = self._create_modifier_checkboxes(self.target_mod_frame, TARGET_MODIFIERS, mode_key)

        # Laske-nappi
        self.laske_btn = tk.Button(self.scrollable_frame, text="LASKE KILL NUMBER", font=FONT_LARGE, bg=COLOR_BTN_DISABLED, fg=COLOR_TEXT_BLACK, relief='flat', command=self.laske_vehicle, state='disabled')
        self.laske_btn.pack(pady=30, ipady=15, ipadx=50)

        # Tuloskehys
        self.tulos_frame = tk.Frame(self.scrollable_frame, bg=COLOR_RESULT_BG, relief='solid', bd=3)
        self.tulos_label = tk.Label(self.tulos_frame, text="", font=FONT_BODY, bg=COLOR_RESULT_BG, fg=COLOR_TEXT_BLACK, justify='left')
        self.tulos_label.pack(pady=20, padx=20)

        self.heita_noppa_btn = tk.Button(self.tulos_frame, text="🎲 HEITÄ NOPPAA", font=FONT_HEADER, bg=COLOR_DICE_BTN, fg=COLOR_TEXT_BLACK, relief='flat', command=self.heita_noppa_vehicle)

    def tarkista_valmiudet(self, *args):
        if hasattr(self, 'ase_var') and hasattr(self, 'kohde_var') and hasattr(self, 'range_var'):
            if self.ase_var.get() and self.kohde_var.get() and self.range_var.get():
                try:
                    int(self.range_var.get())
                    if hasattr(self, 'laske_btn'):
                        self.laske_btn.config(state='normal', bg=COLOR_BTN_ENABLED)
                except ValueError:
                    if hasattr(self, 'laske_btn'):
                        self.laske_btn.config(state='disabled', bg=COLOR_BTN_DISABLED)
            else:
                if hasattr(self, 'laske_btn'):
                    self.laske_btn.config(state='disabled', bg=COLOR_BTN_DISABLED)

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

            mode_key = "msl" if self.current_weapon.wtype in ("MSL", "SAM") else "gun"

            shooter_shifts, shooter_descs = self._calculate_modifier_shifts(self.shooter_mod_vars, SHOOTER_MODIFIERS, mode_key)
            target_shifts, target_descs = self._calculate_modifier_shifts(self.target_mod_vars, TARGET_MODIFIERS, mode_key)

            column_shifts = shooter_shifts + target_shifts
            mod_list = shooter_descs + target_descs

            kn, base_col, final_col, ammo, firepower, armor = kill_number(
                self.current_weapon, target, target_side, range_hexes,
                column_shifts, leadership, fear
            )

            self.viimeisin_kill_number = kn
            differential = firepower - armor

            mod_text = "\n".join(mod_list) if mod_list else "Ei modifiereita"
            total_shift = column_shifts - leadership + fear
            weapon_type_text = "Missile" if mode_key == "msl" else "Gun/Rocket"

            tulos = f"""AJONEUVOTAISTELU (VEHICLE COMBAT)

Weapon Type: {weapon_type_text}
Weapon: {self.current_weapon.name} ({self.current_weapon.wtype})
Target: {target.name} ({target_side})
Ammo: {ammo}
Range: {range_hexes} hexes

Differential = Firepower - Armor
            = {firepower} - {armor}
            = {differential}

Base Column: {base_col if base_col is not None else "N/A"}

Column Shift Modifiers:
{mod_text}
Modifier Total: {column_shifts:+d}

Leadership: -{leadership}
Fear: +{fear}

Total Column Shift: {total_shift:+d}
Final Column: {base_col if base_col is not None else "N/A"} {total_shift:+d} = {final_col if final_col is not None else "N/A"}

>>> KILL NUMBER: {kn if kn is not None else "N/A"} <<<
"""

            self.tulos_label.config(text=tulos)
            self.tulos_frame.pack(pady=10, padx=20, fill='x')
            if kn is not None:
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

        if kn is not None and noppa <= kn:
            result_window.configure(bg=COLOR_SUCCESS)
            tulos = "🎯 TUHOTTU! 💥"
            selite = "Kohde on tuhottu!\nTarget destroyed!"
            vari = COLOR_SUCCESS
        else:
            result_window.configure(bg=COLOR_FAIL)
            tulos = "❌ EI VAIKUTUSTA"
            selite = "Ei vahinkoa\nNo effect"
            vari = COLOR_FAIL

        tk.Label(result_window, text=f"🎲 Noppa: {noppa}", font=FONT_DICE, bg=vari, fg=COLOR_TEXT_WHITE).pack(pady=20)
        tk.Label(result_window, text=f"Kill Number: {kn}", font=FONT_RESULT_DETAIL, bg=vari, fg=COLOR_TEXT_WHITE).pack(pady=10)
        tk.Label(result_window, text=tulos, font=FONT_RESULT_TITLE, bg=vari, fg=COLOR_TEXT_WHITE).pack(pady=10)
        tk.Label(result_window, text=selite, font=FONT_ENTRY, bg=vari, fg=COLOR_TEXT_WHITE).pack(pady=10)
        tk.Button(result_window, text="OK", font=FONT_HEADER, command=result_window.destroy, bg=COLOR_TEXT_WHITE, fg=vari, width=15).pack(pady=20)

    # ============================================================
    # JALKAVÄKITAISTELU
    # ============================================================

    def jalkaväki_valittu(self):
        self.tyhjenna_nakyma()
        self.btn_ajoneuvotaistelu.config(bg=COLOR_BTN_INACTIVE)
        self.btn_jv.config(bg=COLOR_BTN_INFANTRY)

        self.bg_color = INFANTRY_BG
        self.section_bg = INFANTRY_SECTION_BG
        self.text_color = COLOR_TEXT_BLACK

        # Info laatikko
        info_frame = tk.Frame(self.scrollable_frame, bg=COLOR_INFO_BG, relief='solid', bd=2)
        info_frame.pack(pady=15, padx=20, fill='x')
        info_text = """📊 INFANTRY FIRE TABLE (19 COLUMNS: B-T, 14 ROWS)

✅ FIREPOWER → KOLUMNI (B-T)
   Firepower määrittää KOLUMNIN taulukossa
   
✅ DIE ROLL + MODIFIERS → RIVI (1-14)
   Modified die roll määrittää RIVIN

✅ TULOKSET:
   • E = ALL ELIMINATED
   • F = FLIP + OFFICER CHECK
   • 2 = ADD 2 FEAR MARKERS
   • 1 = ADD 1 FEAR MARKER
   • 0 = NO EFFECT"""

        tk.Label(info_frame, text=info_text, font=FONT_SMALL, bg=COLOR_INFO_BG, fg=COLOR_TEXT_BLACK, justify='left').pack(pady=10, padx=15)

        # Firepower input
        ampuja_frame = self.luo_osio_frame("📍 FIREPOWER → KOLUMNI")
        tk.Label(ampuja_frame, text="Syötä Firepower (määrittää KOLUMNIN B-T)", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_firepower_var = tk.StringVar()
        ttk.Entry(ampuja_frame, textvariable=self.jv_firepower_var, font=FONT_ENTRY_LARGE, width=52, justify='center').pack(pady=5, ipady=10)

        # Modifierit
        noppa_frame = self.luo_osio_frame("📍 DIE ROLL + MODIFIERS → RIVI")
        tk.Label(noppa_frame, text="Modified die roll määrittää RIVIN taulukossa (1-14)", font=FONT_SMALL_ITALIC, bg=self.section_bg, fg=COLOR_INFANTRY_HINT).pack(pady=(5, 10))

        tk.Label(noppa_frame, text="Leadership (vähentää - subtract)", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_leadership_var = tk.StringVar(value="0")
        jv_lead = tk.Frame(noppa_frame, bg=self.section_bg)
        jv_lead.pack(pady=5)
        for i in range(4):
            tk.Radiobutton(jv_lead, text=f"-{i}" if i > 0 else "0", variable=self.jv_leadership_var, value=str(i), font=FONT_BODY, bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)

        tk.Label(noppa_frame, text="Fear (lisää - add)", font=FONT_SUBHEADER, bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_fear_var = tk.StringVar(value="0")
        jv_fear = tk.Frame(noppa_frame, bg=self.section_bg)
        jv_fear.pack(pady=5)
        for i in range(3):
            tk.Radiobutton(jv_fear, text=f"+{i}" if i > 0 else "0", variable=self.jv_fear_var, value=str(i), font=FONT_BODY, bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)

        # Terrain modifierit
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

        terrain_mods = [
            ("Target in defilade (+2)", self.jv_defilade),
            ("Target is cautious moving (+3)", self.jv_cautious),
            ("Target in wood buildings (+3)", self.jv_wood_building),
            ("Target in stone buildings (+4)", self.jv_stone_building),
            ("Target in woods vs. direct fire (+2)", self.jv_woods_direct),
            ("Target in woods vs. indirect fire (-1)", self.jv_woods_indirect),
            ("Target in cover (+1)", self.jv_cover),
            ("Target is a vehicle (-2)", self.jv_vehicle),
            ("Target entrenched vs. direct fire (+2)", self.jv_entrench_direct),
            ("Target entrenched vs. indirect fire (+3)", self.jv_entrench_indirect),
        ]
        for text, var in terrain_mods:
            tk.Checkbutton(kohde_frame, text=text, variable=var, font=FONT_BODY, bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(anchor='w', padx=20, pady=2)

        # Heitä noppaa -nappi
        tk.Button(self.scrollable_frame, text="🎲 HEITÄ NOPPAA JA HAE TULOS\nRoll Dice and Get Result", font=FONT_HEADER, bg=COLOR_INFANTRY_BTN_BG, fg=COLOR_TEXT_WHITE, relief='flat', command=self.laske_infantry, cursor='hand2').pack(pady=30, ipady=15, ipadx=30)

        # Tuloskehys
        self.tulos_frame = tk.Frame(self.scrollable_frame, bg=COLOR_RESULT_BG, relief='solid', bd=3)
        self.tulos_label = tk.Label(self.tulos_frame, text="", font=FONT_SMALL_BOLD, bg=COLOR_RESULT_BG, fg=COLOR_TEXT_BLACK, justify='left')
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

            # Heitä noppa
            die_roll = random.randint(1, 10)

            # Laske modifierit
            modifiers = 0
            mod_list = []

            if leadership > 0:
                modifiers -= leadership
                mod_list.append(f"Leadership -{leadership}")

            if fear > 0:
                modifiers += fear
                mod_list.append(f"Fear +{fear}")

            # Terrain modifierit
            terrain_checks = [
                (self.jv_defilade, 2, "Defilade +2"),
                (self.jv_cautious, 3, "Cautious moving +3"),
                (self.jv_wood_building, 3, "Wood buildings +3"),
                (self.jv_stone_building, 4, "Stone buildings +4"),
                (self.jv_woods_direct, 2, "Woods (direct fire) +2"),
                (self.jv_woods_indirect, -1, "Woods (indirect fire) -1"),
                (self.jv_cover, 1, "Cover +1"),
                (self.jv_vehicle, -2, "Vehicle -2"),
                (self.jv_entrench_direct, 2, "Entrenched (direct) +2"),
                (self.jv_entrench_indirect, 3, "Entrenched (indirect) +3"),
            ]
            for var, val, desc in terrain_checks:
                if var.get():
                    modifiers += val
                    mod_list.append(desc)

            # Hae tulos taulukosta
            lookup_result = infantry_fire_table_lookup(user_firepower, die_roll, modifiers)

            result = lookup_result["result"]
            chosen_row_key = lookup_result["chosen_row_key"]
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

            result_symbol = RESULT_SYMBOLS.get(result, "")

            tulos = f"""╔═══════════════════════════════════════╗
║   INFANTRY FIRE TABLE - TULOS        ║
╚═══════════════════════════════════════╝

━━━ 1️⃣ FIREPOWER → KOLUMNI ━━━
Firepower: {user_firepower}
→ KOLUMNI: {column_letter} ({col_range_description})

━━━ 2️⃣ DIE ROLL + MODIFIERS → RIVI ━━━
Die Roll (D10): {die_roll}

Modifiers:
{mod_text}

Total Modifiers: {mod_text_sign}

Modified Die Roll:
{die_roll} {mod_text_sign} = {modified_roll}

→ Rivi: {chosen_row_key} (rajoitettu 1-14)

━━━ 3️⃣ TABLE LOOKUP ━━━
Taulukon koordinaatti: {table_coord}
(Column {column_letter}, Row {chosen_row_key})

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
