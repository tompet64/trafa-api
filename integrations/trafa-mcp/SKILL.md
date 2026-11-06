---
name: trafa-mcp
description: Använd T-stat-pluginens MCP-verktyg för tekniskt validerade anrop till Trafikanalys API. Aktiveras när användaren behöver hämta aktuell statistik eller struktur via MCP. Statistiklogik, produktval, metoddefinitioner och källprioritering styrs av den separat installerade färdigheten trafa-api; denna integration ersätter inte den.
---

# T-stat MCP-integration

Denna färdighet beskriver endast anslutningen till Trafikanalys API via T-stats MCP-verktyg.

## Ansvar och prioritering

- Använd separat installerade `trafa-api` för statistiklogik, produktmetadata, definitioner, urvalsregler, källprioritering, jämförbarhet och resultatkontroll.
- Använd `get_statistics` och vid behov `get_structure` för API-anrop. Kör inte Pythonklienten som mellanled till MCP-servern.
- Kontrollera före en statistikuppgift att den separat installerade `trafa-api` finns tillgänglig och att dess instruktioner kan läsas, innan produkt, mått eller urval fastställs och innan API-anrop görs.
- Om `trafa-api` saknas eller dess instruktioner inte kan läsas: avbryt statistikuppgiften och be användaren installera eller aktivera färdigheten, eller återställa läsåtkomsten. Gör inga `get_structure`- eller `get_statistics`-anrop för uppgiften. Identifiera inte själv produkt, mått eller urval och presentera inga statistikvärden från minne, alternativa källor eller enbart MCP-verktygens tekniska validering. Stoppet gäller även om koderna eller en färdig API-fråga redan är kända. Att enbart redovisa begränsningen är inte tillräckligt för att fortsätta. Påstå inte att otillgängliga instruktioner eller referensfiler har lästs.
- En plugin kan ha integrationsregler som gör att dess instruktioner läses. Påstå därför inte att färdigheterna är fullständigt isolerade utan ett verifierbart test.

## Underagenter och delegering

Använd inte underagenter och delegera inte någon del av uppgiften om användaren inte uttryckligen har begärt sådan delegering för uppgiften. Instruktioner om resultatkontroll, oberoende kontroll eller parallellt arbete innebär inte i sig tillstånd att använda underagenter.

Vid uttryckligen beställd delegering gäller samma källbegränsningar, verktygsbegränsningar och ändringsbefogenheter för alla medverkande agenter. Tillstånd att delegera utökar inte uppdraget eller tillåtna källor och åtgärder. Redovisa vad som delegerades och vilka verktyg, källor och eventuella ändringar underagenterna använde eller utförde. Skilj granskning av samma underlag från oberoende verifiering mot andra underlag eller med en annan kontrollmetod.

## Behörighet och ändringsgränser

- Läsning är standard. Vanliga statistikfrågor, metodfrågor och definitionstolkningar ger inte tillstånd att ändra filer, färdigheter, plugininställningar, pluginpaket, MCP-servern eller GitHub-innehåll.
- Håll dig till den begärda uppgiften och till de källor och verktyg som användaren har tillåtit. Om underlag saknas eller inte kan läsas, redovisa begränsningen och avbryt den delen av arbetet.
- Använd inte underagenter, alternativa verktyg eller webbsökningar för att kringgå uttryckliga källbegränsningar eller utföra obeställda ändringar. Påstå inte att en källa har lästs eller ett uttag har gjorts om det inte har skett.
- När användaren uttryckligen beställer en ändring i projektet ska den förberedas mot GitHub-källan på en separat gren. Ändringar av färdighetsinnehåll ska få ett nytt `skill_version` i manifestet och läggas fram i en pull request för användarens granskning. Lokala ändringar i installerade färdigheter ersätter inte denna process.
- Förberedelser, ändringsförslag och tester innebär inte tillstånd att sammanfoga en pull request, publicera en release eller uppdatera en installerad färdighet, plugin eller MCP-server. Sådana steg kräver separat uttryckligt godkännande.

## Verktygsanrop

Se [references/tools.md](references/tools.md) för parametrar, gränser och teknisk kontroll.

1. Använd produkt, mått, filter och dimensioner som fastställts enligt `trafa-api`.
2. När koderna är kända: anropa `get_statistics` direkt; den gör egen strukturvalidering. Anropa `get_structure` separat endast när det behövs för metadata eller värdekoder.
3. Ange ofiltrerade kategorier i `dimensions` (exempelvis `["fslag"]`), inte som tomma filter. Filtrera tidsdimensionen med konkreta årskoder.
4. Kontrollera `ok`, `DataCount`, `row_count`, `Rows`, `IsTotal`, noter, enheter och felstatus. `max_rows` är inte ett löfte om fullständigt uttag.
5. Bevara exakt `query`, verifierad `source.url`, hämtningstid, serverversion, kontraktsversion och spårningsuppgifter när dessa returneras.
6. Vid nätverksfel, ogiltigt urval eller ofullständigt svar: redovisa felet och avbryt. Byt inte tyst till webbsökning, Python eller en annan datakälla.
7. Gör inte externa webbsökningar för statistikvärden. Följ den fristående färdighetens regler för metodkällor.

## Avgränsning

Inga produktprofiler, metodguider, statistikdefinitioner eller kopior av `trafa-api`s referensfiler ska paketeras i denna integrationsfärdighet. Diagramverktygen är valfria och ingår inte i det obligatoriska API-arbetsflödet.
