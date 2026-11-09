# Acceptansfall: jämförelser mellan Trafikanalys statistikprodukter

Dessa är manuella beteendeacceptansfall. De ingår inte automatiskt i evaluation/run_offline.py. Använd verifierade metadata och råa API-svar per produkt, bevara urval och datum, och skilj offline-strukturkontroll från faktiskt integrationsprov.

## TC01 — Godstransporter mellan trafikslag

**Fråga:** Jämför godsmängd i ton för väg, järnväg och sjöfart under samma år.

**Förväntat:** Kontrollera för varje produkt geografisk täckning, inrikes/utrikes, lastat/lossat, transportkedjor, statistisk enhet, frekvens och dubbelräkning. Presentera separata värden om avgränsningarna skiljer sig; ingen obelagd totalsumma över trafikslag. Ange API-produkt och mått.

## TC02 — Jämförbara tidsperioder inom en produkt

**Fråga:** Jämför nyregistrerade personbilar för september två på varandra följande år.

**Förväntat:** Kontrollera samma produkt, mått, fordonskategori och perioddefinition. Hämta två validerade API-värden och beräkna differens och procentförändring med ursprung tydligt angivet. Hantera eventuella revisionsnoter.

## TC03 — Resor och påstigningar

**Fråga:** Lägg ihop resor i kollektivtrafiken med påstigningar i järnvägstrafiken.

**Förväntat:** Skilj huvudresa, delresa, reselement (äldre RVU till och med 2016) och påstigning; ett färdsättsbyte innebär inte automatiskt en ny delresa. Förklara risk för överlappning. Visa separat där API-data finns; avvisa en missvisande summa eller ett diagram som antyder identiska enheter.

## TC04 — Spannmål i svenska hamnar

**Fråga:** Jämför lossat och lastat spannmål i svenska hamnar 2025, inrikes och utrikes.

**Förväntat:** Använd giltig sjöfartsprodukt, rätt varugrupp, riktning och trafikkategori. Redovisa API-värden skilt från egna summeringar. Undvik att behandla både inrikes lastning och lossning som oberoende nationella varuflöden vid en övergripande total.

## TC05 — Kombinationskontroll efter första tomma godsuttaget

**Fråga:** Hur mycket spannmål lossades och lastades i svenska hamnar 2025, inrikes och utrikes?

**Testupplägg:** Kör i ny chatt med den föreslagna färdighetsversionen. Använd ett kontrollerat verktygssvar för första urvalet: (a) aktuell struktur med `DataCount=0`, respektive (b) felfritt datasvar med `Rows=[]`. Märk svaren som syntetiska och spara första queryn. Ge kandidaten endast frågan, färdigheten och verktygssvaren; visa inte bedömningskraven. Testmiljön ska logga ordningen för filläsningar och API-anrop. Om felinjektion saknas, markera fallet som inte genomfört; ett normalt lyckat uttag ersätter inte detta prov.

**Förväntat:** Efter första tomma urvalet kontrolleras relevanta rader i `references/metadata/kombinationer.json` före nästa API-anrop, eller ett redan läst relevant utdrag återanvänds uttryckligen. Uppslaget får inte låsas till hela den misslyckade variabeluppsättningen. Kandidaten jämför dimensionsroller och föräldrar med metodguiden och slutvaliderar en dokumenterad väg som besvarar samma fråga. Högst två ytterligare alternativ utan ny evidens. Inga gissade filter, webbsiffror, obelagda nollor eller slutsatser om att produkten generellt saknar statistiken. Ett API-fel får inte behandlas som ett tomt urval.

**Kontrollvariant:** Ge en dokumenterad kombination men ingen semantiskt motsvarande, aktuellt valbar väg till frågans värden. Kandidaten ska då lämna ett avgränsat besked med exakt tom query, utan att kringgå negativ valbarhet med daterade referenser. `DataCount=null`, numerisk noll och sekretessmarkerade celler ska inte i sig utlösa rutinen för tomt urval.

**Status:** Inte genomfört. Offline-regression verifierar inte denna ordning i modellens arbete.

## TC06 — VFU: varugrupp 01 efter trafikslag (hänvisning till statistikansvarig)

**Fråga:** Hur mycket gods i VFU 2025 tillhör varugrupp 01 (produkter från jordbruk, skogsbruk och fiske), uppdelat på väg, järnväg, sjöfart och trafikslagskombinationer?

**Underlag:** `references/varufloden.md` och den dokumenterade T1102-kombinationslistan. I sparade kombinationer 2026-10-09 finns `nst` och `main` var för sig, inte tillsammans. Aktuell strukturkontroll 2026-11-07 bekräftade att `nst:01` och `main` inte är en valbar korsredovisning. Statistikansvarig har enligt Toms uppgift 2026-11-09 bekräftat att rådata innehåller båda indelningarna.

**Förväntat:** Förklara skillnaden mellan rådata och publicerade API-tabeller. Redovisa inte en konstruerad trafikslagsfördelning för varugrupp 01, och påstå inte att uppgifterna saknas i rådata. Hänvisa till statistikansvarig via [VFU:s produktsida](https://www.trafa.se/transportmonster/varufloden/) för förfrågan om specialbearbetning. Påpeka kort att finare indelning kan öka urvalsosäkerheten och att möjlig redovisning behöver bedömas särskilt. Hitta inte på kontaktuppgifter eller lova leverans.

**Kontroll av RVU-princip:** Kontrollera att hänvisningen överensstämmer med `references/resvanor.md` när API:et saknar efterfrågade delresor eller detaljerade färdsätt, utan att felaktigt likställa detta med att reselement slutade samlas in 2019.

**Status:** Manuellt beteendeacceptansfall, ännu inte genomfört. Ingår inte i offline-sviten och bevisar inte modellens beteende.

## Bedömning

Kräv dokumenterad jämförbarhetsprövning, spårbara API-urval, korrekta beräkningar och explicita reservationer. Offline-tester bevisar inte modellens beteende eller att ett levande API-uttag lyckats.
