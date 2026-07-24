# CONTEXT — architektura i model danych

Dokument dla osób rozwijających `index.html`. Opis domeny: porównanie dwóch sal weselnych + szacunek całkowitego budżetu.

## Architektura

- **Jeden plik** `index.html`: HTML + CSS (`<style>`) + JS (`<script>`) inline. Zero zależności runtime, zero buildu, zero fetchy — wszystkie dane są zaszyte w JS. Dzięki temu działa po dwukliku i na GitHub Pages bez konfiguracji.
- Render: dane → funkcje budujące `innerHTML` sekcji (`#panel`, `#cols`, `#rachunek`, `#szczegolySek`, `#cechy`, `#reszta`, `#scenariusze`). Każda zmiana inputu w kalkulatorze wywołuje `render()`, a widok scenariuszy (`#scenariusze`) wywołuje `renderScenariusze()`.
- `#rachunek` — zbiorczy rachunek fokusowany na Przystanek Południe (`renderRachunek(ok, wk, R, os)`): itemizowana *Sala i catering* (kwoty punktowe z `wk.rozbicie`) + *Pozostałe koszty* (zakres wg per-pozycja wariantu, `resztaRozbicie()`, z badge budżet/premium) → **RAZEM** jako zakres (punkt sali + zakres reszty), żywo. Pozycje La Flor są zwijane w jeden blok „Dekoracje La Flor" z żywą podsumą przez `rozbicieHTML()` (grupuje `rozbicie` po `g:"laflor"`); ta sama funkcja renderuje rozbicie na kartach porównania.
- **Foldable** (`<details class="fold">` + `<summary>` z chevronem, stała `CHEVRON`): `#rachunek` (domyślnie otwarty; shell budowany raz w init, `renderRachunek` wypełnia `#rachunek-body` i podsumę `#rachunek-suma` widoczną też po zwinięciu), „Szczegóły wybranych pakietów" w `#szczegolySek` (domyślnie zwinięte; `renderSzczegoly` zawsze wypełnia `#szczBox`, widocznością steruje natywny `<details>` — brak już `pokazSzczegoly`/przycisku) oraz „Porównanie cech" w `#cechy` (domyślnie zwinięte).

## Model danych (stałe w `<script>`)

- `OFERTY` — ceny i parametry sal.
- `boho`: stawki bazowe z oferty 2027; menu i napoje w 2028 są podwyższone o 9% i zaokrąglone do pełnych złotych. Model minimum = min. gości/dzień + dopłata 250 zł/brakującą osobę.
  - `kleser` (Przystanek Południe): wszystkie ceny zł/os jako tablica **`[2026, 2027, 2028]`**. Próg minimalnego budżetu `minBudget[sezon][dzień][rok]` (sezon `hi`=VI–IX, `lo`=X–V; źródło: mail). `minOs` = min. gości/dzień (rok-niezależne). `laFlor` = pakiety dekoracji (cena/stolik + stół PM), w tym `WYCENA2027` (konkretna wycena La Flor 11.07.2027: 280 zł/stolik + 800 zł stół PM; źródło `parsed/Przystanek-Poludnie-La-Flor-wycena-11.07.2027.md`) + `laFlorDojazd`. `laFlorOpcje` = duże pozycje opcjonalne z wyceny (fairy lights, podwieszenia boki/cała/nad PM, ogród, pakiet osobisty — ryczałty; podtalerze kryształ/rattan — per os.), doliczane osobnymi liniami gdy wybrany dowolny pakiet.
  - Manualna korekta PP: `dodatki.cieplaMiska` ma w 2028 roku +5 zł/os względem 2027 (`50/55/60` → `55/60/65`). Źródło: weryfikacja Kajetana na miejscu w najnowszej karcie; nie pochodzi z parsowanego PDF/markdown.
- `OPISY` — zawartość pakietów (teksty do panelu szczegółów), w tym `OPISY.kleser.laFlor`.
- `RESZTA` — 23 kategorie kosztów poza salą (foto, wideo…), każda `b=[min,max]` budżet, `p=[min,max]` premium, `opt:true` = domyślnie wyłączone. Źródło: `reports/koszty-wesela-slask-2027.md`.
- `resztaStan` / `resztaOwn` — stan per-pozycja: `resztaStan[k] ∈ 'off'|'b'|'p'|'own'` (init: `opt` → `'off'`, reszta → `'b'`); `resztaOwn[k]` = własna kwota (init: `c.b[0]`). Warianty budżet/premium/własna można **dowolnie mieszać między pozycjami** (nie ma globalnego przełącznika). Przy `'own'` pozycja liczona jako punkt (min=max=`resztaOwn[k]`). UI: segmentowy przełącznik wył·budżet·premium·własna na wiersz (przy „własna" pojawia się pole liczbowe `#rkin_<k>`) + „Ustaw wszystkim" (delegacja `click` i `input` na `#reszta`).

## Model liczenia

- `liczBoho(w)` → `{rozbicie, suma, alerty, czas}`. Suma = menu+napoje+opcje; jeśli < min gości → dopłata.
- `liczKleser(w)` → jw. Kroki: catering per rok (`[yr]`) → `computed`; **próg**: `suma = max(computed, minBudget)`; **La Flor** doliczane *poza progiem* (`suma += baza`, `baza = liczLaFlor(pkg, stoliki)`, `stoliki = ceil(ciała / os_na_stolik)`); opcje z `laFlorOpcje` doliczane osobnymi liniami na wierzch bazy (podtalerze × ciała); czas = f(liczba ciepłych kolacji).
- `liczReszta()` → `{min,max}` = suma włączonych kategorii, każda wg `resztaStan[k]` (budżet/premium/własna per-pozycja; `'own'` → punkt `resztaOwn[k]`), wspólna dla obu sal (koszt niezależny od wyboru sali). `resztaRozbicie()` → lista włączonych pozycji z `tier` (`'b'|'p'|'own'`, do rachunku — badge budżet/premium/własna).
- `scenariuszeDane(dorosli)` → stałe warianty lipcowe do szybkiego porównania: PP niedziela 2027, PP czwartek/niedziela 2028 (kwotowo bez różnicy przy przekroczonym progu), bezalkoholowe+korkowe oraz alkoholowe; Boho czwartek 2028 bezalkoholowe i alkoholowe. `renderScenariusze()` pokazuje je jako dwie macierze: główne porównanie kosztów oraz osobną tabelę szczegółów jedzenia i napojów, z grupowym nagłówkiem PP/Boho. W Boho scenariusze doliczają słodki stół jako ryczałt 3500 zł.
- **Grand total** per sala = `suma` (punkt) + reszta (zakres) → linia „+ reszta wesela → razem X–Y zł" na karcie.

## Niezmienniki / testy

- Self-testy w `runSelfTests()` (uruchamiane przy `#test`): **68 testów** — sumy Boho/Kleser, scenariusze lipcowe, ceny per-rok, patera, La Flor (w tym wycena 2027: baza 3190 zł + delta opcji 3765 zł + podsuma grupy „laflor" 6675 zł), próg, reszta (budżet 32 700–53 050 + mieszany wariant + własna kwota per-pozycja), pokrycie opisów (w tym każdy wariant La Flor). Po zmianie cen/logiki **uruchom `index.html#test`** i utrzymaj zielone (zaktualizuj oczekiwane liczby przy zmianie danych).

## Jak rozszerzać

- Nowa pozycja menu PP → dodaj cenę jako `[2026,2027,2028]` w `OFERTY.kleser` + opis w `OPISY.kleser` + obsługę w `liczKleser`/`szczegolyKleser` + (jeśli wybieralna) kontrolkę w `selKleser`/`odczytKleser`.
- Zmiana kosztów pozabankietowych → edytuj `RESZTA` i zaktualizuj self-test E (sumy 32 700–53 050 budżet) oraz E2 (delta premium−budżet dla `foto`, jeśli zmienisz jego stawki).
- Boho per-rok: ceny bazowe 2027; dla 2028 menu i napoje są liczone z podwyżką 9%, zaokrągloną do pełnych złotych. Pozostałe stawki pozostają bazowe.

## Stan po zmianie (2026-07-24)

Wcielono konkretną wycenę La Flor 11.07.2027 (PP, ~70 gości, kolory pudrowe) — nie jako kolejny cennik, lecz jako realnie wynegocjowany wariant. Dodane: pakiet `WYCENA2027` (280/800) w dropdownie La Flor, `laFlorOpcje` (fairy lights 600, podwieszenia boki 750/cała 1200/nad PM 400, ogród 450, pakiet osobisty 345, podtalerze kryształ 11 / rattan 4 zł/os) jako przełączniki UI doliczane osobnymi liniami w grand total, opis `OPISY.kleser.laFlor.WYCENA2027`, dok. `parsed/Przystanek-Poludnie-La-Flor-wycena-11.07.2027.md`, 4 nowe self-testy (56→63). Baza dla 8 stołów ≈ 3190 zł, z pełnymi opcjami do ~6500 zł.

Dodano też czytelniejsze podsumowanie: pozycje La Flor zwijane w blok „Dekoracje La Flor" z żywą podsumą (`rozbicieHTML()`, tag `g:"laflor"`) — na kartach i w nowym panelu `#rachunek` (zbiorczy rachunek PP: sala+catering kwotami + pozostałe koszty zakresem → RAZEM zakresem, żywo). Fokus na PP (boho zostaje w porównaniu). +1 self-test (63→64).

## Stan po merge tej zmiany (2026-07-15)

Zrobione: dashboard porównania Boho/PP, ceny Boho 2028 skorygowane do +9%, scenariusze lipcowe w osobnym widoku `#scenariusze`, słodki stół Boho 3500 zł, manualna korekta ciepłej miski PP 2028 +5 zł/os, grupowane tabele scenariuszy (główne porównanie + szczegóły), dokumentacja README/CONTEXT zaktualizowana. Remote GitHub skonfigurowany jako `origin`.
