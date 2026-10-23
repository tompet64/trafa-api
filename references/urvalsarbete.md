# Effektiva och kontrollerbara urval

## Arbetsgång

Identifiera mått och population i kort metadata, läs relevanta kombinationer, välj minimala mått och alla relevanta dimensionsroller. Validera och hämta med klientens `extract`. Använd strukturvägen när svaret ryms och den aktuella kontrollen är tillgänglig. Använd daterad referensvalidering enligt metadata-routing.md när den vägen valts; för en känd för stor struktur behöver då bara data hämtas via HTTP.

Strukturvägen gör normalt två sekventiella anrop. Referensvägen kontrollerar de lokala underlagen före ett dataanrop. En okänd struktur som först visar sig för stor kan ge ett avbrutet strukturanrop följt av referensvalidering och data. Spara valideringskvitto med exakt query, språk, metadatarevision och filhashar samt begäransloggar för faktiskt gjorda anrop. Återanvänd ett sparat storlekskvitto så att samma för stora struktur inte hämtas igen.

Aktuell `DataCount=0` avslutar innan data och kräver ett motiverat alternativ eller ett avgränsat besked. Referensvägens `DataCount=null` betyder okänd, inte tom. Bedöm datatäckning från det faktiska datasvaret och dess noteringar. Referensvägen får aldrig användas för att åsidosätta ett aktuellt negativt valbarhetsbesked.

`--rows 10` visar högst tio resultatrader med exakta dimensionskoder/etiketter, måttvärden, IsTotal och not-ID. sample_complete visar om hela svaret ryms. Full råfil och Header/Notes är källan för större svar och fotnoter. HTTP-begäransloggen har elapsed_seconds och attempts för nya anrop; de mäter inte hela modellens svarstid.

## Dokumenterade exempel

| Syfte | Query | Evidens och kontroll |
|---|---|---|
| Malmö, årsbestånd personbilar | `t10026|itrfslut|agarkat:t1|ar:2019,2023|reglan:12|regkom:1280` | Tom återrapporterar lyckat uttag 2026-10-14. Slutvalidera; två år samtidigt. |
| Personbilars månadsavregistreringar | `t10036|avreg|ar:2023|manad` | Tom har kontrollerat att övriga mått inte krävs. Kontrollera exakt tolv månader, preliminär status. |
| Personbilars slutliga årsavregistreringar | `t10016|avregunder|ar:2023` | Tom har kontrollerat att övriga mått inte krävs. Rättelser kan förklara skillnader generellt, inte varje enskild differens utan underlag. |
| A och B samtidigt | `t10012|andelbefolk|ar:2023|korkort` | Tom bekräftar gemensamt uttag. Välj A/B-rader och kontrollera gemensamma nämnare; summera inte till unika innehavare. |
| Regional spårväg och tunnelbana | `t1203|pastig|ar:2025|finans:2|traslag:3,4` | Livekontrollerat 2026-10-14; subventionerad trafik anges explicit. Motsvarande åtta rader kontrollerade 2022–2025. Skilj från implicit standard eller okontrollerad total. |

Exemplen är sökhjälp, inte permanent garanti. För senaste år: utgå från högsta konkreta årskod och kontrollera att båda efterfrågade kategorierna faktiskt har numeriska värden i rätt urval. Hämta inte automatiskt alla historiska år för en senaste-år-fråga.

## Särskilda fall

- T10061: begär godsm och godsmki tillsammans. Behåll officiell bred varugrupp och välj inrikes samt den faktiskt relevanta körningstypen. Ett tomt totalalternativ innebär inte att lastade transporter saknas. Kontrollera exakta returnerade kortyp/riktning-rader innan val av punktskattning och KI; summera inte KI.
- T10092: länsindelningen reglan har mkorstr men inte korstr enligt Toms kontroll 2026-10-14. Det gäller registreringslän, inte platsen för körningen. Led med att territoriell körning inte kan besvaras, i stället för ett närliggande medeltal.
- T1101: huvudresor efter huvudsakligt färdsätt är inte delresor med buss. Begränsa besked om saknat mått till kontrollerat API-innehåll och hänvisa till produktsida/specialbearbetning vid behov. Sök inte bussvärden på externa nyhetssidor som ersättning för RVU.
- T1203/T06013: etiketterna Påstigningar/Resor medför inte olika resbegrepp för spårväg och tunnelbana. Enligt statistikansvariges besked är Bantrafik och Järnvägstransporter huvudsaklig källa och dessa uppgifter används även i T1203. Tom har uppgett att samma påstigningar redovisas med tusentals-/miljontalsavrundning. Överför inte detta till järnvägens samtrafikdefinition eller RVU:s reskedjor. Summera inte produkterna.

## Statusmeddelanden

Behåll API-koder i anrop, översätt dem inte till ämnen via ordlikhet. Skriv egen status i verifierad klartext eller neutralt: Kontrollerar statistikurval, Hämtar årsuppgifter från Trafikanalys. Aktivitetsrubriker som Malmö, skattedata eller lånedata är inte i sig bevis för ett felaktigt urval. Granska query och svar. Deras tekniska ursprung är inte fastställt; lova inte kontroll över automatiska gränssnittsrubriker.
