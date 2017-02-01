Bmbl Primer Designer
====================

De benodigdheden om dit programma te runnen is de volgende software:
* Python 2
* Wx python

Op windows is dit eenvoudig te installeren door eerst python 2 te installeren met behulp van het bestand op de volgende link:

Vervolgens moet wx Python geïnstalleerd worden, wat gedownload kan worden vanaf onderstaande link.

Let hierbij op bij het installeren dat dit in de map geïnstalleerd moet worden van Python 2, welke dus is ingegeven bij de installatie van python 2.

Op linux is dit eenvoudiger, aangezien python al geïnstalleerd is en wx Python een package in de ubuntu repository is. Voer de volgende commando's uit op een terminal:
sudo su
apt-get update
type -P python2 &>/dev/null/ && echo "Python 2 already installed " || apt-get install python2
apt-get install python-wxgtk3.0

Instructies runnen applicatie:
* Windows:
    * Ga naar het zip bestandje en pak deze uit in dezelfde map
      (Stel het volgende: C:\Downloads\BmblPrimerDesing.zip dus uitpakken waardoor de map C:\Downloads\BmblPrimerDesign onstaat. Uiteraard kan dit ook een map naar keuze zijn.)
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
1. Linksboven bevat het invoerveld voor de DNA sequentie waaruit primers gehaald moeten worden (of de algehele sequentie, zie puntje 2). In dit veld kan geplakt en getypt worden en het maakt niet of de text kleine of grote letters bevat. Het programma haalt automatisch letters eruit welke geen nucleotide representeren, echter geeft het daar geen melding van. Het wordt simpelweg gewoon gedaan.
2. Rechtsboven bevat de invoer om de lengte van het maximale PCR product, samen met de invoer van de anneal range. Deze range bepaald waar de primers werkelijk mogen annealen, en dus daar primers in mogen worden gevonden. Het minimum is altijd minder dan het maximum en het maximum is dus altijd meer dan het minimum. Afhankelijk van de lengte van de sequentie worden de maximale instellingen aangepast.
De volgende groepen zijn optioneel, en hoeven dus niet per definitie ingevuld te worden.
3. Linksonder kan een target aangegeven worden welke binnen de anneal range valt, met hetzelfde principe van diezelfde spinners. Wanneer men een target wilt zoeken, moet de "Use target" checkbox wel aangevinkt worden, anders vindt het programma primers welke proberen de hele anneal range te bevatten.
4. Linksonder kan worden aangegeven welke checks op de primers moeten worden uitgevoerd, echter zijn deze zeer experimenteel. Normaliter worden deze checks ondersteund met vrije energie berekeningen, echter wordt dit in het programma gedaan puur gebaseerd op de sequentie van een primer.

Wanneer op "Search primers" gedrukt wordt, zal het programma de beste primer paar presenteren. Wanneer dit niet het geval is, zal het aangeven dat er geen primers gevonden zijn. Vervolgens kan met de knop daar weer teruggegaan worden naar instelscherm waarvan de instellingen zijn bewaard.
Overigens kan het lijken bij lange sequenties dat het programma niet reageert, maar in realiteit is het programma berekeningen aan het maken.