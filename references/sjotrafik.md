# Sjötrafik: produktval och tolkning

Källa: https://www.trafa.se/sjofart/sjotrafik/ , kontrollerad 2026-10-11. Officiell statistik, totalundersökning av fartygsanlöp från cirka 100 aktiva hamnar. Produktprofilerna är delvis granskade från produktsidan, inte fullständigt godkända API-urval.

## Välj rätt produkt och population

- T0802 Sjötrafik: detaljerad årsstatistik. T08021 Sjötrafik kvartal: preliminär kvartalsstatistik med färre uppgifter. Använd aldrig årsproduktens kombinationer som garanti för kvartalsprodukten.
- Statistiken gäller fartygs-, varu- och passagerartrafik till och från svenska hamnar, både inrikes och utrikes. Den är inte avgränsad till svenskregistrerade fartyg och beskriver inte all trafik på svenska vatten.
- Havsgående fartyg med bruttodräktighet minst 20 som anlöper för gods- eller passagerarhantering ingår. Bruttodräktighet är inte vikt i ton. Transit på svenska vatten utan anlöp ingår inte.
- Interregional persontrafik ingår, främst Gotland. Skärgårdstrafikens anlöp och regional linjetrafik i RKM:s regi ingår inte. För sådan trafik hänvisar sidan till Regional linjetrafik; T1203 är en katalogkandidat vars exakta urval behöver valideras.
- Godstransporter på inre vattenvägar ingår och särredovisas i egna årstabeller. Kontrollera att efterfrågad uppdelning finns i API-et; annars hänvisa till produktsidan och alternativa publiceringar.
- Sekretess begränsar hamndetaljer och geografiska områden används i stället. Lova inte enskilda hamnvärden som saknar stöd i aktuellt urval.

## Mått, riktning och revisioner

- Skilj godshantering från transportarbete, och passagerarrörelser/resor från unika personer. Kontrollera om antalfar avser anlöp eller unika fartyg innan resultatet tolkas. Etiketten Antal fartyg är inte tillräcklig för att fastställa unikhet.
- Kontrollera ankomst/avgång och lastning/lossning samt inrikes/utrikes och landets roll. Aland betyder Avgångsland i T0802, inte Åland. För ankomster från ett land, verifiera fartrikt och rätt landdimension. Överför inte koder från andra produkter.
- Summera inte automatiskt lastat och lossat i svenska hamnar till en unik godsmängd: samma inrikes gods kan hanteras i båda ändar. Använd en relevant publicerad total eller belagd aggregationsregel.
- Kvartalsuppgifter är preliminära och kan revideras. Använd senast utgiven statistik även för äldre perioder; gamla publikationer uppdateras normalt inte. Likställ inte en äldre summa av fyra kvartal med en senare årspublicering utan kontroll.
- Fem publiceringar per år: fyra kvartal och en årsutgåva. Sidan anger upp till tre månaders framställningstid för kvartal och drygt en månad längre för år. Anta inte ett specifikt publiceringsdatum utifrån dessa ungefärliga tider.
- Totalundersökning är en uppgift om undersökningsdesign, inte garanti för felfri statistik. Hänvisa detaljer om framställning till aktuell kvalitetsdeklaration på produktsidan.

## Tomt urval är inte saknad årsstatistik – verifierat fall 2026-10-14

För frågan om ankommande passagerare från finska hamnar 2023 är båda följande urvalsvägar dokumenterade, men de har olika faktisk täckning:

- `t0802|pax|ar:2023|passrikt:1|paxland:4`: Selected/Option är true för valen, men DataCount är 0 och data Rows är tom. Orsaken är inte klarlagd. Kalla inte kombinationen ogiltig eller statistik om Finland generellt saknad.
- `t0802|pax|ar:2023|aland:118|fartrikt:1|typh:2|typu:21|skeppstyp`: kontrollerad struktur och data gav en rad. Aland är avgångsland Finland; fartrikt ankommande fartyg; typh utrikes; typu till Sverige från utlandet. Raden avser skeppstyp:1, passagerarfartyg och färjor inklusive roro enligt värdebeskrivningen. Kryssning, övriga och total var inte valbara i samma struktur. Markera avgränsningen; anta inte att saknade kategorier är noll.

Detta visar att ett tomt urval med paxland/passrikt inte motiverar omedelbart byte till kvartalstabeller. Återvalidera hela det alternativa urvalet och kontrollera faktiskt returnerade kategorier, period och enhet. Måttet pax anges i tusental. Spara metoden, inte svarets siffra som en framtida konstant. Källor: aktuella /api/structure och /api/data, språk sv, båda exakta query ovan. Den äldre kombinationslistan är sökhjälp, inte täckningsgaranti.


## Spannmålens import och export – verifierat API-fall 2026-10-26

För en fråga om spannmål som hanterats i svenska hamnar under ett år, välj årsprodukten T0802 och måttet `godsvikt` (Godshantering i 1 000 ton). I T0802 gäller denna klassning:

- `varah:01`: Produkter från jordbruk, skogsbruk och fiske.
- `varau:011`: spannmål. `varau` är underordnad `varah`; behåll båda koderna i urvalet.
- `typh:2`: Utrikes trafik. Använd detta för att avgränsa import/export till utrikes trafik.
- `godsrikt:1`: Lossat gods, relevant som import till svensk hamn.
- `godsrikt:2`: Lastat gods, relevant som export från svensk hamn.
- `godsrikt:t1`: API:ets total för redovisningen; använd inte totalraden som vare sig import eller export.

Verifierad kombination i produktdokumentationen: `godsvikt|ar|godsrikt|typh|varah|varau`. Testad aktuell datafråga:

```
t0802|godsvikt|ar:2025|typh:2|varah:01|varau:011|godsrikt
```

Aktuell strukturvalidering och datahämtning 2026-10-26 gav rader för lossat, lastat och total. Måttet anges i tusental ton. Använd de returnerade radernas värden och etiketter; slå inte ihop riktningarna till en egen total. I testuttaget var summan av de avrundade import- och exportraderna en enhet (1 000 ton) lägre än API:ets totalrad. Lås inte testvärden som framtida konstanter eftersom publicerade data kan revideras.

Tolkningen import = lossat och export = lastat avser utrikes godshantering i svenska hamnar. Den är inte en bilateral handelsredovisning eller ett mått på hela transportkedjan. Om frågan gäller ett visst avsändar-/mottagarland, lägg inte till en landdimension utan att först kontrollera dess roll, värdekoder och en dokumenterad tillåten kombination i aktuell struktur.
