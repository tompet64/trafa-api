# Sjötrafik – prioriterad regression 2026-11-17

Källförslag 1.1.14, utifrån main `8b8c661a6ac7124b90e6cfd4a6c438f4460656f2`.
Kört lokalt på Windows med Python 3.12, UTF-8 och Node 24.
Frysta API-svar från 2026-11-16 används; ingen ny statistik har hämtats.

| Test | Kontroll och observerat resultat | Kodtest |
|---|---|---|
| 1 | T08021:s referensdomän börjar 2020. Begärda år 2016–2019 utesluts synligt; okända år godkänns inte. | Godkänt |
| 5 | Det frysta detaljsvaret innehåller 9 av 16 förväntade delkombinationer. Sju saknas; inga nollor skapas. | Godkänt |
| 6 | Utrikes K3 2025: 18 704 + 19 530 − 34 634 = 3 600 tusen ton. Överskrider den prövade avrundningsgränsen 1,5 tusen ton. | Godkänt |
| 9 | Samma mått och enhet med olika population klassas som olika omfattning. Okänd omfattning klassas som ej bedömbar. | Godkänt |
| 10 | Samtliga sex år 2020–2025 prövas. Enbart lossat IVV-gods förklarar inte differensen. Okänd lastning härleds inte från differensen. | Godkänt |

Hela offline-sviten: 116 tester godkända. Prioriterad körning: 5 av 5
godkända, med JSON-, JUnit- och Markdown-rapport. Rapporteringens hantering av
ett avsiktligt misslyckat deltest verifieras också i offline-sviten.

Detta verifierar beräkningshjälp och kodinvarianter, inte en språkmodells
slutsatser eller aktuella API-värden. De separata beteendefallen i
`evaluation/SHIPPING_CASES.md` är inte genomförda. Ingen installation,
driftsättning, kontakt med statistikansvariga eller ändring av publicerade
statistikvärden ingår.
