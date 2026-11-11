import { useMemo, useState } from 'react';
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { MONTH_SHORT, fmtEur, fmtNum, fmtPct, fmtSignedEur } from '../lib/format';
import { calculate } from '../model/calc';
import type { Scenario } from '../lib/storage';

const COLORS = ['var(--ai)', 'var(--other)', 'var(--target)', 'var(--neg)'];

export function Compare({ scenarios }: { scenarios: Scenario[] }) {
  const [selected, setSelected] = useState<string[]>(() => scenarios.slice(0, 4).map((s) => s.id));
  const chosen = scenarios.filter((s) => selected.includes(s.id)).slice(0, 4);
  const results = useMemo(() => chosen.map((s) => ({ s, r: calculate(s.inputs) })), [chosen]);

  const toggle = (id: string) =>
    setSelected((cur) => (cur.includes(id) ? cur.filter((x) => x !== id) : cur.length >= 4 ? cur : [...cur, id]));

  const data = MONTH_SHORT.map((name, k) => {
    const row: Record<string, number | string> = { name };
    results.forEach(({ s, r }) => (row[s.id] = Math.round(r.months[k].cumRevenue)));
    return row;
  });

  const metrics: [string, (r: ReturnType<typeof calculate>) => string, ((r: ReturnType<typeof calculate>) => string)?][] = [
    ['Liikevaihto', (r) => fmtEur(r.summary.revenue)],
    ['Tavoite', (r) => fmtEur(r.summary.target)],
    ['Ero tavoitteeseen', (r) => fmtSignedEur(r.summary.gap), (r) => (r.summary.gap >= 0 ? 'text-pos' : 'text-neg')],
    ['Ero, %', (r) => `${fmtNum(r.summary.gapPct * 100, 1)} %`, (r) => (r.summary.gap >= 0 ? 'text-pos' : 'text-neg')],
    ['HC joulukuussa', (r) => fmtNum(r.summary.hcDec, 1)],
    ['Rekrytyt yhteensä', (r) => fmtNum(r.summary.hiresTotal, 1)],
    ['AI-osuus liikevaihdosta', (r) => fmtPct(r.summary.aiShareRevYear)],
  ];

  return (
    <div className="space-y-4">
      <section className="card">
        <h3>Valitse 2–4 skenaariota</h3>
        <div className="flex flex-wrap gap-3">
          {scenarios.map((s) => (
            <label key={s.id} className="flex items-center gap-2 text-sm">
              <input type="checkbox" className="h-4 w-4 accent-[var(--accent)]" checked={selected.includes(s.id)}
                disabled={!selected.includes(s.id) && selected.length >= 4} onChange={() => toggle(s.id)} />
              {s.name}
            </label>
          ))}
        </div>
        {chosen.length < 2 && <p className="mt-2 text-sm text-warn">Valitse vähintään kaksi skenaariota.</p>}
      </section>

      {chosen.length >= 1 && (
        <section className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-line text-left">
                <th className="py-1.5 pr-3 text-xs font-medium text-muted">Mittari</th>
                {results.map(({ s }, i) => (
                  <th key={s.id} className="px-2 py-1.5 text-right font-semibold" style={{ color: COLORS[i] }}>{s.name}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {metrics.map(([label, f, cls]) => (
                <tr key={label} className="border-b border-line">
                  <td className="py-1.5 pr-3 text-muted">{label}</td>
                  {results.map(({ s, r }) => (
                    <td key={s.id} className={`whitespace-nowrap px-2 py-1.5 text-right tabular-nums ${cls ? cls(r) : ''}`}>{f(r)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      <section className="card">
        <h3>Kumulatiivinen liikevaihto</h3>
        <div className="h-80 w-full">
          <ResponsiveContainer>
            <LineChart data={data} margin={{ top: 5, right: 16, left: 0, bottom: 0 }}>
              <CartesianGrid stroke="var(--grid)" vertical={false} />
              <XAxis dataKey="name" stroke="var(--muted)" fontSize={11} tickLine={false} />
              <YAxis stroke="var(--muted)" fontSize={11} tickLine={false} width={48} tickFormatter={(v: number) => `${fmtNum(v / 1e6, 1)} M`} />
              <Tooltip contentStyle={{ background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }}
                labelStyle={{ color: 'var(--fg)' }} itemStyle={{ color: 'var(--fg)' }}
                formatter={(v: unknown, n: unknown) => [fmtEur(Number(v)), String(n)] as [string, string]} />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              {results.map(({ s }, i) => (
                <Line key={s.id} dataKey={s.id} name={s.name} stroke={COLORS[i]} strokeWidth={2.5} dot={false} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  );
}
