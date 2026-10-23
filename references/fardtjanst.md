# Färdtjänst och riksfärdtjänst – T1201

Delvis granskad mot aktuell produktsida, kvalitetsdeklaration 2025 och sparad API-metadata. Konkret uttag kräver slutvalidering.

## scope

Kommunernas verksamhet med färdtjänst och riksfärdtjänst i Sverige. Totalundersökning av samtliga 290 kommuner, uppgifter från kommuner/RKM och i vissa fall Riksfärdtjänsten Sverige AB. Inte all taxitrafik, all anropsstyrd kollektivtrafik eller allt resande bland personer med funktionsnedsättning.

## reference_period

Antal personer med färdtjänsttillstånd avser bestånd den 31 december. Antal nyttjare och antal enkelresor avser kalenderåret. Skilj tillståndsinnehavare vid årsslut från nytillkomna/beviljade tillstånd under året; summera inte bestånd över år.

## utilization

andelnyttjatftillst jämför årets antal nyttjare med antalet tillståndsinnehavare den 31 december. Andelen kan överstiga 100 procent utan rapporteringsfel på grund av olika referenstider. Klipp inte värden till 100 och anta inte att samtliga årets nyttjare hade tillstånd vid årets slut.

## ratios

antresppftillst avser enkelresor per person med färdtjänsttillstånd, inte per person som faktiskt reste. antresppnyttjatrf avser enkelresor per person som nyttjade riksfärdtjänst. Skilj nämnare och använd publicerade kvoter; summera inte andelar eller kvoter och använd inte ovägda kommunmedel.

## population_denominator

Per-invånarmåtten använder årets medelbefolkning enligt kvalitetsdeklarationen 2025. Överför inte novemberbefolkningen från fordons-/körkortsstatistik eller anta befolkning enbart den 31 december. Vid egna åldersuppdelade beräkningar behöver exakt medelbefolkningsformel och åldersanknytning kontrolleras.

## trips_people

antresf och antresrf är enkelresor, inte tur-och-returresor eller antal resenärer. antpnyttjatf och antpnyttjatrf är nyttjande personer i respektive tjänst. Samma person kan nyttja båda; summera inte till unika personer utan hantering av överlapp.

## geography

Kommun, län och riket; kommunuppgifter aggregeras till län/riket. Statistiken beskriver kommunernas verksamhet och är inte en OD-matris eller uppgift om alla resor som geografiskt utförs inom området. Kontrollera redovisningsanknytning vid frågor om var resorna går.

## age

Kvalitetsdeklarationen anger åldersklasser 0–19, 20–44, 45–64, 65–79 och 80+. API har hierarkin alder och två nivåer aldergrp1/aldergrp2; bevara relationerna och verifiera aktuella värden. Utgå inte från enskilda åldrar eller att båda grupperingsnivåer kan summeras tillsammans.

## coverage_units

API har antal personer, antal enkelresor, resor per person, nyttjandegrad samt personmått per 1 000 invånare. Etiketter för absoluta antal anger inte tusental; kontrollera faktisk svarsenhet. Per 1 000 och procent är olika skalor. Kommun/län kan sakna valbara kombinationer trots global metadata.

## quality

Totalundersökning innebär inte att uppgifterna är felfria. Uppgifter om nyttjande kan saknas från utförare och imputeras; mätfel och bortfall ska beaktas. Ange inte osäkerheten som ett KI om inget sådant redovisas.

## comparability

Enkelresor könsuppdelas från 2014. Lokala/regionala organisatoriska förändringar kan ändra vad som redovisas som färdtjänst respektive riksfärdtjänst, exempelvis länsfärdtjänst. Stora förändringar kan bero på ändrad avgränsning snarare än ändrat faktiskt resande. Senaste kvalitetsdeklaration/fotnoter ska kontrolleras.

## publication

Årlig publicering i juni. Sveriges officiella statistik från och med referensår 2007, inte automatiskt för tidigare år. Produktsidan anger en korrigering 2023-06-16 av 2021 års uppgifter för 28 kommuner; använd rättad version vid sådana jämförelser.

## Källor

- https://www.trafa.se/kollektivtrafik/fardtjanst/ (läst 2026-10-11).
- https://www.trafa.se/globalassets/statistik/kollektivtrafik/fardtjanst/2025/kvalitetsdeklaration-fardtjanst-och-riksfardtjanst-2025.pdf (2026-06-18, läst 2026-10-11), avsnitt 1.2, 2.2.3 och 5.1.
- Struktur t1201, 2026-10-09.
