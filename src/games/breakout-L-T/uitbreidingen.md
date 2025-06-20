1 stuiter algoritme
 - de hoek waarmee de bal binnenkomt word berekend 
    (eerst de richtingscoefficient met Dy/Dx, en dan is de hoek de inverse tangens van de richtingscoefficient)
 - vervolgens word de hoek van de spiegellijn berekend
    dit is de lijn waarin de binnenkomende hoek word gespiegeld om de uitgaande hoek te berekenen
    (opnieuw eerste de richtingscoefficient met Dy/Dx, en dan de inverse tangens voor de hoek)
    (Dy is altijd hetzelfde, namelijk een punt ver onder de paddle)
    (Dx is de plek waarop de bal de paddle raakt)
 - als we hoek ingaand en hoek spiegellijn hebben kunnen we hoek uitgaand berekenen
 - met hoek uitgaand en de diagonale ballspeed (blijft hetzelfde) kunnen we de x en y componenten van de snelheid uitrekenen
    x = sin(hoek uit) * diagonale snelheid
    y = cos(hoek uit) * diagonale snelheid
 - nu veranderen de hoeken door het spel om te zorgen dat het spel leuk blijft om te spelen, om zelf nog meer sturing te geven 
aan de bal hebben we ook toegevoegd dat de bewegingsrichting van de paddle meegenomen wordt. Dit heeft geen invloed op de hoek van de bal, maar wel op de x richting. De bal zal altijd de richting van de paddle op bewegen.
 - ik hoop dat u nu snapt wat er onder de motorkap gebeurt met het stuiteren van de bal(len) op de paddle, zo niet, dan willen wij u dit graag nog uitleggen.

2 blokken die van kleur veranderen
 - blokken hebben meerdere levens
 - groene blokken zullen eerst paars, dan geel, dan blauw en als laatste rood worden voordat ze verdwijnen
 - dit geld voor alle blokjes, ongeacht op welke kleur ze beginnen.
 - daarnaast hebben alle blokjes 40% kans om hun kleur te behouden de eerste keer dat ze geraakt worden, deze zal dan een gebroken uiterlijk krijgen en zal pas de volgende keer dat deze geraakt word een kleurtje omlaag gaan.

3 levens
 - als alle ballen verdwenen zijn (de grond geraakt hebben), dan zal de speler een hartje verliezen (rechtsboven in het scherm). Als alle hartjes weg zijn moet de speler opnieuw beginnen. De score wordt gereset en de speler moet weer terug naar level 1.

4 score
 - elke keer dat een bal een blokje raakt wordt de score groter (+100)

5 meerdere levels
 - als een level gehaald is kan je door naar het volgende level. Deze heeft nieuwe blokjes met nieuwe vormpjes.
 - level 1 t/m 5 zijn handmatig gemaakt, daarna worden ze random gegenereerd. (Zie uitbreiding 8)

6 powerups
 - als een bal een blokje raakt is er een kans (afhankelijk van het soort powerup) dat er een sterretje naar beneden valt.
 - als dit sterretje wordt opgevangen op de paddle zal de speler een powerup krijgen.
 - er zijn de volgende powerups:
    - extra hartje (kans bij het breken van een rood blokje)
    - extra bal (kans bij het breken van een blauw blokje)
    - laser modus (kans bij het breken van een geel blokje)
    - guns (kans bij het breken van een paars blokje)
 - om te testen en voor u om te bekijken, hebben we een paar knopjes op het toetsenbord toegevoegd om de powerups te activeren
    dit hoort natuurlijk niet bij het echte spel, maar het is voor het ontwikkelen, en beoordelen (;, wel handig.
    - [1] = lasermodus
    - [2] = extra ballen
    - [3] = guns
    - [4] = extra hartjes

7 betere spritesheet gemaakt
 - omdat het er leuk uitziet en om bijvoorbeel de lasermodus duidelijk te maken (met een vuurbal) hebben we de bestaande spritesheet aangepast en verbeterd naar onze behoeftes

8 automatische level maker 
 - er komen iedere 500000 score 1 nieuwe rij en breedte bij totdat het 12 bij 10 is
 - blokken krijgen kleur gebaseerd op moeilijkheid
 - als laatste worden er blokken verwijderd gebaseerd op de score

9 pauzeerknop 
 - druk op [p] om het spel te pauzeren

10 verschillende paddle animaties
 - onze paddle is geanimeerd, het electriciteitsdraadje beweegt
 - dit werkt ook voor het uiterlijk tijdens de lasermodus en de guns powerup

11 game-over en uitleg-scherm
 - als er een level voltooid is of het spel begint of de speler is af dan wordt er op het scherm weergegeven wat de spelstatus is en wat de speler moet doen om verder te gaan

 12 balletje en paddle gaan steeds sneller
 - de score vermenigvuldigen met een muliplier en dit toevoegen aan de basissnelheid