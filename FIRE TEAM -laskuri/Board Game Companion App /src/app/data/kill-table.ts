import { Ammo, WeaponData } from "./weapons";

export interface DiffRow {
  hv_threshold?: number;
  ht_threshold: number;
  kills: (number | null)[];
}

export const KILL_TABLE: DiffRow[] = [
  {
    hv_threshold: -1,
    ht_threshold: -1,
    kills: [1, 1, null, null, null, null, null, null, null, null],
  },
  {
    ht_threshold: 0,
    kills: [1, 1, 1, 1, 1, null, null, null, null, null],
  },
  {
    hv_threshold: 0,
    ht_threshold: 1,
    kills: [2, 2, 1, 1, 1, 1, 1, 1, 1, null],
  },
  {
    hv_threshold: 1,
    ht_threshold: 2,
    kills: [4, 3, 3, 2, 2, 2, 1, 1, 1, null],
  },
  {
    hv_threshold: 2,
    ht_threshold: 3,
    kills: [5, 5, 4, 4, 3, 2, 2, 1, 1, null],
  },
  {
    ht_threshold: 4,
    kills: [6, 6, 5, 4, 4, 3, 2, 1, 1, null],
  },
  {
    hv_threshold: 3,
    ht_threshold: 5,
    kills: [7, 6, 5, 5, 4, 3, 2, 2, 1, 1],
  },
  {
    ht_threshold: 6,
    kills: [8, 7, 6, 5, 4, 3, 3, 2, 1, 1],
  },
  {
    hv_threshold: 4,
    ht_threshold: 7,
    kills: [8, 7, 6, 5, 5, 4, 3, 2, 1, 1],
  },
  {
    hv_threshold: 5,
    ht_threshold: 8,
    kills: [9, 8, 7, 6, 5, 4, 3, 2, 1, 1],
  },
];

function baseColumnForRange(
  weapon: WeaponData,
  range_hexes: number
): number | null {
  if (!weapon.range_bands) return null;
  for (const band of weapon.range_bands) {
    if (band.rmin <= range_hexes && range_hexes <= band.rmax) {
      return band.col;
    }
  }
  return null;
}

function pickRowIndex(differential: number, ammo: Ammo): number | null {
  if (differential < -1) return null;
  if (ammo === "HV") {
    const hv_rows = KILL_TABLE.map((r, i) => ({
      i,
      th: r.hv_threshold,
    })).filter((x) => x.th !== undefined);
    const eligible = hv_rows.filter((x) => x.th! <= differential);
    if (eligible.length === 0) return null;
    return Math.max(...eligible.map((x) => x.i));
  }
  const eligible = KILL_TABLE.map((r, i) => ({
    i,
    th: r.ht_threshold,
  })).filter((x) => x.th <= differential);
  if (eligible.length === 0) return null;
  return Math.max(...eligible.map((x) => x.i));
}

export interface KillResult {
  kill_number: number | null;
  base_col: number | null;
  final_col: number | null;
  ammo: string;
  firepower: number;
  armor: number;
  differential: number;
}

export function calculateKillNumber(
  weapon: WeaponData,
  target: WeaponData,
  target_side: "Front" | "Flank",
  range_hexes: number,
  column_shifts: number,
  leadership: number,
  fear: number
): KillResult {
  let ammo: Ammo;
  let firepower: number;
  let armor: number;

  if (
    weapon.ammo_type === "HT" ||
    weapon.wtype === "MSL" ||
    weapon.wtype === "SAM" ||
    weapon.wtype === "RKT"
  ) {
    ammo = "HT";
    firepower = weapon.firepower_ht || 0;
    armor =
      target_side === "Front"
        ? target.ht_front_armor
        : target.ht_flank_armor;
  } else {
    ammo = "HV";
    firepower = weapon.firepower_hv || 0;
    armor =
      target_side === "Front"
        ? target.hv_front_armor
        : target.hv_flank_armor;
  }

  const differential = firepower - armor;
  const row_index = pickRowIndex(differential, ammo);
  if (row_index === null) {
    return {
      kill_number: null,
      base_col: null,
      final_col: null,
      ammo,
      firepower,
      armor,
      differential,
    };
  }

  const base_col = baseColumnForRange(weapon, range_hexes);
  if (base_col === null) {
    return {
      kill_number: null,
      base_col: null,
      final_col: null,
      ammo,
      firepower,
      armor,
      differential,
    };
  }

  const total_shifts = column_shifts - leadership + fear;
  let final_col = base_col + total_shifts;
  if (final_col > 10) {
    return {
      kill_number: null,
      base_col,
      final_col,
      ammo,
      firepower,
      armor,
      differential,
    };
  }
  if (final_col < 1) final_col = 1;

  let kn = KILL_TABLE[row_index].kills[final_col - 1];

  // Special override for base column 9
  if (base_col === 9) {
    if (ammo === "HV" && differential >= 5) kn = 2;
    if (ammo === "HT" && differential >= 8) kn = 2;
  }

  return {
    kill_number: kn,
    base_col,
    final_col,
    ammo,
    firepower,
    armor,
    differential,
  };
}
