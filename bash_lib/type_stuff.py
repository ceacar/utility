#!/usr/bin/env bash
pause_time=${1}
if [[ "$pause_time" ]];then
    echo "pause_time set to $pause_time"
else
    pause_time=30
fi

while true;do
    sleep_time=$(shuf -i 0-$pause_time -n 1)
    echo "sleeping $sleep_time"
    sleep $sleep_time
    rand_cmd=$(random_cmd.py)
    echo "[$(date)]$rand_cmd"
    delay_time=$(($sleep_time*10))
    echo "delay is $delay_time"
    xdotool type --delay $delay_time "$rand_cmd"
    xdotool key KP_Enter
done
