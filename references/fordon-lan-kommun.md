# Fordon i län och kommuner, T10020

## Produktroll och källstatus

Använd exakt produkt-Name `t10020`. Officiell etikett: Fordon i län och kommuner.

Produktkoden är ny men samlar befintlig fordonsstatistik som tidigare presenterats per fordonstyp i ett tiotal andra produkter. Syftet är att passa Trafikanalys presentationsform interaktiva diagram och rapporter. Beskriv inte detta som att statistikens innehåll eller undersökningen är ny. Ingen fullständig lista över de tidigare produkterna eller deras inbördes likvärdighet har verifierats.

Produktrollen, adressanknytningen och perioddefinitionerna kommer från Toms uttryckliga sakgranskning 2026-10-09, inte från en slutsats dragen ur API-koden. Spara den källskillnaden vid återanvändning. Årsdomänen 2022–2025, koderna och kombinationsraderna kommer från API-struktur respektive dokumentation kontrollerad samma dag.

## Geografi

`lan` = län, `kommun` = kommun. Geografin avser ägarens eller företagets registrerade adress, beroende på ägarkategori. Likställ inte med fordonets användningsplats.

Behåll okända geografiska kategorier. Skyddad identitet är en belagd orsak till okänd geografi, men likställ inte varje okänd post med skyddad identitet. API-koder inkluderar `aa` för okänt län och `aaaa` för okänd kommun, samt kategorier för okänd kommun inom ett känt län. Bevara inledande nollor och exakt skiftläge från API:t.

## Perioder

- `itrfslut`: fordon i trafik den 31 december det angivna året.
- `avstslut`: avställda fordon den 31 december det angivna året.
- `nyregunder`: nyregistreringar under kalenderåret.
- `biltathet`: personbilar i trafik per 1 000 invånare. SCB-befolkningen avser den 1 november samma statistikår, enligt Toms citat ur Excel-bladet Definitioner 2026-10-09. Fordonsbeståndet avser den 31 december. Citatets exakta Excel-årgång är inte angiven och har inte kontrollerats separat. Täljaren inkluderar bilar ägda av juridiska personer, bekräftat av Tom med citat 2026-10-09. Värdet är redan en kvot per tusen: multiplicera inte det publicerade värdet med 1 000 och summera inte kvoter mellan regioner.

Publicering sker årligen i februari enligt Toms sakgranskning. Kvalitetsdeklarationen för 2025, avsnitt 3.1–3.2, anger mitten av februari för Fordon i län och kommuner och slutet av februari för den separata publikationen Fordon. Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/kvalitetsdeklaration-fordon-i-lan-och-kommuner-2025.pdf (kontrollerad 2026-10-09). Skilj publikationerna och deras tidpunkter. Summera inte bestånd över år. Använd variabler från T10020; anta inte att andra fordonsprodukters namn eller kombinationer kan överföras oförändrade.

## Dokumentation och kvarstående frågor

Dokumentationen https://www.trafa.se/sidor/api-dokumentation/?code=T10020 hämtades 2026-10-09. 24 kombinationsrader har sparats i `references/metadata/kombinationer.json`. Läs relevanta rader och validera exakt sluturval enligt metadatavägen i `metadata-routing.md`. Fullproduktens JSON-struktur uppmättes till 123 458 tecken samma dag; använd denna källbelagda storleksindikation för begränsade anslutningar och skilj den från det filtrerade urvalets okända storlek.

Återstående sakfrågor: populationsavgränsningar och undantag per fordonsslag, belagda skillnader och överlapp mot äldre fordonsprodukter. Produkten är delvis sakgranskad, inte generellt godkänd i alla avseenden.

## Fördjupad källgranskning 2026-10-11

Andra genomgången har kompletterat produktprofilerna med aktuella kvalitetsdeklarationer. Äldre expertuppgifter ovan är bevarade som ursprunglig proveniens. Gemensamma definitioner och nya avgränsningar finns i `fordon-bakgrund.md`, körsträckornas versionsskillnader i `korstrackor.md` och aktuella sakfrågor i respektive produktprofil. Tidigare allmänna öppna frågor om population och period är preciserade där; detta är inte en fullständig API-validering.
