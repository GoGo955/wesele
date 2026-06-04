# Dashboard — porównanie ofert weselnych (Boho Pogoria vs Przystanek Południe / Kleser)

Data: 2026-06-04
Status: do akceptacji

## Cel

Jeden samodzielny plik `dashboard.html` (CSS+JS inline, otwierany dwuklikiem,
bez serwera i bez instalacji), który pozwala **porównać dwie oferty weselne** i
**wyliczyć szacowany koszt całkowity** w zależności od liczby gości, dnia
tygodnia i wybranych pakietów/dodatków.

Styl: minimalistyczny, nowoczesny, lekki, jasny. Kluczowa funkcja: łatwe
porównanie obu sal obok siebie + kalkulator kosztu.

## Dwa różne modele kosztów (rdzeń logiki)

### Boho Pogoria — cena „all-in" za menu + dopłata za brakujące głowy
- Menu (zł/os): I = 450, II = 475, III = 510, IV = 570 (pełne menu wielodaniowe:
  powitanie, przystawka, zupa, danie główne, 2–3 kolacje, deser, zimny bufet;
  Pozycja IV = menu serwowane, jedna pozycja dla wszystkich Gości).
- Napoje (zł/os): Wersja I = 95, Wersja II = 155.
- Minimum gości wg dnia (osoby pełnopłatne): pon–czw 50, pt 70, sob 90, nd 70.
- **Dopłata za brakujących**: `max(0, min_dnia − dorośli) × 250 zł`.
- Dzieci: do lat 2 gratis; 3–10 lat = 50% (menu i napoje).
- Opcje dodatkowe:
  - Ceremonia w plenerze: 3500 zł (ryczałt).
  - Dodatkowa godzina ponad 12h: 1500 zł/h (max do 5:00).
  - Bufet dodatkowy (zł/os, min 60 os): Śródziemnomorski 65, Street Food 60, Swojski 55.
  - Nocleg: apartament Pary Młodej gratis; apartament 2-os 600 zł; domek 6-os 1200 zł; śniadanie 80 zł/os.
  - Łódź: sesja zdjęciowa 2000 zł, przypłynięcie do ślubu 2000 zł (ryczałt).
- Opłata rezerwacyjna 8000 zł — zaliczka wliczana w cenę, **nie doliczamy** do sumy.

### Kleser — modularny: obiad bazowy + dokładane bufety/kolacje + próg kwotowy
- Obiad — wybór stylu serwowania:
  - **na talerzu** (zł/os): Pakiet 1 = 240, Pakiet 2 = 290, Pakiet 3 = 330.
  - **na paterze** (zł/os): Pakiet 1 = 350 (1,5 porcji mięsa/os).
- Napoje (zł/os): Pakiet 1 = 90, Pakiet 2 = 125, Pakiet 3 = 180; albo Korkowe = 40 (alternatywa).
- **Minimum logistyczne wg dnia = próg KWOTOWY** (nie dopłata za głowy):
  | Dzień | Min osób | Próg zł |
  |---|---|---|
  | pon* / wt / śr / czw | 50 | 30 000 |
  | pt | 80 | 65 000 |
  | sob | 90 | 75 000 |
  | nd | 70 | 50 000 |
  - `total = max(policzona_suma, próg_dnia)`.
  - Gdy dorośli < min osób → widoczny alert „poniżej minimum logistycznego".
  - *poniedziałek nie podany w ofercie — przyjęto jak wt–czw (50 os / 30 000 zł), oznaczone gwiazdką.
- Dodatki, każdy liczony × osoby (zł/os):
  - Bufet na zimno (śródziemnomorski): 90.
  - Ciepła kolacja — Meksyk (bufet na ciepło): 80.
  - Live cooking (pasta / paella): 70.
  - W ogrodzie: pizza 60, burgery 65, Bliski Wschód 70.
  - Kolacja serwowana: Opcja 1 = 55, Opcja 2 = 65, Opcja 3 = 75.
  - Ciepła miska (po północy): Opcja 1 = 50, Opcja 2 = 55, Opcja 3 = 60.
  - Słodki stół: 3 sztuki = 50, 5 sztuk = 65.
- Czas trwania zależny od liczby ciepłych kolacji: bufet zimno + obiad = 5h;
  +1 kolacja = 6h; +2 = 9h; +3 = 12h. (pokazywane informacyjnie)
  - Jako „ciepła kolacja" liczą się: Ciepła kolacja Meksyk, Live cooking, każda
    pozycja „W ogrodzie", Kolacja serwowana, Ciepła miska. Liczone unikatowo,
    cap = 3 dla mapowania godzin. Bufet na zimno i słodki stół NIE liczą się
    jako ciepła kolacja.
- Dzieci: do 3 lat gratis; 4–10 lat = 50%.
- Brak noclegu i opłaty rezerwacyjnej w ofercie.

## Jednostki rozliczeniowe (oba lokale)

`billable = dorośli + 0,5 × dzieci_ze_zniżką`. Małe dzieci (gratis) nie wliczane do
kosztu, ale liczone do łącznej liczby gości pokazywanej w UI. Różnica progów wieku
(Boho: gratis <2 / 50% 3–10; Kleser: gratis <3 / 50% 4–10) oznaczona gwiazdką —
wspólne pola wejściowe „dzieci 50%" i „dzieci gratis".

## Layout

Pojedyncza strona, układ pionowy:

1. **Nagłówek** — tytuł + jednozdaniowy opis obu sal.
2. **Pasek wejścia wspólnego (sticky góra)**: liczba dorosłych (pole + suwak),
   dzieci 50%, dzieci gratis, dzień tygodnia (pon–nd).
3. **Dwie kolumny obok siebie: Boho | Kleser**. Każda kolumna:
   - własne selektory pakietu (menu/obiad, styl serwowania [Kleser], napoje, dodatki/opcje jako checkboxy + liczniki noclegu [Boho]),
   - duży **koszt całkowity** + **koszt/os**,
   - **rozbicie**: menu/obiad, napoje, dodatki, dopłaty/próg, (rezerwacja info),
   - badge czasu trwania,
   - alerty (Boho: dopłata za brakujących; Kleser: poniżej minimum / próg kwotowy aktywny).
   - Tańsza kolumna podświetlona + pasek „różnica: X zł".
4. **Tabela cech (statyczna)** pod kalkulatorem: pojemność (200 vs 150),
   lokalizacja, czas trwania, model minimum, nocleg, ceremonia, atrakcje
   wyróżniające, opłata rezerwacyjna, kontakt.

## Architektura kodu (w jednym pliku)

- `OFERTY` — obiekt-dane z całym cennikiem (osobno `boho` i `kleser`), w tym
  tabele minimów wg dnia. Jedno źródło prawdy, łatwa edycja cennika.
- `liczBoho(wejście)` → `{ rozbicie, suma, alerty, czas }`.
- `liczKleser(wejście)` → `{ rozbicie, suma, alerty, czas }`.
- `render()` — czyta stan z kontrolek, woła obie funkcje, rysuje obie kolumny,
  liczy różnicę, podświetla tańszą. Wołane na każdy `input`/`change`.
- Brak zależności zewnętrznych, brak build-stepu. Waniliowy JS + CSS.

## Poza zakresem (YAGNI)

- Brak zapisu/eksportu, brak backendu, brak wielu walut, brak logowania.
- Brak pełnych list dań w kalkulatorze (dania są w plikach .md w `parsed/`); w
  dashboardzie tylko nazwy pakietów + ceny.

## Założenia do potwierdzenia

1. Poniedziałek Kleser = jak wt–czw (50 os / 30 000 zł), oznaczony gwiazdką. ✔ (potwierdzone)
2. Minimum Boho liczone względem liczby dorosłych (pełnopłatnych).
3. Dzieci 50% obejmują też napoje (zgodnie z zapisem Boho).
4. Kleser: korkowe 40 zł/os jest alternatywą dla pakietu napojów (przynosisz alkohol).
