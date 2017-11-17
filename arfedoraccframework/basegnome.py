#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  
#  Copyright 2017 youcefsourani <youssef.m.sourani@gmail.com>
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
from subprocess import check_output,call
import sys
from pwd import getpwuid
import os
import gi
from gi.repository import Gio,GLib
import dbus
from time import sleep




home = getpwuid(os.geteuid()).pw_dir


mac_extensions_to_enable = ["user-theme@gnome-shell-extensions.gcampax.github.com",
                            "clipboard-indicator@tudmotu.com",
                            "CoverflowAltTab@palatis.blogspot.com",
                            "dash-to-dock@micxgx.gmail.com",
                            "drive-menu@gnome-shell-extensions.gcampax.github.com",
                            "EasyScreenCast@iacopodeenosee.gmail.com",
                            "simplenetspeed@biji.extension"]

             
       

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
                      [ "background-transparency-percent" , GLib.Variant('i',20)] ,
                      [ "use-transparent-background" , GLib.Variant('b',True)]
                    ]
			
class GnomeShell(object):
	def __init__(self,list_setting):
		self.__list_setting           = list_setting
		self.__bus                    = dbus.SessionBus()
		self.__id                     = "org.gnome.Shell"
		self.__object                 = "/org/gnome/Shell"
		self.__interface_properties   = "org.freedesktop.DBus.Properties"
		self.__interface_extensions   = "org.gnome.Shell.Extensions"
		self.__proxy                  = self.__bus.get_object(self.__id,self.__object)
		self.__interface_p            = dbus.Interface(self.__proxy,self.__interface_properties)
		self.__interface_e            = dbus.Interface(self.__proxy,self.__interface_extensions)
		self.__settings = Gio.Settings(schema='org.gnome.shell')
		self.__settings.delay()
		self.__settings.sync()
		self.__list_setting.append(self.__settings)
		
	def version(self):
		return self.__interface_p.Get(self.__interface_extensions,"ShellVersion")
	
	def list_extensions(self):
		result = {}
		for k,v in self.__interface_e.ListExtensions().items():
			result.setdefault(k,True if v["state"]==1.0 else False)
		return result
		
	def list_enabled_extensions(self):
		result = []
		for k,v in self.__interface_e.ListExtensions().items():
			if v["state"]==1.0:
				result.append(k)
		return result

	def list_disabled_extensions(self):
		result = []
		for k,v in self.__interface_e.ListExtensions().items():
			if v["state"]!=1.0:
				result.append(k)
		return result
		
	def enable_extensions(self,extensions):
		ex = self.__settings.get_strv("enabled-extensions")
		for extension in extensions:
			if extension not in ex:
				ex.append(extension)

		self.__settings.set_strv("enabled-extensions", ex)

		
	def disable_extensions(self,extensions):
		ex = self.__settings.get_strv("enabled-extensions")
		for extension in extensions:
			while extension  in ex:
				ex.remove(extension)
		self.__settings.set_strv("enabled-extensions", ex)
		


def remove_extension_from_home(name):
    l = os.path.join(home,".local/share/gnome-shell/extensions",name)
    if os.path.isdir(l):
        call("rm -rf "+l,shell=True)
	
def gsetting_make_change(extensions_to_enable=False,gsettings=False,gsettings_profile=False,default_terminal_profile=False,speed=0.5,remove_extension_from_h=True):
    if not default_terminal_profile:
        default_gnome_terminal_profile=eval(check_output("gsettings get org.gnome.Terminal.ProfilesList list",shell=True).decode("utf-8").strip())[0]
    else:
        default_gnome_terminal_profile=default_terminal_profile

    list_setting = []
    
    if extensions_to_enable:
        gnome = GnomeShell(list_setting)
        gnome.disable_extensions(gnome.list_extensions().keys())
        if remove_extension_from_h:
            for ext in extensions_to_enable:
                remove_extension_from_home(ext)
        gnome.enable_extensions(extensions_to_enable)

    if gsettings:
	    for i in gsettings:
		    setting = Gio.Settings(i[0])
		    setting.delay()
		    setting.sync()
		    list_setting.append(setting)
		    setting.set_value(i[1],i[2])
		
    if gsettings_profile:
	    setting = Gio.Settings.new_with_path("org.gnome.Terminal.Legacy.Profile","/org/gnome/terminal/legacy/profiles:/:{}/".format(default_gnome_terminal_profile))
	    setting.delay()
	    setting.sync()
	    list_setting.append(setting)
	    for m in gsettings_profile:
		    setting.set_value(m[0],m[1])
		
		
    for s in list_setting:
        sleep(speed)
        s.apply()

