# Postverksamhet – T0701

Profilen är delvis granskad mot produktsida, kvalitetsdeklaration 2025 och sparad API-metadata 2026-10-11. Historiska definitioner och konkreta API-urval kräver ytterligare kontroll.

## Population och produktval

Tillståndspliktig postverksamhet, främst posttjänster och tidningsdistribution. Intressepopulationen är alla tillståndshavare; målpopulationen för undersökningen är tillståndshavare med egen utdelning. Paketdistributörer utan posttillstånd ingår inte. För 2025 anges 19 tillståndshavare, 17 med egen utdelning och 16 svarande. Dessa tal gäller enbart den årgången.

Produkten ger inte hela paketmarknaden, e-handelns volymer eller alla transportföretags leveranser. Traditionella brev är skriftliga meddelanden; varuförsändelser kallas också paketbrev. Vid frågor om hela paketmarknaden, använd PTS separata paketmarknadsstatistik och kontrollera dess population.

PTS utför insamling och kvalitetsgranskning och förvarar primärdata. Trafikanalys är statistikansvarig enligt kvalitetsdeklarationen för 2025. Produkten ingår i SOS. Det är inte en urvalsundersökning med Lastbilstrafiks KI-regel: mätfel är viktigaste uppgivna osäkerhetskällan, bortfall och täckningsfel kan också finnas, inga modellantaganden anges.

## API-koder, enheter och referenstider

Mätvärdet är `antal`; innehåll och skala styrs av dimension och tabell. Operatörer och servicepunkter är antal. Etiketterna för `brevtids:01`, `postfors:01–04` och `varufors:01–02` anger tusental försändelser. Kontrollera generiska totaler och svarsenheter; ge inte måttet `antal` en enda global skalfaktor.

`oprtids` och `oprverks` är dimensioner. Operatörernas bestånd avser 31 december enligt sparad API-beskrivning, försändelser kalenderårsflöden. Referensdag för servicepunkter är inte verifierad. `oprverks:06` avser tillståndshavare som inte ingår i undersökningen; skilj tillståndsbestånd, undersökningspopulation och svarande.

`postfors:01/02` är utdelade traditionella brev/varuförsändelser i Sverige, `03/04` skickade till utlandet. Utdelade i Sverige är inte automatiskt samma som från Sverige. `vag:01` anger från Sverige till Sverige; `02/03` från övriga EU/utanför EU till Sverige; `04/05` Sverige till övriga EU/utanför EU. `vag` är riktning, inte transportsätt. Validera faktisk kombination. Behåll ledande nollor.

Fullservicekontor erbjuder hämtning/sändning inklusive kontantköp och värdehantering, exempelvis rekommenderade försändelser. Egen regi och ombud är delkategorier. Brevlådor, kontor och lantbrevbärarlinjer är olika objekt: summera dem inte som unika fullservicekontor eller geografisk tillgänglighet. Inga län-/kommunsdimensioner observerades i produktstrukturen. Summera aldrig totaler tillsammans med delarna eller bestånd över år.

## Tidsserier och uppdatering

- Från undersökningen 2019 gjordes stora förändringar. Endast antal tillståndshavare och utdelade brev i Sverige bedöms jämförbara med tidigare publiceringar.
- Från undersökningen 2023 togs viktklassen 2 001–20 000 g bort (`varufors:02`). Kvarvarande kod betyder inte att nya år har värden. Källan hänvisar till PTS rapport Den svenska paketmarknaden.
- Från undersökningen 2025 togs frågan om lantbrevbärarlinjer bort (`servicepkt:05`); redovisningen anges till och med 2024. Saknad uppgift är inte noll.
- PTS och Trafikanalys samarbetar från 2003; tidigare separata bearbetningar kan ge skillnader. Addera inte överlappande publiceringar.
- År 1995 var en provundersökning och inte fullt jämförbart med senare år. Årsdomänen 1993–2025 garanterar inte varje måtts täckning eller jämförbarhet.
- Endast slutlig statistik redovisas, men korrigeringar kan införas påföljande år. Använd senaste utgåvan även för äldre år; skilj sekretess, saknad uppgift och noll.

Årlig undersökning, insamling i januari och normalt tre månaders framställningstid. 2025 års statistik publicerades 2026-03-27; kontrollera aktuell publiceringsplan. Alternativ post-/paketstatistik finns hos PTS, men dess definitioner och population ska kontrolleras innan användning.

## Källor och öppna frågor

Produktsida: https://www.trafa.se/brev-och-paketdistribution/postverksamhet/
Kvalitetsdeklaration 2025 (2026-03-27): https://www.trafa.se/globalassets/statistik/postverksamhet/2025/kvalitetsdeklaration-postverksamhet-2025.pdf

Återstår: servicepunkternas referensdag, totalernas enheter och avgränsning, servicekategoriernas jämförbarhet efter 2019 och faktisk API-täckning efter borttagna frågor. Produktsidans PTS-länk till /post/svensk-postmarknad/ gav 404 vid kontroll; hitta aktuell ingång via PTS webbplats före hänvisning.

## Kommande överföring till PTS

Tom uppger 2026-10-11 att Post- och Telestatistiken kommer att överföras till PTS inom något år eller två. Detta är en expertuppgift om en framtida förändring; exakt datum, formellt ansvar och API-konsekvenser är okända. PTS producerar redan statistiken, vilket ska skiljas från den uppgivna kommande överföringen. Behåll nuvarande produktkoder och roller tills ändringen verifierats. Vid genomförande: kontrollera API, produktkoder, publiceringskanaler, länkar och historisk åtkomst. Ingen automatisk bevakning är installerad.
