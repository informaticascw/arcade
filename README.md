# arcade

This repository contains the code for an arcade running python games.

It is inspired on the arcade running javascript games at:
[https://github.com/emmauscollege/arcade](https://github.com/emmauscollege/arcade)<br>
and would never have come to life without the hard work of [Spookie6](https://github.com/Spookie6) and [Fabstershu](https://github.com/Fabsterschu)

# werkafspraken

-   code alleen aan de main-branche toevoegen als hij runt en leesbaar is
-   altijd documentatie (readme) aanpassen tegelijk met je code
-   maak incidenten aan en assign die aan jezelf, zodat iedereen ziet waaraan je werkt

# files

`keymapping.*`<br>
Mapping of joysticks and buttons on the arcade console to keys on the keyboard emulator attached to the raspberry pi.

`install-arcade.sh*`<br>
Installs/updates the arcade files onto the pi 5

# startup guide

To initialize the startup files, you'll have to download the file called `install-arcade.sh` enter terminal and make a directory called "Arcade". This is done by entering `mkdir Arcade`. Now type `mv Downloads/install-arcade.sh ~/Arcade`. To make sure the file is executable type `chmod +x ~/Arcade/install-arcade.sh`. To make it run on startup, create a file named `install-arcade.desktop` in the autostart directory using: `sudo nano ~/.config/autostart/install-arcade.desktop`. Now type:

```
[Desktop Entry]
Type=Application
Name=Start Arcade
Exec=lxterminal -e "bash ~/Arcade/install-arcade.sh"
Terminal=true
```

## test in a Codespace
-   Start a Codespace
-   Run `python ./menu/main.py` in the terminal to start
-   Type CTRL+C keys in the terminal to stop the menu or game
