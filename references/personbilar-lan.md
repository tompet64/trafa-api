# Personbilar per län och drivmedel

Verifierat med produktstruktur, dokumentation och data 2026-10-07. Använd profilen för direkt produktval; validera sluturvalet enligt vald metadataväg i `metadata-routing.md` före nya datauttag. Kontrollera produktdokumentationen på nytt vid ändrat innehåll eller osäker jämförbarhet.

- Produkt: `t10026`, Personbilar. Årsbestånd vid årets slut; geografin avser ägarens registrerade hemvist, inte körplats.
- Mått: `itrfslut`, Antal i trafik. Antal fordon; API-fältet Unit var tomt.
- Dimensioner: `ar`, `reglan`, `drivmedel`. Förväxla inte `drivmedel` med andra produkters `drivm`.
- Verifierade år: 2010–2025, 16 explicita värden, samt dynamiska `senaste` och `forra`. Behandla inte 2025 som permanent senaste år.
- Drivmedel: `103` El, `105` Laddhybrid, `t1` Totalt. Elbilsandel = El / Totalt inom samma län och år.
- `reglan` innehöll 21 län, `aa` Okänt län och `t1` Totalt. Hämta aktuell domän vid behov av enskilda länskoder; summera aldrig rikstotal tillsammans med län.
- Dokumenterad kombination: `T10026|itrfslut|nyregunder|ar|drivmedel|reglan`. Delurval med endast `itrfslut` validerades och hämtades framgångsrikt.
- Struktur: https://api.trafa.se/api/structure?query=t10026
- Dokumentation: https://www.trafa.se/sidor/api-dokumentation/?code=T10026 (produktval med parametern `code`).
- Definitioner: https://www.trafa.se/globalassets/statistik/vagtrafik/fordon/2026/fordon-i-lan-och-kommuner-2025.pdf

För ändpunktsjämförelse 2020–2025, validera först:
`t10026|itrfslut|ar:2020,2025|reglan|drivmedel:103,t1`
Det kombinerade tvåårsuttaget har inte provhämtats. Separata årsuttag med dessa kolumner gav 46 observationer och 35 099–35 156 JSON-svarstecken per år. Två år uppskattas därför till cirka 70 000 tecken, vilket talar för ett gemensamt dataanrop under den lokala målgränsen 80 000. Verifiera faktiskt svar och storlek; detta är ingen garanti för andra format eller urval.

Om relevant metadata redan finns, räcker normalt en slutvalidering enligt vald metadataväg och ett dataanrop för denna jämförelse. Tillämpa målgränsen ovan endast när den valda anslutningen behöver den. Återanvänd redan hämtade data om de besvarar frågan och ingen uppdatering behövs.
