# Säkra filtrerade delhämtningar

Följ tidigare arbetsunderlag gpt_instruktion_chunking.md (2026-09-09) och den faktiskt använda anslutningens villkor. För en anslutning med en gräns kring 100 000 svarstecken, använd 80 000 tecken som lokal målgräns med marginal. Gör inte detta till en generell gräns för Trafikanalys API eller direkt Python. Utan motsvarande anslutningsgräns, bedöm i stället uppmätt storlek, tid och minne. Läs bara nödvändiga utdrag i modellkontext även när en stor råfil kan hämtas.

Behåll högst 20 dataanropsförsök per interaktivt arbetsflöde, inklusive misslyckade försök, som lokal arbetsbudget. Målgränsen och försöksbudgeten är metodregler, inte automatisk paginering eller generella servergränser. Redovisa uppmätt storlek bara när den faktiskt mätts. Skilj datasvarets storlek från strukturens; välj referensmetadata för en för stor struktur enligt metadata-routing.md utan att automatiskt dela upp ett litet datauttag.

## Välj först om uppdelning behövs

Minimera urvalet enligt SKILL.md innan storleksbedömningen. Välj minsta antal anrop som bedöms rymmas under målgränsen med rimlig marginal; dela inte rutinmässigt per år. Använd jämförbara svar med samma format och kolumner för uppskattning, och märk uppskattningar som uppskattningar. Om två år beräknas rymmas i ett svar, hämta båda tillsammans. Vid osäker storlek, hämta en del som ändå behövs, mät den och dimensionera återstående delar. Hämta inte provdelen igen.

## Planera och hämta

- Frys produkt, mått, redovisningsdimensioner, språk, enheter och övriga filter. Dela en befintlig filterdimension, helst period och därefter exempelvis kommun. Ändra inte tabellens dimensionsuppsättning för att minska svaret utan ny validering.
- Om dimensionen redan valts utan filter, gör dess faktiska värdemängd till explicit filtrerat urval med bevarad täckning. Använd bara källbelagda koder. Upplös dynamiska senaste-val till konkreta koder när möjligt.
- Definiera parvis disjunkta delmängder vars union är exakt det efterfrågade urvalet. Kontrollera båda villkoren i kod. Frys värdemängd och spara hämtningstider; samma filter låser inte en revisionsversion.
- Använd ett nödvändigt provuttag eller befintlig jämförbar storleksmätning för att dimensionera delarna. Vid uttryckligt storleksfel halvera bara misslyckad del och ersätt den i planen med barn-delar. Behåll varje värde exakt en gång i den aktiva planen. Anpassa mål efter aktuellt verktyg om det kräver mindre svar.
- Dela inte på syntax- eller kombinationsfel. Stoppa när odelbar del är för stor eller budgeten är slut; spara återstående plan och använd separat batchskript för fortsatt körning. Byt inte till skript som ett dolt sätt att fortsätta över den interaktiva budgeten.

Manifest: `del-id, parent-id, query, filterkoder, status, hämtningstid, rader, tecken, källa/revision om tillgänglig, fel`. Använd status planerad, klar, misslyckad eller ersatt. Markera klar först när innehållet är validerat.

## Sammanfoga och kontrollera

- Normalisera till långform vid behov. Bygg nyckel av produkt, alla dimensionskoder, period, fasta filter, mått och relevanta versionsuppgifter. Lägg till partitionens filter som kolumn om det saknas i svaret. Kontrollera kompatibla kolumner, enheter och definitioner före sammanfogning.
- Lägg samma måtts delar efter varandra som rader. Summera inte delar för att rekonstruera en tabell. Bevara noteringar med del-id; lokala noterings-id:n behöver inte vara globala.
- Logga identiska dubletter innan eventuell deduplicering. Behandla olika värden för samma observationsnyckel som konflikt, inte värden att summera. Om revisionerna ändrats, hämta om berörda delar eller redovisa att jämförbarheten är osäker.
- Kontrollera att varje aktiv planerad del är klar och urvalet täckt utan överlapp. En gles tabell måste inte ha hela kartesiska antalet rader; uteblivna rader är inte automatiskt noll.
- Kontrollera med publicerad total när en jämförbar additiv total finns. Håll totaler skilda från sina underkategorier och bestånd skilda från flöden. Bevara sekretess och saknadmarkeringar.
- Vid ofullständig hämtning, redovisa klara och saknade filterdelar. Presentera inte slutlig totalsiffra från ofullständigt underlag.

Illustration, endast om storleken kräver uppdelning och alla tre år behövs, inte live-verifierat uttag: dela `t10011|itrfslut|ar:2023,2024,2025|drivm` i tre queries med samma produkt/mått/dimensioner men ett år per query. Konkatenera resultaten; summera inte fordonsbestånden över år.
