# Uitbereidingen 

Goedemorgen!
Wij hebben op de basisgame, te maken door de stappen te volgen op de [informatica website](https://stanislas.informatica.nu/), de volgende uitbreidingen gemaakt:

## Gelijk zichtbaar
Zoals je gelijk al kunt zien als je het spel opent, hebben we een Menu toegevoegd, met een zelf gemaakte achtergrond. Zoals het menu al zegt, kun je op twee toetsen drukken om naar de bijbehorende spel modi te gaan. Je kunt ```r``` indrukken voor *Bricked* en ```c``` voor *Pong*.

Je kunt altijd naar dit menu terugkeren door in een willekeurige modus op de toets ```q``` te drukken, en altijd pauzeren door op ```c``` te drukken.

In de modi zijn gelijk meerdere dingen zichtbaar. Daarom staan ze hier in een handig lijstje.

- Nieuwe achtergrond toegevoegd.
- Levens, in de vorm van hartjes. Bij *Bricked* staan ze linksboven en bij *Pong* linksboven en rechtsonder voor respectievelijk beide spelers. <br> Elke keer dat de bal voorbij de paddle komt, of in *Pong*, voorbij één van de paddles, gaat er van die speler een hartje af.
- Een Highscore, te vinden in de rechterbovenhoek.
    - Deze neemt toe wanneer een blok explodeert en natuurlijk over tijd. Deze is invloedbaar door een van de powerups.
    - Je highscore verschijnt ook boven het *"You lost!"*/*"You won!"* bericht als het spel eindigt.
- De bloklayout aangepast naar de vorm van een *Space Invader*.

## Tijdens het spelen
Gelijk als je begint met spelen zie je gelijk dat de bal begint op een willekeurige horizontale plek. Dit gebeurt ook wanneer een leven omlaag gaat, en is zo zodat je niet telkens hetzelfde spel speelt.

Als je een blok raakt merk je ook dat er nu meerdere stages zijn, een blok breekt eerst voordat hij bij de volgende keer raken verdwijnt. Als een blok breekt merk je ook op dat er een kans is dat een speciaal object eruit valt;

> Controls

Je beweegt de paddle met ```a``` en ```d```. In *Pong*, waar er twee paddles zijn, speelt speler twee met de toetsen ```j``` en ```l```.

> Een Powerup.

Deze worden willekeurig bepaald voordat het spel start. Er zijn twee soorten powerups die een brick kan hebben;
1. Een speed boost. Deze maakt de paddle sneller.
2. Een highscore multiplier. Deze stackt, dus stel je voor je hebt all een multiplier, als je er dan nog een pakt komt er 0.5 bij. Dus van ```1.5x``` multiplier naar ```2.0x```.
Als je een powerup hebt, verschijnt er een counter links naast de highscore. Deze geeft aan hoe lang je de powerup nog hebt. Voor beide powerups is er een eigen counter.

> Statusberichten

1. Een static status bericht in het rood, verschijnt in het midden van het scherm als;
    - Een speler verliest
    - Het spel op pauze staat
    - Een speler wint.
2. Een status bericht met een fade, is ingebouwd in een zelfgemaakte functie. Je kunt het bericht, duratie in seconden, en kleur opgeven als (bericht, duratie, kleur). Deze verschijnt wanneer;
    - De speler een leven verliest
    - Als de speler een powerup pakt
    - Het spel met de debugfunctie wordt gerestart

> Animaties

Er zijn meerdere animaties, bestaande uit een varierend aantal frames.
Deze zijn:
- Een explosie Animatie wanneer een steen verdwijnt. Deze heeft ```10``` frames.
- Een stofwolk animatie als de bal de rand raakt. Deze heeft ```6``` frames.

> Debug tools

Ook hebben we meerdere debug tools toegevoegt, voor het comfort van de tester / gebruiker.
Onder deze vallen:
- Testmodus waarbij de paddle automatisch de bal volgt.
<br> Druk op toets ```t```.
- Pauzetoets.
<br> Druk op toets ```c```.
- Restart toets (Alleen *Bricked*).
<br> Druk op toets ```r```.

## Buiten het spel
Deze uitbreiding is alleen zichtbaar in de code. We hebben de lijsten logica uit de stappen verandert naar een array met data keys voor meer overzicht.



