# -*- coding: utf-8 -*-
# Configuration file for Qtile
# Author: Eyal Schuller
# Date: December 26, 2021

from typing import List  # noqa: F401

from scripts import storage

import os
import subprocess
from libqtile import qtile, bar, layout, hook, widget
from libqtile.config import Click, Drag, Key, Match, Group, Screen
from libqtile.lazy import lazy

HOME = os.environ['HOME']
COLORS_CACHE = HOME + '/.cache/wal/colors'

mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Launch terminal and dmenu
    Key([mod, "shift"], "Return", lazy.spawn("dmenu_run -p 'Run: '"),
        desc="Run dmenu launcher"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

# Run at start
@hook.subscribe.startup
def start_once():
    start_script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.call([start_script])

#@hook.subscribe.startup_once
#def start_always():
#    # fixes the cursor
#    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])



# Colors
def load_colors(cache):
    with open(cache, 'r') as f:
        colors = f.read().split()[:8]
    colors.append('#ffffff')
    lazy.reload()
    return colors
colors = load_colors(COLORS_CACHE)


# custom workspace names and initialization
def init_group_names():
    return [("", {"layout": "monadtall"}),     # Terminals
            ("", {"layout": "monadtall"}),     # Web Browser
            ("", {"layout": "monadtall"}),     # File Manager
            ("", {"layout": "monadtall"}),     # Text Editor
            ("", {"layout": "monadtall"}),     # Media/zoom
            ("漣", {"layout": "monadtall"}),    # Settings
            ("", {"layout": "monadtall"}),     # Music
            ("", {"layout": "monadtall"}),     # Mail
            ("", {"layout": "monadtall"})]     # Messages/Slack

def init_groups(group_names):
    return [Group(name, **kwargs) for name, kwargs in group_names]

if __name__ in ["config", "__main__"]:
    group_names = init_group_names()
    groups = init_groups(group_names)

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group


##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 2,
                "margin": 8,
                "font": "Source Code Pro Medium",
                "font_size": 10,
                "border_focus": colors[4],
                "border_normal": colors[1]
                }


# window layoyts
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
    layout.Stack(num_stacks=2, **layout_theme),
    layout.Bsp(**layout_theme),
    layout.Tile(**layout_theme),

    # Try more layouts by unleashing below layouts.
    # layout.Columns(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

### Widgets
def icon(nerdfont_icon, fg_color):
    return widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = nerdfont_icon,
                foreground = fg_color)

def wid(w):
    return {
        'sep':widget.Sep(
                        size_percent = 60,
                        padding = 15,
                        linewidth = 2,
                        foreground = "#555555"),
        'group_box':widget.GroupBox(
                        font = "Iosevka Nerd Font",
                        fontsize = 15,
                        foreground = colors[-1],
                        borderwidth = 4,
                        highlight_method = "text",
                        this_current_screen_border = colors[5],
                        active = colors[3],
                        inactive = colors[-1]),
        'battery':widget.Battery(
                        foreground = colors[-1],
                        format = "{percent:2.0%}"),
        'brightness':widget.Backlight(
                        foreground = colors[-1],
                        backlight_name = "intel_backlight", # name of backlight obtained with brightnessctl command
                        change_command = "brightnessctl s {0}%",
                        step = 5),
        'volume':widget.Volume(foreground = colors[-1]),
        'current_layout':widget.CurrentLayout(foreground = colors[-1]),
        'cpu':widget.CPU(
                        format = "{load_percent}%",
                        foreground = colors[-1],
                        update_interval = 2,
                        mouse_callbacks = {
                            'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                        }),
        'memory':widget.Memory(
                        format = "{MemUsed:.0f}{mm}",
                        foreground = colors[-1],
                        update_interval = 2,
                        mouse_callbacks = {
                            'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                        }),
        'disk_space':widget.GenPollText(
                        foreground = colors[-1],
                        update_interval = 5,
                        func = lambda: storage.diskspace('FreeSpace'),
                        mouse_callbacks = {
                            'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                        }),
        'num_updates':widget.CheckUpdates(foreground = colors[-1]),
        'internet':widget.Wlan(
                        interface = "wlp4s0",
                        foreground = colors[-1],
                        mouse_callbacks = {
                            'Button1': lambda: subprocess.call(['networkmanager_dmenu', '-l', '15'])
                        }
        ),
        'bluetooth':widget.Bluetooth(foreground = colors[-1]),
        'clock':widget.Clock(format = '%b %d, %Y  -  %H:%M ')
    }[w]

widget_defaults = dict(
    font='Source Code Pro Medium',
    fontsize=12,
    padding=5,
)
extension_defaults = widget_defaults.copy()

def init_widget_list():
    space = widget.Spacer(length = 5)
    widget_list = [
        space,
        wid('group_box'),
        wid('sep'),
        icon(' ', colors[6]),
        wid('current_layout'),

        widget.Spacer(),

        wid('clock'),

        widget.Spacer(),

        widget.WidgetBox(widgets = [
            icon(" ﬙ ",colors[7]),
            wid('cpu'),
            icon("  ",colors[4]),
            wid('memory'),
            icon("  ",colors[6]),
            wid('disk_space'),
            icon("  ",colors[5]),
            wid('num_updates')
        ]),
        wid('sep'),
        icon(' ',colors[4]),
        wid('internet'),
        icon('  ',colors[7]),
        wid('bluetooth'),
        icon(" 墳",colors[5]),
        wid('volume'),
        icon("  ",colors[6]),
        wid('brightness'),
        icon("  ",colors[7]),
        space
    ]
    return widget_list

# screens/bar
def init_screens():
    screen = Screen(top=bar.Bar(
                widgets=init_widget_list(),
                background = colors[0],
                size=35,
                opacity=0.7,
                margin=[3,5,0,5]
    ))
    return [screen]




screens = init_screens()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# assign apps to groups/workspace
#@hook.subscribe.client_new
#def assign_app_group(client):
#    d = {}

    # assign deez apps
    #d[group_names[0][0]] = ['Alacritty', 'xfce4-terminal']
    #d[group_names[1][0]] = ['Navigator', 'discord', 'brave-browser', 'midori', 'qutebrowser']
    #d[group_names[2][0]] = ['pcmanfm', 'thunar']
    #d[group_names[3][0]] = ['code', 'geany']
    #d[group_names[4][0]] = ['vlc', 'obs', 'mpv', 'mplayer', 'lxmusic', 'gimp']
    #d[group_names[5][0]] = ['spotify']
    #d[group_names[6][0]] = ['lxappearance', 'gpartedbin', 'lxtask', 'lxrandr', 'arandr', 'pavucontrol', 'xfce4-settings-manager']

    #wm_class = client.window.get_wm_class()[0]
    #for i in range(len(d)):
    #    if wm_class in list(d.values())[i]:
    #        group = list(d.keys())[i]
    #        client.togroup(group)
    #        client.group.cmd_toscreen(toggle=False)


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
