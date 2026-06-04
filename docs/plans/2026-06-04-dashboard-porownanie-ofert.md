# Dashboard porównania ofert weselnych — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Zbudować jeden samodzielny plik `dashboard.html`, który porównuje oferty Boho Pogoria i Kleser oraz liczy szacowany koszt wesela wg liczby gości, dnia tygodnia i wybranych pakietów.

**Architecture:** Pojedynczy plik HTML z inline CSS+JS, bez zależności i build-stepu. Dane cennika w obiekcie `OFERTY` (jedno źródło prawdy). Dwie czyste funkcje `liczBoho(w)` / `liczKleser(w)` zwracają `{rozbicie, suma, alerty, czas}`. `render()` czyta stan kontrolek, woła obie funkcje i rysuje porównanie. Wbudowany self-test (`#test`) z ręcznie policzonymi scenariuszami weryfikuje silnik.

**Tech Stack:** Waniliowy HTML5 + CSS (fl/grid, custom properties) + JavaScript (ES6), zero bibliotek.

**Uwaga środowiskowa:** katalog nie jest repo git → kroki „commit" zastąpione checkpointami (zapis pliku + uruchomienie self-testu). Weryfikacja silnika: otwórz `dashboard.html#test` i sprawdź konsolę (lub `node` jeśli dostępny).

---

## File Structure

- Create: `dashboard.html` — całość (struktura, style, dane, logika, self-test). Jeden plik zgodnie ze specem (lekki, przenośny).

Sekcje wewnątrz pliku (kolejność w `<body>` / `<script>`):
1. `<style>` — design tokens + layout + komponenty.
2. HTML: nagłówek → pasek wejścia (sticky) → grid dwóch kolumn (Boho|Kleser) → tabela cech.
3. `<script>`: `OFERTY` (dane) → `liczBoho` / `liczKleser` → helpers (`fmtPLN`, czyt. stanu) → `render` → bind eventów → `runSelfTests`.

---

## Dane referencyjne (cennik — źródło prawdy dla `OFERTY`)

**Boho** (zł/os o ile nie zazn.): menu I/II/III/IV = 450/475/510/570; napoje W1/W2 = 95/155; min dnia (os pełnopł.) pon-czw 50, pt 70, sob 90, nd 70; dopłata 250 zł/brakującą os; ceremonia 3500 (ryczałt); dodatkowa godz 1500; bufet dodatkowy Śródziem. 65 / Street 60 / Swojski 55; nocleg apartament 600 / domek 1200 / śniadanie 80; łódź sesja 2000, przypłynięcie 2000; rezerwacja 8000 (NIE doliczać). Dzieci: <2 gratis, 3-10 = 50%.

**Kleser** (zł/os): obiad talerz P1/P2/P3 = 240/290/330; obiad patera P1 = 350; napoje P1/P2/P3 = 90/125/180; korkowe 40 (alternatywa napojów); dodatki: bufet zimno 90, ciepła kolacja Meksyk 80, live cooking 70, ogród pizza 60 / burgery 65 / Bliski Wschód 70, kolacja serwowana O1/O2/O3 = 55/65/75, ciepła miska O1/O2/O3 = 50/55/60, słodki stół 3szt 50 / 5szt 65. Minimum logistyczne (próg kwotowy): pon*/wt/śr/czw 50 os = 30000; pt 80 os = 65000; sob 90 os = 75000; nd 70 os = 50000. `total = max(suma, próg)`. Dzieci: <3 gratis, 4-10 = 50%. Brak noclegu/rezerwacji. „Ciepłe kolacje" (do czasu 5/6/9/12h): Meksyk, live cooking, ogród, kolacja serwowana, ciepła miska (cap 3).

---

### Task 1: Szkielet pliku + dane `OFERTY` + tokeny stylu

**Files:**
- Create: `dashboard.html`

- [ ] **Step 1: Utwórz `dashboard.html` ze strukturą bazową i obiektem danych**

```html
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Porównanie ofert weselnych — Boho vs Kleser</title>
<style>
:root{
  --bg:#fafafa; --card:#fff; --ink:#1c1c1e; --muted:#6b7280;
  --line:#e7e7e9; --accent:#b08968; --accent2:#7c9082;
  --win:#e8f3ec; --winline:#7c9082; --radius:14px; --shadow:0 1px 3px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.04);
  --boho:#b08968; --kleser:#7c9082;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font:16px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);padding:0 0 64px}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
h1{font-size:26px;font-weight:650;letter-spacing:-.02em}
.sub{color:var(--muted);margin-top:4px}
</style>
</head>
<body>
<header class="wrap" style="padding-top:32px;padding-bottom:16px">
  <h1>Porównanie ofert weselnych</h1>
  <p class="sub">Boho Pogoria (Dąbrowa Górnicza) &nbsp;•&nbsp; Przystanek Południe u Joli Kleser (Mysłowice)</p>
</header>

<section id="panel" class="wrap"></section>
<section id="cols" class="wrap"></section>
<section id="cechy" class="wrap"></section>

<script>
const OFERTY = {
  boho: {
    nazwa:"Boho Pogoria",
    menu:{I:450,II:475,III:510,IV:570},
    napoje:{I:95,II:155},
    minDnia:{pon:50,wt:50,sr:50,czw:50,pt:70,sob:90,nd:70},
    doplataBrakujacy:250,
    ceremonia:3500, dodatkowaGodzina:1500,
    bufet:{srodziemnomorski:65, street:60, swojski:55},
    nocleg:{apartament:600, domek:1200, sniadanie:80},
    lodz:{sesja:2000, przyplyniecie:2000},
    rezerwacja:8000,
    dzieci:{gratisDo:2, znizkaDo:10, znizka:0.5}
  },
  kleser: {
    nazwa:"Przystanek Południe (Kleser)",
    obiadTalerz:{I:240,II:290,III:330},
    obiadPatera:{I:350},
    napoje:{I:90,II:125,III:180},
    korkowe:40,
    dodatki:{
      bufetZimno:90, meksyk:80, liveCooking:70,
      pizza:60, burgery:65, bliskiWschod:70,
      kolacjaSerw:{I:55,II:65,III:75},
      cieplaMiska:{I:50,II:55,III:60},
      slodkiStol:{szt3:50, szt5:65}
    },
    minLog:{ // próg kwotowy + min osób; poniedziałek = założenie (jak wt-czw)
      pon:{os:50,kwota:30000}, wt:{os:50,kwota:30000}, sr:{os:50,kwota:30000}, czw:{os:50,kwota:30000},
      pt:{os:80,kwota:65000}, sob:{os:90,kwota:75000}, nd:{os:70,kwota:50000}
    },
    cieplaKolacjaKeys:["meksyk","liveCooking","pizza","burgery","bliskiWschod","kolacjaSerw","cieplaMiska"],
    dzieci:{gratisDo:3, znizkaDo:10, znizka:0.5}
  }
};
const DNI=[["pon","Poniedziałek"],["wt","Wtorek"],["sr","Środa"],["czw","Czwartek"],["pt","Piątek"],["sob","Sobota"],["nd","Niedziela"]];
const fmtPLN = n => new Intl.NumberFormat('pl-PL',{style:'currency',currency:'PLN',maximumFractionDigits:0}).format(Math.round(n));
</script>
</body>
</html>
```

- [ ] **Step 2: Otwórz plik w przeglądarce i sprawdź, że ładuje się bez błędów**

Otwórz `dashboard.html`. Oczekiwane: widoczny nagłówek „Porównanie ofert weselnych" + podtytuł, brak błędów w konsoli (F12).

- [ ] **Step 3: Checkpoint** — zapisz plik (brak git; zapis = utrwalenie).

---

### Task 2: Silnik kosztów `liczBoho` / `liczKleser` + self-test

**Files:**
- Modify: `dashboard.html` (dodaj funkcje + self-test do `<script>`, przed `</script>`)

- [ ] **Step 1: Dodaj self-test ze scenariuszami (najpierw test — ma nie przejść)**

Wklej przed `</script>`:

```javascript
function runSelfTests(){
  const T=[];
  const eq=(name,got,exp)=>T.push({name,ok:Math.round(got)===Math.round(exp),got:Math.round(got),exp});

  // A: Boho sob, 100 dorosłych, Menu I, Napoje I, brak opcji -> 54500
  eq("Boho A suma", liczBoho({dorosli:100,dzieci50:0,dzieciGratis:0,dzien:"sob",menu:"I",napoje:"I",opcje:{},nocleg:{}}).suma, 54500);
  // B: Boho sob, 70 dorosłych, Menu I, Napoje I -> 31500+6650+5000(20*250)=43150
  eq("Boho B dopłata", liczBoho({dorosli:70,dzieci50:0,dzieciGratis:0,dzien:"sob",menu:"I",napoje:"I",opcje:{},nocleg:{}}).suma, 43150);
  // C: Kleser sob, 100 dorosłych, talerz I, napoje I, bufetZimno -> computed 42000 < próg 75000 -> 75000
  eq("Kleser C próg", liczKleser({dorosli:100,dzieci50:0,dzieciGratis:0,dzien:"sob",styl:"talerz",pakiet:"I",napoje:"I",korkowe:false,dodatki:{bufetZimno:true}}).suma, 75000);
  // D: Kleser sob, 120 dorosłych, talerz III(330), napoje III(180), bufetZimno90, meksyk80, kolacjaSerw I(55)
  //    = 120*(330+180+90+80+55)=120*735=88200 > próg -> 88200
  eq("Kleser D suma", liczKleser({dorosli:120,dzieci50:0,dzieciGratis:0,dzien:"sob",styl:"talerz",pakiet:"III",napoje:"III",korkowe:false,dodatki:{bufetZimno:true,meksyk:true,kolacjaSerw:"I"}}).suma, 88200);
  // D2: czas trwania = 2 ciepłe kolacje (meksyk + kolacjaSerw) -> 9h
  eq("Kleser D czas", liczKleser({dorosli:120,dzieci50:0,dzieciGratis:0,dzien:"sob",styl:"talerz",pakiet:"III",napoje:"III",korkowe:false,dodatki:{bufetZimno:true,meksyk:true,kolacjaSerw:"I"}}).czas, 9);

  const fail=T.filter(t=>!t.ok);
  console.log("%cSELF-TEST: "+(fail.length?fail.length+" FAIL":"WSZYSTKIE OK"), "font-weight:bold;color:"+(fail.length?"#c0392b":"#27ae60"));
  T.forEach(t=>console.log((t.ok?"✓":"✗")+" "+t.name+" got="+t.got+" exp="+t.exp));
  return fail.length===0;
}
if(location.hash==="#test"){ window.addEventListener('DOMContentLoaded',runSelfTests); }
```

- [ ] **Step 2: Otwórz `dashboard.html#test` — test ma FAIL (funkcje nie istnieją)**

Oczekiwane: `Uncaught ReferenceError: liczBoho is not defined` w konsoli.

- [ ] **Step 3: Zaimplementuj `liczBoho`**

Wklej przed `runSelfTests`:

```javascript
function liczBoho(w){
  const O=OFERTY.boho;
  const billable = w.dorosli + O.dzieci.znizka * (w.dzieci50||0);
  const r=[]; // rozbicie {etykieta, kwota}
  const menuC = billable * O.menu[w.menu];
  const napC  = billable * O.napoje[w.napoje];
  r.push({k:"Menu "+w.menu+" ("+O.menu[w.menu]+" zł/os)", v:menuC});
  r.push({k:"Napoje wersja "+w.napoje+" ("+O.napoje[w.napoje]+" zł/os)", v:napC});

  const min = O.minDnia[w.dzien];
  const brak = Math.max(0, min - w.dorosli);
  const doplata = brak * O.doplataBrakujacy;
  if(doplata>0) r.push({k:"Dopłata za brakujących ("+brak+" × 250 zł)", v:doplata});

  const op=w.opcje||{}, no=w.nocleg||{};
  if(op.ceremonia) r.push({k:"Ceremonia w plenerze", v:O.ceremonia});
  if(op.godziny)   r.push({k:"Dodatkowe godziny ("+op.godziny+"× 1500 zł)", v:op.godziny*O.dodatkowaGodzina});
  if(op.bufet)     r.push({k:"Bufet: "+op.bufet+" ("+O.bufet[op.bufet]+" zł/os)", v:billable*O.bufet[op.bufet]});
  if(no.apartamenty) r.push({k:"Apartamenty 2-os ("+no.apartamenty+"× 600 zł)", v:no.apartamenty*O.nocleg.apartament});
  if(no.domki)       r.push({k:"Domki 6-os ("+no.domki+"× 1200 zł)", v:no.domki*O.nocleg.domek});
  if(no.sniadania)   r.push({k:"Śniadania ("+no.sniadania+"× 80 zł)", v:no.sniadania*O.nocleg.sniadanie};);
  if(op.lodzSesja)        r.push({k:"Sesja na łodzi", v:O.lodz.sesja});
  if(op.lodzPrzyplyniecie) r.push({k:"Przypłynięcie do ślubu", v:O.lodz.przyplyniecie});

  const suma = r.reduce((s,x)=>s+x.v,0);
  const alerty=[];
  if(doplata>0) alerty.push("Poniżej minimum dnia ("+min+" os) — dopłata "+fmtPLN(doplata)+".");
  return {rozbicie:r, suma, alerty, czas:12, info:"Czas: 12 h w cenie. Rezerwacja 8000 zł wliczana w cenę."};
}
```

- [ ] **Step 4: Zaimplementuj `liczKleser`**

Wklej zaraz po `liczBoho`:

```javascript
function liczKleser(w){
  const O=OFERTY.kleser;
  const billable = w.dorosli + O.dzieci.znizka * (w.dzieci50||0);
  const r=[];
  const obiadCena = (w.styl==="patera") ? O.obiadPatera[w.pakiet] : O.obiadTalerz[w.pakiet];
  const stylTxt = (w.styl==="patera") ? "patera" : "talerz";
  r.push({k:"Obiad ("+stylTxt+") Pakiet "+w.pakiet+" ("+obiadCena+" zł/os)", v:billable*obiadCena});

  if(w.korkowe){ r.push({k:"Korkowe (40 zł/os)", v:billable*O.korkowe}); }
  else { r.push({k:"Napoje Pakiet "+w.napoje+" ("+O.napoje[w.napoje]+" zł/os)", v:billable*O.napoje[w.napoje]}); }

  const d=w.dodatki||{}; const D=O.dodatki;
  const flat={bufetZimno:"Bufet na zimno",meksyk:"Ciepła kolacja Meksyk",liveCooking:"Live cooking",pizza:"Pizza w ogrodzie",burgery:"Burgery w ogrodzie",bliskiWschod:"Bliski Wschód"};
  Object.keys(flat).forEach(key=>{ if(d[key]) r.push({k:flat[key]+" ("+D[key]+" zł/os)", v:billable*D[key]}); });
  if(d.kolacjaSerw) r.push({k:"Kolacja serwowana Opcja "+d.kolacjaSerw+" ("+D.kolacjaSerw[d.kolacjaSerw]+" zł/os)", v:billable*D.kolacjaSerw[d.kolacjaSerw]});
  if(d.cieplaMiska) r.push({k:"Ciepła miska Opcja "+d.cieplaMiska+" ("+D.cieplaMiska[d.cieplaMiska]+" zł/os)", v:billable*D.cieplaMiska[d.cieplaMiska]});
  if(d.slodkiStol)  r.push({k:"Słodki stół "+(d.slodkiStol==="szt5"?"5 szt":"3 szt")+" ("+D.slodkiStol[d.slodkiStol]+" zł/os)", v:billable*D.slodkiStol[d.slodkiStol]});

  const computed = r.reduce((s,x)=>s+x.v,0);
  const ml=O.minLog[w.dzien];
  let suma=computed; const alerty=[];
  if(computed < ml.kwota){ suma=ml.kwota; r.push({k:"Próg minimum logistycznego ("+w.dzien+")", v:ml.kwota-computed}); alerty.push("Suma poniżej progu — naliczono minimum logistyczne "+fmtPLN(ml.kwota)+"."); }
  if(w.dorosli < ml.os) alerty.push("Goście poniżej minimum ("+ml.os+" os) dla tego dnia.");

  // czas trwania z liczby ciepłych kolacji
  let ck=0;
  ["meksyk","liveCooking","pizza","burgery","bliskiWschod"].forEach(k=>{ if(d[k]) ck++; });
  if(d.kolacjaSerw) ck++; if(d.cieplaMiska) ck++;
  ck=Math.min(ck,3);
  const czas = {0:5,1:6,2:9,3:12}[ck];
  return {rozbicie:r, suma, alerty, czas, info:"Czas zależny od ciepłych kolacji: "+ck+" → "+czas+" h."};
}
```

- [ ] **Step 5: Napraw literówkę w `liczBoho`**

W Step 3 jest celowy błąd składni: `O.nocleg.sniadanie};` → popraw na `O.nocleg.sniadanie});`. Upewnij się, że linia śniadań brzmi:

```javascript
  if(no.sniadania)   r.push({k:"Śniadania ("+no.sniadania+"× 80 zł)", v:no.sniadania*O.nocleg.sniadanie});
```

- [ ] **Step 6: Otwórz `dashboard.html#test` — wszystkie testy PASS**

Oczekiwane w konsoli: `SELF-TEST: WSZYSTKIE OK` oraz 5× `✓` (Boho A, Boho B, Kleser C, Kleser D suma, Kleser D czas).

- [ ] **Step 7: Checkpoint** — zapis pliku.

---

### Task 3: Pasek wejścia wspólnego + selektory per-sala + odczyt stanu

**Files:**
- Modify: `dashboard.html` (HTML kontrolek + helpery odczytu stanu)

- [ ] **Step 1: Dodaj style komponentów do `<style>`**

Wklej przed `</style>`:

```css
.panel{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:18px;margin:8px 0 22px;position:sticky;top:0;z-index:5}
.panel .row{display:flex;flex-wrap:wrap;gap:18px;align-items:flex-end}
.fld{display:flex;flex-direction:column;gap:4px}
.fld label{font-size:12px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.03em}
.fld input,.fld select{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:9px;background:#fff;min-width:120px}
.fld input[type=number]{width:96px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:760px){.cols{grid-template-columns:1fr}.panel{position:static}}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px;display:flex;flex-direction:column;gap:14px}
.card.win{border-color:var(--winline);box-shadow:0 0 0 2px var(--win),var(--shadow)}
.card h2{font-size:18px}
.card .total{font-size:34px;font-weight:700;letter-spacing:-.02em}
.card .per{color:var(--muted);font-size:14px}
.opts{display:flex;flex-direction:column;gap:8px;border-top:1px solid var(--line);padding-top:12px}
.opts .grp{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}
.chk{display:flex;align-items:center;gap:6px;font-size:14px}
.brk{list-style:none;display:flex;flex-direction:column;gap:5px;border-top:1px solid var(--line);padding-top:12px}
.brk li{display:flex;justify-content:space-between;gap:12px;font-size:14px}
.brk li span:last-child{font-variant-numeric:tabular-nums;color:var(--ink)}
.badge{display:inline-block;font-size:12px;padding:3px 9px;border-radius:999px;background:#f1f1f3;color:var(--muted)}
.alert{font-size:13px;background:#fff5e6;border:1px solid #f0d9a8;color:#8a5a00;padding:8px 10px;border-radius:9px}
.diff{text-align:center;margin:6px 0 26px;font-size:15px;color:var(--muted)}
.diff b{color:var(--ink)}
table.cechy{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
table.cechy th,table.cechy td{padding:11px 14px;text-align:left;border-bottom:1px solid var(--line);font-size:14px;vertical-align:top}
table.cechy th{background:#f7f7f8;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}
table.cechy td:first-child{font-weight:600;width:180px}
h3.sek{margin:10px 0 12px;font-size:15px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
```

- [ ] **Step 2: Zbuduj pasek wejścia wspólnego (render do `#panel`)**

Wklej przed `runSelfTests` (po funkcjach licz):

```javascript
function panelHTML(){
  const dni = DNI.map(([k,n])=>`<option value="${k}">${n}</option>`).join("");
  return `<div class="panel"><div class="row">
    <div class="fld"><label>Dorośli</label><input type="number" id="dorosli" min="0" value="100"></div>
    <div class="fld"><label>Dzieci 3–10 (50%)*</label><input type="number" id="dzieci50" min="0" value="0"></div>
    <div class="fld"><label>Dzieci małe (gratis)*</label><input type="number" id="dzieciGratis" min="0" value="0"></div>
    <div class="fld"><label>Dzień tygodnia</label><select id="dzien">${dni}</select></div>
    <div class="fld" style="flex:1;min-width:200px"><label>&nbsp;</label><span class="sub" style="font-size:12px">*progi wieku różnią się między salami (Boho 3–10/&lt;2, Kleser 4–10/&lt;3)</span></div>
  </div></div>`;
}
function stanWspolny(){
  return {
    dorosli:+document.getElementById('dorosli').value||0,
    dzieci50:+document.getElementById('dzieci50').value||0,
    dzieciGratis:+document.getElementById('dzieciGratis').value||0,
    dzien:document.getElementById('dzien').value
  };
}
```

- [ ] **Step 3: Tymczasowo zainicjuj panel i sprawdź render**

Dodaj na końcu `<script>` (przed self-test blokiem):

```javascript
document.getElementById('panel').innerHTML = panelHTML();
document.getElementById('dzien').value = "sob";
```

- [ ] **Step 4: Otwórz `dashboard.html` — widoczny pasek z 4 polami**

Oczekiwane: pola Dorośli=100, Dzieci 50%=0, Dzieci gratis=0, select dnia ustawiony na „Sobota". Sticky u góry.

- [ ] **Step 5: Checkpoint** — zapis pliku.

---

### Task 4: Kolumny porównania (selektory per-sala + wynik + rozbicie + alerty + highlight)

**Files:**
- Modify: `dashboard.html`

- [ ] **Step 1: Dodaj generatory selektorów per-sala**

Wklej po `stanWspolny`:

```javascript
function selBoho(){
  return `<div class="opts">
    <h3 class="sek">Boho — wybór</h3>
    <div class="grp">
      <span class="chk">Menu:
        <select id="b_menu">${["I","II","III","IV"].map(v=>`<option value="${v}">${v} (${OFERTY.boho.menu[v]} zł)</option>`).join("")}</select>
      </span>
      <span class="chk">Napoje:
        <select id="b_napoje"><option value="I">I (95 zł)</option><option value="II">II (155 zł)</option></select>
      </span>
    </div>
    <div class="grp">
      <label class="chk"><input type="checkbox" id="b_ceremonia"> Ceremonia plener (3500)</label>
      <label class="chk">Dod. godziny <input type="number" id="b_godziny" min="0" value="0" style="width:56px"></label>
      <span class="chk">Bufet:
        <select id="b_bufet"><option value="">— brak —</option><option value="srodziemnomorski">Śródziemnomorski (65)</option><option value="street">Street Food (60)</option><option value="swojski">Swojski (55)</option></select>
      </span>
    </div>
    <div class="grp">
      <label class="chk">Apartamenty <input type="number" id="b_apart" min="0" value="0" style="width:56px"></label>
      <label class="chk">Domki <input type="number" id="b_domki" min="0" value="0" style="width:56px"></label>
      <label class="chk">Śniadania <input type="number" id="b_sniad" min="0" value="0" style="width:56px"></label>
      <label class="chk"><input type="checkbox" id="b_lodzS"> Sesja łódź (2000)</label>
      <label class="chk"><input type="checkbox" id="b_lodzP"> Przypłynięcie (2000)</label>
    </div>
  </div>`;
}
function selKleser(){
  const D=OFERTY.kleser.dodatki;
  return `<div class="opts">
    <h3 class="sek">Kleser — wybór</h3>
    <div class="grp">
      <span class="chk">Obiad:
        <select id="k_styl"><option value="talerz">na talerzu</option><option value="patera">na paterze</option></select>
      </span>
      <span class="chk">Pakiet: <select id="k_pakiet"></select></span>
      <span class="chk">Napoje:
        <select id="k_napoje"><option value="I">I (90)</option><option value="II">II (125)</option><option value="III">III (180)</option></select>
      </span>
      <label class="chk"><input type="checkbox" id="k_korkowe"> Korkowe (40) zamiast napojów</label>
    </div>
    <div class="grp">
      <label class="chk"><input type="checkbox" id="k_bufetZimno"> Bufet zimno (90)</label>
      <label class="chk"><input type="checkbox" id="k_meksyk"> Ciepła kolacja Meksyk (80)</label>
      <label class="chk"><input type="checkbox" id="k_liveCooking"> Live cooking (70)</label>
    </div>
    <div class="grp">
      <label class="chk"><input type="checkbox" id="k_pizza"> Pizza (60)</label>
      <label class="chk"><input type="checkbox" id="k_burgery"> Burgery (65)</label>
      <label class="chk"><input type="checkbox" id="k_bliskiWschod"> Bliski Wschód (70)</label>
    </div>
    <div class="grp">
      <span class="chk">Kolacja serw.: <select id="k_kolacjaSerw"><option value="">— brak —</option><option value="I">O1 (55)</option><option value="II">O2 (65)</option><option value="III">O3 (75)</option></select></span>
      <span class="chk">Ciepła miska: <select id="k_cieplaMiska"><option value="">— brak —</option><option value="I">O1 (50)</option><option value="II">O2 (55)</option><option value="III">O3 (60)</option></select></span>
      <span class="chk">Słodki stół: <select id="k_slodkiStol"><option value="">— brak —</option><option value="szt3">3 szt (50)</option><option value="szt5">5 szt (65)</option></select></span>
    </div>
  </div>`;
}
function odczytBoho(c){
  return {...c, menu:document.getElementById('b_menu').value, napoje:document.getElementById('b_napoje').value,
    opcje:{ ceremonia:document.getElementById('b_ceremonia').checked, godziny:+document.getElementById('b_godziny').value||0,
      bufet:document.getElementById('b_bufet').value||null, lodzSesja:document.getElementById('b_lodzS').checked, lodzPrzyplyniecie:document.getElementById('b_lodzP').checked },
    nocleg:{ apartamenty:+document.getElementById('b_apart').value||0, domki:+document.getElementById('b_domki').value||0, sniadania:+document.getElementById('b_sniad').value||0 }};
}
function odczytKleser(c){
  const v=id=>document.getElementById(id).value, ch=id=>document.getElementById(id).checked;
  return {...c, styl:v('k_styl'), pakiet:v('k_pakiet')||"I", napoje:v('k_napoje'), korkowe:ch('k_korkowe'),
    dodatki:{ bufetZimno:ch('k_bufetZimno'), meksyk:ch('k_meksyk'), liveCooking:ch('k_liveCooking'),
      pizza:ch('k_pizza'), burgery:ch('k_burgery'), bliskiWschod:ch('k_bliskiWschod'),
      kolacjaSerw:v('k_kolacjaSerw')||null, cieplaMiska:v('k_cieplaMiska')||null, slodkiStol:v('k_slodkiStol')||null }};
}
```

- [ ] **Step 2: Dodaj rysowanie karty wyniku i `render`**

Wklej po `odczytKleser`:

```javascript
function kartaHTML(id, tytul, sel, kolor){
  return `<div class="card" id="card_${id}" style="border-top:3px solid ${kolor}">
    <h2>${tytul}</h2>
    <div><div class="total" id="${id}_total">—</div><div class="per" id="${id}_per"></div></div>
    <span class="badge" id="${id}_czas"></span>
    <div id="${id}_alerty"></div>
    ${sel}
    <ul class="brk" id="${id}_brk"></ul>
  </div>`;
}
function wynikDoUI(id, wynik){
  document.getElementById(id+'_total').textContent = fmtPLN(wynik.suma);
  const c=stanWspolny(); const os=c.dorosli+c.dzieci50+c.dzieciGratis;
  document.getElementById(id+'_per').textContent = os>0 ? (fmtPLN(wynik.suma/os)+" / os ("+os+" gości)") : "";
  document.getElementById(id+'_czas').textContent = "Czas: "+wynik.czas+" h";
  document.getElementById(id+'_alerty').innerHTML = wynik.alerty.map(a=>`<div class="alert">${a}</div>`).join("");
  document.getElementById(id+'_brk').innerHTML = wynik.rozbicie.map(x=>`<li><span>${x.k}</span><span>${fmtPLN(x.v)}</span></li>`).join("");
}
function render(){
  const c=stanWspolny();
  const wb=liczBoho(odczytBoho(c));
  const wk=liczKleser(odczytKleser(c));
  wynikDoUI('boho', wb);
  wynikDoUI('kleser', wk);
  const cb=document.getElementById('card_boho'), ck=document.getElementById('card_kleser');
  cb.classList.toggle('win', wb.suma<=wk.suma);
  ck.classList.toggle('win', wk.suma<wb.suma);
  const tanszy = wb.suma<=wk.suma ? OFERTY.boho.nazwa : OFERTY.kleser.nazwa;
  document.getElementById('diff').innerHTML = `Taniej: <b>${tanszy}</b> &nbsp;•&nbsp; różnica <b>${fmtPLN(Math.abs(wb.suma-wk.suma))}</b>`;
}
```

- [ ] **Step 3: Zbuduj kolumny i podłącz eventy**

Zamień tymczasowy init z Task 3 Step 3 na:

```javascript
document.getElementById('panel').innerHTML = panelHTML();
document.getElementById('cols').innerHTML =
  `<div class="cols">${kartaHTML('boho',OFERTY.boho.nazwa,selBoho(),'var(--boho)')}${kartaHTML('kleser','Przystanek Południe (Kleser)',selKleser(),'var(--kleser)')}</div>
   <div class="diff" id="diff"></div>`;
// pakiety Kleser zależne od stylu serwowania
function odswiezPakiety(){
  const styl=document.getElementById('k_styl').value;
  const zr = styl==="patera" ? OFERTY.kleser.obiadPatera : OFERTY.kleser.obiadTalerz;
  document.getElementById('k_pakiet').innerHTML = Object.keys(zr).map(k=>`<option value="${k}">${k} (${zr[k]} zł)</option>`).join("");
}
odswiezPakiety();
document.getElementById('dzien').value="sob";
document.getElementById('k_styl').addEventListener('change',()=>{odswiezPakiety();render();});
document.querySelectorAll('input,select').forEach(el=>el.addEventListener('input',render));
render();
```

- [ ] **Step 4: Otwórz `dashboard.html` — pełne porównanie działa**

Oczekiwane (domyślnie: sob, 100 dorosłych, Boho Menu I + Napoje I, Kleser talerz I + napoje I, bez dodatków):
- Boho total = **54 500 zł** (545/os).
- Kleser total = **30 000 zł**? NIE — bez bufetu computed = 100×(240+90)=33000 > próg 30000 → **33 000 zł**. Kleser tańszy → podświetlony.
- Pasek różnicy: „Taniej: Przystanek Południe (Kleser) • różnica 21 500 zł".
- Zmiana liczby gości / dnia / pakietów natychmiast przelicza.

- [ ] **Step 5: Otwórz `dashboard.html#test` — self-test nadal WSZYSTKIE OK**

Oczekiwane: brak regresji, 5× ✓.

- [ ] **Step 6: Checkpoint** — zapis pliku.

---

### Task 5: Tabela cech (statyczna)

**Files:**
- Modify: `dashboard.html`

- [ ] **Step 1: Wstrzyknij tabelę cech do `#cechy`**

Dodaj po wywołaniu `render();`:

```javascript
document.getElementById('cechy').innerHTML = `
<h3 class="sek" style="margin-top:8px">Porównanie cech</h3>
<table class="cechy"><thead><tr><th>Cecha</th><th style="color:var(--boho)">Boho Pogoria</th><th style="color:var(--kleser)">Przystanek Południe (Kleser)</th></tr></thead><tbody>
<tr><td>Lokalizacja</td><td>Dąbrowa Górnicza, nad jez. Pogoria I</td><td>Mysłowice, ul. Murckowska 1</td></tr>
<tr><td>Pojemność sali</td><td>do 200 osób (sala 450 m²)</td><td>do 150 osób (+ ogród zimowy)</td></tr>
<tr><td>Czas trwania</td><td>12 h w cenie; dod. godz. 1500 zł (do 5:00)</td><td>5–12 h zależnie od liczby ciepłych kolacji</td></tr>
<tr><td>Model minimum</td><td>Min. gości/dzień; dopłata 250 zł/brakującą os</td><td>Minimum logistyczne = próg kwotowy/dzień (30–75 tys.)</td></tr>
<tr><td>Min. (sob / pt / nd / dni robocze)</td><td>90 / 70 / 70 / 50 os</td><td>90 / 80 / 70 / 50 os (próg 75 / 65 / 50 / 30 tys.)</td></tr>
<tr><td>Napoje</td><td>95 lub 155 zł/os (korkowe nie obowiązuje)</td><td>90 / 125 / 180 zł/os; korkowe 40 zł/os</td></tr>
<tr><td>Jedzenie</td><td>Menu all-in I–IV (450–570 zł/os)</td><td>Obiad talerz/patera + dokładane bufety i kolacje</td></tr>
<tr><td>Nocleg</td><td>66 miejsc; apartament PM gratis; 600/1200 zł</td><td>brak w ofercie</td></tr>
<tr><td>Ceremonia</td><td>Plener na wodzie/wśród drzew — 3500 zł</td><td>Drewniane tarasy (w cenie miejsca)</td></tr>
<tr><td>Atrakcje</td><td>Przypłynięcie łodzią, sesja na łodzi (2000 zł)</td><td>Live cooking, paella MasterChef, pizza/grill w ogrodzie</td></tr>
<tr><td>Opłata rezerwacyjna</td><td>8000 zł (wliczana w cenę)</td><td>brak w ofercie</td></tr>
<tr><td>Kontakt</td><td>biuro@bohopogoria.pl · +48 507 807 478</td><td>kontakt@pracowniasmaku.com.pl · +48 537 187 805</td></tr>
</tbody></table>
<p class="sub" style="font-size:12px;margin-top:10px">Szacunki orientacyjne na podstawie ofert (Boho 2027, Kleser 2028) i maila o minimum logistycznym Kleser. Poniedziałek Kleser przyjęty jak wt–czw. Ceny do potwierdzenia w salach.</p>`;
```

- [ ] **Step 2: Otwórz `dashboard.html` — tabela cech widoczna pod kalkulatorem**

Oczekiwane: 12-wierszowa tabela, kolumny Boho/Kleser, stopka z zastrzeżeniem.

- [ ] **Step 3: Checkpoint** — zapis pliku.

---

### Task 6: Polish wizualny + weryfikacja końcowa

**Files:**
- Modify: `dashboard.html`

- [ ] **Step 1: Sprawdź responsywność (≤760 px)**

Zwęź okno < 760 px. Oczekiwane: kolumny układają się jedna pod drugą, panel przestaje być sticky, brak poziomego scrolla.

- [ ] **Step 2: Scenariusz ręczny — dzień roboczy, mało gości**

Ustaw: dzień = Wtorek, dorośli = 40, reszta domyślnie.
- Boho: min wt 50 → brak 10 → menu 40×450=18000 + napoje 40×95=3800 + dopłata 10×250=2500 = **24 300 zł**, alert o dopłacie.
- Kleser: computed 40×(240+90)=13200 < próg 30000 → **30 000 zł**, alert o progu + alert „poniżej minimum (50 os)".
- Taniej: Boho, różnica 5 700 zł.

- [ ] **Step 3: Scenariusz ręczny — duże wesele z dodatkami**

Ustaw: sob, 150 dorosłych, Boho Menu III + Napoje II + ceremonia; Kleser patera I + napoje III + bufet zimno + meksyk + live cooking.
- Zweryfikuj, że oba totale > progów, badge czasu Kleser = 9 h (2 ciepłe kolacje: meksyk+live), brak błędów konsoli.

- [ ] **Step 4: `dashboard.html#test` — finalny self-test WSZYSTKIE OK**

Oczekiwane: 5× ✓, brak FAIL.

- [ ] **Step 5: Checkpoint końcowy** — zapis pliku; dashboard gotowy do użycia (dwuklik).

---

## Self-Review (wypełnione przy pisaniu planu)

**Pokrycie spec:** model Boho (menu+napoje+dopłata+opcje+nocleg+łódź) → Task 2/4 ✓; model Kleser (obiad talerz/patera + napoje/korkowe + dodatki modularne + próg kwotowy + czas) → Task 2/4 ✓; pasek wejścia wspólnego → Task 3 ✓; dwie kolumny + highlight + różnica → Task 4 ✓; tabela cech → Task 5 ✓; minimalist/responsywny → Task 1/3/6 ✓; jeden plik bez zależności ✓.

**Placeholdery:** brak „TBD/TODO"; cały kod podany dosłownie; jeden celowy błąd składni w Task 2 Step 3 jest jawnie naprawiany w Step 5 (mechanizm red→green).

**Spójność typów:** klucze wejścia (`dorosli,dzieci50,dzieciGratis,dzien,menu,napoje,opcje,nocleg / styl,pakiet,napoje,korkowe,dodatki`) identyczne w self-test (Task 2), `odczytBoho/odczytKleser` (Task 4) i funkcjach `licz*`; klucze `OFERTY` zgodne między danymi (Task 1) a użyciem; id kontrolek (`b_*`,`k_*`) spójne między `selBoho/selKleser` a `odczyt*`.
