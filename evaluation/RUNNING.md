# Första regressionssviten, edition 2026-10-19.1

Sviten gäller färdigheten trafa-api och dess fristående klient. Den är inte en
testsvit för biblioteket TrafaPy. `baseline.json` låser ursprungligt Git-commit
och SHA-256 för färdighetens samtliga ursprungliga filer. Den granskade bundlen
har samma funktionella innehåll; endast ikonen skiljer sig.

## Kör deterministiska tester utan nätverk

Kör från färdighetens katalog med Python 3.9 eller senare:

```bash
python evaluation/run_offline.py
```

För en separat checkout av basversionen, sätt `TRAFA_SKILL_ROOT` till den
katalog som innehåller basversionens SKILL.md. Fixturer och testkod kommer
fortfarande från denna evaluationskatalog. Inga extra paket behövs.

Runnern blockerar Python-socketanslutningar och DNS i huvudprocessen och dess
Python-underprocesser. Den ersätter inte en operativsystemsandbox för godtyckliga
externa program. All testdata är lokal. Rutinmässig CI får inte starta collect.py
eller uppdatera referenssvar. Insamlingsskript ingår avsiktligt inte i testkörningen.

- 86 äldre kodtester i scripts/.
- 9 nya klient-/kontraktstester i test_baseline.py.
- 3 separata kontroller av facitpaketets konsistens i test_oracle_integrity.py.

Transportreplay måste matcha exakt URL-query för att välja rätt inspelade bytes.
Det kravet gäller fixturidentifiering i kodtestet, inte hur assistenten måste lösa
statistikfrågan. Numeriska facitvärden är snapshots, aldrig allmänna konstanter.

## Kör beteendefallen separat

`cases.json` innehåller tio beteendefall och fem tekniska fall. B07–B10 är
punktlighetsfall med frysta API-svar, strukturuttag, valideringskvitton,
anropsloggar och parafraserade utdrag ur officiella definitioner och
publiceringsnotisen.
Starta varje kandidat i en ny tråd med en oförändrad basversion. Ge kandidaten
endast originalfrågan, färdigheten och tillåtna råkällor. Låt kandidaten välja
produktväg och beräkningar. Visa inte oracle.json, fallens bedömningsrubrik,
tidigare svar, misstänkt fel eller graderingsresultat. Lägg inte facit i den
katalog som kandidaten normalt inventerar. De första körningarna använde
separata agenttrådar utan ärvd chatthistorik. Inga beteendefall gjorde nätanrop.

Exempel på kandidatprompt för B01 (byt frågan och ge endast tilldelade råkällor
för respektive fall):

> Använd den oförändrade trafa-api-färdigheten i BASVERSION för att besvara:
> Hur stor andel av nyregistrerade personbilar var elbilar i september 2026?
> Sparade API-svar och anropsloggar finns i RÅKÄLLOR. Arbeta utan nätverk.
> Läs endast BASVERSION och RÅKÄLLOR. Spara ditt svar och en kort logg.
> Ange om underlaget inte räcker. Ändra inga färdighetsfiler.

Tekniska scenarier tilldelas enligt följande. Använd den fullständiga
ursprungsfrågan från B01/B02, inte bara ett internt fall-ID.

| Fall | Tilldelat underlag |
|---|---|
| T01 | B01; ev.structure.json med DataCount 1, men synthetic/empty-data.json som enda datasvar. |
| T02 | B01; ev.structure.json och HTTP 200 med synthetic/http200-errors.json som enda datasvar. |
| T03 | B01; kandidatquery med drivm:NOT_A_CODE och endast ordinarie referensmetadata. |
| T04 | B02; malmo.json, dess struktur/logg och synthetic/years.json; fråga också efter domänens min/max-år. |
| T05 | B01; kopiera referensmetadata till en temporär rot, ta bort T10036 ur kombinationer.json och tilldela endast den roten för validering. Inga struktursvar eller data. |

Kandidaten får inte använda vanliga lyckade datasvar i T01–T03/T05. T05 får inte
ersätta den tilldelade referensroten med andra kataloger. Avsaknad av nätverk är
ett dokumenterat testvillkor, inte något som kandidaten ska kringgå.

För B07–B10 ska kandidaten få endast de råuttag och definitioner som respektive
fall behöver. B07 ska få de fyra punktlighetsutragen och
`fixtures/official/punktlighet-q3-2026-publiceringsnotis.json`; B08 ska dessutom
få `fixtures/official/punktlighet-kvalitetsdeklaration-2025.json`. B09 behöver
RT-uttaget och kvalitetsdeklarationen. B10 behöver publiceringsnotisen. Använd
inte de frysta värdena som facit för andra perioder.

En separat bedömare får sedan fallrubrik, oracle.json, primärkällor och
kandidatsvar. Bedöm slutsatsernas statistiska giltighet, numerik och spårbarhet.
Godta likvärdiga produktvägar och avrundningar. Kräv inte specifika ord, en viss
klient, antal anrop eller queryordning. Behåll godkänt/underkänt/ej bedömbart
separat från kodtesternas resultat. En agent som avstår från en obelagd siffra
kan vara korrekt. En lyckad parserkörning är inte ett lyckat beteendetest.

## Källor och granskningsgräns

`sources.json` innehåller exakt endpoint, query, språk, URL, hämtningstid,
svarshash, storlek och motivering för varje fångat API-svar. Där finns också
definitionskällor med edition, lokaliseringsstöd och källstatus. Fulla
requestloggar ligger intill råsvaren. `fixtures/synthetic/manifest.json` skiljer
konstruerade fel från observerade API-svar. Syntetiska fall har ingen påstådd
API-hämtningstid.

Facitnumerik är självständigt avläst från primära Cell-värden och kontrollerad
med Decimal, utan att använda kandidatsvaren eller klientens sammanfattning
som sanning. Facitets statistiska begränsningar är uttryckliga: ren malm,
A/B-union, RVU-bussdelresor och total över alla skeppstyper är inte numeriskt
fastställda. KI-fältets representation har bevarad expertproveniens; den är
inte nydokumenterad av API-etiketten ensam.

Årspublikationen Lastbilstrafik 2023 avser undersökningens kalenderveckor,
normalt 364 dagar, enligt kvalitetsdeklaration 1.2.5. Kalla inte dess årsvolym
en exakt dag-för-dag-summa för 1 januari–31 december utan ytterligare stöd.

Detta är en enstaka körning per beteendefall med förberedda råkällor.
Den testar inte öppen metadatasökning från noll, webbfallback, en installerad
MCP-anslutning, annan modellversion eller statistisk framgångsfrekvens över
upprepade körningar. Upprepa i nya trådar vid förändringar. Bevara originalspår
innan en produktionsrättning görs; ändra aldrig facit för att få gröna tester.

## Jämför direktklient och MCP

Se [COMPARISON.md](COMPARISON.md) för reproducerbart transportreplay,
normaliserade spår, levande kontroll och separat beteendeprotokoll. Den nya
GitHub Actions-konfigurationen kör hela offline-sviten på Python 3.10, 3.12 och
3.13. Den testar inte automatiskt en installerad plugin eller modellens
webbval. Se också [granskningen 2026-10-24](comparison/FINDINGS-2026-10-24.md).
