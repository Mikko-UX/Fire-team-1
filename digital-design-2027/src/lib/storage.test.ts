import { describe, expect, it } from 'vitest';
import { exportJson, normalizeInputs, parseImport } from './storage';
import { calculate, defaultInputs } from '../model/calc';
import { PRESETS } from '../model/presets';

describe('JSON vienti ja tuonti', () => {
  it('kierto säilyttää tulokset', () => {
    const scenarios = PRESETS.map((p, i) => ({ id: `s${i}`, name: p.name, inputs: p.make() }));
    const text = exportJson({ scenarios, activeId: 's0' });
    const back = parseImport(text);
    expect(back).toHaveLength(scenarios.length);
    back.forEach((b, i) => {
      expect(b.name).toBe(scenarios[i].name);
      expect(calculate(b.inputs).summary.revenue).toBeCloseTo(calculate(scenarios[i].inputs).summary.revenue, 6);
    });
  });

  it('puutteellinen tai virheellinen data korvataan oletuksilla', () => {
    const n = normalizeInputs({ startFte: 'abc', priceAi: -5, hires: [{ count: 2 }] });
    expect(n.startFte).toBe(defaultInputs().startFte);
    expect(n.priceAi).toBe(0);
    expect(n.hires).toHaveLength(1);
    expect(n.monthlyUtil).toHaveLength(12);
    expect(() => parseImport('{"foo":1}')).toThrow();
  });
});
