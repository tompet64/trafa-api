# Bantrafik och Järnvägstransporter

Källor: https://www.trafa.se/bantrafik/bantrafik/ och https://www.trafa.se/bantrafik/jarnvagstransporter/ , lästa 2026-10-11. Exakta koder och metodnoter nedan kommer från sparad API-metadata 2026-10-09. Profilerna är delvis granskade.

## Produktval

| Kod | Roll |
|---|---|
| T06011 Infrastruktur | Bantrafikens årliga infrastruktur, investeringar, underhåll, korsningar och infrastrukturpersonal |
| T06012 Fordon | Bantrafikens årliga fordon och kapacitet |
| T06013 Trafik och transport | Bantrafikens årliga trafik- och transportarbete, resor, gods och trafikpersonal |
| T0603 Järnvägtransporter | Preliminära kvartalsuppgifter och rullande fyrakvartalsmått för järnväg |

Bantrafik omfattar kommersiell järnväg, spårväg och tunnelbana i Sverige; Järnvägstransporter gäller järnväg. Museitrafik och trafik inne på industriområden är exempel på undantag. Välj trafikslag och mått, och likställ inte all bantrafik med järnväg eller regional kollektivtrafik i RKM:s regi. Sekretess innebär i princip nationella summeringar utan företags-/sträckdetaljer; T06011 har dock län i metadata, så fastställ geografisk nivå i aktuell struktur.

Årsstatistiken publiceras i juni. Kvartalsstatistiken publiceras fyra gånger per år, cirka 2,5 månader efter kvartalets slut, och är preliminär. Godstransporter redovisas med och utan malmtransporter på Malmbanan; dessa alternativ får inte summeras till en total. Använd senaste utgåva även för äldre perioder, och kontrollera revisioner vid jämförelse mellan år och kvartal. Senaste Excel-tabeller kan ha expanderbar historik, för Bantrafik som längst från 2000 och Järnvägstransporter från 2003; antag inte att API har samma täckning.

## Mått och jämförbarhet

- T0603 använder pesonkm och rullpesonkm; T06013 använder personkm. Behåll de exakta Name-koderna, även när stavningen ser fel ut.
- Rullresor, rullpesonkm, rullton och rulltonkm avser summan av fyra senaste kvartal. Använd ett matchande publicerat rullande värde för en sådan fråga; summera inte flera överlappande rullande värden. Skilj från kalenderår.
- Resor är inte unika resenärer. Skilj personkilometer, tonkilometer, tågkilometer, godsmängd och platskilometer. Skala varierar mellan tusental och miljoner; behandla inte bruttotonkilometer som gods-tonkilometer.
- Infrastrukturproduktens km anges som trafikerade spår: likställ inte med banlängd utan verifierad definition. Fordonskapacitet är inte faktiskt resande.
- API-metodnoter anger förändrade skattningsmetoder för resor/persontransportarbete mellan 2016–2017 och 2019–2020, den senare med cirka 3 procents effekt på antal resor. Gör inte trendtolkningar utan att beakta noterna, och omräkna inte själv historiken utan underlag.
- Godsmängd och godstransportarbete från 2018 anges som ej jämförbara med tidigare år på grund av ändrad insamling/bearbetning. T06013 anger undantag för farligt gods enligt RID; överför inte undantaget till varje annan produkt.
- T06011:s korsningsmått har omklassificeringar 2015 och 2017–2019 som påverkar jämförbarhet. Bevara metodnoten vid relevant tidsjämförelse.
- Energia-noter i T06011/T06013 anger att bantrafikens energianvändning publiceras av Energimyndigheten från 2016. Hänvisa dit eller till produktsidans dokumentation vid nyare energiuppgifter; metadataförekomst garanterar inte aktuell statistik. Enheten i T06013 varierar med energislag: GWh för el och m3 för diesel.
- Detaljer om framställning hänvisas till respektive produktsida och aktuell kvalitetsdeklaration. Slutvalidera alla API-kombinationer.

## Spårväg och tunnelbana: primär källa

Trafikanalys statistikansvarige har enligt Toms återgivning 2026-10-23 bekräftat att totalundersökningen Bantrafik och Järnvägstransporter är den huvudsakliga källan för resande med spårväg och tunnelbana; dessa uppgifter används även i Regional linjetrafik (T1203). För frågor specifikt om regional linjetrafik är T1203 fortfarande den relevanta publiceringsprodukten, men dess spårvägs-/tunnelbaneuppgifter är inte en oberoende datakälla från totalundersökningen. Kontrollera aktuella mått, perioder och tillåtna urval. Överlapp innebär inte automatiskt samma enhet, avrundning eller definition; summera inte uppgifter mellan produkterna.

## Komplettering efter test 8, 2026-10-14

T1203 gav numeriska påstigningar för både spårväg och tunnelbana samtliga år 2022–2025 med finans:2 explicit. Query: `t1203|pastig|ar:2022,2023,2024,2025|finans:2|traslag:3,4`. Ett tomt uttag utan finans får inte beskrivas som att produkten saknar dessa år. Vid frågor om just Regional linjetrafik, hämta T1203 och begär båda trafikslagen samtidigt.

Tom bekräftar att motsvarande Bantrafik-tal finns 2022–2025 och betecknar samma påstigningar, avrundade till miljontal i stället för tusental i T1203. Bantrafik 2025:s statistikblad bekräftar 2025 års spårvägs-/tunnelbanevärden. Alla prövade API-varianter av T06013 i denna felsökning gav DataCount 0; en fungerande T06013-query har därför inte verifierats här. Kalla inte detta att Bantrafik saknar uppgifter. Källa: https://www.trafa.se/globalassets/statistik/bantrafik/bantrafik/2025/bantrafik-2025.pdf .

Korrigering av tidigare osäkerhet om källkedjan: enligt Toms återgivning av besked från statistikansvarige (2026-10-23) är totalundersökningen Bantrafik och Järnvägstransporter huvudsaklig källa för spårväg och tunnelbana, och uppgifterna används också i Regional linjetrafik. Detta stämmer med riktningen i kvalitetsdeklarationen för T1203 (Bantrafik/Järnvägstransporter → T1203). Den tidigare formuleringen om motsatt riktning ska inte återanvändas. Ekonomins insamling är en separat fråga.
