# Välj struktur eller referensmetadata

## Beslutsregel före HTTP

Sök produkt, variabler, värden och dokumenterade kombinationer i referensfilerna först. Skilj sökning från validering. Välj därefter en metadataväg för exakt query och språk enligt tabellen.

| Situation | Åtgärd |
|---|---|
| Direkt Python utan angiven strukturbudget | Validera mot aktuell struktur. Ingen generell Action-gräns införs. |
| Begränsad anslutning, exakt strukturquery tidigare uppmätt över budget | Använd daterad referensvalidering i `auto`; gör inte om samma strukturanrop. |
| Begränsad anslutning, bara full produktstruktur känd över budget | Välj referenser försiktigt i `auto`. Märk detta som en produktindikation, inte en mätning av det filtrerade urvalet. |
| Okänd storlek och angiven budget | Prova vald struktur inom budget. Vid belagd storleksöverskridning, avbryt och validera med referenser i `auto`. |
| Uttryckligen vald referensväg | Validera hela urvalet med daterade referenser före data. |
| Saknat referensstöd eller observerad motsägelse | Stoppa. Uppdatera underlaget eller undersök en annan dokumenterad urvalsväg. |
| Behörighets-, nätverks-, HTTP-, API-, format- eller schemafel | Stoppa det misslyckade steget och redovisa dess verkliga feltyp. Använd inte felet som skäl att godkänna referensvägen. |

Håll metadataväg och transport separata. En Pythonklient kan använda referenser, och en Action kan använda aktuell struktur när den ryms. Metodens kontroller gäller även i andra klienter. OpenAPI-kontraktet eller referensfilerna installerar inte någon anslutning.

## Krav för daterad referensvalidering

Använd `scripts/reference_metadata.py` via `metadata_lookup.py` eller `trafa_client.py`. Utan körmiljö, genomför och dokumentera samma kontroller med de tillgängliga referenserna; hoppa inte över en kontroll för att dataoperationen går att anropa.

1. Matcha exakt API-produktkod mot den sparade strukturkatalogen. Kräv användbar, fullständig och daterad API-metadata. Stoppa vid konflikt med en uttrycklig produktidentitet i manuella tillägg.
2. Matcha varje variabels exakta `api_name`, typ D/H/M och verifierade källa. Följ föräldrar till rätt produkt. Bevara skiftläge och inledande nollor; använd inte etiketter som anropskoder.
3. Kontrollera varje filtervärde mot rätt fullständiga värdemängd och dess uttryckliga produkt-/variabelbindning. Expandera endast belagda årintervall; bevara luckor. Avvisa okända koder, tomma eller dubblerade val samt dynamiska filter som `senaste` och `forra` utan aktuell kontroll.
4. Kräv att alla begärda mått uttryckligen ingår i en och samma dokumenterade kombinationsrad och att urvalets D/H motsvarar just den radens dimensioner. En rad utan mått godkänner inget mått. Flera listade mått innebär inte att alla måste hämtas. Bygg aldrig en ny kombination genom korsning av marginaltabeller.
5. Spara kvitto med exakt query och språk, `validation_source=references`, metadatarevisionens datum, tidpunkt för den lokala kontrollen, den använda kombinationsraden och källans ursprungliga status. Spara filhashar för inlästa referenser; Pythonklienten lägger också till kontraktsversion och kontraktshash.

Behåll `DataCount=null` och en uttrycklig varning: referensvalidering bekräftar inte aktuell `Selected`, `Option`, `DataCount` eller observationstäckning. Den lokala kontrollens datum är inte ett nytt API-verifieringsdatum. Bedöm revisionens relevans för frågan och stoppa vid känd ändring eller saknat nödvändigt stöd. Gissa inte nya år eller koder för att underlaget är äldre än frågan.

Kontrollera det efterföljande datasvaret mot kontrakt, `Errors`, rader, perioder, enheter, noteringar och revisioner. Ett giltigt referensurval garanterar inte numeriska värden. Låt aktuell motsägande struktur väga tyngre än referenserna.

## Klientens kommandon

Kör från färdighetens rot. Följande planering är helt lokal:

```bash
python3 scripts/trafa_client.py plan --query 't10020|itrfslut|ar:2023|fslag' --structure-max-chars 80000
python3 scripts/metadata_lookup.py --query 't10036|nyreg|ar:2026|drivm:103|manad:09' --validate-reference
```

Det första exemplet använder fullproduktens storlek som försiktighetsindikator. Det andra visar referenskontroll av ett exakt urval, inte hämtad statistik eller en färdig andel.

Hämta med vald väg när nätverksanropet är tillåtet:

```bash
python3 scripts/trafa_client.py extract --query 'EXAKT_QUERY' --raw /tmp/uttag.json --rows 10
python3 scripts/trafa_client.py extract --query 'EXAKT_QUERY' --metadata-source references --raw /tmp/uttag.json --rows 10
python3 scripts/trafa_client.py extract --query 'EXAKT_QUERY' --structure-max-chars 80000 --raw /tmp/uttag.json --rows 10
```

Utelämna budgetflaggan för vanlig direkt Python när ingen sådan gräns behövs. `--structure-max-chars` begränsar bara struktursvaret; den gör inte Pythonklienten till en Action och begränsar inte datanedladdningen. Bedöm och dela datasvar enligt partition.md när den faktiska transporten kräver det.

Använd `--metadata-source structure` för att kräva strukturkontroll och avstå från automatisk referensfallback. En exakt tidigare uppmätt query över budget stoppas före HTTP. Om endast fullproduktens storlek är känd kan ett uttryckligt strukturläge göra ett begränsat försök med det filtrerade urvalet; dess exakta storlek är fortfarande okänd.

Ange `--metadata-root` för en annan validerad referensrevision och `--structure-inventory` för en annan storleksinventering. Ett observerat storleksstopp skapar exempelvis `/tmp/uttag.structure.json.size.json`; ange den filen som `--structure-inventory` vid ett senare försök med samma urval. Inläsningen avbryts över teckenbudgeten, en nedre gräns loggas och ett partiellt svar används aldrig som giltig struktur.

## Storleksinventering och komplettering

Läs `references/metadata/structure_sizes.json`. Inventeringen omfattar **56 giltiga produktstrukturer**, JSON på svenska, från 2026-10-09. Ursprungliga mätposter finns byteidentiskt i `structure_measurements_20261009.json`; filhash och exakt JSON-pekare kontrolleras. Varje storlek och produktidentitet kontrollerades åter mot arkiverade svarsfiler 2026-10-18, utan nya API-anrop. Mätposterna, svarsfils- och logghashar samt ursprungsarkivet är spårbara från inventeringen. Håll granskningsdatum skilt från mätdatum.

Skilj underlagens proveniens: 55 giltiga produkter har sparade HTTP-svarskroppar efter HTTP-avkodning. T10020 kompletterades från en sparad JSON-fil vars storlek och produktidentitet är verifierade, men vars byteidentitet med den ursprungliga HTTP-kroppen inte kan styrkas. Posten är märkt `measurement_basis=saved_json_document`; dess Content-Type rekonstruerades i arkivet. Använd detta som daterat storleksunderlag med den angivna begränsningen.

Använd de uppmätta talen i stället för den tidigare ungefärliga uppgiften om cirka 18 stora produkter: **14 över 100 000 tecken och 16 över 80 000**. Tabellen gäller fullproduktstrukturer, inte de filtrerade strukturernas eller datasvarens storlek.

| Produkt | Fullständig JSON-struktur, tecken |
|---|---:|
| T1004 Vägtrafikskador | 208 414 |
| T0802 Sjötrafik | 137 931 |
| T0501 Luftfart | 135 042 |
| T10030 Nyregistreringar | 131 541 |
| T10039 Övriga fordonsslag | 124 846 |
| T10020 Fordon i län och kommuner | 123 458 |
| T10026 Personbilar | 119 856 |
| T10023 Lastbilar | 117 303 |
| T10036 Personbilar | 116 448 |
| T10029 Övriga fordonsslag | 115 694 |
| T10021 Bussar | 114 648 |
| T1201 Färdtjänst och riksfärdtjänst | 112 159 |
| T10061 Lastbilstrafik år | 111 919 |
| T1102 Varuflöden | 105 861 |
| T0808 Fartyg | 82 234 |
| T0301 Utländska lastbilstransporter i Sverige | 80 290 |

T0401 gav ett JSON-svar på 70 tecken utan giltig vald produkt. Behåll detta som ett uteslutet historiskt försök, aldrig som en liten produktstruktur. Produktlistan och testprodukten atft ingår inte i produktantalet. Septemberpaketets tomma `structure_matningar.json` och dess komprimerade katalogstorlekar ger ingen strukturstorlek; använd oktoberpaketets verkliga mätningar. Inga XML-storlekar har belagts i den här inventeringen.

För ett filtrerat T10036-urval, exempelvis `t10036|nyreg|ar:2026|drivm:103|manad:09`, väljer `auto` med 80 000 teckens budget nu referenser med orsaken `full_product_size_precaution`. Det är en försiktighetsåtgärd grundad på fullproduktmätningen. Det filtrerade struktursvaret är fortfarande inte storleksmätt.

Spara varje ny faktisk mätning med endpoint, exakt query, språk, begärt och observerat format, UTC-tid, antal tecken och bytes samt råfil eller annan spårbar källa. Skilj fullständig mätning från en nedre gräns efter avbruten läsning. En exakt querymätning prioriteras framför en fullproduktindikation; kontrollera åldern före återanvändning. Blanda inte XML, JSON, språk eller tecken- och bytemått. En filstorlek eller minifierad återserialisering är inte automatiskt den ursprungliga svarslängden.

Komplettera inventeringen när strukturer ändå behöver uppdateras genom en tillåten transport. Starta inte en bred hämtning av alla produkter för en liten statistikfråga. Återanvänd redan uppmätta svar och uppdatera berörda referenser i samma metadataarbete.
