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
import os
from gi.repository import GLib


authors_ = ["Youssef Sourani <youssef.m.sourani@gmail.com>"]
version_ = "3.3"
copyright_ ="Copyright © 2017 Youssef Sourani"
comments_ = "ArControlCenter"
website_ = "https://arfedora.blogspot.com"
translators_ = ("translator-credit")
appname = "arfedoracontrolcenter"
appwindowtitle       = "ArControlCenter"
appid="org.github.yucefsourani.ArControlCenter"
icon_ =  "/usr/share/pixmaps/{}.png".format(appid)
mainbuttonsizewidth      = 50
mainbuttonsizeheight     = 50
maxwidgetinrow           = 5
mainbuttonbold           = True
category_icon_theme_size = 32
category_icon_theme_flag = 16

#dont change this
homeconfig = GLib.get_user_config_dir()+"/"+appname
homedata   = GLib.get_user_data_dir()+"/"+appname
os.makedirs(homedata,exist_ok=True)
os.makedirs(homeconfig,exist_ok=True)

