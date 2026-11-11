import { defaultInputs, hire, type Inputs } from './calc';

export interface Preset {
  id: string;
  name: string;
  make: () => Inputs;
}

export const PRESETS: Preset[] = [
  {
    id: 'suositus',
    name: 'Suositus (portitettu)',
    make: () => defaultInputs(),
  },
  {
    id: 'maltillinen',
    name: 'Maltillinen',
    make: () => ({
      ...defaultInputs(),
      targetRevenue: 8_000_000,
      startFte: 56,
      startAi: 0,
      priceAi: 105,
      priceOther: 105,
      utilization: 77.8,
      conversionsPerMonth: 0,
      hires: [hire(1, 1, 'other'), hire(7, 3, 'ai')],
    }),
  },
  {
    id: 'rohkea',
    name: 'Rohkea',
    make: () => ({
      ...defaultInputs(),
      targetRevenue: 8_600_000,
      priceAi: 120,
      priceOther: 100,
      utilization: 78,
      conversionsPerMonth: 1,
      hires: [hire(1, 2, 'ai'), hire(4, 3, 'ai'), hire(7, 3, 'other')],
    }),
  },
  {
    id: 'huimapaainen',
    name: 'Huimapäinen',
    make: () => ({
      ...defaultInputs(),
      targetRevenue: 9_500_000,
      utilization: 80,
      conversionsPerMonth: 2,
      hires: [hire(1, 4, 'ai'), hire(4, 5, 'ai'), hire(7, 3, 'other'), hire(10, 1, 'ai')],
    }),
  },
  {
    id: '2026-jatko',
    name: '2026 jatko',
    make: () => ({
      ...defaultInputs(),
      startFte: 56,
      startAi: 10,
      conversionsPerMonth: 0,
      utilization: 73.6,
      hires: [],
    }),
  },
];
