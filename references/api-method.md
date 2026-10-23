# Anrop och källor

Använd server och operationer i `openapi-trafa.json`: `https://api.trafa.se/api` med `/structure` för urvalets metadata och `/data` för statistik. Bygg `query` enligt `produkt|mått|dimension|dimension:kod1,kod2`. En dimension utan kolon och värdekoder, exempelvis `|fslag`, tas med i svaret utan att begränsas till en värdemängd; `|fslag:` med tomt värde är inte samma sak och ska inte användas. Kontrollera alltid i aktuell struktur och produktdokumentation att den redovisningsdimensionen är tillåten tillsammans med måttet och övriga urval. När alla kategorier efterfrågas behövs ingen förhandsgranskning av alla produkter: gör kontrollen för det valda uttaget. Om anslutningen inte kan representera en ofiltrerad dimension, använd direktklienten om den är tillgänglig; annars ange begränsningen. Skicka `lang=sv` eller `lang=en` efter behov. Använd HTTP-klientens parametervärden för URL-kodning.

Illustration från officiell beskrivning: `t10011|itrfslut|ar|pass`. Kontrollera koder och kombination enligt vald metadataväg innan återanvändning. Lägg på ett val i taget i struktur när aktuell valbarhet behöver utforskas och svaret ryms.

Begär JSON med `Accept: application/json` när klienten stöder det; kontrollera faktiskt returformat. Den medföljande klienten och kontraktet stödjer JSON. XML kräver en separat verifierad adapter med namnrymdshantering och motsvarande semantik; försök inte tolka det som JSON eller som ett storleksfel. Ett formatbyte garanterar inte ett mindre svar. Spara rå metadata lokalt när det behövs, men läs endast relevanta utdrag i kontext.

Vid fel: skilj felaktig kod, syntax, ogiltig kombination, storleksfel, tomt urval, format-/schemafel och tillfälligt tjänstefel. Kontrollera exakt Name och vald metadatakälla; gissa inte koder. Vid 429 följ Retry-After om tillgängligt; begränsa återförsök till tre och använd ökande väntetid. Klienten stoppar om en numerisk Retry-After överstiger 30 sekunder. Gör inte upprepade identiska för stora anrop. Automatisk referensfallback får bara utlösas av belagd överskriden strukturbudget. HTTP-fel och `Errors` i ett JSON-svar stoppar uttaget; de blir inte valideringsgodkännanden.

## Nätverk och behörigheter

Välj först en API-anslutning eller körmiljö som faktiskt är tillgänglig. Vid det första nödvändiga API-anropet via ett körverktyg, begär `sandbox_permissions="require_escalated"` om verktyget stöder det och miljön tillåter sådan prövning. Vänta då inte på ett misslyckat standardförsök. Detta är ett argument till körverktyget, inte en Pythoninställning, HTTP-parameter eller del av OpenAPI-kontraktet. En redan tillgänglig Action använder sin egen anslutningsbehörighet.

Respektera ett avslag och gör inte samma blockerade åtgärd via en annan väg. Fortsätt med tillåtet offlinearbete om det hjälper. Ange exakt om körverktyget saknas, utökad behörighet inte är tillgänglig, behörighetsprövningen avslås, nätverksanslutningen misslyckas eller API-servern returnerar ett fel. Ange serverfel endast när ett faktiskt HTTP- eller API-svar finns. Ett storleksfel i anslutningen är inte automatiskt ett serverfel. Påstå inte att aktuell statistik har hämtats efter ett blockerat anrop.

## Källhierarki

- Aktuell struktur och svar för valt urval: primär källa för koder, valbarhet och data.
- Produktdokumentation: definitioner, variabler och kombinationer, https://www.trafa.se/sidor/api-dokumentation/ . Produktinnehållet kan laddas dynamiskt; en sida utan vald produkt innehåller inte dess kombinationslista.
- Teknisk beskrivning: https://www.trafa.se/globalassets/ovriga-dokument/api-beskrivning.pdf . Läst 2026-10-07. Beskrivningen är inte en ny verifiering av varje produkt.
- Daterad strukturkatalog, värdemängder och dokumenterade kombinationer: sökhjälp samt valideringsunderlag enligt metadata-routing.md; ingen garanti om aktuell valbarhet eller datatäckning.
- Äldre eller ofullständiga kataloger och arbetsinstruktioner: sökhjälp och lokala metodregler.

Använd aktuell åtkomlig dokumentation vid ändrade förutsättningar. Produktlistan, representativa datasvar och den korrigerade strukturkatalogen verifierades 2026-10-09. Produktlistan har 56 statistikprodukter efter att testprodukten atft uteslutits. Äldre katalog hade flera identiska titlar, bland annat Personbilar och Bussar; lagra inte deras tänkta avgränsningar som fakta. Katalogens berikningar är fortfarande förslag.

## Direkt körning utan rutinmässig hjälp- eller filinventering

När scriptsökvägen är känd, använd direkt:

```bash
python3 scripts/trafa_client.py structure --query 'EXAKT_QUERY' --raw /tmp/urval.structure.json --names relevanta_koder
python3 scripts/trafa_client.py data --query 'EXAKT_QUERY' --structure /tmp/urval.structure.json --raw /tmp/urval.data.json
```

Kör från färdighetens rot eller använd dess absoluta sökväg. Anpassa filnamn per urval. Klienten sparar begäransloggen och kontrollerar matchningen mellan struktur och data. Exemplen använder strukturvägen. Läs relevant produktreferens och begränsade metadatadelar först; kör inte --help eller upprepade filinventeringar som standard. Använd dem bara vid konkret oklarhet eller fel. Ange `--rows 10` för ett begränsat utdrag av cellvärden; läs bara nödvändiga rader/celler ur råfilen för fortsatt analys.

## Samlad körning och begränsad metadata

Använd i normalfallet `python3 scripts/trafa_client.py extract --query 'EXAKT_QUERY' --raw /tmp/uttag.json --rows 10`. Kommandot väljer metadataväg och validerar före data. Standard för direkt Python är aktuell struktur utan förinställd teckenbudget. Ange en budget för en begränsad anslutning eller välj referensvägen uttryckligen enligt metadata-routing.md. Spara rådata, begäransloggar för gjorda anrop och valideringskvitto. Vid aktuell DataCount 0 sker inget dataanrop; referensvägens DataCount är okänd. Vid felsökning kan separata structure/data fortfarande användas.

Metadata: `metadata_lookup.py --product t1203 --section combinations --variables pastig finans traslag`; läs sedan bara relevanta variabler med `--variables ... --values`. `--section profile` visar sakprofil, `--section all` det äldre fullständiga formatet. En lista över flera mått i dokumentationen betyder inte automatiskt att samtliga krävs; testa bara nödvändiga mått tillsammans med rätt redovisningsdimensioner.
