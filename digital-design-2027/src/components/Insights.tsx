import { fmtEur, fmtNum, fmtPct, fmtSignedEur, fmtSignedPct, MONTH_LONG } from '../lib/format';
import type { ExtraHireRow, Result } from '../model/calc';

export function KpiRow({ result }: { result: Result }) {
  const s = result.summary;
  const pos = s.gap >= 0;
  const items = [
    { label: 'Liikevaihto 2027', value: fmtEur(s.revenue), tone: '' },
    { label: 'Tavoite', value: fmtEur(s.target), tone: '' },
    {
      label: 'Ero tavoitteeseen',
      value: `${fmtSignedEur(s.gap)} (${fmtSignedPct(s.gapPct)})`,
      tone: pos ? 'text-pos' : 'text-neg',
      icon: pos ? '▲' : '▼',
    },
    { label: 'FTE joulukuussa', value: fmtNum(s.hcDec, 1), tone: '' },
    { label: 'Rekryjä yhteensä', value: fmtNum(s.hiresTotal, 1), tone: '' },
    { label: 'AI-osuus liikevaihdosta', value: fmtPct(s.aiShareRevYear), tone: '' },
  ];
  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
      {items.map((k) => (
        <div key={k.label} className="card !p-3">
          <div className="text-xs text-muted">{k.label}</div>
          <div className={`mt-1 break-words text-base font-semibold leading-tight sm:text-lg ${k.tone}`}>
            {k.icon && <span aria-hidden className="mr-1 text-xs">{k.icon}</span>}
            {k.value}
          </div>
        </div>
      ))}
    </div>
  );
}

export function Warnings({ warnings }: { warnings: string[] }) {
  if (!warnings.length) return null;
  return (
    <div role="alert" className="rounded-xl border border-warn p-3 text-sm text-warn">
      {warnings.map((w) => <p key={w}>⚠ {w}</p>)}
    </div>
  );
}

export function KeyFigures({ result }: { result: Result }) {
  const s = result.summary;
  const m = result.margin;
  const rows: [string, string][] = [
    ['AI-osuus FTE:stä, joulukuu', fmtPct(s.aiShareFteDec)],
    ['AI-osuus FTE:stä, vuosi', fmtPct(s.aiShareFteYear)],
    ['AI-osuus liikevaihdosta, joulukuu', fmtPct(s.aiShareRevDec)],
    ['AI-osuus liikevaihdosta, vuosi', fmtPct(s.aiShareRevYear)],
    ['Sekahinta (vuoden ka)', `${fmtNum(s.blendedYear, 1)} €/h`],
    ['Rev/FTE', `${fmtEur(s.revPerFteMonth)} / kk`],
    ['HC joulukuussa', fmtNum(s.hcDec, 1)],
    ['Rekryjä yhteensä', fmtNum(s.hiresTotal, 1)],
  ];
  const st = {
    ok: { cls: 'text-pos', icon: '●', text: 'Vihreä – kate riittää' },
    warn: { cls: 'text-warn', icon: '●', text: 'Keltainen – rajalla (alle 5 % marginaali)' },
    bad: { cls: 'text-neg', icon: '●', text: 'Punainen – palkka ylittää katetavoitteen' },
  }[m.status];
  return (
    <section className="card">
      <h3>Tunnusluvut ja katetarkistus</h3>
      <dl className="grid grid-cols-1 gap-x-6 gap-y-1 text-sm sm:grid-cols-2">
        {rows.map(([k, v]) => (
          <div key={k} className="flex justify-between gap-3 border-b border-line py-1">
            <dt className="text-muted">{k}</dt>
            <dd className="font-medium">{v}</dd>
          </div>
        ))}
      </dl>
      <div className="mt-4 rounded-lg border border-line p-3 text-sm">
        <div className={`mb-2 font-semibold ${st.cls}`}>
          <span aria-hidden>{st.icon}</span> {st.text}
        </div>
        <div className="grid grid-cols-1 gap-1 sm:grid-cols-3">
          <div><div className="text-xs text-muted">Max. kustannus</div>{fmtNum(m.maxCostPerHour, 1)} €/h</div>
          <div><div className="text-xs text-muted">Max. keskipalkka</div>{fmtEur(m.maxSalary)} / kk</div>
          <div><div className="text-xs text-muted">Syötetty keskipalkka</div>{fmtEur(m.salary)} / kk</div>
        </div>
        <p className="mt-2 text-xs text-muted">
          Vihreä: palkka ≤ 95 % maksimista, keltainen: ≤ 100 %, punainen: yli maksimin.
        </p>
      </div>
    </section>
  );
}

export function ExtraHiring({ rows, shortfall }: { rows: ExtraHireRow[]; shortfall: number }) {
  return (
    <section className="card">
      <h3>Lisärekrytarve vuositavoitteeseen</h3>
      {rows.length === 0 ? (
        <p className="text-sm text-pos">Toteuma saavuttaa vuositavoitteen – lisärekrytarvetta ei ole.</p>
      ) : (
        <>
          <p className="mb-2 text-sm">
            Vaje tavoitteeseen: <strong>{fmtEur(shortfall)}</strong>. Lisähenkilöiden tarve, jos he aloittavat:
          </p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-xs text-muted">
                  <th className="py-1 pr-3">Aloitus</th>
                  <th className="py-1 pr-3">Hinta</th>
                  <th className="py-1 text-right">Lisähenkilöä (FTE)</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={`${r.startMonth}-${r.type}`} className="border-b border-line">
                    <td className="py-1 pr-3">{MONTH_LONG[r.startMonth - 1]}</td>
                    <td className="py-1 pr-3">{r.type === 'ai' ? 'AI' : 'Muu'} {fmtNum(r.price)} €/h</td>
                    <td className="py-1 text-right font-medium">{fmtNum(r.fte, 1)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-2 text-xs text-muted">Tunnit vuoden keskiarvolla; tarve = vaje / (tunnit × hinta × jäljellä olevat kuukaudet).</p>
        </>
      )}
    </section>
  );
}
