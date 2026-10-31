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

**Förväntat:** Förklara skillnader mellan resor, delresor och påstigningar och risk för överlappning. Visa separat där API-data finns; avvisa en missvisande summa eller ett diagram som antyder identiska enheter.

## TC04 — Spannmål i svenska hamnar

**Fråga:** Jämför lossat och lastat spannmål i svenska hamnar 2025, inrikes och utrikes.

**Förväntat:** Använd giltig sjöfartsprodukt, rätt varugrupp, riktning och trafikkategori. Redovisa API-värden skilt från egna summeringar. Undvik att behandla både inrikes lastning och lossning som oberoende nationella varuflöden vid en övergripande total.

## Bedömning

Kräv dokumenterad jämförbarhetsprövning, spårbara API-urval, korrekta beräkningar och explicita reservationer. Offline-tester bevisar inte modellens beteende eller att ett levande API-uttag lyckats.
