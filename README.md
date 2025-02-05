# arcade

This repository will be used to make the code for an arcade running python games.

It is inspired on the arcade running javascript games at [https://github.com/emmauscollege/arcade](https://github.com/emmauscollege/arcade)

# werkafspraken
- code alleen aan de main-branche toevoegen als hij runt en leesbaar is
- altijd documentatie (readme) aanpassen tegelijk met je code
- maak incidenten aan en assign die aan jezelf, zodat iedereen ziet waaraan je werkt

# files
`keymapping.*`<br>
Mapping of joysticks and buttons on the arcade console to keys on the keyboard emulator attached to the raspberry pi.

`install-arcade.sh*`<br>
Installs/updates the arcade files onto the pi 5

# startup guide

Create a file named autostart using: `sudo nano ~/.config/autostart/install-arcade.desktop`. Now type:
`[Desktop Entry]
Type=Application
Name=Start Arcade
Exec=lxterminal -e "bash /home/arcade/install-arcade.sh"
Terminal=true`
