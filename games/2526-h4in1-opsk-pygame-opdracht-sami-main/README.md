# PyGame opdracht
Hier is mijn code ig <br/>
[idk.py](/neferen/idk.py) moet je negeren

## Code uitvoeren

eerst moet [rust](https://rust-lang.org/tools/install/) zijn geinstalleert en [python](https://www.python.org/downloads/) [3.14](https://www.python.org/downloads/latest/python3.14/) of later <br/>

uitvoeren
```sh
pip install .
maturin develop
python3 -m pijthon_psel
```

met virtual env
```sh
python -m venv .venv
source .venv/bin/activate
pip install .
maturin develop
python3 -m pijthon_psel
```

## Code waar wat hoe

| waar                                  | wat                                   | hoe                   |
|---------------------------------------|---------------------------------------|-----------------------|
| [pijthon_psel](/pijthon_psel)         | python code                           | pygame python module  |
| [pijthon_psel_ffi](/pijthon_psel_ffi) | rust code voor versnelling van dingne | rust project met pyo3 |


## Opdracht

<a href="https://stanislas.informatica.nu/game/?authuser=0" style="color:grey; text-decoration:none">source</a>

- [ ] ~~Stap 0: Kopieer startcode voor je game~~ nee
- [ ] ~~Stap 1: Voeg commentaar toe~~
- [x] Stap 2: Beweeg de bal schuin
- [x] Stap 3: Stuiter de bal tegen de onder- en bovenkant van het scherm
- [x] Stap 4: Teken de plank
- [x] Stap 5: Beweeg de plank
- [x] Stap 6: Stop de plank aan de randen van het scherm
- [x] Stap 7: Stuiter de bal tegen de plank
- [x] Stap 8: Stop het spel als je af bent
- [x] Stap 9: Toon een bericht als je af bent
- [x] Stap 10: Teken een blok in het veld
- [x] Stap 11: Detecteer als de bal het blok raakt
- [x] Stap 12: Stuiter de bal omhoog als hij het blok raakt
- [x] Stap 13: Stuiter de bal omlaag als hij het blok raakt
- [x] Stap 14: Stuiter de bal links of rechts als hij het blok raakt
- [x] Stap 15: Maak een tweede blok
- [x] Stap 16: Zet blokken in genummerde lijsten
- [x] Stap 17: Gebruik for-loop bij blokken tekenen
- [x] Stap 19: Maak een veld met 24 blokken
- [x] Stap 20: Haal een blok weg als de bal een blok raakt
- [x] Stap 21: Toon bericht als je wint

- [x] Uitbreiding: Bal die steeds sneller gaat ⭐️
- [x] Uitbreiding: Blokken van verschillende kleuren tekenen ⭐️ of ⭐️⭐️
- [x] Uitbreiding: Blokken laten barsten bij de eerste hit en verdwijnen bij de tweede hit ⭐️ of ⭐️⭐️
- [x] Uitbreiding: Beter kaats-algoritme voor plankje ⭐️ of ⭐️⭐️
- [x] Uitbreiding: Uitlegscherm en gameoverscherm ⭐️ of ⭐️⭐️
- [ ] ~~Uitbreiding: Animaties als een blok verdwijnt ⭐️⭐️⭐️~~ geen zin
- [x] Uitbreiding: Meerdere ballen tegelijk ⭐️⭐️⭐️ of ⭐️⭐️⭐️⭐️
- [x] Uitbreiding: Schieten ⭐️⭐️⭐️ of ⭐️⭐️⭐️⭐️


## Uitbereidingen 

~~Wij~~ Ik heb deze uitbreidingen gemaakt:

- [x] paddle snelheid hangt af van hoogte
- [x] meerdere block tiers en cracking
- [x] levels in json
- [x] meerdere levels
- [x] scoreboard
- [x] maak powerups
- [ ] multiplayer
- [ ] interactieve tutorial
- [ ] main menu scroll menu
- [ ] level editor

- [x] gebruik classes
- [x] voeg main menu
- [ ] ~~gebruik vectors~~ onnodig
- [ ] ~~voeg event engine~~
- [ ] collision raytracing, trace path from previous frame to current frame and check for collisions
- [ ] optimize loops
- [ ] cleanup imports

- [x] versschillende art-styles
- [ ] sfx
- [ ] ~~motion blur~~ vervelend met pygame
- [ ] switch to single file textures
- [ ] make all coords relative

- [ ] ffi accelerated
- [ ] cross platform multiplayer
- [ ] microtransactions
- [ ] gambling

<i style="color:grey">

- [ ] geplanned
- [x] afgerond
</i>


## ConceptArt
![menu concept](/rest/ConceptMenu-dark.svg)
