/**
 * Digital Design 2027 – laskentamalli.
 * Puhdas moduuli: ei UI-riippuvuuksia.
 */

export const MONTH_COUNT = 12;

export type HireType = 'ai' | 'other';
export type TargetSplit = 'even' | 'capacity' | 'custom';

export interface HireRow {
  id: string;
  startMonth: number; // 1..12
  count: number; // desimaalit sallittu
  type: HireType;
  rate: number | null; // oma €/h, null = tyypin oletushinta
  label: string;
  enabled: boolean;
}

export interface Inputs {
  // Tavoite
  targetRevenue: number;
  revenue2026: number;
  targetSplit: TargetSplit;
  customWeights: number[]; // 12 painoa
  // Henkilöstö
  startFte: number;
  startAi: number;
  attrition: number; // lähtijöitä vuodessa
  replaceLeavers: boolean;
  rampMonths: number;
  rampStartPct: number;
  // Hinnat ja tunnit
  priceAi: number;
  priceOther: number;
  hoursPerYear: number;
  utilization: number; // %
  monthlyUtil: (number | null)[]; // % tai null = käytä koko vuoden arvoa
  useWorkdayWeights: boolean;
  workdayWeights: number[]; // suhteelliset painot
  // Konversio
  conversionsPerMonth: number;
  conversionFirst: number;
  conversionLast: number;
  // Rekrytoinnit
  hires: HireRow[];
  // Kate
  avgSalary: number;
  socialPct: number;
  salaryMonths: number;
  marginTarget: number; // %
}

let idCounter = 0;
export function newId(): string {
  idCounter += 1;
  return `h${Date.now().toString(36)}${idCounter.toString(36)}${Math.random().toString(36).slice(2, 5)}`;
}

export function hire(
  startMonth: number,
  count: number,
  type: HireType,
  label = '',
  rate: number | null = null,
): HireRow {
  return { id: newId(), startMonth, count, type, rate, label, enabled: true };
}

export function defaultHires(): HireRow[] {
  return [hire(1, 2, 'ai'), hire(2, 2, 'ai'), hire(4, 3, 'ai'), hire(7, 2, 'other')];
}

/** Oletusarvot = "Suositus (portitettu)" -skenaario. */
export function defaultInputs(): Inputs {
  return {
    targetRevenue: 8_700_000,
    revenue2026: 7_000_000,
    targetSplit: 'even',
    customWeights: Array(12).fill(1),
    startFte: 56,
    startAi: 10,
    attrition: 0,
    replaceLeavers: false,
    rampMonths: 0,
    rampStartPct: 50,
    priceAi: 120,
    priceOther: 100,
    hoursPerYear: 1640,
    utilization: 78,
    monthlyUtil: Array(12).fill(null),
    useWorkdayWeights: false,
    workdayWeights: Array(12).fill(1),
    conversionsPerMonth: 1,
    conversionFirst: 1,
    conversionLast: 12,
    hires: defaultHires(),
    avgSalary: 4850,
    socialPct: 22,
    salaryMonths: 12.5,
    marginTarget: 40,
  };
}

// ---------------------------------------------------------------- apurit

const sum = (a: number[]) => a.reduce((x, y) => x + y, 0);
const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));
/** Ei-negatiivinen äärellinen luku, muuten 0. */
const nn = (v: unknown): number => (typeof v === 'number' && Number.isFinite(v) && v > 0 ? v : 0);
const month = (v: unknown): number =>
  typeof v === 'number' && Number.isFinite(v) ? clamp(Math.round(v), 1, 12) : 1;

function arr12<T>(a: T[] | undefined, fill: T): T[] {
  return Array.from({ length: 12 }, (_, k) => (a && a[k] !== undefined ? a[k] : fill));
}

/** Siivoaa syötteet: ei negatiivisia arvoja, kuukaudet 1–12, taulukot pituudeltaan 12. */
export function sanitize(i: Inputs): Inputs {
  return {
    ...i,
    targetRevenue: nn(i.targetRevenue),
    revenue2026: nn(i.revenue2026),
    customWeights: arr12(i.customWeights, 1).map(nn),
    startFte: nn(i.startFte),
    startAi: nn(i.startAi),
    attrition: nn(i.attrition),
    rampMonths: nn(i.rampMonths),
    rampStartPct: clamp(nn(i.rampStartPct), 0, 100),
    priceAi: nn(i.priceAi),
    priceOther: nn(i.priceOther),
    hoursPerYear: nn(i.hoursPerYear),
    utilization: nn(i.utilization),
    monthlyUtil: arr12<number | null>(i.monthlyUtil, null).map((v) =>
      v === null || typeof v !== 'number' || !Number.isFinite(v) ? null : Math.max(0, v),
    ),
    workdayWeights: arr12(i.workdayWeights, 1).map(nn),
    conversionsPerMonth: nn(i.conversionsPerMonth),
    conversionFirst: month(i.conversionFirst),
    conversionLast: month(i.conversionLast),
    hires: (i.hires ?? []).map((h) => ({
      ...h,
      startMonth: month(h.startMonth),
      count: nn(h.count),
      rate: h.rate === null || typeof h.rate !== 'number' || !Number.isFinite(h.rate) ? null : Math.max(0, h.rate),
    })),
    avgSalary: nn(i.avgSalary),
    socialPct: nn(i.socialPct),
    salaryMonths: nn(i.salaryMonths),
    marginTarget: clamp(nn(i.marginTarget), 0, 100),
  };
}

// ---------------------------------------------------------------- tulokset

export interface MonthResult {
  month: number; // 1..12
  hc: number;
  ai: number;
  other: number;
  hoursPerFte: number; // laskutettavia tunteja per FTE
  util: number; // %
  blended: number; // sekahinta €/h
  revAi: number;
  revOther: number;
  revenue: number;
  target: number;
  diff: number; // liikevaihto − kuukausitavoite
  neededFte: number;
  hireNeed: number; // max(0, tarvittu − HC)
  cumHireNeed: number; // kertynyt vaje (suurin tarve tähän asti)
  cumRevenue: number;
  cumTarget: number;
}

export type MarginStatus = 'ok' | 'warn' | 'bad';

export interface Margin {
  maxCostPerHour: number;
  maxSalary: number;
  salary: number;
  status: MarginStatus;
}

export interface Summary {
  revenue: number;
  target: number;
  gap: number; // liikevaihto − tavoite
  gapPct: number;
  shortfall: number; // max(0, tavoite − liikevaihto)
  quarters: number[];
  hcDec: number;
  aiDec: number;
  aiShareFteDec: number;
  aiShareFteYear: number;
  aiShareRevDec: number;
  aiShareRevYear: number;
  blendedYear: number;
  revPerFteMonth: number;
  hiresTotal: number;
  avgHoursPerFte: number;
}

export interface Result {
  months: MonthResult[];
  summary: Summary;
  margin: Margin;
  warnings: string[];
}

export function calculate(raw: Inputs): Result {
  const inp = sanitize(raw);
  const warnings: string[] = [];

  const wsum = inp.useWorkdayWeights ? sum(inp.workdayWeights) : 0;
  const weightFactor = (k: number) => (wsum > 0 ? (12 * inp.workdayWeights[k]) / wsum : 1);

  const rows = inp.hires.filter((h) => h.enabled && h.count > 0);
  const R = inp.rampMonths;
  const r0 = inp.rampStartPct / 100;
  const prod = (monthsSinceStart: number) =>
    R > 0 ? r0 + (1 - r0) * Math.min(1, monthsSinceStart / R) : 1;

  let capped = false;
  let aiOver = false;
  let negHc = false;

  type Raw = Omit<MonthResult, 'target' | 'diff' | 'neededFte' | 'hireNeed' | 'cumHireNeed' | 'cumRevenue' | 'cumTarget'>;
  const raws: Raw[] = [];

  for (let k = 0; k < 12; k++) {
    const m = k + 1;
    let hiresAll = 0;
    let hiresAi = 0;
    let lossAi = 0;
    let lossOther = 0;
    let customAiEff = 0;
    let customOtherEff = 0;
    let customRevAi = 0; // Σ eff · oma hinta
    let customRevOther = 0;
    for (const h of rows) {
      if (h.startMonth > m) continue;
      const f = prod(m - h.startMonth);
      hiresAll += h.count;
      if (h.type === 'ai') {
        hiresAi += h.count;
        lossAi += h.count * (1 - f);
      } else {
        lossOther += h.count * (1 - f);
      }
      if (h.rate !== null) {
        const eff = h.count * f;
        if (h.type === 'ai') {
          customAiEff += eff;
          customRevAi += eff * h.rate;
        } else {
          customOtherEff += eff;
          customRevOther += eff * h.rate;
        }
      }
    }

    const leavers = (inp.attrition * m) / 12;
    const replaced = inp.replaceLeavers ? (inp.attrition * (m - 1)) / 12 : 0;
    let hc = inp.startFte + hiresAll - leavers + replaced;
    if (hc < 0) {
      negHc = true;
      hc = 0;
    }

    const aiBase = inp.startAi + hiresAi;
    const nConv =
      inp.conversionLast >= inp.conversionFirst
        ? clamp(m - inp.conversionFirst + 1, 0, inp.conversionLast - inp.conversionFirst + 1)
        : 0;
    const convRaw = inp.conversionsPerMonth * nConv;
    const conv = Math.min(convRaw, Math.max(0, hc - aiBase));
    if (conv < convRaw - 1e-9) capped = true;

    let ai = aiBase + conv;
    if (ai > hc + 1e-9) {
      aiOver = true;
      ai = hc;
    }
    const other = hc - ai;

    const aiEff = Math.max(0, ai - lossAi);
    const otherEff = Math.max(0, other - lossOther);
    const aiStd = Math.max(0, aiEff - customAiEff);
    const otherStd = Math.max(0, otherEff - customOtherEff);

    const util = inp.monthlyUtil[k] ?? inp.utilization;
    const hoursPerFte = (inp.hoursPerYear / 12) * weightFactor(k) * (util / 100);

    const revAi = (aiStd * inp.priceAi + customRevAi) * hoursPerFte;
    const revOther = (otherStd * inp.priceOther + customRevOther) * hoursPerFte;
    const revenue = revAi + revOther;
    const blended = hc > 0 && hoursPerFte > 0 ? revenue / (hc * hoursPerFte) : 0;

    raws.push({ month: m, hc, ai, other, hoursPerFte, util, blended, revAi, revOther, revenue });
  }

  // Kuukausitavoitteet
  const capW = raws.map((r) => r.hc * r.hoursPerFte);
  let weights: number[];
  if (inp.targetSplit === 'capacity' && sum(capW) > 0) weights = capW;
  else if (inp.targetSplit === 'custom' && sum(inp.customWeights) > 0) weights = inp.customWeights;
  else weights = Array(12).fill(1);
  const wTotal = sum(weights);

  let cumRevenue = 0;
  let cumTarget = 0;
  let cumHireNeed = 0;
  const months: MonthResult[] = raws.map((r, k) => {
    const target = (inp.targetRevenue * weights[k]) / wTotal;
    const neededFte = r.blended > 0 && r.hoursPerFte > 0 ? target / (r.blended * r.hoursPerFte) : 0;
    const hireNeed = Math.max(0, neededFte - r.hc);
    cumHireNeed = Math.max(cumHireNeed, hireNeed);
    cumRevenue += r.revenue;
    cumTarget += target;
    return {
      ...r,
      target,
      diff: r.revenue - target,
      neededFte,
      hireNeed,
      cumHireNeed,
      cumRevenue,
      cumTarget,
    };
  });

  // Yhteenveto
  const revenue = sum(months.map((x) => x.revenue));
  const target = inp.targetRevenue;
  const gap = revenue - target;
  const quarters = [0, 1, 2, 3].map((q) => sum(months.slice(q * 3, q * 3 + 3).map((x) => x.revenue)));
  const dec = months[11];
  const hcSum = sum(months.map((x) => x.hc));
  const aiSum = sum(months.map((x) => x.ai));
  const revAiYear = sum(months.map((x) => x.revAi));
  const fteHours = sum(months.map((x) => x.hc * x.hoursPerFte));
  const blendedYear = fteHours > 0 ? revenue / fteHours : 0;
  const avgUtil = sum(months.map((x) => x.util)) / 12;

  const summary: Summary = {
    revenue,
    target,
    gap,
    gapPct: target > 0 ? gap / target : 0,
    shortfall: Math.max(0, target - revenue),
    quarters,
    hcDec: dec.hc,
    aiDec: dec.ai,
    aiShareFteDec: dec.hc > 0 ? dec.ai / dec.hc : 0,
    aiShareFteYear: hcSum > 0 ? aiSum / hcSum : 0,
    aiShareRevDec: dec.revenue > 0 ? dec.revAi / dec.revenue : 0,
    aiShareRevYear: revenue > 0 ? revAiYear / revenue : 0,
    blendedYear,
    revPerFteMonth: hcSum > 0 ? revenue / hcSum : 0,
    hiresTotal: sum(rows.map((h) => h.count)),
    avgHoursPerFte: sum(months.map((x) => x.hoursPerFte)) / 12,
  };

  // Katetarkistus
  const maxCostPerHour = (1 - inp.marginTarget / 100) * blendedYear * (avgUtil / 100);
  const denom = inp.salaryMonths * (1 + inp.socialPct / 100);
  const maxSalary = denom > 0 ? (maxCostPerHour * inp.hoursPerYear) / denom : 0;
  const status: MarginStatus =
    inp.avgSalary <= maxSalary * 0.95 ? 'ok' : inp.avgSalary <= maxSalary ? 'warn' : 'bad';
  const margin: Margin = { maxCostPerHour, maxSalary, salary: inp.avgSalary, status };

  // Varoitukset
  if (inp.startAi > inp.startFte)
    warnings.push('Lähtö-AI-designerien määrä ylittää lähtö-FTE:n. AI-FTE rajataan kokonais-FTE:n määrään.');
  else if (aiOver)
    warnings.push('AI-FTE ylittäisi kokonais-FTE:n joinain kuukausina. AI-FTE rajataan FTE-määrään.');
  if (capped)
    warnings.push('Konversioita on rajattu, jotta AI-FTE ei ylitä kokonais-FTE:tä.');
  if (inp.conversionLast < inp.conversionFirst && inp.conversionsPerMonth > 0)
    warnings.push('Viimeinen konversiokuukausi on ennen ensimmäistä – konversioita ei tehdä.');
  if (negHc) warnings.push('Poistuma ylittää henkilöstön määrän – FTE rajattu nollaan.');

  return { months, summary, margin, warnings };
}

// ---------------------------------------------------------------- lisärekrytarve

export interface ExtraHireRow {
  startMonth: number;
  type: HireType;
  price: number;
  fte: number;
}

/** Kun toteuma jää tavoitteesta: montako lisähenkilöä tarvitaan. Tunnit vuoden keskiarvolla. */
export function additionalHiring(raw: Inputs, result: Result): ExtraHireRow[] {
  const inp = sanitize(raw);
  const gap = result.summary.shortfall;
  if (gap <= 0) return [];
  const hours = result.summary.avgHoursPerFte;
  const rows: ExtraHireRow[] = [];
  for (const startMonth of [1, 4, 7]) {
    for (const type of ['other', 'ai'] as HireType[]) {
      const price = type === 'ai' ? inp.priceAi : inp.priceOther;
      const denom = hours * price * (13 - startMonth);
      rows.push({ startMonth, type, price, fte: denom > 0 ? gap / denom : 0 });
    }
  }
  return rows;
}

// ---------------------------------------------------------------- vipuvaikutukset

export interface WaterfallStep {
  label: string;
  kind: 'total' | 'delta';
  value: number; // total: taso, delta: lisä
  cumulative: number;
}

const revenueOf = (i: Inputs) => calculate(i).summary.revenue;

export function waterfall(raw: Inputs): WaterfallStep[] {
  const s = sanitize(raw);
  const mixPerHour = s.startAi * s.priceAi + Math.max(0, s.startFte - s.startAi) * s.priceOther;
  // "Nykyinen utilisaatio" = taso, jolla lähtöhenkilöstö tuottaa vuoden 2026 liikevaihdon
  const baseUtil =
    mixPerHour > 0 && s.hoursPerYear > 0 ? (s.revenue2026 / (mixPerHour * s.hoursPerYear)) * 100 : s.utilization;

  const base: Inputs = {
    ...s,
    hires: [],
    conversionsPerMonth: 0,
    attrition: 0,
    utilization: baseUtil,
    monthlyUtil: Array(12).fill(null),
  };
  const steps: WaterfallStep[] = [];
  let prev = revenueOf(base);
  steps.push({ label: 'Lähtötaso (2026)', kind: 'total', value: prev, cumulative: prev });

  const add = (label: string, inputs: Inputs) => {
    const cur = revenueOf(inputs);
    steps.push({ label, kind: 'delta', value: cur - prev, cumulative: cur });
    prev = cur;
  };

  let cur: Inputs = { ...base, utilization: s.utilization, monthlyUtil: s.monthlyUtil };
  add('Utilisaatio', cur);
  if (s.attrition > 0) {
    cur = { ...cur, attrition: s.attrition };
    add('Poistuma', cur);
  }
  cur = { ...cur, conversionsPerMonth: s.conversionsPerMonth };
  add('Konversiot', cur);

  const active = s.hires.filter((h) => h.enabled && h.count > 0);
  const MONTHS = ['tammi', 'helmi', 'maalis', 'huhti', 'touko', 'kesä', 'heinä', 'elo', 'syys', 'loka', 'marras', 'joulu'];
  active.forEach((h, idx) => {
    cur = { ...cur, hires: active.slice(0, idx + 1) };
    const name = h.label.trim() || (h.type === 'ai' ? 'AI' : 'Muu');
    add(`Rekry: ${h.count} × ${name}, ${MONTHS[h.startMonth - 1]}`, cur);
  });

  steps.push({ label: 'Yhteensä', kind: 'total', value: prev, cumulative: prev });
  return steps;
}

// ---------------------------------------------------------------- herkkyys

export interface SensitivityRow {
  label: string;
  low: number; // vaikutus liikevaihtoon, kun arvo −10 %
  high: number; // kun arvo +10 %
}

export function sensitivity(raw: Inputs, delta = 0.1): SensitivityRow[] {
  const s = sanitize(raw);
  const base = revenueOf(s);
  const params: { label: string; apply: (i: Inputs, f: number) => Inputs }[] = [
    {
      label: 'Utilisaatio',
      apply: (i, f) => ({
        ...i,
        utilization: i.utilization * f,
        monthlyUtil: i.monthlyUtil.map((v) => (v === null ? null : v * f)),
      }),
    },
    { label: 'AI-design €/h', apply: (i, f) => ({ ...i, priceAi: i.priceAi * f }) },
    { label: 'Muu design €/h', apply: (i, f) => ({ ...i, priceOther: i.priceOther * f }) },
    { label: 'Konversiovauhti', apply: (i, f) => ({ ...i, conversionsPerMonth: i.conversionsPerMonth * f }) },
    { label: 'Lähtö-AI', apply: (i, f) => ({ ...i, startAi: i.startAi * f }) },
    { label: 'Rekrytointien määrä', apply: (i, f) => ({ ...i, hires: i.hires.map((h) => ({ ...h, count: h.count * f })) }) },
  ];
  return params
    .map((p) => ({
      label: p.label,
      low: revenueOf(p.apply(s, 1 - delta)) - base,
      high: revenueOf(p.apply(s, 1 + delta)) - base,
    }))
    .sort((a, b) => Math.max(Math.abs(b.low), Math.abs(b.high)) - Math.max(Math.abs(a.low), Math.abs(a.high)));
}
