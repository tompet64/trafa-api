# Vägtrafikskador – T1004

Delvis granskad 2026-10-11 mot produktsida, kvalitetsdeklaration 2025 och sparad API-metadata; slutvalidera uttag.

## population

Vägtrafikolyckor med personskada på svenska vägar där minst ett fordon i rörelse varit inblandat, huvudsakligen polisrapporterade till Transportstyrelsen. Dödsfall kompletteras med andra register. Inte alla skador i trafikmiljö eller alla sjukvårdsregistrerade trafikskador.

## source_roles

Trafikanalys producerar statistiken och är källa vid API-hämtning. Polisen rapporterar olyckor, Transportstyrelsen samlar uppgifterna och dödsfall kompletteras från bland annat SCB, RMV och Socialstyrelsen. Benämn inte api.trafa.se som Trafikverket.

## death

Dödade avser personer avlidna till följd av trafikolyckan inom 30 dagar. Perioden knyts till olyckans datum, inte dödsdatum. Självmord och andra avsiktliga händelser exkluderas från 2010; sjukdomsfall som avlidit av annan orsak än krockvåldet avgränsas särskilt.

## historical_deaths

Kvalitetsdeklarationen beskriver 1960–1993 som regelrätta olyckor, 1994–2002 som olyckor + sjukdom + självmord, 2003–2009 som olyckor + självmord och från 2010 som regelrätta olyckor. Tidigare kontroller är delvis osäkra. Överför inte dagens exkluderingar bakåt i serien eller skarva utan reservation.

## injury

Svårt och lindrigt skadade enligt polisbaserad statistik är inte automatiskt likvärdiga med sjukvårdsbaserad svårighetsgrad, medicinsk invaliditet eller Bantrafikskadors allvarligt skadade. Exakt skadegradsdefinition ska kontrolleras i produktspecifik dokumentation före sådana jämförelser.

## undercoverage

Alla personskadeolyckor når inte polisen; skadade och olyckor har betydande undertäckning, särskilt cykelsingelolyckor. Dödsfallen har betydligt högre täckning genom kompletterande källor. Tolka inte minskad polisrapportering som säker minskning av faktiska skador. Historiska täckningsandelar är inte generella korrigeringsfaktorer.

## health_alternative

Vägtrafikskadade i sjukvården bygger på Socialstyrelsens patientregister och är jämförelsematerial utanför Sveriges officiella statistik enligt produktsidan. Vid frågor om faktiska skador, särskilt oskyddade trafikanter, hänvisa till denna alternativa källa; summera inte överlappande polis- och sjukvårdspopulationer.

## measure_units

Skilj olyckor, personer, motorfordonsförare och trafikelement. antpersd är dödade personer; antford dödade motorfordonsförare. Kombinerade mått antolyckds/dsl och antpersds/dsl överlappar sina delmått och ska inte adderas till dem. Välj publicerad total. API-mått per 100 000 invånare är inte procent eller exponeringsrisk per körd kilometer.

## road_type

vagtyp bytte indelning från 2020 enligt metadata och jämförelser med tidigare år kan inte göras direkt. Flera väglänkar kan kopplas till samma olycka och varje unik vägtyp räknas: vägtypsrader summerar därför till fler olyckor/personer än totalen. Behandla kategorierna som potentiellt överlappande.

## location_speed

Län och kommun avser olycksplats, inte de drabbades bostadsort. hastighet är högsta tillåtna hastigheten där olyckan skedde, inte uppmätt faktisk hastighet hos inblandade fordon. Metadata anger att okänd bebyggelsetyp förs till Ej tättbebyggt område; tolka inte den kategorin som enbart verifierad landsbygd.

## seasons

arstid använder produktens definition: vinter december–mars, vår april–maj, sommar juni–september, höst oktober–november. Överför inte standardårstider eller meteorologiska definitioner. Kontrollera periodanknytning om vintrar ska jämföras över årsskiften.

## alcohol

alkhalt avser blodalkohol bland omkomna motorfordonsförare, inte alla förare eller alla olycksinblandade. Uppgifter saknas för vissa och alkoholhalten är efter död snarare än vid olyckstillfället; kvalitetsdeklarationen anger risk för underskattning. Ange rätt population och nämnare vid andelar.

## overlap_rail

Plankorsningsolyckor och vissa olyckor med spårväg kan ingå även i Bantrafikskador T0602. Summera inte produkterna till en gemensam olycks-/persontotal utan hantering av överlapp.

## official_status

Vägtrafikskador ingår i Sveriges officiella statistik, men EU-jämförelsetabellerna 7.1 och 7.2 i publikationen 2025 gör det inte. API har land i metadata; kontrollera proveniens och märk inte varje uttag som SOS bara för att produkten har SOS-symbol.

## publication

Årlig slutlig publicering i slutet av april, normalt inom fyra månader efter året. Månad i API betyder inte preliminär månadsprodukt. För aktuella preliminära månadsuppgifter hänvisar kvalitetsdeklarationen till Transportstyrelsen; kontrollera källa och revisionsstatus.

## coverage

Sparad API-metadata innehåller skadade av olika svårighetsgrad även om senaste publicering främst fokuserar omkomna och bara behåller lindrigt skadade i några tidsserier. Verifiera faktisk täckning per år och urval, inte endast global variabelförekomst.

## Källor

- https://www.trafa.se/vagtrafik/vagtrafikskador/
- https://www.trafa.se/globalassets/statistik/vagtrafik/vagtrafikskador/2025/kvalitetsdeklaration-vagtrafikskador-2025.pdf (publicerad 2026-04-27), avsnitt 1.2, 2, 3 och 5 samt SOS-avsnittet. Förstasidans TK1001 motsägs av SOS-avsnittets TK1004; API-kod T1004 är verifierad i metadata och ersätts inte utifrån dokumentets kodavvikelse.
- Sparad struktur t1004, 2026-10-09.
- Bantrafikskador, kvalitetsdeklaration 2025 avsnitt 5.2–5.3, för överlapp.
