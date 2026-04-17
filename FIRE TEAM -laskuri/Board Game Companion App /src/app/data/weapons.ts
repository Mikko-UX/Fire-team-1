export type Side = "US" | "Soviet" | "FIN";
export type Ammo = "HV" | "HT" | "SAM";
export type WeaponType = "GUN" | "RKT" | "MSL" | "SAM";

export interface RangeBand {
  col: number;
  rmin: number;
  rmax: number;
}

export interface WeaponData {
  name: string;
  side: Side;
  wtype: WeaponType;
  firepower_hv?: number;
  firepower_ht?: number;
  ammo_type?: Ammo;
  range_bands?: RangeBand[];
  hv_front_armor: number;
  hv_flank_armor: number;
  ht_front_armor: number;
  ht_flank_armor: number;
}

export const WEAPONS_DB: WeaponData[] = [
  // US WEAPONS
  {
    name: "Dragon MSL",
    side: "US",
    wtype: "MSL",
    firepower_ht: 10,
    ammo_type: "HT",
    range_bands: [{ col: 3, rmin: 3, rmax: 10 }],
    hv_front_armor: 0,
    hv_flank_armor: 0,
    ht_front_armor: 0,
    ht_flank_armor: 0,
  },
  {
    name: "TOW MSL",
    side: "US",
    wtype: "MSL",
    firepower_ht: 15,
    ammo_type: "HT",
    range_bands: [
      { col: 1, rmin: 7, rmax: 40 },
      { col: 2, rmin: 6, rmax: 6 },
      { col: 3, rmin: 5, rmax: 5 },
      { col: 4, rmin: 4, rmax: 4 },
      { col: 6, rmin: 2, rmax: 3 },
    ],
    hv_front_armor: 0,
    hv_flank_armor: 0,
    ht_front_armor: 0,
    ht_flank_armor: 0,
  },
  {
    name: "M1",
    side: "US",
    wtype: "GUN",
    firepower_hv: 16,
    ammo_type: "HV",
    range_bands: [
      { col: 1, rmin: 0, rmax: 7 },
      { col: 2, rmin: 8, rmax: 11 },
      { col: 3, rmin: 12, rmax: 14 },
      { col: 4, rmin: 15, rmax: 18 },
      { col: 5, rmin: 19, rmax: 21 },
      { col: 6, rmin: 22, rmax: 26 },
      { col: 7, rmin: 27, rmax: 32 },
    ],
    hv_front_armor: 10,
    hv_flank_armor: 5,
    ht_front_armor: 12,
    ht_flank_armor: 6,
  },
  {
    name: "M60a3",
    side: "US",
    wtype: "GUN",
    firepower_hv: 12,
    ammo_type: "HV",
    range_bands: [
      { col: 1, rmin: 0, rmax: 6 },
      { col: 2, rmin: 7, rmax: 9 },
      { col: 3, rmin: 10, rmax: 11 },
      { col: 4, rmin: 12, rmax: 13 },
      { col: 5, rmin: 14, rmax: 16 },
      { col: 6, rmin: 17, rmax: 22 },
      { col: 7, rmin: 23, rmax: 30 },
    ],
    hv_front_armor: 4,
    hv_flank_armor: 2,
    ht_front_armor: 8,
    ht_flank_armor: 3,
  },

  // SOVIET WEAPONS
  {
    name: "BMP-1",
    side: "Soviet",
    wtype: "GUN",
    firepower_ht: 9,
    ammo_type: "HT",
    range_bands: [
      { col: 1, rmin: 0, rmax: 4 },
      { col: 2, rmin: 5, rmax: 5 },
      { col: 3, rmin: 6, rmax: 6 },
      { col: 4, rmin: 7, rmax: 7 },
      { col: 5, rmin: 8, rmax: 8 },
      { col: 6, rmin: 9, rmax: 10 },
      { col: 7, rmin: 11, rmax: 12 },
      { col: 8, rmin: 13, rmax: 14 },
    ],
    hv_front_armor: 4,
    hv_flank_armor: 2,
    ht_front_armor: 4,
    ht_flank_armor: 2,
  },
  {
    name: "T-80",
    side: "Soviet",
    wtype: "GUN",
    firepower_hv: 17,
    ammo_type: "HV",
    range_bands: [
      { col: 1, rmin: 0, rmax: 7 },
      { col: 2, rmin: 8, rmax: 11 },
      { col: 3, rmin: 12, rmax: 14 },
      { col: 4, rmin: 15, rmax: 16 },
      { col: 5, rmin: 17, rmax: 19 },
      { col: 6, rmin: 20, rmax: 21 },
      { col: 7, rmin: 22, rmax: 23 },
      { col: 8, rmin: 24, rmax: 26 },
    ],
    hv_front_armor: 10,
    hv_flank_armor: 4,
    ht_front_armor: 11,
    ht_flank_armor: 4,
  },
  {
    name: "T-72",
    side: "Soviet",
    wtype: "GUN",
    firepower_hv: 17,
    ammo_type: "HV",
    range_bands: [
      { col: 1, rmin: 0, rmax: 7 },
      { col: 2, rmin: 8, rmax: 11 },
      { col: 3, rmin: 12, rmax: 14 },
      { col: 4, rmin: 15, rmax: 16 },
      { col: 5, rmin: 17, rmax: 19 },
      { col: 6, rmin: 20, rmax: 21 },
      { col: 7, rmin: 22, rmax: 23 },
      { col: 8, rmin: 24, rmax: 26 },
    ],
    hv_front_armor: 10,
    hv_flank_armor: 4,
    ht_front_armor: 11,
    ht_flank_armor: 4,
  },

  // FINNISH WEAPONS
  {
    name: "Leopard 2",
    side: "FIN",
    wtype: "GUN",
    firepower_hv: 18,
    ammo_type: "HV",
    range_bands: [
      { col: 1, rmin: 0, rmax: 7 },
      { col: 2, rmin: 8, rmax: 11 },
      { col: 3, rmin: 12, rmax: 14 },
      { col: 4, rmin: 15, rmax: 18 },
      { col: 5, rmin: 19, rmax: 21 },
      { col: 6, rmin: 22, rmax: 26 },
      { col: 7, rmin: 27, rmax: 32 },
    ],
    hv_front_armor: 10,
    hv_flank_armor: 5,
    ht_front_armor: 12,
    ht_flank_armor: 6,
  },
];

export function getWeaponsBySide(side: Side): WeaponData[] {
  return WEAPONS_DB.filter((w) => w.side === side);
}

export function getWeaponByName(name: string): WeaponData | undefined {
  return WEAPONS_DB.find((w) => w.name === name);
}
