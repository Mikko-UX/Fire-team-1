import { useEffect, useMemo, useRef, useState } from 'react';
import { ChartsGrid } from './components/Charts';
import { Compare } from './components/Compare';
import { ExtraHiring, KeyFigures, KpiRow, Warnings } from './components/Insights';
import { InputsPanel } from './components/InputsPanel';
import { MonthlyTable } from './components/MonthlyTable';
import {
  exportJson, initialState, parseImport, saveState, shareUrl, type AppState, type Scenario,
} from './lib/storage';
import { additionalHiring, calculate, defaultInputs, newId, sensitivity, waterfall, type Inputs } from './model/calc';
import { PRESETS } from './model/presets';

function download(name: string, text: string, type: string) {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}

export default function App() {
  const [state, setState] = useState<AppState>(initialState);
  const [view, setView] = useState<'calc' | 'compare'>('calc');
  const [panelOpen, setPanelOpen] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const active = state.scenarios.find((s) => s.id === state.activeId) ?? state.scenarios[0];

  useEffect(() => saveState(state), [state]);
  // Jaetun linkin hash poistetaan osoiterivistä, jotta uudelleenlataus ei lisää skenaariota uudestaan.
  useEffect(() => {
    if (location.hash.startsWith('#s=')) history.replaceState(null, '', location.pathname + location.search);
  }, []);
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 3000);
    return () => clearTimeout(t);
  }, [toast]);

  const result = useMemo(() => calculate(active.inputs), [active.inputs]);
  const wf = useMemo(() => waterfall(active.inputs), [active.inputs]);
  const sens = useMemo(() => sensitivity(active.inputs), [active.inputs]);
  const extra = useMemo(() => additionalHiring(active.inputs, result), [active.inputs, result]);

  const patchScenario = (id: string, p: Partial<Scenario>) =>
    setState((st) => ({ ...st, scenarios: st.scenarios.map((s) => (s.id === id ? { ...s, ...p } : s)) }));
  const setInputs = (p: Partial<Inputs>) => patchScenario(active.id, { inputs: { ...active.inputs, ...p } });

  const addScenarios = (list: Scenario[]) =>
    setState((st) => ({ scenarios: [...st.scenarios, ...list], activeId: list[list.length - 1].id }));

  const createNew = () => addScenarios([{ id: newId(), name: `Uusi skenaario ${state.scenarios.length + 1}`, inputs: defaultInputs() }]);
  const copy = () =>
    addScenarios([{ id: newId(), name: `${active.name} (kopio)`, inputs: structuredClone(active.inputs) }]);
  const remove = () => {
    if (state.scenarios.length <= 1) return;
    if (!window.confirm(`Poistetaanko skenaario "${active.name}"?`)) return;
    setState((st) => {
      const scenarios = st.scenarios.filter((s) => s.id !== active.id);
      return { scenarios, activeId: scenarios[0].id };
    });
  };

  const share = async () => {
    const url = shareUrl(active);
    try {
      await navigator.clipboard.writeText(url);
      setToast('Jakolinkki kopioitu leikepöydälle.');
    } catch {
      window.prompt('Kopioi jakolinkki:', url);
    }
  };

  const onImport = async (file?: File) => {
    if (!file) return;
    try {
      const list = parseImport(await file.text());
      addScenarios(list);
      setToast(`Tuotu ${list.length} skenaariota.`);
    } catch (e) {
      setToast(`Tuonti epäonnistui: ${(e as Error).message}`);
    }
    if (fileRef.current) fileRef.current.value = '';
  };

  return (
    <div className="mx-auto max-w-[1700px] px-4 pb-10 pt-4">
      <header className="mb-4">
        <h1 className="text-xl font-bold sm:text-2xl">Digital Design 2027 – rekry- ja liikevaihtolaskuri</h1>
        <p className="text-sm text-muted">Muuta lähtöarvoja – tulokset ja kaaviot päivittyvät heti.</p>
      </header>

      {/* Skenaariot */}
      <section className="card mb-4 !p-3">
        <div role="tablist" aria-label="Skenaariot" className="flex flex-wrap gap-2">
          {state.scenarios.map((s) => (
            <button key={s.id} role="tab" aria-selected={s.id === active.id && view === 'calc'}
              onClick={() => { setState((st) => ({ ...st, activeId: s.id })); setView('calc'); }}
              className={`rounded-md border px-3 py-1.5 text-sm font-medium ${
                s.id === active.id && view === 'calc' ? 'border-transparent bg-accent' : 'border-line hover:bg-black/5'
              }`}
              style={s.id === active.id && view === 'calc' ? { color: 'var(--on-accent)' } : undefined}>
              {s.name}
            </button>
          ))}
          <button role="tab" aria-selected={view === 'compare'} onClick={() => setView('compare')}
            className={`rounded-md border px-3 py-1.5 text-sm font-medium ${view === 'compare' ? 'border-transparent bg-accent' : 'border-line hover:bg-black/5'}`}
            style={view === 'compare' ? { color: 'var(--on-accent)' } : undefined}>
            Vertailu
          </button>
        </div>
        <div className="mt-3 flex flex-wrap items-end gap-2">
          <label className="min-w-[10rem] flex-1 text-xs text-muted sm:max-w-xs">
            Skenaarion nimi
            <input className="inp" value={active.name} onChange={(e) => patchScenario(active.id, { name: e.target.value })} />
          </label>
          <button className="btn" onClick={createNew}>+ Uusi</button>
          <button className="btn" onClick={copy}>Kopioi</button>
          <button className="btn" onClick={remove} disabled={state.scenarios.length <= 1}>Poista</button>
          <select className="inp !w-auto" aria-label="Lisää esiasetus" value=""
            onChange={(e) => {
              const p = PRESETS.find((x) => x.id === e.target.value);
              if (p) addScenarios([{ id: newId(), name: p.name, inputs: p.make() }]);
            }}>
            <option value="">+ Esiasetus…</option>
            {PRESETS.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
          <span className="mx-1 hidden h-6 w-px bg-[var(--border)] sm:block" />
          <button className="btn" onClick={share}>Jaa linkki</button>
          <button className="btn" onClick={() => download('digital-design-2027.json', exportJson(state), 'application/json')}>Vie JSON</button>
          <button className="btn" onClick={() => fileRef.current?.click()}>Tuo JSON</button>
          <input ref={fileRef} type="file" accept="application/json,.json" className="hidden" onChange={(e) => onImport(e.target.files?.[0])} />
        </div>
        {toast && <p role="status" className="mt-2 text-sm text-accent">{toast}</p>}
      </section>

      {view === 'compare' ? (
        <Compare scenarios={state.scenarios} />
      ) : (
        <>
          <KpiRow result={result} />
          <div className="mt-4 lg:grid lg:grid-cols-[380px_minmax(0,1fr)] lg:gap-4">
            <aside>
              <button className="btn mb-3 w-full lg:hidden" aria-expanded={panelOpen} onClick={() => setPanelOpen((o) => !o)}>
                {panelOpen ? 'Piilota syötteet ▲' : 'Näytä syötteet ▼'}
              </button>
              <div className={`${panelOpen ? 'block' : 'hidden'} lg:sticky lg:top-4 lg:block lg:max-h-[calc(100vh-2rem)] lg:overflow-y-auto lg:pr-1`}>
                <InputsPanel inputs={active.inputs} set={setInputs} />
              </div>
            </aside>
            <main className="mt-4 min-w-0 space-y-4 lg:mt-0">
              <Warnings warnings={result.warnings} />
              <ChartsGrid result={result} waterfall={wf} sens={sens} />
              <div className="grid grid-cols-1 gap-4 2xl:grid-cols-2">
                <KeyFigures result={result} />
                <ExtraHiring rows={extra} shortfall={result.summary.shortfall} />
              </div>
              <MonthlyTable result={result} name={active.name} />
            </main>
          </div>
        </>
      )}
    </div>
  );
}
