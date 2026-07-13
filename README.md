# Porównanie ofert weselnych — Boho Pogoria vs Przystanek Południe

Interaktywny kalkulator porównujący dwie sale weselne i szacujący całkowity koszt wesela.
Jeden samodzielny plik `index.html` (HTML + CSS + JS inline, **zero zależności**, **zero buildu**) — działa po dwukliku i po wystawieniu na GitHub Pages.

## Co liczy

- **Koszt sala + catering** dla obu sal na żywo wg: liczby gości, dnia tygodnia, **roku (2026/2027/2028)** i **sezonu** (PP), wybranych pakietów menu, napojów, bufetów i ciepłych kolacji.
- **Przystanek Południe**: ceny per rok, próg minimalnego budżetu (rok × sezon × dzień), dekoracje **La Flor** (BASIC/STANDARD/PREMIUM, liczone wg liczby stolików).
- **Boho Pogoria**: menu I–IV, model minimum gości/dzień; stawki bazowe z oferty 2027, a menu i napoje na 2028 podwyższone o 15% i zaokrąglone do pełnych złotych.
- **Pozostałe koszty wesela** (poza salą): foto, wideo, muzyka, suknia, atrakcje… jako zakres budżet ↔ premium → **całkowity budżet** per sala.
- Panel szczegółów zawartości pakietów + tabela porównania cech.

## Struktura repo

```
index.html        ← aplikacja (cała: struktura, dane, logika, self-testy)
parsed/           ← oferty i cenniki w markdown (źródło danych dla index.html)
converted/        ← surowe konwersje PDF→md (robocze)
raw/              ← oryginalne PDF-y ofert (źródła)
reports/          ← raport kosztów wesela (Śląsk 2027)
scripts/          ← narzędzia (pdf_to_png.py — render PDF do PNG)
docs/             ← spec + plan (dziennik budowy)
CONTEXT.md        ← architektura i model danych (dla rozwijających)
```

## Uruchomienie lokalne

Otwórz `index.html` w przeglądarce (dwuklik).

**Self-testy silnika cenowego:** otwórz `index.html#test` i sprawdź konsolę (F12) — oczekiwane „SELF-TEST: WSZYSTKIE OK" (44 testy).

Headless (Node + jsdom):
```
npm i jsdom
node -e "const{JSDOM}=require('jsdom');new JSDOM(require('fs').readFileSync('index.html','utf8'),{runScripts:'dangerously',url:'http://x/#test'})"
```

## Publikacja na GitHub Pages

1. Utwórz repozytorium na GitHub, dodaj remote i wypchnij gałąź `main`:
   ```
   git remote add origin https://github.com/<user>/<repo>.git
   git push -u origin main
   ```
2. **Settings → Pages → Source:** gałąź `main`, katalog `/ (root)`.
3. Strona: `https://<user>.github.io/<repo>/` (serwuje `index.html`).

Plik `.nojekyll` wyłącza przetwarzanie Jekyll — pliki serwowane są jako statyczne.

## Źródła danych

Ceny pochodzą z ofert sal (PDF w `raw/`, sparsowane do `parsed/`) oraz oferty mailowej PP (min. budżety 2026/2027/2028). Pozostałe koszty: `reports/koszty-wesela-slask-2027.md`. **Wszystkie ceny orientacyjne — do potwierdzenia w salach.**
