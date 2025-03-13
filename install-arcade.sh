#!/bin/bash

echo "Checking for internet connection..."

#Testing internet connectivity until connected at 10 second intervals
ONLINE=1
TRIES=0

start_with_internet() {
	sudo apt install wget unzip
	wget https://github.com/leerlingenscw/2425-arcade/archive/refs/heads/main.zip
	rm -rf ~/Arcade/2425-arcade-main
	unzip -o ~/main.zip  -d ~/Arcade/
	rm -rf ~/main.zip
}

while [ $ONLINE -ne 0 ]
do
#Pinging a frequently used google DNS server
	ping -c 1 8.8.8.8 > /dev/null 2>&1
	ONLINE=$?
	if [ $ONLINE -ne 0 ]
	then
 		if $TRIES >= 7 then
   			echo "No internet was found within a minute after starting up"
      			echo "Starting Arcade without internet..."
	 		break 1
	 	else
			echo "Couldn't establish an internet connection."
			sleep 10
	fi
done
if [ $ONLINE -ne 0 ]
then
	echo "Internet Connected!"
	echo "Downloading and updating Arcade..."
 	start_with_internet

bash ~/Arcade/2425-arcade-main/watchdog.sh


read -p "Press [Enter] to close..."
