# Kommersiell linjetrafik på väg – T1202

Delvis granskad mot produktsida, kvalitetsdeklaration 2025 och API-metadata. Konkret urval ska slutvalideras.

## population

Kommersiell tidtabellbunden kollektivtrafik på väg öppen för allmänheten i Sverige, utan offentlig trafikreglerande avtalsrelation. Inte all busstrafik eller trafik med privata utförare: offentligt upphandlad trafik är inte kommersiell i denna mening. Anropsstyrd trafik, charter och icke linjelagd beställningstrafik ingår inte.

## frame

Målpopulationen identifieras genom kommersiell trafik anmäld till Samtrafikens tidtabellsdatabas, med krav på planerat utbud minst 200 mil (2 000 km). Företag kan ingå även om de inte trafikerat hela året. Ej anmäld trafik kan ge undertäckning i förhållande till intressepopulationen.

## classification

Insamlade uppgifter indelas regional/interregional på företagsnivå; samtliga uppgifter förs till företagets kategori även vid blandad trafik. Planerat utbud klassificeras utifrån turer med särskild metod för länsöverskridande trafik. Anta inte att regional betyder enbart inom ett län eller att de två måttfamiljerna har identisk klassificeringsenhet.

## overlap

Den regionala redovisningsgruppen ingår även i Regional linjetrafik T1203. Summera inte hela T1202 med T1203. För regional kommersiell vägtrafik kan båda vara relevanta källor; kontrollera version och urval. Interregional trafik hör till T1202.

## boardings

pastig är påstigningar, inte unika resenärer eller hela reskedjor. Tur/retur ger två och byten ny påstigning. Avgiftsbelagda och kostnadsfria påstigningar ingår, men resande med biljettgiltighet från subventionerad trafik ska inte tas med enligt kvalitetsdeklarationen.

## planned_performed

utbudskm avser utförd passagerartrafik inklusive förstärkning och exklusive inställd trafik; depåkörning ska om möjligt undantas. planutbud och planavg kommer från bearbetad tidtabellsdata, inte observerad utförd trafik. planavg räknar avgångar från hållplatser: en tur med två mellanliggande hållplatser ger tre avgångar.

## capacity

Exakt kod sittkm har etiketten Platskilometer i T1202. Kvalitetsdeklarationen definierar platskilometer med både sitt- och ståplatser. Tolka inte kodnamnet som sittplatskilometer eller överför betydelsen från andra produkter.

## units

API-måtten pastig, utbudskm, personkm, sittkm, planavg och planutbud har etiketter i tusental. Kontrollera svarsenhet och skala före omräkning. Produkten har inga ekonomimått i sparad metadata; komplettera inte med T1203:s subventionerade ekonomi som om den avsåg kommersiell trafik.

## uncertainty

Bortfall och mätosäkerhet påverkar resultaten; bortfall kan imputeras. För 2025 återanvändes föregående års uppgifter för ett bortfallsföretag och inget partiellt bortfall förekom enligt deklarationen. Generalisera inte detta till andra år eller till universella korrigeringsfaktorer.

## comparability

Före 2017 är jämförbarheten sämre genom ändrade frågor, populationsidentifiering och imputering. Föregångaren Långväga buss omfattade trafik över minst en länsgräns och har inte samma population som dagens regionala plus interregionala kommersiella trafik. Skarva inte serier utan kontroll av definitioner.

## publication

Årlig officiell statistik om utbud och resande, endast slutlig statistik redovisas; publicering i juni cirka sex månader efter året. Regional/interregional/totalt är de aktuella API-grupperna; inget län eller operatör finns i sparad metadata. Exakt täckning ska kontrolleras vid uttag.

## Källor

- https://www.trafa.se/kollektivtrafik/linjetrafik-pa-vag/ (läst 2026-10-11).
- https://www.trafa.se/globalassets/statistik/kollektivtrafik/kommersiell-linjetrafik/2025/kvalitetsdeklaration-kommersiell-linjetrafik-pa-vag-2025.pdf (publicerad 2026-06-26, läst 2026-10-11), avsnitt 1.2, 2.2 och 4.
- Sparad API-struktur t1202, 2026-10-09. `trafiktyp:1` regional, `2` interregional, `t1` totalt.
