# JSON-kontrakt och klient

## Schema och verifieringsläge

Använd `openapi-trafa.json` som kanoniskt OpenAPI 3.1.0-kontrakt, version 2.1.0. JSON ersätter den tidigare YAML-filen så att både en OpenAPI-anslutning och Pythonklienten kan läsa samma fil utan ett extra YAML-paket. Behåll en enda kontraktskälla.

Version 2.0.0 byggde på 56 sparade strukturuttag inklusive ett tomt svar, produktlistan samt representativa datasvar och ett medvetet felsvar, verifierade 2026-10-09. Version 2.1.0 bevarar svarsfälten och förtydligar anropsvillkor och referensvägen. Dess nya klientkontroller provas med lokala tester; detta innebär inte en ny hämtning av samtliga produktstrukturer. Kontraktet är inte en heltäckande specifikation av framtida svar. XML-formatets serialisering ingår inte.

- `/structure`: utelämna `query` för produktlistan. Använd `lang=sv` eller `lang=en`.
- Följ både rekursiva `StructureItems` och `ParentName`. Variablerna kan ligga som rotens syskon till produktposterna; en vald P-post kan ha tom barnlista trots fullständig produktstruktur.
- Bevara typerna P, D, H, M, DV och F. DV-koder är strängar. F är dynamiska filter; expandera inte `senaste` till en fast kod utan aktuell kontroll.
- Skilj Selected från Option. Selected anger gjorda val; Option anger valbarhet för aktuellt urval. Återanvänd inte en generell produkts Option-värden som godkännande av en ny kombination.
- `DataCount` är inte antal strukturposter. Ett rent produktanrop gav 0; ett sluturval med en observation gav 1. Använd det som storleksindikator tillsammans med jämförbara datasvar, inte som ensam garanti eller teckenbudget.
- `Header.Column` beskriver kolumnerna; `Rows[].Cell[].Column` kopplar cell till kolumn. Mätvärden kan ligga som numeriska strängar i Value. FormattedValue kan innehålla formatering och ska inte användas i beräkningar.
- Unit kan vara tom trots att klartextetiketten anger tusental. Fastställ multiplikator från måttets definition/etikett och dokumentera den separat.
- HTTP 200 kan innehålla Errors. Vid Errors, stoppa uttaget. Vid Rows=[] och Errors=null, utred urvalet; likställ inte med noll eller säker datalucka.
- Behåll Notes, NoteIds och Versions där de finns. Schemat tillåter nya fält med additionalProperties; schema-godkännande ersätter inte semantisk granskning.

## Klient

Använd `scripts/api_contract.py` via `trafa_client.py`. Kontraktet bestämmer server, sökväg, HTTP-metod, tillåtna parametrar och JSON-format. Klienten kontrollerar svarens struktur innan semantisk urvalsvalidering eller resultattolkning. Spara kontraktets version och SHA-256 i begäranslogg och valideringskvitto.

Behandla den inbyggda validatorn som stöd för just kontraktets uttryckliga schema-del: lokala `$ref`, typer inklusive null, obligatoriska fält, objekt, arrayer, `enum`, `anyOf`, `minLength` och `additionalProperties`. Den avvisar okända schemaegenskaper vid inläsning. Den är inte en generell OpenAPI- eller JSON Schema-motor. Utöka validatorn och testerna innan kontraktet börjar använda fler egenskaper.

Kör från skillens rot eller använd absoluta skriptvägar. Exempel:

```bash
python scripts/trafa_client.py structure --query 't10026|itrfslut|ar:2023|reglan:01|drivmedel:103' --raw /tmp/trafa-structure.json --summary /tmp/trafa-structure-summary.json --names reglan drivmedel --values
python scripts/trafa_client.py data --query 't10026|itrfslut|ar:2023|reglan:01|drivmedel:103' --structure /tmp/trafa-structure.json --raw /tmp/trafa-data.json --summary /tmp/trafa-data-summary.json
```

Råsvaret och en `.request.json`-logg sparas. Vid strukturvägen kräver live-data exakt samma query/språk som den sparade strukturbegäran och matchande filhash. Kontrollera aktualitet före återanvändning. Vid uttrycklig referensväg krävs i stället ett godkänt daterat referensunderlag för exakt query före anropet. Spara `.validation.json` för båda vägarna. `--input` läser ett tidigare svar utan nätverk. Klienten partitionerar eller aggregerar inte själv.

Läs endast sammanfattningen i kontext, eller välj variabler med `--names`. `--values` inkluderar deras värden med Selected, Option och ParentName. En tom struktur ger bara en tom produktlista i sammanfattningen; validering av ett efterföljande dataurval avvisar den.

## Användning som Action eller annan API-anslutning

Importera kontraktet i en miljö som faktiskt stöder OpenAPI-baserade anrop och följ dess registreringsflöde. Att placera filen i `references/` eller ändra dess filformat skapar ingen Action. Kontrollera de exponerade operationerna, att JSON faktiskt returneras och att ett litet struktur- och datauttag fungerar. Använd inte en påhittad parameter för format eller en ospecificerad proxy för att få importen att se fungerande ut.

Låt färdighetens arbetsgång välja och dokumentera metadataväg före statistikoperationen. OpenAPI-kontraktet beskriver anrop och svar; produktens kombinationsregler och kravet på föregående validering behöver fortfarande genomföras av klienten eller assistentens arbetsgång. Pythonkoden är en fristående implementation, inte ett krav för att använda en redan installerad Action.

GPT Actions produktionsdokumentation anger svar under 100 000 tecken och en tidsgräns på 45 sekunder. Den tillåter inte godtyckliga egna headers. Pythonklienten kan sätta `Accept: application/json`; en Action måste verifieras med sina faktiska formatmöjligheter. Använd 80 000 tecken som lokal marginal när denna anslutning används, inte som en universell API-gräns. Pythonklientens timeout gäller blockerande nätverksoperationer och är ingen garanti om ett helt arbetsflödes tid. Kontrollera aktuella anslutningsvillkor vid installation eller byte av miljö.

Tekniska källor: [OpenAI, GPT Actions production notes](https://developers.openai.com/api/docs/actions/production), [Python, urllib.request](https://docs.python.org/3/library/urllib.request.html). Använd en anslutning endast om miljön faktiskt erbjuder den; kontraktet ändrar inte miljöns nätverksbehörigheter.

## Metadata och dokumenterade kombinationer

Använd `scripts/metadata_lookup.py` för sökning och relevanta domäner. Kompakt katalog och gemensamma värdefiler i `references/metadata/` bygger på API-strukturen; HTML-tabellernas utelämnade värden är reparerade. Historiska HTML-anmärkningar och berikningsförslag har inte förvandlats till godkända definitioner.

`references/metadata/kombinationer.json` innehåller tidigare dokumenterade kombinationsrader, grupperade per produkt och med källa. Använd dem för att finna kandidater och som ett av de obligatoriska underlagen vid daterad referensvalidering. Följ metadata-routing.md; ändra inte historisk källstatus till ett påstående om ny API-verifiering. T10020 kompletterades med 24 dokumenterade kombinationsrader 2026-10-09. Produktroll, geografisk adressanknytning och periodavgränsning har sakgranskats av användaren. Publiceringsfrekvens och biltäthetens befolkningsreferens har också kompletterats. Biltäthetens täljare inkluderar juridiskt ägda personbilar enligt användarens kompletterande citat. Fullständiga populationsavgränsningar återstår. Granskade tillägg och deras källor finns i `references/metadata/berikningar_manuella.json`.

Verifierade små observationer 2026-10-09:

- `t10026|itrfslut|ar:2023|reglan:01|drivmedel:103`: en rad, 103982 personbilar med el i trafik vid årets slut i Stockholms län.
- `t10036|ar:2025,2018|manad:forra|nyreg`: november inom båda åren. Detta bevisar inte motsvarande beteende för alla produkter, kvartal eller ofullständiga år.
- Samma personbilsuttag utan ar gav HTTP 200, Rows=[] och Errors=null. Ange avsedd tid; påstå inte att API:t alltid ger ett uttryckligt fel när ar saknas.

Källor: Trafikanalys officiella API-beskrivning, https://www.trafa.se/globalassets/ovriga-dokument/api-beskrivning.pdf (läst 2026-10-09), uppladdade råsvar och API-verifiering 2026-10-09. Underlaget använder ingen trafapy-kod.
