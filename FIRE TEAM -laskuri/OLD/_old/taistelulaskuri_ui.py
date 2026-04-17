import tkinter as tk
from tkinter import ttk, messagebox
import random
from dataclasses import dataclass
from typing import List, Optional, Literal, Tuple

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
# INFANTRY FIRE TABLE - KORJATTU LOGIIKKA
# ============================================================

# Firepower headers (Rivi 1, numeerisina)
FIREPOWER_HEADERS = [2, 4, 6, 8, 10, 12, 14, 16, 18, 21, 24, 28, 32, 36, 48, 60, 80, 100, 120]

# Infantry Fire Table
# Kolumni A = Row key (1-14)
INFANTRY_FIRE_TABLE = {
    1:  ["E", "E", "E", "E", "E", "E", "1", "1", "1", "1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "no effect"],
    2:  ["E", "E", "E", "E", "E", "1", "1", "1", "1", "1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "no effect", "no effect"],
    3:  ["E", "E", "E", "E", "+2 fear", "1", "1", "1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect"],
    4:  ["E", "E", "E", "1", "1", "1", "1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect"],
    5:  ["E", "E", "1", "1", "1", "1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect"],
    6:  ["E", "1", "1", "1", "1", "1", "1", "+1 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect"],
    7:  ["1", "1", "1", "1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect"],
    8:  ["1", "1", "1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect"],
    9:  ["1", "1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect"],
    10: ["1", "1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect"],
    11: ["1", "1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect"],
    12: ["1", "+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect"],
    13: ["+2 fear", "+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect"],
    14: ["+2 fear", "+2 fear", "+2 fear", "+1 fear", "+1 fear", "+1 fear", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect", "no effect"],
}

def infantry_fire_table_lookup(firepower_input: int, die_roll: int, modifiers: int = 0):
    """
    Infantry Fire Table Lookup - KORJATTU LOGIIKKA
    
    UUSI SÄÄNTÖ:
    - Jos die_roll + modifiers ≤ 0 → käytä riviä 1 (paras mahdollinen tulos)
    - Jos die_roll + modifiers > 14 → käytä riviä 14 (huonoin taulukossa)
    
    Returns:
        dict with keys: result, raw, chosen_firepower_header, target_row_key, 
                       excel_row, excel_col, clamped, decoded
    """
    # 1. Valitse lähin firepower header
    chosen_firepower = min(FIREPOWER_HEADERS, key=lambda fp: abs(fp - firepower_input))
    chosen_col_index = FIREPOWER_HEADERS.index(chosen_firepower)
    excel_col_letter = chr(67 + chosen_col_index)  # C=67 (ASCII)
    excel_col_number = chosen_col_index + 3  # C=3, D=4, jne.
    
    # 2. Laske target row key (raaka arvo)
    target_row_key_raw = die_roll + modifiers
    
    # 3. KORJATTU: Clamp välille 1-14, JOS ≤ 0 → käytä 1
    clamped = False
    clamp_note = ""
    
    if target_row_key_raw <= 0:
        target_row_key = 1
        clamped = True
        clamp_note = f"Clamped {target_row_key_raw} → 1 (paras tulos)"
    elif target_row_key_raw > 14:
        target_row_key = 14
        clamped = True
        clamp_note = f"Clamped {target_row_key_raw} → 14 (huonoin tulos)"
    else:
        target_row_key = target_row_key_raw
    
    # 4. Hae tulos taulukosta
    raw_value = INFANTRY_FIRE_TABLE[target_row_key][chosen_col_index]
    excel_row = target_row_key + 1  # +1 koska header on row 1
    
    # 5. Decode tulos
    decode_map = {
        "+1 fear": "+1 FEAR",
        "+2 fear": "+2 FEAR",
        "1": "1 FLIP + OFFICER CHECK",
        "no effect": "NO EFFECT",
        "E": "ELIMINATED"
    }
    decoded = decode_map.get(raw_value, raw_value)
    
    return {
        "result": raw_value,
        "raw": raw_value,
        "chosen_firepower_header": chosen_firepower,
        "target_row_key_raw": target_row_key_raw,
        "target_row_key": target_row_key,
        "excel_row": excel_row,
        "excel_col": excel_col_letter,
        "excel_col_number": excel_col_number,
        "clamped": clamped,
        "clamp_note": clamp_note,
        "decoded": decoded
    }

def explain_infantry_result(result: str) -> str:
    """Selittää jalkaväkituloksen yksityiskohtaisesti"""
    result = result.strip().lower()
    
    explanations = {
        "no effect": "✅ NO EFFECT\nEi vaikutusta kohteeseen",
        "+1 fear": "⚠️ ADD 1 FEAR MARKER\nLisää 1 pelkomerkki (fear marker) kohteelle",
        "+2 fear": "⚠️⚠️ ADD 2 FEAR MARKERS\nLisää 2 pelkomerkkiä (fear markers) kohteelle",
        "1": "💔 UNIT FLIPPED + OFFICER CHECK\n\nYksikkö käännetään (flipped to reduced side)\n\nJos upseeri (Officer) on läsnä:\n  Heitä D10:\n  • 1-2: Upseeri eliminoitu (Officer eliminated)\n         → Lisää +2 Fear markers\n  • 3-10: Upseeri selvisi (Officer survives)\n          → Lisää +1 Fear marker",
        "e": "🔥 UNIT ELIMINATED\n\nYksikkö tuhottu kokonaan!\nPoista yksikkö pelistä."
    }
    return explanations.get(result, f"Tulos: {result}")

def get_excel_column_letter(index: int) -> str:
    """Muuntaa indeksin Excel-kolumnin kirjaimeksi (0=C, 1=D, 2=E, ...)"""
    return chr(67 + index)

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
    
    # [Ajoneuvotaistelu-koodi pysyy samana - jätetään pois tilan säästämiseksi]
    
    def on_weapon_selected(self, *args):
        weapon_name = self.ase_var.get()
        if not weapon_name:
            return
            
        self.current_weapon = get_weapon_by_name(weapon_name)
        
        if self.current_weapon:
            self.nayta_modifierit()
            self.tarkista_valmiudet()
    
    def nayta_modifierit(self):
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
        
        self.shooter_mod_frame = self.luo_osio_frame("AMPUJAN MODIFIERIT (Column Shift)")
        
        self.shooter_cautious_move = tk.BooleanVar()
        self.shooter_change_facing = tk.BooleanVar()
        self.shooter_opportunity_fire = tk.BooleanVar()
        self.shooter_moving_fire = tk.BooleanVar()
        self.shooter_out_of_smoke = tk.BooleanVar()
        self.shooter_night = tk.BooleanVar()
        self.shooter_firing_ramp = tk.BooleanVar()
        
        if is_missile:
            tk.Checkbutton(self.shooter_mod_frame, text="Cautious move (+4)", variable=self.shooter_cautious_move, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Change facing (+2)", variable=self.shooter_change_facing, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Opportunity fire (+1)", variable=self.shooter_opportunity_fire, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Label(self.shooter_mod_frame, text="Moving fire: Not allowed", font=('Arial', 10, 'italic'), bg=self.section_bg, fg='#c0392b').pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Out of smoke (+4)", variable=self.shooter_out_of_smoke, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Night (+2)", variable=self.shooter_night, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="In firing ramp (-1)", variable=self.shooter_firing_ramp, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        else:
            tk.Checkbutton(self.shooter_mod_frame, text="Cautious move (+3)", variable=self.shooter_cautious_move, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Change facing (+2)", variable=self.shooter_change_facing, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Opportunity fire (+1)", variable=self.shooter_opportunity_fire, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Moving fire (+3)", variable=self.shooter_moving_fire, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Out of smoke (+3)", variable=self.shooter_out_of_smoke, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="Night (+2)", variable=self.shooter_night, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.shooter_mod_frame, text="In firing ramp (-1)", variable=self.shooter_firing_ramp, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        
        self.kohde_frame_main = self.luo_osio_frame("KOHDE")
        tk.Label(self.kohde_frame_main, text="Kohde", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.kohde_var = tk.StringVar()
        self.kohde_var.trace('w', self.tarkista_valmiudet)
        self.kohde_combo = ttk.Combobox(self.kohde_frame_main, textvariable=self.kohde_var, values=get_all_weapon_names(), font=('Arial', 12), state='readonly', width=50)
        self.kohde_combo.pack(pady=5, ipady=8)
        
        tk.Label(self.kohde_frame_main, text="Osuma-alue", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.target_side_var = tk.StringVar(value="Front")
        side_frame = tk.Frame(self.kohde_frame_main, bg=self.section_bg)
        side_frame.pack(pady=5)
        tk.Radiobutton(side_frame, text="Etu (Front)", variable=self.target_side_var, value="Front", font=('Arial', 11), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=20)
        tk.Radiobutton(side_frame, text="Kylki (Flank)", variable=self.target_side_var, value="Flank", font=('Arial', 11), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=20)
        
        self.target_mod_frame = self.luo_osio_frame("KOHTEEN MODIFIERIT (Column Shift)")
        
        self.target_in_buildings = tk.BooleanVar()
        self.target_in_smoke = tk.BooleanVar()
        self.target_in_woods = tk.BooleanVar()
        self.target_defilade_fire_ramp = tk.BooleanVar()
        self.target_cautious_move = tk.BooleanVar()
        
        if is_missile:
            tk.Checkbutton(self.target_mod_frame, text="In buildings (+2)", variable=self.target_in_buildings, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="In smoke (+3)", variable=self.target_in_smoke, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="In woods (+2)", variable=self.target_in_woods, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="Defilade/fire ramp (+1)", variable=self.target_defilade_fire_ramp, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="Cautious move (+1)", variable=self.target_cautious_move, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        else:
            tk.Checkbutton(self.target_mod_frame, text="In buildings (+1)", variable=self.target_in_buildings, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="In smoke (+2)", variable=self.target_in_smoke, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="In woods (+2)", variable=self.target_in_woods, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="Defilade/fire ramp (+2)", variable=self.target_defilade_fire_ramp, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
            tk.Checkbutton(self.target_mod_frame, text="Cautious move (+1)", variable=self.target_cautious_move, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        
        self.laske_btn = tk.Button(self.scrollable_frame, text="LASKE KILL NUMBER", font=('Arial', 14, 'bold'), bg='#2ecc71', fg='#000000', relief='flat', command=self.laske_vehicle)
        self.laske_btn.pack(pady=30, ipady=15, ipadx=50)
        
        self.tulos_frame = tk.Frame(self.scrollable_frame, bg='#1abc9c', relief='solid', bd=3)
        self.tulos_label = tk.Label(self.tulos_frame, text="", font=('Arial', 10, 'bold'), bg='#1abc9c', fg='#000000', justify='left')
        self.tulos_label.pack(pady=20, padx=20)
        
        self.heita_noppa_btn = tk.Button(self.tulos_frame, text="🎲 HEITÄ NOPPAA", font=('Arial', 12, 'bold'), bg='#f39c12', fg='#000000', relief='flat', command=self.heita_noppa_vehicle)
    
    def ajoneuvotaistelu_valittu(self):
        self.tyhjenna_nakyma()
        self.btn_ajoneuvotaistelu.config(bg='#3498db')
        self.btn_jv.config(bg='#95a5a6')
        
        self.bg_color = '#D3D3D3'
        self.section_bg = '#E8E8E8'
        self.text_color = '#000000'
        
        ampuja_frame = self.luo_osio_frame("AMPUJA")
        
        tk.Label(ampuja_frame, text="Ase", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
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
        
        tk.Label(ampuja_frame, text="Etäisyys (hexiä)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.range_var = tk.StringVar()
        self.range_var.trace('w', self.tarkista_valmiudet)
        ttk.Entry(ampuja_frame, textvariable=self.range_var, font=('Arial', 12), width=52).pack(pady=5, ipady=8)
    
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
            
            tulos = f"""AJONEUVOTAISTELU

Weapon Type: {weapon_type_text}
Weapon: {self.current_weapon.name} ({self.current_weapon.wtype})
Target: {target.name} ({target_side})
Ammo: {ammo}
Range: {range_hexes} hexiä

Differential = Firepower - Armor
            = {firepower} - {armor}
            = {differential}

Base Column: {base_col}

Column Shift Modifiers:
{mod_text}
Modifier Total: {column_shifts:+d}

Leadership: -{leadership}
Fear: +{fear}

Total Column Shift: {total_shift:+d}
Final Column: {base_col} {total_shift:+d} = {final_col}

>>> KILL NUMBER: {kn if kn else "-"} <<<
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
        result_window.title("Nopanheitto")
        result_window.geometry("450x300")
        
        if kn and noppa <= kn:
            result_window.configure(bg='#27ae60')
            tulos = "🎯 TUHOTTU! 💥"
            selite = "Kohde on tuhottu!"
            vari = '#27ae60'
        else:
            result_window.configure(bg='#c0392b')
            tulos = "❌ EI VAIKUTUSTA"
            selite = "Ei vahinkoa"
            vari = '#c0392b'
        
        tk.Label(result_window, text=f"🎲 Noppa: {noppa}", font=('Arial', 20, 'bold'), bg=vari, fg='white').pack(pady=20)
        tk.Label(result_window, text=f"Kill Number: {kn}", font=('Arial', 14), bg=vari, fg='white').pack(pady=10)
        tk.Label(result_window, text=tulos, font=('Arial', 18, 'bold'), bg=vari, fg='white').pack(pady=10)
        tk.Label(result_window, text=selite, font=('Arial', 12), bg=vari, fg='white').pack(pady=10)
        tk.Button(result_window, text="OK", font=('Arial', 12, 'bold'), command=result_window.destroy, bg='white', fg=vari, width=15).pack(pady=20)
    
    # ============================================================
    # JALKAVÄKITAISTELU - KORJATTU
    # ============================================================
    
    def jalkaväki_valittu(self):
        self.tyhjenna_nakyma()
        self.btn_ajoneuvotaistelu.config(bg='#95a5a6')
        self.btn_jv.config(bg='#2ecc71')
        
        self.bg_color = '#C8E6C9'
        self.section_bg = '#A5D6A7'
        self.text_color = '#000000'
        
        info_frame = tk.Frame(self.scrollable_frame, bg='#FFF9C4', relief='solid', bd=2)
        info_frame.pack(pady=15, padx=20, fill='x')
        info_text = """📊 INFANTRY FIRE TABLE - KORJATTU LOGIIKKA

✅ FIREPOWER → Lähin header → KOLUMNI

✅ DIE ROLL + MODIFIERS → RIVI
   → Jos ≤ 0: Käytä RIVIÄ 1 (paras tulos)
   → Jos > 14: Käytä RIVIÄ 14 (huonoin tulos)

✅ TULOKSET:
   • E = ELIMINATED
   • 1 = FLIP + OFFICER CHECK
   • +2 fear = ADD 2 FEAR
   • +1 fear = ADD 1 FEAR
   • no effect = NO EFFECT"""
        
        tk.Label(info_frame, text=info_text, font=('Arial', 9), bg='#FFF9C4', fg='#000000', justify='left').pack(pady=10, padx=15)
        
        ampuja_frame = self.luo_osio_frame("📍 FIREPOWER → KOLUMNI")
        tk.Label(ampuja_frame, text="Syötä Firepower", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_firepower_var = tk.StringVar()
        ttk.Entry(ampuja_frame, textvariable=self.jv_firepower_var, font=('Arial', 14, 'bold'), width=52, justify='center').pack(pady=5, ipady=10)
        
        noppa_frame = self.luo_osio_frame("📍 DIE ROLL + MODIFIERS → RIVI")
        tk.Label(noppa_frame, text="Jos ≤ 0 → Rivi 1 (paras), Jos > 14 → Rivi 14", font=('Arial', 9, 'italic'), bg=self.section_bg, fg='#B71C1C').pack(pady=(5, 10))
        
        tk.Label(noppa_frame, text="Leadership (vähentää)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_leadership_var = tk.StringVar(value="0")
        jv_lead = tk.Frame(noppa_frame, bg=self.section_bg)
        jv_lead.pack(pady=5)
        for i in range(4):
            tk.Radiobutton(jv_lead, text=f"-{i}" if i > 0 else "0", variable=self.jv_leadership_var, value=str(i), font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)
        
        tk.Label(noppa_frame, text="Fear (lisää)", font=('Arial', 11, 'bold'), bg=self.section_bg, fg=self.text_color).pack(pady=(10, 5))
        self.jv_fear_var = tk.StringVar(value="0")
        jv_fear = tk.Frame(noppa_frame, bg=self.section_bg)
        jv_fear.pack(pady=5)
        for i in range(3):
            tk.Radiobutton(jv_fear, text=f"+{i}" if i > 0 else "0", variable=self.jv_fear_var, value=str(i), font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color).pack(side='left', padx=10)
        
        kohde_frame = self.luo_osio_frame("📍 TERRAIN MODIFIERS")
        
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
        
        tk.Checkbutton(kohde_frame, text="Target in defilade (+2)", variable=self.jv_defilade, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target is cautious moving (+3)", variable=self.jv_cautious, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in wood buildings (+3)", variable=self.jv_wood_building, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in stone buildings (+4)", variable=self.jv_stone_building, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in woods vs. direct fire (+2)", variable=self.jv_woods_direct, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in woods vs. indirect fire (-1)", variable=self.jv_woods_indirect, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target in cover (+1)", variable=self.jv_cover, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target is a vehicle (-2)", variable=self.jv_vehicle, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target entrenched vs. direct fire 16.2 (+2)", variable=self.jv_entrench_direct, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        tk.Checkbutton(kohde_frame, text="Target entrenched vs. indirect fire 16.2 (+3)", variable=self.jv_entrench_indirect, font=('Arial', 10), bg=self.section_bg, fg=self.text_color, selectcolor=self.bg_color, activebackground=self.section_bg, activeforeground=self.text_color).pack(anchor='w', padx=20, pady=2)
        
        tk.Button(self.scrollable_frame, text="🎲 HEITÄ NOPPAA JA HAE TULOS", font=('Arial', 14, 'bold'), bg='#4CAF50', fg='#FFFFFF', relief='flat', command=self.laske_infantry, cursor='hand2').pack(pady=30, ipady=15, ipadx=30)
        
        self.tulos_frame = tk.Frame(self.scrollable_frame, bg='#1abc9c', relief='solid', bd=3)
        self.tulos_label = tk.Label(self.tulos_frame, text="", font=('Arial', 10, 'bold'), bg='#1abc9c', fg='#000000', justify='left')
        self.tulos_label.pack(pady=20, padx=20)
    
    def laske_infantry(self):
        try:
            fp_str = self.jv_firepower_var.get().strip()
            if not fp_str:
                messagebox.showerror("Virhe", "Syötä Firepower-arvo")
                return
                
            user_firepower = int(fp_str)
            if user_firepower < 1:
                messagebox.showerror("Virhe", "Firepower pitää olla vähintään 1")
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
            
            # KORJATTU LOOKUP
            lookup_result = infantry_fire_table_lookup(user_firepower, die_roll, modifiers)
            
            result = lookup_result["result"]
            chosen_fp = lookup_result["chosen_firepower_header"]
            target_row_key_raw = lookup_result["target_row_key_raw"]
            target_row_key = lookup_result["target_row_key"]
            excel_col = lookup_result["excel_col"]
            excel_row = lookup_result["excel_row"]
            excel_col_number = lookup_result["excel_col_number"]
            clamped = lookup_result["clamped"]
            clamp_note = lookup_result["clamp_note"]
            decoded = lookup_result["decoded"]
            
            explanation = explain_infantry_result(result)
            
            mod_text = "\n".join(mod_list) if mod_list else "Ei modifiereita"
            
            if modifiers > 0:
                mod_text_sign = f"+{modifiers}"
            elif modifiers < 0:
                mod_text_sign = f"{modifiers}"
            else:
                mod_text_sign = "±0"
            
            clamp_display = ""
            if clamped:
                clamp_display = f"\n⚠️ {clamp_note}"
            
            excel_coord = f"{excel_col}{excel_row}"
            
            tulos = f"""╔════════════════════════════════════════════╗
║     INFANTRY FIRE TABLE - TULOS           ║
╚════════════════════════════════════════════╝

━━━ 1️⃣ FIREPOWER → KOLUMNI ━━━
Syötetty Firepower: {user_firepower}
→ Lähin header: {chosen_fp}
→ Kolumni: {excel_col} (numero: {excel_col_number})

━━━ 2️⃣ DIE ROLL + MODIFIERS → RIVI ━━━
Die Roll (D10): {die_roll}

Modifiers:
{mod_text}

Total: {mod_text_sign}

Target Row Key (raaka):
{die_roll} {mod_text_sign} = {target_row_key_raw}{clamp_display}

Käytetty rivi (Kolumni A): {target_row_key}

━━━ 3️⃣ TABLE LOOKUP ━━━
Excel-koordinaatti: {excel_coord}
(Kolumni {excel_col}, Rivi {target_row_key})

╔════════════════════════════════════════════╗
║         >>> TULOS: {result.upper()} <<<           ║
║         ({decoded})                        ║
╚════════════════════════════════════════════╝

{explanation}
"""
            
            self.tulos_label.config(text=tulos)
            self.tulos_frame.pack(pady=10, padx=20, fill='x')
            
        except ValueError:
            messagebox.showerror("Virhe", "Syötä kelvollinen Firepower-arvo (numero)")
        except Exception as e:
            messagebox.showerror("Virhe", f"Virhe laskennassa: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaisteluLaskuriUI(root)
    root.mainloop()
