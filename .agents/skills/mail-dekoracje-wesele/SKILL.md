---
name: mail-dekoracje-wesele
description: Generates Polish wedding decoration inquiry emails from conversation context and selects the correct inspiration attachments from raw/dekoracje while excluding venue-specific images. Use when the user wants to prepare or fill a decoration quote email, adapt it for another venue or date, or include decor inspiration photos as attachments.
---

# Mail Dekoracje Wesele

## Quick start

1. Z rozmowy wyciagnij:
   - odbiorce / nazwe firmy
   - nazwe sali lub obiektu
   - termin
   - liczbe gosci
   - opis wizji dekoracji
   - pytania dodatkowe do uslugodawcy
2. Otworz [TEMPLATE.md](TEMPLATE.md) i uzupelnij placeholdery.
3. Uruchom `.\.agents\skills\mail-dekoracje-wesele\scripts\list_attachments.ps1` z katalogu glownego repo.
4. Zwroc:
   - gotowy mail albo generyczny template
   - liste zalacznikow
   - liste brakujacych pol, jesli uzytkownik nie podal wszystkich danych

## Rules

- Domyslnie pisz po polsku.
- Mail pisz w formie zenskiej.
- Traktuj nazwe sali, termin, liczbe gosci i odbiorce jako pola zmienne.
- Jesli uzytkownik chce template generyczny, zostaw placeholdery w nawiasach kwadratowych.
- Jesli uzytkownik chce gotowa wersje, uzupelnij tylko dane wynikajace z rozmowy; brakujacych nie zgaduj.
- Zawsze wspomnij w mailu, ze zdjecia inspiracyjne sa w zalaczniku.
- Zawsze dolacz wszystkie pliki z `raw/dekoracje`, z jednym wyjatkiem: `raw/dekoracje/przystanek_poludnie.jpg` ma byc pominiety, bo dotyczy wylacznie Przystanku Poludnie.
- Nie wspominaj o pominietym pliku w tresci maila, chyba ze uzytkownik pyta o szczegoly doboru zalacznikow.
- Zachowaj ten sam sens wizji: swiece, male wazoniki z kwiatami sezonowymi w rozach i bezach, dwa warianty ukladu stolow, spojny stol pary mlodej, pytanie o serwetki materialowe, prosba o wstepny kosztorys.
- Zachowaj zwiezly, uprzejmy ton maila do uslugodawcy.

## Output shape

### Mail

[gotowa tresc]

### Zalaczniki

- [pelna sciezka 1]
- [pelna sciezka 2]

### Brakujace pola

- [placeholder lub "brak"]
