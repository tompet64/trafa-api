# Jämför fristående färdighet och installerad MCP-plugin

## Tre skilda frågor

1. **Transportregression:** bevaras urval, koder, tabell och fel när samma
   verifierade sluturval körs genom Python respektive MCP-serverkod?
2. **Levande anslutning:** fungerar installerade verktyg och direktklient just nu?
3. **Assistentens arbetsgång:** väljer assistenten rätt produkt, gör den onödiga
   uppslag eller webbsökningar och blir slutsvaret statistiskt korrekt?

Ett godkänt transporttest besvarar inte fråga 3. Färdigheten är instruktioner;
Pythonklienten är en av dess transportvägar. Ett skript med förutbestämt urval
mäter inte tiden för att använda hela färdigheten. Rapportera nivåerna separat.

## Automatiserat transportreplay

Kör från repositoryts rot:

```bash
python evaluation/run_offline.py
python evaluation/comparison/run_replay.py > replay-direct.json
python evaluation/comparison/run_replay.py --worker /ABSOLUT/SÖKVÄG/worker/index.js > replay-pair.json
```

Det sista kommandot kräver Node 20+ och den verifierade serverkällan, inte en
omskriven kopia av serverns logik. Använd ett separat checkout av den publicerade
serverversionen. Anteckna Git-SHA, kontrollera ren arbetskatalog och jämför med
Sites-versionens `source.commit_sha`. Rapporten registrerar även serverfilens
SHA-256. Importen kör kod: använd endast granskad serverkälla. Replay ersätter
`fetch` och `urlopen` med exakt query-/språkmatchade, befintliga fixturer. Det är
en transportstub, inte en OS-sandbox för godtycklig serverkod.

B01 (elbilsandel) kör täljare och nämnare, B02 (Malmö) kör ändpunkterna, B04
(körkort) två överlappande kategorier, B06 (Finland) en ofiltrerad dimension.
MCP-gränssnittets oförmåga att uttrycka B06 markeras `unsupported`, aldrig som
ett korrekt nollvärde. Jämför hela Header/Rows mot inspelade API-svar; en
numeriskt korrekt tabell är fortfarande inte ett granskat statistiskt slutsvar.

För att återskapa en avsiktligt redundant preflight, lägg till `--preflight`
till kommandot med `--worker`. Denna diagnosgren är inte standardarbetsgång och
visar inte hur ofta assistenten använder mönstret. Jämför endpointlistan med
standardkörningen. En oväntad MCP-error eller ändrad råtabell ger exitkod 1;
`unsupported` redovisas som en kompatibilitetslucka och `raw_data_equal: null`.

Serverns console-loggar samlas separat i `mcp.server_logs`. Standardutmatningen
innehåller fortfarande exakt ett JSON-dokument, även när servern skriver
strukturerade loggar. Med serverversion 0.2.0 finns också serverns eget kvitto i
`mcp.result.trace`; håll dess interna tider skilda från replay-fixturernas
tider. Ett sådant kvitto kan lämnas direkt till trace_report.py. Det täcker
upstream-anrop, medan värdens webbsökningar fortfarande är okända.

Replay registrerar varje HTTP-anrop, query, språk, storlek och varaktighet.
Tiden avser lokal fixturläsning och serverns kvarvarande väntelogik, inte
verklig API- eller ChatGPT-latens. Den ska inte användas för att utse den
snabbaste användarupplevelsen. Nya offline-tester bevakar direktvägens
anropsbudget i just dessa fixerade fall; de föreskriver inte en enda tillåten
arbetsgång för andra frågor. Befintliga T01/T02 testar tomma svar och HTTP 200
med Errors för Pythonklienten; dessa tester bevisar inget om MCP-servern.

## Levande kontroller

Direktklienten kan provas uttryckligen, aldrig som del av vanlig CI:

```bash
python evaluation/comparison/run_direct_live.py --allow-network > direct-live.json
```

Kör samma urval via den installerade pluginens `get_statistics`. Registrera
indata, starttid UTC, förfluten tid vid klientgränsen och fullständigt verktygssvar.
Använd sparade querysträngar i respektive fixturs `.request.json`; inga facitvärden
behöver ges till en kandidat. Dela queryn i produkt, mått och filter enligt
verktygets aktuella schema. Skicka inte en ofiltrerad dimension som ett mått
eller en tom filterlista. Bevara fel och timeout som resultat, inte som saknade
körningar. Följ tjänstens anropsgränser.

Jämför API-värden och metadata först. Revisioner sedan fixturens datum kan vara
legitima; ett avvikande fryst värde är en granskningssignal, inte automatiskt ett
statistiskt fel. Kör inga automatiska uppdateringar av oracle.json.

## Kontrollerad jämförelse av hela arbetsgången

- Återanvänd originalfrågorna B01, B02, B04 och B06 ur cases.json. Lägg till B05
  (RVU-begrepp som kan kräva avstående) och B07 (senaste punktlighet med behov
  av officiellt publiceringsdatum) för att pröva motiverad webbanvändning.
- Kör varje fråga i en ny chatt, med samma modell/version, språk, prompt och
  svarskrav. Ge ingen kandidat facit, tidigare svar eller felhypotes.
- Gör först en jämförelse av **faktiskt installerade system**. Registrera båda
  instruktionernas hash, metadatahashar, pluginrelease och servercommit. Om de
  skiljer sig kan skillnaden inte tillskrivas enbart MCP-transporten.
- För en efterföljande transportisolering: använd identiska instruktioner och
  metadata men växla endast tillgänglig transport. Håll tillgången till webben
  lika. Förbjud inte webben i ena armen om dess användning ska jämföras.
- Kör minst fem parade repetitioner per fråga. Fördela AB/BA i förväg med sparat
  slumpfrö. Rapportera varje observation, median, variationsbredd och parade
  tidsskillnader. Fem par är en pilot, inte ett precist prestationsestimat.
- Håll kall/varm cache separat. Registrera cacheläge som okänt om serverns cache
  inte kan styras. Skilj första uppstart, verktygsupptäckt och eventuell
  godkännandeväntan från statistiksteget. Kassera inte långsamma eller felade
  körningar; redovisa fullföljandegrad och censurerad tid för timeouter.
- Tidtagning: använd en monoton klocka från användarfrågan till färdigt svar.
  Registrera separata spann för produkt-/referensläsning, metadata, HTTP-försök,
  MCP-verktyg, webbåtgärder, beräkning och eventuell rendering. Registrera UTC
  för korrelation. Summera inte överlappande verktygs- och HTTP-spann.
- Bevara originalspår privat före normalisering. Publicera endast relevanta
  query-/timingspår; uteslut autentisering, headers, personuppgifter och andra
  chattar. Logga inte bara lyckade anrop.

## Spårformat och rapportering

`comparison/trace_report.py` läser en normaliserad JSON-fil:

```json
{
  "schema_version": 1,
  "run_id": "B02-mcp-01",
  "case_id": "B02",
  "route": "mcp",
  "total_ms": 2500,
  "coverage": {"host": "partial", "upstream": "complete"},
  "statistical_grade": "unassessed",
  "events": [
    {"id": "tool1", "kind": "tool", "start_ms": 0, "duration_ms": 2000,
     "outcome": "success", "name": "get_statistics"},
    {"id": "http1", "parent_id": "tool1", "kind": "http", "start_ms": 10,
     "duration_ms": 500, "outcome": "success", "endpoint": "structure",
     "query": "t10026|itrfslut|ar:2019,2023|reglan:12|regkom:1280", "lang": "sv"}
  ]
}
```

```bash
python evaluation/comparison/trace_report.py normaliserat-spar.json
```

Tillåtna händelser: `metadata`, `http`, `tool`, `web_search`, `web_open`,
`calculation`, `render`. Alla ska ha unikt id, start_ms och duration_ms från
**samma relativa klocka**, samt outcome: success/error/cancelled/unknown.
HTTP ska ha endpoint, exakt query och lang; format är json om inte annat anges.
Ange `parent_id` för interna anrop och `attempt` för omförsök. Lägg till
`source`, `sha256` och relevanta variabelnamn för lokala metadatauppslag.
För webbåtgärder: ange domän/URL eller sökfråga samt `reason` för den konkreta
informationsluckan. Lägg till saknade dokumentationsuppgifter som hittades och
om sökningen ändrade produktval eller slutsats i granskningsanteckningen.

Coverage är `complete`, `partial` eller `unavailable` per lager. Saknad coverage
betyder okänd täckning. Utan fullständigt värdspår är antalet webbåtgärder okänt,
inte noll. Utan fullständiga serverspår är antal interna HTTP-anrop okänt.
En MCP-källhänvisning för data listar inte automatiskt strukturhämtningen.
Matcha klient- och serverloggar med korrelations-id; blanda inte deras klockor
utan känd offset. `observed_busy_ms` är unionen av observerade spann, inte total
svarstid eller en skattning av modellens tänketid. Återstående tid kan även
omfatta nätverk, köer och loggluckor.

Rapporten flaggar upprepade **lyckade** identiska HTTP-förfrågningar efter
endpoint, query, språk och format. Bedöm sedan motivering, cacheläge och
revisionsrisk. Misslyckat försök följt av retry är inte samma sak som en
onödig dubbelhämtning. Alternativa queryordningar kan vara semantiskt likvärdiga
utan att flaggas; normalisera dem först efter produktgranskning.

Bedömaren använder befintliga fallrubriker och oracle separat. B01 kräver rätt
nämnare; B02 rätt år och förändring; B04 får inte kalla 102,4 procent en union;
B06 får inte generalisera 3 021 000 till alla skeppstyper. B05 kan korrekt avstå.
Bedöm korrekthet, täckning, begrepp, enheter och källspår före hastighet. Ett
snabbt felaktigt svar är inte en förbättring. Markera statistisk bedömning
pass/fail/unassessed; rapportverktyget bedömer inte fri svarstext automatiskt.

## Vad som kan köras var

| Kontroll | GitHub utan hemligheter | Kräver ytterligare åtkomst |
|---|---|---|
| Pythonregression, metadata-JSON, anropsbudget, rapportlogik | Ja, befintliga fixturer | Nej |
| Replay av MCP-kod och dess interna fetch-anrop | Ja om granskad serverkälla görs tillgänglig | Nu separat Sites-källa |
| Installerade MCP-verktyg | Nej i nuvarande CI | Autentiserad ChatGPT-anslutning |
| Faktisk metadata-/API-tid, kö och cache i servern | Inte från befintliga klientkvitton | Instrumenterade serverspår |
| Modellens metadata- och webbval | Nej i nuvarande CI | Fullständiga värd-/verktygsspår eller kontrollerad kandidatmiljö |
| Statistisk giltighet i slutsvaret | Delvis numerik, inte semantik | Separat sakkunnig bedömning |

Serverloggarna som nu är åtkomliga visar invokation, verktygsnamn, HTTP-status,
wallTimeMs och cpuTimeMs, men inte interna upstream-spann. HTTP 200 på /mcp
bevisar inte `result.isError=false`. Loggarna kan inte visa ChatGPT:s externa
webbsökningar. Komplettera servern med request-id, verktygs-/serverversion,
query, endpoint, försök, cacheutfall, kötid, API-tid, byteantal och felstatus.
Behåll värdens spår som separat källa. Inför inte hemligheter i vanlig PR-CI.
