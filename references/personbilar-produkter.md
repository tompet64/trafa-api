# Skilj personbilsprodukter och publikationer

Behåll officiell API-etikett Personbilar för T10026, T10016 och T10036. Använd den granskade presentationskontexten och föreslagna förtydligade namnen för produktval. Publikationsnamn är inte API-koder.

| API-produkt | Kontext och upplösning | Mått | D inklusive År | H | Geografi i strukturen |
|---|---|---:|---:|---:|---|
| T10026 | Fordon i län och kommuner; regional årsstatistik | 4 | 8 | 2 | reglan och regkom |
| T10016 | Fordon; detaljerad årsstatistik för personbilar | 4 | 16 | 4 | Ingen läns- eller kommundimension i sparad struktur |
| T10036 | Månadsstatistik för personbilar | 5 | 7 | 1 | kommun under region; ingen länsdimension |
| T10020 | Fordon i län och kommuner; flera fordonsslag, årsstatistik | 4 | 11 | 0 | lan och kommun |

Toms jämförelse 7 respektive 15 variabler för T10026 och T10016 stämmer när År räknas separat. H-poster är hierarkier, inte ytterligare fristående D-dimensioner. Dokumentera alltid räkneregeln.

## Innehåll och val

- T10026: itrfslut, avstslut, nyregunder och biltathet. Regional årsstatistik med bland annat drivmedel, leasing och ägarkategori. Årsdomänen i snapshot 2026-10-09 är 2010–2025.
- T10016: itrfslut, avstslut, nyregunder och avregunder. Fler tekniska och ägarrelaterade indelningar, inklusive tjänstevikt, direktimport, fordonsålder, bransch och avregistreringsorsak. Publikationen Fordon innehåller även körkort, men T10016 har ingen körkortsstatistik. Använd T10012 för körkort och validera dess urval separat.
- T10036: nyreg, akumunyreg, itrf, avst och avreg. Månad och kommun finns; län saknas. Ackumulerade nyregistreringar (akumunyreg) avser januari till och med vald månad inom samma kalenderår, bekräftat av Tom 2026-10-09. Summera inte ackumulerade månadsvärden; decembervärdet avser hela kalenderåret. Itrf och avst avser bestånd vid vald månads slut och inkluderar tillfälligt registrerade fordon. Motsvarande årsbestånd i T10016, T10026 och T10020 utesluter dessa fordon (Tom, 2026-10-09). Decemberbestånd och årsbestånd den 31 december kan därför skilja sig trots samma referensdag. Likställ dem inte utan populationskontroll.
- T10020 överlappar enligt Tom i stort sett T10026:s personbilsinnehåll, men exakta variabel- och värdekoder skiljer sig och likvärdighet av alla urval är inte belagd. Den sparade årsdomänen är 2022–2025. Ersätt inte T10026 automatiskt när en äldre period eller särskild indelning efterfrågas.

Använd inte lika kodnamn som bevis för lika betydelse: exempelvis avser fslag en underkategori i T10026 men fordonsslag i T10020. Återanvänd inte filtervärden mellan produkter utan kontroll.

Kvalitetsdeklarationen för 2025 beskriver att månatliga bestånd inkluderar tillfälligt registrerade fordon, vilka inte ingår i de officiella årspublikationerna. Behåll denna skillnad vid jämförelser och kontrollera definitionen för aktuell årgång: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-i-lan-och-kommuner-2025.pdf, avsnitt 5.4 (kontrollerat 2026-10-09).

Källstatus: koder, typer, antal och mått är kontrollerade i sparad API-struktur 2026-10-09. Presentationskontext och den breda innehållsjämförelsen kommer från Toms sakgranskning 2026-10-09 kl. 20:27. Metadata är fortsatt delvis granskad; produktprofilerna är inte godkännande av varje API-kombination.

## Körsträckor och ägandebegrepp

T10094 har officiell etikett Personbilar och avser körsträckor, inte en produkt begränsad till enskilda näringsidkare (Tom, 2026-10-09). Måtten är korstr (Körsträckor, mil), anttrf (Antal Personbilar), mkorstr (Medelkörsträcka, mil) och gdkor (Genomsnittlig daglig körsträcka). Anttrf avser personbilar som varit i trafik någon gång under året; likställ inte antalet med bestånd vid årets slut.

Skilj agarkat (Ägarkategori: fysisk eller juridisk person) från ftgtyp (Företagstyp) i T10094. Enskild näringsidkare är ett värde i ftgtyp, kod 1, inte en separat ägarkategori. T10016 använder i stället bolagsform (Bolagsform), med värdet Enskilda näringsidkare, kod 21. Behåll respektive produkts officiella kod och etikett; överför inte koder mellan dessa variabler.

Medelkörsträcka (mkorstr) är total körsträcka dividerad med antalet fordon som varit i trafik minst en dag under kalenderåret, inklusive fordon med noll körsträcka (Tom, 2026-10-10, eget utdrag ur kvalitetsdeklarationen; dokumentversion inte angiven eller oberoende kontrollerad). Körsträckan härleds från två eller tre på varandra följande mätaravläsningar vid obligatoriska besiktningar. Använd inte års-slutsbestånd som nämnare. Summera inte gruppmedel eller använd oviktat medel av dem; använd jämförbara totaler eller fordonsantal som vikter för disjunkta grupper. För gdkor är den fordonsvisa metoden nu dokumenterad nedan, men aggregeringen återstår att granska.

Daglig körsträcka för ett enskilt fordon beräknas som körda mil mellan de två senaste besiktningarna dividerat med dagarna i trafik mellan dessa besiktningar. Dagar i trafik är dagar mellan besiktningarna minus avställda dagar enligt Transportstyrelsens av- och påställningsuppgifter (Tom, utdrag ur kvalitetsdeklarationen för 2025 års statistik, 2026-10-10; inte oberoende kontrollerad). Intervallet är mellan besiktningar, inte automatiskt kalenderåret. Utdraget anger inte hur dessa fordonsvärden vägs samman till API-måttet gdkor. Anta därför inte oviktat medel, kvot mellan totaler eller mkorstr/365 (366).

### Metodversion och geografisk avgränsning

Tom uppger 2026-10-10 att API-et ännu inte uppdaterats med nya metodens siffror; införandeplanen är okänd och metodversion per årgång är inte oberoende kontrollerad. Avvakta med tillämpning av den nya metodens specifika regler på API-resultat. Behåll tidigare dokumentation som källunderlag, inte som bevis för API-versionen. Aggregeringsformeln för gdkor är fortsatt okänd.

Körsträckestatistiken omfattar svenskregistrerade fordons körning både i Sverige och utomlands och visar inte var de körts (Tom, 2026-10-10). Registreringslän beskriver inte körningens plats. Använd därför inte körsträckor som ett direkt mått på trafikarbete inom Sveriges eller ett läns gränser.

### Övriga produkter med körsträckor

T10091 (Bussar), T10092 (Lastbilar) och T10093 (Motorcyklar) avser årlig körsträckestatistik. Grundpopulationen är respektive fordonsslag som varit i trafik minst en dag under kalenderåret (Tom, 2026-10-10). Anttrf är därför inte års-slutsbestånd. Profilerna är delvis granskade; överför inte produktunika indelningar eller nya metodens regler mellan produkterna. T10091 och T10092 har måtten korstr, anttrf, mkorstr och gdkor. T10093 har korstr, anttrf och mkorstr; gdkor saknas i den sparade strukturen.

### Produktval för lastbilar

Alla följande produkter har officiell etikett Lastbilar. T10013 avser detaljerad årsstatistik: bestånd, ny- och avregistreringar, tekniska egenskaper och ägaruppgifter. T10023 avser regional årsstatistik: i trafik och avställda efter län, kommun, lastbilstyp och drivmedel. T10033 avser månadsstatistik: bestånd, ny- och avregistreringar efter lastbilstyp. Dessa förtydligade roller och periodicitet bekräftades av Tom 2026-10-10. T10092 är den separata körsträckeprodukten. Profilerna är delvis granskade; överför inte populationsdefinitioner eller kombinationer automatiskt.

### Produktval för bussar

T10011 och T10021 har officiell etikett Bussar. T10011 avser detaljerad årsstatistik: bestånd, ny- och avregistreringar, bland annat bussklass, drivmedel och ägaruppgifter. T10021 avser regional årsstatistik: i trafik och avställda efter län, kommun och drivmedel. Roller och periodicitet bekräftades av Tom 2026-10-10. T10091 är den separata körsträckeprodukten. Profilerna är delvis granskade; godkänn inte nya kombinationer eller populationsdefinitioner enbart utifrån detta.

### Produktval för motorcyklar och mopeder klass I

T10014 (Motorcyklar) och T10015 (Mopeder klass I) avser årsstatistik om bestånd och registreringar, bekräftat av Tom 2026-10-10. Båda har itrfslut, avstslut, nyregunder och avregunder. T10014 har cylindervolym, fordonsålder och ägaruppgifter. T10015 har även måttet andelitrafik och indelningar efter ägarkategori, kön och ägarens ålder. API-beskrivningen anger procent vid periodens slut för andelitrafik. Arbetsantagandet är 100 * itrfslut / (itrfslut + avstslut) inom samma redovisningsgrupp den 31 december (Tom, 2026-10-10). Detta är inte en verifierad definition: Tom hittar ingen annan information och andelen saknas enligt honom i Excelbladet. Ange antagandet vid användning; summera inte procentandelar. T10093 är den separata körsträckeprodukten för motorcyklar. Profilerna är delvis granskade.

### Övriga fordonsbestånd

Roller och årsperiodicitet bekräftade av Tom 2026-10-10: T10017 Släpvagnar har bestånd, ny- och avregistreringar efter karosseri och totalvikt. T10018 Traktorer har samma fyra mått samt tjänstevikt, drivmedel, fordonsålder och ägaruppgifter. T10019 Terrängskotrar har samma fyra mått efter fordonsslag. T10029 Övriga fordonsslag har i trafik och avställda efter fordonsslag, län och kommun. Profilerna är delvis granskade; exakt population och kombinationer kräver fortsatt kontroll.

### Produkter för flera fordonsslag

T10010 Fordon på väg avser årsstatistik för flera fordonsslag med bestånd, registreringar, avregistreringar och egenskaper. T10030 Nyregistreringar avser månadsstatistik och har även bestånd, avregistreringar, skrotning och export samt län och kommun. T10039 Övriga fordonsslag avser månadsstatistik om bestånd och registreringar, med län och kommun. Tom bekräftade rollerna 2026-10-10 och att T10010 och T10030 liksom T10020 omstuvat innehåll från äldre fordonsprodukter för den nya presentationsformen. Anta inte exakta motsvarigheter mellan variabler och kombinationer.

### Körkort

T10012 Körkort avser årsstatistik med antal körkort och andel av befolkningen efter körkortsklass, län, kön och innehavarens åldersklass (Tom, 2026-10-10). Alder är endast åldersklasser, inte enskilda åldrar. Bevara officiell etikett och koder; skapa inte finare åldersfördelning från klasserna. Körkortsinnehavet (antalkorkort) avser den 31 december statistikåret. Befolkningen i nämnaren för andelbefolk avser den 1 november samma statistikår (Tom, 2026-10-10). Behåll de olika referensdatumen och använd inte automatiskt befolkning vid årets slut. Exakt gruppmatchning och population återstår att granska. A och B överlappar: samma person kan räknas i båda, och summan av andelarna kan överstiga 100 procent (Tom, 2026-10-10). Summera inte klasserna till unika innehavare. Tom observerar endast data för A och B, inga C/D eller totaler, trots att dessa finns i den sparade metadatadomänen. Observationens år och query är inte angivna; kontrollera datatäckning vid aktuellt uttag. Skapa inte en total från A och B. Produktkodens framtidsplan är okänd.

För T10012 anger Tom 2026-10-10 att körkortsstatistikens Excelblad kan ge mer fullständig information än API-et. Hänvisa vid otillräcklig API-täckning till aktuell produktsida eller trafa.se, meny Statistik. Kontrollera filversion och faktisk täckning innan alternativet används; lås inte instruktionen till Excel eftersom publiceringsformerna förändras.

## Fördjupad källgranskning 2026-10-11

Andra genomgången har kompletterat produktprofilerna med aktuella kvalitetsdeklarationer. Äldre expertuppgifter ovan är bevarade som ursprunglig proveniens. Gemensamma definitioner och nya avgränsningar finns i `fordon-bakgrund.md`, körsträckornas versionsskillnader i `korstrackor.md` och aktuella sakfrågor i respektive produktprofil. Tidigare allmänna öppna frågor om population och period är preciserade där; detta är inte en fullständig API-validering.
