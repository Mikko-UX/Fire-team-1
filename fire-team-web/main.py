from dataclasses import dataclass, field
from typing import List, Optional, Literal, Dict, Any, NamedTuple
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# ============================================================
# FIRE TEAM 6.5 - COMPLETE SYSTEM
# ============================================================

# --- Type Definitions ---

Side = Literal["US", "Soviet", "FIN"]
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

# --- Weapon Database - KORJATTU RKT-aseiden range bands (min range = 1) ---

WEAPONS_DB: List[WeaponData] = [
    # ============================================================
    # US WEAPONS
    # ============================================================
    WeaponData("Heli RKT", "US", "RKT", firepower_ht=6, ammo_type="HT",
               range_bands=[RangeBand(3, 6, 22), RangeBand(4, 23, 33), RangeBand(5, 34, 42), RangeBand(6, 43, 50)],
               hv_front_armor=1, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),
    
    WeaponData("Law RKT", "US", "RKT", firepower_ht=6, ammo_type="HT",
               range_bands=[RangeBand(2, 1, 1), RangeBand(4, 2, 2), RangeBand(6, 3, 3), RangeBand(7, 4, 5)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("Dragon MSL", "US", "MSL", firepower_ht=10, ammo_type="HT",
               range_bands=[RangeBand(3, 3, 10)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("TOW MSL", "US", "MSL", firepower_ht=15, ammo_type="HT",
               range_bands=[RangeBand(1, 7, 40), RangeBand(2, 6, 6), RangeBand(3, 5, 5), RangeBand(4, 4, 4), RangeBand(6, 2, 3)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("Hellfire MSL", "US", "MSL", firepower_ht=18, ammo_type="HT",
               range_bands=[RangeBand(1, 6, 55), RangeBand(2, 5, 5), RangeBand(3, 4, 4), RangeBand(4, 2, 2)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("Stinger SAM", "US", "MSL", firepower_ht=6, ammo_type="HT",
               range_bands=[RangeBand(4, 0, 20), RangeBand(5, 21, 25), RangeBand(6, 26, 30)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("M1", "US", "GUN", firepower_hv=16, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 7), RangeBand(2, 8, 11), RangeBand(3, 12, 14), RangeBand(4, 15, 18),
                           RangeBand(5, 19, 21), RangeBand(6, 22, 26), RangeBand(7, 27, 32)],
               hv_front_armor=10, hv_flank_armor=5, ht_front_armor=12, ht_flank_armor=6),
    
    WeaponData("M2", "US", "GUN", firepower_hv=7, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 11),
                           RangeBand(5, 12, 14), RangeBand(6, 15, 18), RangeBand(7, 19, 22)],
               hv_front_armor=4, hv_flank_armor=2, ht_front_armor=4, ht_flank_armor=2),
    
    WeaponData("AH-64", "US", "GUN", firepower_hv=4, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 11),
                           RangeBand(5, 12, 14), RangeBand(6, 15, 18), RangeBand(7, 19, 22)],
               hv_front_armor=2, hv_flank_armor=1, ht_front_armor=2, ht_flank_armor=1),
    
    WeaponData("M60a3", "US", "GUN", firepower_hv=12, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 6), RangeBand(2, 7, 9), RangeBand(3, 10, 11), RangeBand(4, 12, 13), RangeBand(5, 14, 16), RangeBand(6, 17, 22), RangeBand(7, 23, 30)],
               hv_front_armor=4, hv_flank_armor=2, ht_front_armor=8, ht_flank_armor=3),
    
    WeaponData("M  113", "US", "GUN", firepower_hv=0, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 3), RangeBand(2, 4, 6), RangeBand(3, 7, 9)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),
    
    WeaponData("M 163", "US", "RKT", firepower_hv=0, ammo_type="HV",
               range_bands=[RangeBand(2, 1, 3), RangeBand(3, 4, 5), RangeBand(4, 6, 6), RangeBand(5, 7, 7), RangeBand(6, 8, 8), RangeBand(7, 9, 9), RangeBand(8, 10, 10)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),
    
    # ============================================================
    # SOVIET WEAPONS
    # ============================================================
    WeaponData("RPG-16 RKT", "Soviet", "RKT", firepower_ht=6, ammo_type="HT",
               range_bands=[RangeBand(2, 1, 1), RangeBand(3, 2, 2), RangeBand(4, 3, 3), RangeBand(5, 4, 4)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),

    WeaponData("Sagger MSL", "Soviet", "MSL", firepower_ht=11, ammo_type="HT",
               range_bands=[RangeBand(1, 12, 37), RangeBand(3, 9, 11), RangeBand(4, 7, 8), RangeBand(6, 6, 6), RangeBand(8, 5, 5), RangeBand(10, 4, 4)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),

    WeaponData("Spandrel MSL", "Soviet", "MSL", firepower_ht=13, ammo_type="HT",
               range_bands=[RangeBand(1, 4, 40), RangeBand(2, 3, 3), RangeBand(4, 2, 2), RangeBand(5, 1, 1)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),

    WeaponData("Spigot MSL", "Soviet", "MSL", firepower_ht=13, ammo_type="HT",
               range_bands=[RangeBand(2, 5, 40), RangeBand(3, 4, 4), RangeBand(4, 3, 3), RangeBand(6, 2, 2), RangeBand(8, 1, 1)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),

    WeaponData("Spiral MSL", "Soviet", "MSL", firepower_ht=17, ammo_type="HT",
               range_bands=[RangeBand(1, 3, 40), RangeBand(2, 2, 2), RangeBand(3, 1, 1)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),

    WeaponData("SA-14 SAM", "Soviet", "SAM", firepower_ht=8, ammo_type="HT",
               range_bands=[RangeBand(3, 0, 20), RangeBand(4, 21, 30), RangeBand(5, 31, 40)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),

    WeaponData("AGS-17", "Soviet", "RKT", firepower_ht=6, ammo_type="HT",
               range_bands=[RangeBand(2, 1, 3), RangeBand(3, 4, 5), RangeBand(4, 6, 6), RangeBand(5, 7, 7), RangeBand(6, 8, 8), RangeBand(7, 9, 9), RangeBand(8, 10, 10)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),

    WeaponData("SPG-9", "Soviet", "RKT", firepower_ht=9, ammo_type="HT",
               range_bands=[RangeBand(2, 1, 2), RangeBand(3, 3, 3), RangeBand(4, 4, 4), RangeBand(5, 5, 5), RangeBand(6, 6, 6), RangeBand(7, 7, 7)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),

    WeaponData("BMP-1", "Soviet", "GUN", firepower_hv=9, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 10), RangeBand(5, 11, 12), RangeBand(6, 13, 14), RangeBand(7, 15, 16)],
               hv_front_armor=4, hv_flank_armor=2, ht_front_armor=4, ht_flank_armor=2),

    WeaponData("BMP-2", "Soviet", "GUN", firepower_hv=7, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 10), RangeBand(5, 11, 12), RangeBand(6, 13, 14), RangeBand(7, 15, 16)],
               hv_front_armor=4, hv_flank_armor=2, ht_front_armor=4, ht_flank_armor=2),

    WeaponData("ASU-85", "Soviet", "GUN", firepower_hv=6, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 8), RangeBand(4, 9, 10), RangeBand(5, 11, 12)],
               hv_front_armor=2, hv_flank_armor=1, ht_front_armor=2, ht_flank_armor=1),

    WeaponData("Mi-6", "Soviet", "GUN", firepower_hv=2, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 8), RangeBand(3, 9, 10)],
               hv_front_armor=1, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),

    WeaponData("Mi-24", "Soviet", "GUN", firepower_hv=4, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 11)],
               hv_front_armor=2, hv_flank_armor=1, ht_front_armor=2, ht_flank_armor=1),

    WeaponData("SAU-122", "Soviet", "GUN", firepower_hv=9, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 11), RangeBand(5, 12, 13)],
               hv_front_armor=2, hv_flank_armor=1, ht_front_armor=2, ht_flank_armor=1),

    WeaponData("T-80", "Soviet", "GUN", firepower_hv=10, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 7), RangeBand(2, 8, 9), RangeBand(3, 10, 11), RangeBand(4, 12, 13), RangeBand(5, 14, 15), RangeBand(6, 16, 18), RangeBand(7, 19, 21), RangeBand(8, 22, 25)],
               hv_front_armor=11, hv_flank_armor=4, ht_front_armor=11, ht_flank_armor=4),

    WeaponData("T-72", "Soviet", "GUN", firepower_hv=9, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 7), RangeBand(2, 8, 11), RangeBand(3, 12, 14), RangeBand(4, 15, 16), RangeBand(5, 17, 19), RangeBand(6, 20, 21), RangeBand(7, 22, 23), RangeBand(8, 24, 26)],
               hv_front_armor=10, hv_flank_armor=4, ht_front_armor=11, ht_flank_armor=4),

    WeaponData("T-62", "Soviet", "GUN", firepower_hv=14, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 10), RangeBand(5, 11, 12), RangeBand(6, 13, 14), RangeBand(7, 15, 17), RangeBand(8, 18, 20)],
               hv_front_armor=4, hv_flank_armor=2, ht_front_armor=8, ht_flank_armor=3),

    WeaponData("MT-LB", "Soviet", "GUN", firepower_hv=2, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 8), RangeBand(3, 9, 10)],
               hv_front_armor=1, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),

    WeaponData("BTR-80", "Soviet", "GUN", firepower_hv=3, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 8), RangeBand(4, 9, 10)],
               hv_front_armor=1, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),

    WeaponData("Heli RKT", "Soviet", "RKT", firepower_ht=6, ammo_type="HT",
               range_bands=[RangeBand(3, 6, 20), RangeBand(4, 21, 30), RangeBand(5, 31, 37)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    # ============================================================
    # FINNISH WEAPONS
    # ============================================================
    WeaponData("T-72", "FIN", "GUN", firepower_hv=17, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 7), RangeBand(2, 8, 11), RangeBand(3, 12, 14), RangeBand(4, 15, 16), RangeBand(5, 17, 19), RangeBand(6, 20, 21), RangeBand(7, 22, 23), RangeBand(8, 24, 26)],
               hv_front_armor=10, hv_flank_armor=4, ht_front_armor=11, ht_flank_armor=4),
    
    WeaponData("Leopard 2", "FIN", "GUN", firepower_hv=18, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 7), RangeBand(2, 8, 11), RangeBand(3, 12, 14), RangeBand(4, 15, 18),
                           RangeBand(5, 19, 21), RangeBand(6, 22, 26), RangeBand(7, 27, 32)],
               hv_front_armor=10, hv_flank_armor=5, ht_front_armor=12, ht_flank_armor=6),
    
    WeaponData("CV90C", "FIN", "GUN", firepower_hv=9, firepower_ht=3, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 5), RangeBand(2, 6, 7), RangeBand(3, 8, 9), RangeBand(4, 10, 11),
                           RangeBand(5, 12, 14), RangeBand(6, 15, 18), RangeBand(7, 19, 22)],
               hv_front_armor=6, hv_flank_armor=4, ht_front_armor=4, ht_flank_armor=2),
    
    WeaponData("BMP-1", "FIN", "GUN", firepower_ht=9, ammo_type="HT",
               range_bands=[RangeBand(1, 0, 4), RangeBand(2, 5, 5), RangeBand(3, 6, 6), RangeBand(4, 7, 7), RangeBand(5, 8, 8), RangeBand(6, 9, 10), RangeBand(7, 11, 12), RangeBand(8, 13, 14)],
               hv_front_armor=4, hv_flank_armor=2, ht_front_armor=4, ht_flank_armor=2),
    
    WeaponData("BMP-2", "FIN", "GUN", firepower_hv=7, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 4), RangeBand(2, 5, 6), RangeBand(3, 7, 8), RangeBand(4, 9, 10), RangeBand(5, 11, 12), RangeBand(6, 13, 14), RangeBand(7, 15, 17), RangeBand(8, 18, 20)],
               hv_front_armor=4, hv_flank_armor=2, ht_front_armor=4, ht_flank_armor=2),
    
    WeaponData("ZU-23", "FIN", "GUN", firepower_hv=6, ammo_type="HV",
               range_bands=[RangeBand(1, 0, 4), RangeBand(2, 5, 6), RangeBand(3, 7, 8), RangeBand(4, 9, 10), RangeBand(5, 11, 12), RangeBand(6, 13, 14), RangeBand(7, 15, 17)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("LAW", "FIN", "RKT", firepower_ht=6, ammo_type="HT",
               range_bands=[RangeBand(2, 1, 1), RangeBand(4, 2, 2), RangeBand(6, 3, 3), RangeBand(7, 4, 5)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("Pasi", "FIN", "GUN", firepower_hv=0, ammo_type="HV",
               range_bands=[RangeBand(2, 1, 1), RangeBand(3, 2, 3), RangeBand(4, 4, 5), RangeBand(5, 6, 6), RangeBand(6, 7, 8), RangeBand(7, 9, 10)],
               hv_front_armor=1, hv_flank_armor=0, ht_front_armor=1, ht_flank_armor=0),
    
    WeaponData("Musti", "FIN", "GUN", firepower_ht=9, ammo_type="HT",
               range_bands=[RangeBand(1, 0, 4), RangeBand(2, 5, 5), RangeBand(3, 6, 6), RangeBand(4, 7, 7), RangeBand(5, 8, 8), RangeBand(6, 9, 10), RangeBand(7, 11, 12), RangeBand(8, 13, 14)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("Spigot MSL", "FIN", "MSL", firepower_ht=13, ammo_type="HT",
               range_bands=[RangeBand(1, 4, 25), RangeBand(2, 3, 3), RangeBand(3, 2, 2), RangeBand(4, 1, 1)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("Apilas", "FIN", "GUN", firepower_ht=9, ammo_type="HT",
               range_bands=[RangeBand(2, 1, 1), RangeBand(4, 2, 2), RangeBand(6, 3, 3), RangeBand(7, 4, 5)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
    
    WeaponData("TOW", "FIN", "MSL", firepower_ht=15, ammo_type="HT",
               range_bands=[RangeBand(1, 7, 40), RangeBand(2, 6, 6), RangeBand(3, 5, 5), RangeBand(4, 4, 4), RangeBand(6, 2, 3)],
               hv_front_armor=0, hv_flank_armor=0, ht_front_armor=0, ht_flank_armor=0),
]

_WEAPONS_BY_NAME: Dict[str, WeaponData] = {w.name: w for w in WEAPONS_DB}
_SORTED_WEAPON_NAMES: List[str] = sorted(w.name for w in WEAPONS_DB)

def get_weapon_by_name(name: str) -> Optional[WeaponData]:
    return _WEAPONS_BY_NAME.get(name)

def get_all_weapon_names() -> List[str]:
    return _SORTED_WEAPON_NAMES

def get_weapons_by_side(side: Side) -> List[str]:
    """Palauttaa aakkosjärjestyksessä aseet tietylle puolelle"""
    return sorted([w.name for w in WEAPONS_DB if w.side == side])

def get_weapons_by_side_with_range_bands(side: Side) -> List[str]:
    """Palauttaa aakkosjärjestyksessä aseet tietylle puolelle jotka omaa range bands (ampuja)"""
    return sorted([w.name for w in WEAPONS_DB if w.side == side and w.range_bands])

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

def kill_number(weapon: WeaponData, target: WeaponData, target_side: Literal["Front", "Flank"], range_hexes: int, column_shifts: int, leadership: int, fear: int, shooter_modifiers: int = 0, target_modifiers: int = 0) -> KillResult:
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

    total_shifts = column_shifts - leadership + fear + shooter_modifiers + target_modifiers
    final_col = base_col + total_shifts
    if final_col > 10:
        return KillResult(None, base_col, final_col, ammo, firepower, armor)
    if final_col < 1:
        final_col = 1

    kn = KILL_TABLE[row_index].kills[final_col - 1]
    # special override for base column 9:
    # HV differential 5+ or HT differential 8+ yields kill number 2
    if base_col == 9:
        if ammo == "HV" and differential >= 5:
            kn = 2
        if ammo == "HT" and differential >= 8:
            kn = 2
    return KillResult(kn, base_col, final_col, ammo, firepower, armor)

# ============================================================
# INFANTRY FIRE TABLE
# ============================================================

COLUMN_LETTERS = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

INFANTRY_FIRE_TABLE = {
    1:  ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "1"],
    2:  ["E", "E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1"],
    3:  ["E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1"],
    4:  ["E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1", "1"],
    5:  ["E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "0", "0", "0"],
    6:  ["E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1", "0", "0", "0"],
    7:  ["E", "E", "E", "E", "1", "F", "1", "F", "F", "F", "F", "2", "2", "1", "1", "1", "0", "0", "0"],
    8:  ["E", "E", "E", "F", "F", "F", "F", "F", "F", "2", "2", "2", "1", "1", "1", "0", "0", "0", "0"],
    9:  ["E", "E", "E", "F", "F", "F", "F", "2", "2", "2", "2", "1", "1", "1", "0", "0", "0", "0", "0"],
    10: ["E", "E", "E", "F", "F", "F", "F", "2", "2", "2", "2", "1", "1", "1", "0", "0", "0", "0", "0"],
    11: ["E", "E", "F", "F", "F", "F", "2", "2", "2", "2", "1", "1", "0", "0", "0", "0", "0", "0", "0"],
    12: ["F", "F", "F", "F", "F", "2", "2", "2", "2", "2", "1", "0", "0", "0", "0", "0", "0", "0", "0"],
    13: ["F", "F", "F", "F", "F", "2", "2", "2", "2", "2", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    14: ["F", "F", "F", "F", "F", "2", "2", "2", "2", "2", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
}

COL_FP_RANGES = {
    0: "FP > 120", 1: "FP 100-119", 2: "FP 80-99", 3: "FP 60-79", 4: "FP 48-59",
    5: "FP 36-47", 6: "FP 32-35", 7: "FP 28-31", 8: "FP 24-27", 9: "FP 21-23",
    10: "FP 18-20", 11: "FP 16-17", 12: "FP 14-15", 13: "FP 12-13", 14: "FP 10-11",
    15: "FP 8-9", 16: "FP 6-7", 17: "FP 4-5", 18: "FP 2-3",
}

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

Target is unaffected.
No fear markers, no damage.""",

    "1": """⚠️ ADD 1 FEAR MARKER (1)

Add 1 fear marker to the target unit.
Unit is not flipped, not eliminated.""",

    "2": """⚠️⚠️ ADD 2 FEAR MARKERS (2)

Add 2 fear markers to the target unit.
Unit is not flipped, not eliminated.""",

    "F": """💔 FLIP + OFFICER CHECK (F)

Flip the unit to its reduced side.

════════════════════════════════════════
OFFICER CHECK - If an officer is present:
If an officer is present, roll D10:
════════════════════════════════════════

🎲 Roll D10:

  • 1-2: ☠️ OFFICER ELIMINATED
         Officer is eliminated
         → Add +2 Fear markers to the unit
         
  • 3-10: ✅ OFFICER SURVIVES
          Officer survives
          → Add +1 Fear marker to the unit

════════════════════════════════════════
If no officer: only +1 Fear marker
════════════════════════════════════════""",

    "E": """🔥💀 ALL ELIMINATED (E)

ALL UNITS ELIMINATED!

════════════════════════════════════════
The entire unit is completely destroyed!
Remove the unit from play.
No fear markers - unit is gone.
════════════════════════════════════════"""
}

def get_column_index_from_firepower(firepower: int) -> int:
    """Determine the column index based on the Firepower value."""
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
    """Infantry Fire Table Lookup"""
    col_index = get_column_index_from_firepower(firepower_input)
    column_letter = COLUMN_LETTERS[col_index]
    
    modified_roll = die_roll + modifiers
    
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

def calculate_hit_probability(
    combat_type,   # "vehicle" | "infantry"
    country,       # "us" | "soviet" | "fin"
    weapon,
    leadership,    # int 0-3
    fear,          # int 0-4
    range_hexes    # int
):
    """
    Calculate hit/miss probability based on combat parameters.
    """
    # --- placeholder formula ---
    base = 0.6
    base += leadership * 0.05
    base -= fear * 0.04
    base -= range_hexes * 0.02
    if country == "fin":
        base += 0.05
    hit = round(max(0.0, min(1.0, base)) * 100, 1)
    return {
        "hit_probability": hit,
        "miss_probability": round(100 - hit, 1),
    }

import os
from pathlib import Path

# Get the directory of the current script
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/weapons")
async def get_weapons():
    weapon_data = []
    for weapon in WEAPONS_DB:
        weapon_data.append({
            "name": weapon.name,
            "country": weapon.side,
            "type": weapon.wtype
        })
    return {"weapons": weapon_data}

@app.post("/api/vehicle-combat")
async def calculate_vehicle_combat(
    shooter_weapon: str = Form(...),
    target_weapon: str = Form(...),
    target_side: str = Form(...),
    range_hexes: int = Form(...),
    column_shifts: int = Form(...),
    leadership: int = Form(...),
    fear: int = Form(...),
    shooter_modifiers: int = Form(0),
    target_modifiers: int = Form(0)
):
    shooter = get_weapon_by_name(shooter_weapon)
    target = get_weapon_by_name(target_weapon)
    if not shooter or not target:
        return {"error": "Invalid weapon"}
    
    result = kill_number(shooter, target, target_side, range_hexes, column_shifts, leadership, fear, shooter_modifiers, target_modifiers)

    import random
    die_roll = random.randint(1, 10)
    if result.kill_number is None:
        solver = "No kill number available"
        hit = False
    else:
        hit = die_roll <= result.kill_number
        solver = "Target destroyed!" if hit else "No effect"

    return {
        "kill_number": result.kill_number,
        "base_col": result.base_col,
        "final_col": result.final_col,
        "ammo": result.ammo,
        "firepower": result.firepower,
        "armor": result.armor,
        "die_roll": die_roll,
        "hit": hit,
        "solver": solver,
        "hit_threshold": result.kill_number
    }

@app.post("/api/infantry-combat")
async def calculate_infantry_combat(
    firepower: int = Form(...),
    modifiers: int = Form(0),
    leadership: int = Form(1),
    fear: int = Form(1)
):
    # Generate random die roll (1-10) as in original
    import random
    die_roll = random.randint(1, 10)
    
    # Apply leadership and fear modifiers as in original
    total_modifiers = modifiers
    if leadership > 0:
        total_modifiers -= leadership
    if fear > 0:
        total_modifiers += fear
    
    result = infantry_fire_table_lookup(firepower, die_roll, total_modifiers)
    explanation = explain_infantry_result(result["result"])
    return {**result, "explanation": explanation, "leadership": leadership, "fear": fear}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)