# Regional linjetrafik – T1203

Delvis granskad mot produktsida och kvalitetsdeklaration 2025, lästa 2026-10-11, och metadata från 2026-10-09. Toms sakgranskning 2026-10-11 anger T1203 som primär publicerad statistikprodukt för trafik- och transportfrågor främst om spårväg/tunnelbana. Enligt ett senare besked från statistikansvarige är den underliggande huvudsakliga källan Trafikanalys totalundersökning Bantrafik och Järnvägstransporter; dessa uppgifter används även i T1203. Skilj alltså mellan svarande produkt och primär datakälla. För olyckor/personskador används T0602.

## population

Tidtabellbunden regional linjetrafik, både samhällssubventionerad trafik organiserad av RKM och kommersiell trafik. Inte enbart RKM-trafik och inte all svensk kollektivtrafik eller all järnvägstrafik. Avgränsa regionalt kontra interregionalt och finansiering.

## geography_economy

Subventionerad trafik redovisas per län och riket; kommersiell regional trafik redovisas för riket. Ekonomi samlas endast in för subventionerad trafik. Län ska inte automatiskt tolkas som all trafik som geografiskt utförts inom länet; exakt fördelning av länsöverskridande RKM-trafik behöver kontrolleras vid sådana frågor.

## boardings

pastig är påstigningar, inte unika resenärer eller sammanhållna reskedjor. Tur och retur räknas två gånger och varje övergång ger ny påstigning. Både avgiftsbelagda och kostnadsfria påstigningar ingår.

För jämförelser med RVU: se [resvanor.md](resvanor.md) om huvudresa, delresa, reselement och påstigning. Ett färdsättsbyte innebär inte automatiskt en ny delresa, men kan ge en ny påstigning.

## performed_planned

Utfört utbud omfattar trafik öppen för passagerare inklusive förstärkningstrafik; inställd trafik undantas och depåkörning ska om möjligt undantas. planavg och planutbud baseras på bearbetad tidtabellsdata från Samtrafiken och är planerat utbud, inte observerat utfört utbud. planavg avser avgångar från hållplats/station, inte självklart antalet hela fordonsturer.

## km_measures

utbudskm räknar tåg som enheter i spårtrafik, medan fordonskm räknar spårfordon/vagnar; därför kan de skilja sig. personkm är passagerarnas sammanlagda reslängd. platskm avser sitt- och ståplatser medan sittkm avser sittplatser. Metadata anger dock kapacitetskilometer inklusive ståplatser för fartyg även under sittkm: kontrollera trafikslag och fotnoter före jämförelse.

## units

Metadataetiketter anger tusental för pastig, utbudskm, fordonskm, personkm, platskm, sittkm, planavg och planutbud; intak/kostnad anges i tusental kronor och löpande priser. Nyckeltal intakp*/kostp* anges i kronor per påstigning eller kilometer. Kontrollera svarsenheten och skalfaktorn innan omräkning; använd inte samma faktor för absoluta mått och kvoter.

## ratio_coverage

Publicerade intäkts- och kostnadskvoter bygger enligt metadata endast på respondenter med båda nödvändiga uppgifter. Kvoten kan därför avvika från kvoten mellan publicerade totaler. Använd publicerat nyckeltal när det besvarar frågan; summera inte kvoter och använd inte ovägda medel.

## missingness

API-metadata varnar att rikstotaler och finansieringstotaler är summor av tillgängliga uppgifter. Partiellt bortfall kan ge underskattning. Tolka inte saknade värden som noll eller publicerad total som bevis för full täckning. Metoder och bortfall varierar mellan insamlingar och år.

## rail_overlap

För spårväg och tunnelbana är Trafikanalys totalundersökning Bantrafik och Järnvägstransporter den huvudsakliga källan för trafik- och resandeuppgifter. Dessa uppgifter används även i T1203; T1203 är därmed en publiceringsprodukt för regional linjetrafik, inte en oberoende primär datakälla för just dessa uppgifter. Ekonomi för dessa trafikslag samlas fortsatt från RKM. Regional kommersiell vägtrafik ingår både i T1203 och Kommersiell linjetrafik på väg T1202. Kommersiell regional vattenstatistik särredovisas även i ett eget tabellverk/API-produkt T1204. Summera inte överlappande produkter; all Bantrafiks järnvägstrafik kan inte ersätta RKM:s järnvägsuppgifter.

## measurement

Personkilometer för subventionerad trafik beräknas ofta med antagen medelfärdlängd per påstigning, ibland med stöd av RVU. Beskriv inte transportarbete som genomgående direkt observerad reslängd.

## time_comparability

Utbudskilometer fick definitionsförändringar 2006–2007 och Stockholms pendeltågs vagnkilometer ändrad bas 2008. Vatteninsamlingen hade annan ram 2013 än från 2014. Inför statistikåret 2025 ändrades insamlingsformuläret så att saknade värden måste markeras; partiellt bortfall minskade avsevärt, vilket kan påverka tidsjämförelser. Statliga bussbidrag kan ge engångseffekter i ekonomi. Kontrollera senaste fotnoter och kvalitetsdeklaration.

## publication

Årlig officiell statistik, publicering i juni cirka sex månader efter årets slut. Använd senaste publicering även för tidigare år eftersom äldre publikationer normalt inte uppdateras.

## Källor och API-koder

- https://www.trafa.se/kollektivtrafik/kollektivtrafik/
- https://www.trafa.se/globalassets/statistik/kollektivtrafik/kollektivtrafik/2025/kvalitetsdeklaration-regional-linjetrafik-2025.pdf (2026-06-26), avsnitt 1.2, 2.2.6, 5.1 och bilaga 9.
- `finans:1` kommersiell, `finans:2` subventionerad; `traslag:1` väg, `2` järnväg, `3` spårväg, `4` tunnelbana, `5` sjötrafik. `t1` är total i respektive dimension; slutvalidera aktuellt urval.

## Komplettering efter test 8, 2026-10-14

För frågor om Regional linjetrafik, hämta T1203 och begär båda trafikslagen samtidigt. Verifierat exempel för ett helår: `t1203|pastig|ar:2025|finans:2|traslag:3,4` gav två numeriska rader. Vid frågor om senaste år, fastställ aktuellt högsta konkreta år i relevant struktur och hämta endast det året; 2025 är ett verifierat exempel, inte ett permanent senaste år. En tidigare kontroll bekräftade numeriska värden för båda trafikslagen samtliga år 2022–2025 med finans:2 explicit. Den kontrollens fyraårsintervall ska inte återanvändas som standarduttag. Ett tomt uttag utan finans får inte beskrivas som att produkten saknar dessa år.

Tom bekräftar att motsvarande Bantrafik-tal finns 2022–2025 och betecknar samma påstigningar, avrundade till miljontal i stället för tusental i T1203. Bantrafik 2025:s statistikblad bekräftar 2025 års spårvägs-/tunnelbanevärden. Alla prövade API-varianter av T06013 i denna felsökning gav DataCount 0; en fungerande T06013-query har därför inte verifierats här. Kalla inte detta att Bantrafik saknar uppgifter. Källa: https://www.trafa.se/globalassets/statistik/bantrafik/bantrafik/2025/bantrafik-2025.pdf .

Korrigering av tidigare osäkerhet om källkedjan: enligt Toms återgivning av besked från statistikansvarige (2026-10-23) är totalundersökningen Bantrafik och Järnvägstransporter huvudsaklig källa för spårväg och tunnelbana, och uppgifterna används också i Regional linjetrafik. Detta stämmer med riktningen i kvalitetsdeklarationen för T1203 (Bantrafik/Järnvägstransporter → T1203). Den tidigare formuleringen om motsatt riktning ska inte återanvändas. Ekonomins insamling är en separat fråga.
