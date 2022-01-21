#!/bin/env bash

# set background and colorscheme
wal -R
feh --no-fehbg -bg-scale "$HOME/.conf/qtile/wallpaper.jpg"

# Kill if already running
killall -9 picom xfce4-power-manager dunst

# Launch notification daemon
dunst -config $HOME/.config/qtile/dunstrc &

# power manager and picom start
xfce4-power-manager &
picom --xrender-sync-fence --config $HOME/.config/qtile/picom.conf &

# start udiskie
udiskie &
