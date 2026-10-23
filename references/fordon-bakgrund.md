# Fordon och körkort – fördjupad källbakgrund

Andra genomgången, 2026-10-11. Publicerings- och metodkällor har granskats; API-snapshot är fortsatt från 2026-10-09. Alla gamla expertuppgifter är bevarade i profilerna. Läs aktuell produktprofil med metadata_lookup.py och validera sluturvalet.

## Dokumenterade definitioner

- Registreringspliktiga fordon i Transportstyrelsens vägtrafikregister. Moped klass II, statliga militära fordon och ej registreringspliktiga fordon inom inhägnat område ingår inte. Terrängvagn, terrängsläp och motorredskap finns i registret men redovisas inte i denna statistik. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, 1.2.1.)
- Årsbestånd avser 31 december; ny- och avregistreringar avser kalenderåret. I trafik betyder registrerat och inte avställt, inte observerad körning. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, 1.2.5; Bilaga 1, Status.)
- Administrativa totalregister ger ingen urvalsosäkerhet. Kodningsfel och saknade variabeluppgifter kan förekomma. Årsmodell kompletteras med tillverkningsår när den saknas. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, 2.1–2.2.4.)
- Län/kommun är ägarens folkbokföring eller företagets registrerade adress, inte körplats. Statistikens ägarkategori kan inte besvara antal tjänstebilar. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, 1.1.2; Bilaga 1, Ägande.)
- Regional årsstatistik publiceras i mitten av februari, den detaljerade Fordon-publikationen i slutet av februari. Månadsstatistik publiceras andra vardagen följande månad. (Källa: https://www.trafa.se/vagtrafik/fordon/, Publicering.)
- Månadsbestånd inkluderar tillfälligt registrerade fordon; officiella årsbestånd utesluter dem. Månatliga avregistreringar är preliminära, årsredovisningen slutlig. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, 5.4.)
- Registrerade drivmedel beskriver inte faktiskt använt bränsle. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, Bilaga 1, Drivmedel.)
- El är ren eldrift. Elhybrid och laddhybrid är skilda kategorier; mildhybrider redovisas under bensin/diesel. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, Bilaga 1, Drivmedel.)
- I Fordon-definitionerna redovisas enskild näringsverksamhet bland juridiska personer, trots att den juridiskt inte är en juridisk person. Skilj statistisk ägarkategori från legal form och företagstyp; kontrollera motsvarande definition i varje API-produkt. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, Bilaga 1, Ägande.)
- Släpvagnars karosseriindelning justerades vid Fordon 2020, med revidering av 2010–2019. Äldre Excel-filer har inte uppdaterats; reviderad SL4-serie finns enligt sidan i statistikportalen. (Källa: https://www.trafa.se/vagtrafik/fordon/, Om statistiken.)
- Lätt lastbil har totalvikt högst 3 500 kg, tung över 3 500 kg. Maximilastvikt är totalvikt minus tjänstevikt. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, Bilaga 1, Lastbil och Maximilastvikt.)
- Populationen är personer folkbokförda i Sverige med svenskt körkort. Icke-folkbokförda svenska körkortsinnehavare täcks inte. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, 1.2.1; 2.2.2.)
- Körkortsinnehav avser 31 december; ålder, kön och folkbokföringslän avser innehavaren. Registret kan ha fördröjningar vid aktivering, återkallelse eller inregistrering. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, 1.2.2; 1.2.5; 2.2.)
- Körkort ingår i den detaljerade årsrapporten Fordon som publiceras i slutet av februari. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-2025.pdf, 3.1–3.2.)

## Produkter och kvarstående kontroller

| Kod | Produktroll | Särskild kontroll |
|---|---|---|
| T10011 | Bussar – detaljerad årsstatistik | Exakta urval, koder och överlapp |
| T10014 | Motorcyklar – årsstatistik om bestånd och registreringar | Exakta urval, koder och överlapp |
| T10015 | Mopeder klass I – årsstatistik om bestånd och registreringar | Arbetsantagandets nämnare |
| T10017 | Släpvagnar – årsstatistik om bestånd och registreringar | Historiska karosserirevisioner |
| T10018 | Traktorer – årsstatistik om bestånd och registreringar | Exakta urval, koder och överlapp |
| T10019 | Terrängskotrar – årsstatistik om bestånd och registreringar | Exakta urval, koder och överlapp |
| T10021 | Bussar – regional årsstatistik | Exakta urval, koder och överlapp |
| T10023 | Lastbilar – regional årsstatistik | Exakta urval, koder och överlapp |
| T10026 | Personbilar – regional årsstatistik, län och kommuner | Exakta urval, koder och överlapp |
| T10029 | Övriga fordonsslag – regional årsstatistik | Exakta urval, koder och överlapp |
| T10033 | Lastbilar – månadsstatistik | Preliminära avregistreringar och tillfällig registrering |
| T10036 | Personbilar – månadsstatistik, registreringar och bestånd, även per kommun | Preliminära avregistreringar och tillfällig registrering |
| T10039 | Övriga fordonsslag – månadsstatistik om bestånd och registreringar | Preliminära avregistreringar och tillfällig registrering |
| T10016 | Personbilar – detaljerad årsstatistik, tekniska egenskaper och ägande | Exakta urval, koder och överlapp |
| T10013 | Lastbilar – detaljerad årsstatistik | Exakta urval, koder och överlapp |
| T10030 | Nyregistreringar – månadsstatistik om registreringar och bestånd för flera fordonsslag | Preliminära avregistreringar och tillfällig registrering |
| T10010 | Fordon på väg – årsstatistik för flera fordonsslag | Exakta urval, koder och överlapp |
| T10020 | Fordon i län och kommuner – årsuppgifter för flera fordonsslag | Exakta urval, koder och överlapp |
| T10012 | Körkort – årsstatistik efter behörighet, län, kön och åldersklass | A/B-överlapp och faktisk API-täckning |

## Regler för återanvändning

- Registrerat bestånd är inte antal fordon som faktiskt kör eller ägare som använder fordon. Körsträckor har annan population och ger inte körningens geografiska plats.
- Skilj nyregistrering i det svenska registret från tillverkning av ett nytt fordon; import kan omfatta begagnade fordon. Återpåställning är inte en nyregistrering.
- Skilj avställning från avregistrering. Skrotning och export är avregistreringsorsaker; addera inte orsakerna ovanpå totalen. Administrativ skrotning visar inte när faktisk skrotning skedde.
- Använd produktens specifika koder och tillåtna kombinationer. Omstuvade produkter överlappar äldre produkter; addera dem inte och anta inte en automatisk ett-till-ett-ersättning.
- Summera inte bestånd över perioder, procentandelar eller gruppmedel. Offentlig statistik har fler publiceringsformer än API-et; kontrollera aktuell produktversion när ett urval saknas.
- Bussbestånd är inte antal avgångar, resor eller bussar i en viss kollektivtrafikoperatörs trafik. Bussklass är fordonsutformning, inte automatiskt regional/interregional trafik.
- Terrängskotrar omfattar snöskotrar och terränghjulingar; en fyrhjuling kan ha annan registreringsklass. Tolka inte alla fyrhjulingar som terränghjulingar i denna produkt.
- Totalvikt >3,5 ton i Fordon är inte samma avgränsning som Lastbilstrafiks maxlastvikt ≥3,5 ton. Använd T10061/T10062 för transporter, inte fordonsbestånd.
- Personbilar kan omfatta klass II/husbilar; välj registrerad kategori om frågan enbart gäller vanliga personbilar. Drivmedelsandel anger fordonsantal, inte andel körsträcka eller energi.
- Övriga fordonsslag är en produktspecifik samling; använd exakta underkategorier och hierarkier. Likställ inte Övriga med alla fordon utanför personbilar.
- itrf och avst är månadsbestånd; nyreg och avreg är periodflöden. akumunyreg, när måttet finns, är januari till vald månad samma år och får inte summeras mellan månader.
- Månadsvis summerade avregistreringar är inte garanterat identiska med slutligt årsantal. För årsfrågor välj årsprodukten eller ange preliminär status.
- biltathet gäller personbilar inklusive juridiska ägares bilar, per 1 000 invånare. SCB-befolkningens 1 november och fordonsbeståndets 31 december behålls enligt Toms sakgranskning; ingen ny kontroll av Excel-definitionen här.
- A och B kan överlappa; summera inte dem till unika innehavare eller totalandel. Behörigheter i dokumentationen garanterar inte data i API-et.
- Bevara Toms observation om enbart A/B och avsaknad av total; validera efterfrågat år och urval. Vid otillräcklig täckning kontrollera aktuellt tabellverk via produktsidan.
- Använd åldersklasser, inte påhittade enskilda åldrar. Behåll befolkningsdatum 1 november enligt Toms sakgranskning och särskilj från innehav 31 december.
