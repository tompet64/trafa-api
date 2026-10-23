# Luftfart – T0501

Delvis granskad 2026-10-11 mot officiella källor och metadata från 2026-10-09; konkret urval kräver slutvalidering.

## population

Civil luftfart i Sverige: trafik och transporter, flygplatsinfrastruktur, registrerade luftfartyg och olyckor. Flera olika populationer beroende på mått; flygplatsanknuten trafik är inte begränsad till svenskregistrerade flygplan eller svenska flygbolag. Godkända/icke-godkända flygplatser och trafikflygplatser är inte disjunkta bestånd.

## period

Trafik, transporter och registreringsflöden avser kalenderåret. Flygplats-/luftfartygsbestånd och vissa gällande bevis/certifikat avser 31 december enligt metadata och tabellrubrik. Skilj bestånd från registreringar/utfärdanden under året.

## passengers

Passagerare i flygplatsstatistiken är inte unika resenärer. Betalande passagerare, barn under två år utan egen stol, besättningsöverföringar och transferpassagerare ingår enligt deklarationen. Skilj ankommande/avresande och inrikes/utrikes; summera inte flygplatshanteringar till unika resor utan kontroll av dubbelräkning och totalens definition.

## direction

flygtrafik:1 är Utrikes, 2 Inrikes. typres:1 Ankommande, 2 Avresande; typlast:1 Ankommande, 2 Avgående. t1 är total i respektive dimension. Metadata anger att avresande passagerare/avgående godston rapporteras noggrannare, vilket kan ge skillnader mellan riktningarna. Tvinga inte riktningarna till likhet.

## land_secrecy

Land betyder inte passagerarens nationalitet eller nödvändigtvis slutlig destination efter byten. Deklarationen anknyter landredovisningen till första landningsflygplats efter start från Sverige; kontrollera riktningens tabelldefinition särskilt för ankommande. Från 2019 döljs relationer med färre än tre flygbolag; under 500 passagerare per år grupperas också bland övriga/ej redovisade länder. Saknat landvärde betyder inte noll trafik.

## transport_work

pkm, fkm och tonkm är modellberäknat person-/trafik-/godstransportarbete. Inrikes avstånd bygger på storcirklar, inte faktiskt flugen rutt. För utrikes beräknas transportarbete inom svenskt luftrum; använd inte som hela internationella resans transportarbete. Saknade avstånd kan skattas.

## capacity_units

antalufp är utbjudna flygstolar, inte passagerare. kabinfaktor är procent och ska inte summeras eller medelvärdesbildas ovägt. pkm/fkm/tonkm anges i tusental enligt etikett. antalanav anges i ton och avser endast fluget gods/post. Separata internationella ton-måttet har etiketten Gods, ton i miljoner; kontrollera population och skala per mått.

## movements

Landningar, starter och flygplansrörelser är olika mått. Rörelser i svenskkontrollerat luftrum kan omfatta överflygningar och är inte en summa av svenska flygplatslandningar. Välj typfpr/flygverk/flygtrafik efter aktuell tillåten kombination, inte efter antagandet att alla dimensioner kan kombineras.

## accidents

Olyckstabeller kan avse svenskregistrerade motordrivna luftfartyg eller olyckor i Sverige oavsett luftfartygets nationalitet. Skilj olyckor med dödlig utgång från antal omkomna/skadade och från materielskador. Kontrollera typskada och luftfartygspopulation innan summering eller internationell jämförelse.

## comparability

Fraktton saknas för 2019 och serien före/efter är inte jämförbar enligt kvalitetsdeklarationen. Linje/charter kan inte fullt särskiljas från 1994. Vissa certifikatmått upphörde från rapporten 2016. Metadataförekomst garanterar inte aktualitet eller obruten serie.

## official_status

Luftfart är officiell statistik, men världsluftfart/internationell statistik i tabell 6 och delar av tabell 5 är inte SOS. Överför inte nationella populationer eller SOS-status till dessa API-mått. ICAO- och Eurostatstatistik kan ha olika linje/charter-täckning.

## publication_sources

Årlig publicering, utgåva 2025 publicerades 2026-04-13. Trafikanalys är statistikansvarig/API-källa och Transportstyrelsen producent med administrativa register och flygplatsrapportering. Tätare statistik finns hos Transportstyrelsen och ska skiljas från Trafikanalys årsprodukt i källa och status.

## confidentiality

Flyglinjedetaljer kan begränsas av statistiksekretess. Metadata anger att företag med färre än fem anställda något av åren inte redovisas. Godkänn inte företags-/linjeuttag bara för att en närliggande dimension finns; följ aktuell struktur och dokumentation.

## Källor

- https://www.trafa.se/luftfart2/luftfart/ (verifierad aktuell produktsida; /luftfart/luftfart/ kunde inte läsas).
- https://www.trafa.se/globalassets/statistik/luftfart/2025/kvalitetsdeklaration-luftfart-2025.pdf (2026-04-13), avsnitt 1.2, 2.2.6, 5 och SOS-avsnitt.
- Struktur t0501, 2026-10-09.
