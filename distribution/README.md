# Distribution och versionsspårning

GitHub `main` är gemensam källa för Trafikanalys API-färdighetens instruktioner, referensmaterial, API-klient och tester. ChatGPT-pluginen **T-stat** (underrubrik: **Officiell statistik om resor och transporter**) och fristående färdigheten ska paketeras från samma granskade Git-commit.

## Releaseprocess

1. Fastställ `skill_commit` (full Git-SHA) och bygg båda paketen från samma revision.
2. Spara ett ifyllt manifest enligt `manifest.template.json` **i varje distribuerat paket**. Ange separat pluginpaketets version, verifierad MCP-serverversion, API-kontraktsversion och synkroniseringstid. Lämna okända fält som `null`.
3. Jämför innehållet eller SHA-256 för `SKILL.md`, `references/resvanor.md` och `references/regional-linjetrafik.md` i båda paketen. Dokumentera avsiktliga plattformsskillnader.
4. Kör offline-regression. Kör därefter beteendetest i ny chatt: (a) fyra resebegrepp utan webbsökning, (b) reselement 2016 kontra 2025, (c) T04021 med exakt API-query och klickbar direktlänk. Notera faktiskt lästa filer och verktygsval. CI verifierar inte automatiskt modellbeteende.
5. Kontrollera MCP-serverns anslutning och behörigheter separat. Återanslutning till servern är inte samma sak som synkronisering av referensfiler.
6. Publicera först när installerad pluginrelease och färdighetens manifest pekar på samma granskade källrevision.

Behåll historiska källangivelser till Trafikanalys. Kontrollera eventuella nya myndighetsnamn och API-värdar innan de ändras i kod eller dokumentation. Ange på produktnivå om en sammanställning inte ingår i Sveriges officiella statistik.

Detta är en distributionsrutin, inte bevis för att en viss pluginrelease redan har uppdaterats.
