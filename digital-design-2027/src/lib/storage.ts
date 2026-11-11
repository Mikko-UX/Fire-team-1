import { defaultInputs, newId, sanitize, type HireRow, type Inputs } from '../model/calc';
import { PRESETS } from '../model/presets';

export interface Scenario {
  id: string;
  name: string;
  inputs: Inputs;
}
export interface AppState {
  scenarios: Scenario[];
  activeId: string;
}

const KEY = 'dd2027.state.v1';

// ------------------------------------------------------------ normalisointi

const isNum = (v: unknown): v is number => typeof v === 'number' && Number.isFinite(v);

/** Yhdistää tuntemattoman JSON:n oletusarvoihin kenttä kerrallaan. */
export function normalizeInputs(raw: unknown): Inputs {
  const d = defaultInputs();
  if (!raw || typeof raw !== 'object') return d;
  const r = raw as Record<string, unknown>;
  const out: Record<string, unknown> = { ...d };
  for (const key of Object.keys(d) as (keyof Inputs)[]) {
    const dv = d[key];
    const v = r[key];
    if (v === undefined) continue;
    if (typeof dv === 'number' && isNum(v)) out[key] = v;
    else if (typeof dv === 'boolean' && typeof v === 'boolean') out[key] = v;
    else if (key === 'targetSplit' && (v === 'even' || v === 'capacity' || v === 'custom')) out[key] = v;
    else if (Array.isArray(dv) && Array.isArray(v) && key !== 'hires') {
      out[key] = Array.from({ length: 12 }, (_, i) => {
        const x = v[i];
        return key === 'monthlyUtil' ? (isNum(x) ? x : null) : isNum(x) ? x : (dv as number[])[i];
      });
    } else if (key === 'hires' && Array.isArray(v)) {
      out[key] = v
        .filter((h) => h && typeof h === 'object')
        .map((h: Record<string, unknown>): HireRow => ({
          id: typeof h.id === 'string' ? h.id : newId(),
          startMonth: isNum(h.startMonth) ? h.startMonth : 1,
          count: isNum(h.count) ? h.count : 0,
          type: h.type === 'other' ? 'other' : 'ai',
          rate: isNum(h.rate) ? h.rate : null,
          label: typeof h.label === 'string' ? h.label : '',
          enabled: h.enabled !== false,
        }));
    }
  }
  return sanitize(out as unknown as Inputs);
}

function normalizeScenario(raw: unknown): Scenario | null {
  if (!raw || typeof raw !== 'object') return null;
  const r = raw as Record<string, unknown>;
  return {
    id: newId(),
    name: typeof r.name === 'string' && r.name.trim() ? r.name : 'Tuotu skenaario',
    inputs: normalizeInputs(r.inputs),
  };
}

// ------------------------------------------------------------ localStorage

export function loadState(): AppState | null {
  try {
    const txt = localStorage.getItem(KEY);
    if (!txt) return null;
    const j = JSON.parse(txt);
    if (!j || !Array.isArray(j.scenarios)) return null;
    const scenarios = j.scenarios
      .map((s: unknown) => {
        const n = normalizeScenario(s);
        if (n && s && typeof (s as Scenario).id === 'string') n.id = (s as Scenario).id;
        return n;
      })
      .filter(Boolean) as Scenario[];
    if (!scenarios.length) return null;
    const activeId = scenarios.some((s) => s.id === j.activeId) ? j.activeId : scenarios[0].id;
    return { scenarios, activeId };
  } catch {
    return null;
  }
}

export function saveState(state: AppState): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch {
    /* localStorage ei käytettävissä – sovellus toimii ilman */
  }
}

// ------------------------------------------------------------ URL-hash

function toBase64Url(s: string): string {
  const bytes = new TextEncoder().encode(s);
  let bin = '';
  bytes.forEach((b) => (bin += String.fromCharCode(b)));
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function fromBase64Url(s: string): string {
  const b64 = s.replace(/-/g, '+').replace(/_/g, '/');
  const bin = atob(b64 + '='.repeat((4 - (b64.length % 4)) % 4));
  return new TextDecoder().decode(Uint8Array.from(bin, (c) => c.charCodeAt(0)));
}

export function shareUrl(s: Scenario): string {
  const payload = toBase64Url(JSON.stringify({ name: s.name, inputs: s.inputs }));
  return `${location.origin}${location.pathname}#s=${payload}`;
}

export function scenarioFromHash(hash: string): Scenario | null {
  try {
    const m = /^#s=(.+)$/.exec(hash);
    if (!m) return null;
    const s = normalizeScenario(JSON.parse(fromBase64Url(m[1])));
    return s ? { ...s, name: `Jaettu: ${s.name}` } : null;
  } catch {
    return null;
  }
}

// ------------------------------------------------------------ alkutila

export function initialState(): AppState {
  const stored = loadState();
  const shared = scenarioFromHash(typeof location !== 'undefined' ? location.hash : '');
  let base = stored;
  if (!base) {
    const p = PRESETS[0];
    const s: Scenario = { id: newId(), name: p.name, inputs: p.make() };
    base = { scenarios: [s], activeId: s.id };
  }
  if (shared) return { scenarios: [...base.scenarios, shared], activeId: shared.id };
  return base;
}

// ------------------------------------------------------------ JSON vienti / tuonti

export function exportJson(state: AppState): string {
  return JSON.stringify(
    { app: 'digital-design-2027', version: 1, activeId: state.activeId, scenarios: state.scenarios },
    null,
    2,
  );
}

/** Palauttaa tuodut skenaariot (uusilla id:illä) tai heittää virheen. */
export function parseImport(text: string): Scenario[] {
  const j = JSON.parse(text);
  const list = Array.isArray(j?.scenarios) ? j.scenarios : j?.inputs ? [j] : null;
  if (!list) throw new Error('Tiedostosta ei löytynyt skenaarioita.');
  const out = list.map(normalizeScenario).filter(Boolean) as Scenario[];
  if (!out.length) throw new Error('Tiedostosta ei löytynyt kelvollisia skenaarioita.');
  return out;
}
