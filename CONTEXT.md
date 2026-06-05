# CONTEXT — architektura i model danych

Dokument dla osób rozwijających `index.html`. Opis domeny: porównanie dwóch sal weselnych + szacunek całkowitego budżetu.

## Architektura

- **Jeden plik** `index.html`: HTML + CSS (`<style>`) + JS (`<script>`) inline. Zero zależności runtime, zero buildu, zero fetchy — wszystkie dane są zaszyte w JS. Dzięki temu działa po dwukliku i na GitHub Pages bez konfiguracji.
- Render: dane → funkcje budujące `innerHTML` sekcji (`#panel`, `#cols`, `#szczegolySek`, `#cechy`, `#reszta`). Każda zmiana inputu wywołuje `render()`.

## Model danych (stałe w `<script>`)

- `OFERTY` — ceny i parametry sal.
  - `boho`: ceny **stałe** (oferta 2027). Model minimum = min. gości/dzień + dopłata 250 zł/brakującą osobę.
  - `kleser` (Przystanek Południe): wszystkie ceny zł/os jako tablica **`[2026, 2027, 2028]`**. Próg minimalnego budżetu `minBudget[sezon][dzień][rok]` (sezon `hi`=VI–IX, `lo`=X–V; źródło: mail). `minOs` = min. gości/dzień (rok-niezależne). `laFlor` = pakiety dekoracji (cena/stolik + stół PM) + `laFlorDojazd`.
- `OPISY` — zawartość pakietów (teksty do panelu szczegółów), w tym `OPISY.kleser.laFlor`.
- `RESZTA` — 23 kategorie kosztów poza salą (foto, wideo…), każda `b=[min,max]` budżet, `p=[min,max]` premium, `opt:true` = domyślnie odznaczone. Źródło: `reports/koszty-wesela-slask-2027.md`.

## Model liczenia

- `liczBoho(w)` → `{rozbicie, suma, alerty, czas}`. Suma = menu+napoje+opcje; jeśli < min gości → dopłata.
- `liczKleser(w)` → jw. Kroki: catering per rok (`[yr]`) → `computed`; **próg**: `suma = max(computed, minBudget)`; **La Flor** doliczane *poza progiem* (`suma += dekor`, `dekor = liczLaFlor(pkg, stoliki)`, `stoliki = ceil(ciała / os_na_stolik)`); czas = f(liczba ciepłych kolacji).
- `liczReszta()` → `{min,max}` = suma zaznaczonych kategorii dla wybranego wariantu (budżet/premium), wspólna dla obu sal (koszt niezależny od wyboru sali).
- **Grand total** per sala = `suma` (punkt) + reszta (zakres) → linia „+ reszta wesela → razem X–Y zł" na karcie.

## Niezmienniki / testy

- Self-testy w `runSelfTests()` (uruchamiane przy `#test`): **44 testy** — sumy Boho/Kleser, ceny per-rok, patera, La Flor, próg, reszta, pokrycie opisów. Po zmianie cen/logiki **uruchom `index.html#test`** i utrzymaj zielone (zaktualizuj oczekiwane liczby przy zmianie danych).

## Jak rozszerzać

- Nowa pozycja menu PP → dodaj cenę jako `[2026,2027,2028]` w `OFERTY.kleser` + opis w `OPISY.kleser` + obsługę w `liczKleser`/`szczegolyKleser` + (jeśli wybieralna) kontrolkę w `selKleser`/`odczytKleser`.
- Zmiana kosztów pozabankietowych → edytuj `RESZTA` i zaktualizuj self-test E (sumy 32 700–53 050 budżet).
- Boho per-rok: obecnie brak danych innych lat — ceny stałe 2027 (zaznaczone w UI i stopce).

## Stan (2026-06-05)

Zrobione: parse ofert PP (catering + cennik La Flor) do `parsed/`; dashboard z cenami PP per-rok 2026/2027/2028 + sezon, próg min. budżetu z maila, patera 250/290/330, picker La Flor, warstwa „Pozostałe koszty wesela" (pod porównaniem cech). Gotowe pod GitHub Pages (`index.html` + `.nojekyll`). Brak skonfigurowanego remote. Pliki niezacommitowane.
