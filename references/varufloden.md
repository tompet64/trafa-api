# Varuflödesundersökningen – varusändningar och transportkedjor

Granskat 2026-10-11 mot dokumentation och sparad API-metadata. Delvis granskad profil; aktuell API-årstäckning och sluturval måste verifieras.

Varuägar-/arbetsställebaserad undersökning för hela transportkedjor, godsvikt, varuvärde, bransch och start/mål. Komplement till trafikslagsspecifik godstransportstatistik.

## Definitioner och avgränsningar

- Urval inom gruvor/mineralutvinning, tillverkning samt parti- och distanshandel kompletteras med administrativa och centrala källor. (Källa: https://www.trafa.se/transportmonster/varufloden/, Undersökningens omfattning.)
- Avgående sändningar omfattar inrikes och export; ankommande avser import. Transit och förflyttningar inom eget industriområde ingår inte. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf, 1.2.1.)
- Sändning avser leverans av samma varukod till viss mottagare; leveranser mellan arbetsställen inom samma företag och returer ingår. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/varuflodesundersokningen-2025.pdf, Definitioner.)
- Godsvikt är nettovikt utan emballage. Värde är fakturavärde i SEK utan moms och fraktkostnader. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf, 1.2.2.)
- Storleksklass avser antal anställda vid arbetsstället, inte hela företaget. Branschvisa cut-off-gränser begränsar populationen. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf, 1.2.1; 1.2.4.)
- En sändning räknas en gång längs transportkedjan. Trafikslagsspecifik statistik kan räkna samma gods i flera led; volymerna kan därför inte adderas till VFU. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf, 5.2.)
- När hela kedjan är okänd kan uppgiftslämnaren ange trafikslaget för den längsta sträckan. Därav-rader är delmängder, inte ytterligare volym. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/varuflodesundersokningen-2025.pdf, Tabell 1.1, fotnot.)
- 95-procentiga KI kvantifierar urvalsosäkerhet; mätfel ingår inte. Register-/centraldata kräver ibland harmonisering och imputering. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf, 2.1.)
- Tabellverket 2025 redovisar punktskattning ± KI i måttets enhet; för procentandelar är KI i procentenheter. Verifiera motsvarande numeriska representation i aktuellt API. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/varuflodesundersokningen-2025.pdf, Tabell 1.1–1.4.)
- Undersökningen är intermittent: 2001, 2004/2005, 2009, 2016, 2021, 2025. Nästa omgång är inte planerad enligt deklarationen. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf, 3.2.)
- Jämförelser före 2016 är mer begränsade. Ändrad täckning i register-/centralkällor kan påverka nivåer även mellan senare omgångar. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf, 5.1.)
- Branschavgränsningen täcker inte alla sändningar, särskilt import. Tolka inte ankommande total som hela Sveriges import. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/varuflodesundersokningen-2025.pdf, Kort om statistiken.)
- 2025 års resultat publicerades 2026-09-18. Produktsidans äldre text om fem omgångar till 2021 är eftersläpande; aktuell publiceringslista innehåller också 2025. (Källa: https://www.trafa.se/transportmonster/varufloden/, Publiceringar; Publicering.)
- Statistiken ingår i SOS; deklarationen anger TK11, skilt från API-koden T1102. (Källa: https://www.trafa.se/globalassets/statistik/varufloden/2025/kvalitetsdeklaration-vfu-2025.pdf, Allmänna uppgifter A.)

## API-tolkning

- För ton malm på svenskregistrerade tunga lastbilar i inrikes trafik används T10061; VFU har annan population, mäter hela kedjor och ger inte detta fordonsurval.
- Vikt, värde och antal sändningar har olika andelar. andelv, andelva och andelsand är inte utbytbara; kontrollera nämnaren inom samma riktning, period och urval.
- Avgående inrikes plus export bildar avgående total när källans redovisning medger det. Ankommande är import, inte samma inrikes gods vid mottagaränden. Tolka aldrig riktningar utan aktuell metadata.
- trafikslag är H med main och sub. Skilj hela trafikslagskedjor från huvudsakligt trafikslag; en väg–sjöfart–väg-kedja är inte tre oberoende sändningar. Behåll parentrelationer och addera inte därav-rader.
- anstallda och vissa vägregions-/storleksklasstabeller kan vara begränsade till urvalsinsamlingen. Överför inte den delpopulationens andelar till totalen inklusive registerdata utan kontroll av tabellfotnoter.
- Start-/målregion beskriver sändningens ändpunkter, inte alla regioner längs rutten. Avsändande/mottagande bransch och geografiska roller måste följa vald riktning. NST-grupper kan vara bredare än ordet malm.
- Begär punktskattning och tillhörande KI i samma kombination om tillåtet; alla detaljkombinationer har inte KI i den sparade listan. Saknat KI betyder inte noll osäkerhet. Summera inte marginaler eller KI.
- 2025 års tabellverk använder ± för 95-procentigt KI. Kontrollera aktuellt API mot denna konvention före presentation. KI 0 kan avse registerdel eller avrundning och betyder inte frånvaro av alla fel.
- Vikt i tusen ton och värde i miljoner kronor är inte tonkilometer eller fasta priser. Beräkna inte transportarbete utan sträckunderlag och ingen prisjusterad utveckling utan dokumenterad deflator.
- Behåll luckor mellan undersökningsår och perioden 2004/2005; interpolera inte som observerad årsstatistik. Produktsidans nya publicering bevisar inte att API-et har samma år.
- Bevara markeringar: .. saknat/alltför osäkert, . ej tillämpligt, – noll, 0 positivt under halva enheten, U undertryckt enligt tabellverket. Översätt inte automatiskt PDF-markeringar till API-nollor.

Mått och KI-koder:

| Mått | Enhet | KI-kod |
|---|---|---|
| vikt | tusen ton | viktki |
| varde | miljoner kronor | vardeki |
| andelv | procent av godsvikt | andelvki |
| andelva | procent av varuvärde | andelvaki |
| antalsan | tusen sändningar | antalsanki |
| genomkg | kilogram per sändning | genomkgki |
| andelsand | procent av antal sändningar | andelsandki |

## Öppna frågor

- Faktisk API-tillgänglighet för 2025 och eventuell ändring av kodverk, kombinationer och KI-konvention jämfört med sparad struktur.
- Exakt delpopulation och nämnare för varje storleksklass-, vägregions- och geografisk detaljkombination.
- Hur API-et kodar undertryckta, osäkra och avrundade värden i respektive aktuellt urval.
