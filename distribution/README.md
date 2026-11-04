# Distribution och versionsspårning

GitHub `main` är gemensam källa för Trafikanalys API-färdighetens instruktioner, referensmaterial, API-klient och tester. ChatGPT-pluginen **T-stat** (underrubrik: **Officiell statistik om resor och transporter**) och fristående färdigheten ska paketeras från samma granskade Git-commit.

## Granskning och versionsnummer

Alla ändringar ska först finnas på en separat GitHub-branch och i en pull request. Tom granskar och sammanfogar pull requesten innan den installerade färdigheten eller pluginen uppdateras.

`manifest.json` är källmanifestet. Varje ändring av färdighetens innehåll får ett nytt `skill_version` i samma pull request. Det första ifyllda källmanifestet anger den föreslagna färdighetsversionen `1.1.4`. `release_status: "unreleased"` betyder att versionen ännu inte intygas som distribuerad. `skill_commit` och `synced_at` lämnas som `null` tills den granskade revisionen har fastställts och paketeringen verifierats. Källmanifestet uppdaterar inte installerade paket.

Manifestformatet är `1.1`, utökat med `skill_version` och `release_status`. I ett verifierat distributionsmanifest anges `release_status: "released"` och aktuell distribution. `plugin_version` avser en faktiskt verifierad pluginrelease och får ett nytt versionsnummer när pluginen uppdateras; det lämnas som `null` i källmanifestet när pluginuppdateringen återstår.

## Releaseprocess

1. Fastställ `skill_commit` (full Git-SHA) och bygg båda paketen från samma revision.
2. Spara ett ifyllt manifest enligt `manifest.template.json` **i varje distribuerat paket**. Ange färdighetens version från källmanifestet samt separat pluginpaketets version, verifierad MCP-serverversion, API-kontraktsversion och synkroniseringstid. Lämna okända fält som `null`.
3. Verifiera att båda paketen bygger på samma granskade Git-revision enligt manifestens `skill_commit`. Kontrollera innehåll och SHA-256 för `SKILL.md`, `references/resvanor.md` och `references/regional-linjetrafik.md` i det fristående `trafa-api`-paketet mot motsvarande filer i källrevisionen. Kontrollera separat att pluginpaketet använder `trafa-mcp` från `integrations/trafa-mcp/` i samma revision, saknar inbyggd `trafa-api` och duplicerade statistikmetadata, metodguider och statistikreferensfiler samt bevarar nödvändig MCP-konfiguration. De två `SKILL.md`-filerna ska jämföras mot respektive källa, inte mot varandra. Dokumentera de avsiktliga skillnaderna mellan paketen.
4. Kör offline-regression. Kör därefter beteendetest i ny chatt: (a) fyra resebegrepp utan webbsökning, (b) reselement 2016 kontra 2025, (c) T04021 med exakt API-query och klickbar direktlänk. Notera faktiskt lästa filer och verktygsval. CI verifierar inte automatiskt modellbeteende.
5. Kontrollera MCP-serverns anslutning och behörigheter separat. Återanslutning till servern är inte samma sak som synkronisering av referensfiler.
6. Publicera först när installerad pluginrelease och färdighetens manifest pekar på samma granskade källrevision.

Båda distributionsmanifesten ska ange samma fullständiga `skill_commit`. Deras `skill_version` ska motsvara källmanifestet i den revisionen. `distribution` ska identifiera respektive paket; paketens innehåll och `plugin_version` behöver inte vara identiska. Samma versionsnummer eller godkänd CI räcker inte för att styrka gemensamt källursprung: verifiera filerna mot den angivna revisionen. Okänd källrevision innebär att kontrollen inte är godkänd.

Använd befintliga `notes` i respektive distributionsmanifest för att hänvisa till ett paketspecifikt kontrollprotokoll som följer med paketet; ange protokollets relativa sökväg och SHA-256. Protokollet ska redovisa källrevision, mappning mellan paket- och källsökvägar, kontrollerade filers SHA-256 och avsiktliga skillnader. För pluginens MCP-konfiguration (`.app.json`, pluginmanifest och anslutningsinställningar) ska det även ange vilken godkänd konfigurationsbas som jämförelsen gjorts mot och kontrollresultatet; dessa filer förutsätts inte finnas i `trafa-api`-källan. Dokumentera konfiguration utan hemligheter. Ingen ändring av manifestformatet krävs.

Automatiska paketkontroller ska verifiera filstruktur, manifestens JSON-struktur och obligatoriska värden, gemensam källrevision, filhashar, avsaknad av duplicerade statistikreferenser och bevarad MCP-konfiguration. De ersätter inte offline-regressionen, de manuella beteendeacceptansfallen (inklusive integrationsgränser) eller den separata kontrollen av MCP-anslutning och behörigheter.

Behåll historiska källangivelser till Trafikanalys. Kontrollera eventuella nya myndighetsnamn och API-värdar innan de ändras i kod eller dokumentation. Ange på produktnivå om en sammanställning inte ingår i Sveriges officiella statistik.

Detta är en distributionsrutin, inte bevis för att en viss pluginrelease redan har uppdaterats.

## Föreslagen separat MCP-integration (från källversion 1.1.5)

`integrations/trafa-mcp/` är en separat minimal färdighet avsedd för T-stat-pluginen. Den innehåller enbart tekniska MCP-instruktioner och inga kopior av statistikmetadata. `trafa-api` förblir fristående och styr statistiklogik, metod och källprioritering. Vid framtida pluginpaketering ersätts pluginens inbyggda `trafa-api` av `trafa-mcp`; MCP-konfigurationen (`.app.json`, pluginmanifest och anslutningsinställningar) ska bevaras oförändrad.

Detta är en föreslagen målarkitektur, inte en utförd pluginuppdatering. Förutsättningen att pluginen kan använda en separat installerad `trafa-api` är funktionellt testad, men konsekvent instruktionsprioritet och automatisk tillgänglighet för andra användare är inte bevisad.

Före release: bygg och inspektera ett pluginpaket med enbart `trafa-mcp`; verifiera att `get_statistics` och `get_structure` fungerar; kör RVU 2016/2025 utan API-anrop samt T10030 2025 med ofiltrerad `fslag`; dokumentera lästa färdigheter, API-fråga, täckning, svarstid och fel. Testa också användning utan separat installerad `trafa-api` och säkerställ att ingen statistikmetod uppfinns. Uppdatera därefter distributionsmanifest och pluginversion från verifierad release.
