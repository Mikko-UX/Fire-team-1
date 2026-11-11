import type { ReactNode } from 'react';
import {
  Area, Bar, BarChart, CartesianGrid, Cell, ComposedChart, Legend, Line, LineChart,
  ReferenceDot, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts';
import { MONTH_SHORT, fmtEur, fmtNum, fmtSignedEur } from '../lib/format';
import type { Result, SensitivityRow, WaterfallStep } from '../model/calc';

const tipStyle = {
  contentStyle: { background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 8, color: 'var(--fg)', fontSize: 12 },
  labelStyle: { color: 'var(--fg)', fontWeight: 600 },
  itemStyle: { color: 'var(--fg)' },
};
const axis = { stroke: 'var(--muted)', fontSize: 11, tickLine: false } as const;
const kAxis = (v: number) => (Math.abs(v) >= 1e6 ? `${fmtNum(v / 1e6, 1)} M` : `${fmtNum(v / 1000)} k`);

function Card({ title, children, note }: { title: string; children: ReactNode; note?: string }) {
  return (
    <section className="card">
      <h3>{title}</h3>
      <div className="h-72 w-full">{children}</div>
      {note && <p className="mt-2 text-xs text-muted">{note}</p>}
    </section>
  );
}

export function ChartsGrid({ result, waterfall, sens }: { result: Result; waterfall: WaterfallStep[]; sens: SensitivityRow[] }) {
  const data = result.months.map((m) => ({
    name: MONTH_SHORT[m.month - 1],
    'AI-design': Math.round(m.revAi),
    'Muu design': Math.round(m.revOther),
    Kuukausitavoite: Math.round(m.target),
    Kumulatiivinen: Math.round(m.cumRevenue),
    Tavoitepolku: Math.round(m.cumTarget),
    'AI-FTE': +m.ai.toFixed(2),
    'Muu FTE': +m.other.toFixed(2),
    'Tarvittu FTE': +m.neededFte.toFixed(2),
    'Kuukausittainen vaje': +m.hireNeed.toFixed(2),
    'Kertynyt vaje': +m.cumHireNeed.toFixed(2),
  }));
  const eur = (v: unknown, n: unknown) => [fmtEur(Number(v)), String(n)] as [string, string];
  const fte = (v: unknown, n: unknown) => [`${fmtNum(Number(v), 1)} FTE`, String(n)] as [string, string];

  // vipuportaikko
  let prev = 0;
  const wf = waterfall.map((s) => {
    const base = s.kind === 'total' ? 0 : Math.min(prev, s.cumulative);
    const bar = s.kind === 'total' ? s.value : Math.abs(s.value);
    prev = s.cumulative;
    return { name: s.label, base, bar, value: s.value, kind: s.kind };
  });
  const wfMin = Math.max(0, Math.floor((Math.min(...waterfall.map((s) => s.cumulative)) * 0.9) / 1e5) * 1e5);

  const tornado = sens.map((r) => ({ name: r.label, '−10 %': Math.round(r.low), '+10 %': Math.round(r.high) }));

  const dec = data[11];

  return (
    <div className="grid grid-cols-1 gap-4 2xl:grid-cols-2">
      <Card title="Kuukausittainen liikevaihto">
        <ResponsiveContainer>
          <ComposedChart data={data} margin={{ top: 5, right: 8, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="var(--grid)" vertical={false} />
            <XAxis dataKey="name" {...axis} />
            <YAxis {...axis} tickFormatter={kAxis} width={48} />
            <Tooltip {...tipStyle} formatter={eur} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="AI-design" stackId="r" fill="var(--ai)" />
            <Bar dataKey="Muu design" stackId="r" fill="var(--other)" />
            <Line dataKey="Kuukausitavoite" stroke="var(--target)" strokeWidth={2} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </Card>

      <Card title="Kumulatiivinen liikevaihto">
        <ResponsiveContainer>
          <LineChart data={data} margin={{ top: 24, right: 24, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="var(--grid)" vertical={false} />
            <XAxis dataKey="name" {...axis} />
            <YAxis {...axis} tickFormatter={kAxis} width={48} />
            <Tooltip {...tipStyle} formatter={eur} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Line dataKey="Kumulatiivinen" stroke="var(--ai)" strokeWidth={2.5} dot={false} />
            <Line dataKey="Tavoitepolku" stroke="var(--target)" strokeWidth={2} strokeDasharray="6 4" dot={false} />
            <ReferenceDot x="Jou" y={dec.Tavoitepolku} r={5} fill="var(--target)" stroke="none"
              label={{ value: `Tavoite ${fmtNum(dec.Tavoitepolku / 1e6, 2)} M€`, position: 'insideTopRight', dy: -16, fill: 'var(--target)', fontSize: 11 }} />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      <Card title="FTE per kuukausi">
        <ResponsiveContainer>
          <ComposedChart data={data} margin={{ top: 5, right: 8, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="var(--grid)" vertical={false} />
            <XAxis dataKey="name" {...axis} />
            <YAxis {...axis} width={36} />
            <Tooltip {...tipStyle} formatter={fte} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Area dataKey="AI-FTE" stackId="f" stroke="var(--ai)" fill="var(--ai)" fillOpacity={0.55} />
            <Area dataKey="Muu FTE" stackId="f" stroke="var(--other)" fill="var(--other)" fillOpacity={0.55} />
            <Line dataKey="Tarvittu FTE" name="Tarvittu FTE kuukausitavoitteeseen" stroke="var(--target)" strokeWidth={2} strokeDasharray="6 4" dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </Card>

      <Card title="Rekrytarve per kuukausi" note="Kertynyt vaje = suurin kuukausittainen FTE-vaje tähän kuukauteen mennessä.">
        <ResponsiveContainer>
          <ComposedChart data={data} margin={{ top: 5, right: 8, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="var(--grid)" vertical={false} />
            <XAxis dataKey="name" {...axis} />
            <YAxis {...axis} width={36} />
            <Tooltip {...tipStyle} formatter={fte} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="Kuukausittainen vaje" fill="var(--other)" />
            <Line dataKey="Kertynyt vaje" stroke="var(--target)" strokeWidth={2} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </Card>

      <Card title="Vipuportaikko (vuoden liikevaihto)">
        <ResponsiveContainer>
          <BarChart data={wf} layout="vertical" margin={{ top: 5, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="var(--grid)" horizontal={false} />
            <XAxis type="number" {...axis} tickFormatter={kAxis} domain={[wfMin, 'auto']} allowDataOverflow />
            <YAxis type="category" dataKey="name" {...axis} width={135} interval={0} />
            <Tooltip {...tipStyle} cursor={{ fill: 'transparent' }}
              formatter={(_v: unknown, _n: unknown, p: { payload?: { value: number; kind: string } }) => {
                const pl = p.payload!;
                return [pl.kind === 'total' ? fmtEur(pl.value) : fmtSignedEur(pl.value), pl.kind === 'total' ? 'Taso' : 'Lisä'] as [string, string];
              }} />
            <Bar dataKey="base" stackId="w" fill="transparent" isAnimationActive={false} />
            <Bar dataKey="bar" stackId="w" isAnimationActive={false}>
              {wf.map((w, i) => (
                <Cell key={i} fill={w.kind === 'total' ? 'var(--muted)' : w.value >= 0 ? 'var(--pos)' : 'var(--neg)'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>

      <Card title="Herkkyys (tornado): syöte ±10 %" note="Vaikutus vuoden liikevaihtoon, lajiteltu suurimmasta pienimpään.">
        <ResponsiveContainer>
          <BarChart data={tornado} layout="vertical" stackOffset="sign" margin={{ top: 5, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="var(--grid)" horizontal={false} />
            <XAxis type="number" {...axis} tickFormatter={kAxis} />
            <YAxis type="category" dataKey="name" {...axis} width={120} interval={0} />
            <Tooltip {...tipStyle} cursor={{ fill: 'transparent' }} formatter={(v: unknown, n: unknown) => [fmtSignedEur(Number(v)), String(n)] as [string, string]} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <ReferenceLine x={0} stroke="var(--muted)" />
            <Bar dataKey="−10 %" stackId="t" fill="var(--neg)" />
            <Bar dataKey="+10 %" stackId="t" fill="var(--pos)" />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </div>
  );
}
