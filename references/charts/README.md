# Cirkeldiagram från en redan validerad tabell

Generatorn hämtar ingen statistik och ersätter inte klientens urvalsvalidering.
Kör med Node.js 22 eller senare (inga extra paket):

```bash
node scripts/create_pie_chart.mjs evaluation/charts/vehicles-2025.json fordon.png
node --test evaluation/charts/pie.test.mjs
```

Utdata: PNG i 1200 × 950 bildpunkter, `.png.table.json` och `.png.table.md`.
Använd PNG som bild och erbjud samma fil som nedladdning. Visa också tabellen;
en lokal sökväg på en extern MCP-server är ingen fungerande ChatGPT-fillänk.

## Indatakontrakt

Exemplet i `evaluation/charts/vehicles-2025.json` är komplett och återanvändbart.
Fälten title, period, unit, source, query och retrieved_at är obligatoriska.
`rows` har code, label, value (ändligt icke-negativt tal, eller dokumenterat nollstreck), is_total (boolean).
`complete`, `disjoint` och `additive` måste vara true. Dessa är uttryckliga
sakliga intyg från anroparen, inte något en teknisk generator kan bevisa.
Behåll benämningar och skalor från källan. `unit` ska ange faktisk enhet eller,
vid antal med tomt API-enhetsfält, det officiella antalsmåttets benämning.

En period, ett mått, en enhet och en fullständig disjunkt kategoriindelning per
anrop. Gör ingen automatisk sammanslagning, residualberäkning eller sortering.
Totalrader markeras uttryckligen; högst en total tillåts. Den utesluts ur
cirkeln och måste stämma med kategorisumman. Utan publicerad total anges
nämnaren som summa av validerade kategorier. Överlappande kategorier och
procentsatser hör inte hemma i detta kontrakt. Nollrader behålls i tabell och
förklaring. För uppräkningsbara antal: ange `value_kind:"count"` och
`legend_source` med underlaget för teckenförklaringen. Då omkodas endast `-`
och `–` till exakt 0, med originalet i `source_symbol` i utdatatabellen. Ange
inte count för skalade/avrundade antal eller andra kvantiteter. Utan dessa
fält accepteras bara numeriska värden. Andra markeringar omkodas aldrig.
Se [teckenförklaringen](../teckenforklaring.md). Positiva andelar under 0,1 %
visas som `<0,1 %`, så att de inte förväxlas med exakt noll. Tomma tabeller, nollsumma, dubbletter, saknade tal och motstridiga
totaler stoppas. Avrundade mått som inte stämmer exakt ska först utredas,
inte göras godkända med en generell avvikelsetolerans.

Max 12 kategorier; svenska/latinska etiketter stöds. Tecken utan fontstöd ger
fel i stället för tyst ersättning. Fonten är inbäddade rasterglypher från DejaVu
Sans; dess licens medföljer i scripts/charts/FONT-LICENSE.txt. Inga systemfonter,
Matplotlib, webbtjänster eller bildgenereringsmodeller krävs vid körning.

## Verifierade kontrollfall 2026-10-24

* `t10030|nyreg|ar:2025|fslag`: åtta rader, summa 402 098. Aktuell MCP-validering
  och källsvar finns i fordonets `.raw.json`; tabellen är en explicit projektion
  av dessa rader. Fordonsslagen behandlas som disjunkta och antalsmåttet som
  additivt. API-svaret har ingen totalrad.
* `t10036|nyreg|ar:2026|manad:09|drivm`: kombinationen nyreg/ar/drivm/manad finns i
  referensmetadata och det slutliga urvalet validerades mot aktuell struktur av
  MCP-verktyget. Gas har `-` i det oförändrade källsvaret. Efter Toms
  sakgranskning 2026-10-25 tillämpas teckenförklaringen: exakt noll för antal.
  Diagrammet innehåller samtliga åtta kategorier; summa 29 850. Originalstrecket
  bevaras, och omkodningen redovisas i bild, tabell och proveniens. De övriga
  siffrorna kommer från samma daterade API-uttag; ingen ny datahämtning behövs.

Fixturerna är daterade observationer, inte löften om framtida API-värden.

## MCP-integrationen

Serverns källkod finns i det separata Sites-projektet, inte i detta repository.
Den förberedda ändringen lägger till `create_pie_chart` och behåller det äldre
`create_chart` för bakåtkompatibilitet. Kopiera scripts/charts till worker/charts;
serverns build måste inkludera båda modulerna och fontlicensen.

Det nya verktyget returnerar MCP content med `image/png` (base64), en fristående
svensk texttabell samt structuredContent med tabellen och `download_url`.
GET `/chart.png?input=...` validerar den självständiga tabellpayloaden igen och
returnerar samma PNG med `Content-Disposition: attachment`, `no-store` och
`nosniff`. Ingen serversökväg eller minnescache används som fillänk. Länken
innehåller hela tabellen; Sites befintliga åtkomstkontroll gäller även denna
route. Inga lagringsbindningar eller externa bildtjänster införs.

Publicera först efter godkännande och testa sedan i en ny ChatGPT-chatt:
1. Hämta de redan definierade API-kontrollfallen med oförändrad statistikvalidering.
2. Skicka en bekräftad fullständig tabell till create_pie_chart.
3. Kontrollera att PNG visas, att fallbacktabellen syns och att download_url
   går att öppna och ladda ned från det konto som har åtkomst till pluginen.
4. Kontrollera både webb och Android. Prova även att streck med count och
   legend_source blir exakt 0, medan `..`/`.` stoppas. Om värden saknas: behåll råtabellen och
   förklara varför cirkeldiagrammet stoppades.

Lokala HTTP/MCP-tester och PNG-avkodning bevisar serverns svar och bytes.
De bevisar inte att ChatGPT eller Android visar en ännu opublicerad version,
eller att Sites gateway accepterar nedladdningsrouten. Detta återstår efter
publicering; hävda inte verifierad värdvisning före det testet.

Mycket breda benämningar som inte ryms inom layouten stoppas uttryckligen.
Ingen etikett kapas eller ersätts automatiskt. Behåll då tabellen eller använd
en källbelagd kortform. Generatorns avgränsningar är avsiktliga för första versionen.
