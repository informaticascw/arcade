#!/bin/bash

echo "Checking for internet connection..."

#Testing internet connectivity until connected at 1 minute intervals
ONLINE=1
while [ $ONLINE -ne 0 ]
do
#Pinging a frequently used google DNS server
	ping -c 1 8.8.8.8 > /dev/null 2>&1
	ONLINE=$?
	if [ $ONLINE -ne 0 ]
	then
		echo "Couldn't establish an internet connection."
		sleep 60
	fi
done
echo "Internet Connected!"
#The rest of the code
sleep(5)
