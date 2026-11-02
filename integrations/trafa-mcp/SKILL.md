---
name: trafa-mcp
description: Använd T-stat-pluginens MCP-verktyg för tekniskt validerade anrop till Trafikanalys API. Aktiveras när användaren behöver hämta aktuell statistik eller struktur via MCP. Statistiklogik, produktval, metoddefinitioner och källprioritering styrs av den separat installerade färdigheten trafa-api; denna integration ersätter inte den.
---

# T-stat MCP-integration

Denna färdighet beskriver endast anslutningen till Trafikanalys API via T-stats MCP-verktyg.

## Ansvar och prioritering

- Använd separat installerade `trafa-api` för statistiklogik, produktmetadata, definitioner, urvalsregler, källprioritering, jämförbarhet och resultatkontroll.
- Använd `get_statistics` och vid behov `get_structure` för API-anrop. Kör inte Pythonklienten som mellanled till MCP-servern.
- Om `trafa-api` inte finns tillgänglig, påstå inte att dess referensfiler eller instruktioner har lästs. Be om installation eller redovisa begränsningen. Gör inte semantiska antaganden enbart utifrån verktygens tekniska validering.
- En plugin kan ha integrationsregler som gör att dess instruktioner läses. Påstå därför inte att färdigheterna är fullständigt isolerade utan ett verifierbart test.

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
