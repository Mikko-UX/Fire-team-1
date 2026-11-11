import { MONTH_LONG, fmtEur, fmtNum, fmtSignedEur } from '../lib/format';
import type { Result } from '../model/calc';

export function MonthlyTable({ result, name }: { result: Result; name: string }) {
  const { months, summary } = result;

  const exportCsv = () => {
    const n = (v: number, d = 2) => v.toFixed(d).replace('.', ',');
    const head = ['Kuukausi', 'HC', 'AI-FTE', 'Muu FTE', 'Sekahinta €/h', 'Utilisaatio %', 'Liikevaihto €', 'Kuukausitavoite €', 'Ero €', 'Rekrytarve FTE'];
    const lines = [
      head,
      ...months.map((m) => [
        MONTH_LONG[m.month - 1], n(m.hc), n(m.ai), n(m.other), n(m.blended, 1), n(m.util, 1),
        n(m.revenue, 0), n(m.target, 0), n(m.diff, 0), n(m.hireNeed),
      ]),
      ['Yhteensä', '', '', '', n(summary.blendedYear, 1), '', n(summary.revenue, 0), n(summary.target, 0), n(summary.gap, 0), ''],
    ];
    const csv = '﻿' + lines.map((l) => l.join(';')).join('\r\n');
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    const a = document.createElement('a');
    a.href = url;
    a.download = `${name.replace(/[^\p{L}\p{N}]+/gu, '-')}-kuukausitaulukko.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const th = 'whitespace-nowrap px-2 py-1.5 text-right text-xs font-medium text-muted';
  const td = 'whitespace-nowrap px-2 py-1.5 text-right tabular-nums';
  return (
    <section className="card">
      <div className="mb-3 flex items-center justify-between gap-2">
        <h3 className="!mb-0">Kuukausitaulukko</h3>
        <button type="button" className="btn" onClick={exportCsv}>Vie CSV</button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-line">
              <th className={`${th} !text-left`}>Kuukausi</th>
              <th className={th}>HC</th><th className={th}>AI-FTE</th><th className={th}>Muu FTE</th>
              <th className={th}>Sekahinta</th><th className={th}>Util.</th>
              <th className={th}>Liikevaihto</th><th className={th}>Kk-tavoite</th>
              <th className={th}>Ero</th><th className={th}>Rekrytarve</th>
            </tr>
          </thead>
          <tbody>
            {months.map((m) => (
              <tr key={m.month} className="border-b border-line">
                <td className={`${td} !text-left`}>{MONTH_LONG[m.month - 1]}</td>
                <td className={td}>{fmtNum(m.hc, 1)}</td>
                <td className={td}>{fmtNum(m.ai, 1)}</td>
                <td className={td}>{fmtNum(m.other, 1)}</td>
                <td className={td}>{fmtNum(m.blended, 1)} €/h</td>
                <td className={td}>{fmtNum(m.util, 1)} %</td>
                <td className={td}>{fmtEur(m.revenue)}</td>
                <td className={td}>{fmtEur(m.target)}</td>
                <td className={`${td} ${m.diff >= 0 ? 'text-pos' : 'text-neg'}`}>{fmtSignedEur(m.diff)}</td>
                <td className={td}>{fmtNum(m.hireNeed, 1)}</td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr className="font-semibold">
              <td className={`${td} !text-left`}>Yhteensä</td>
              <td className={td} colSpan={3}></td>
              <td className={td}>{fmtNum(summary.blendedYear, 1)} €/h</td>
              <td className={td}></td>
              <td className={td}>{fmtEur(summary.revenue)}</td>
              <td className={td}>{fmtEur(summary.target)}</td>
              <td className={`${td} ${summary.gap >= 0 ? 'text-pos' : 'text-neg'}`}>{fmtSignedEur(summary.gap)}</td>
              <td className={td}></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </section>
  );
}
