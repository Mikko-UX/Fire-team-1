import { useState } from 'react';
import { fmtNum } from '../lib/format';

const toText = (v: number) => String(Math.round(v * 1e6) / 1e6).replace('.', ',');
const parse = (t: string) => parseFloat(t.replace(/\s/g, '').replace(',', '.'));

interface Props {
  label: string;
  unit?: string;
  value: number;
  onChange: (v: number) => void;
  def: number;
  min?: number;
  sliderMin: number;
  sliderMax: number;
  step?: number;
  tip: string;
  disabled?: boolean;
  decimals?: number;
}

export function NumField({
  label, unit, value, onChange, def, min = 0, sliderMin, sliderMax, step = 1, tip, disabled, decimals = 0,
}: Props) {
  const [draft, setDraft] = useState<string | null>(null);
  const [warn, setWarn] = useState(false);
  const [tipOpen, setTipOpen] = useState(false);
  const sliderValue = Math.min(sliderMax, Math.max(sliderMin, value));
  const changed = Math.abs(value - def) > 1e-9;

  return (
    <div className={`py-2 ${disabled ? 'opacity-50' : ''}`}>
      <div className="mb-1 flex items-center justify-between gap-2">
        <label className="flex items-center gap-1 text-sm font-medium">
          {label}
          <button
            type="button"
            title={tip}
            aria-label={`Ohje: ${label}`}
            aria-expanded={tipOpen}
            onClick={() => setTipOpen((o) => !o)}
            className="flex h-4 w-4 items-center justify-center rounded-full border border-line text-[10px] text-muted hover:text-fg"
          >
            ?
          </button>
        </label>
        <div className="flex items-center gap-2 text-xs text-muted">
          <span>{fmtNum(value, decimals)} {unit}</span>
          <button
            type="button"
            className="rounded border border-line px-1.5 py-0.5 hover:bg-black/5 disabled:opacity-30"
            title={`Palauta oletus (${fmtNum(def, decimals)} ${unit ?? ''})`}
            aria-label={`Palauta oletus: ${label}`}
            disabled={!changed || disabled}
            onClick={() => { setDraft(null); setWarn(false); onChange(def); }}
          >
            ↺
          </button>
        </div>
      </div>
      {tipOpen && <p className="mb-1 text-xs text-muted">{tip}</p>}
      <div className="flex items-center gap-3">
        <input
          type="range"
          aria-label={`${label} (liukusäädin)`}
          min={sliderMin}
          max={sliderMax}
          step={step}
          value={sliderValue}
          disabled={disabled}
          onChange={(e) => { setDraft(null); setWarn(false); onChange(Number(e.target.value)); }}
        />
        <input
          className="inp w-28 text-right"
          inputMode="decimal"
          aria-label={`${label} (numero)`}
          value={draft ?? toText(value)}
          disabled={disabled}
          onChange={(e) => {
            const t = e.target.value;
            setDraft(t);
            const v = parse(t);
            if (Number.isNaN(v)) return;
            if (v < min) { setWarn(true); onChange(min); } else { setWarn(false); onChange(v); }
          }}
          onBlur={() => { setDraft(null); setWarn(false); }}
        />
      </div>
      {warn && <p className="mt-1 text-xs text-neg">Negatiivisia arvoja ei sallita (min {fmtNum(min, decimals)}).</p>}
    </div>
  );
}

/** Pieni numerokenttä kuukausiruudukkoon. Tyhjä = null (jos allowNull). */
export function MiniNum({
  value, onChange, placeholder, label, allowNull,
}: {
  value: number | null;
  onChange: (v: number | null) => void;
  placeholder?: string;
  label: string;
  allowNull?: boolean;
}) {
  const [draft, setDraft] = useState<string | null>(null);
  return (
    <input
      className="inp px-1 text-center"
      inputMode="decimal"
      aria-label={label}
      placeholder={placeholder}
      value={draft ?? (value === null ? '' : toText(value))}
      onChange={(e) => {
        const t = e.target.value;
        setDraft(t);
        if (t.trim() === '') { if (allowNull) onChange(null); return; }
        const v = parse(t);
        if (!Number.isNaN(v)) onChange(Math.max(0, v));
      }}
      onBlur={() => setDraft(null)}
    />
  );
}
