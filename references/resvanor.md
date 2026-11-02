# Resvanor i Sverige – huvudresor, färdlängd och restid

Granskat 2026-10-11 mot dokumentation och sparad API-metadata. Delvis granskad profil; aktuell API-årstäckning och sluturval måste verifieras.

Resebegreppen och metodbrottet 2019 förtydligade 2026-11-02 mot originalkällor och Toms sakgranskning. API-metadata har inte omverifierats vid denna komplettering.

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
- **Reselement (äldre RVU till och med 2016):** del av en delresa som genomförs med ett färdsätt. Byte av färdsätt ger ett nytt reselement; byte mellan fordon med samma färdsätt, exempelvis buss till buss, gör det inte. Från och med 2019 års undersökning samlas reselement inte in.
- **Påstigning:** ombordstigning i ett kollektivtrafikfordon; en delresa kan medföra flera påstigningar.

Kontrollera exakta definitioner och eventuella ändringar mellan undersökningsomgångar i RVU:s kvalitetsdeklaration innan detaljerade historiska jämförelser. Påstigningar i T1203 är inte liktydiga med RVU:s huvudresor eller delresor.

### Metodbrottet 2019 och jämförelser av reselement

**Från och med 2019 finns endast huvudresor och delresor som hierarkiska resenivåer i RVU. Reselement samlas inte längre in.** Detta är en förändring av undersökningens innehåll, inte enbart en begränsning i API-publiceringen.

Antalet reselement i RVU 2016 och RVU 2025 kan därför inte jämföras som samma insamlade mått: reselement ingick 2016 men samlas inte in 2025. Besvara denna fråga med stöd av detta avsnitt. Ersätt inte reselement med huvudresor, delresor eller påstigningar. Vid jämförelser av huvudresor eller delresor över metodbytet måste dessutom bytet från telefonintervjuer till pappers- och webbenkät beaktas.

Källstöd, kontrollerat 2026-11-02:

- [Kvalitetsdeklaration RVU Sverige 2015–2016](https://www.trafa.se/globalassets/statistik/resvanor/2016/rvu-sverige-2016-kvalitetsdeklaration.pdf), avsnitt 1.2.1, s. 6: mätdagens reselement ingår uttryckligen. Avsnitt 5.3, s. 13: gränsen mellan reselement går vid byte av färdsätt.
- [Mobilnätsdata som källa till Resvanor i Sverige, PM 2023:6](https://www.trafa.se/globalassets/pm/2023/pm-2023_6-mobilnatsdata-som-kalla-till-resvanor-i-sverige.pdf), avsnitt 3.1–3.2, s. 13: RVU gjordes om från 2019 och undersökningen har två hierarkiskt ordnade resebegrepp, huvudresa och delresa.
- [Kvalitetsdeklaration Resvanor i Sverige 2025](https://www.trafa.se/globalassets/statistik/resvanor/2026/kvalitetsdeklaration-resvanor-i-sverige-2025.pdf), avsnitt 3.2, s. 13: insamlingen i nuvarande form har pågått sedan 2019. Avsnitt 5.1, s. 17: 2025 kan jämföras med 2019–2024, medan jämförelser med äldre telefonundersökningar kräver försiktighet.

Sakgranskning 2026-11-02: Tom bekräftar uttryckligen att reselement inte samlas in från 2019. Tvånivåbeskrivningen kommer från PM 2023:6; påstå inte att 2025 års kvalitetsdeklaration ordagrant anger att reselement har tagits bort.

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
