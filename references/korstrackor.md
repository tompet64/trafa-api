# Körsträckor – population och metodversion

Andra genomgången, 2026-10-11. Publicerings- och metodkällor har granskats; API-snapshot är fortsatt från 2026-10-09. Alla gamla expertuppgifter är bevarade i profilerna. Läs aktuell produktprofil med metadata_lookup.py och validera sluturvalet.

## Dokumenterade definitioner

- Personbilar, lastbilar, bussar och motorcyklar som varit i trafik någon gång under året. Mopeder, traktorer, släp och terrängskotrar saknar underlag av mätarställningar och ingår inte. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/korstrackor/2025/kvalitetsdeklaration-korstrackor-2025.pdf, 1.2.1.)
- Total körsträcka divideras med antal fordon i trafik minst en dag under året. Utländsk körning ingår; registreringsregion är inte körplats. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/korstrackor/2025/kvalitetsdeklaration-korstrackor-2025.pdf, 1.2.2.)
- Fordon utan giltiga mätarställningspar får modellskattade körsträckor. Totalregister innebär inte att alla körsträckor är observerade. Ingen kvantifierad osäkerhet eller KI publiceras. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/korstrackor/2024/kvalitetsdeklaration-korstrackor-2024.pdf, 2.1; 2.2.1.)
- Årlig publicering i april för personbilar, lastbilar och bussar; motorcyklar uppdateras på hösten. Kontrollera referensår per trafikslag. (Källa: https://www.trafa.se/vagtrafik/korstrackor/, Publicerade rapporter.)
- Körsträckor 2025 redovisar vissa 2023–2025-uppgifter med båda metoderna; endast ny metod planeras från Körsträckor 2026. Det fastställer inte metodversionen i API-et. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/korstrackor/2025/kvalitetsdeklaration-korstrackor-2025.pdf, 5.1.)
- Modellbyte 2012 omfattade historiska årgångar. Besiktningsändringen 2018 ändrade referensfönstret för personbilar/lätta lastbilar, inte buss/MC; äldre och reviderade utgåvor får inte blandas. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/korstrackor/2025/kvalitetsdeklaration-korstrackor-2025.pdf, 5.1; F Historik.)
- Ny metod korrigerar felaktigt inkluderade avställda fordon och byter imputation från geometriskt till aritmetiskt medel med fler förklaringsvariabler. Dokumentera detta som metodbakgrund tills API-införandet verifierats. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/korstrackor/2025/metodrapport-korstrackor.pdf, 3; 5.)
- Den nya metodens fordonsvisa dagliga mil beräknas över trafikdagar mellan besiktningar och multipliceras med trafikdagar under referensåret för årskörsträcka. Detta definierar inte API-måttets aggregering gdkor. (Källa: https://www.trafa.se/globalassets/statistik/vagtrafik/korstrackor/2025/metodrapport-korstrackor.pdf, 2.)

## Produkter och kvarstående kontroller

| Kod | Produktroll | Särskild kontroll |
|---|---|---|
| T10091 | Bussar – årlig körsträckestatistik | Metodversion i API och gdkor |
| T10092 | Lastbilar – årlig körsträckestatistik | Metodversion i API och gdkor |
| T10093 | Motorcyklar – årlig körsträckestatistik | Metodversion i API och gdkor |
| T10094 | Personbilar – körsträckor och antal fordon i trafik någon gång under året | Metodversion i API och gdkor |

## Regler för återanvändning

- korstr och mkorstr anges i mil i sparad API-metadata; 1 mil = 10 km. Kontrollera skalning separat i publikationen, där summor kan anges i miljoner mil.
- anttrf avser fordon i trafik någon gång under året, även fordon som senare avregistrerats. Använd inte års-slutsbestånd som nämnare.
- Gruppmedel får inte summeras eller vägas lika utan fordonsantal. En beräkning från totaler kräver samma population, period och skala.
- Körsträckor är inte tonkilometer/personkilometer och inte direkt trafikarbete på svensk mark. Regional registreringsadress ger ingen territoriell fördelning av körningen.
- Bevara Toms API-observation 2026-10-10: ny metod ännu inte införd enligt hans granskning; aktuell API-version är inte oberoende verifierad. Tillämpa inte nya metodens regler som säker förklaring av API-resultat.
- gdkor, där måttet finns, får inte härledas som mkorstr/365 eller oviktat medel utan belagd aggregeringsformel och rätt enhet.
- Lätt/tung bygger på totalvikt, inte Lastbilstrafiks maxlastvikt. Körsträckor omfattar både lätt och tung lastbil enligt valt urval.
- T10093 saknar gdkor i sparad struktur. Årsresultat för MC publiceras senare; anta inte samma senaste referensår som personbil/buss/lastbil.
- agarkat är ägarkategori och ftgtyp företagstyp; enskild näringsidkare hör till ftgtyp. Fordon-publikationens särskilda statistiska ägarklassificering får inte överföras till Körsträckor utan produktkontroll.
