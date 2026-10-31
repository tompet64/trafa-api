# Resvanor i Sverige – huvudresor, färdlängd och restid

Granskat 2026-10-11 mot dokumentation och sparad API-metadata. Delvis granskad profil; aktuell API-årstäckning och sluturval måste verifieras.

Personbaserad nationell resvaneundersökning. Välj för resmönster, ärenden, huvudsakliga färdsätt och skillnader mellan befolkningsgrupper; inte operatörernas antal påstigningar.

## Beslutsväg vid frågor om delresor med buss

Kontrollera först att det efterfrågade begreppet och färdsättet finns i aktuell produktstruktur, innan årsdata hämtas. I det underlag som granskats och i användarens omtest 2026-10-15 redovisar T1101 huvudresor efter huvudsakligt färdsätt med en samlad kollektivkategori. Detta besvarar inte antal delresor med buss. Om aktuell struktur bekräftar samma begränsning, avsluta API-spåret utan att hämta kollektivkategorins huvudresevolym som ersättning. Hämta den endast om användaren uttryckligen efterfrågar den som komplettering.

Avgränsa slutsatsen till API-et: frånvaron där bevisar inte att undersökningen saknar underlag för delresor eller att uppgiften saknas i andra publiceringar. Hänvisa till https://www.trafa.se/transportmonster/RVU-Sverige/ och möjligheten att fråga Trafikanalys om en specialbearbetning. Om frågan kräver sökning utanför API-et, kontrollera i första hand produktens aktuella officiella tabellverk med en riktad hämtning eller sökning begränsad till trafa.se. Gör ingen bred webbsökning efter motsvarande ord på operatörers, branschmediers eller andra organisationers sidor: dessa kan inte fastställa RVU:s publicerade delresor. Lova inte att specialbearbetning är möjlig innan den har prövats.

## Definitioner och avgränsningar

- Målpopulationen är folkbokförda personer 6–84 år. En tilldelad mätdag används för individens resande; referensperioden 2025 är kalenderåret. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2026/kvalitetsdeklaration-resvanor-i-sverige-2025.pdf, 1.2.1; 1.2.5.)
- Sedan 2019 används pappers- och webbenkät, stratifierad efter bostadens län, ålder och kön. Årlig publicering. (Källa: https://www.trafa.se/transportmonster/RVU-Sverige/, Om statistiken.)
- En huvudresa kan innehålla flera förflyttningar, färdsätt och ärenden; avslutas vid arbetsplats, skola, bostad eller annan övernattningsplats. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2025/resvanor-i-sverige-2024.pdf, Fotnot 1.)
- Publicerad färdlängd inkluderar resor till och från utlandet; använd inte totalen som enbart resande inom Sverige. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2025/resvanor-i-sverige-2024.pdf, Gång, cykel och kollektivtrafik.)
- Kollektiva färdsätt omfattar allmän buss, tåg, spårvagn och tunnelbana. Övriga omfattar bland annat färdtjänst, taxi, flyg och sjöfart. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2026/kvalitetsdeklaration-resvanor-i-sverige-2025.pdf, 1.2.4.)
- Bortfallet är 74 procent 2025. Uppräkningsvikter används, men systematiska skillnader i resande kan kvarstå. Små redovisningsgrupper har begränsad precision. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2026/kvalitetsdeklaration-resvanor-i-sverige-2025.pdf, 2.1; 2.2.4.)
- 2019–2025 kan jämföras enligt kvalitetsdeklarationen. Telefoninsamling före metodbytet 2019 begränsar jämförbarheten med äldre undersökningar. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2026/kvalitetsdeklaration-resvanor-i-sverige-2025.pdf, 5.1.)
- Kvalitetsdeklarationen anger SKR:s kommungrupper 2024. Sparad API-metadata anger SKR 2017 till och med 2021 och SKR 2023 från 2022; dessutom finns kom med etikett SKL 2011. Klarlägg klassificeringen per period före jämförelser. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2026/kvalitetsdeklaration-resvanor-i-sverige-2025.pdf, 1.2.4; jämförelse med sparad API-struktur.)
- Resdefinitionen skiljer sig från Regional linjetrafik, bland annat genom anslutningsresor. Avrundning gör att deltotaler kan avvika från totalen. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2026/kvalitetsdeklaration-resvanor-i-sverige-2025.pdf, 5.3; 5.4.)
- Statistiken ingår i SOS, med statistisk produktkod TK1101. API-koden är separat T1101. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2026/kvalitetsdeklaration-resvanor-i-sverige-2025.pdf, Allmänna uppgifter A.)
- Statistikbladet 2024 visar 95-procentiga konfidensintervall. API-strukturen har åtta tillhörande KI-mått; deras exakta numeriska representation behöver verifieras i samma API-uttag. (Källa: https://www.trafa.se/globalassets/statistik/resvanor/2025/resvanor-i-sverige-2024.pdf, Figurer 1–8.)

## Rese- och påstigningsbegrepp

Skilj fyra begrepp vid jämförelser:

- **Huvudresa:** resa mellan huvudresepunkter; kan omfatta flera delresor.
- **Delresa:** förflyttning mellan punkter där ärenden uträttas; ett byte av färdsätt utan nytt ärende innebär inte automatiskt en ny delresa.
- **Reselement:** del av en delresa som genomförs med ett färdsätt. Begreppet förekommer i äldre RVU till och med 2016; förutsätt inte att det ingår i senare publicerade API-tabeller.
- **Påstigning:** ombordstigning i ett kollektivtrafikfordon; en delresa kan medföra flera påstigningar.

Kontrollera exakta definitioner och eventuella ändringar mellan undersökningsomgångar i RVU:s kvalitetsdeklaration innan detaljerade historiska jämförelser. Påstigningar i T1203 är inte liktydiga med RVU:s huvudresor eller delresor.

## API-tolkning

- anthresar räknar huvudresor, inte unika resenärer, delresor eller fordonsrörelser. antpers är ett personmått i tusental, inte antal enkätsvar eller antal hushåll.
- hfardsatt och harende avser huvudsakligt färdsätt respektive ärende. En huvudresa kan innehålla flera färdsätt; tolka inte färdsättskategorin som samtliga delsträckor. Exakt tilldelningsregel behöver kontrolleras vid detaljfrågor.
- Håll årsvolym, medelvärde per huvudresa och medelvärde per person och dag isär. Summera inte medelvärden över grupper eller år; använd publicerat mått med rätt nämnare.
- Hushållets biltillgång är tillgång enligt undersökningen, inte samma sak som personens eller hushållets registrerade ägande i Fordon. Kommungrupp är hemortsgruppering, inte en kommunkod eller plats där resan genomförts.
- Hämta varje punktskattning med dess KI i samma urval när kombinationen medger det. Fastställ om KI är felmarginal eller gränser före ±-presentation; överför inte Lastbilstrafiks definition automatiskt. Omräkna båda konsekvent.
- Addera inte KI och beräkna inte KI för en egen summa, andel eller förändring utan underlag för varians och kovarians. Procentuell förändring i punktskattningar är inte automatiskt statistiskt säkerställd.
- Sortera konkreta år numeriskt och behandla flerårsperioder separat; tolka inte blandade periodkoder som en årlig serie. Kontrollera aktuell klassificering och tillåtna dimensionskombinationer.
- Undersökningen samlar fler uppgifter än API-et publicerar. Saknat API-urval ska hänvisas till produktsidan eller möjligheten till specialbearbetning efter prövning; skapa inte en korsklassificering av marginaltabeller.

Mått och KI-koder:

| Mått | Enhet | KI-kod |
|---|---|---|
| anthresar | tusen huvudresor per år | anthresarki |
| antfardlangd | miljoner kilometer per år | antfardlangdki |
| fardlangd | kilometer per huvudresa | fardlangdki |
| restid | minuter per huvudresa | restidki |
| anthrespers | huvudresor per person och dag | anthresperski |
| fardlangdpers | kilometer per person och dag | fardlangdperski |
| restidpers | minuter per person och dag | restidperski |
| antpers | tusen personer | antperski |

## Öppna frågor

- Exakt KI-representation i aktuellt API, särskilt årsvolymer och medelvärden, samt nivå för äldre undersökningsomgångar.
- Vilken kommungruppsindelning gäller faktiskt respektive API-år? Källorna anger olika editionsår.
- Exakt regel för huvudsakligt färdsätt/ärende samt nämnaren för per-person-mått vid detaljerade urval.
- Faktisk API-årstäckning, flerårsperioder och införande av 2025 års resultat; publicering på webben bevisar inte API-tillgänglighet.
