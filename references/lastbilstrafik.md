# Lastbilstrafik: urvalsundersökning och osäkerhet

T10061 (Lastbilstrafik år) och T10062 (Lastbilstrafik kvartal) avser trafik och transporter med svenskregistrerade tunga lastbilar såväl inom Sverige som utomlands. Statistiken bygger på en urvalsundersökning (Tom, produktcitat och expertuppgift, 2026-10-10). Lastbilen ska ha maxlastvikt minst 3,5 ton (3 500 kg, inklusive gränsvärdet), enligt Toms läsning av kvalitetsdeklarationen 2026-10-10. Gränsen gäller maxlastvikt, inte totalvikt; överför inte en generell definition av tung lastbil till undersökningens urval. För övriga detaljer om population, urval och framställning, hänvisa till aktuell produktsida och dess kvalitetsdeklaration eller metodrapport. Profilen återger inte alla metoddetaljer. Skilj dessa produkter från fordonsbestånd och körsträckestatistik.

| Punktskattning | Tillhörande KI | API-skala för båda |
|---|---|---|
| anttrp | anttrpki | 1 000 transporter |
| kordakm | kordakmki | 1 000 km |
| godsm | godsmki | 1 000 ton |
| trparbete | trparbeteki | miljoner ton-km |

Hämta tillhörande KI tillsammans med varje efterfrågad punktskattning, i samma urval och period. Redovisa båda; om KI saknas, säg det. De sparade API-etiketterna anger 95 procent. Behåll exakta API-koder i respektive struktur; suffixet skrivs med gemener i de verifierade Name-koderna.

Tom bekräftade 2026-10-10 att KI-värdet är felmarginalen (halva intervallbredden) i ett tvåsidigt 95-procentigt konfidensintervall. Redovisa skattning ± KI, eller gränserna skattning - KI och skattning + KI. Kalla inte detta ett ensidigt 95-procentigt intervall. Om skattningen räknas om till ton/km/antal ska KI räknas om med samma faktor. Summera inte KI eller felmarginaler över år, kvartal eller grupper för att konstruera ett nytt KI; använd publicerad total med dess KI eller en statistiskt belagd metod med nödvändigt kovariansunderlag.

Statistisk tolkning: 95-procentig konfidens avser intervallets täckningsgrad vid upprepade urval under metodens förutsättningar, inte en posterior sannolikhet för det fasta populationsvärdet givet ett redan observerat intervall. Se NIST:s förklaring av konfidensintervall: https://itl.nist.gov/div898/handbook/prc/section1/prc14.htm .

## T0301: utländska lastbilstransporter

T0301 Utländska lastbilstransporter i Sverige är ett komplement till Lastbilstrafik och ingår inte i Sveriges officiella statistik enligt Tom (produktsideutdrag och expertuppgift 2026-10-10). Produkten sammanställer deltagande EU-länders och frivilliga europeiska länders rapporterade urvalsundersökningar. Den avser transporter till, från, genom (transit) och inom (cabotage) Sverige. Fordonsgränsen är minst 3,5 ton maxlastvikt **eller** 6 ton totalvikt för det enskilda fordonet; överför inte exakt populationsgräns från T10061/T10062.

Deltagande länder varierar mellan år; statistiken täcker inte alla utländska registreringsländer. Ryssland nämns som ej inkluderat. Anta inte att alla länder utanför EU är uteslutna, eftersom frivilliga europeiska länder kan ingå. Otillåten trafik saknas sannolikt enligt utdraget. Tom bedömer att skattningarna sannolikt är underskattade; det är en kvalitativ bedömning utan kvantifierad korrigering.

Måtten är tonkm (miljoner tonkilometer), ton (1 000 ton), antal (1 000 transporter) och trfarb (1 000 km). Konfidensintervall saknas enligt Tom. Ange relevant urvals- och täckningsosäkerhet; konstruera inga KI eller korrigerade totaler utan underlag. Koppla inte svenska undersökningens KI till dessa värden. Kontrollera jämförbar period, population, sträckavgränsning och landtäckning före summering med svenskregistrerade lastbilar eller beräkning av marknadsandelar. Transporter till/från Sverige innebär inte automatiskt att hela måttets sträcka ligger inom Sverige. Hänvisa detaljer om framställning och aktuell landtäckning till produktsidan.
