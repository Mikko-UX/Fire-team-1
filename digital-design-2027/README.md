# Digital Design 2027 – rekry- ja liikevaihtolaskuri

Web-sovellus, jolla mallinnetaan vuoden 2027 liikevaihto, FTE-määrä ja rekrytarve kuukausitasolla ja verrataan tulosta vuositavoitteeseen. Kaikkia lähtöarvoja voi muuttaa, ja tulokset ja kaaviot päivittyvät heti. Käyttöliittymä on suomeksi.

Tekniikka: Vite + React + TypeScript, Tailwind, Recharts, Vitest. Ei backendia.

## Käynnistys

```bash
npm install
npm run dev        # kehityspalvelin, http://localhost:5173
npm run build      # tyyppitarkistus + tuotantobuild (dist/)
npm run preview    # esikatsele buildia
```

## Testit

```bash
npm test           # Vitest: kaikki yksikkötestit
npm run typecheck  # tsc --noEmit
```

Testit (`src/model/calc.test.ts`) kattavat hyväksymiskriteerit 1–6 ±1 € tarkkuudella (mm. oletusarvoilla 8 647 392 €) sekä mallin muut osat. `src/lib/storage.test.ts` kattaa JSON-viennin ja -tuonnin.

## Rakenne

- `src/model/calc.ts` – puhdas laskentamoduuli ilman UI-riippuvuuksia (`calculate`, `additionalHiring`, `waterfall`, `sensitivity`, `sanitize`)
- `src/model/presets.ts` – valmiit skenaariot
- `src/lib/storage.ts` – localStorage (try/catch), URL-hash-jako, JSON-vienti ja -tuonti
- `src/components/` – syötteet, kaaviot, taulukot, vertailu

## Skenaariot ja tallennus

- Skenaariot tallentuvat localStorageen. Jos se ei ole käytössä, sovellus toimii silti, mutta tila ei säily.
- **Jaa linkki** kopioi osoitteen, jonka `#s=`-hashissa on nykyinen skenaario. Linkin avaaminen lisää sen uutena skenaariona.
- **Vie JSON / Tuo JSON** siirtää kaikki skenaariot tiedostona. Tuonti lisää skenaariot nykyisten perään.
- **Vertailu** näyttää 2–4 skenaariota rinnakkain ja niiden kumulatiivisen liikevaihdon yhdessä kaaviossa.

## Laskentamalli

Kuukaudelle `m = 1..12`:

```
laskutettavia tunteja per FTE_m = tuntia_per_vuosi / 12 × painokerroin_m × utilisaatio_m
painokerroin_m = 12 × paino_m / Σ paino   (1, jos työpäiväpainot eivät ole käytössä)

FTE_m     = lähtö_FTE + Σ rekryt (aloitus ≤ m) − poistuma_kertynyt_m + korvaukset_kertyneet_m
AI_FTE_m  = lähtö_AI + Σ AI-rekryt (aloitus ≤ m) + konversiot_kertyneet_m
Muu_FTE_m = FTE_m − AI_FTE_m
liikevaihto_m = (AI_FTE_m × hinta_AI + Muu_FTE_m × hinta_muu) × laskutettavia tunteja per FTE_m
```

- `poistuma_kertynyt_m = poistuma × m / 12`. Korvaus (jos valittu): `poistuma × (m − 1) / 12`, eli yhden kuukauden viiveellä.
- `konversiot_kertyneet_m = konversio_per_kk × (kuukausia ensimmäisestä konversiokuukaudesta m:ään, enintään viimeiseen kuukauteen)`. Kuukausi, jona konversio alkaa, lasketaan mukaan. Konversio siirtää FTE:n muusta designista AI-designiin eikä lisää FTE:itä. Konversiot rajataan niin, ettei AI-FTE ylitä kokonais-FTE:tä.
- **Rekryrivin oma €/h** korvaa tyypin hinnan vain kyseisen rivin FTE:iden osalta. Rivi lasketaan erillisenä liikevaihtoeränä (`FTE × oma hinta × tunnit`), ja muu osa lasketaan tyypin hinnalla.
- **Tuottavuuden nousu:** rekryn tuottavuuskerroin kuukautena `k` aloituksesta (0 = ensimmäinen kuukausi) on `alku + (1 − alku) × min(1, k / nousuaika)`. Se vaikuttaa vain liikevaihtoon, ei HC:hen.
- **Kuukausitavoite** = vuositavoite × jako. Jako on tasan (1/12), kapasiteetin mukaan (`FTE_m × tunnit_m`) tai omien painojen mukaan.
- **Rekrytarve:** `tarvittu_FTE_m = kuukausitavoite_m / (sekahinta_m × laskutettavia tunteja_m)` ja `rekrytarve_m = max(0, tarvittu_FTE_m − FTE_m)`.
- **Lisärekrytarve:** `tarve = vaje / (tunnit_ka × hinta × (13 − aloituskuukausi))`, jossa `tunnit_ka` on laskutettavien tuntien keskiarvo per FTE ja kuukausi. Taulukko näytetään, kun toteuma jää tavoitteesta.
- **Vipuportaikko:** (a) lähtöhenkilöstö ilman muutoksia, (b) + utilisaatio, (c) + konversiot, (d) + rekryrivit yksi kerrallaan.
- **Herkkyys:** jokaista syötettä muutetaan ±10 %, ja vaikutus vuoden liikevaihtoon lajitellaan suurimmasta pienimpään.
- **Katetarkistus:** `max. kustannus/h = (1 − kate-tavoite) × sekahinta × utilisaatio` ja `max. keskipalkka = max. kustannus/h × tuntia_per_vuosi / (palkkakuukaudet × (1 + sivukulut))`.

## Oletukset (epäselvät kohdat)

- **Nimitys FTE / HC:** HC on kokonaishenkilöstö. Tuottavuuden nousu ei vähennä HC:tä, vain tuotetun liikevaihdon FTE-painoa.
- **Sekahinta** lasketaan `liikevaihto / (HC × tunnit)`. Ilman tuottavuuden nousua ja rekryrivien omia hintoja tämä on sama kuin `(AI × hinta_AI + Muu × hinta_muu) / FTE`.
- **Poistuma ja korvaukset** koskevat muuta designia: lähtijät vähennetään Muu FTE:stä ja korvaajat lisätään sinne. Korvaajat ovat heti täysin tuottavia.
- **Työpäiväpainot** ovat suhteellisia lukuja (oletus 1 kullekin kuukaudelle) ja skaalataan summaan 12. Oletus vastaa tasajakoa 1/12.
- **Kertynyt vaje** (rekrytarvekaavio) on suurin kuukausittainen FTE-vaje tähän kuukauteen mennessä. FTE-vajeiden summaaminen ei ole mielekästä, koska vaje on varanto eikä virta.
- **Vipuportaikon lähtötaso** on taso, jolla lähtöhenkilöstö tuottaa vuoden 2026 liikevaihdon (kalibroitu utilisaatio). "+ Utilisaatio" -askel on ero tähän nähden. Poistuma näytetään omana askeleenaan vain, jos se on > 0.
- **Esiasetusten "Q1" ja "Q3"** tulkittiin kvartaalin ensimmäiseksi kuukaudeksi (tammikuu ja heinäkuu). Muiden kuin kuvattujen kenttien arvot tulevat oletusarvoista.
- **Katetarkistuksen merkki:** vihreä, kun palkka ≤ 95 % maksimista, keltainen kun ≤ 100 %, punainen kun ylittää.
- **Validointi:** negatiiviset arvot katkaistaan nollaan (kenttä näyttää huomautuksen). Jos AI-FTE ylittäisi FTE:t, se rajataan FTE-määrään ja näytetään varoitus. Sovellus ei kaadu.
- **Skenaariot:** sovellus alkaa yhdellä skenaariolla ("Suositus"). Muut esiasetukset lisätään valikosta "+ Esiasetus…".
