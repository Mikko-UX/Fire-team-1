/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  darkMode: 'media',
  theme: {
    extend: {
      colors: {
        bg: 'var(--bg)',
        card: 'var(--card)',
        fg: 'var(--fg)',
        muted: 'var(--muted)',
        line: 'var(--border)',
        accent: 'var(--accent)',
        ai: 'var(--ai)',
        other: 'var(--other)',
        target: 'var(--target)',
        pos: 'var(--pos)',
        neg: 'var(--neg)',
        warn: 'var(--warn)',
      },
    },
  },
  plugins: [],
};
