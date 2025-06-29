#!/bin/bash

cd ~/Arcade/arcade-main

find_keyboard_device() {
	grep -E -A 5 "Ultimarc|Keyboard" /proc/bus/input/devices | grep -oE "event[0-9]+" | head -n 1
}

KEYBOARD_DEVICE="/dev/input/$(find_keyboard_device)"

echo "keyboard: $KEYBOARD_DEVICE"

if [ -z "$KEYBOARD_DEVICE" ]; then
	echo "Couldn't find an attached keyboard device"
 	exit 1
fi

PYTHON_SCRIPT="src/menu/main.py"

python "$PYTHON_SCRIPT" &

close_all_games() {
    for pid in $(pgrep -f "python"); do
        if ! ps -p "$pid" -o cmd= | grep -q "$PYTHON_SCRIPT"; then
            kill -KILL "$pid"
        fi
    done
    sleep 0.5
}

restart_menu() {
	close_all_games
 
	if pgrep -f "$PYTHON_SCRIPT" > /dev/null; then
		pkill -KILL -f "$PYTHON_SCRIPT"
		sleep 1
	fi
	python3 "$PYTHON_SCRIPT" &
}

sudo evtest "$KEYBOARD_DEVICE" | while true; do
    if read -t 300 line; then  # if line read within 300 seconden
	if echo "$line" | grep -q "KEY_1" && echo "$line" | grep -q "value 1"; then
 		echo "KEY_1 pressed. Closing all games and restarting menu."
		restart_menu
	fi
 	if echo "$line" | grep -q "KEY_2" && echo "$line" | grep -q "value 1"; then
                echo "KEY_2 pressed. Closing all games."
		close_all_games
	fi
     else
        echo "No input for 5 minutes. Closing all games."
        close_all_games
     fi
done
