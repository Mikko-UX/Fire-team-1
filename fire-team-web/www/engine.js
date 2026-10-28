// FIRE TEAM 6.5 combat engine: weapon data and the vehicle and infantry
// combat calculations. Runs entirely in the browser (and in the iOS app),
// so no server or network is needed.
(function (global) {
  'use strict';

  // --- Weapon database: firepower, range bands (column, min hex, max hex) and armor ---
  const WEAPONS = [
    // US
    { name: "Heli RKT", side: "US", type: "RKT", fpHV: null, fpHT: 6, ammo: "HT",
      ranges: [[3, 6, 22], [4, 23, 33], [5, 34, 42], [6, 43, 50]],
      armor: { hvFront: 1, hvFlank: 0, htFront: 1, htFlank: 0 } },
    { name: "Law RKT", side: "US", type: "RKT", fpHV: null, fpHT: 6, ammo: "HT",
      ranges: [[1, 0, 0], [2, 1, 1], [4, 2, 2], [6, 3, 3], [7, 4, 5]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // NLAW (Saab): 150 mm top-attack shaped charge, 20–1000 m. HT 14 sits between Spandrel (13) and TOW (15)
    // because the top attack largely bypasses frontal armor; best columns at short range.
    { name: "NLAW MSL", side: "US", type: "MSL", fpHV: null, fpHT: 14, ammo: "HT",
      ranges: [[1, 0, 3], [2, 4, 5], [3, 6, 7], [4, 8, 10]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // Javelin (FGM-148): 127 mm tandem shaped charge, top attack, fire-and-forget, about 65–2500 m.
    // HT 17 like Spiral, just under Hellfire (18). Like TOW/Hellfire it is best at longer range;
    // very close shots lose the top-attack profile.
    { name: "Javelin MSL", side: "US", type: "MSL", fpHV: null, fpHT: 17, ammo: "HT",
      ranges: [[1, 3, 25], [2, 2, 2], [3, 1, 1]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // Spike-LR / Spike-MR (Rafael): tandem shaped charge, top or direct attack, fire-and-forget with
    // operator updates. HT 16 between TOW (15) and Javelin (17); LR about 200–4000 m, MR 200–2500 m.
    { name: "Spike LR MSL", side: "US", type: "MSL", fpHV: null, fpHT: 16, ammo: "HT",
      ranges: [[1, 4, 40], [2, 3, 3], [3, 2, 2]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Spike MR MSL", side: "US", type: "MSL", fpHV: null, fpHT: 16, ammo: "HT",
      ranges: [[1, 4, 25], [2, 3, 3], [3, 2, 2]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Dragon MSL", side: "US", type: "MSL", fpHV: null, fpHT: 10, ammo: "HT",
      ranges: [[3, 3, 10]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "TOW MSL", side: "US", type: "MSL", fpHV: null, fpHT: 15, ammo: "HT",
      ranges: [[1, 7, 40], [2, 6, 6], [3, 5, 5], [4, 4, 4], [6, 2, 3]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Hellfire MSL", side: "US", type: "MSL", fpHV: null, fpHT: 18, ammo: "HT",
      ranges: [[1, 6, 55], [2, 5, 5], [3, 4, 4], [4, 3, 3], [5, 2, 2]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Stinger SAM", side: "US", type: "MSL", fpHV: null, fpHT: 6, ammo: "HT",
      ranges: [[4, 0, 20], [5, 21, 25], [6, 26, 30]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "M1", side: "US", type: "GUN", fpHV: 16, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 7], [2, 8, 11], [3, 12, 14], [4, 15, 18], [5, 19, 21], [6, 22, 26], [7, 27, 32]],
      armor: { hvFront: 10, hvFlank: 5, htFront: 12, htFlank: 6 } },
    // Unarmed vehicles (target only, no firepower).
    { name: "M-1150 ABV", side: "US", type: "VEH", fpHV: null, fpHT: null, ammo: null,
      ranges: [],
      armor: { hvFront: 10, hvFlank: 5, htFront: 12, htFlank: 6 } },
    { name: "M-1074 Bridge", side: "US", type: "VEH", fpHV: null, fpHT: null, ammo: null,
      ranges: [],
      armor: { hvFront: 10, hvFlank: 5, htFront: 12, htFlank: 6 } },
    { name: "M2", side: "US", type: "GUN", fpHV: 7, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 5], [2, 6, 7], [3, 8, 9], [4, 10, 11], [5, 12, 14], [6, 15, 18], [7, 19, 22]],
      armor: { hvFront: 4, hvFlank: 2, htFront: 4, htFlank: 2 } },
    { name: "AH-64", side: "US", type: "GUN", fpHV: 4, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 5], [2, 6, 7], [3, 8, 9], [4, 10, 11], [5, 12, 14], [6, 15, 18], [7, 19, 22]],
      armor: { hvFront: 2, hvFlank: 1, htFront: 2, htFlank: 1 } },
    { name: "M60a3", side: "US", type: "GUN", fpHV: 12, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 6], [2, 7, 9], [3, 10, 11], [4, 12, 13], [5, 14, 16], [6, 17, 22], [7, 23, 30]],
      armor: { hvFront: 4, hvFlank: 2, htFront: 8, htFlank: 3 } },
    { name: "M  113", side: "US", type: "GUN", fpHV: 0, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 3], [2, 4, 6], [3, 7, 9]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 1, htFlank: 0 } },
    { name: "M 163", side: "US", type: "RKT", fpHV: 0, fpHT: null, ammo: "HV",
      ranges: [[2, 1, 3], [3, 4, 5], [4, 6, 6], [5, 7, 7], [6, 8, 8], [7, 9, 9], [8, 10, 10]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 1, htFlank: 0 } },
    // Soviet
    { name: "RPG-16 RKT", side: "Soviet", type: "RKT", fpHV: null, fpHT: 6, ammo: "HT",
      ranges: [[1, 0, 0], [2, 1, 1], [3, 2, 2], [4, 3, 3], [5, 4, 4]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Sagger MSL", side: "Soviet", type: "MSL", fpHV: null, fpHT: 11, ammo: "HT",
      ranges: [[1, 12, 37], [3, 9, 11], [4, 7, 8], [6, 6, 6], [8, 5, 5], [10, 4, 4]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Spandrel MSL", side: "Soviet", type: "MSL", fpHV: null, fpHT: 13, ammo: "HT",
      ranges: [[1, 4, 40], [2, 3, 3], [4, 2, 2], [5, 1, 1]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Spigot MSL", side: "Soviet", type: "MSL", fpHV: null, fpHT: 13, ammo: "HT",
      ranges: [[1, 4, 25], [2, 3, 3], [3, 2, 2], [4, 1, 1]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Spiral MSL", side: "Soviet", type: "MSL", fpHV: null, fpHT: 17, ammo: "HT",
      ranges: [[1, 9, 55], [2, 7, 8], [3, 6, 6]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // 9M133 Kornet (AT-14): laser beam-riding, tandem shaped charge (~1100–1200 mm behind ERA),
    // direct attack, about 100–5500 m. HT 18 like Hellfire; best at long range like TOW/Hellfire.
    { name: "Kornet MSL", side: "Soviet", type: "MSL", fpHV: null, fpHT: 18, ammo: "HT",
      ranges: [[1, 6, 55], [2, 4, 5], [3, 2, 3], [4, 1, 1]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // 9M131 Metis-M1 (AT-13): man-portable wire-guided, tandem shaped charge (~900 mm behind ERA),
    // about 80–2000 m. HT 16 like Spike; range bands shaped like Spigot.
    { name: "Metis-M1 MSL", side: "Soviet", type: "MSL", fpHV: null, fpHT: 16, ammo: "HT",
      ranges: [[1, 4, 20], [2, 3, 3], [3, 2, 2], [4, 1, 1]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "SA-14 SAM", side: "Soviet", type: "SAM", fpHV: null, fpHT: 8, ammo: "HT",
      ranges: [[6, 0, 27], [7, 28, 45]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "AGS-17", side: "Soviet", type: "RKT", fpHV: null, fpHT: 6, ammo: "HT",
      ranges: [[1, 0, 0], [2, 1, 3], [3, 4, 5], [4, 6, 6], [5, 7, 7], [6, 8, 8], [7, 9, 9], [8, 10, 10]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "SPG-9", side: "Soviet", type: "RKT", fpHV: null, fpHT: 9, ammo: "HT",
      ranges: [[1, 0, 4], [2, 5, 5], [3, 6, 6], [4, 7, 7], [5, 8, 8], [6, 9, 10], [7, 11, 12], [8, 13, 14]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "BMP-1", side: "Soviet", type: "GUN", fpHV: 9, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 4], [2, 5, 5], [3, 6, 6], [4, 7, 7], [5, 8, 8], [6, 9, 10], [7, 11, 12], [8, 13, 14]],
      armor: { hvFront: 4, hvFlank: 2, htFront: 4, htFlank: 2 } },
    { name: "BMP-2", side: "Soviet", type: "GUN", fpHV: 7, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 4], [2, 5, 6], [3, 7, 8], [4, 9, 10], [5, 11, 12], [6, 13, 14], [7, 15, 17], [8, 18, 20]],
      armor: { hvFront: 4, hvFlank: 2, htFront: 4, htFlank: 2 } },
    { name: "ASU-85", side: "Soviet", type: "GUN", fpHV: 6, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 4], [2, 5, 6], [3, 7, 8], [4, 9, 10], [5, 11, 12], [6, 13, 14], [7, 15, 17], [8, 18, 20]],
      armor: { hvFront: 2, hvFlank: 1, htFront: 2, htFlank: 1 } },
    { name: "Mi-6", side: "Soviet", type: "GUN", fpHV: 2, fpHT: null, ammo: "HV",
      ranges: [[2, 0, 0], [3, 1, 1], [4, 2, 3], [5, 4, 5], [6, 6, 6], [7, 7, 8], [8, 9, 10]],
      armor: { hvFront: 1, hvFlank: 0, htFront: 1, htFlank: 0 } },
    { name: "Mi-24", side: "Soviet", type: "GUN", fpHV: 4, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 4], [2, 5, 6], [3, 7, 8], [4, 9, 10], [5, 11, 12], [6, 13, 14], [7, 15, 17], [8, 18, 20]],
      armor: { hvFront: 2, hvFlank: 1, htFront: 2, htFlank: 1 } },
    { name: "SAU-122", side: "Soviet", type: "GUN", fpHV: 9, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 2], [2, 3, 3], [3, 4, 4], [4, 5, 6], [5, 7, 8], [6, 9, 11], [7, 12, 14], [8, 15, 19]],
      armor: { hvFront: 2, hvFlank: 1, htFront: 2, htFlank: 1 } },
    { name: "T-80", side: "Soviet", type: "GUN", fpHV: 17, fpHT: 10, ammo: "HV",
      ranges: [[1, 0, 7], [2, 8, 11], [3, 12, 14], [4, 15, 16], [5, 17, 19], [6, 20, 21], [7, 22, 23], [8, 24, 26]],
      armor: { hvFront: 10, hvFlank: 4, htFront: 11, htFlank: 4 } },
    { name: "T-72", side: "Soviet", type: "GUN", fpHV: 17, fpHT: 10, ammo: "HV",
      ranges: [[1, 0, 7], [2, 8, 11], [3, 12, 14], [4, 15, 16], [5, 17, 19], [6, 20, 21], [7, 22, 23], [8, 24, 26]],
      armor: { hvFront: 10, hvFlank: 4, htFront: 11, htFlank: 4 } },
    // Unarmed vehicles (target only, no firepower).
    { name: "MTU-72 Bridge", side: "Soviet", type: "VEH", fpHV: null, fpHT: null, ammo: null,
      ranges: [],
      armor: { hvFront: 10, hvFlank: 4, htFront: 11, htFlank: 4 } },
    { name: "T-72 KMT", side: "Soviet", type: "VEH", fpHV: null, fpHT: null, ammo: null,
      ranges: [],
      armor: { hvFront: 10, hvFlank: 4, htFront: 11, htFlank: 4 } },
    { name: "Ural-4320", side: "Soviet", type: "VEH", fpHV: null, fpHT: null, ammo: null,
      ranges: [],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "T-62", side: "Soviet", type: "GUN", fpHV: 14, fpHT: 9, ammo: "HV",
      ranges: [[1, 0, 5], [2, 6, 7], [3, 8, 9], [4, 10, 10], [5, 11, 12], [6, 13, 14], [7, 15, 17], [8, 18, 20]],
      armor: { hvFront: 4, hvFlank: 2, htFront: 8, htFlank: 3 } },
    { name: "MT-LB", side: "Soviet", type: "GUN", fpHV: 2, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 5], [2, 6, 8], [3, 9, 10]],
      armor: { hvFront: 1, hvFlank: 0, htFront: 1, htFlank: 0 } },
    { name: "BTR-80", side: "Soviet", type: "GUN", fpHV: 3, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 5], [2, 6, 7], [3, 8, 8], [4, 9, 10]],
      armor: { hvFront: 1, hvFlank: 0, htFront: 1, htFlank: 0 } },
    { name: "Heli RKT", side: "Soviet", type: "RKT", fpHV: null, fpHT: 6, ammo: "HT",
      ranges: [[3, 6, 20], [4, 21, 30], [5, 31, 37]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // FIN
    { name: "T-72", side: "FIN", type: "GUN", fpHV: 17, fpHT: 10, ammo: "HV",
      ranges: [[1, 0, 7], [2, 8, 11], [3, 12, 14], [4, 15, 16], [5, 17, 19], [6, 20, 21], [7, 22, 23], [8, 24, 26]],
      armor: { hvFront: 10, hvFlank: 4, htFront: 11, htFlank: 4 } },
    { name: "Leopard 2", side: "FIN", type: "GUN", fpHV: 18, fpHT: 10, ammo: "HV",
      ranges: [[1, 0, 7], [2, 8, 11], [3, 12, 14], [4, 15, 18], [5, 19, 21], [6, 22, 26], [7, 27, 32]],
      armor: { hvFront: 12, hvFlank: 6, htFront: 11, htFlank: 5 } },
    // CV9030FIN: 30 mm APFSDS (no HEAT round, no missile); modern fire control gives M1-like column 1 reach.
    { name: "CV90C", side: "FIN", type: "GUN", fpHV: 9, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 7], [2, 8, 10], [3, 11, 13], [4, 14, 16], [5, 17, 19], [6, 20, 22], [7, 23, 25]],
      armor: { hvFront: 4, hvFlank: 2, htFront: 4, htFlank: 2 } },
    // Unarmed vehicles (target only, no firepower).
    { name: "M-1150 ABV", side: "FIN", type: "VEH", fpHV: null, fpHT: null, ammo: null,
      ranges: [],
      armor: { hvFront: 10, hvFlank: 5, htFront: 12, htFlank: 6 } },
    { name: "M-1074 Bridge", side: "FIN", type: "VEH", fpHV: null, fpHT: null, ammo: null,
      ranges: [],
      armor: { hvFront: 10, hvFlank: 5, htFront: 12, htFlank: 6 } },
    { name: "SA-SISU 150", side: "FIN", type: "VEH", fpHV: null, fpHT: null, ammo: null,
      ranges: [],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "BMP-1", side: "FIN", type: "GUN", fpHV: null, fpHT: 9, ammo: "HT",
      ranges: [[1, 0, 4], [2, 5, 5], [3, 6, 6], [4, 7, 7], [5, 8, 8], [6, 9, 10], [7, 11, 12], [8, 13, 14]],
      armor: { hvFront: 4, hvFlank: 2, htFront: 4, htFlank: 2 } },
    { name: "BMP-2", side: "FIN", type: "GUN", fpHV: 7, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 4], [2, 5, 6], [3, 7, 8], [4, 9, 10], [5, 11, 12], [6, 13, 14], [7, 15, 17], [8, 18, 20]],
      armor: { hvFront: 4, hvFlank: 2, htFront: 4, htFlank: 2 } },
    { name: "ZU-23", side: "FIN", type: "GUN", fpHV: 6, fpHT: null, ammo: "HV",
      ranges: [[1, 0, 4], [2, 5, 6], [3, 7, 8], [4, 9, 10], [5, 11, 12], [6, 13, 14], [7, 15, 17]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "LAW", side: "FIN", type: "RKT", fpHV: null, fpHT: 6, ammo: "HT",
      ranges: [[2, 1, 1], [4, 2, 2], [6, 3, 3], [7, 4, 5]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Pasi", side: "FIN", type: "GUN", fpHV: 0, fpHT: null, ammo: "HV",
      ranges: [[2, 1, 1], [3, 2, 3], [4, 4, 5], [5, 6, 6], [6, 7, 8], [7, 9, 10]],
      armor: { hvFront: 1, hvFlank: 0, htFront: 1, htFlank: 0 } },
    { name: "Musti", side: "FIN", type: "GUN", fpHV: null, fpHT: 9, ammo: "HT",
      ranges: [[1, 0, 4], [2, 5, 5], [3, 6, 6], [4, 7, 7], [5, 8, 8], [6, 9, 10], [7, 11, 12], [8, 13, 14]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Spigot MSL", side: "FIN", type: "MSL", fpHV: null, fpHT: 13, ammo: "HT",
      ranges: [[1, 4, 25], [2, 3, 3], [3, 2, 2], [4, 1, 1]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Apilas", side: "FIN", type: "GUN", fpHV: null, fpHT: 9, ammo: "HT",
      ranges: [[2, 1, 1], [4, 2, 2], [6, 3, 3], [7, 4, 5]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // NLAW (Saab): 150 mm top-attack shaped charge, 20–1000 m. HT 14 sits between Spandrel (13) and TOW (15)
    // because the top attack largely bypasses frontal armor; best columns at short range.
    { name: "NLAW MSL", side: "FIN", type: "MSL", fpHV: null, fpHT: 14, ammo: "HT",
      ranges: [[1, 0, 3], [2, 4, 5], [3, 6, 7], [4, 8, 10]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // Javelin (FGM-148): 127 mm tandem shaped charge, top attack, fire-and-forget, about 65–2500 m.
    // HT 17 like Spiral, just under Hellfire (18). Like TOW/Hellfire it is best at longer range;
    // very close shots lose the top-attack profile.
    { name: "Javelin MSL", side: "FIN", type: "MSL", fpHV: null, fpHT: 17, ammo: "HT",
      ranges: [[1, 3, 25], [2, 2, 2], [3, 1, 1]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    // Spike-LR / Spike-MR (Rafael): tandem shaped charge, top or direct attack, fire-and-forget with
    // operator updates. HT 16 between TOW (15) and Javelin (17); LR about 200–4000 m, MR 200–2500 m.
    { name: "Spike LR MSL", side: "FIN", type: "MSL", fpHV: null, fpHT: 16, ammo: "HT",
      ranges: [[1, 4, 40], [2, 3, 3], [3, 2, 2]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "Spike MR MSL", side: "FIN", type: "MSL", fpHV: null, fpHT: 16, ammo: "HT",
      ranges: [[1, 4, 25], [2, 3, 3], [3, 2, 2]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
    { name: "TOW", side: "FIN", type: "MSL", fpHV: null, fpHT: 15, ammo: "HT",
      ranges: [[1, 7, 40], [2, 6, 6], [3, 5, 5], [4, 4, 4], [6, 2, 3]],
      armor: { hvFront: 0, hvFlank: 0, htFront: 0, htFlank: 0 } },
  ];

  // --- Vehicle kill table: differential thresholds per ammo, kill numbers for columns 1–10 ---
  const KILL_TABLE = [
    { hv: -1, ht: -1, kills: [1, 1, null, null, null, null, null, null, null, null] },
    { hv: null, ht: 0, kills: [1, 1, 1, 1, 1, null, null, null, null, null] },
    { hv: 0, ht: 1, kills: [2, 2, 1, 1, 1, 1, 1, 1, 1, null] },
    { hv: 1, ht: 2, kills: [4, 3, 3, 2, 2, 2, 1, 1, 1, null] },
    { hv: 2, ht: 3, kills: [5, 5, 4, 4, 3, 2, 2, 1, 1, null] },
    { hv: null, ht: 4, kills: [6, 6, 5, 4, 4, 3, 2, 1, 1, null] },
    { hv: 3, ht: 5, kills: [7, 6, 5, 5, 4, 3, 2, 2, 1, 1] },
    { hv: null, ht: 6, kills: [8, 7, 6, 5, 4, 3, 3, 2, 1, 1] },
    { hv: 4, ht: 7, kills: [8, 7, 6, 5, 5, 4, 3, 2, 1, 1] },
    { hv: 5, ht: 8, kills: [9, 8, 7, 6, 5, 4, 3, 2, 1, 1] },
  ];

  // --- Infantry fire table: rows 1–14 (modified roll), columns B–T ---
  const COLUMN_LETTERS = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"];
  // Transcribed from the Infantry Fire Table (6.3) card. Cells: "1"/"2" = (+1)/(+2) fear,
  // "F" = 1 (step loss: flip + officer check), "E" = eliminated, "0" = no effect.
  const INFANTRY_FIRE_TABLE = {
    1: ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "1"],
    2: ["E", "E", "E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "1"],
    3: ["E", "E", "E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "2", "1"],
    4: ["E", "E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1", "1"],
    5: ["E", "E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1", "0", "0"],
    6: ["E", "E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1", "1", "0", "0"],
    7: ["E", "E", "E", "F", "F", "F", "F", "F", "F", "F", "F", "2", "2", "1", "1", "1", "1", "0", "0"],
    8: ["E", "E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "2", "1", "1", "1", "1", "0", "0", "0"],
    9: ["E", "F", "F", "F", "F", "F", "F", "F", "2", "2", "2", "1", "1", "1", "0", "0", "0", "0", "0"],
    10: ["F", "F", "F", "F", "F", "F", "2", "2", "2", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0"],
    11: ["F", "F", "F", "F", "F", "2", "2", "2", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    12: ["F", "F", "F", "F", "F", "2", "2", "2", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    13: ["F", "F", "F", "F", "2", "2", "2", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    14: ["F", "F", "F", "2", "2", "2", "2", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
  };
  const COL_FP_RANGES = {"0": "FP 120+", "1": "FP 100-119", "2": "FP 80-99", "3": "FP 60-79", "4": "FP 48-59", "5": "FP 36-47", "6": "FP 32-35", "7": "FP 28-31", "8": "FP 24-27", "9": "FP 21-23", "10": "FP 18-20", "11": "FP 16-17", "12": "FP 14-15", "13": "FP 12-13", "14": "FP 10-11", "15": "FP 8-9", "16": "FP 6-7", "17": "FP 4-5", "18": "FP 2-3"};
  const DECODE_MAP = {"E": "ALL ELIMINATED", "F": "FLIP + OFFICER CHECK", "2": "ADD 2 FEAR MARKERS", "1": "ADD 1 FEAR MARKER", "0": "NO EFFECT"};
  const INFANTRY_EXPLANATIONS = {
    "0": "✅ NO EFFECT (0)\n\nTarget is unaffected.\nNo fear markers, no damage.",
    "1": "⚠️ ADD 1 FEAR MARKER (1)\n\nAdd 1 fear marker to the target unit.\nUnit is not flipped, not eliminated.",
    "2": "⚠️⚠️ ADD 2 FEAR MARKERS (2)\n\nAdd 2 fear markers to the target unit.\nUnit is not flipped, not eliminated.",
    "F": "💔 FLIP + OFFICER CHECK (F)\n\nFlip the unit to its reduced side.\n\n════════════════════════════════════════\nOFFICER CHECK - If an officer is present:\nIf an officer is present, roll D10:\n════════════════════════════════════════\n\n🎲 Roll D10:\n\n  • 1-2: ☠️ OFFICER ELIMINATED\n         Officer is eliminated\n         → Add +2 Fear markers to the unit\n         \n  • 3-10: ✅ OFFICER SURVIVES\n          Officer survives\n          → Add +1 Fear marker to the unit\n\n════════════════════════════════════════\nIf no officer: only +1 Fear marker\n════════════════════════════════════════",
    "E": "🔥💀 ALL ELIMINATED (E)\n\nALL UNITS ELIMINATED!\n\n════════════════════════════════════════\nThe entire unit is completely destroyed!\nRemove the unit from play.\nNo fear markers - unit is gone.\n════════════════════════════════════════",
  };

  const rollD10 = () => 1 + Math.floor(Math.random() * 10);

  function findWeapon(name, side) {
    return WEAPONS.find(w => w.name === name && (!side || w.side === side)) || null;
  }

  function baseColumnForRange(weapon, rangeHexes) {
    if (!weapon.ranges) return null;
    const band = weapon.ranges.find(([, rmin, rmax]) => rmin <= rangeHexes && rangeHexes <= rmax);
    return band ? band[0] : null;
  }

  // The highest kill table row whose threshold the differential reaches.
  // HV fire skips the rows that only exist for HT.
  function pickRowIndex(differential, ammo) {
    if (differential < -1) return null;
    let row = null;
    KILL_TABLE.forEach((r, i) => {
      const threshold = ammo === 'HV' ? r.hv : r.ht;
      if (threshold !== null && threshold <= differential) row = i;
    });
    return row;
  }

  function killNumber(weapon, target, targetSide, rangeHexes, columnShifts, leadership, fear, shooterModifiers, targetModifiers, ammoChoice) {
    // Guns that carry both HV and HT rounds fire whichever the player picks (HV by default).
    let useHT = weapon.ammo === 'HT' || ['MSL', 'SAM', 'RKT'].includes(weapon.type);
    if (weapon.type === 'GUN' && weapon.fpHV !== null && weapon.fpHT !== null && (ammoChoice === 'HV' || ammoChoice === 'HT')) {
      useHT = ammoChoice === 'HT';
    }
    const front = targetSide === 'Front';
    const ammo = useHT ? 'HT' : 'HV';
    const firepower = (useHT ? weapon.fpHT : weapon.fpHV) || 0;
    const armor = useHT
      ? (front ? target.armor.htFront : target.armor.htFlank)
      : (front ? target.armor.hvFront : target.armor.hvFlank);
    const none = { kill_number: null, base_col: null, final_col: null, ammo, firepower, armor };

    const differential = firepower - armor;
    const rowIndex = pickRowIndex(differential, ammo);
    if (rowIndex === null) return none;

    const baseCol = baseColumnForRange(weapon, rangeHexes);
    if (baseCol === null) return none;

    let finalCol = baseCol + columnShifts - leadership + fear + shooterModifiers + targetModifiers;
    if (finalCol > 10) return { ...none, base_col: baseCol, final_col: finalCol };
    if (finalCol < 1) finalCol = 1;

    let kn = KILL_TABLE[rowIndex].kills[finalCol - 1];
    // Special case for base column 9: HV differential 5+ or HT differential 8+ gives kill number 2.
    if (baseCol === 9) {
      if (ammo === 'HV' && differential >= 5) kn = 2;
      if (ammo === 'HT' && differential >= 8) kn = 2;
    }
    return { kill_number: kn, base_col: baseCol, final_col: finalCol, ammo, firepower, armor };
  }

  function vehicleCombat(p, dieRoll = rollD10()) {
    const shooter = findWeapon(p.shooterWeapon, p.shooterCountry);
    const target = findWeapon(p.targetWeapon, p.targetCountry);
    if (!shooter || !target) return { error: 'Invalid weapon' };

    const r = killNumber(shooter, target, p.targetSide, Number(p.rangeHexes), Number(p.columnShifts) || 0,
      Number(p.leadership) || 0, Number(p.fear) || 0, Number(p.shooterModifiers) || 0, Number(p.targetModifiers) || 0, p.ammo || null);
    const hit = r.kill_number !== null && dieRoll <= r.kill_number;
    const solver = r.kill_number === null ? 'No kill number available' : (hit ? 'Target destroyed!' : 'No effect');
    return { ...r, die_roll: dieRoll, hit, solver, hit_threshold: r.kill_number };
  }

  function columnIndexFromFirepower(fp) {
    const lowerBounds = [120, 100, 80, 60, 48, 36, 32, 28, 24, 21, 18, 16, 14, 12, 10, 8, 6, 4];
    const i = lowerBounds.findIndex(min => fp >= min);
    return i === -1 ? 18 : i;
  }

  // Firepower multipliers are [numerator, denominator] pairs (e.g. [1, 2] for ½).
  // They combine by multiplication and the result is rounded down.
  const FRACTION_SYMBOLS = { '1/2': '½', '1/3': '⅓', '2/3': '⅔' };
  const fractionText = ([n, d]) => (d === 1 ? String(n) : FRACTION_SYMBOLS[`${n}/${d}`] || `${n}/${d}`);

  function infantryCombat(p, dieRoll = rollD10()) {
    const firepower = Number(p.firepower);
    const multipliers = p.fpMultipliers || [];
    const num = multipliers.reduce((a, [n]) => a * n, 1);
    const den = multipliers.reduce((a, [, d]) => a * d, 1);
    const effectiveFirepower = Math.floor(firepower * num / den);
    const leadership = Number(p.leadership) || 0;
    const fear = Number(p.fear) || 0;
    let modifiers = Number(p.modifiers) || 0;
    if (leadership > 0) modifiers -= leadership;
    if (fear > 0) modifiers += fear;

    const colIndex = columnIndexFromFirepower(effectiveFirepower);
    const columnLetter = COLUMN_LETTERS[colIndex];
    const modifiedRoll = Math.min(14, Math.max(1, dieRoll + modifiers));
    const result = INFANTRY_FIRE_TABLE[modifiedRoll][colIndex];
    return {
      result,
      chosen_row_key: modifiedRoll,
      firepower_input: firepower,
      effective_firepower: effectiveFirepower,
      multiplier_text: multipliers.map(m => `× ${fractionText(m)}`).join(' '),
      die_roll: dieRoll,
      modifiers,
      modified_roll: modifiedRoll,
      col_index: colIndex,
      column_letter: columnLetter,
      col_range_description: COL_FP_RANGES[colIndex],
      decoded: DECODE_MAP[result] || result,
      table_coord: `${columnLetter}${modifiedRoll}`,
      explanation: INFANTRY_EXPLANATIONS[result] || `Result: ${result}`,
      leadership,
      fear
    };
  }

  global.FireTeamEngine = {
    weapons: WEAPONS.map(w => ({ name: w.name, country: w.side, type: w.type, firepower_hv: w.fpHV, firepower_ht: w.fpHT })),
    vehicleCombat,
    infantryCombat
  };
})(typeof window !== 'undefined' ? window : globalThis);
