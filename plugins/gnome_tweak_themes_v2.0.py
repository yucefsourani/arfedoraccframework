#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#  Copyright 2017 youcef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import os
import sys
import pwd
import threading
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GdkPixbuf, Pango, GLib
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location
from arfedoraccframework.basegnome import gsetting_make_change
from arfedoraccframework.widgetsutils import TooltipWindow

desktop=os.getenv("XDG_CURRENT_DESKTOP")

button_label         = _("Gnome Tweak Themes")
button_image         = "gnome.svg"
category             = _("Utilities")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Gnome Tweak Themes")
blockclose           = False
if_true_skip         = not os.path.isfile("/usr/bin/dnf")
if_false_skip        = True if "GNOME" in desktop else False
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "preferences-desktop-personal"

"""mac_extensions_to_enable = ["user-theme@gnome-shell-extensions.gcampax.github.com",
                            "clipboard-indicator@tudmotu.com",
                            "CoverflowAltTab@dmo60.de",
                            "dash-to-dock@micxgx.gmail.com",
                            "drive-menu@gnome-shell-extensions.gcampax.github.com",
                            "EasyScreenCast@iacopodeenosee.gmail.com",
                            "simplenetspeed@biji.extension",
                            "background-logo@fedorahosted.org"]"""

             
mac_extensions_to_enable = ["user-theme@gnome-shell-extensions.gcampax.github.com",
                            "clipboard-indicator@tudmotu.com",
                            "CoverflowAltTab@dmo60.de",
                            "dash-to-dock@micxgx.gmail.com",
                            "drive-menu@gnome-shell-extensions.gcampax.github.com",
                            "simplenetspeed@biji.extension",
                            "background-logo@fedorahosted.org"]
                            

mac_gsettings = [ ["org.gnome.desktop.background"          , "show-desktop-icons",GLib.Variant('b',False)] ,
			    ["org.gnome.desktop.background"           , "picture-uri",GLib.Variant('s',"file:///usr/share/backgrounds/arfedora/Anderson_4K_Abstract_Wallpaper.jpg")] ,
			    ["org.gnome.desktop.screensaver"          , "picture-uri",GLib.Variant('s',"file:///usr/share/backgrounds/arfedora/Anderson_4K_Abstract_Wallpaper.jpg")] ,
			    ["org.gnome.desktop.interface"            , "icon-theme",GLib.Variant('s',"macOS")] ,
			    ["org.gnome.shell.extensions.user-theme"  , "name",GLib.Variant('s',"Ant")] ,
			    ["org.gnome.desktop.interface"            , "gtk-theme",GLib.Variant('s',"Ant")] ,
			    ["org.gnome.desktop.interface"            , "enable-animations",GLib.Variant('b',True)] ,
			    ["org.gnome.desktop.wm.preferences"       , "button-layout",GLib.Variant('s',":minimize,close")] ,
			    ["org.gnome.desktop.interface"            , "cursor-theme",GLib.Variant('s',"Breeze_Snow")] ,
			    ["org.gnome.Terminal.Legacy.Settings"     , "theme-variant",GLib.Variant('s',"light")] ,
			    ["org.gnome.Terminal.Legacy.Settings"     , "default-show-menubar",GLib.Variant('b',False)]]

			
mac_gnome_terminal = [[ "use-theme-colors" , GLib.Variant('b',False)] ,
                      [ "use-system-font" , GLib.Variant('b',False)] ,
                      [ "background-color" , GLib.Variant('s',"#FFFFFF")] ,
                      [ "font" , GLib.Variant('s',"Monospace 15")] ,\
                      [ "foreground-color" , GLib.Variant('s',"#5940BF")] ,
                      [ "cursor-background-color" , GLib.Variant('s',"#EF2929")] ,
                      [ "cursor-colors-set" ,GLib.Variant('b',True)] ,
                      [ "background-transparency-percent" , GLib.Variant('i',5)] ,
                      [ "use-transparent-background" , GLib.Variant('b',True)]
                    ]
                    


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self.tooltipwindow=False
        self._mainbox_.set_border_width(5)
        self._mainbox_.set_spacing(20)
        headericon   = get_icon_location("GnomeLogoHorizontal.svg")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>Gnome Tweak Themes</b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        self._mainbox_.pack_start(headerbox,False,False,0)
        vseparator = Gtk.Separator()
        vseparator.set_margin_top(10)
        self._mainbox_.pack_start(vseparator,False,False,0)

        machbox = Gtk.HBox(spacing=20)
        self._mainbox_.pack_start(machbox,False,False,0)
        button_mac_vbox = Gtk.VBox(spacing=1)
        pixbufmac=GdkPixbuf.Pixbuf.new_from_file_at_size(get_icon_location("Screenshot from 2017-11-17 15-56-12.jpg"),500,400)
        imagemac = Gtk.Image.new_from_pixbuf(pixbufmac)
        label_mac = Gtk.Label("Ant")
        button_mac = Gtk.Button()
        button_mac.connect("clicked",self.on_button_clicked,mac_extensions_to_enable,mac_gsettings,mac_gnome_terminal)
        button_mac_vbox.pack_start(imagemac,False,False,0)
        button_mac_vbox.pack_start(label_mac,False,False,0)
        button_mac.add(button_mac_vbox)
        machbox.pack_start(button_mac,True,False,0)
        



    def on_button_clicked(self,button,extensions_to_enable=False,gsettings=False,gsettings_profile=False,default_terminal_profile=False,speed=1):
        t = threading.Thread(target=self.make_change,args=(extensions_to_enable,gsettings,gsettings_profile,default_terminal_profile,speed))
        t.start()
        
    def make_change(self,extensions_to_enable,gsettings,gsettings_profile,default_terminal_profile,speed):
        GLib.idle_add(self._parent_.set_sensitive,False)
        gsetting_make_change(extensions_to_enable,gsettings,gsettings_profile,default_terminal_profile,speed)
        GLib.idle_add(self._parent_.set_sensitive,True)
        
        
