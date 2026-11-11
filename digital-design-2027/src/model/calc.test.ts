import { describe, expect, it } from 'vitest';
import {
  additionalHiring,
  calculate,
  defaultInputs,
  hire,
  sanitize,
  sensitivity,
  waterfall,
  type Inputs,
} from './calc';
import { PRESETS } from './presets';

/** ±1 € tarkkuus */
const near = (actual: number, expected: number, tol = 1) =>
  expect(Math.abs(actual - expected)).toBeLessThanOrEqual(tol);
const k = (v: number) => Math.round(v / 1000);

describe('hyväksymiskriteerit', () => {
  it('1. lähtötaso: 7 000 000 €', () => {
    const i: Inputs = {
      ...defaultInputs(),
      utilization: (7_000_000 / 9_512_000) * 100,
      conversionsPerMonth: 0,
      hires: [],
    };
    const r = calculate(i);
    near(r.summary.revenue, 7_000_000);
    expect(i.utilization.toFixed(1)).toBe('73.6');
  });

  it('2. konversiomalli 06: 7 611 240 €', () => {
    const i: Inputs = {
      ...defaultInputs(),
      startAi: 0,
      utilization: 78,
      conversionsPerMonth: 1,
      conversionFirst: 2,
      conversionLast: 12,
      hires: [hire(1, 2, 'ai')],
    };
    const r = calculate(i);
    near(r.summary.revenue, 7_611_240);
    expect(k(r.months[0].revenue)).toBe(623);
    expect(k(r.months[11].revenue)).toBe(646);
  });

  it('3. suositus 07: 8 647 392 €', () => {
    const r = calculate(defaultInputs());
    near(r.summary.revenue, 8_647_392);
    expect(k(r.months[0].revenue)).toBe(646);
    expect(r.months[0].hc).toBe(58);
    expect(r.months[0].ai).toBe(13);
    expect(k(r.months[11].revenue)).toBe(755);
    expect(r.months[11].hc).toBe(65);
    expect(r.months[11].ai).toBe(29);
    expect(r.summary.quarters.map(k)).toEqual([1996, 2155, 2239, 2258]);
  });

  it('4. herkkyys', () => {
    const base = defaultInputs();
    const m = (i: Inputs) => calculate(i).summary.revenue / 1e6;
    expect(m({ ...base, utilization: 74 })).toBeCloseTo(8.2, 2);
    expect(m({ ...base, utilization: 76 })).toBeCloseTo(8.43, 2);
    expect(m({ ...base, priceAi: 110 })).toBeCloseTo(8.36, 2);
    expect(m({ ...base, conversionLast: 6 })).toBeCloseTo(8.6, 2);
  });

  it('5. lisärekrytarve', () => {
    const i: Inputs = {
      ...defaultInputs(),
      hires: [hire(1, 2, 'ai')],
      targetRevenue: 8_700_000,
    };
    const r = calculate(i);
    expect(r.summary.shortfall / 1e6).toBeCloseTo(0.81, 2);
    const rows = additionalHiring(i, r);
    const get = (month: number, price: number) => rows.find((x) => x.startMonth === month && x.price === price)!.fte;
    expect(get(1, 100)).toBeCloseTo(6.3, 1);
    expect(get(1, 120)).toBeCloseTo(5.3, 1);
    expect(get(4, 100)).toBeCloseTo(8.4, 1);
    expect(get(4, 120)).toBeCloseTo(7.0, 1);
  });

  it('6. validointi: negatiiviset arvot ja AI > FTE eivät kaada mallia', () => {
    const bad: Inputs = {
      ...defaultInputs(),
      startFte: -5,
      startAi: 80,
      utilization: -10,
      priceAi: -1,
      hires: [hire(99, -3, 'ai')],
    };
    const s = sanitize(bad);
    expect(s.startFte).toBe(0);
    expect(s.utilization).toBe(0);
    expect(s.hires[0].startMonth).toBe(12);
    expect(s.hires[0].count).toBe(0);
    expect(() => calculate(bad)).not.toThrow();

    const over: Inputs = { ...defaultInputs(), startAi: 70 };
    const r = calculate(over);
    expect(r.warnings.length).toBeGreaterThan(0);
    r.months.forEach((m) => {
      expect(m.ai).toBeLessThanOrEqual(m.hc + 1e-9);
      expect(m.other).toBeGreaterThanOrEqual(0);
    });
    expect(Number.isFinite(r.summary.revenue)).toBe(true);
  });
});

describe('mallin muut osat', () => {
  it('konversio ei lisää FTE:itä', () => {
    const a = calculate({ ...defaultInputs(), conversionsPerMonth: 0 });
    const b = calculate(defaultInputs());
    a.months.forEach((m, idx) => expect(m.hc).toBe(b.months[idx].hc));
    expect(b.summary.revenue).toBeGreaterThan(a.summary.revenue);
  });

  it('rekryrivin oma €/h korvaa hinnan vain kyseiselle riville', () => {
    const base: Inputs = { ...defaultInputs(), startAi: 0, conversionsPerMonth: 0, hires: [hire(1, 1, 'ai')] };
    const custom: Inputs = { ...base, hires: [hire(1, 1, 'ai', '', 150)] };
    const hours = 1640 * 0.78;
    near(calculate(custom).summary.revenue - calculate(base).summary.revenue, 30 * hours);
  });

  it('osa-aikainen rekry (0,5) ja pois käytöstä oleva rivi', () => {
    const i: Inputs = {
      ...defaultInputs(),
      conversionsPerMonth: 0,
      hires: [hire(1, 0.5, 'other'), { ...hire(1, 5, 'other'), enabled: false }],
    };
    expect(calculate(i).months[0].hc).toBe(56.5);
  });

  it('tuottavuuden nousuaika vähentää liikevaihtoa, ei HC:tä', () => {
    const base: Inputs = { ...defaultInputs(), conversionsPerMonth: 0 };
    const ramp: Inputs = { ...base, rampMonths: 3, rampStartPct: 50 };
    const a = calculate(base);
    const b = calculate(ramp);
    expect(b.months[0].hc).toBe(a.months[0].hc);
    expect(b.summary.revenue).toBeLessThan(a.summary.revenue);
  });

  it('poistuma ja korvaus yhden kuukauden viiveellä', () => {
    const i: Inputs = { ...defaultInputs(), hires: [], conversionsPerMonth: 0, attrition: 12, replaceLeavers: true };
    const r = calculate(i);
    expect(r.months[0].hc).toBeCloseTo(55, 6); // −1 lähtenyt, korvaus vasta helmikuussa
    expect(r.months[11].hc).toBeCloseTo(55, 6);
    const noRepl = calculate({ ...i, replaceLeavers: false });
    expect(noRepl.months[11].hc).toBeCloseTo(44, 6);
  });

  it('konversiot rajataan niin, ettei AI ylitä FTE:tä', () => {
    const r = calculate({ ...defaultInputs(), startFte: 12, startAi: 10, hires: [], conversionsPerMonth: 2 });
    r.months.forEach((m) => expect(m.ai).toBeLessThanOrEqual(12));
    expect(r.warnings.some((w) => w.includes('rajattu'))).toBe(true);
  });

  it('kuukausitavoitteiden summa on vuositavoite kaikilla jaoilla', () => {
    for (const split of ['even', 'capacity', 'custom'] as const) {
      const r = calculate({ ...defaultInputs(), targetSplit: split, customWeights: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] });
      near(r.months[11].cumTarget, 8_700_000);
    }
  });

  it('työpäiväpainot ja kuukausikohtainen utilisaatio', () => {
    const base = defaultInputs();
    const w = calculate({ ...base, useWorkdayWeights: true, workdayWeights: Array(12).fill(1) });
    near(w.summary.revenue, calculate(base).summary.revenue);
    const u = calculate({ ...base, monthlyUtil: [70, ...Array(11).fill(null)] });
    expect(u.months[0].util).toBe(70);
    expect(u.months[1].util).toBe(78);
    expect(u.summary.revenue).toBeLessThan(calculate(base).summary.revenue);
  });

  it('rekrytarve on 0 kun kapasiteetti riittää, positiivinen kun ei', () => {
    const hi = calculate({ ...defaultInputs(), targetRevenue: 5_000_000 });
    hi.months.forEach((m) => expect(m.hireNeed).toBe(0));
    const lo = calculate({ ...defaultInputs(), targetRevenue: 12_000_000 });
    expect(lo.months[11].hireNeed).toBeGreaterThan(0);
    expect(lo.months[11].cumHireNeed).toBeGreaterThanOrEqual(lo.months[0].cumHireNeed);
  });

  it('vipuportaikon loppusumma = vuoden liikevaihto, lähtötaso = 2026', () => {
    const i = defaultInputs();
    const steps = waterfall(i);
    near(steps[0].value, 7_000_000);
    const last = steps[steps.length - 1];
    near(last.value, calculate(i).summary.revenue);
    const deltaSum = steps.filter((s) => s.kind === 'delta').reduce((a, s) => a + s.value, 0);
    near(steps[0].value + deltaSum, last.value);
  });

  it('herkkyys on lajiteltu suurimmasta pienimpään ja suunta on oikea', () => {
    const rows = sensitivity(defaultInputs());
    expect(rows).toHaveLength(6);
    const span = (r: { low: number; high: number }) => Math.max(Math.abs(r.low), Math.abs(r.high));
    for (let n = 1; n < rows.length; n++) expect(span(rows[n - 1])).toBeGreaterThanOrEqual(span(rows[n]));
    const util = rows.find((r) => r.label === 'Utilisaatio')!;
    expect(util.low).toBeLessThan(0);
    expect(util.high).toBeGreaterThan(0);
  });

  it('katetarkistus', () => {
    const r = calculate(defaultInputs());
    const util = 0.78;
    const maxCost = 0.6 * r.summary.blendedYear * util;
    near(r.margin.maxCostPerHour, maxCost, 1e-6);
    near(r.margin.maxSalary, (maxCost * 1640) / (12.5 * 1.22), 1e-6);
    expect(['ok', 'warn', 'bad']).toContain(r.margin.status);
  });

  it('esiasetukset laskevat ilman virheitä', () => {
    PRESETS.forEach((p) => {
      const r = calculate(p.make());
      expect(Number.isFinite(r.summary.revenue)).toBe(true);
      expect(r.summary.revenue).toBeGreaterThan(0);
    });
  });
});
