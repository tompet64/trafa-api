# Bantrafikskador – T0602

Profilen är delvis granskad mot produktsida, kvalitetsdeklaration 2025 och API-metadata. Den godkänner inte konkreta API-kombinationer.

## scope

Allvarliga händelser i kommersiell bantrafik; museitrafik och viss industrispårstrafik undantas. Händelser med farligt gods behandlas separat.

## events_vs_people

Antal händelser och antal avlidna/allvarligt skadade är olika mått. Flera personer kan drabbas i samma händelse; avlidna avser alla relevanta personkategorier, inte bara passagerare.

## event_type

Olyckor och självmordshändelser redovisas separat. Självmordshändelser omfattar självmord och självmordsförsök; deras antal är inte antalet fullbordade självmord. Fråga eller ange uttryckligt urval vid tvetydiga frågor om dödsfall.

## severity

En allvarlig händelse kan kvalificera genom dödsfall inom 30 dagar, personskada med mer än 24 timmars sjukhusvård, materiell skada minst 150 000 euro eller totalt trafikstopp minst sex timmar. Reglerna för farligt gods är separata. Allvarlig händelse innebär därför inte nödvändigtvis personskada.

## reference_period

Kalenderår; årlig publicering i juni. Hämta historiska uppgifter ur senaste publicering, eftersom äldre publikationer normalt inte revideras.

## overlap_with_road

Plankorsningsolyckor och vissa vägtrafikolyckor vid spårvägsdrift kan ingå även i Vägtrafikskador. Summera inte produkterna till ett transportsystemtotal utan kontrollerad avgränsning och hantering av överlapp.

## time_comparability

Kriterier för allvarlig händelse ändrades 2007. Växlingsolyckor saknas före 2007; kategorier har tillkommit 2004, 2005, 2006 och 2014 beroende på trafikslag/personkategori; kön finns från 2009. Självmordsklassning ändrades 2016 på det statliga järnvägsnätet. Kontrollera avsnitt 5.1 vid tidsjämförelser; syntetisera inte äldre saknade kategorier som noll.

## geography

Produktsidan beskriver nationella summeringar och ingen företags-/sträckredovisning. API-metadata innehåller lan. Verifiera dess aktuella kombinationer och faktiska täckning; lova varken länsdata eller deras frånvaro utifrån sidan ensam.

## international_comparison

Nationell Bantrafikskador omfattar spårväg, tunnelbana och fristående järnvägsnät; ERA-statistik utesluter dessa. Välj jämförbar population vid internationell jämförelse.

## survey

Totalundersökning baserad på rapportering till Transportstyrelsen. Trafikanalys är statistikleverantör; totalundersökning innebär inte frånvaro av mät- eller klassificeringsosäkerhet.

## API-koder

Mått: `handelse`, `avlidna`, `allvars`. `handelsetyp:1` betyder Olyckor och `handelsetyp:2` Självmordshändelser. `drift:b02` Järnväg, `b03` Spårväg, `b04` Tunnelbana, `t1` Totalt. Koder kontrollerade i sparad struktur 2026-10-09; slutvalidera aktuellt urval. Hierarkin `olyckskat` → `kategori` → `katsepc` ska bevaras.

## Källor

- https://www.trafa.se/bantrafik/bantrafikskador/ (läst 2026-10-11).
- https://www.trafa.se/globalassets/statistik/bantrafik/bantrafiksskador/2025/kvalitetsdeklaration-bantrafikskador-2025.pdf (publicerad 2026-06-11, läst 2026-10-11), avsnitt 1.2, 2.1, 5.1–5.3. Referensåret är 2025 enligt omslag och avsnitt Referenstid; formuleringen Sverige 2024 i populationsavsnittet bedöms vara en kvarvarande årtalsuppgift och används inte som täckningsgräns.
