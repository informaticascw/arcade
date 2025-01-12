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

To initialize the startup files, you'll have to download the file called `arcade-install.sh` enter terminal and make a directory called "Arcade" by entering `mkdir Arcade`. Now type `mv Downloads/arcade-install ~/Arcade`, then `nano ~/.config/labwc/init` and lastly `lxterminal -e ~/Arcade/arcade-install.sh`. Once you've done this press Ctrl + O, Enter, Ctrl + X to to save and quit. You can now reboot the pi 5 and it should configure itself.
