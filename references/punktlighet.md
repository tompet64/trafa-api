# Punktlighet på järnväg

Delvis granskad mot produktsida och kvalitetsdeklaration 2025, lästa 2026-10-11, samt sparad API-metadata från 2026-10-09. Konkret uttag kräver slutvalidering.

| Produktkod | Roll |
|---|---|
| T0604_RT_ar | Punktlighet för framförda tåg, årspublicering |
| T0604_RT_Kv | Punktlighet för framförda tåg, preliminär kvartalspublicering |
| T0604_STM_ar | Punktlighet på järnväg, STM, årspublicering |
| T0604_STM_kv | Punktlighet på järnväg, STM, preliminär kvartalspublicering |

## population

Planerade persontågsankomster vid slutstationer på järnvägsanläggningar i Sverige, utom Saltsjöbanan och Roslagsbanan. Inte godståg, spårväg eller tunnelbana. Tågankomster är inte resenärers ankomster eller uppmätt väntetid för alla resenärer.

## rt

RT anger andelen framförda persontåg som ankommit slutstation inom vald tidsgräns. Inställda tåg ingår inte i denna nämnare.

## stm

STM anger andelen planerade tåg dagen före avgång som ankommit slutstation inom vald tidsgräns. Avvikelser efter kl. 0.00 dagen före planerad avgång beaktas. Anta inte att alla inställningar sedan den årliga tågplanen ingår.

## replacement_trains

Sent anordnade tåg antas ersätta sent inställda tåg. Kvittade inställningar räknas inte som inställda i STM, andel framförda tåg och förseningstid. Använd publicerade mått; beräkna inte STM genom en egen förenklad inställningsformel.

## stm_return

STM pausades från 2023 och återinfördes som huvudmått i årsstatistiken för 2025. Årsutgåvan redovisar även retroaktiva uppgifter för 2023 och 2024; RT finns kvar som kompletterande mått. Detta bekräftar publiceringsinnehåll, inte att alla API-produkter är uppdaterade. Kontrollera aktuell API-täckning eller använd verifierad alternativ publicering.

## publication

Fastställd årsstatistik publiceras cirka två månader efter årets slut, preliminär kvartalsstatistik efter ungefär en månad. Årspubliceringen har mer detaljer. Använd senaste version även för historiska perioder; årspublicering kan revidera kvartalsvärden. Skilj publiceringsfrekvens från tidsupplösning: månadsvärden kan tillgängliggöras i API-produkterna i samband med kvartalspubliceringen. En API-rad för en viss månad är inte belägg för en separat månadsrelease. När användaren frågar efter den senaste statistiken, ange publiceringsperiod och publiceringsdatum; om en månadsrad redovisas, märk den som en månadsuppgift i den kvartalsvisa publiceringen.

## annual_vs_quarter

Års- och kvartalsprodukt betecknar publicering och revisionsstatus, inte exklusiv tidsupplösning. Samtliga fyra API-produkter innehåller ar, kvartal och manad i metadata; årsprodukterna har dessutom tid, veckodag och region/lan. Detta beskriver API:ets möjliga tidsupplösning, inte publiceringens frekvens. Verifiera kombinationer och periodtotaler innan uttag. Aktuell struktur och data validerades 2026-10-23 för `T0604_STM_kv|stm5|ar:2026|manad:09`; API:t accepterade `manad:09` och returnerade en septemberrad i den preliminära kvartalsprodukten. Det är ett konkret API-belägg, inte en separat release.

## geography

Län är ankomstlän för slutstationen enligt kvalitetsdeklarationen. Det är inte förseningsorsakens geografiska plats eller mått för all trafik genom länet. Inga operatörs- eller stationsdetaljer publiceras enligt produktsidan; använd metadata och aktuellt tillåtet urval för län.

## official_statistics

Uppgifter från 2013 ingår i Sveriges officiella statistik. Historisk serie 2001–2012 ingår inte och är inte kvalitetsgranskad; faktisk API-täckning ska kontrolleras.

## planning_break

Trafikverkets nya planeringssystem infördes i samband med tågplan 2023. API-beskrivningarna anger att anordnade och inställda tåg från 2024 inte är jämförbara med tidigare år. Kvalitetsdeklaration 2025 bedömer liten eller ingen påverkan på återställda STM. Överför inte jämförbarhetsbedömningen för STM till alla planeringsmått.

## train_classes

Kort-, medel- och långdistanståg klassas av operatörerna i samråd med Trafikverket efter transportuppgift och tekniska egenskaper. Klasserna är inte enkla kilometerintervall. Ändrad klassning och trafikmix kan påverka läns- och tidsjämförelser.

## aggregation

RT, STM och regularitet är kvoter med olika nämnare. Vid en bred fråga om senaste punktligheten: redovisa i normalfallet både RT(5) och STM(5) för samma period när de finns i API:t. STM(5) är huvudmått för sammanvägd tillförlitlighet; RT(5) kompletterar med punktlighet bland framförda tåg. Säg uttryckligen att RT utesluter inställda tåg ur nämnaren, medan STM utgår från planerade tåg dagen före och beaktar sena inställningar enligt definitionen. Fråga inte användaren att välja mellan måtten när en kort jämförelse svarar på den breda frågan. Om bara ett mått efterfrågas, följ frågans uttryckliga måttval; använd annars STM(5) som huvudmått och nämn kort att RT finns som alternativ.

Ange alltid vald tidsgräns. När användaren vill jämföra andra förseningstoleranser, erbjud de publicerade kumulativa gränserna 0, 2, 5, 10, 15, 30, 45 eller 60 minuter för RT respektive STM, om aktuell struktur tillåter dem. Redovisa inte gränserna som disjunkta förseningsklasser. Summera inte procenttal och använd inte ovägda månads-/kvartalsmedel. Använd publicerad periodtotal eller kompatibla täljare och nämnare över disjunkta grupper. RT × regularitet ger STM med rätt skala och samma population; multiplikation av procenttal kräver division med 100.

## thresholds

ank0, ank2, ank5, ank10, ank15, ank30, ank45 och ank60 samt motsvarande rt/stm är kumulativa tidsgränser, inte disjunkta förseningsklasser. Summera dem inte. Ankomster före tidtabell räknas som enligt tidtabell. Vid en allmän fråga om tillförlitlighet redovisa RT(5) och STM(5) sida vid sida när båda finns; använd STM(5) som huvudmått och definiera båda. Erbjud andra tidsgränser om de är relevanta eller efterfrågas.

## delay_measures

Samma kod som forstim eller genforsamt kan ha olika etikett och population i RT- och STM-produkterna. I STM beräknas sent inställda tågs försening med antagna 30/60/90 minuter för kort-/medel-/långdistans. Beskriv inte detta som observerad faktisk ankomstförsening eller resenärernas totala försening.

## source_roles

Trafikanalys är statistikansvarig och API-källa; Trafikverket är statistikproducent och tillhandahåller uppföljningsdata. Statusmeddelanden om hämtning från api.trafa.se ska fortsatt ange Trafikanalys.

## Källor

- https://www.trafa.se/bantrafik/punktlighet-pa-jarnvag/
- https://www.trafa.se/globalassets/statistik/bantrafik/punktlighet-pa-jarnvag/2026/kvalitetsdeklaration-punktlighet-pa-jarnvag-2025.pdf (publicerad 2026-02-26), avsnitt 1.2, 2.2.6, 2.3, 5 och bilaga 1.
- Sparad struktur för respektive exakt API-Name i produktprofilens metadata_source.
