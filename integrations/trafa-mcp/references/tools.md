# T-stat MCP-verktyg

## `get_statistics`

Parametrar: `product` (produktkod), `measures` (1–4 mått), `filters` (kod till värdelista), `dimensions` (0–8 ofiltrerade dimensioner), `time_dimension` (tidskod), `max_rows` (1–200, standard 100), `lang` (sv/en).

Exempel: `product:"t10030", measures:["nyreg"], filters:{ar:["2025"]}, dimensions:["fslag"], time_dimension:"ar"` ger `t10030|nyreg|ar:2025|fslag`.

`get_statistics` kontrollerar aktuell struktur och tillåtna kombinationer före datahämtning. Separat `get_structure` behövs normalt inte för ett redan känt giltigt urval.

## `get_structure`

Parametrar: `product`, valfria `measures`, `filters`, `dimensions`, `variable`, `offset` (0–20000), `limit` (1–100), `lang`. Använd för aktuell produktstruktur eller paginerade värdekoder när metadata saknas.

## Svarskontroll

Kontrollera `ok`, `DataCount`, `row_count`, `Header`, `Rows`, `Notes`, `IsTotal`, `source.query`, `source.url` och `trace`. `trace.elapsed_ms` är serverns tid, inte hela ChatGPT-svarstiden. `trace.upstream_count` anger interna uppströmsanrop; `structure_cache.status` anger cacheutfall. Saknad eller begränsad täckning ska redovisas, inte döljas.

## Versionsgränser

MCP-serverversion och API-kontraktsversion är inte versioner av `trafa-api`. Kontrollera separat installationsmanifest för att intyga färdighetsversion. Förändringar av MCP-verktygens schema kräver översyn av denna fil; statistikmetod hör till `trafa-api`.
