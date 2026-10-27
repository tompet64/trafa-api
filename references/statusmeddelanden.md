# Observerade fel i statusmeddelanden

## Syfte och begränsning

Använd samma krav på korrekta källor och benämningar i statusmeddelanden som i slutsvaret. Denna fil samlar konkreta observationer och stödjer felsökning. Den är inte en källa för statistikvärden eller ett belägg för att färdigheten styr alla etiketter i ChatGPT.

Skilj mellan:
- assistentens egenformulerade kommentarer,
- verktygsnamn, anropsargument och returnerade svar,
- etiketter som användaren ser i gränssnittet.

En etikett kan saknas i assistentens tillgängliga logg. Fastställ inte dess tekniska ursprung utan belägg. Instruktioner kan vägleda modellens formuleringar men garanterar inte kontroll över separat genererade gränssnittsetiketter. Historiska etiketter kan inte lovas bli rättade genom en dokumentationsändring.

## Arbetsgång vid ett rapporterat fel

1. Läs tillgänglig skärmbild och jämför med kommentar, anropsargument och svar från det berörda anropet. Be bara om ytterligare underlag när det behövs för slutsatsen.
2. Anteckna observationsdatum, exakt synlig feltext, berört anrop, korrekt benämning och belägg. Skilj händelsedatum från rapporteringsdatum. Gissa inte saknad ordalydelse.
3. Markera varje fall som bildverifierat, loggverifierat eller användarrapporterat. En bild verifierar vad som visades, inte hur etiketten skapades.
4. Rätta fel i egenformulerad text uttryckligen. Använd verifierade namn och neutrala handlingsbeskrivningar, utan att tolka förkortningar eller filnamn genom ordlikhet.
5. Om feltexten bara finns i gränssnittet, redovisa begränsningen. En skärmbild tillsammans med relevant anropslogg kan utgöra underlag för en felrapport till OpenAI. Skicka ingen rapport utan användarens instruktion.
6. Vid återkommande fel, komplettera den generella regeln i SKILL.md och denna fallista. Lägg bara produktspecifika kodbetydelser i respektive produktguide när de är metadataförankrade.

Publicera inte privata skärmbilder, kontouppgifter eller fullständiga chattloggar i ett offentligt repository. Dokumentera nödvändiga sakuppgifter och korta relevanta textutdrag.

## SJ vid läsning av metodguide för sjötrafik

- Observationsdatum: 2026-10-27.
- Status: bildverifierat; berört anrop och svar kontrollerade i den aktuella chatten.
- Exakt synlig feltext: ”Analyserar SJ:s trafikdata API”.
- Placering: etikett vid GitHub-anropet under ”Used GitHub och Trafikanalys API”.
- Berörd handling: GitHub-verktyget `fetch_file` läste `references/sjotrafik.md` i `tompet64/trafa-api`.
- Korrekt benämning: ”Läser metodguiden för sjötrafik i Trafikanalys API-repositoriet”.
- Belägg: användarens skärmbild och anropets argument/svar. Filen handlar om sjötrafik och bland annat spannmål i utrikes godshantering. SJ förekommer inte i det berörda anropets argument eller svar. Feltexten finns inte i assistentens egenformulerade kommentar.
- Bedömning: etiketten saknar sakligt stöd. Att filnamnet skulle ha misstolkats är en möjlig förklaring, inte en fastställd orsak. Loggen fastställer inte vilken komponent som skapade etiketten.

## Taxering vid fordonsstatistik

- Rapporteringsdatum: 2026-10-27. Händelsedatum är inte fastställt.
- Status: användarrapporterat.
- Rapporterat felord: ”taxering”. Fullständig feltext saknas.
- Sammanhang: arbete med fordonsstatistik enligt användaren.
- Berört anrop: inte identifierat i tillgängligt underlag.
- Korrekt neutral formulering: exempelvis ”Kontrollerar fordonsstatistikens metadata”, om det motsvarar den faktiska handlingen.
- Belägg: användarens uppgift; ingen skärmbild eller identifierad anropslogg har granskats för detta fall.
- Bedömning: varken exakt formulering eller teknisk orsak kan fastställas. Registrera inte ”taxering” som synonym till fordonsstatistik och konstruera ingen koppling till en viss produkt eller variabel.
