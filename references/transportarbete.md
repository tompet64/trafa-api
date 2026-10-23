# Trafikarbete och transportarbete

Läs endast avsnittet för aktuell produkt. Granskat 2026-10-11 mot aktuella publikationer och sparad API-metadata. Profiler är delvis granskade; alla urval och metodversioner i API-et är inte verifierade.

Innehåll: [T04010](#t04010--trafikarbete-på-svenska-vägar--modellerade-fordonskilometer), [T04020](#t04020--transportarbete-i-sverige--trafikslagsöversikt), [T04021](#t04021--transportarbete-i-sverige--väg), [T04022](#t04022--transportarbete-i-sverige--bantrafik), [T04023](#t04023--transportarbete-i-sverige--sjöfart), [T04024](#t04024--transportarbete-i-sverige--luftfart).

## Gemensamma skillnader

Trafikarbete är fordonskilometer; persontransportarbete är personkilometer; godstransportarbete är tonkilometer. De får inte adderas eller omvandlas utan nödvändig beläggning/lastinformation. T04020–24 använder miljoner personkm/tonkm. Sammanställningen Transportarbete är inte SOS och överlappar sina primärkällor.

Metod-PM 2025: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf
Produktsida transportarbete: https://www.trafa.se/transportmonster/transportarbete/
Trafikarbetsprodukt: https://www.trafa.se/vagtrafik/trafikarbete/
Aktuellt tabellverk: https://www.trafa.se/globalassets/statistik/trafikarbete/2026/trafikarbete-pa-svenska-vagar---1990-2025---2026-09-21.pdf

## T04010 – Trafikarbete på svenska vägar – modellerade fordonskilometer

Nationell modell för fordonskilometer, inte regional karta över faktisk körning. Produktnamnets ny är en etikett, inte en daterad metodversion.

- Modellen sammanväger trafikförändringar på statligt vägnät med körsträckor från svenskregistrerade fordons besiktningar. Explicit korrigering för svenska fordon utomlands och utländska fordon i Sverige gäller enligt PM lastbilar över 16 tons totalvikt; för övriga antas i praktiken balans mellan trafik över gränsen. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 2.1.)
- Modellen går inte att bryta ned regionalt. Trafikverkets statliga-vägnätsunderlag är en insats i Trafikanalys modell, inte likvärdigt med modellens all-vägsresultat. (Källa: https://www.trafa.se/vagtrafik/trafikarbete/, Statistikens beskrivning.)
- Preliminära uppgifter i april, slutliga senare i september när MC och utländska lastbilar tillkommit. Aktuell tabell är daterad 2026-09-21. (Källa: https://www.trafa.se/vagtrafik/trafikarbete/, Publicerade rapporter.)
- Produktsidan beskriver tillämpning tillbaka till 1990, men tabellverkets utgåva 2026-09-21 anger att nuvarande modell applicerats tillbaka till 2000 och att tidsseriebrott finns mellan 1999 och 2000. Källorna motsäger varandra; bevara båda och uppmärksamma tabellens uttryckliga reservation. (Källa: https://www.trafa.se/globalassets/statistik/trafikarbete/2026/trafikarbete-pa-svenska-vagar---1990-2025---2026-09-21.pdf, Kort om statistiken.)
- Utgåvan 2023-09-22 reviderade trafikarbete 2012–2022 på grund av utvecklad utländsk-lastbilsstatistik. Lastbilar 16,001–26 ton och över 26 ton påverkades; använd senaste serie utan att lägga äldre och nyare serier efter varandra. (Källa: https://www.trafa.se/globalassets/statistik/trafikarbete/2026/trafikarbete-pa-svenska-vagar---1990-2025---2026-09-21.pdf, Kort om statistiken.)

- fordonkm är miljoner km, inte mil eller personkilometer. Personkilometer kräver beläggning och tonkilometer lastvikt; förväxla inte produkterna.
- fslag lastbilsklasser bygger på totalvikt, inte Lastbilstrafiks maxlastvikt. API-etiketter 3,51/16,1 är avrundade jämfört med tabellens 3,501/16,001; använd exakta koder och klarlägg gräns vid detaljfrågor.
- Strukturen innehåller korstr, mkorstr, anttrf, reglan och andra MC-liknande variabler, men den sparade dokumentationen tillåter bara fordonkm|ar respektive fordonkm|ar|fslag. Tolka inte variablerna som en verifierad regional nedbrytning av modellerade fordonskilometer.
- Registreringslän anger inte platsen där ett fordon kör; råa körsträckor ger inte Sverige/utland. Bevara Toms tidigare metodversionsreservation för körsträckor.
- Historiska tomma T0401 ska inte automatiskt ersättas med T04010. Kontrollera period och metod vid jämförelser med 1950–1989 eller 1990–1999.

Öppna frågor:
- Klarlägg motsägelsen om modellens tillämpning före 2000 mellan produktsida och aktuellt tabellverk.
- Varför MC-körsträckevariabler finns i T04010 och deras faktiska kombinationer, population, årstäckning och metodversion; inga körbara urval för dem verifierade.
- Hur ny körsträckemetod påverkar aktuell trafikarbetsmodell och API-version.
- SOS-status för just trafikarbetsprodukten är inte fastställd i de granskade källorna; överför inte transportarbetsproduktens status utan kontroll.

## T04020 – Transportarbete i Sverige – trafikslagsöversikt

Översikt för väg, bantrafik, sjöfart och luftfart; använd T04021–24 för trafikslagets undergrupper. Inte en separat oberoende mätning att addera till delprodukterna.

- Sekundärsammanställning av flera statistikprodukter och modellskattningar; inte klassad som Sveriges officiella statistik. Underliggande källors SOS-status gör inte sammanställningen till SOS. (Källa: https://www.trafa.se/transportmonster/transportarbete/, 1.)
- Utgångspunkten är transportarbete på svensk mark, svenskt territorialvatten och svenskt luftrum. Inrikestransporter räknas dock på hela sträckan även där den går utanför svenskt territorium, exempelvis Gotland. Täckningen och transitbehandlingen varierar per trafikslag. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1.2.)
- Årlig tidsupplösning. Preliminär publicering vid månadsskiftet juni/juli; slutlig på hösten. Produktsidan anger oktober/november, metod-PM slutet av oktober. Kontrollera version och publiceringsplan; äldre år kan revideras. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1; 5.)
- Vägtransporter inkluderar transit för personer och gods. Bantrafik inkluderar godstransit men inte persontransit. Sjöfartstransit och luftfartens överflygningar särredovisas men ingår inte i totalerna. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1.2, tabell 1.2.)

- trfslag:1 Vägtrafik, 2 Bantrafik, 3 Sjöfart, 4 Luftfart. Person- och godstransportarbete är skilda mått; addera dem inte.
- T04020 överlappar T04021–24 och deras primärkällor. Använd trafikslagsöversikten för jämförelser, delprodukterna för avgränsade frågor; kontrollera samma version innan egna andelar beräknas.
- Nya modeller togs fram 2016 och reviderades 2019/2020 med serier från 2000. Äldre 1950–2002-serier är inte jämförbara med dagens serier och uppdateras inte.

Öppna frågor:
- Verifiera överensstämmelse mellan översikt och delprodukter i samma aktuella API-version; inga datajämförelser gjorda i denna granskning.

## T04021 – Transportarbete i Sverige – väg

Sammanställning av modellerat persontransportarbete och godstransportarbete på svenska vägar; bredare än svenskregistrerade tunga lastbilars inrikestrafik.

- Sekundärsammanställning av flera statistikprodukter och modellskattningar; inte klassad som Sveriges officiella statistik. Underliggande källors SOS-status gör inte sammanställningen till SOS. (Källa: https://www.trafa.se/transportmonster/transportarbete/, 1.)
- Utgångspunkten är transportarbete på svensk mark, svenskt territorialvatten och svenskt luftrum. Inrikestransporter räknas dock på hela sträckan även där den går utanför svenskt territorium, exempelvis Gotland. Täckningen och transitbehandlingen varierar per trafikslag. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1.2.)
- Årlig tidsupplösning. Preliminär publicering vid månadsskiftet juni/juli; slutlig på hösten. Produktsidan anger oktober/november, metod-PM slutet av oktober. Kontrollera version och publiceringsplan; äldre år kan revideras. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1; 5.)
- Personbil: trafikarbete gånger RVU-skattad beläggning. Buss: trafikarbete gånger schablonen 10 personer per buss för alla år från 2000, med oklar ursprungskälla enligt PM. MC-beläggning hämtas från personskadeolyckor och är inte säkert representativ. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.1; 8.1.)
- Moped, cykel och gång beräknas med reslängd per person och befolkning 6–84 år folkbokförd i Sverige. Yngre/äldre och personer bosatta utomlands saknas. Mopedsträckan är en äldre konstant 17 km per person och år, inte en årlig observation. RVU-metodändringen 2019 ger brott för bil, cykel och gång. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 2.2; 3.1.)
- Persontransportarbete i lätta lastbilar beräknas endast för privatägda fordon med bilarnas beläggning. Godstransportarbete omfattar både privat- och företagsägda lätta lastbilar med schablonlast 84 kg över alla km inklusive tomkörning från norska undersökningar; samma faktor från 2000. Svensk undersökning 2022 är enligt PM ännu inte införd i modellen. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.1; 4.1.)
- Väggodstotalen omfattar svenska tunga lastbilars inrikes transporter, 44 procent av deras utrikes transportarbete från start till mål, utländska tunga lastbilars till/från-, cabotage- och transittransporter på svensk mark samt lätta lastbilar. 0,44 är en metodschablon, inte ett generellt filter på enskilda transporter. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 4.1.)
- Vid preliminär publicering skattas senaste årets utländska lastbilars transportarbete med linjär extrapolation och fördelning med senaste fem årens genomsnittsandelar. Höstpublicering tillför dessa uppgifter och reviderat trafikarbete. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 5.)
- Godstransporter med tunga lastbilar vars maxlastvikt understiger 3,5 ton samt andra färdsätt som cykelbud, moped och bussgods täcks inte fullständigt. Målet om alla kommersiella transporter är inte samma som faktisk täckning. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 4.1.)

- trpsatt och nation/riktning/intra är olika urvalsvägar; validera hela kombinationen. nation avser tunga lastbilars registreringsnationalitet, inte förarens medborgarskap.
- Dokumentationens nation|nation är en upprepad variabel i vissa kombinationsrader. Bevara rålistan men kopiera inte upprepningen blint; kontrollera aktuell struktur och avsedd hierarki.
- T10061/T10062 inkluderar svenskregistrerade lastbilars utrikestransporters hela körning; deras råa total är inte automatiskt transportarbetet på svensk mark. T0301 och körsträckestatistik är överlappande underlag, inte ytterligare volymer.
- trpsatt:24 Bussgods finns i domänen men innebär inte att aktuella eller fullständiga data finns.
- Ingen KI-dimension är observerad i sammanställningen. Överför inte KI från en enskild komponent till den sammansatta totalen.

Öppna frågor:
- Faktisk årstäckning för bussgods och andra metadataalternativ.
- Vilka metodversioner och omräknade 2016–2018-serier används i aktuellt API efter RVU-brottet 2019?
- Metod-PM beskriver RVU både som folkbokförda och på ett ställe som svenska medborgare; anta inte ett medborgarskapskrav utan kontroll.
- När ny körsträckemetod faktiskt införs i API och sammanställning; framtida förbättring i PM är inte införandebevis.

## T04022 – Transportarbete i Sverige – bantrafik

Sekundärredovisning från Bantrafik av järnväg, tunnelbana och spårväg, med anpassad godsvikt för kombigods.

- Sekundärsammanställning av flera statistikprodukter och modellskattningar; inte klassad som Sveriges officiella statistik. Underliggande källors SOS-status gör inte sammanställningen till SOS. (Källa: https://www.trafa.se/transportmonster/transportarbete/, 1.)
- Utgångspunkten är transportarbete på svensk mark, svenskt territorialvatten och svenskt luftrum. Inrikestransporter räknas dock på hela sträckan även där den går utanför svenskt territorium, exempelvis Gotland. Täckningen och transitbehandlingen varierar per trafikslag. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1.2.)
- Årlig tidsupplösning. Preliminär publicering vid månadsskiftet juni/juli; slutlig på hösten. Produktsidan anger oktober/november, metod-PM slutet av oktober. Kontrollera version och publiceringsplan; äldre år kan revideras. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1; 5.)
- Personer: järnväg, tunnelbana och spårväg på svenska banor, inrikes och svensk del av utrikes; ingen persontransit, ombordpersonal, museitrafik, militär trafik eller trafik utan intäkter. Gods: järnväg, inklusive transit, men inte intern verksamhet eller anläggnings-/underhållstransporter. Transit Norge–Norge genom Sverige saknas före 2009. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.2; 4.2.)
- Kombigodsets lastbärarvikt exkluderas genom modellberäkning för jämförbarhet mellan trafikslag. Bantrafik innehåller både med och utan lastbärare; välj motsvarande serie. Ungefärlig minskning 20–30 procent i PM är inte en generell omräkningsfaktor. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 4.2.)

- trpsatt:21 järnväg, 22 tunnelbana, 23 spårväg. Godstransportarbete redovisas endast för järnväg, inte automatiskt samma färdsättstäckning som personmåttet.
- lasttyp:1 vagnslastgods, 2 malm på Malmbanan, 3 kombigods; bekräfta kategoriernas additivitet och lastbärardefinition.
- riktning är H med riktningh och riktningu; riktningu:11 Regionalt är en underkategori, inte hela bantrafiken. Bevara parentrelationerna.
- För frågor främst om spårväg/tunnelbana är T1203 relevant publiceringsprodukt; enligt statistikansvariges besked är Bantrafik och Järnvägstransporter den huvudsakliga källan och uppgifterna används även i T1203. T04022 kan vara sammanställning/komplement. Addera inte T1203, T06013 och T04022 för samma transporter.

Öppna frågor:
- Exakt avgränsning av API-underkategorin Regionalt och faktisk årstäckning; inte automatiskt lika med RKM-regi.
- Verifiera jämförbar godsserie utan lastbärarvikt och aktuella tidsseriebrott i Bantrafik.

## T04023 – Transportarbete i Sverige – sjöfart

Havsgående transporter från Sjötrafik, passagerartransportarbete i skärgårdstrafik från Regional linjetrafik samt separat transitredovisning.

- Sekundärsammanställning av flera statistikprodukter och modellskattningar; inte klassad som Sveriges officiella statistik. Underliggande källors SOS-status gör inte sammanställningen till SOS. (Källa: https://www.trafa.se/transportmonster/transportarbete/, 1.)
- Utgångspunkten är transportarbete på svensk mark, svenskt territorialvatten och svenskt luftrum. Inrikestransporter räknas dock på hela sträckan även där den går utanför svenskt territorium, exempelvis Gotland. Täckningen och transitbehandlingen varierar per trafikslag. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1.2.)
- Årlig tidsupplösning. Preliminär publicering vid månadsskiftet juni/juli; slutlig på hösten. Produktsidan anger oktober/november, metod-PM slutet av oktober. Kontrollera version och publiceringsplan; äldre år kan revideras. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1; 5.)
- Inrikes transportarbete avser hela hamn-till-hamn-sträckan även utanför svenskt territorialvatten. Utrikes avser endast svensk territorialvattensträcka. AIS-baserad distansmatris från 2018 har använts för att revidera 2015–2017; vissa saknade avstånd skattas. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.3; 4.3.)
- Eurostats sjötransit beräknas i svensk exklusiv ekonomisk zon (EEZ), som är vidare än territorialvattnet. Transit särredovisas från 2023 års publikation, med eftersläpning, och ingår inte i totalen. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.3; 4.3.)
- Persontransportarbetet består av havsgående sjötrafik och skärgårdstrafik inklusive viss hamntrafik, den senare från Regional linjetrafik. Fritidsbåtar och Trafikverkets vägfärjor ingår inte; vissa kommunala entreprenadvägfärjor i Stockholm, Jönköping och Skåne ingår enligt fotnot. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.3.)
- Kryssningspassagerare ingår från undersökningsår 2020 med jämförbara tidsserier från 2015. Havsgående fartyg kan trafikera inre vattenvägar; separat inre-vattenvägsserie är inte automatiskt disjunkt med havsgående serien. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.3; 4.3.)

- riktningh:1 inrikes, 2 utrikes, 3 transit. Addera inte transit till publicerad total om svaret ska följa produktens totaldefinition.
- riktningu:21 till utlandet, 22 från utlandet, 26 havsgående, 27 skärgård, 28 inre vattenvägar. Valbarhet och överlapp måste kontrolleras mot överordnad kategori.
- T0802 och T1203 är underlag med olika populationer; totalen i T04023 är inte identisk med något av dem ensamt.
- Godstransportarbete avser godsvikt gånger avstånd, exklusive lastbärarvikt; det är inte hamnarnas lastade/lossade ton summerade över båda ändar.

Öppna frågor:
- Aktuella referensår och API-version för transitserier med eftersläpning.
- Exakt hantering av inre vattenvägar i varje API-total; inga disjunkta uttag för summering verifierade.

## T04024 – Transportarbete i Sverige – luftfart

Sekundärredovisning av Luftfarts passagerar- och godsarbete med separat överflygningsserie.

- Sekundärsammanställning av flera statistikprodukter och modellskattningar; inte klassad som Sveriges officiella statistik. Underliggande källors SOS-status gör inte sammanställningen till SOS. (Källa: https://www.trafa.se/transportmonster/transportarbete/, 1.)
- Utgångspunkten är transportarbete på svensk mark, svenskt territorialvatten och svenskt luftrum. Inrikestransporter räknas dock på hela sträckan även där den går utanför svenskt territorium, exempelvis Gotland. Täckningen och transitbehandlingen varierar per trafikslag. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1.2.)
- Årlig tidsupplösning. Preliminär publicering vid månadsskiftet juni/juli; slutlig på hösten. Produktsidan anger oktober/november, metod-PM slutet av oktober. Kontrollera version och publiceringsplan; äldre år kan revideras. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 1; 5.)
- Inrikes omfattar hela avståndet mellan svenska flygplatser även utanför svenskt luftrum, utrikes endast svensk-luftrumsdelen. Storcirkelavstånd och Eurostatmatriser används; saknade avstånd imputeras. Det är inte den faktiskt flugna rutten för varje resa. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.4; 4.4.)
- Överflygningar särredovisas från 2019 års publikation, bygger på Eurostat med eftersläpning och ingår inte i ordinarie total. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 3.4; 4.4.)
- Frakt och post inklusive bellyfrakt men exklusive passagerarbagage och lastbärarvikt. Truckad flygfrakt som körs på väg räknas inte som lufttransportarbete. Statliga flygplatsers flygfrakt saknas 2019 och årets värden har imputerats som medelvärde av 2018/2020. (Källa: https://www.trafa.se/globalassets/statistik/transportarbete/2025/transportarbete-i-sverige-2000-2025---metod-pm.pdf, 4.4.)
- API-måtten ptrparb/gtrparb anger omräkning för 2006–2018 för att inkludera taxiflyg; märk reviderad tidsserie och använd inte äldre publicering utan versionskontroll. (Källa: https://www.trafa.se/sidor/api-dokumentation/?code=T04024, API-measure descriptions.)

- riktning:1 inrikes, 2 utrikes, 3 överflygningar; t1 total. Överflygningar får inte läggas ovanpå t1 som om de redan ingick i samma totaldefinition.
- Skilj flygfraktens ton från tonkilometer och resor/passagerare från personkilometer; omräkning mellan enheter ersätter inte ett saknat avstånd.
- T0501 Luftfart är källa och överlappar denna produkt. Kontrollera skala: T04024 miljoner, medan Luftfarts arbetsmått enligt sparad metadata anges i tusental.

Öppna frågor:
- Verifiera att aktuellt API använder de dokumenterade imputerade 2019-värdena och reviderade taxiflygserierna.
- Aktuella referensår för Eurostats överflygningar och hur totalerna representeras i API-et.
