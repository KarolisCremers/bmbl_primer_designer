Bmbl Primer Designer
====================

De benodigdheden om dit programma te runnen is de volgende software:
* Python 2
* Wx python

Op windows is dit eenvoudig te installeren door eerst python 2 te installeren met behulp van het bestand op de volgende link:
https://www.python.org/downloads/

Vervolgens moet wx Python geïnstalleerd worden, wat gedownload kan worden vanaf onderstaande link:
https://wxpython.org/download.php

Let hierbij op bij het installeren dat dit in de map geïnstalleerd moet worden van Python 2, welke dus is ingegeven bij de installatie van python 2.

Op linux is dit eenvoudiger, aangezien python al geïnstalleerd is en wx Python een package in de ubuntu repository is. Voer de volgende commando's uit op een terminal:
sudo su
apt-get update
type -P python2 &>/dev/null/ && echo "Python 2 already installed " || apt-get install python2
apt-get install python-wxgtk3.0

Instructies runnen applicatie:
* Windows:
    * Ga naar het zip bestandje en pak deze uit in dezelfde map
      (Stel het volgende: C:\Downloads\BmblPrimerDesing.zip dus uitpakken waardoor de map C:\Downloads\BmblPrimerDesign onstaat.
       Uiteraard kan dit ook een map naar keuze zijn.)
    * Ga naar de map welke de python bestanden bevat.
    * shift + rechtermuisklik, kies "Opdrachtvenster hier openen"
    * Vervolgens moet je het volgende commando uitvoeren:
python Frame.py
* Linux:
    * Ga naar het zip bestandje in de terminal
    * Voer de volgende commando's uit:
unzip BmblPrimerDesign.zip
cd BmblPrimerDesign
python2 Frame.py

Instructies instellen programma:
Het programma kent 4 gegroepeerde invoervelden:
1. Linksboven bevat het invoerveld voor de DNA sequentie waaruit primers gehaald moeten worden (of de algehele sequentie, zie puntje 2). In dit veld kan geplakt en getypt
   worden en het maakt niet uit of de text kleine of grote letters bevat. Het programma haalt automatisch letters eruit welke geen nucleotide representeren, echter geeft
   het daar geen melding van. Het wordt simpelweg gewoon gedaan.
2. Rechtsboven bevat de invoer om de lengte van het maximale PCR product in te voeren, samen met de invoer van de anneal range. Deze range bepaald waar de primers
   werkelijk mogen annealen, en dus daar primers in mogen worden gevonden. Het minimum is altijd minder dan het maximum en het maximum is dus altijd meer dan het minimum.
    Afhankelijk van de lengte van de sequentie worden de maximale instellingen aangepast (dat wil zeggen, je kan een range niet groter maken dan de grootte van de
    sequentie).
De volgende groepen zijn optioneel, en hoeven dus niet per definitie ingevuld te worden.
3. Linksonder kan een target aangegeven worden welke binnen de anneal range valt, met hetzelfde principe van diezelfde spinners. Wanneer men een target wilt zoeken, moet
   de "Use target" checkbox wel aangevinkt worden, anders vindt het programma primers welke proberen de hele anneal range te bevatten.
4. Rechtsonder kan worden aangegeven welke checks op de primers moeten worden uitgevoerd, echter zijn deze zeer experimenteel. Normaliter worden deze checks ondersteund
   met vrije energie berekeningen, echter wordt dit in het programma gedaan puur gebaseerd op de sequentie van een primer. Om deze reden is het expirementeel.

De belangrijkste stap van het instellen, is het instellen van het maximale PCR product en de annealing range. Wanneer het maximale PCR product 0 is, kan er nooit een
primer uitkomen aangezien het PCR product te klein is. Het PCR product is in te stellen tot het maximum van de annealing range minus het minimum van de annealing range.
Vervolgens moet er een degelijke annealing range ingesteld worden. In deze range wordt aangegeven in welke locatie van de gegeven sequentie de primers mogen
annealen. Wanneer deze niet ingesteld wordt, is er geen plek voor de primers en dus kunnen er geen primers gevonden worden.

Een optionele instelling is om primers te zoeken voor een target sequentie. Dit wordt gedaan met behulp van de "use target" checkbox. Wanneer deze checkbox aangevinkt
is, zal gezocht worden voor een primer paar welke het beste de target range bevat. Wanneer deze range zeer groot is, is het mogelijk dat er minder snel een goed primer
paar wordt gevonden. Let erop dat hierbij ook de PCR grootte en annealing range een rol speelt! De range van het target moet tussen de annealing range liggen zodat
primers gevonden kunnen worden in die sequentie (of omgeving, afhankelijk van de instelling).

Wanneer er geen primers worden gevonden met de experimentele checkers, is het mogelijk dat deze te veel primers weg filtert. Het advies luidt dan ook om deze niet te
gebruiken, maar verveling heeft toegeslagen en is toch wel geïmplementeerd.

Wanneer op "Search primers" gedrukt wordt, zal het programma het beste primer paar presenteren. Wanneer dit niet het geval is, zal het aangeven dat er geen primers
gevonden zijn. Vervolgens kan met de knop daar weer teruggegaan worden naar instelscherm waarvan de instellingen zijn bewaard.
Overigens kan het lijken bij lange sequenties dat het programma niet reageert, maar in realiteit is het programma berekeningen aan het maken.

Voorbeelden
===========

In alle voorbeelden wordt de volgende sequentie gebruikt (lengte 200nt):
TCGTACAGACCGAAATCTTAAGTCAAATCACGCGACTAGGCTCAGCTCTATTTTAGTGGTCATGGGTTTTGGTCCGCCCGAGCGGTGCAACCGATTAGGACCATGTAAAACATTTGTTACAAGTCTTCTTTTAAACACAATCTTCCTGCTCAGTGGCGCATGATTATCGTTGTTGCTAGCCAGCGTGGTAAGTAACAGCA

Voorbeeld 1:
Een primer paar vinden zonder target. Een primer paar moet gevonden worden in de annealing range van 50 tot 150. Hier kan ik geen real life use case bij verzinnen, en
 us doen we het maar gewoon.

In deze volgorde zijn de instellingen gedaan:
1. Ervoor zorgen dat de "Use target" NIET aangevinkt is.
2. De annealing range instellen van 50 tot 150
3. Het Max PCR product instellen tot 100, zodat elk primer paar over de hele anneal range mogelijk is. (Er komt echter geen lijst van primers uitrollen, dit is
   toekomstige functie)
4. Ik vind het belangrijk dat primers zo veel mogelijk checks hebben gehad, dus ik vink alle experimentele checkers aan.
5. Search primers!

Hieruit kwam de volgende output (dit is een ASCII tabel, niet de werkelijke grafische output):

            +---------------------------+--------------------------+
            | Forward primer            | Reverse primer           |
+-----------+---------------------------+--------------------------+
|Sequence:  | 5'-GTGGTCATGGGTTTTGGTC-3' | 5'-CACGTTGGCTAATCCTGG-3' |
|Melt temp: | 58C                       | 56C                      |
|GC%:       | 52.6315789474%            | 55.5555555556%           |
|Position:  | 56..75                    | 85..103                  |
|PCR:       | 47                        |                          |
+-----------+---------------------------+--------------------------+

Voorbeeld 2:
Een primer paar vinden met target. Het doel hierbij is om primers te vinden om een PCR uit te voeren voor de sequentie 30..90.

In deze volgorde zijn de instellingen gedaan:
1. Ervoor zorgen dat "Use target" aangevinkt is.
2. De annealing range instellen van 1 tot 120. (Soms is het spelen met deze instelling omdat je nooit weet waar de primers zich bevinden)
3. Het maximum PCR product instellen op 75. (Hiermee is soms ook even spelen met de instelling nodig)
4. De target range instellen van 30 tot 90.
5. Wederom alle experimentele checks aanvinken, want controlestappen zijn meestal goed.
6. Search primers!

            +---------------------------+--------------------------+
            | Forward primer            | Reverse primer           |
+-----------+---------------------------+--------------------------+
|Sequence:  | 5'-TCAATCACGCACTAGGC-3'   | 5'-CTCGCCACGTTGGCTAAT-3' |
|Melt temp: | 58C                       | 56C                      |
|GC%:       | 52.6315789474%            | 55.5555555555%           |
|Position:  | 23..42                    | 80..96                   |
|PCR:       |  75                       |                          |
+-----------+---------------------------+--------------------------+
