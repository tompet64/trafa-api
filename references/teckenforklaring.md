# Teckenförklaring för Trafikanalys statistik

| Tecken | Betydelse | Hantering |
|---|---|---|
| `..` | Uppgift inte tillgänglig eller alltför osäker | Bevara markeringen. Ersätt inte med noll. |
| `.` | Uppgift kan inte förekomma | Bevara som ej tillämplig. Ersätt inte med noll. |
| `–` / `-` | Noll (inget finns att redovisa) | Använd exakt 0 vid beräkningar av uppräkningsbara antal; bevara originaltecknet och dokumentera omkodningen. |
| `0` i en avrundad publicering | Mindre än hälften av enheten, men större än noll | Tolka inte som exakt noll. Kontrollera skala och avrundning. |
| `U` | Undertryckt uppgift på grund av röjanderisk; belagt på Trafikanalys sida om punktlighet | Bevara skyddsmarkeringen. Återskapa eller uppskatta inte ett undertryckt värde. |
| `p` | Preliminär uppgift; belagt i Trafikarbete på svenska vägar, publicering 2026-04-17 | Bevara status med värdet; tolka inte som en fristående siffra. |
| `k` | Korrigerad uppgift | Bevara korrigeringsmarkeringen med värdet. |
| `r` | Reviderad uppgift | Bevara revisionsmarkeringen med värdet. |
| `xxx` samt horisontell/vertikal linje | Betydande skillnad i jämförbarheten i en tidsserie | Markera tidsseriebrott och utred jämförbarhet före förändringsberäkning. |

## Produktspecifika, historiska och obekräftade varianter

| Tecken | Källäge | Regel |
|---|---|---|
| `0,0` | Belagt som avrundningsmarkering i SIKA:s Sjöfartsföretag 2005, tryckt sida 4. Inte belagt i de två insända 2025-legenderna. | Tolka enligt aktuell produkts precision och enhet, inte automatiskt som exakt noll. |
| `*` | Preliminärmarkering i samma historiska SIKA-publikation, numera arkiverad på trafa.se. Inte därmed belagd som generell aktuell Trafikanalys-regel. | Kräv stöd i den aktuella produktens legend eller not. En asterisk kan också hänvisa till en fotnot. |
| `...` | Användaren har återgett betydelsen sekretess i en annan, ej identifierad förklaring. Den riktade kontrollen har inte verifierat denna betydelse i Trafikanalys egna källor. | Bevara som okänd/ej numerisk tills produktens förklaring har kontrollerats. Varken noll eller bevisad sekretess. |
| `—` (långt streck) | Användarens alternativa lista. De två skärmbilderna visar kortare streck, och API-kontrollfallet använder `-`. | Normalisera inte en ny typografisk variant utan att först kontrollera att den har samma betydelse i källan. |

Att ett tecken saknas i de kontrollerade källorna bevisar inte att det aldrig
används av Trafikanalys. Förklaringarna gäller dokumenterade produkter och
editioner; överför inte historiska SIKA-regler till ett aktuellt API utan stöd.

Vid avrundning av ett positivt värde till `0` eller `0,0`: använd halva den
sista visade decimalens steg, multiplicerat med redovisningsenheten, som övre
gräns. Exempel: `0` i tusental innebär 0 < antal < 500; `0,0` i tusental innebär
0 < antal < 50. Det exakta värdet är okänt. Sätt inte värdet till noll eller
till intervallets mittpunkt i beräkningar eller cirkeldiagram.

Skilj teckenförklaringens tryckta `0` från ett faktiskt numeriskt nollvärde i
ett rådatafält. Gör ingen generell omskrivning av alla nollor till små positiva
värden. För skalade/avrundade antal, andelar, index och andra mått: kontrollera
enhet och produktens specifika teckenförklaring före numerisk tolkning. En
uttrycklig avvikande produktförklaring har företräde.

Tillämpa teckentolkningen i beräknings-/presentationsledet. Låt råsvar,
API-klientens kontraktsvalidering och originalmarkeringar vara oförändrade.
Blanda inte samman sekretess, ej tillämpligt och noll.

## Underlag och räckvidd

Tecknens betydelser är avlästa från användarens skärmbild
`Screenshot_20261025_033926_Excel.jpg`, fliken Teckenförklaring_Legends i
`punktlighet-pa-jarnvag-2025`, tillhandahållen 2026-10-25. Skärmbilden visar
själva teckenförklaringen; den bevisar inte ensam varje API-produkts tillämpning.
Tom har samma datum uttryckligen sakgranskat att streck betyder noll för
uppräkningsbara antal och begärt att regeln införs i Trafikanalys-färdigheten.
Den tillämpas därför även på Gas i kontrollfallet T10036/nyreg/september 2026.
Detta är dokumenterat användarunderlag och sakgranskning, inte en ny kontroll
av samtliga statistikmyndigheters publiceringsregler.

## Kompletterande källkontroll 2026-10-25

* Användarens `Screenshot_20261025_035532_Excel.jpg`, Regional linjetrafik 2025,
  Teckenförklaring_Legends: bekräftar `.`, `..`, streck, avrundat `0`, `k`, `r`
  och jämförbarhetsbrott. Bilden innehåller inte `...` eller `*`.
* [Trafikanalys, Punktlighet på järnväg](https://prod.trafa.se/bantrafik/punktlighet-pa-jarnvag/?cw=1),
  avsnitt Teckenförklaring: även `U` för skyddad uppgift. Hämtat 2026-10-25.
* [Trafikarbete på svenska vägar 1990–2025](https://www.trafa.se/globalassets/statistik/trafikarbete/2026/trafikarbete-pa-svenska-vagar---1990-2025---2026-04-17.pdf),
  publicering 2026-04-17, PDF-sida 2: `p`, `r`, `k`. Kontrollerat 2026-10-25.
* [SIKA Statistik 2007:16, Sjöfartsföretag 2005](https://www.trafa.se/globalassets/sika/sika-statistik/ss_2007_16.pdf),
  tryckt sida 4 / PDF-sida 6: `*` och `0,0`. Historisk källa, kontrollerad 2026-10-25.

Kontrollen var riktad, inte en totalinventering av Trafikanalys publikationer.
Inga nya statistikvärden hämtades eller ändrades.

## Observerat i API via MCP 2026-10-25

Publikationslegend är inte bevis för API-representation. Fem lyckade datauttag
(38 rader, 50 mätceller) från T10036, T0604_stm_kv, T1203 och T08091 gav:

* T10036/nyreg/september 2026/Gas: Value="-", FormattedValue="-".
* T1203/pastig/2024/subventionerad/Gotland/järnväg: Value="," och
  FormattedValue=",". Versions innehåller datum 2025-06-26T13:38:09.72 och
  värdet "..". Det aktuella kommatecknets betydelse är inte fastställd. Det är
  varken ett tal, ett belagt nolltecken eller en verifierad sekretesskod.
  Den äldre versionens ".." får inte tyst ersätta aktuellt värde.
* T0604_stm_kv/stm5/2026/kvartal 3: numeriskt Value="87,2854122298808",
  FormattedValue="87,29", tomma NoteIds och Versions. Inget p/P/* i cellen.
  Att ingen preliminärmarkering finns i cellen bevisar inte slutlig status.
* Inga U, p/P, *, ... eller avrundningsmarkeringen 0/0,0 observerades som
  aktuella mätcellvärden i dessa fem uttag. Detta är ett stickprov, inte ett
  påstående att symbolerna aldrig förekommer.

MCP-svaren med källa, exakt query och hämtningstid sparas som
`evaluation/charts/symbols-api-*.json`. Inga noll- eller sekretessdefinitioner
härleds enbart från observerad förekomst.

[API-beskrivningen](https://www.trafa.se/globalassets/ovriga-dokument/api-beskrivning.pdf),
PDF-sida 2, dokumenterar Notes, NoteIds och Versions, men ger ingen uttömmande
symbolkatalog. Kontrollerad 2026-10-25. Den granskade MCP-serverversionen 0.3.1
behåller cellernas NoteIds och Versions, men utelämnar toppnivåfältet Notes i
get_statistics. Därför kan detta verktyg inte visa hela nottextkedjan. Frånvaro
av Notes i MCP-svaret är inte bevis för frånvaro i det ursprungliga API-svaret.
Denna lucka ska åtgärdas och provas separat före påstående om full notbevaring.

I serverversion 0.4.0 är notförmedlingen rättad: Notes lämnas vidare oförändrat
när fältet finns, liksom cellernas NoteIds och Versions. Ett särskilt
regressionstest kontrollerar kopplingen. Observationen ovan gäller 0.3.1.
