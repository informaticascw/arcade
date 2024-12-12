# arcade

This repository will be used to make the code for an arcade running python games.

It is inspired on the arcade running javascript games at [https://github.com/emmauscollege/arcade](https://github.com/emmauscollege/arcade)

# werkafspraken

-   code alleen aan de main-branche toevoegen als hij runt en leesbaar is
-   altijd documentatie (readme) aanpassen tegelijk met je code
-   maak incidenten aan en assign die aan jezelf, zodat iedereen ziet waaraan je werkt

## Menu

-   Run `./src/menu/main.py` to start

    Ik doe mn best om over alles te commenten maar mischien mist er ergens nog iets.

    `/menu` bevat:

    -   `/components`: Dit is een componenten library met allemaal classes om menu pages / hud elements te maken.
    -   `/events` Een apparte module om pygame events te handelen.
    -   `/pages` Dit is een collectie aan pages die in het menu zitten, elke file stelt een pagina voor, hierin zit een variable dat verwijst naar een ge-inialized page component uit de components library. Er moet een page met de naam "main" aanwezig zijn, dit is het entry point voor het menu, er kunnen geen dubbele page namen voorkomen, dit veroorzaakt een error.

    -   `/util` Extra utility om te helpen met verschillende dingen:
        -   `/constants`: Constante waardes voor het project, zoals resolutie, fps, kleuren, etc.
        -   `/data`: Een bestand dat een `data` variable bevat waarin je data mee op kunt slaan op een data.json bestand
        -   `/router` Dit initialiseert de `Router` component van de components library. Dit is een centraal punt om te navigeren door de menu pages (en de verschillende games).
