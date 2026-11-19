# Täckning, jämförbarhet och oförklarade avvikelser

Läs vid tidsserier, flera statistikprodukter, saknade detaljrader eller en total
som inte stämmer med delarna. Kontrollerna gäller det använda underlaget, inte
hela produkten eller modellens allmänna tillförlitlighet.

## Före och efter uttaget

- Matcha efterfrågade år mot produktens konkreta värdekoder före statistikuttagen.
  Redovisa år utanför domänen; anta inte att domänen garanterar observationer för
  alla kvartal eller kategorier. Utvidga inte användarens period tyst.
- Spara produkt, query, period, geografisk avgränsning, population, mått, enhet,
  hanteringsprincip och publicerings-/revisionsstatus per serie. Samma måttkod
  eller enhet bevisar inte samma omfattning. Okänd definition är okänd, inte lika.
- `row_count = DataCount` är inte bevis för fullständig observationstäckning.
  Kontrollera förväntade nycklar när frågan behöver en komplett serie/tabell.
  En förväntad korsprodukt kräver sakligt stöd; glesa tabeller kan vara legitima.
  Saknade kombinationer, numerisk noll och sekretess/symboler är skilda tillstånd.
- Summera bara disjunkta, additiva och tillräckligt täckta delar. Kontrollera mot
  publicerad total när den finns. Bedöm avrundning i originalenheten: vid
  avrundning till närmaste enhet kan n delvärden och en total tillsammans avvika
  med högst `(n+1)/2` enheter. Använd inte den gränsen för trunkering, okänd
  avrundningsmetod eller data från olika revisionsversioner.
- Rullande fyra kvartal kräver fyra kronologiskt sorterade, sammanhängande
  kvartal. Ett bortfall får inte bli noll eller ersättas av nästa tillgängliga
  kvartal. Märk egna beräkningar och behåll originalvärdena.

## Belägg för en förklaring

Skilj observerad differens, dokumenterad avgränsning och möjlig förklaring.
En numerisk avstämning är inte ensam bevis för orsaken. En likhet under ett år
fastställer inte samma samband för övriga år. Använd inte differensen för att
konstruera ett saknat förklaringsled och sedan hävda att orsaken verifierats.
Testa inte ett lossat mått som om det vore både lastat och lossat. Även en
fördubbling behöver uttryckligt sakstöd; den kan högst vara en märkt kontroll.

Definitioner och avgränsningar framgår inte alltid tydligt av API:et. Sök först
i produktreferensen. Vid en konkret dokumentationslucka, läs relevant
kvalitetsdeklaration och vid behov äldre publicerade Excel-tabellers rubriker,
noter och definitioner. Ange edition och avsnitt/cell och håll dokumentationsstöd
skilt från statistikkälla. Ett dokument från en äldre publicering bevisar inte
att en senare revision eller ett annat API-urval har samma omfattning.

## Misstänkta brister i API:et

Efter den begränsade kontrollen av dokumenterade urvalsvägar: redovisa det
exakta uttaget och vilka värden/nycklar som saknas eller motsäger en total.
Uppmana användaren att själv kontrollera andra publiceringsformer via den
aktuella produktsidan och rapportera misstänkta brister till statistikansvariga
via kontaktinformationen där. Om andra publiceringar inte har kontrollerats,
påstå inte att de innehåller värdena. Om de har kontrollerats, ange skillnaden
med period, urval och version. Kalla inte en misstanke för fastställd rotorsak.
Hitta inte på namn, e-postadresser eller kontaktvägar och skicka ingen rapport
utan uttrycklig beställning. Byt inte statistikkälla tyst eller utöver uppdraget.

## Körbara kontroller

`python scripts/statistics_checks.py kontroll.json --output kontrollresultat.json`
läser enbart tilldelad JSON; inga nätanrop görs. Indata är ett objekt med en eller
flera av följande kontroller:

```json
{
  "years": {"requested": ["2016", "2020"], "available": ["2020", "2021"]},
  "coverage": {"rows": [{"q": "1", "value": 0}], "keys": ["q"], "expected_keys": [["1"], ["2"]]},
  "totals": [{"total": "34634", "parts": ["18704", "19530"], "complete": true, "disjoint": true, "additive": true, "rounding_unit": "1"}],
  "explanation": {"difference": "1597", "components": ["800", null]}
}
```

`scopes` tar `left` och `right`, vardera med `metric`, `unit`, `population`,
`geography`, `period` och `handling`. Dessa uppgifter måste vara källbelagda;
verktyget kan inte fastställa dem från en etikett. `complete`, `disjoint`,
`additive`, `expected_keys` och `rounding_unit` är granskarens uttryckliga
förutsättningar, inte egenskaper som verktyget själv bevisar. Kontrollera
resultatets status; en lyckad körning betyder inte att data är godkända.
