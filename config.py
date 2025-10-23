# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration, RectDecoration


power = os.path.expanduser('~/.config/qtile/powermenu')
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call(home)

mod = "mod4"
terminal = guess_terminal()
alt = "mod1"
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "c", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    #Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "Tab", lazy.spawn('rofi -show window')),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    #Key([mod], "space", lazy.spawn('dmenu_run -l 15 -nb "#282828" -p "Run:" -sb "#d79921" -sf "#282828"')),
    Key([mod], "space", lazy.spawn('rofi -show drun')),
    Key([mod], "e", lazy.spawn('thunar')),
    Key([mod],"Print",lazy.spawn('screengrab')),
    Key([mod],"p", lazy.spawn(power)),
    Key([alt], "Shift_L",  lazy.widget["keyboardlayout"].next_keyboard()),
    Key([mod], "b", lazy.spawn('brave')),
    Key([mod], "s", lazy.spawn('spotify')),
    Key([mod, "shift"], "e", lazy.spawn('emacs')),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


#groups = [Group(i) for i in "123456789"]



#groups = [
    #Group("1"),
    #Group("2"),
    #Group("3", matches=[Match(wm_class=["qutebrowser"])]),
    #]



groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

group_labels = ["", "", "", "", "", "", "", "", ""]
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]




for i in range(len(group_names)):
    groups.append(

        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],

        ))

@hook.subscribe.client_new
def assign_app_group(client):
    wm_class = client.window.get_wm_class()
    if wm_class in [['brave-browser', 'Brave-browser']]:
        client.togroup("2")
        client.group.cmd_toscreen()
    elif wm_class in [['telegram-desktop', 'TelegramDesktop']]:
        client.togroup("3")
        client.group.cmd_toscreen()
    elif wm_class in [['emacs', 'Emacs']]:
        client.togroup("1")
        client.group.cmd_toscreen()
    elif wm_class in [['steamwebhelper','steam']]:
        client.togroup("4")
        client.group.cmd_toscreen()
    elif wm_class in [['spotify', 'Spotify']]:
        client.togroup("5")

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
color7 = "#81c8be"
layout_theme = {"border_width": 3,
                "margin": 10,
                "border_focus":color_fg_base,
                "border_normal": bg
                }



layouts = [
    layout.Columns(
        #border_width=2,
        #border_focus = "#5e81ac",
        #border_normal = "#4c556a",
        **layout_theme
    ),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Tile(**layout_theme),
    layout.Max(**layout_theme),

    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()
#bg = "#232634"
#bg = "#6c6f85"
bg = "#181825"
#color1 = "#f4b8e4"
#color2 = "#ca9ee6"
#color3 = "#ea999c"
#color4 = "#e5c890"
#color5 = "#a6d189"
#color6 = "#689d6a"
##color7 = "#81c8be"
#color8 = "#ef9f76"
color9 = "#f9e2af"
fg1 = "#c6d0f5"
color_fg_base = "#fdefcc"

widget_defaults = dict(
    #font="JetBrains Mono Medium",
    font = "JetBrains Mono Bold",
    fontsize = 14,
    padding = 20,
)



screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.Spacer(length=4),

                widget.GroupBox(
                    margin_x=20,
                    fontsize = 15,
                    borderwidth = 0,
                    padding_x = 0,
                    active = "#c6ac70",
                    inactive = "#fdefcc",
                    this_screen_border = color4,
                    other_current_screen_border = color7,
                    other_screen_border = color4,
                    highlight_color = bg,
                    highlight_method = "text",
                    this_current_screen_border = color8,
                    block_highlight_text_color = color8,
                    #background = bg,
                    radius = True,
                    decorations=[
                        RectDecoration(
                            colour=bg,
                            radius=10,
                            filled=True,
                        )
                    ],
                ),
                #widget.Prompt(foreground=color8),
                #

                widget.Spacer(length=6),
                widget.WindowName(
                    format='{state}{name}',
                    width =300,
                    empty_group_string="",
                    scroll=True,
                    padding=13,
                    foreground =  bg,
                    decorations=[
                        RectDecoration(
                            colour=color9,
                            radius=10,
                            filled=True,
                        )
                    ],


                ),
                #widget.CheckUpdates(
                 #   foreground =color1,
                  #  colour_have_updates =color1,
                   # colour_no_updates = color1,
                    #distro = 'Arch_checkupdates',
                    #update_interval = 60,
                    #display_format = '󰮯  {updates}',
                    #no_update_string='󰚰 none',
                     #decorations=[
                      #  RectDecoration(
                       #     colour=bg,
                        #    radius=10,
                         #   filled=True,
                          #  )
                          #],
                          #),
                widget.Spacer(lenght=10),
                widget.Clock(
                    foreground = color9,
                    format = "%a %d, %b %Y",
                     decorations=[
                        RectDecoration(
                            colour=bg,
                            radius=[10,0,0,10],
                            filled=True,
                        )
                    ],
                 ),
                widget.Clock(
                    format  = "%H:%M:%S",
                    foreground = bg,
                    decorations=[

                        RectDecoration(
                            colour=color9,
                            radius=[0,10,10,0],
                            filled=True,
                        )
                    ],

                ),

                widget.Spacer(leght=bar.STRETCH),
                widget.KeyboardLayout(
                    foreground =  color_fg_base,
                    fmt = '  {}',
                    padding=13,
                    configured_keyboards=['us','ru'],
                     decorations=[
                        RectDecoration(
                            colour= bg,
                            radius=10,
                            filled=True,
                        )
                    ],
                 ),

                widget.Spacer(length=6),
                widget.CPU(
                    format = ' {load_percent}%',
                    foreground =   color_fg_base,
                    padding=13,
                     decorations=[
                        RectDecoration(
                            colour=bg,
                            radius=10,
                            filled=True,
                        )
                    ],
                ),
                widget.Spacer(length=6),
                widget.DF(
                    update_interval = 60,
                    foreground =  color_fg_base,
                    padding = 13,
                    partition = '/home',
                    format = '{uf}{m}',
                    fmt = ' {}',
                    visible_on_warn = False,
                     decorations=[
                        RectDecoration(
                            colour=bg,
                            radius=10,
                            filled=True,
                        )
                    ],
                 ),
                widget.Spacer(length=6),
                widget.Volume (
                     foreground =  color_fg_base,
                     padding = 13,
                     fmt = '  {}',
                     step = 5,
                     decorations=[
                        RectDecoration(
                            colour=bg,
                            radius=10,
                            filled=True,
                        )
                    ],

                 ),

                widget.Spacer(length=6),
                widget.Net(
                    interface = "enp6s0",
                    format='󰈀 {down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}',
                    foreground =  color_fg_base,
                    padding=13,
                     decorations=[
                        RectDecoration(
                            colour=bg,
                            radius=10,
                            filled=True,
                        )
                    ],
                ),
                


                widget.Systray(padding=10),

            ],
            35,
           
            background="#00000000",
            border_color="#00000000",
            border_width=[4, 8, 4, 8],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    border_focus = color_fg_base,
    border_normal = "4c556a"
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
