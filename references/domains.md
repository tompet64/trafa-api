# Komprimera utan informationsförlust

Skilj komprimerad presentation för modellen från de fullständiga filterkoder som HTTP-anropet behöver. Använd aldrig en lokal domänreferens eller en presentationsförkortning som API-filter.

1. Lista varje variabel en gång inom en produkt. Använd kolumner för kod, benämning, typ, beskrivning och värdemängdsreferens. Håll en tom rad mellan variabler när det ökar läsbarheten.
2. Skapa separata domäner med stabilt lokalt id, källa, produkt/dimension, verifieringsdatum, antal värden och fullständig kod–etikett-mappning. Lagra alla koder som strängar.
3. Deduplicera domäner bara om hela kod–etikett-mappningen, tidsmässig giltighet och relevant semantik överensstämmer. Samma dimensionsnamn eller samma antal värden räcker inte. Ange varje produkts eventuella delmängd explicit.
4. Visa år som exempelvis `2018–2025, 8 värden` endast efter kontroll att varje år finns. Visa luckor explicit. Bevara månads- och kvartalskoder oförändrade. Skapa inte mellanliggande perioder från min/max.
5. Visa stora geografiska domäner som `kommuner → domän-id, N värden`, med uppslag för efterfrågade koder. Anta inte att alla kommuner finns i alla produkter. Bevara historiska indelningar, totalvärden och okända områden separat; anta inte en generell totalkod.
6. Slå upp användarens kommunnamn i den relevanta domänen. Om namnet inte matchar entydigt, utred; skapa inte kod från namn eller från geografiskt minne.
7. Bevara belagda kombinationer som separata poster; komprimera aldrig en lista till ett påstått fritt kartesiskt urval. Dela gemensamma domäner, inte kombinationsregler.
8. Saknas värdemängd, behåll dimensionen med flaggan `värdemängd saknas – behöver verifierat underlag`. Sök först rätt domänbindning i referensfilerna. Hämta därefter relevant struktur endast genom en tillåten anslutning där svaret ryms; beställ inte rutinmässigt hela en redan känd för stor produktstruktur. Uppdatera annars underlaget genom ett separat tillåtet metadataarbete eller stoppa det berörda filtret. Utelämna dimensionen från ett körbart filterindex tills värdena är verifierade, men radera inte dess existens ur fullständig katalog.

Använd en domän för referensvalidering endast om dess uttryckliga `uses`-bindning stämmer med produkt och variabel. Bevara verifieringsdatum och källa. En komprimerad referensrevision får inte uppdateras genom att lägga till gissade senaste år, förväntade kommuner eller ett generellt intervall som fyller dokumenterade luckor. Spara ny struktur- och storleksevidens tillsammans när metadata faktiskt uppdateras.

Domänschema, lokalt och inte API-syntax:
`domain_id, source, retrieved_at, product, dimension, count, values[{code,label}], validity, exceptions`.
