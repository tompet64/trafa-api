# Kommersiell linjetrafik på vatten – T1204

Delvis granskad mot produktsida, kvalitetsdeklaration Regional linjetrafik 2025 och sparad API-metadata; granskad 2026-10-11. Konkret uttag kräver slutvalidering.

## scope

Kommersiell tidtabellbunden persontrafik på vatten i egen regi, utan offentlig trafikreglerande avtalsrelation. Charter och icke linjelagd beställningstrafik ingår inte. Kvalitetsdeklarationen för Regional linjetrafik beskriver denna insamling som regional kommersiell trafik i Sverige; den ska inte beskrivas som all passagerarsjöfart.

## overlap

Undersökningen är en del av Regional linjetrafik, med separat tabellverk och API-kod T1204. Samma regionala kommersiella trafik ingår i T1203. Summera inte T1204 med T1203:s motsvarande del eller total.

## sjotrafik_boundary

Skilj regional vattenkollektivtrafik från hamnanknuten Sjötrafik T0802/T08021, som har annan population och undantag för regional linjetrafik/skärgårdstrafik. En bred fråga om båtar eller färjor kräver avgränsning till regional/interregional/utrikes och finansiering; anta inte att produkterna tillsammans ger ett komplett disjunkt total.

## boarding_capacity

pastig har etiketten Ombordstigningar, tusental: inte unika personer. utbudskm avser fartygskilometer och personkm passagerarnas sammanlagda reslängd. sittkm har etiketten Platskilometer; för vatten räknas högsta tillåtna passagerarantal inklusive sitt- och ståplatser gånger distans. Tolka inte sittkm som endast sittplatser.

## metadata

Sparad struktur innehåller trafiktyp:1 Regional, 2 Interregional och t1 Totalt, samt konkreta år 2022–2025. Att Interregional finns i värdemängden bevisar inte tillgängliga observationer eller att dokumentationens regionala population utvidgats. Kontrollera aktuell struktur och data för efterfrågat urval; beteckna täckningen som oklar tills förklarad.

## units

Fyra API-mått: pastig, utbudskm, personkm och sittkm, med etiketter i tusental. Ingen geografi utöver trafiktyp, inga ekonomimått eller planerade utbudsmått finns i sparad produktmetadata. Överför inte sådana mått från T1202 eller T1203 som om de fanns här. Kontrollera aktuell enhet och skala innan omräkning.

## frame

Företag/organisationer med regional kommersiell tidtabellbunden vattenpersontrafik, även del av året. Samtrafikens gemensamma tidtabellsdatabas utgör underlag för målpopulationen. Överför inte vägproduktens krav på minst 200 mil utan produktspecifikt belägg.

## quality

Kvalitetsdokumentationen ingår i Regional linjetrafik och är inte en separat kvalitetsdeklaration för API-koden. Deklarationen 2025 anger uttryckligen att ingen imputering skett i årets vattenmätning, även om en imputeringsmetod beskrivs. Påstå inte att årets värden korrigerats med 0,9 eller 33 procent utifrån metodbeskrivningen.

## history

Produktsidan anger första särredovisningen i juni 2023 men innehåller även äldre pilot-/publikationsmaterial. Insamling har historik före de år som syns i API-metadata. Anta inte att statistik saknas före 2022 eller att pilot, äldre insamling och aktuell serie är direkt jämförbara.

## publication

Årlig publicering i anslutning till Regional linjetrafik i juni. Behåll kalenderår och faktiska tillgängliga perioder; senaste publikation för äldre uppgifter enligt gemensamma revisionsinstruktioner. Kontrollera aktuell publicering om API-et är ofullständigt.

## Källor

- https://www.trafa.se/kollektivtrafik/linjetrafik-pa-vatten/
- https://www.trafa.se/globalassets/statistik/kollektivtrafik/kollektivtrafik/2025/kvalitetsdeklaration-regional-linjetrafik-2025.pdf (2026-06-26), avsnitt 1.2.4 och 2.2.6 samt bilaga 9. Populationsavsnittet innehåller årtalet 2024 trots utgåva 2025; använd inte det som API-täckningsgräns.
- T0802/T08021:s granskade profil: references/sjotrafik.md.
- Struktur t1204, 2026-10-09.

## Sakkomplettering: interregional kategori

Interregional finns i T1204 analogt med indelningen i T1202 enligt Toms sakuppgift. Möjliga förklaringar till begränsad redovisning är att trafiken är ovanlig eller att antalet utförare är för litet för redovisning av sekretesskäl; dessa orsaker är inte fastställda. Skilj kategorins existens från observationernas täckning och redovisningsstatus. Ett tomt eller saknat värde innebär inte noll och får inte automatiskt betecknas som sekretessbelagt.

Källa: Tom, sakkomplettering 2026-10-11. Analogin är sakuppgift; förklaringarna om låg förekomst och sekretess är uttryckligen möjliga orsaker.
