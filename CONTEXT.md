# CONTEXT — architektura i model danych

Dokument dla osób rozwijających `index.html`. Opis domeny: porównanie dwóch sal weselnych + szacunek całkowitego budżetu.

## Architektura

- **Jeden plik** `index.html`: HTML + CSS (`<style>`) + JS (`<script>`) inline. Zero zależności runtime, zero buildu, zero fetchy — wszystkie dane są zaszyte w JS. Dzięki temu działa po dwukliku i na GitHub Pages bez konfiguracji.
- Render: dane → funkcje budujące `innerHTML` sekcji (`#panel`, `#cols`, `#szczegolySek`, `#cechy`, `#reszta`, `#scenariusze`). Każda zmiana inputu w kalkulatorze wywołuje `render()`, a widok scenariuszy (`#scenariusze`) wywołuje `renderScenariusze()`.

## Model danych (stałe w `<script>`)

- `OFERTY` — ceny i parametry sal.
- `boho`: stawki bazowe z oferty 2027; menu i napoje w 2028 są podwyższone o 9% i zaokrąglone do pełnych złotych. Model minimum = min. gości/dzień + dopłata 250 zł/brakującą osobę.
  - `kleser` (Przystanek Południe): wszystkie ceny zł/os jako tablica **`[2026, 2027, 2028]`**. Próg minimalnego budżetu `minBudget[sezon][dzień][rok]` (sezon `hi`=VI–IX, `lo`=X–V; źródło: mail). `minOs` = min. gości/dzień (rok-niezależne). `laFlor` = pakiety dekoracji (cena/stolik + stół PM) + `laFlorDojazd`.
  - Manualna korekta PP: `dodatki.cieplaMiska` ma w 2028 roku +5 zł/os względem 2027 (`50/55/60` → `55/60/65`). Źródło: weryfikacja Kajetana na miejscu w najnowszej karcie; nie pochodzi z parsowanego PDF/markdown.
- `OPISY` — zawartość pakietów (teksty do panelu szczegółów), w tym `OPISY.kleser.laFlor`.
- `RESZTA` — 23 kategorie kosztów poza salą (foto, wideo…), każda `b=[min,max]` budżet, `p=[min,max]` premium, `opt:true` = domyślnie odznaczone. Źródło: `reports/koszty-wesela-slask-2027.md`.

## Model liczenia

- `liczBoho(w)` → `{rozbicie, suma, alerty, czas}`. Suma = menu+napoje+opcje; jeśli < min gości → dopłata.
- `liczKleser(w)` → jw. Kroki: catering per rok (`[yr]`) → `computed`; **próg**: `suma = max(computed, minBudget)`; **La Flor** doliczane *poza progiem* (`suma += dekor`, `dekor = liczLaFlor(pkg, stoliki)`, `stoliki = ceil(ciała / os_na_stolik)`); czas = f(liczba ciepłych kolacji).
- `liczReszta()` → `{min,max}` = suma zaznaczonych kategorii dla wybranego wariantu (budżet/premium), wspólna dla obu sal (koszt niezależny od wyboru sali).
- `scenariuszeDane(dorosli)` → stałe warianty lipcowe do szybkiego porównania: PP niedziela 2027, PP czwartek/niedziela 2028 (kwotowo bez różnicy przy przekroczonym progu), bezalkoholowe+korkowe oraz alkoholowe; Boho czwartek 2028 bezalkoholowe i alkoholowe. `renderScenariusze()` pokazuje je jako dwie macierze: główne porównanie kosztów oraz osobną tabelę szczegółów jedzenia i napojów, z grupowym nagłówkiem PP/Boho. W Boho scenariusze doliczają słodki stół jako ryczałt 3500 zł.
- **Grand total** per sala = `suma` (punkt) + reszta (zakres) → linia „+ reszta wesela → razem X–Y zł" na karcie.

## Niezmienniki / testy

- Self-testy w `runSelfTests()` (uruchamiane przy `#test`): **56 testów** — sumy Boho/Kleser, scenariusze lipcowe, ceny per-rok, patera, La Flor, próg, reszta, pokrycie opisów. Po zmianie cen/logiki **uruchom `index.html#test`** i utrzymaj zielone (zaktualizuj oczekiwane liczby przy zmianie danych).

## Jak rozszerzać

- Nowa pozycja menu PP → dodaj cenę jako `[2026,2027,2028]` w `OFERTY.kleser` + opis w `OPISY.kleser` + obsługę w `liczKleser`/`szczegolyKleser` + (jeśli wybieralna) kontrolkę w `selKleser`/`odczytKleser`.
- Zmiana kosztów pozabankietowych → edytuj `RESZTA` i zaktualizuj self-test E (sumy 32 700–53 050 budżet).
- Boho per-rok: ceny bazowe 2027; dla 2028 menu i napoje są liczone z podwyżką 9%, zaokrągloną do pełnych złotych. Pozostałe stawki pozostają bazowe.

## Stan po merge tej zmiany (2026-07-15)

Zrobione: dashboard porównania Boho/PP, ceny Boho 2028 skorygowane do +9%, scenariusze lipcowe w osobnym widoku `#scenariusze`, słodki stół Boho 3500 zł, manualna korekta ciepłej miski PP 2028 +5 zł/os, grupowane tabele scenariuszy (główne porównanie + szczegóły), dokumentacja README/CONTEXT zaktualizowana. Remote GitHub skonfigurowany jako `origin`.
