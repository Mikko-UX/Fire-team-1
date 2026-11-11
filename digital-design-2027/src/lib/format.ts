const nf = (d: number) => new Intl.NumberFormat('fi-FI', { minimumFractionDigits: d, maximumFractionDigits: d });
const cache: Record<number, Intl.NumberFormat> = {};
const get = (d: number) => (cache[d] ??= nf(d));

export const MONTH_SHORT = ['Tam', 'Hel', 'Maa', 'Huh', 'Tou', 'Kes', 'Hei', 'Elo', 'Syy', 'Lok', 'Mar', 'Jou'];
export const MONTH_LONG = [
  'Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu', 'Toukokuu', 'Kesäkuu',
  'Heinäkuu', 'Elokuu', 'Syyskuu', 'Lokakuu', 'Marraskuu', 'Joulukuu',
];

export const fmtNum = (n: number, d = 0) => get(d).format(Number.isFinite(n) ? n : 0);
export const fmtEur = (n: number) => `${fmtNum(n)} €`;
export const fmtSignedEur = (n: number) => `${n > 0 ? '+' : n < 0 ? '−' : ''}${fmtNum(Math.abs(n))} €`;
export const fmtK = (n: number) => `${fmtNum(n / 1000)} k€`;
export const fmtM = (n: number, d = 2) => `${fmtNum(n / 1e6, d)} M€`;
export const fmtPct = (frac: number, d = 1) => `${fmtNum(frac * 100, d)} %`;
export const fmtSignedPct = (frac: number, d = 1) =>
  `${frac > 0 ? '+' : frac < 0 ? '−' : ''}${fmtNum(Math.abs(frac) * 100, d)} %`;
