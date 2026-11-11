import type { ReactNode } from 'react';
import { defaultHires, defaultInputs, hire, type HireRow, type Inputs } from '../model/calc';
import { MONTH_LONG, MONTH_SHORT } from '../lib/format';
import { MiniNum, NumField } from './NumField';

const D = defaultInputs();

function Section({ title, children, open = true }: { title: string; children: ReactNode; open?: boolean }) {
  return (
    <details open={open} className="card group !p-0">
      <summary className="flex cursor-pointer select-none items-center justify-between px-4 py-3 text-sm font-semibold">
        {title}
        <span className="text-muted transition-transform group-open:rotate-90">›</span>
      </summary>
      <div className="border-t border-line px-4 pb-3 pt-1">{children}</div>
    </details>
  );
}

function MonthGrid({
  values, onChange, placeholder, labelPrefix, allowNull,
}: {
  values: (number | null)[];
  onChange: (idx: number, v: number | null) => void;
  placeholder?: string;
  labelPrefix: string;
  allowNull?: boolean;
}) {
  return (
    <div className="grid grid-cols-4 gap-2">
      {values.map((v, i) => (
        <label key={i} className="text-center text-[11px] text-muted">
          {MONTH_SHORT[i]}
          <MiniNum
            value={v}
            allowNull={allowNull}
            placeholder={placeholder}
            label={`${labelPrefix} ${MONTH_LONG[i]}`}
            onChange={(x) => onChange(i, x)}
          />
        </label>
      ))}
    </div>
  );
}

function Toggle({ label, checked, onChange, tip }: { label: string; checked: boolean; onChange: (b: boolean) => void; tip?: string }) {
  return (
    <label className="flex items-center justify-between gap-3 py-2 text-sm font-medium" title={tip}>
      {label}
      <input type="checkbox" className="h-4 w-4 accent-[var(--accent)]" checked={checked} onChange={(e) => onChange(e.target.checked)} />
    </label>
  );
}

function HiresTable({ hires, set }: { hires: HireRow[]; set: (h: HireRow[]) => void }) {
  const upd = (id: string, p: Partial<HireRow>) => set(hires.map((h) => (h.id === id ? { ...h, ...p } : h)));
  const num = (t: string) => {
    const v = parseFloat(t.replace(',', '.'));
    return Number.isNaN(v) ? 0 : Math.max(0, v);
  };
  return (
    <div className="space-y-2 py-2">
      {hires.length === 0 && <p className="text-xs text-muted">Ei rekrytointeja.</p>}
      {hires.map((h) => (
        <div key={h.id} className={`rounded-lg border border-line p-2 ${h.enabled ? '' : 'opacity-50'}`}>
          <div className="grid grid-cols-[auto_1fr_1fr_auto] items-end gap-2">
            <label className="flex flex-col items-center text-[11px] text-muted">
              Käytössä
              <input type="checkbox" className="mt-1.5 h-4 w-4 accent-[var(--accent)]" checked={h.enabled}
                aria-label="Rivi käytössä" onChange={(e) => upd(h.id, { enabled: e.target.checked })} />
            </label>
            <label className="text-[11px] text-muted">
              Aloituskuukausi
              <select className="inp" value={h.startMonth} onChange={(e) => upd(h.id, { startMonth: Number(e.target.value) })}>
                {MONTH_LONG.map((m, i) => <option key={m} value={i + 1}>{i + 1} – {m}</option>)}
              </select>
            </label>
            <label className="text-[11px] text-muted">
              Tyyppi
              <select className="inp" value={h.type} onChange={(e) => upd(h.id, { type: e.target.value as HireRow['type'] })}>
                <option value="ai">AI-design</option>
                <option value="other">Muu design</option>
              </select>
            </label>
            <button type="button" className="btn !px-2" aria-label="Poista rivi" title="Poista rivi"
              onClick={() => set(hires.filter((x) => x.id !== h.id))}>✕</button>
          </div>
          <div className="mt-2 grid grid-cols-2 gap-2">
            <label className="text-[11px] text-muted">
              Lukumäärä (FTE)
              <input className="inp" inputMode="decimal" defaultValue={String(h.count).replace('.', ',')}
                key={`${h.id}-c`} onChange={(e) => upd(h.id, { count: num(e.target.value) })} />
            </label>
            <label className="text-[11px] text-muted">
              Oma €/h (tyhjä = oletus)
              <input className="inp" inputMode="decimal" placeholder={h.type === 'ai' ? 'AI-hinta' : 'Muu hinta'}
                defaultValue={h.rate === null ? '' : String(h.rate).replace('.', ',')} key={`${h.id}-r`}
                onChange={(e) => upd(h.id, { rate: e.target.value.trim() === '' ? null : num(e.target.value) })} />
            </label>
          </div>
          <label className="mt-2 block text-[11px] text-muted">
            Selite
            <input className="inp" value={h.label} placeholder="esim. Aki Ilveskero, Oulu"
              onChange={(e) => upd(h.id, { label: e.target.value })} />
          </label>
        </div>
      ))}
      <div className="flex flex-wrap gap-2">
        <button type="button" className="btn" onClick={() => set([...hires, hire(1, 1, 'ai')])}>+ Lisää rekry</button>
        <button type="button" className="btn" onClick={() => set(defaultHires())}>Palauta suositusrekryt</button>
      </div>
    </div>
  );
}

export function InputsPanel({ inputs: s, set }: { inputs: Inputs; set: (p: Partial<Inputs>) => void }) {
  const setIdx = <T,>(arr: T[], i: number, v: T) => arr.map((x, k) => (k === i ? v : x));

  return (
    <div className="space-y-3">
      <Section title="Tavoite">
        <NumField label="Vuositavoite 2027" unit="€" value={s.targetRevenue} def={D.targetRevenue} sliderMin={5e6} sliderMax={12e6} step={50_000}
          onChange={(v) => set({ targetRevenue: v })} tip="Vuoden 2027 liikevaihtotavoite euroina." />
        <NumField label="Liikevaihto 2026 (vertailu)" unit="€" value={s.revenue2026} def={D.revenue2026} sliderMin={5e6} sliderMax={10e6} step={50_000}
          onChange={(v) => set({ revenue2026: v })} tip="Edellisen vuoden liikevaihto. Määrittää vipuportaikon lähtötason (nykyinen utilisaatio)." />
        <div className="py-2">
          <label className="mb-1 block text-sm font-medium">Kuukausitavoitteen jako</label>
          <select className="inp" value={s.targetSplit} onChange={(e) => set({ targetSplit: e.target.value as Inputs['targetSplit'] })}>
            <option value="even">Tasan</option>
            <option value="capacity">Kapasiteetin mukaan</option>
            <option value="custom">Oma (12 painoa)</option>
          </select>
          {s.targetSplit === 'custom' && (
            <div className="mt-2">
              <p className="mb-1 text-xs text-muted">Suhteelliset painot; summa skaalataan vuositavoitteeseen.</p>
              <MonthGrid values={s.customWeights} labelPrefix="Tavoitepaino" onChange={(i, v) => set({ customWeights: setIdx(s.customWeights, i, v ?? 0) })} />
            </div>
          )}
        </div>
      </Section>

      <Section title="Henkilöstö">
        <NumField label="Lähtö-FTE 1.1.2027" unit="FTE" value={s.startFte} def={D.startFte} sliderMin={40} sliderMax={90} step={1} decimals={1}
          onChange={(v) => set({ startFte: v })} tip="Designereiden määrä vuoden alussa (kaikki design-FTE:t)." />
        <NumField label="Joista AI-designereita" unit="FTE" value={s.startAi} def={D.startAi} sliderMin={0} sliderMax={60} step={1} decimals={1}
          onChange={(v) => set({ startAi: v })} tip="Lähtö-FTE:stä AI-hintaisessa työssä olevien määrä. Ei saa ylittää lähtö-FTE:tä." />
        <NumField label="Poistuma" unit="hlö/v" value={s.attrition} def={D.attrition} sliderMin={0} sliderMax={15} step={1} decimals={1}
          onChange={(v) => set({ attrition: v })} tip="Lähtijöitä vuodessa; jaetaan tasan vuodelle ja vähennetään muu design -FTE:istä." />
        <Toggle label="Lähtijät korvataan" checked={s.replaceLeavers} onChange={(b) => set({ replaceLeavers: b })}
          tip="Korvaava henkilö tulee yhden kuukauden viiveellä." />
        <NumField label="Uuden rekryn tuottavuuden nousuaika" unit="kk" value={s.rampMonths} def={D.rampMonths} sliderMin={0} sliderMax={6} step={1} decimals={1}
          onChange={(v) => set({ rampMonths: v })} tip="Montako kuukautta uudella rekryllä menee 100 % tuottavuuteen. 0 = heti täysi tuottavuus." />
        <NumField label="Tuottavuus ensimmäisenä kuukautena" unit="%" value={s.rampStartPct} def={D.rampStartPct} sliderMin={0} sliderMax={100} step={5}
          disabled={s.rampMonths <= 0}
          onChange={(v) => set({ rampStartPct: v })} tip="Käytössä, jos nousuaika > 0. Tuottavuus nousee lineaarisesti tästä 100 %:iin." />
      </Section>

      <Section title="Hinnat ja tunnit">
        <NumField label="AI-design" unit="€/h" value={s.priceAi} def={D.priceAi} sliderMin={80} sliderMax={180} step={1} decimals={0}
          onChange={(v) => set({ priceAi: v })} tip="AI-designerin laskutushinta." />
        <NumField label="Muu design (UX/Visual/Product)" unit="€/h" value={s.priceOther} def={D.priceOther} sliderMin={70} sliderMax={150} step={1}
          onChange={(v) => set({ priceOther: v })} tip="Muun designin laskutushinta." />
        <NumField label="Tuntia / FTE / vuosi" unit="h" value={s.hoursPerYear} def={D.hoursPerYear} sliderMin={1400} sliderMax={1800} step={10}
          onChange={(v) => set({ hoursPerYear: v })} tip="Vuosityöaika tunteina yhtä FTE:tä kohden." />
        <NumField label="Utilisaatio (koko vuosi)" unit="%" value={s.utilization} def={D.utilization} sliderMin={50} sliderMax={95} step={0.5} decimals={1}
          onChange={(v) => set({ utilization: v })} tip="Laskutusaste. Kuukausikohtaiset arvot (alla) ylikirjoittavat tämän yksittäisille kuukausille." />
        <details className="py-2">
          <summary className="cursor-pointer text-sm font-medium">Utilisaatio kuukausittain</summary>
          <p className="my-1 text-xs text-muted">Tyhjä kenttä = koko vuoden arvo ({s.utilization} %).</p>
          <MonthGrid values={s.monthlyUtil} allowNull placeholder={String(s.utilization)} labelPrefix="Utilisaatio %"
            onChange={(i, v) => set({ monthlyUtil: setIdx(s.monthlyUtil, i, v) })} />
          <button type="button" className="btn mt-2" onClick={() => set({ monthlyUtil: Array(12).fill(null) })}>Tyhjennä kuukausiarvot</button>
        </details>
        <details className="py-2">
          <summary className="cursor-pointer text-sm font-medium">Työpäiväpainot kuukausittain</summary>
          <Toggle label="Käytä työpäiväpainoja" checked={s.useWorkdayWeights} onChange={(b) => set({ useWorkdayWeights: b })}
            tip="Jos pois päältä, kuukaudet ovat tasan 1/12." />
          <p className="mb-1 text-xs text-muted">Suhteelliset painot (esim. työpäivien määrä); skaalataan summaan 12.</p>
          <MonthGrid values={s.workdayWeights} labelPrefix="Työpäiväpaino" onChange={(i, v) => set({ workdayWeights: setIdx(s.workdayWeights, i, v ?? 0) })} />
          <button type="button" className="btn mt-2" onClick={() => set({ workdayWeights: Array(12).fill(1) })}>Tasan</button>
        </details>
      </Section>

      <Section title="Konversio">
        <p className="pt-1 text-xs text-muted">Siirtää FTE:n muusta designista AI-designiin (hinta nousee). Ei lisää FTE:itä.</p>
        <NumField label="Konversioita per kk" unit="FTE" value={s.conversionsPerMonth} def={D.conversionsPerMonth} sliderMin={0} sliderMax={5} step={0.5} decimals={1}
          onChange={(v) => set({ conversionsPerMonth: v })} tip="Kuinka monta FTE:tä siirtyy AI-hintaiseen työhön kuukaudessa." />
        <NumField label="Ensimmäinen konversiokuukausi" unit="kk" value={s.conversionFirst} def={D.conversionFirst} sliderMin={1} sliderMax={12} step={1}
          onChange={(v) => set({ conversionFirst: Math.round(v) })} tip="1 = tammikuu … 12 = joulukuu." />
        <NumField label="Viimeinen konversiokuukausi" unit="kk" value={s.conversionLast} def={D.conversionLast} sliderMin={1} sliderMax={12} step={1}
          onChange={(v) => set({ conversionLast: Math.round(v) })} tip="Viimeinen kuukausi, jolloin konversioita tehdään." />
      </Section>

      <Section title="Rekrytoinnit">
        <HiresTable hires={s.hires} set={(hires) => set({ hires })} />
      </Section>

      <Section title="Kate- ja palkkatarkistus" open={false}>
        <NumField label="Keskipalkka" unit="€/kk" value={s.avgSalary} def={D.avgSalary} sliderMin={3000} sliderMax={7000} step={50}
          onChange={(v) => set({ avgSalary: v })} tip="Designerin keskimääräinen kuukausipalkka." />
        <NumField label="Sivukulut" unit="%" value={s.socialPct} def={D.socialPct} sliderMin={0} sliderMax={40} step={0.5} decimals={1}
          onChange={(v) => set({ socialPct: v })} tip="Työnantajan sivukulut palkan päälle." />
        <NumField label="Palkkakuukausia / v" unit="kk" value={s.salaryMonths} def={D.salaryMonths} sliderMin={12} sliderMax={14} step={0.1} decimals={1}
          onChange={(v) => set({ salaryMonths: v })} tip="Esim. 12,5 sisältää lomarahan." />
        <NumField label="Kate-tavoite" unit="%" value={s.marginTarget} def={D.marginTarget} sliderMin={0} sliderMax={70} step={1}
          onChange={(v) => set({ marginTarget: v })} tip="Tavoiteltu kate liikevaihdosta." />
      </Section>
    </div>
  );
}
