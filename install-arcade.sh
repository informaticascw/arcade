#!/bin/bash

echo "Checking for internet connection..."

#Testing internet connectivity until connected at 10 second intervals
ONLINE=1
TRIES=0

start_with_internet() {
	sudo apt install -y wget unzip
	wget https://github.com/informaticascw/arcade/archive/refs/heads/main.zip
	rm -rf ~/Arcade/arcade-main
	unzip -o ~/main.zip  -d ~/Arcade/
	rm -rf ~/main.zip
}

while [ $ONLINE -ne 0 ]
do
	TRIES=$((TRIES + 1))
	#Pinging a frequently used google DNS server
	ping -c 1 8.8.8.8 > /dev/null 2>&1
	ONLINE=$?
	if [ $ONLINE -ne 0 ]
	then
 		if [ $TRIES \> 2 ] 
		then
   			echo "No internet was found within 3 attempts"
      			echo "Starting Arcade without internet..."
	 		break 1
	 	else
			echo "Couldn't establish an internet connection, trying again after 10 seconds"
			sleep 10
   		fi
	fi
done
if [ $ONLINE -eq 0 ]
then
	echo "Internet Connected!"
	echo "Downloading and updating Arcade..."
 	start_with_internet
fi

bash ~/Arcade/arcade-main/watchdog.sh


read -p "Press [Enter] to close..."
