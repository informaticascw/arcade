#!/bin/bash

echo "Checking for internet connection..."

#Testing internet connectivity until connected at 10 second intervals
ONLINE=1
while [ $ONLINE -ne 0 ]
do
#Pinging a frequently used google DNS server
	ping -c 1 8.8.8.8 > /dev/null 2>&1
	ONLINE=$?
	if [ $ONLINE -ne 0 ]
	then
		echo "Couldn't establish an internet connection."
		sleep 10
	fi
done
echo "Internet Connected!"

echo "Downloading files..."
sudo apt install wget unzip

wget https://github.com/leerlingenscw/2425-arcade/archive/refs/heads/main.zip
rm -rf ~/Arcade/2425-arcade-main
unzip -o ~/main.zip  -d ~/Arcade/
rm -rf ~/main.zip
bash ~/Arcade/2425-arcade-main/watchdog.sh
# python ~/Arcade/2425-arcade-main/src/games/flappybird/main.py


read -p "Press [Enter] to close..."
