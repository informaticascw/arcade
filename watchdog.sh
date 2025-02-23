#!/bin/bash

cd ~/Arcade/2425-arcade-main

find_keyboard_device() {
	grep -E -A 5 "Keyboard" /proc/bus/input/devices | grep -oE "event[0-9]+" | head -n 1
}

KEYBOARD_DEVICE="/dev/input/$(find_keyboard_device)"

echo "keyboard: $KEYBOARD_DEVICE"

if [ -z "$KEYBOARD_DEVICE" ]; then
	echo "Couldn't find an attached keyboard device"
 	exit 1
fi

PYTHON_SCRIPT="src/menu/main.py"

python "$PYTHON_SCRIPT" &

restart_menu() {
	if pgrep -f "$PYTHON_SCRIPT" > /dev/null; then
		pkill -f "$PYTHON_SCRIPT"
		sleep 1
	fi
	python3 "$PYTHON_SCRIPT" &
}

sudo evtest "$KEYBOARD_DEVICE" | while read line; do
	if echo "$line" | grep -q "KEY_1" && echo "$line" | grep -q "value 1"; then
		restart_menu
	fi
done
