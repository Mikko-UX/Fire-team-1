# FIRE TEAM 6.5 - Taistelulaskuri (Combat Calculator)

**Purpose:** A Tkinter-based desktop GUI application that serves as a combat resolution calculator for the "Fire Team 6.5" tabletop wargame. It automates table lookups and die rolls for two combat types.

**Language:** Python 3 (uses `tkinter`, `random`, `dataclasses`)

---

## Architecture Overview

The application is a single-file, ~1010-line Python script with three logical layers:

1. **Data layer** (lines 11–135) — Data classes, weapon database, and kill table
2. **Combat logic layer** (lines 137–378) — Resolution functions for vehicle and infantry combat
3. **GUI layer** (lines 384–1010) — Tkinter UI in class `TaisteluLaskuriUI`

---

## Data Model

| Class | Description |
|---|---|
| `WeaponData` | Immutable dataclass holding a weapon/vehicle's name, side (US/SOVIET), type (GUN/RKT/MSL/SAM), firepower values (HV and HT), range bands, and armor values (front/flank for both HV and HT). |
| `RangeBand` | Maps a hex range interval to a base column number for table lookup. |
| `DiffRow` / `KILL_TABLE` | 10-row kill probability table indexed by firepower–armor differential and column. |

### Weapon Database (`WEAPONS_DB`)

14 predefined weapons/vehicles:

| Side | Weapons |
|---|---|
| **US** (9) | M-1, M-60, M-2, M-113, M-106, TOW MSL, Dragon MSL, Hellfire MSL, AH-64 |
| **Soviet** (5) | T-80, T-72, BMP-1, BMP-2, Mi-24 |

---

## Combat Systems

### 1. Vehicle Combat (Ajoneuvotaistelu)

**Core function:** `kill_number()`

Resolution steps:

1. Determine ammo type (HV or HT) based on weapon type.
2. Calculate **differential** = firepower − target armor (front or flank).
3. Look up the kill table row from the differential.
4. Determine **base column** from range in hexes.
5. Apply **column shifts**: shooter modifiers + target modifiers − leadership + fear.
6. Read the **kill number** from the table intersection.

The kill number is a D10 threshold: roll ≤ kill number = target destroyed.

#### Shooter Modifiers (Column Shift)

| Modifier | Gun Value | Missile Value |
|---|---|---|
| Cautious move | +3 | +4 |
| Change facing | +2 | +2 |
| Opportunity fire | +1 | +1 |
| Moving fire | +3 | Not allowed |
| Out of smoke | +3 | +4 |
| Night | +2 | +2 |
| In firing ramp | −1 | −1 |

#### Target Modifiers (Column Shift)

| Modifier | Gun Value | Missile Value |
|---|---|---|
| In buildings | +1 | +2 |
| In smoke | +2 | +3 |
| In woods | +2 | +2 |
| Defilade / fire ramp | +2 | +1 |
| Cautious move | +1 | +1 |

---

### 2. Infantry Combat (Jalkaväkitaistelu)

**Core function:** `infantry_fire_table_lookup()`

Resolution steps:

1. **Firepower** determines the table **row** (snapped to nearest of 19 predefined values: 2–120).
2. **D10 roll + modifiers** determines the table **column** (B through H).
3. Look up result from a 19×7 table.

#### Column Mapping

| Modified Roll | Column |
|---|---|
| ≤ 1 | B (best) |
| 2–4 | C |
| 5–6 | D |
| 7–8 | E |
| 9–10 | F |
| 11–12 | G |
| 13+ | H (worst) |

#### Result Codes

| Code | Meaning |
|---|---|
| **E** | All Eliminated — entire unit destroyed, remove from play |
| **F** | Flip + Officer Check — flip unit to reduced side, roll D10 for officer survival |
| **2** | Add 2 Fear Markers |
| **1** | Add 1 Fear Marker |
| **0** | No Effect |

#### Infantry Terrain Modifiers

| Modifier | Value |
|---|---|
| Target in defilade | +2 |
| Target cautious moving | +3 |
| Target in wood buildings | +3 |
| Target in stone buildings | +4 |
| Target in woods (direct fire) | +2 |
| Target in woods (indirect fire) | −1 |
| Target in cover | +1 |
| Target is a vehicle | −2 |
| Target entrenched (direct fire) | +2 |
| Target entrenched (indirect fire) | +3 |

---

## GUI Structure (`TaisteluLaskuriUI`)

- **Tab-style navigation** at the top with two buttons: "AJONEUVOTAISTELU" (blue) and "JALKAVÄKITAISTELU" (green).
- **Scrollable content area** that dynamically rebuilds when switching tabs.
- **Vehicle tab:** weapon selector, leadership/fear radio buttons, range input, shooter/target modifier checkboxes, calculate button, and a result panel with a "Roll Dice" button that opens a popup window.
- **Infantry tab:** firepower input, leadership/fear radio buttons, terrain modifier checkboxes, combined "Roll & Calculate" button, and an inline result display with detailed explanations.
- **UI labels and messages** are bilingual (Finnish primary, English secondary).

---

## Running the Application

```bash
python taistelulaskuri_ui.py
```

No external dependencies — only the Python standard library is required.
