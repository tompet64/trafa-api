---
name: trafa-api
description: Lös statistikfrågor och metadataarbete med Trafikanalys API (api.trafa.se). Använd för produkt- och variabelidentifiering, tillåtna API-kombinationer, värdemängder, filtrerade statistikuttagsfrågor, komprimerade kataloger och säker uppdelning av stora hämtningar. Bevara källkoder, kontrollera urval och återanvänd samma metod mellan statistikprodukter.
---

# Trafikanalys API

## Använd kontraktet och välj metadataväg

- Använd [references/openapi-trafa.json](references/openapi-trafa.json), OpenAPI 3.1.0 och kontraktsversion 2.1.0, som gemensam teknisk grund. Pythonklienten läser server, operationer och parametrar ur kontraktet och kontrollerar JSON-svar mot dess schema. Vid en installerad API-anslutning, matcha de faktiskt tillgängliga verktygen mot kontraktet. En kontraktsfil registrerar ingen Action och ger inga nätverksbehörigheter.
- Sök först i produktprofilerna och `references/metadata/` efter produkt, exakta koder, relevanta värden och dokumenterade kombinationer. Välj sedan **aktuell struktur** eller **daterade referenser** för slutvalidering enligt [references/metadata-routing.md](references/metadata-routing.md). Båda vägarna kräver kontroll före datahämtning; redovisa vilken som användes.
- Tillämpa den valda anslutningens storleksgräns. Direkt Python har ingen förinställd gräns på 100 000 tecken. För en anslutning med begränsad svarsstorlek, använd känd storlek och en uttrycklig budget för att undvika redan kända för stora strukturanrop. `structure_sizes.json` innehåller källbelagda fullproduktmätningar för 56 giltiga produkter från 2026-10-09: 14 över 100 000 och 16 över 80 000 tecken. T0401:s tomma historiska svar är uteslutet. Avsaknad av relevant mätning betyder okänd storlek.
- Om strukturen överskrider budgeten, använd fullständigt referensstöd för exakt produkt, variabler, värdekoder, föräldrar och en dokumenterad kombination. Stoppa om stödet saknas. Referenser bekräftar inte dagens `Selected`, `Option`, `DataCount` eller datatäckning. Låt inte nätverksfel, behörighetsavslag, syntaxfel eller API-fel utlösa automatisk referensfallback.
- Bevara portabiliteten: använd tillgänglig Action/API-anslutning eller den fristående Pythonklienten. Färdighetens statistiklogik kräver inte Work, en viss klientenhet eller `trafapy`. Följ miljöns behörighetsregler enligt [references/api-method.md](references/api-method.md).

## Skriv källtrogna statusmeddelanden

- Tillämpa samma källkrav på framstegsmeddelanden och egenformulerade verktygsrubriker som på slutsvaret. Benämn `api.trafa.se` och `trafa.se` som Trafikanalys. Skriv Trafikverket endast när en faktisk källa från Trafikverket används; skilj statistikleverantör från eventuell ursprunglig uppgiftslämnare.
- Översätt variabelkoder med aktuell produkts metadata, aldrig genom ordlikhet eller gissning. I Sjötrafik `t0802` betyder `aland` Avgångsland, inte Åland; `aland:118` avser Finland, verifierat 2026-10-07. Överför inte denna betydelse till andra produkter: i Lastbilstrafik `t10061` betyder `aland` Avlastningsland.
- Beskriv pågående handling och dess verifieringsläge. Skriv exempelvis ”Kontrollerar avgångsland och riktning i Trafikanalys API” före validering och ”Hämtar passageraruppgifter från Finland till Sverige” först när urvalet är verifierat. Vid osäker etikett, skriv neutralt ”Kontrollerar urvalets metadata”.
- Påstå inte att ett resultat har hämtats innan svaret har kontrollerats. Gör inte en bred varugrupp snävare i statusen: behåll exempelvis ”Malm och andra produkter från utvinning”.
- Rätta felaktiga statusuppgifter uttryckligen om de upptäcks. Om användaren rapporterar en etikett som inte syns i tillgänglig logg, skilj vad loggen visar från vad användaren såg; förneka inte observationen. Lova inte kontroll över automatiskt genererade gränssnittsetiketter och fastslå inte deras tekniska ursprung utan belägg.

## Fastställ statistikfrågan

Precisera mått, population, geografi, period, frekvens, enhet och önskad redovisning. Skilj resor från resenärer, ton från tonkilometer, flöden från bestånd och registreringar från fordon i trafik. Fråga bara om oklarheten påverkar produktval eller resultat; fortsätt annars med tydligt angivet antagande. Använd en publicerad total när den besvarar frågan.

## Minimera arbetet före första anropet

- Tolka aldrig årens ordning i dokumentation, metadata eller svar som kronologisk. Välj första/sista tillgängliga år genom numeriskt min/max av konkreta årskoder i relevant urval; välj önskade år med exakta koder. Behåll luckor och originalkoder. Skilj dynamiska filter som senaste/forra och totaler från konkreta år. Sortera tidsserier kronologiskt efter år och eventuell månad/kvartal före presentation eller tidsberäkning. Tillgängliga år i ett filtrerat struktur-svar gäller det urvalet, inte automatiskt hela produkten.
- Bestäm vilka observationer och beräkningar svaret faktiskt behöver. Vid jämförelse mellan två tidpunkter, hämta endast start- och slutperiod. Hämta mellanperioder bara för efterfrågad tidsserie, trend, variation, periodsumma eller annan beräkning som kräver dem. Vid allmän ”förändring mellan år A och B”, välj ändpunkter och ange detta kort; kalla inte två punkter en trendanalys.
- Begränsa även mått, geografi och kategorier till svaret och nödvändiga kontroller. Behåll rätt nämnare för andelar. Skapa inte extra diagram, arkiv eller kataloger om de inte efterfrågas eller behövs för leveransen. En demonstration ska också vara proportionerlig; aktivera inte varje villkorad gren för att visa den.
- Ett tomt datauttag är inte bevis för att uppgiften saknas i produkten. Selected/Option anger urvalsstatus och valbarhet, inte datatäckning; kontrollera även DataCount och Rows. Innan byte till webbtabeller, annan leverantör eller kvartalssummering: läs produktens relevanta kombinationer och pröva en semantiskt motsvarande dokumenterad urvalsväg, om sådan finns. Begränsa felsökningen till motiverade alternativ och redovisa vilket urval som var tomt. Välj verifierad årsuppgift för helårsfrågor. Vid Sjötrafik från Finland: läs det konkreta fallet i references/sjotrafik.md.
- Återanvänd giltiga svar och metadata från pågående arbete. Cachelagra efter endpoint, exakt query, språk och format med hämtningstid. Läs bara relevanta utdrag i kontext. Hämta inte samma svar igen utan konkret skäl, såsom ändrat urval, revisionsrisk eller begärd uppdatering. Skilj sakprofiler från daterad, maskinellt verifierbar referensmetadata. Använd vald metadataväg för slutvalidering och redovisa aktualiteten.
- Använd fungerande API-klient direkt. Undvik parallella webbsökningar efter samma API-innehåll. Använd webbsökning för saknad dokumentation eller definitioner. Kör oberoende nödvändiga läsningar samlat, högst tre samtidiga HTTP-anrop; håll beroende urvalssteg sekventiella.

## Välj en kort, spårbar arbetsgång

- Läs bara det som behövs: `metadata_lookup.py --product t1203 --variables pastig finans traslag --values` visar valda variabler utan hela berikningen; `--section combinations --variables pastig finans traslag` visar relevanta kombinationsrader; `--section profile` visar sakprofilen. Standard utan sektion är en kort översikt. Använd `--section all` bara när hela profilen faktiskt behövs. Kör inte rutinmässigt hjälpkommandon eller filinventeringar när sökvägar och syntax är kända.
- Läs dokumenterade kombinationer före första oprövade uttaget. En kombinationsrad kan lista flera tillgängliga mått; tolka den inte som krav att hämta alla. Behåll behövliga dimensioner, välj bara nödvändiga mått och slutvalidera. När användaren ber om alla kategorier av en variabel, ta med variabeln som redovisningsdimension men utelämna dess värdefilter. Kontrollera för varje uttag att variabeln är en dimension och att kombinationen med mått, tid och övriga urval är tillåten i den aktuella strukturen eller styrkt av fullständig dokumentation; någon förhandsgranskning av alla produkter behövs inte. Exempel: `t10030|nyreg|ar:2025|fslag` redovisade åtta fordonskategorier utan värdefilter 2026-10-23. Bedöm att hela kategorimängden ryms inom svarstaket; om inte, använd en fullständig, kontrollerad kodlista eller partitionera med täckningskontroll. Ett uttag med ofiltrerad dimension redovisar kategorirader, inte automatiskt en total. Om den aktiva anslutningen bara stöder värdefilter och saknar sätt att inkludera en dimension utan värdefilter, använd en tillgänglig direktklient; annars redovisa begränsningen. Utelämna inte dimensionen, skicka inte en tom filterlista och kalla inte en summering av en ofullständig kategorilista för API:ets total.
- Kör ett känt sluturval direkt med `scripts/trafa_client.py extract --query 'EXAKT_QUERY' --raw /tmp/uttag.json --rows 10`. Klienten väljer metadataväg, validerar före data och sparar valideringskvitto samt begäransloggar för gjorda HTTP-anrop. Ange `--structure-max-chars 80000` endast när den aktuella anslutningens budget motiverar det; använd `--metadata-source references` för en uttrycklig referensväg. Inspektera beslut utan nätverk med `plan --query 'EXAKT_QUERY'` och samma tillval. Vid aktuell DataCount 0 görs inget dataanrop; referensvägens okända DataCount är inte noll. Kontrollera sample_complete; ett stickprov är inte hela uttaget när detta är false. Läs [references/urvalsarbete.md](references/urvalsarbete.md) för exempel och gränser.
- Vid tomma/saknade värden: kontrollera tabellens obligatoriska redovisningsdimensioner, population och explicit relevant total/delgrupp. Gör inte upprepade gissningar. Högst två ytterligare dokumenterade alternativ i normalfallet; fortsätt bara om ny konkret evidens motiverar det. Beskriv annars det exakta uttagsproblemet och använd rätt alternativ publicering. Förklara inte en saknad totalsrad som att alla delgrupper saknar uppgifter.
- Använd Trafikanalys egna källor för definitioner och täckningsfrågor. Kontrollera lagrad källas relevans och edition först; gör en riktad uppdatering om årgång eller ändringssignal kräver det. Gör ingen bred sökning på bransch- och nyhetssidor för att fastställa vad API-et innehåller. Begränsa ett negativt besked till den kanal och det urval som faktiskt kontrollerats.
- Svara först på användarens faktiska fråga. Om den inte kan besvaras med underlaget, säg det först. Ett närliggande mått kan ges som tydligt märkt komplettering om det hjälper; hämta inte jämförelsetal enbart för att fylla svaret. För överlappande behörigheter A/B besvarar summan inte unionen; redovisa inte den som huvudsvaret på andel med minst en behörighet.
- Knyt slutsvaret till de använda raderna: filter, återstående redovisningskategorier, mått, period, skala, total/delgrupp och eventuellt KI-par. Om en dimension lämnats ofiltrerad ska det framgå vilka rader som används. Läs definition och källa; olika etiketter är inte bevis för olika statistiska begrepp. För spårväg/tunnelbana överlappar Bantrafiks resor och T1203:s påstigningar; anta inte samma likvärdighet för järnväg eller RVU.

## Identifiera med metadata och struktur

Använd först `scripts/metadata_lookup.py --search "ämne"` eller `--product t10026 --variables reglan --values`. Katalogerna i `references/metadata/` innehåller verifierade API-koder, typer, föräldrar och värdemängder från 2026-10-09 för 56 då aktuella statistikprodukter. Använd dem för sökning och, när villkoren i metadata-routing.md är uppfyllda, daterad referensvalidering. Ett vanligt sökresultat är inget valideringskvitto. Läs inte hela katalogerna i kontext. T0401 är historisk och saknas i den då verifierade produktlistan; ersätt den inte automatiskt med T04010. T10020 har kompletterats med dokumentation och 24 kombinationsrader 2026-10-09. Läs [references/fordon-lan-kommun.md](references/fordon-lan-kommun.md) för sakgranskad produktroll, adressanknytning och perioddefinitioner; använd `references/metadata/T10020-documentation.json` för dokumentationsdetaljer.

Behandla produktlistans ordning som inläggningsordning, inte som tematisk klassifikation, prioritet eller produktens ålder. Använd `scripts/metadata_lookup.py --list` för en separat redaktionell ämnesöversikt. Grupperna i `references/metadata/produktgrupper_visning.json` är navigeringshjälp, inte officiell API-taxonomi eller belägg för produkters utbytbarhet.

1. Sök befintligt metadataunderlag efter ämne, benämning och synonymer. Kontrollera källa, verifieringsdatum och fullständighet. Välj metadataväg innan ett strukturanrop och skilj referensstöd från aktuell API-verifiering.
2. Hämta produktlistan från `/api/structure` endast om rätt produkt inte redan identifierats i tillgänglig metadata eller en verifierad produktprofil. Jämför kandidater med samma titel mot population, periodicitet, mått och geografi. Välj inte efter titel ensam eller antagen betydelse av produktkod.
3. Använd relevanta delar av den sparade strukturen eller referenskatalogen. Hämta ett exakt struktururval när den vägen är vald; undvik rutinmässig hämtning av hela produktstrukturen. Följ nästlade poster och föräldrar och använd exakt `Name` som kod. Använd inte etikett eller internt `Id` som anropskod. Bevara skiftläge och inledande nollor.
4. Skilj P (produkt), D (dimension), M (mätvärde), H (hierarki) och DV (dimensionvärde). Bevara föräldrarelationer. Tolka inte en hierarki som ett fritt utbytbart filter.
5. Kontrollera tillåtna kombinationer i produktdokumentationen och återanvänd relevant underlag. För en tidigare belagd kombination med kända värdekoder, gå direkt till vald slutvalidering. Vid aktuell struktur, kontrollera `Selected` och `Option` för valda variabler och filtervärden. Vid referensvalidering, kräv att måtten uttryckligen ingår i en enda dokumenterad kombinationsrad och att dess dimensioner överensstämmer med urvalet. Global förekomst eller en sakprofil ensam räcker inte.
6. Validera hela sluturvalet före datahämtning. Stoppa vid motsägelse mellan aktuell struktur och referenser; använd aldrig referensvägen för att köra över ett negativt aktuellt besked. Stoppa också vid otillräckligt referensstöd, okända värden eller dynamiska filter som inte kontrollerats aktuellt. Undersök separata tillåtna uttag vid behov; konstruera inte en korsklassificering genom att sammanfoga marginaltabeller.

Läs [references/fordon-bakgrund.md](references/fordon-bakgrund.md) vid fordonsbestånd, registreringar och T10012 Körkort: registeravgränsning, totalvikt kontra maxlastvikt, preliminära månadsavregistreringar, statistiskt ägande och drivmedel. Läs [references/korstrackor.md](references/korstrackor.md) vid T10091–94. Skilj ny metod i publikationen från dess ej verifierade införande i API-et; antag inte en formel för gdkor.

Läs [references/personbilar-produkter.md](references/personbilar-produkter.md) för att skilja regional årsstatistik, detaljerad årsstatistik och månadsstatistik för personbilar. Använd [references/personbilar-lan.md](references/personbilar-lan.md) som verifierad sökhjälp för personbilsbestånd per län och drivmedel.

Läs [references/bantrafik.md](references/bantrafik.md) vid T06011, T06012, T06013 och T0603 för trafikslagsavgränsning, år/kvartal, rullande mått, enheter och metodförändringar.

Läs [references/sjofartsforetag.md](references/sjofartsforetag.md) vid T08091 och T08092 för historisk företagsstatistik, upphörd undersökning, SCB-hänvisning samt skillnader i valuta och landtäckning.

Läs [references/fartyg.md](references/fartyg.md) vid T0808 för flottans population, svensk regi kontra registrering, källornas uppdateringsluckor och tidsseriebrott.

Läs [references/sjotrafik.md](references/sjotrafik.md) vid T0802 och T08021: hamnanknuten population, undantag för transit och skärgårdstrafik, inre vattenvägar, sekretess, måttskillnader och revisioner.

Läs [references/lastbilstrafik.md](references/lastbilstrafik.md) vid T10061, T10062 och T0301. T0301 är en separat sammanställning med ofullständig landtäckning och utan redovisade KI; överför inte svenska undersökningens KI-regler till den. T10061 och T10062 är urvalsundersökningar: hämta och redovisa varje punktskattning med dess tillhörande KI i samma urval och period. KI är enligt sakgranskad definition halva bredden av det tvåsidiga 95-procentiga intervallet: redovisa skattning ± KI eller motsvarande gränser. Omräkna båda med samma enhetsfaktor.

Läs [references/api-method.md](references/api-method.md) för syntax, format, källor och felhantering. Läs [references/domains.md](references/domains.md) vid katalogbygge eller stora värdemängder. Läs [references/partition.md](references/partition.md) före uppdelade uttag.

Läs [references/api-contract.md](references/api-contract.md) vid teknisk integration, felsvar och svarstolkning, och [references/metadata-routing.md](references/metadata-routing.md) vid anslutningsgränser och referensvalidering. Använd `scripts/trafa_client.py` för direkt HTTP till råfil och begränsade sammanfattningar. Klienten använder Pythons standardbibliotek och kräver Python 3.9 eller senare, inte trafapy. Behåll exakt query, språk, kontraktshash och metadataunderlag i valideringskvittot före dataanrop.

Läs relevant avsnitt i [references/transportarbete.md](references/transportarbete.md) vid T04010 eller T04020–24. Skilj fordonskilometer från person-/tonkilometer, nationell vägmodell från registreringslän och transit från totaler. Transportarbete är en sekundärsammanställning utan SOS-status; addera inte dess värden till primärkällorna.

Läs [references/resvanor.md](references/resvanor.md) före datauttag vid T1101, särskilt beslutsvägen för delresor med buss: kontrollera begrepp och färdsätt innan årsvolym hämtas. Där finns också folkbokförda 6–84 år, huvudresor kontra påstigningar, metodbytet 2019, kommungruppsversioner och KI. Läs [references/varufloden.md](references/varufloden.md) vid T1102: branschavgränsade sändningar och hela transportkedjor, import kontra avgående flöden, nettovikt/varuvärde, intermittenta år och KI. Hämta tillhörande KI där kombinationen medger det; kontrollera representation per produkt och urval.

Läs [references/postverksamhet.md](references/postverksamhet.md) vid T0701 för tillståndshavare kontra egen utdelning, avgränsning mot hela paketmarknaden, dimensionsberoende enheter och ändringar 2019/2023/2025. Vid T0701 och T0901: beakta Toms uppgift om kommande överföring till PTS; exakt tidpunkt och API-konsekvenser är okända.

Läs [references/televerksamhet.md](references/televerksamhet.md) vid T0901 för PTS-population kontra historiska SNI-/ekonomimått, abonnemang kontra personer, enheter, överlappande storleksklasser och ändringar 2019/2025. Koder i metadata är inte belägg för fortsatt insamling.

Läs [references/luftfart.md](references/luftfart.md) vid T0501 för olika flygplats-/luftfartygspopulationer, riktningar, sekretess, modellberäknat transportarbete och fraktseriens brott kring 2019. Utrikes transportarbete avser delen inom svenskt luftrum, inte hela internationella resan.

Läs [references/vagtrafikskador.md](references/vagtrafikskador.md) vid T1004 för polisrapporteringens täckning, 30-dagarsdefinitionen och historiska avgränsningar, skadebegrepp och alternativa sjukvårdskällor. Vägtypsrader kan överlappa och indelningen ändrades 2020; summera dem inte till en unik total.

Läs [references/fardtjanst.md](references/fardtjanst.md) vid T1201 för tillstånd den 31 december kontra årets nyttjare och enkelresor, medelbefolkning som nämnare och ändrade lokala avgränsningar. Nyttjandegrad kan överstiga 100 procent på grund av olika referenstider; behandla inte det automatiskt som fel.

Läs [references/kommersiell-linjetrafik-vatten.md](references/kommersiell-linjetrafik-vatten.md) vid T1204 för överlapp med T1203, avgränsning mot Sjötrafik och oklar interregional kategori. `sittkm` avser Platskilometer; antag inte interregional täckning bara för att kategorin finns i metadata.

Läs [references/kommersiell-linjetrafik-vag.md](references/kommersiell-linjetrafik-vag.md) vid T1202 för kommersiell population, klassificering på företagsnivå, planerat kontra utfört utbud och överlapp med T1203. `sittkm` betyder Platskilometer i denna produkt; tolka aldrig kodnamnet ensam.

Läs [references/regional-linjetrafik.md](references/regional-linjetrafik.md) vid T1203 för finansierings- och länstäckning, påstigningar kontra reskedjor, planerat kontra utfört utbud, kapacitetsmått, bortfall och överlapp med andra produkter.

Läs [references/punktlighet.md](references/punktlighet.md) vid de fyra T0604-produkterna. Skilj publiceringsfrekvens från API:ets tidsupplösning: kvartals- och årsprodukter kan innehålla månadsrader; kalla inte en månadsrad en separat månadsrelease. För en bred fråga om senaste punktligheten, redovisa i normalfallet både senaste kvartalsvärdet och dess tre månadsuppgifter, med RT(5) och STM(5) sida vid sida där båda finns. Märk månadsraderna som delar av kvartalspubliceringen och verifiera publiceringsdatum på Trafikanalys publiceringssida. Förklara måttens olika nämnare. STM är huvudmått för sammanvägd tillförlitlighet; använd inte det som skäl att utelämna RT. Hitta inte på kvartalsvärdet som ett ovägt medel av månadsandelarna. Ange vald femminutersgräns och erbjud vid behov andra publicerade gränser. STM är återinfört som huvudmått i årsutgåvan 2025 med retroaktiva 2023–2024-värden; kontrollera faktisk API-täckning. Summera inte procenttal eller kumulativa tidsgränser.

Läs [references/bantrafikskador.md](references/bantrafikskador.md) vid T0602. Skilj händelser från personer, olyckor från självmordshändelser, kontrollera definitionsförändringar och undvik dubbelräkning med Vägtrafikskador. Använd T0602 som primär källa för olycks- och personskadefrågor även om trafikslaget är spårväg eller tunnelbana.

När frågan främst gäller trafik och transporter med spårväg eller tunnelbana, använd Regional linjetrafik (T1203) som relevant publiceringsprodukt. Trafikanalys totalundersökning Bantrafik och Järnvägstransporter är enligt statistikansvarige den huvudsakliga datakällan, och dess uppgifter återanvänds i T1203; behandla därför inte produkterna som oberoende källor eller summera dem. Kontrollera efterfrågat mått och urval. Läs [references/bantrafik.md](references/bantrafik.md) för gränsdragning och jämförbarhet.

## Hämta, kontrollera och redovisa

- Använd tillgänglig API-anslutning eller HTTP-klient med parametrar som kodas korrekt. Hitta aktuella verktyg; förutsätt inte ett visst operationsnamn såsom getStructure eller getStatistics. Använd inte verktyg som saknas.
- Begär endast behövliga mått, dimensioner och filter. Bedöm datasvarets storlek från aktuell `DataCount` när den finns och från jämförbara uppmätta datasvar. Referensvalidering saknar aktuell DataCount; en stor produktstruktur betyder inte ett stort datauttag. Hämta hela önskade urvalet direkt om det bedöms rymmas med marginal. Gör ett separat provuttag endast vid osäker storlek eller svarstolkning; låt det ingå i slutresultatet. Inspektera innehållet även vid HTTP 200; ett felsvar eller avklippt svar är inte data.
- Kontrollera produkt, kolumner, tidsomfång, enheter, definitioner, filter, noteringar och revisioner. Bevara kodvärden och källmarkeringar. Skilj noll, saknat värde och sekretess.
- Sammanfoga partitioner i kod med dokumenterade nycklar och täckningskontroll. Redovisa aldrig en delhämtning som fullständig. Följ den särskilda partitioneringsmetoden även om filter inte visas som svarskolumner.
- Aggreggera bara additiva, jämförbara mått över disjunkta kategorier. Summera inte bestånd över tid eller totaler tillsammans med sina delar. Beräkna andelar med rätt nämnare; väg kvoter enligt måttets definition.
- Ange källa, exakt query, hämtningstid, enhet, urval och relevanta begränsningar. Skilj API-värden från egna beräkningar och antaganden. Svara normalt på svenska, använd mellanslag som tusentalsavskiljare och heltal för antal; bevara precision för andra mått.

## När API-innehållet inte räcker

- Hänvisa detaljerade frågor om statistikens framställning till respektive produktsida och dess kvalitetsdeklaration eller metodrapport. Använd sakgranskade kärndefinitioner för produktval och svarstolkning; behandla inte produktprofilen som en fullständig metodbeskrivning.

- När API-innehållet är oklart, ofullständigt eller inte motsvarar statistikfrågans förväntade täckning, ange konkret vad som saknas och hänvisa till respektive statistikprodukts sida på trafa.se eller till [Trafikanalys](https://www.trafa.se/), meny Statistik. Kontrollera produktlänken; använd webbplatsens ingång om den exakta sidan inte är känd.
- Undersök andra tillgängliga publiceringsformer när det behövs för att besvara frågan: exempelvis Excel-tabeller, statistikblad och interaktiva diagram eller rapporter. Ett otillräckligt API-svar betyder inte att statistiken saknas där. Kontrollera täckning, definitioner och version innan en alternativ källa beskrivs som mer fullständig eller används som ersättning. Skilj dess uppgifter från API-resultat.
- Behandla Excel som en möjlig källa, inte en permanent reservkanal. Anpassa hänvisningen till aktuell produktsidas faktiskt tillgängliga publiceringar. Tom uppger 2026-10-10 att Excel successivt ska fasas ut i takt med omstuvade produktkoder; tidplan är inte angiven och framtida instruktioner behöver omprövas när publiceringen ändras.

## Återanvänd verifierad kunskap

Spara vid behov en produktprofil: exakt produkt-Name, officiell etikett, definition/population, frekvens, geografisk upplösning, mått/enheter, dimensionskoder, domänreferenser, belagda kombinationer, källa och verifieringsdatum. Märk saknad information som okänd. Lagra inte fullständiga datauttag i skillen.

Uppdatera metod eller profiler när ett återkommande problem fått en belagd lösning och användaren bett att den sparas. Beskriv ändringen konkret. Anta inte att skillen självlär eller att ett enstaka lyckat anrop gör alla närliggande kombinationer giltiga.

Vid den pågående produktgranskningen: slutför första genomgången av samtliga aktuella produktkoder och gör därefter en andra genomgång av de tidiga profilerna enligt Toms instruktion 2026-10-11. Komplettera dem med aktuella produktsidor, kvalitetsdeklarationer och relevanta metodrapporter. Bevara användarens sakgranskning och dess proveniens; skilj dokumenterade fakta, expertuppgifter och öppna frågor. En ny publicerad metod är inte belägg för att API-et har infört den.

Vid underhåll: håll verifieringsdatum för API-struktur och metodkällor separata. Jämför nya produktlistor, koder, värdemängder, kombinationer och dokumentversioner med föregående underlag innan kataloger ersätts. Bevara historiska definitioner och tidsseriebrott; markera berörda profiler för granskning vid förändring. Kontrollera vid ny publicering eller konkret ändringssignal och validera aktuellt sluturval vid datauttag. Anta inte att någon schemalagd uppdatering finns. Läs endast relevanta produktreferenser och begränsade katalogutdrag i kontext.

## Regressionstestning vid utveckling

Läs [evaluation/RUNNING.md](evaluation/RUNNING.md) när användaren ber om tester eller utveckling av färdigheten. Håll deterministiska kodtester och källbelagda beteendebedömningar åtskilda. Kör `python evaluation/run_offline.py` utan nätverk. Bevara basversionens resultat före rättningar och tillåt statistiskt likvärdiga lösningar. Läs inte evaluationsfacit eller tidigare kandidatsvar under en kandidatkörning eller för att besvara en vanlig statistikfråga; använd då metadata och primärkällor enligt arbetsgången ovan.

Vid jämförelse mellan direktklient och installerad MCP-plugin: läs
[evaluation/COMPARISON.md](evaluation/COMPARISON.md). Håll transportreplay,
levande verktygsprov och bedömning av assistentens fullständiga arbetsgång
åtskilda. Registrera även interna struktur-/dataanrop och motiverade
webbåtgärder när loggåtkomsten medger det; redovisa annars luckorna som okända.
Ett MCP-verktyg som redan slutvaliderar urvalet behöver inte föregås av samma
strukturhämtning. Använd en separat metadatasökning när en kod, definition
eller kombination fortfarande behöver fastställas. Hoppa aldrig över validering.
