#!/bin/bash

KEYBOARD_DEVICE="/dev/input/event5"
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
