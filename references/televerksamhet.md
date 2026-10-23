# Televerksamhet – T0901

Läs vid frågor om elektronisk kommunikation, abonnemang, trafikvolymer, investeringar eller företagsstatistik. Profilen är delvis granskad 2026-10-11; inte alla historiska mått eller API-kombinationer är sakvaliderade.

## Population, källor och aktualitet

Den aktuella undersökningen omfattar företag och andra aktörer på den svenska marknaden för elektronisk kommunikation. Det är en totalundersökning med ram från PTS-anmälda aktörer. PTS producerar statistiken efter 2019, Trafikanalys är statistikansvarig och sekundärpublicerar huvuddelen. PTS Svensk telekommarknad erbjuder fler detaljer för samma population; uppgifterna ska inte adderas som två oberoende undersökningar.

Skilj antal PTS-organisationer (`antalforpts`), företag inom televerksamhet (`antalfortele`) och SNI 61-företag (`antalsni`). Äldre ekonomimått har inte automatiskt dagens population. Årsdomänen 1994–2025 innebär inte att varje mått finns varje år.

Årlig publicering i september, cirka åtta månaders framställningstid. 2025 års statistik publicerades 2026-09-01. PTS huvudpublicering anges ske maj/juni. PTS samlar från 2025 in Svensk telekommarknad en gång per år, tidigare även halvårsvis. T0901 har endast år som observerad tidsdimension.

## Definitioner och enheter

Abonnemang är inte unika personer eller hushåll. Beståndsuppgifter i PTS årsrapport avser årets slut; trafik och intäkter avser årsflöden. Kontrollera referenstiden per API-mått och årgång. `abonn` anger Företag/Privat, medan `abon`, `abon1`, `abon2` beskriver abonnemangstyper.

Aktuell personalredovisning avser heltidsanställda inom televerksamhet, över 35 timmar per vecka. Detta är inte automatiskt heltidsekvivalenter eller alla anställda. Äldre `tid` och `medelantal` kräver egen definitionskontroll.

Enligt sparade API-etiketter: `antalanstal` och `antalabon` är tusental; `antalmint` och `antalsamtal` miljoner; ekonomiska belopp miljoner kronor; `datatrafik` terabyte; `svarande` procent. Bekräfta enheter i uttaget. Skalan för `trafikminut` och definitionen av `medelantal` återstår. `trafikminuta` är minuter per abonnemang med ännu ej verifierad nämnare; summera inte kvoter.

`forstrorlek` innehåller flera överlappande klassindelningar, bl.a. 0–9/1–9, 0–19/10–19 och 50–/50–249/250–. Summera bara en verifierad disjunkt indelning, aldrig alla koder och totalen tillsammans. Företag kan vara aktiva i flera tjänsteområden; områdesantal ger inte unika företag.

PTS beskriver teknikbruk som abonnemang som använt viss teknik under de senaste tre månaderna. Anta inte disjunkta 3G/4G/5G-grupper eller att detta mäter geografisk nät­täckning. Bekräfta definition och motsvarighet för det valda API-urvalet.

## Tidsseriebrott och osäkerhet

- Import/export-frågan togs bort inför undersökningen 2019 och tabell 2.11 upphörde. Bevara historiska koder; deras existens är inte belägg för nya värden.
- Från statistikåret 2025 samlas inte utgående trafikminuter in efter vilka nät samtalen gått mellan, endast totalt. Äldre `tjanst2`-kategorier kan fortfarande finnas i metadata. Utebliven uppgift är inte noll.
- PTS reviderar historiska värden efter publicering. Använd senaste publicering även för äldre år och kontrollera fotnoter och PTS förändringslogg (från 2015 års insamling).
- Totalundersökning har bortfall, mätfel och viss registereftersläpning. 2025 svarade 640 av 674, cirka 95 procent; ingen generell KI-regel kan hämtas från Lastbilstrafik.
- Kvalitetsdeklarationens tabell 1 innehåller 787 för annan elektronisk kommunikation, större än totalt antal svarande. Enhet eller uppgift är oklar; citera inte detta som ett verifierat unikt företagsantal.

Statistiken ingår i SOS, men tabeller/figurer utan SOS-symbol gör det inte. Enskilda företags uppgifter skyddas mot röjande. Skilj noll, sekretess och andra saknade värden.

## Källor och kvarstående kontroller

Produktsida: https://www.trafa.se/elektronisk-kommunikation/televerksamhet/
Kvalitetsdeklaration 2025 (2026-09-01): https://www.trafa.se/globalassets/statistik/televerksamhet/2025/televerksamhet-2025---kvalitetsdeklaration.pdf
PTS statistik: https://statistik.pts.se/svensk-telekommarknad
PTS rapport 2025: https://statistik.pts.se/files/svensk-telekommarknad/rapport_svensk_telekommarknad_2025_t.pdf

Kontrollera historiska ekonomimåtts årstäckning och population, ospecificerade skalfaktorer, abonnemangens aktivitets-/referensdefinition och den faktiska API-redovisningen efter ändringen 2025. Vid geografisk bredbands- eller mobiltäckning: använd PTS separata kartläggning via dess webbplats, inte telekomabonnemang som ersättningsmått.

## Kommande överföring till PTS

Tom uppger 2026-10-11 att Post- och Telestatistiken kommer att överföras till PTS inom något år eller två. Detta är en expertuppgift om en framtida förändring; exakt datum, formellt ansvar och API-konsekvenser är okända. PTS producerar redan statistiken, vilket ska skiljas från den uppgivna kommande överföringen. Behåll nuvarande produktkoder och roller tills ändringen verifierats. Vid genomförande: kontrollera API, produktkoder, publiceringskanaler, länkar och historisk åtkomst. Ingen automatisk bevakning är installerad.
